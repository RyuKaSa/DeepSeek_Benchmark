# LLM Coding Benchmark: DeepSeek R1 vs ChatGPT O1

## Overview
This repository serves as a testing ground for evaluating the coding capabilities of two competing Large Language Models (LLMs): **DeepSeek R1** and **ChatGPT o1**. The goal is to implement technically complex programming challenges, focusing on areas such as physics simulations, AI-driven algorithms, and computational modeling.

Each project consists of:
- **Independent implementations** from both LLMs.
- **Five prompt iterations** allowed for parameter tuning and refinement.
- **A hybrid script**, where I combine the best aspects of both models and apply my own modifications within an hour.

The repository follows a structured **naming scheme**:
- `main-o1.py` → ChatGPT O1’s implementation
- `main-R1.py` → DeepSeek R1’s implementation
- `combined.py` → The final hybrid version, incorporating both LLMs' code's best aspects and incorporates additional human-lead optimizations, with about an additional hour.
---

## Projects
### 1. Fluid Simulation
#### Goal
To simulate **100 water molecules** (particles) using physics-based motion. The simulation includes gravity, friction, and fluid-like behavior. The particles should be constrained within the window and dynamically respond to window resizing.

#### Initial Prompt Given to Both LLMs
```
Develop a senior-level Python script that spawns 100 balls, simulating 100 molecules of water. Incorporate the following physics principles:

Core Mechanics:
- Newtonian physics: Apply F = ma for motion.
- Motion integration: Use Euler or Verlet integration.

Fluid Simulation (Particle Interactions):
- Pressure forces: Maintain density using an equation of state.
- Viscosity forces: Simulate internal friction for smooth flow.
- Surface tension: Keep droplets cohesive.

Collision Handling:
- Particle-particle: Implement elastic collisions or repulsion forces.
- Particle-boundary: Ensure walls reflect or absorb kinetic energy.

External Forces:
- Gravity pulls molecules downward.
- Turbulence or external forces can be added for realism.

Implementation Requirements:
- Use Pygame or Pygame + NumPy for visualization.
- Implement Smoothed Particle Hydrodynamics (SPH) or Verlet Integration for fluid-like behavior.
- Optimize with a quadtree or grid-based neighbor search for efficiency.
- Ensure particles remain strictly within the window boundaries, adjusting dynamically if the window is resized.
```

#### Evaluation Process
- Both LLMs are allowed **up to 5 iterative refinements** to improve parameters, ensure consistency in **particle size, gravity, and behavior**, and refine the simulation.
- Once finalized, their scripts are compared for performance, realism, and adherence to the problem constraints.
- The **hybrid script (`combined.py`)** merges the best aspects from both implementations and incorporates additional human-lead optimizations.

---

## Future Projects
Additional technical challenges will be introduced, focusing on AI, physics, and computational modeling.

Stay tuned for more benchmarking experiments!

---

## Contribution
This repository is primarily for testing and comparison. However, feel free to fork, experiment, or suggest improvements!