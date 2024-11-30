
# NED - Nuclear wastE Dss

## Overview
This project provides three main features: a Geometry (Domain Modeling) tool for simulating a radioactive process, Bayesian Analysis for assessing sensor and asset performance, and GSPN Models for advanced metric evaluation. 

### Key Process Description
- **Geometry Tool**: The domain modeling component allows for the simulation of a radioactive process that interacts with sensors and an Asset of Interest (AoI). The simulated process generates data that reflects the interactions of radioactive sources with these components.

- **Bayesian Analysis**: This module processes time series data from the radioactive source, sensors, and AoI, along with thresholds (for sensors) and tolerance levels (for the AoI). It evaluates whether sensor readings above a threshold correspond to values observed at the AoI. This analysis generates a Bayesian table that computes probabilities for various scenarios, enabling a posteriori mapping of the system's performance.

- **GSPN Models**: Starting from the scheduling, the computed probabilities, and the simulated process, the GSPN module calculates two metrics:
  1. **Mean Time Over Threshold (MToT)**: The average time during which values exceed a predefined threshold.
  2. **Increased Sensor Lifetime (ISL)**: A measure of the system's sustainability against the use of the sensors.

The tool is fully configurable through `configuration.ini`, `scheduler.ini`, `process.ini`, and `sensors.ini`, placed in `replication/`.

## Features
- **Geometry Modeling**: Simulates radioactive processes, sensing devices, Asset of Interest and their interactions.
- **Bayesian Analysis**: Computes posterior probabilities using time series data and thresholds.
- **GSPN Metric Evaluation**: Calculates MToT and ISL metrics based on system configurations.

## Directory Structure
- `main.py`: The main entry point for the project.
- `replication/`: Contains scripts and data for reproducing results.
- `bayes/`: Contains Bayesian analysis-related modules.
- `domain/`: Includes domain-specific models and utilities.
- `gspn_model/`: Utilities for Generalized Stochastic Petri Nets modeling.
- `output/`: Directory where outputs and results are stored.
- `repository/`: Contains auxiliary data or code repositories.
- `requirements.txt`: Lists dependencies for the project.
- `utils/`: Utility scripts and helper functions.

## Requirements
To run this project, you need the following dependencies, which are listed in `requirements.txt`. Install them using pip:

```bash
pip install -r requirements.txt
```

## Usage
1. Clone the repository.
2. Install dependencies using the command above.
3. Navigate to the `gspn_model` directory and run the following command to generate the necessary `.o` and `.so` files:

```bash
make
```

4. Run `main.py` to execute the primary workflow:

```bash
python main.py
```

## Output
Results from the scripts are saved in the `output/` directory. This includes logs, visualizations, or processed data.

## License
[Insert license information if applicable.]

## Contributions
Contributions are welcome! Please submit a pull request or open an issue for discussion.

## Contact
For further information or questions, contact {stefano.marrone, michele.digiovanni}@unicampania.it.
