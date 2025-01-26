import pygame
import numpy as np
from pygame.locals import *

# Constants
WINDOW_SIZE = (800, 600)
BACKGROUND_COLOR = (30, 30, 30)
PARTICLE_COLOR = (100, 100, 255)
PARTICLE_RADIUS = 8
NUM_PARTICLES = 100
GRAVITY = np.array([0, 980.0])
DAMPING = 0.95
SMOOTHING_RADIUS = 30
PRESSURE_STIFFNESS = 0.08
VISCOSITY = 0.02
REST_DENSITY = 300.0
TIME_STEP = 0.016

# Smoothing kernels
def poly6_kernel(r, h):
    return 315 / (64 * np.pi * h**9) * (h**2 - r**2)**3 if r < h else 0.0

def spiky_gradient(r, h):
    return -45 / (np.pi * h**6) * (h - r)**2 if r < h else 0.0

def viscosity_laplacian(r, h):
    return 45 / (np.pi * h**6) * (h - r) if r < h else 0.0

class SpatialGrid:
    def __init__(self, cell_size):
        self.cell_size = cell_size
        self.grid = {}
        
    def update(self, particles):
        self.grid = {}
        for i, p in enumerate(particles):
            cell = (int(p.pos[0]/self.cell_size), int(p.pos[1]/self.cell_size))
            if cell not in self.grid:
                self.grid[cell] = []
            self.grid[cell].append(i)
    
    def get_neighbors(self, pos):
        cell = (int(pos[0]/self.cell_size), int(pos[1]/self.cell_size))
        neighbors = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                adjacent_cell = (cell[0]+dx, cell[1]+dy)
                if adjacent_cell in self.grid:
                    neighbors.extend(self.grid[adjacent_cell])
        return neighbors

class Particle:
    def __init__(self, pos):
        self.pos = np.array(pos, dtype=np.float64)
        self.vel = np.zeros(2, dtype=np.float64)
        self.acc = np.zeros(2, dtype=np.float64)
        self.density = REST_DENSITY
        self.pressure = 0.0

    def update(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt
        self.acc = np.zeros(2, dtype=np.float64)

class FluidSimulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.particles = []
        self.grid = SpatialGrid(SMOOTHING_RADIUS)
        
        # Initialize particles
        for _ in range(NUM_PARTICLES):
            pos = [np.random.uniform(0, width), np.random.uniform(0, height)]
            self.particles.append(Particle(pos))
    
    def handle_boundaries(self):
        for p in self.particles:
            # Window boundaries with momentum preservation
            if p.pos[0] < PARTICLE_RADIUS:
                p.pos[0] = PARTICLE_RADIUS
                p.vel[0] *= -DAMPING
            elif p.pos[0] > self.width - PARTICLE_RADIUS:
                p.pos[0] = self.width - PARTICLE_RADIUS
                p.vel[0] *= -DAMPING
                
            if p.pos[1] < PARTICLE_RADIUS:
                p.pos[1] = PARTICLE_RADIUS
                p.vel[1] *= -DAMPING
            elif p.pos[1] > self.height - PARTICLE_RADIUS:
                p.pos[1] = self.height - PARTICLE_RADIUS
                p.vel[1] *= -DAMPING
    
    def update_physics(self):
        # Update spatial grid
        self.grid.update(self.particles)
        
        # Compute densities and pressures
        for p in self.particles:
            neighbor_ids = self.grid.get_neighbors(p.pos)
            neighbors = [self.particles[i] for i in neighbor_ids]
            
            density = 0.0
            for neighbor in neighbors:
                r = np.linalg.norm(p.pos - neighbor.pos)
                density += poly6_kernel(r, SMOOTHING_RADIUS)
            p.density = density
            p.pressure = PRESSURE_STIFFNESS * (p.density - REST_DENSITY)
        
        # Compute forces
        for p in self.particles:
            pressure_force = np.zeros(2)
            viscosity_force = np.zeros(2)
            
            neighbor_ids = self.grid.get_neighbors(p.pos)
            neighbors = [self.particles[i] for i in neighbor_ids]
            
            for neighbor in neighbors:
                if p == neighbor:
                    continue
                
                r_vec = neighbor.pos - p.pos
                r = np.linalg.norm(r_vec)
                if r == 0:
                    continue
                
                # Pressure force
                pressure_force += -r_vec/r * (p.pressure + neighbor.pressure)/(2 * neighbor.density) * \
                                 spiky_gradient(r, SMOOTHING_RADIUS)
                
                # Viscosity force
                viscosity_force += VISCOSITY * (neighbor.vel - p.vel)/neighbor.density * \
                                  viscosity_laplacian(r, SMOOTHING_RADIUS)
            
            # External forces
            gravity_force = GRAVITY * p.density
            friction_force = -0.1 * p.vel * p.density
            
            total_force = pressure_force + viscosity_force + gravity_force + friction_force
            p.acc = total_force / p.density
    
    def on_resize(self, new_size):
        self.width, self.height = new_size
        # Adjust particles to new boundaries
        for p in self.particles:
            p.pos[0] = min(max(p.pos[0], PARTICLE_RADIUS), self.width - PARTICLE_RADIUS)
            p.pos[1] = min(max(p.pos[1], PARTICLE_RADIUS), self.height - PARTICLE_RADIUS)

def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, HWSURFACE|DOUBLEBUF|RESIZABLE)
    clock = pygame.time.Clock()
    
    sim = FluidSimulation(*WINDOW_SIZE)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == VIDEORESIZE:
                screen = pygame.display.set_mode(event.size, HWSURFACE|DOUBLEBUF|RESIZABLE)
                sim.on_resize(event.size)
        
        # Physics steps
        sim.update_physics()
        for p in sim.particles:
            p.update(TIME_STEP)
        sim.handle_boundaries()
        
        # Rendering
        screen.fill(BACKGROUND_COLOR)
        for p in sim.particles:
            pygame.draw.circle(screen, PARTICLE_COLOR, 
                             (int(p.pos[0]), int(p.pos[1])), PARTICLE_RADIUS)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()

if __name__ == "__main__":
    main()