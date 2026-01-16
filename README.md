# Maximum Clique Problem Solver

This repository contains a software framework developed as part of a Bachelor's Thesis. It implements and compares multiple heuristic and meta-heuristic strategies to solve the Maximum Clique Problem on undirected graphs.

The project is designed with a modular architecture that separates data management, algorithmic strategies, and optimization logic, allowing for easy extensibility and comparison of results.

## Project Overview

The main objective is to find the maximum clique (a subset of vertices of an undirected graph such that every two distinct vertices in the clique are adjacent) using various computational approaches. The software handles standard DIMACS graph files.

## Implemented Algorithms

The solver features a two-phase approach: a constructive phase using greedy heuristics followed by an optimization phase using Iterated Local Search.

### 1. Constructive Heuristics
The project implements three main families of greedy strategies:

* **Independent Set Reduction:** Approaches that solve the problem by finding the maximum Independent Set on the complement graph.
    * *Minimum Degree Selection:* Iteratively selects nodes with the minimum degree in the complement graph.
    * *K-Min Degree Selection:* Adds diversification by selecting randomly among the *k* nodes with the lowest degree.

* **Local Score Heuristics:** Approaches based on a specific scoring function (ratio between a node's degree and the average degree of its neighbors).
    * *Random Tie-Breaking:* Standard greedy approach with randomized tie-breaking for equal scores.
    * *Top-K Randomized Selection:* Selects the next node randomly from a pool of the best *k* compatible candidates to avoid local optima.

* **Vertex Cover Reduction:** Approaches that reduce the problem to finding the minimum Vertex Cover on the complement graph.
    * *Maximum Degree:* Approximates the Vertex Cover by selecting nodes with the highest degree.
    * *Matching-Based:* Approximates the Vertex Cover using maximal random matching logic.

### 2. Optimization (Meta-heuristic)
To improve the solution found by the constructive phase, the software utilizes an **Iterated Local Search (ILS)** algorithm featuring:
* **Perturbation:** A mechanism to escape local optima by removing a random subset of nodes from the current clique.
* **Local Search:** A (1,k)-swap heuristic that attempts to remove one node to add multiple new nodes, effectively increasing the clique size.

## Project Structure

The codebase adheres to clean code principles and is structured as follows:

* `src/strategies/`: Contains the isolated implementation of the specific greedy algorithms.
* `src/local_search.py`: Implements the ILS meta-heuristic logic.
* `src/loader.py`: Handles file I/O operations for DIMACS format graphs.
* `main.py`: The entry point that orchestrates the execution flow and performance reporting.