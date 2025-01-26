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

---

#### Results

##### o1:
![o1](fluid_simulation/images/o1.gif)

##### R1:
![R1](fluid_simulation/images/R1.gif)

##### combined:
![combined](fluid_simulation/images/combined.gif)

#### Commentary

**o1** had better particle-to-particle interactions, but **R1** had better window-resizing handling.

The third result *combines* both, along with improved particle-to-particle interactions, mostly using pressure stiffness, which prevents the balls from touching their neighbors directly, reflecting real physics models more accurately.

In this mini-project, **o1** was easier to work with, as **R1** tended to get stuck in its *inner monologue/reasoning* loop. However, the combined result was mostly based on **R1**'s output.

---

## Future Projects
Additional technical challenges will be introduced, focusing on AI, physics, and computational modeling.

Stay tuned for more benchmarking experiments!

---

## Contribution
This repository is primarily for testing and comparison. However, feel free to fork, experiment, or suggest improvements!