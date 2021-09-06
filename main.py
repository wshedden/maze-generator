import pygame
import random

BLACK = (0, 0, 0)


class Maze:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.visited = [[False for i in range(width)] for i in range(height)]
        self.walls = [[[True, True, True, True] for i in range(width)] for i in range(height)]

        self.dfs(1, 0)
        self.walls[0][1][1], self.walls[height-1][width-2][2] = False, False

    def dfs(self, x, y):
        self.visited[y][x] = True
        neighbours = [[0, x-1, y], [1, x, y-1], [2, x, y+1], [3, x+1, y]]  # l, u, d, r
        random.shuffle(neighbours)
        for count, next_x, next_y in neighbours:
            if 0 <= next_x < self.width and 0 <= next_y < self.height:
                if not self.visited[next_y][next_x]:
                    self.walls[y][x][count] = False
                    self.walls[next_y][next_x][3-count] = False
                    self.dfs(next_x, next_y)

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



def initialise():
    pygame.init()
    screen = pygame.display.set_mode([1000, 800])
    return screen


def display(screen, maze):
    screen.fill((255, 255, 255))
    maze.display(screen)
    pygame.display.flip()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    main_screen = initialise()
    maze = Maze(50, 50)
    display(main_screen, maze)
    pygame.quit()
