import pickle
import numpy as np
from scipy.interpolate import CubicSpline
from flygym.util import get_data_path
from flygym.examples.cpg_controller import CPGNetwork
from flygym.preprogrammed import get_cpg_biases


dofs_per_leg = [
            "Coxa",
            "Coxa_roll",
            "Coxa_yaw",
            "Femur",
            "Femur_roll",
            "Tibia",
            "Tarsus1",
        ]


intrinsic_freqs = np.ones(6) * 12
intrinsic_amps = np.ones(6) * 1
phase_biases = np.pi * np.array(
    [
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
        [0, 1, 0, 1, 0, 1],
        [1, 0, 1, 0, 1, 0],
    ]
)
coupling_weights = (phase_biases > 0) * 10
convergence_coefs = np.ones(6) * 1000


class Simulation_CPG:
    def __init__(self, timesteps=1e-4):
        # Load single steps data and retrieve necessary information
        self.single_steps_data = self.load_single_steps_data()
        self.preprogrammed_steps_length = len(self.single_steps_data["joint_LFCoxa"])
        self.preprogrammed_steps_timestep = self.single_steps_data["meta"]["timestep"]
        # Assert data consistency
        for k, v in self.single_steps_data.items():
            if k.startswith("joint_"):
                assert len(v) == self.preprogrammed_steps_length
                assert v[0] == v[-1]
                
        # Initialize legs and degrees of freedom
        self.legs = [f"{side}{pos}" for side in "LR" for pos in "FMH"]
        self.dofs_per_leg = dofs_per_leg
        self.psi_funcs = self.initialize_cubic_splines()
        self.swing_start, self.swing_end, self.psi_rest_phases = self.calculate_phases()

        self.cpg_network = CPGNetwork(
            timestep=timesteps,
            intrinsic_freqs=intrinsic_freqs,
            intrinsic_amps=intrinsic_amps,
            coupling_weights=coupling_weights,
            phase_biases=phase_biases,
            convergence_coefs=convergence_coefs,
            seed=1,
            )
        self.cpg_network.reset()
    
    @staticmethod
    def load_single_steps_data():
        single_steps_path = get_data_path("flygym", "data") / "behavior/single_steps_untethered.pkl"
        with open(single_steps_path, "rb") as f:
            init_single_steps_data = pickle.load(f)
        return init_single_steps_data
    
    def initialize_cubic_splines(self):
        phase_grid = np.linspace(0, 2 * np.pi, self.preprogrammed_steps_length)
        psi_funcs = {}
        for leg in self.legs:
            joint_angles = np.array(
                [self.single_steps_data[f"joint_{leg}{dof}"] for dof in self.dofs_per_leg]
            )
            psi_funcs[leg] = CubicSpline(phase_grid, joint_angles, axis=1, bc_type="periodic")
        return psi_funcs

    def calculate_phases(self):
        swing_start, swing_end = self.calculate_swing_phases()
        psi_rest_phases = (swing_end + 2 * np.pi) / 2
        return swing_start, swing_end, psi_rest_phases
    
    def calculate_swing_phases(self):
        swing_start = np.empty(6)
        swing_end = np.empty(6)
        for i, leg in enumerate(self.legs):
            swing_start[i] = self.single_steps_data["swing_stance_time"]["swing"][leg]
            swing_end[i] = self.single_steps_data["swing_stance_time"]["stance"][leg]
        swing_start /= self.preprogrammed_steps_length * self.preprogrammed_steps_timestep
        swing_start *= 2 * np.pi
        swing_end /= self.preprogrammed_steps_length * self.preprogrammed_steps_timestep
        swing_end *= 2 * np.pi
        return swing_start, swing_end

    def get_adhesion_onoff(self, theta):
        theta = theta % (2 * np.pi)
        return ~((theta > self.swing_start) & (theta < self.swing_end)).squeeze()

    def update(self, fly_joints):
        self.cpg_network.step()
        joints_angles = {}
        for i, leg in enumerate(self.legs):
            psi = self.psi_funcs[leg](self.cpg_network.curr_phases[i])
            psi_base = self.psi_funcs[leg](self.psi_rest_phases[i])
            adjusted_psi = psi_base + (psi - psi_base) * self.cpg_network.curr_magnitudes[i]
            for dof, angle in zip(self.dofs_per_leg, adjusted_psi):
                joints_angles[f"joint_{leg}{dof}"] = angle

        adhesion_onoff = self.get_adhesion_onoff(self.cpg_network.curr_phases)

        action = {
            "joints": np.array([joints_angles[dof] for dof in fly_joints]),
            "adhesion": adhesion_onoff.astype(int),
        }

        return action
    