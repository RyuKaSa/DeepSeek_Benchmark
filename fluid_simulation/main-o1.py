import pygame
import random
import math

# ---------------------
# CONFIGURABLE CONSTANTS
# ---------------------
NUM_BALLS      = 100
BALL_RADIUS    = 8
GRAVITY        = 0.2   # Downward acceleration
FRICTION       = 0.99  # Velocity damping each frame
ELASTICITY     = 0.9   # Bounciness in collisions
SCREEN_WIDTH   = 800
SCREEN_HEIGHT  = 600

# ---------------------
# BALL CLASS
# ---------------------
class Ball:
    def __init__(self, x, y, vx=0.0, vy=0.0):
        self.x  = x
        self.y  = y
        self.vx = vx
        self.vy = vy

    def update(self):
        # Apply gravity
        self.vy += GRAVITY

        # Update position
        self.x += self.vx
        self.y += self.vy

        # Apply friction/damping
        self.vx *= FRICTION
        self.vy *= FRICTION

    def draw(self, surface):
        pygame.draw.circle(surface, (30, 144, 255), (int(self.x), int(self.y)), BALL_RADIUS)

# ---------------------
# COLLISION FUNCTIONS
# ---------------------
def handle_ball_collisions(balls):
    """ Naive O(n^2) collision check between balls. """
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            dx = balls[j].x - balls[i].x
            dy = balls[j].y - balls[i].y
            dist_sq = dx*dx + dy*dy
            # If overlapping
            if dist_sq < (2*BALL_RADIUS)**2:
                dist = math.sqrt(dist_sq) if dist_sq != 0 else 0.0001
                # Normalized collision vector
                nx = dx / dist
                ny = dy / dist
                # Overlap correction (push them apart)
                overlap = (2*BALL_RADIUS - dist) * 0.5
                balls[i].x -= nx * overlap
                balls[i].y -= ny * overlap
                balls[j].x += nx * overlap
                balls[j].y += ny * overlap

                # Basic elastic collision response (1D along normal)
                rel_vx = balls[j].vx - balls[i].vx
                rel_vy = balls[j].vy - balls[i].vy
                sep_speed = rel_vx * nx + rel_vy * ny
                # Only separate if moving closer
                if sep_speed < 0:
                    imp = -(1 + ELASTICITY) * sep_speed / 2
                    ix = imp * nx
                    iy = imp * ny
                    # Apply impulses
                    balls[i].vx -= ix
                    balls[i].vy -= iy
                    balls[j].vx += ix
                    balls[j].vy += iy

def handle_wall_collisions(balls, width, height):
    for b in balls:
        # Check left/right walls
        if b.x < BALL_RADIUS:
            b.x = BALL_RADIUS
            b.vx = -b.vx * ELASTICITY
        elif b.x > width - BALL_RADIUS:
            b.x = width - BALL_RADIUS
            b.vx = -b.vx * ELASTICITY

        # Check top/bottom walls
        if b.y < BALL_RADIUS:
            b.y = BALL_RADIUS
            b.vy = -b.vy * ELASTICITY
        elif b.y > height - BALL_RADIUS:
            b.y = height - BALL_RADIUS
            b.vy = -b.vy * ELASTICITY

# ---------------------
# MAIN SIMULATION
# ---------------------
def main():
    pygame.init()
    pygame.display.set_caption("Water Molecule Simulation")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    clock = pygame.time.Clock()

    # Create balls with random positions/velocities
    balls = []
    for _ in range(NUM_BALLS):
        x  = random.uniform(BALL_RADIUS, SCREEN_WIDTH - BALL_RADIUS)
        y  = random.uniform(BALL_RADIUS, SCREEN_HEIGHT - BALL_RADIUS)
        vx = random.uniform(-3, 3)
        vy = random.uniform(-3, 3)
        balls.append(Ball(x, y, vx, vy))

    current_width, current_height = SCREEN_WIDTH, SCREEN_HEIGHT

    running = True
    while running:
        clock.tick(60)  # Limit FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                # Rescale positions to fit new window size
                new_width, new_height = event.w, event.h
                if new_width < 2*BALL_RADIUS or new_height < 2*BALL_RADIUS:
                    # Prevent weirdness with extremely small windows
                    continue
                scale_x = new_width  / current_width
                scale_y = new_height / current_height
                for b in balls:
                    b.x *= scale_x
                    b.y *= scale_y
                current_width, current_height = new_width, new_height
                screen = pygame.display.set_mode((new_width, new_height), pygame.RESIZABLE)

        # Update physics
        for b in balls:
            b.update()

        handle_ball_collisions(balls)
        handle_wall_collisions(balls, current_width, current_height)

        # Draw
        screen.fill((0, 0, 0))
        for b in balls:
            b.draw(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()