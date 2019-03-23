import pygame
import random
import numpy as np
import copy
from math import floor
from Graph.Graph import Graph

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

block_size = 32
sc_width = 8
sc_height = 8


pygame.init()
pygame.font.init() # you have to call this at the start,
                   # if you want to use this module.
myfont = pygame.font.SysFont('Comic Sans MS', 30)


# Set the width and height of the screen [width, height]
size = (block_size * sc_width, block_size * sc_height)
screen = pygame.display.set_mode(size)
pygame.display.update()

pygame.display.set_caption("My Game")

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

def dfs_paths(graph, start, end) -> list:
    '''
        finding all possible paths from start_node to end_node
        with dfs algorithm
        start - where to start node
        end - where to end node

        LIFO structure
    '''
    stack = [(start, [start])]
    while stack:
        (vertex, path) = stack.pop()
        for next in graph[vertex] - set(path):
            if next == end:
                yield path + [next]
            else:
                stack.append((next, path + [next]))

    return stack

def bfs_paths(graph, start, end) -> list:
    '''
        finding all possible path with bfs algo
        start - where to start
        end - where to end

        FIFO structure
    '''
    queue = [(start, [start])]
    while queue:
        (vertex, path) = queue.pop(0)
        for next in graph[vertex] - set(path):
            if next == end:
                yield path + [next]
            else:
                queue.append((next, path + [next]))

def to_my_coords(x, y, width):
    return width * y + x

def to_real_coords(num, width):
    y = floor(num / width)
    return num - width * y, y


class RealPlayer(object):
    def process_movement(self):
        events = pygame.event.get()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                Snake.last_tail.tail = Tail(Snake.last_tail.x, Snake.last_tail.y, Snake.last_tail)
                Snake.last_tail = Snake.last_tail.tail
            if event.key == pygame.K_LEFT:
                if self.direction!=3:
                    self.direction = 2
            elif event.key == pygame.K_RIGHT:
                if self.direction!=2:
                    self.direction = 3
            elif event.key == pygame.K_UP:
                if self.direction!=0:
                    self.direction = 1
            elif event.key == pygame.K_DOWN:
                if self.direction!=1:
                    self.direction = 0


class FakePlayer(object):
    def __init__(self):
        self.current_path = list()
        self.graph = dict()
        m = np.zeros((sc_width,sc_height))
        #generate self graph
        counter = 0
        for i in m:
            line_counter = 0
            for j in i:
                nodes = set()
                x1 = counter - 1 if counter - 1 >= 0 and line_counter > 0 else None
                if x1 is not None:
                    nodes.add(x1)
                x2 = counter + 1 if counter + 1 <= sc_width * sc_height and line_counter+1<sc_width else None
                if x2 is not None:
                    nodes.add(x2)
                y1 = counter + sc_width if counter + sc_width < sc_width * sc_height else None
                if y1 is not None:
                    nodes.add(y1)
                y2 = counter - sc_width if counter - sc_width >= 0 else None
                if y2 is not None:
                    nodes.add(y2)
                self.graph.update({counter: nodes})
                counter+=1
                line_counter +=1

    def create_path(self, dfs = False, bfs = False):
        where_to_start = to_my_coords(self.x, self.y, sc_width)
        where_to_end = to_my_coords(Snake.meal.x, Snake.meal.y, sc_width)

        delete_coords = [to_my_coords(i.x, i.y, sc_width) for i in Snake.tail_list]
        new_graph = copy.deepcopy(self.graph)
        for node, links in self.graph.items():
            for link in links:
                if link in delete_coords:
                    new_graph[node].remove(link)
            if node in delete_coords:
                del new_graph[node]

        if dfs:
            path = next(dfs_paths(new_graph, where_to_start, where_to_end))
            path.pop(0)
            return path
        if bfs:
            path = next(bfs_paths(new_graph, where_to_start, where_to_end))
            path.pop(0)
            return path

    def get_neighbours(self):
        my_coords = to_my_coords(self.x, self.y, sc_width)
        nodes = set()
        x1 = my_coords - 1 if my_coords - 1 >= 0 else None
        if x1 is not None and x1:
            nodes.add((2, x1))
        x2 = my_coords + 1 if my_coords + 1 <= sc_width * sc_height else None
        if x2 is not None and x2:
            nodes.add((3, x2))
        y1 = my_coords + sc_width if my_coords + sc_width < sc_width * sc_height else None
        if y1 is not None and y1:
            nodes.add((0, y1))
        y2 = my_coords - sc_width if my_coords - sc_width >= 0 else None
        if y2 is not None and y2:
            nodes.add((1, y2))

        return nodes

    def get_move_direction(self, neigh, go_to):
        for i in neigh:
            if i[1] == go_to:
                return i[0]

    def update(self):
        n = self.get_neighbours()
        move_to = self.current_path.pop(0)#self.current_path[0]
        direction = self.get_move_direction(n, move_to)
        self.direction = direction


    def process_movement(self):
        events = pygame.event.get()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                Snake.last_tail.tail = Tail(Snake.last_tail.x, Snake.last_tail.y, Snake.last_tail)
                Snake.last_tail = Snake.last_tail.tail
        if len(self.current_path)==0:
            self.current_path = self.create_path(bfs = True)


