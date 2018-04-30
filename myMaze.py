# Author: William Zhang
# Description: This is a maze solving algorithm. This is an implementation of the Wall Follower Algorithm.
# It uses the "left hand" of the robot as a means to solve the maze.
# Date: April 23, 2018
# Copyright 2018

import sys, pygame
from pygame.locals import *
import random
from entities import *

size_x = 32
size_y = 32

change_x = 32
change_y = 32

Size = 32

SPEED = 32
timer = 375

COLORS = {
    'DAY9YELLOR': (255, 167, 26),
    'PURPLE': (144, 124, 180),
    'PINK': (255, 124, 180),
    'BLUE': (50, 50, 255),
    'CYAN': (55, 202, 180),
    'GREEN': (55, 202, 18),
    'BROWN': (113, 49, 18),
    'DARKBLUE': (0, 36, 255),
    'LIGHTPURPLE': (178, 174, 255),
    'DARKPURPLE': (178, 53, 255),
}

DAY9YELLOW = (255, 167, 26)

GOAL = (245, 163, 183)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLUE = (50, 50, 255)

DIRECTIONS = {
    'left':(0, 32),
    'right':(-32, 0),
    'up': (32, 0),
    'down':(-32, 0)
}

m = 21
n = 21

goal_x = 640
goal_y = 576

# List to hold all the sprites
all_sprite_list = pygame.sprite.Group()
clock = pygame.time.Clock()

            # x--->
           # 0 ------------------>                      21
maze = [    [1,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],  # 0      y
            [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],  # 1      |
            [1,0,1,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],  # 2    \ | /
            [1,0,1,0,0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,1,1,1],  # 3     \ /
            [1,0,1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],  # 4      `
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],  # 5
            [1,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],  # 6
            [1,0,0,1,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1,1,1],  # 7
            [1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,1,1,1],  # 8
            [1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],  # 9
            [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],  # 10
            [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,1,1,1],  # 11
            [1,0,0,0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,1,1,1],  # 12
            [1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],  # 13
            [1,0,0,0,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,1,1,1],  # 14
            [1,0,1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1],  # 15
            [1,1,1,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1],  # 16
            [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1],  # 17
            [1,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,0,0,1,1,1],  # 18
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1],  # 19
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1],  # 20
            [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,1,1]  ]  # 21

visited = [[[] for cell in line] for line in maze]

class Robot(pygame.sprite.Sprite):

    def __init__(self, x, y, id, color=DAY9YELLOW):
        # Call the parent's constructor
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([Size, Size])
        self.image.fill(color)

        # Make our top-left corner the passed-in location.
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x

        self.face = 5
        self.lhs = 4

        # Set speed vector
        self.change_x = 0
        self.change_y = 0

        self.walls = None
        self.goals = None
        self.space = None
        self.path = []
        self.id = id

    def update(self):
        """ Update the robot position. """
        # Move left/right=====
        self.rect.x += self.change_x

        if((self.change_x<0) & (maze[int(self.rect.x/32)][int(self.rect.y/32)+1] != 1)):
            print ("Going West, Turning Left")
            self.face = (self.face - 1) % 4
            self.lhs = (self.lhs - 1) % 4


        if((self.change_x>0) & (maze[int(self.rect.x/32)][int(self.rect.y/32)-1] != 1)):
            print ("Going East, Turning Left")
            self.face = (self.face - 1) % 4
            self.lhs = (self.lhs - 1) % 4


        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Wall to the east
            if ((self.change_x > 0) & (self.face %4 == 1)):
                if((maze[int(self.rect.x/32)][int(self.rect.y/32)] == 0)):
                    print("what")
                self.rect.x -= self.change_x
                print ("You've hit a wall at the East")
                self.rect.right = block.rect.left
                print ("Turning Right")
                self.face = (1 + self.face ) % 4
                self.lhs = (1 + self.lhs) % 4

            # Wall to the west
            elif ((self.change_x < 0) & (self.face %4 ==3)):
                self.rect.x -= self.change_x
                print ("You've hit a wall at the West!")
                self.rect.left = block.rect.right
                print ("Turning Right")
                self.face = (self.face + 1) % 4
                self.lhs = (1 + self.lhs) % 4


        self.rect.y += self.change_y

        if((self.change_y>0) & (maze[int(self.rect.x/32)+1][int(self.rect.y/32)] != 1)):
            print ("Going South, Turning Left")
            self.face = (self.face - 1) % 4
            self.lhs = (self.lhs - 1) % 4


        if((self.change_y<0) & (maze[int(self.rect.x/32)-1][int(self.rect.y/32)] != 1)):
            print ("Going North, Turning Left")
            self.face = (self.face - 1) % 4
            self.lhs = (self.lhs - 1) % 4

        block_hit_list = pygame.sprite.spritecollide(self, self.walls, False)
        for block in block_hit_list:

            # Wall to the South
            if ((self.change_y > 0) & (self.face %4 == 2)):
                self.rect.y -= self.change_y
                print ("You've hit a wall at the South!")
                self.rect.bottom = block.rect.top
                print ("Turning Right")
                self.face = (1 + self.face ) % 4
                self.lhs = (1 + self.lhs) % 4

            # Wall to the North
            elif ((self.change_y < 0) & (self.face %4 == 0)):
                self.rect.y -= self.change_y
                print ("You've hit a wall at the North!")
                self.rect.top = block.rect.bottom
                print ("Turning Right")
                self.face = (self.face + 1) % 4
                self.lhs = (1 + self.lhs) % 4

        if(self.rect.x == goal_x) & (self.rect.y == goal_y):
            print("You've solved the maze! Hooray!!!")
            pygame.quit()
            sys.exit(0)

        visited[self.rect.x/32][self.rect.y/32].append(self.id)
        self.change_x = 0
        self.change_y = 0




