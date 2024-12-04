import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mass Evolution Simulation")

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Frame rate
FPS = 24
clock = pygame.time.Clock()

# Dot class
class Dot:
    def __init__(self, x, y, speed, vision):
        self.x = x
        self.y = y
        self.speed = speed
        self.vision = vision
        self.energy = 100
        self.reproduction_cooldown = 0

    def move(self, food_items, dots):
        # Find nearest food within vision range
        target = None
        min_distance = self.vision
        for food in food_items:
            distance = math.hypot(self.x - food.x, self.y - food.y)
            if distance < min_distance:
                min_distance = distance
                target = food
        
        # Move toward target if visible
        if target:
            angle = math.atan2(target.y - self.y, target.x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        else:
            # Random movement if no target is visible
            self.x += random.uniform(-self.speed, self.speed)
            self.y += random.uniform(-self.speed, self.speed)
        
        # Keep within bounds
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))
        # Energy decay
        self.energy -= 0.1

        # Reproduction decision
        if self.energy > 150 and self.reproduction_cooldown <= 0:
            offspring = self.reproduce()
            if offspring:
                dots.append(offspring)
                self.reproduction_cooldown = 50  # Cooldown period before reproducing again

        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1

    def eat(self, food):
        # Consume food if within range
        distance = math.hypot(self.x - food.x, self.y - food.y)
        if distance < 10:  # Larger radius for fewer dots
            self.energy += 50
            return True
        return False

    def reproduce(self):
        # Reproduce only if sufficient energy
        if self.energy > 200:
            self.energy -= 100
            return Dot(
                self.x + random.uniform(-20, 20),
                self.y + random.uniform(-20, 20),
                max(0.5, self.speed + random.uniform(-0.1, 0.1)),
                max(10, self.vision + random.uniform(-2, 2))
            )

    def is_dead(self):
        return self.energy <= 0

    def draw(self):
        pygame.draw.circle(screen, RED, (int(self.x), int(self.y)), 5)

# Predator class
class Predator:
    def __init__(self, x, y, speed, vision):
        self.x = x
        self.y = y
        self.speed = speed
        self.vision = vision
        self.energy = 150
        self.reproduction_cooldown = 0

    def move(self, dots, predators):
        # Find nearest dot within vision range
        target = None
        min_distance = self.vision
        for dot in dots:
            distance = math.hypot(self.x - dot.x, self.y - dot.y)
            if distance < min_distance:
                min_distance = distance
                target = dot
        
        # Move toward target if visible
        if target:
            angle = math.atan2(target.y - self.y, target.x - self.x)
            self.x += self.speed * math.cos(angle)
            self.y += self.speed * math.sin(angle)
        else:
            # Random movement if no target is visible
            self.x += random.uniform(-self.speed, self.speed)
            self.y += random.uniform(-self.speed, self.speed)
        
        # Keep within bounds
        self.x = max(0, min(WIDTH, self.x))
        self.y = max(0, min(HEIGHT, self.y))
        # Energy decay
        self.energy -= 0.2

        # Reproduction decision
        if self.energy > 200 and self.reproduction_cooldown <= 0:
            offspring = self.reproduce()
            if offspring:
                predators.append(offspring)
                self.reproduction_cooldown = 100  # Cooldown period before reproducing again

        if self.reproduction_cooldown > 0:
            self.reproduction_cooldown -= 1

    def attack(self, dot):
        # Attack dot if within range
        distance = math.hypot(self.x - dot.x, self.y - dot.y)
        if distance < 10:  # Attack radius
            self.energy += 50
            return True
        return False

    def reproduce(self):
        # Reproduce only if sufficient energy
        if self.energy > 250:
            self.energy -= 125
            return Predator(
                self.x + random.uniform(-20, 20),
                self.y + random.uniform(-20, 20),
                max(1.0, self.speed + random.uniform(-0.1, 0.1)),
                max(20, self.vision + random.uniform(-5, 5))
            )

    def is_dead(self):
        return self.energy <= 0

    def draw(self):
        pygame.draw.circle(screen, BLUE, (int(self.x), int(self.y)), 7)

# Food class
class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def draw(self):
        pygame.draw.circle(screen, GREEN, (int(self.x), int(self.y)), 5)

# Initialize dots, predators, and food
dots = [Dot(random.randint(0, WIDTH), random.randint(0, HEIGHT), 2, 50) for _ in range(50)]
predators = [Predator(random.randint(0, WIDTH), random.randint(0, HEIGHT), 2.5, 70) for _ in range(2)]
food_items = [Food(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# Main loop
running = True
while running:
    screen.fill(BLACK)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Update dots
    new_dots = []
    for dot in dots:
        dot.move(food_items, dots)  # Movement with vision
        dot.draw()

        # Check for food
        for food in food_items:
            if dot.eat(food):
                food_items.remove(food)
                food_items.append(Food(random.randint(0, WIDTH), random.randint(0, HEIGHT)))

        # Remove dead dots
        if not dot.is_dead():
            new_dots.append(dot)

    dots = new_dots

    # Update predators
    new_predators = []
    for predator in predators:
        predator.move(dots, predators)  # Predators hunt dots and reproduce
        predator.draw()

        # Check for attacks
        for dot in dots:
            if predator.attack(dot):
                dots.remove(dot)

        # Remove dead predators
        if not predator.is_dead():
            new_predators.append(predator)

    predators = new_predators

    # Draw food
    for food in food_items:
        food.draw()

    # Update display
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
