import pygame
import random

BLACK = (0, 0, 0)


class Maze:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.visited = [[False for i in range(width)] for i in range(height)]
        self.walls = [[[True, True, True, True] for i in range(width)] for i in range(height)]

        self.dfs()
        self.walls[0][1][1], self.walls[height-1][width-2][2] = False, False

    def dfs(self):
        def is_valid(arr):
            if 0 <= arr[1] < self.width and 0 <= arr[2] < self.height:
                return not self.visited[arr[2]][arr[1]]

        stack = [[1, 0]]

        while stack:
            x, y = stack[-1]
            self.visited[y][x] = True
            neighbours = [[0, x - 1, y], [1, x, y - 1], [2, x, y + 1], [3, x + 1, y]]  # l, u, d, r
            valid_neighbours = list(filter(is_valid, neighbours))
            if valid_neighbours:
                count, next_x, next_y = random.choice(valid_neighbours)
                stack.append([next_x, next_y])
                self.walls[y][x][count] = False
                self.walls[next_y][next_x][3 - count] = False
            else:
                del stack[-1]

    def display(self, screen, side_len=30, pad_x=20, pad_y=20, width=5):
        for y in range(len(self.walls)):
            for x, (left, up, down, right) in enumerate(self.walls[y]):
                if left:
                    start, end = (x*side_len+pad_x, y*side_len+pad_y), (x*side_len+pad_x, (y+1)*side_len+pad_y)
                    pygame.draw.line(screen, BLACK, start, end, width)
                if up:
                    start, end = (x*side_len+pad_x, y*side_len+pad_y), ((x+1)*side_len+pad_x, y*side_len+pad_y)
                    pygame.draw.line(screen, BLACK, start, end, width)
                if down:
                    start, end = (x*side_len+pad_x, (y+1)*side_len+pad_y), ((x+1)*side_len+pad_x, (y+1)*side_len+pad_y)
                    pygame.draw.line(screen, BLACK, start, end, width)
                if right:
                    start, end = ((x+1)*side_len+pad_x, y*side_len+pad_y), ((x+1)*side_len+pad_x, (y+1)*side_len+pad_y)
                    pygame.draw.line(screen, BLACK, start, end, width)


def initialise(width, height):
    pygame.init()
    screen = pygame.display.set_mode([width, height])
    return screen


def display(screen, maze, side_len):
    screen.fill((255, 255, 255))
    maze.display(screen, side_len=side_len)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main_screen = initialise(1000, 1000)
    maze = Maze(96, 96)
    display(main_screen, maze, side_len=10)
    pygame.quit()