# Left-Hand Rule wall following algorithm
def LHRwallFollowing(robot, screen):
    face = robot.face # 0 is north, 1 is east, 2 is south, 3 is west
    LHS = robot.lhs
    position = robot

    robot.change_x = random.choice([32, -32])
    robot.change_y = random.choice([32, -32])
    # #lhs is north
    # if(LHS%4 == 0):
    #     print("Current Position: (", int((robot.rect.x/32)+2),", ", int((robot.rect.y/32)-1), ") --Going East")
    #     robot.change_x += SPEED

    # #lhs is east
    # if(LHS%4 == 1):
    #     print("Current Position: (", int((robot.rect.x/32)+2),", ", int((robot.rect.y/32)-1), ") --Going South")
    #     robot.change_y += SPEED

    # #lhs is south
    # if(LHS%4 == 2):
    #     print("Current Position: (",  int((robot.rect.x/32)+2),", ", int((robot.rect.y/32)-1), ") --Going West")
    #     robot.change_x += -SPEED

    # #lhs is west
    # if(LHS%4 == 3):
    #     print("Current Position: (",  int((robot.rect.x/32)+2), ", ", int((robot.rect.y/32)-1), ") --Going North")
    #     robot.change_y += -SPEED


def create_entities():
    # Make the walls. (x_pos, y_pos, width, height)
    wall_list = pygame.sprite.Group()

    # Make the goal. (x_pos, y_pos, width, height)
    goal_list = pygame.sprite.Group()

    # Make the space. (x_pos, y_pos, width, height)
    space_list = pygame.sprite.Group()

    # robots
    robots = pygame.sprite.Group()

    for j in range(0, n):
        for i in range(0, m):
            if(maze[i][j] == 1):
                wall = Wall(i*32, j*32, Size, Size)
                wall_list.add(wall)
                all_sprite_list.add(wall)
            if(maze[i][j] == 2):
                goal = Goal(i*32, j*32, Size, Size)
                goal_list.add(wall)
                all_sprite_list.add(goal)
            if(maze[i][j] == 0):
                space = Space(i*32, j*32, Size, Size)
                space_list.add(space)
                all_sprite_list.add(space)

    for index, color in enumerate(COLORS.values()):
        robot = Robot(-64, 32, index, color=color)
        robot.face = 1
        robot.lhs = 0
        robot.walls = wall_list
        robot.goals = goal_list
        robot.space = space_list

        robots.add(robot)
        all_sprite_list.add(robot)

    return wall_list, goal_list, space_list, robots, all_sprite_list


def init_game():
    pygame.init()
    size = width, height = 640, 640
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Maze Solving Project by William Z.')

    background = pygame.Surface(screen.get_size())
    background = background.convert()
    background.fill(WHITE)

    return screen


def move_robots(robots, screen, movement_function=LHRwallFollowing):
    for robot in robots:
        movement_function(robot, screen)

def main():
    screen = init_game()
    _, _, _, robots, all_sprite_list = create_entities()

    clock = pygame.time.Clock()

    done = False

    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        move_robots(robots, screen, LHRwallFollowing)

        all_sprite_list.update()

        screen.fill(GREY)

        all_sprite_list.draw(screen)

        pygame.display.flip()

        clock.tick(60)
        pygame.time.wait(timer)

    pygame.quit()

if __name__ == '__main__':
    main()
