# SnakeAI
Snake with BFS and DFS simpel pathfinding

## Code
If you wanna to make yourself pathfind algorithm for snake simple overload `FakePlayer.update()` method
```
...
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
...
```
`proccess_movement` calling every frame
`update` will be call only when timer reach some var called as game speed:
```
# --- Game logic should go here
snake.process_movement()
if timer<5:
    timer+=1
else:
    snake.update()
    timer = 0
```
Otherwise if you want control snake manual from keyboard you need simply change father of Snake object to `RealPlayer`
```
...
class Snake(RealPlayer):
...
```

## To Do
- [ ] More pathfinding
