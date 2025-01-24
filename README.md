# Genetic Algorithm for Quadratic Assignment Problem (QAP)

## Introduction
This project solves the **Quadratic Assignment Problem (QAP)** using **Genetic Algorithms (GAs)**. The QAP is a combinatorial optimization problem with applications in facility layout, circuit design, and more. The goal is to minimize the total transportation cost by assigning facilities to locations based on given flow and distance matrices.

The implemented Genetic Algorithm includes variants to enhance performance and explore solution spaces effectively.

---

## Features

### Implemented Algorithms
- **Standard Genetic Algorithm**:
  - Evolves a population of candidate solutions through selection, crossover, and mutation.
  - Uses elitism to preserve the best solution in each generation.
  
- **Baldwinian Genetic Algorithm**:
  - Incorporates local search during fitness evaluation but does not directly modify individuals.
  - Encourages population learning while maintaining genetic diversity.
  
- **Lamarckian Genetic Algorithm**:
  - Incorporates local search results directly into the genetic material.
  - Accelerates convergence by inheriting "learned" traits in the population.

---

## How to Run

### Requirements
- Python 3.9 or later
- Dependencies listed in `requirements.txt`

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your_username/genetic-algorithm-qap.git
   cd genetic-algorithm-qap


Create and activate a virtual environment:

bash
Copiar
Editar
python -m venv venv
source venv/bin/activate  # For Unix/MacOS
.\venv\Scripts\activate   # For Windows
Install dependencies:

bash

pip install -r requirements.txt
Running the Algorithm
Basic Command
bash

python -m src.main --variant <algorithm_variant> --data <path_to_data> --output <output_directory> [options]
Example
bash
python -m src.main --variant standard --data data/raw/tai256c.dat --output results/standard_ga/ --population 300 --generations 500 --crossover_rate 0.8 --mutation_rate 0.02 --elitismo --seed 42

## Command-line Arguments

### Main Arguments
- `--variant`:  
  Specify the algorithm variant to use. Options:  
  - `standard`: Standard Genetic Algorithm.  
  - `baldwinian`: Baldwinian Genetic Algorithm.  
  - `lamarckian`: Lamarckian Genetic Algorithm.

- `--data`:  
  Path to the QAP data file (e.g., `data/raw/tai256c.dat`).

- `--output`:  
  Directory to save results and logs.

### Optional Parameters
- `--population`:  
  Size of the population. Default: `100`.

- `--generations`:  
  Number of generations. Default: `500`.

- `--crossover_rate`:  
  Probability of crossover between individuals. Default: `0.8`.

- `--mutation_rate`:  
  Probability of mutation in an individual. Default: `0.02`.

- `--elitismo`:  
  If included, ensures the best individual is carried forward to the next generation.

- `--seed`:  
  Seed for random number generation to ensure reproducibility of results.

---

## Description of Algorithms

### Standard Genetic Algorithm
1. **Initialization**:  
   A population of candidate solutions is generated randomly.

2. **Evolution**:  
   The population evolves over generations using:
   - **Tournament Selection**:  
     Parents are selected based on fitness comparisons.
   - **PMX Crossover (Partially Mapped Crossover)**:  
     Produces offspring by recombining parent solutions.
   - **Swap Mutation**:  
     Randomly swaps two genes in a chromosome to introduce diversity.

3. **Elitism**:  
   The best solution from the current generation is preserved for the next generation.

---

### Baldwinian Genetic Algorithm
1. **Local Search during Fitness Evaluation**:  
   Applies a local search heuristic to improve evaluation of individuals without altering their genetic structure.

2. **Learning**:  
   Encourages the population to learn indirectly from better evaluations, maintaining genetic diversity.

3. **Exploration vs. Exploitation**:  
   Balances the exploration of new solutions with the exploitation of known good solutions.

---

### Lamarckian Genetic Algorithm
1. **Local Search and Genetic Material Update**:  
   Similar to Baldwinian, but incorporates the results of the local search directly into the genetic material.

2. **Inheritance of Traits**:  
   Allows "learned" traits from local search to be passed down to offspring, accelerating convergence.

---

## Output
Results are saved in the specified output directory and include the following files:
- **`mejor_solucion.txt`**:  
  Contains the best solution and its associated cost.
  
- **`historial_fitness.json`**:  
  A log of fitness values per generation, useful for tracking performance over time.
  
- **Fitness Progress Plots** (if enabled):  
  Visual representation of fitness trends throughout the evolutionary process.

---

### Example Output (Console)

Example Output:
Inicializando población
Generación 0: Mejor fitness = 45000000
Generación 100: Mejor fitness = 44500000
Generación 200: Mejor fitness = 44050000
Generación 500: Mejor fitness = 43759294
Project Structure:
genetic-algorithm-qap/
├── src/
│   ├── __init__.py
│   ├── main.py                # Main script to run the algorithms
│   ├── genetic_algorithm.py   # Standard Genetic Algorithm
│   ├── baldwinian_ga.py       # Baldwinian Genetic Algorithm
│   ├── lamarckian_ga.py       # Lamarckian Genetic Algorithm
│   ├── fitness.py             # Fitness functions
│   ├── selection.py           # Tournament selection
│   ├── crossover.py           # PMX crossover implementation
│   ├── mutation.py            # Swap mutation
│   ├── optimization.py        # 2-opt optimization for local search
│   ├── utils.py               # Utility functions (e.g., data loading)
│   └── plotting.py            # Fitness progress visualization
├── tests/                     # Unit tests for the project
├── data/                      # Input data for QAP
├── results/                   # Output directory for results
├── requirements.txt           # Python dependencies
└── README.md                  # Project documentation

python -m src.main --variant standard --data data/raw/tai256c.dat --output results/standard_ga/ --population 150 --generations 2000 --crossover_rate 0.9 --mutation_rate 0.05 --elitismo --seed 42

python -m src.main --variant standard --data data/raw/tai256c.dat --output results/standard_ga/ --population 300 --generations 3000 --crossover_rate 0.9 --mutation_rate 0.08 --elitismo --seed 42

python -m src.main --variant baldwinian --data data/raw/tai256c.dat --output results/baldwinian/ --population 300 --generations 3000 --crossover_rate 0.9 --mutation_rate 0.08 --elitismo --seed 42

python -m src.main --variant baldwinian --data data/raw/tai256c.dat --output results/baldwinian/ --population 500 --generations 500 --crossover_rate 0.9 --mutation_rate 0.12 --elitismo --seed 42 --hill_climbing_max_iter 10 --opt_population_size 20