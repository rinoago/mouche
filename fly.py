from flygym import Fly, Simulation, Camera, get_data_path
import numpy as np
from flygym.examples.common import PreprogrammedSteps

preprogrammed_steps =PreprogrammedSteps()
class MovingFly(Fly): #definition of our fly class
    def __init__(self, init_pose="stretch", actuated_joints=None, control="position",
                 initial_position=None, initial_orientation=None, obj_threshold=0.08, decision_interval=0.05, **kwargs):
        super().__init__(**kwargs, init_pose=init_pose, actuated_joints=actuated_joints, control=control,
                         spawn_pos=initial_position, spawn_orientation=initial_orientation, enable_vision=True)
        self.visual_inputs_hist = []
        self.standing=[] #joints angles to stand
        self.strech=[] #linespace to strech the elg
        self.mid_leg_end_effector=[] #init des end effector
        self.joint_record=[] #init des end effector
        self.fly_pos_hist=[] #history of position

        self.fly_joints_angles_30=[] #history of joints angles
        self.fly_joints_angles_28=[]
        self.fly_joints_angles_9=[]
        self.fly_joints_angles_7=[]
        self.fly_joints_angles_8=[]
        self.fly_joints_angles_31=[]
        self.mid_leg_end_effector_L=[]
        self.mid_leg_end_effector_R=[]

        self.obj_threshold = obj_threshold
        self.decision_interval = decision_interval
        self.num_substeps = int(self.decision_interval / 1e-4)
        self.visual_inputs_hist = []

        self.coms = np.empty((self.retina.num_ommatidia_per_eye, 2))

        for i in range(self.retina.num_ommatidia_per_eye):
            mask = self.retina.ommatidia_id_map == i + 1
            self.coms[i, :] = np.argwhere(mask).mean(axis=0)


            
    def process_visual_observation(self, vision_input): 
        # function to get the distance of the fly based on the size 
        features = np.zeros((2, 3))

        for i, ommatidia_readings in enumerate(vision_input):
            # Identify if readings correspond to an object
            is_obj = ommatidia_readings.max(axis=1) < self.obj_threshold
            is_obj_coords = self.coms[is_obj]

            if is_obj_coords.shape[0] > 0:
                # Compute the mean coordinates for detected objects
                features[i, :2] = is_obj_coords.mean(axis=0)
            
            # Store the number of detected object coordinates (area) in features[i, 2]
            features[i, 2] = is_obj_coords.shape[0]

        # Normalize the y_center and x_center
        features[:, 0] /= self.retina.nrows  # normalize y_center
        features[:, 1] /= self.retina.ncols  # normalize x_center

        # Normalize the area by the number of ommatidia per eye
        features[:, 2] /= self.retina.num_ommatidia_per_eye  # normalize area

        # Flatten the features array and convert to float32
        return features.ravel().astype("float32")


    
    def simulate_step(self, sim: Simulation, roll_angle: float, yaw_angle: float, side: str='L'):
        action = {"joints": self.simulate_movement(sim, roll_angle, yaw_angle, side)}
        if side =='L':
            action["adhesion"] = np.array([1,0,1,1,1,1]) #add adhesion 
        else:
            action["adhesion"] = np.array([1,1,1,1,0,1]) #add adhesion 
        return action

    def simulate_movement(self, sim: Simulation, roll_angle: float, yaw_angle: float, side: str, increment: float = 0.00015,):
        joint_pos = self.standing.copy()

        joint_angles = preprogrammed_steps.get_joint_angles("LM" if side == "L" else "RM", 0)

        if side == "L":
            joint_pos[7:14] = joint_angles + self.strech
            joint_pos[9], joint_pos[7] = roll_angle, yaw_angle  # Setting specific yaw and pitch
        else:
            joint_pos[28:35] = joint_angles + self.strech
            joint_pos[30], joint_pos[28] = roll_angle, yaw_angle

        self.record_mov(sim, side, joint_pos)
        return joint_pos

    def record_mov(self, sim: Simulation, side: str, joint_pos):
        observation = self.get_observation(sim)
        end_effector = observation["end_effectors"]
        if side=='L': self.mid_leg_end_effector.append([end_effector[1,:]])
        else : self.mid_leg_end_effector.append([end_effector[4,:]])
        self.fly_pos_hist.append(observation["fly"])
        self.joint_record.append(joint_pos)

    def record_joints(self):
        #record joints angles
        joint_pos = self.standing.copy()
        self.fly_joints_angles_30.append(joint_pos[30])
        self.fly_joints_angles_28.append(joint_pos[28])
        self.fly_joints_angles_9.append(joint_pos[9])
        self.fly_joints_angles_7.append(joint_pos[7])
        self.fly_joints_angles_8.append(joint_pos[8])
        self.fly_joints_angles_31.append(joint_pos[31])

    def record_general(self, sim: Simulation):
        observation = self.get_observation(sim)
        end_effector = observation["end_effectors"]
        self.mid_leg_end_effector_L.append([end_effector[1,:]])
        self.mid_leg_end_effector_R.append([end_effector[4,:]])
        #self.fly_pos_hist.append(observation["fly"])
        self.record_joints()