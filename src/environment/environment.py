from gymnasium import spaces
from stable_baselines3 import PPO
import pygame
import numpy as np
import gymnasium as gym
import math
import cv2
import sys

WIDTH = 800
HEIGHT = 600
ROAD_COLOR = (50, 50, 50)

class CarEnvironment(gym.Env):
    def __init__(self):
        super(CarEnvironment, self).__init__()
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.track = pygame.Surface((WIDTH, HEIGHT))
        self.size = 20
        self.font = pygame.font.Font(None, 20)

        self._load_spaces()
        self.track.fill((52, 235, 110))
        self.total_reward = 0
        self.clock = pygame.time.Clock()

    def _load_spaces(self):
        self.action_space = spaces.Discrete(5)
        self.observation_space = spaces.Box(low=np.array([0, 0, -np.pi]), high=np.array([WIDTH, HEIGHT, np.pi], dtype=np.float32))

    def reset(self, seed=None, options=None):
        self._reset_presets()
        self._generate_coordinates()
        self.car_sprite = CarAgent()

        self.draw_environment()
        pygame.display.flip()
        self.total_reward = 0
        #print(self._get_observation())
        obs = self._get_observation()
        return obs, {} 
    
    def step(self, action=None, human=None):
        self.car_sprite.update(action, human)

        is_on_road = self._is_on_road()
        reward = 1 if is_on_road else -10
        done = not is_on_road
        self.total_reward += reward
        return self._get_observation(), reward, done, {}, {}
    
    def _is_on_road(self):
        pixel_color = self.track.get_at((int(self.car_sprite.x), int(self.car_sprite.y)))[:3]
        return pixel_color == (190, 190, 190)

    
    def _get_observation(self):
        frame = pygame.surfarray.array3d(self.screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
        frame = cv2.resize(frame, (80, 80))
        return np.expand_dims(frame, axis=-1)    

    def _reset_presets(self):
        self.rect_coordinates = []
        self.top_left_coordinates = []
        self.top_right_coordinates = []
        self.bottom_left_coordinates = []
        self.bottom_right_coordinates = []

    def _draw_roads(self):
        #print(self.rect_coordinates)
        for coordinate in self.rect_coordinates:
            pygame.draw.rect(self.track, "gray", pygame.Rect(coordinate[0], coordinate[1], self.size, self.size))
        
        for coordinate in self.top_left_coordinates:
            pygame.draw.circle(self.track, "gray", [coordinate[0], coordinate[1]], self.size, draw_top_left=True)

        for coordinate in self.top_right_coordinates:
            pygame.draw.circle(self.track, "gray", [coordinate[0], coordinate[1]], self.size, draw_top_right=True)

        for coordinate in self.bottom_left_coordinates:
            pygame.draw.circle(self.track, "gray", [coordinate[0], coordinate[1]], self.size, draw_bottom_left=True)

        for coordinate in self.bottom_right_coordinates:
            pygame.draw.circle(self.track, "gray", [coordinate[0], coordinate[1]], self.size, draw_bottom_right=True)
            
    def _generate_coordinates(self):
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

    def draw_environment(self):
        self.screen.blit(self.track, (0, 0))
        self._draw_roads()
        self.car_sprite.render(self.screen)
    
    def render(self):
        self.draw_environment()
        coordinate_text = self.font.render(f"x: {self.car_sprite.rect.x}, y: {self.car_sprite.rect.y}", True, (0, 0, 0))
        self.screen.blit(coordinate_text, (10, 10))
      
        pygame.display.flip()
        
        self.clock.tick(60)

    def close(self):
        print(f"Total reward: {self.total_reward}")
        pygame.quit()

class CarAgent:
    def __init__(self, x=40, y=40, acceleration=0.1):
        self.x, self.y = x, y
        self.angle = 0
        self.heading = 0
        self.min_angle = 1
        self.min_angle = math.radians(self.min_angle)

        self.velocity = pygame.math.Vector2(0, 0)
        self.speed = 0
        self.position = pygame.math.Vector2(40, 40)

        self._load_car_presets()

        self.acceleration = acceleration
        self.friction = 0.05
        self.max_speed = 5
        self.rotation_speed = 5


    def _load_car_presets(self):
        self.car_image = pygame.transform.scale(pygame.image.load("car.png").convert_alpha(), (10, 15))
        self.images = []
        for i in range(0, 360):
            rotated_img = pygame.transform.rotozoom(self.car_image, 360-90-(i*self.min_angle), 1)
            self.images.append(rotated_img)

        self.image = self.images[0]
        self.rect = self.image.get_rect(center=(40, 40))

    def human_update(self):
        action = 0
        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            action = 1
        elif keys[pygame.K_DOWN]:
            action = 2
        if keys[pygame.K_LEFT]:
            action = 3
        elif keys[pygame.K_RIGHT]:
            action = 4
    
        self.move(action)


    def _accelerate(self, amount):
        self.speed += amount

    def _brake(self):
        self.speed -= 0.5
        if self.speed < 0.1:
            self.speed = 0

    def _turn(self, degrees):
        self.heading += math.radians(degrees)
        index = int(self.heading / self.min_angle) % len(self.images)
        if(self.image != self.images[index]):
            self.image = self.images[index]

        
    def move(self, action: int):
        if action == 1:
            self._accelerate(0.01)
        elif action == 2:
            self._brake()
        elif action == 3:
            self._turn(-1.5)
        elif action == 4:
            self._turn(1.5)

    def update(self, action=None, human=False):
        if human:
            return self.human_update()

        return self.move(action)
 
    def render(self, screen):
        self.velocity.from_polar((self.speed, math.degrees(self.heading)))
        self.position += self.velocity
        self.rect.center = (round(self.position[0]), round(self.position[1]))
        
        screen.blit(self.image, self.rect)

def human_main():
    env = CarEnvironment()
    pygame.mixer.init()

    env.reset()

    running = True

    while running:
        env.render()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        env.step(action=None, human=True)
        
    env.close()


def ai_main():
    env = CarEnvironment()
    
    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10_000)
    model.save("car_ai_model")

    print("Here")

    obs, _ = env.reset()
    print(obs)
    running = True

    while running:
        env.render()
        action, _states = model.predict(obs)
        print(action)
        obs, reward, done, truncated, info = env.step(action)

        if done or truncated:
            obs, _ = env.reset()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    env.close()

def main():
    argv = sys.argv
    if len(argv) != 2:
        raise Exception("Too many arguments")

    if argv[1] == "human":
        human_main()
    elif argv[1] == "ai":
        ai_main()

if __name__ == "__main__":
    main()
    







        