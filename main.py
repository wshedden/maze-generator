import pygame
import random
import sys

BLACK = (0, 0, 0)
BLUE = (64, 106, 189)
PAD = 20


class Maze:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.visited = [[False for i in range(width)] for i in range(height)]
        self.walls = [[[True, True, True, True] for i in range(width)] for i in range(height)]
        self.flags = [[False for i in range(width)] for i in range(height)]  # for solving
        self.flags[self.height-1][self.width-2] = True
        self.walls[0][1][1], self.walls[height-1][width-2][2] = False, False
        self.dfs()

    def dfs(self):
        def is_valid(arr):
            if 0 <= arr[1] < self.width and 0 <= arr[2] < self.height:
                return not self.visited[arr[2]][arr[1]]

        def is_flag(arr):
            return self.flags[arr[2]][arr[1]]

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
                if stack:
                    self.flags[stack[-1][1]][stack[-1][0]] = self.flags[stack[-1][1]][stack[-1][0]] or self.flags[y][x]

    def display(self, screen, side_len=30, width=5):
        for y in range(len(self.walls)):
            for x, (left, up, down, right) in enumerate(self.walls[y]):
                if self.flags[y][x]:
                    pygame.draw.rect(screen, BLUE, (x*side_len+PAD, y*side_len+PAD, side_len+1, side_len+1))
                lines = []
                l_x, r_x, t_y, b_y = x*side_len+PAD, (x+1)*side_len+PAD, y*side_len+PAD, (y+1)*side_len+PAD
                if left:
                    lines.append([(l_x, t_y), (l_x, b_y)])
                if up:
                    lines.append([(l_x, t_y), (r_x, t_y)])
                if down:
                    lines.append([(l_x, b_y), (r_x, b_y)])
                if right:
                    lines.append([(r_x, t_y), (r_x, b_y)])
                for start, end in lines:
                    pygame.draw.line(screen, BLACK, start, end, width)


def initialise(width, height):
    pygame.init()
    screen = pygame.display.set_mode([width, height])
    return screen


def display_maze(screen, maze, side_len):
    screen.fill((255, 255, 255))
    maze.display(screen, side_len=side_len, width=2)
    pygame.display.flip()

    running = True
    while running:
        pygame.event.wait()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


if __name__ == "__main__":
    try:
        x, y, side_len = [int(i) for i in sys.argv[1:]]
    except ValueError:
        print("Arguments not inputted; defaults used")
        print("x = 50\ny = 50\nside length = 10")
        x, y, side_len = 100, 100, 10

    width, height = 2 * PAD + side_len * x, 2 * PAD + side_len * y

    main_screen = initialise(width, height)
    maze = Maze(x, y)
    display_maze(main_screen, maze, side_len=side_len)
    pygame.quit()
