# Middle-leg reaching behavior with NeuroMechFly

## Introduction

Welcome to our GitHub repository dedicated to exploring the neuromechanical control of Drosophila melanogaster behavior using NeuroMechFly.

Animals require a diverse set of adaptable behaviors to survive, often described using ethograms that detail distinct patterns observed in activities like mating, fighting, or defending specific territories. These behaviors are composed of specific, recognizable modules. While statistical analyses reveal the occurrence and transitions of these behaviors, their neurological basis remains unclear.

## Focus of Our Project

Our project investigates the territorial defense behavior of Drosophila, specifically the middle leg reaching movements used to sense and repel invaders. This behavior, which can occur without direct contact, involves intricate neuromechanical processes that are still not fully understood. Please refer to our final report to read all the researchs and detailed methods we have used in this code.

## NeuroMechFly

To study the neuromechanical aspects of Drosophila behavior, we use NeuroMechFly, an open-source, highly accurate digital model that replicates the fly's body morphology and joint dynamics. This model, combined with a central pattern generator (CPG) network, helps us explore how visual inputs translate into motor commands for adaptive behaviors.

## Project Objectives

1. **Simulate Fly Behavior**: Implement a scenario where a stationary 'main' fly reaches out with its middle leg towards a moving 'invading' fly.
2. **Visual Detection**: Explore how the main fly’s leg movements correspond to the invading fly’s movements within its visual field.
3. **Motor Control**: Investigate the transmission of sensory inputs to motor commands controlling the middle leg’s outward movement.
4. **Neuromechanical Insights**: Provide insights into the neural mechanisms behind these interactions, contributing to the broader understanding of neuromechanical control in Drosophila.

## How to Use This Repository
To begin with the course materials, ensure you have Git, conda, and the FlyGym Python package installed.

### **Install Dependencies**:
To be able to run this project, the new version of flygym is necessary: switch to the dev-v1.0.0 branch of the flygym repository.
```sh
git clone https://github.com/NeLy-EPFL/flygym.git flygym-v1
cd flygym-v1
git checkout dev-v1.0.0
conda create -y -n flygym-v1 python=3.11
conda activate flygym-v1
pip install -e ".[dev]"
```



### **Clone the Repository to your local machine**: 
```sh
git clone https://github.com/rinoago/mouche.git
```

### **Run Simulations**: 
Choose the flygym-v1 kernel.

Run the simulation using the `main.ipynb` file. It can take some time.
### **Analyze Results**: 
Use the provided analysis scripts to interpret the simulation data and visualize the fly’s behaviors.

## Contributions and References

Please read our `finalreport` file for more insights on our researchs, and a list of all the references used for this project. 

We would like to thank Professor Pavan Ramdya, Victor Alfred Stimpfling and Thomas Ka Chung Lam for their precious help in the realisation of this project.

[NeuroMechFly, a neuromechanical model of adult Drosophila melanogaster](https://www.nature.com/articles/s41592-022-01466-7)

[NeuroMechFly 2.0, a framework for simulating embodied sensorimotor control in adult Drosophila](https://www.biorxiv.org/content/10.1101/2023.09.18.556649v1)

## Contact

For any questions or issues, please open an issue on GitHub or contact us directly at [laetitia.wilhelm@epfl.ch], [hugo.masson@epfl.ch] or [theophine.gurlie@epfl.ch].

Thank you for your interest in our project! We hope this repository provides valuable insights into the fascinating world of Drosophila neuromechanics. 
