import pygame
import math
import numpy as np
import random 

WIDTH = 800
HEIGHT = 800

class Agent(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.min_angle = 1
        self.car_image = pygame.transform.scale(pygame.image.load("car.png").convert_alpha(), (20, 25))
        self.images = []
        self.q_table = {}

        for i in range(0, 360):
            rotated_img = pygame.transform.rotozoom(self.car_image, 360-90-(i*self.min_angle), 1)
            self.images.append(rotated_img)

        self._initialize_variables()
       

    def _initialize_variables(self):
        self.min_angle = math.radians(self.min_angle)
        self.image = self.images[0]

        self.rect = self.image.get_rect()
        self.rect.center = (40, 40)
        self.reversing = False
        self.heading = 0
        self.speed = 0
        self.obj = None

        self.velocity = pygame.math.Vector2(0, 0)
        self.position = pygame.math.Vector2(40, 40)

    def _get_state(self):
        return (self.rect.center[0], self.rect.center[1])
    
    def _get_action(self, state):
        if state in self.q_table:
            return np.argmax(self.q_table[state])

        return random.randint(0, 3)
    

    def train(self, episodes=100):
        for _ in range(episodes):
            self._initialize_variables()
            state = self._get_state()
            done = False
            reward = 0

            while not done:
                action = self._get_action()

    
    def turn(self, degrees):
        self.heading += math.radians(degrees)
        print("Heading: ", self.heading)
        index = int(self.heading / self.min_angle) % len(self.images)
        if(self.image != self.images[index]):
            self.image = self.images[index]
    
    def accelerate(self, amount):
        if self.reversing is False:
            self.speed += amount
        else:
            self.speed -= amount    
            
    def brake(self):
        self.speed -= 0.5
        if abs(self.speed) < 0.1:
            self.speed = 0

    def reset(self):
        self.reversing = False
        self.heading = 0
        self.speed = 0
        self.rect.center = (40, 40)

        
    def reverse(self):
        self.speed = 0
        self.reversing = not self.reversing
    
    def update(self):
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))
        self.position += self.velocity
        self.rect.center = (round(self.position[0]), round(self.position[1]))


class Environment:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
        self.surface = pygame.Surface((WIDTH, HEIGHT))
        self.size = 20

        self.rect_coordinates = []
        self.top_left_coordinates = []
        self.top_right_coordinates = []
        self.bottom_left_coordinates = []
        self.bottom_right_coordinates = []

        self.generate_coordinates()

        self.surface.fill((52, 235, 110))
        #self.screen.fill((52, 235, 110))
        self.agent = Agent()
        

    def generate_coordinates(self):
        for i in range(40, 501, self.size):
            for j in range(20, 41, self.size):
                self.rect_coordinates.append((j, i))

        self.top_left_coordinates.append((40, 40))

        for j in range(40, 501, self.size):
            for i in range(20, 41, self.size):
                self.rect_coordinates.append((j, i))

        self.bottom_left_coordinates.append((40, 520))

        for i in range(40, 501, self.size):
            for j in range(500, 521, self.size):
                self.rect_coordinates.append((i, j))

        self.bottom_right_coordinates.append((520, 520))

        for j in range(40, 501, self.size):
            for i in range(500, 521, self.size):
                self.rect_coordinates.append((i, j))

        self.top_right_coordinates.append((520, 40))

            
    def draw_grid(self):
        for x in range(0, WIDTH, self.size):
            for y in range(0, HEIGHT, self.size):
                pygame.draw.rect(self.screen, "white", pygame.Rect(x, y, self.size, self.size), 1)

    def draw_agent(self):
        self.agent.obj = pygame.Rect(self.agent.x, self.agent.y, 10, 20)
        pygame.draw.rect(self.screen, "blue", self.agent.obj)
        pygame.display.update()

    def draw_roads(self):
        for coordinate in self.rect_coordinates:
            pygame.draw.rect(self.surface, "gray", pygame.Rect(coordinate[0], coordinate[1], self.size, self.size))
        
        for coordinate in self.top_left_coordinates:
            pygame.draw.circle(self.surface, "gray", [coordinate[0], coordinate[1]], self.size, draw_top_left=True)

        for coordinate in self.top_right_coordinates:
            pygame.draw.circle(self.surface, "gray", [coordinate[0], coordinate[1]], self.size, draw_top_right=True)

        for coordinate in self.bottom_left_coordinates:
            pygame.draw.circle(self.surface, "gray", [coordinate[0], coordinate[1]], self.size, draw_bottom_left=True)

        for coordinate in self.bottom_right_coordinates:
            pygame.draw.circle(self.surface, "gray", [coordinate[0], coordinate[1]], self.size, draw_bottom_right=True)
        
        pygame.display.flip()
        """for i in range(40, 501, self.size):
            for j in range(20, 41, self.size):
                pygame.draw.rect(self.surface, "gray", pygame.Rect(j, i, self.size, self.size))
        pygame.draw.circle(self.surface, "gray", [40, 40], self.size, 0, draw_top_left=True)

        for j in range(40, 501, self.size):
            for i in range(20, 41, self.size):
                pygame.draw.rect(self.surface, "gray", pygame.Rect(j, i, self.size, self.size))
        pygame.draw.circle(self.surface, "gray", [40, 520], self.size, 0, draw_bottom_left=True)

        for i in range(40, 501, self.size):
            for j in range(500, 521, self.size):
                pygame.draw.rect(self.surface, "gray", pygame.Rect(i, j, self.size, self.size))
        pygame.draw.circle(self.surface, "gray", [520, 520], self.size, 0, draw_bottom_right=True)

        for j in range(40, 501, self.size):
            for i in range(500, 521, self.size):
                pygame.draw.rect(self.surface, "gray", pygame.Rect(i, j, self.size, self.size))
        pygame.draw.circle(self.surface, "gray", [520, 40], self.size, 0, draw_top_right=True)
        pygame.display.flip()"""

def refresh_environment(env):
    env.screen.fill((52, 235, 110))
    env.draw_roads()

pygame.init()
pygame.mixer.init()
env = Environment()
#env.draw_grid()
env.draw_roads()


running = True
car = Agent()


sprites = pygame.sprite.GroupSingle()
sprites.add(car)

clock = pygame.time.Clock()

font = pygame.font.Font(None, 20)


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                car.brake()
            elif event.key == pygame.K_DOWN:
                car.accelerate(0.1)

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        car.turn(-1.5)

    if keys[pygame.K_RIGHT]:
        car.turn(1.5)

    coordinate_text = font.render(f"x: {car.rect.x}, y: {car.rect.y}", True, (0, 0, 0))
    
    
    env.screen.blit(env.surface, (0, 0))
    env.screen.blit(coordinate_text, (10, 10))

    sprites.update()
    sprites.draw(env.screen)
 
    
    pygame.display.flip()
    clock.tick(60)


    