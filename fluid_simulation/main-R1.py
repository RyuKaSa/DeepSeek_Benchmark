import pygame
import math
import random
import numpy as np

# Constants
NUM_PARTICLES = 100
PARTICLE_RADIUS = 8
GRAVITY = 750.0
DAMPING = 0.95
BOUNDARY_DAMPING = 0.8
INITIAL_WINDOW_SIZE = (800, 600)
BACKGROUND_COLOR = (30, 30, 30)
PARTICLE_COLOR = (100, 150, 255)

# SPH Parameters
SMOOTHING_RADIUS = 30.0
REST_DENSITY = 1000.0
PRESSURE_STIFFNESS = 50.0  # Increased for better stability
VISCOSITY_STRENGTH = 1.0
SURFACE_TENSION = 0.05
EPSILON = 1e-8  # Numerical safety margin

class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.ax = 0.0
        self.ay = 0.0
        self.radius = PARTICLE_RADIUS
        self.mass = 1.0
        self.density = REST_DENSITY
        self.pressure = 0.0

    def apply_force(self, fx, fy):
        self.ax += fx / self.mass
        self.ay += fy / self.mass

def sph_kernel(r, h):
    return 315 / (64 * np.pi * h**9) * (h**2 - r**2)**3 if r < h else 0

def sph_kernel_derivative(r, h):
    return -45 / (np.pi * h**6) * (h - r)**2 if r < h else 0

def sph_viscosity_kernel(r, h):
    """Numerically stable viscosity kernel"""
    if r < EPSILON:
        return 0.0
    return (15 / (2 * np.pi * h**3)) * (
        - (r**3) / (2*h**3) + 
        r**2 / h**2 + 
        h / (2*(r + EPSILON)) -  # Prevent division by zero
        1
    ) if r < h else 0

def find_neighbors(particles, h):
    neighbors = [[] for _ in particles]
    for i, p1 in enumerate(particles):
        for j, p2 in enumerate(particles[i+1:], i+1):
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            r = math.hypot(dx, dy)
            if r < h:
                neighbors[i].append((j, r))
                neighbors[j].append((i, r))
    return neighbors

def compute_density_pressure(particles, neighbors, h):
    for i, p in enumerate(particles):
        density = 0.0
        for j, r in neighbors[i]:
            density += particles[j].mass * sph_kernel(r, h)
        p.density = max(density, REST_DENSITY*0.1)  # Prevent negative pressure
        p.pressure = PRESSURE_STIFFNESS * (p.density - REST_DENSITY)

def compute_forces(particles, neighbors, h):
    for i, p in enumerate(particles):
        pressure_force_x = 0.0
        pressure_force_y = 0.0
        viscosity_force_x = 0.0
        viscosity_force_y = 0.0
        tension_force_x = 0.0
        tension_force_y = 0.0
        
        for j, r in neighbors[i]:
            pj = particles[j]
            dx = pj.x - p.x
            dy = pj.y - p.y
            distance = max(r, EPSILON)  # Ensure non-zero distance
            dir_x = dx / distance
            dir_y = dy / distance
            
            # Pressure force
            shared_pressure = (p.pressure + pj.pressure) / 2
            pressure_force = -shared_pressure * sph_kernel_derivative(r, h)
            pressure_force_x += pressure_force * dir_x
            pressure_force_y += pressure_force * dir_y
            
            # Viscosity force
            vel_diff_x = pj.vx - p.vx
            vel_diff_y = pj.vy - p.vy
            viscosity = VISCOSITY_STRENGTH * sph_viscosity_kernel(r, h)
            viscosity_force_x += viscosity * vel_diff_x
            viscosity_force_y += viscosity * vel_diff_y
            
            # Surface tension
            cohesion = sph_kernel(r, h) * SURFACE_TENSION
            tension_force_x += cohesion * dir_x
            tension_force_y += cohesion * dir_y
        
        # Apply forces
        p.apply_force(pressure_force_x, pressure_force_y)
        p.apply_force(viscosity_force_x, viscosity_force_y)
        p.apply_force(tension_force_x, tension_force_y)

def handle_collisions(particles):
    for i in range(len(particles)):
        for j in range(i+1, len(particles)):
            p1 = particles[i]
            p2 = particles[j]
            
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            distance = math.hypot(dx, dy)
            min_dist = p1.radius + p2.radius
            
            if distance < min_dist and distance > EPSILON:
                # Collision resolution with positional correction
                nx = dx / distance
                ny = dy / distance
                overlap = (min_dist - distance) / 2
                
                # Position correction
                p1.x -= overlap * nx
                p1.y -= overlap * ny
                p2.x += overlap * nx
                p2.y += overlap * ny
                
                # Velocity update
                dvx = p2.vx - p1.vx
                dvy = p2.vy - p1.vy
                impulse = (2.0 * (dvx * nx + dvy * ny)) / (p1.mass + p2.mass)
                
                p1.vx += impulse * p2.mass * nx
                p1.vy += impulse * p2.mass * ny
                p2.vx -= impulse * p1.mass * nx
                p2.vy -= impulse * p1.mass * ny

def main():
    pygame.init()
    width, height = INITIAL_WINDOW_SIZE
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption("SPH Fluid Simulation (Stable)")
    clock = pygame.time.Clock()
    
    particles = [
        Particle(
            random.uniform(PARTICLE_RADIUS, width - PARTICLE_RADIUS),
            random.uniform(PARTICLE_RADIUS, height - PARTICLE_RADIUS)
        ) for _ in range(NUM_PARTICLES)
    ]
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Cap at 60 FPS
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.w, event.h
                for p in particles:
                    p.x = max(PARTICLE_RADIUS, min(p.x, new_width - PARTICLE_RADIUS))
                    p.y = max(PARTICLE_RADIUS, min(p.y, new_height - PARTICLE_RADIUS))
                width, height = new_width, new_height
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
        
        # SPH simulation steps
        neighbors = find_neighbors(particles, SMOOTHING_RADIUS)
        compute_density_pressure(particles, neighbors, SMOOTHING_RADIUS)
        compute_forces(particles, neighbors, SMOOTHING_RADIUS)
        
        # Apply gravity
        for p in particles:
            p.apply_force(0, GRAVITY * p.mass)
        
        # Update particles
        for p in particles:
            p.vx += p.ax * dt
            p.vy += p.ay * dt
            p.x += p.vx * dt
            p.y += p.vy * dt
            p.ax = 0
            p.ay = 0
            
            # Boundary constraints with damping
            if p.x < p.radius:
                p.x = p.radius
                p.vx *= -BOUNDARY_DAMPING
            elif p.x > width - p.radius:
                p.x = width - p.radius
                p.vx *= -BOUNDARY_DAMPING
            if p.y < p.radius:
                p.y = p.radius
                p.vy *= -BOUNDARY_DAMPING
            elif p.y > height - p.radius:
                p.y = height - p.radius
                p.vy *= -BOUNDARY_DAMPING
        
        # Handle collisions
        handle_collisions(particles)
        
        # Apply global damping
        for p in particles:
            p.vx *= DAMPING
            p.vy *= DAMPING
        
        # Render frame
        screen.fill(BACKGROUND_COLOR)
        for p in particles:
            pygame.draw.circle(screen, PARTICLE_COLOR, (int(p.x), int(p.y)), p.radius)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()