class Snake(FakePlayer):
    meal = None
    last_tail = None
    tail_list = list()

    def __init__(self):
        self.x = 1
        self.y = 1
        self.prev_x = self.x
        self.prev_y = self.y
        self.direction = 0 # 0 is down 1 is up 2 is left 3 is right
        self.length = 1
        self.tail = Tail(self.x-1, self.y, self)
        self.one_press = True
        self.stop = True
        Snake.last_tail = self.tail
        super(Snake, self).__init__()

    def draw(self):
        pygame.draw.rect(screen, BLACK, (self.x * block_size, self.y * block_size, block_size, block_size))
        if self.tail is not None:
            self.tail.draw()

    def convert_coords(self):
        return to_my_coords(self.x, self.y, sc_width)

    def update(self):
        if self.stop != False:
            super(Snake, self).update()
            self.prev_x = self.x
            self.prev_y = self.y
            if self.direction == 0:
                self.y+=1
            elif self.direction == 1:
                self.y-=1
            elif self.direction == 2:
                self.x-=1
            elif self.direction == 3:
                self.x+=1
            if self.tail is not None:
                self.tail.update()
            if Snake.meal == self:
                self.length += 1
                Snake.meal = Meal()
                Snake.last_tail.tail = Tail(Snake.last_tail.x, Snake.last_tail.y, Snake.last_tail)
                Snake.last_tail = Snake.last_tail.tail


class Tail(Snake):
    def __init__(self, x, y, father):
        self.x = x
        self.y = y
        self.prev_x = x
        self.prev_y = y
        self.father = father
        self.tail = None
        Snake.tail_list.append(self)

    def update(self):
        self.prev_x = self.x
        self.prev_y = self.y
        self.x = self.father.prev_x
        self.y = self.father.prev_y
        if self.tail:
            self.tail.update()

    def mark_self(self, m):
        m[self.y][self.x] = 1
        if self.tail:
            m = self.tail.mark_self(m)
        return m


class Meal(object):
    def __init__(self):
        delete_coords = set([i.convert_coords() for i in Snake.tail_list])
        possible_coords = set([i for i in range(0, sc_width*sc_height, 1)]) - delete_coords
        rnd = random.choice(tuple(possible_coords))
        self.x, self.y = to_real_coords(rnd, sc_width)

    def draw(self):
        pygame.draw.rect(screen, RED, (self.x * block_size, self.y * block_size, block_size, block_size))

    def __eq__(self, other):
        if other.x == self.x and other.y == self.y:
            return True
        else:
            return False

def text_to_screen(screen, text, x, y, size = 50,
            color = (0, 0, 0), font_type = 'data/fonts/orecrusherexpand.ttf'):
    try:

        text = str(text)
        font = pygame.font.SysFont('Comic Sans MS', size)
        text = font.render(text, True, color)
        screen.blit(text, (x, y))

    except Exception as e:
        print('Font Error, saw it coming')
        raise e

# -------- Main Program Loop -----------
snake = Snake()
Snake.meal = Meal()
timer = 0
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # --- Game logic should go here
    snake.process_movement()
    if timer<3:
        timer+=1
    else:
        snake.update()
        timer = 0

    # --- Screen-clearing code goes here
    screen.fill(WHITE)


    # --- Drawing code should go here
    snake.draw()
    Snake.meal.draw()


    texts = [[None for i in range(sc_width)] for j in range(sc_height)]
    counter = 0
    '''for i in range(sc_width):
        for j in range(sc_height):
            text_to_screen(screen, str(counter), j*block_size,i*block_size, size = 16)
            counter+=1'''
    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock.tick(60)

# Close the window and quit.
pygame.quit()
