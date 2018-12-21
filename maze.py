import turtle
import random

#setup maze window
maze = turtle.Screen()
maze.bgcolor("black")
maze.title("Maze")

#register GIF files as shapes, all 24x24 px
turtle.register_shape("wall2424.gif")
turtle.register_shape("vanellope2424.gif")
turtle.register_shape("cookie2424.gif")
turtle.register_shape("bowser2424.gif")

#class for walls
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wall2424.gif")
        #self.color("blue")
        self.penup()
        #fastest speed
        self.speed()
        
#class for treasures
class Treasure(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("cookie2424.gif")
        #self.color("gold")
        self.penup()
        self.speed(0)
        self.gold = 100
        self.goto(x, y)

    def destroy(self):
        self.goto(2000,2000)
        self.hideturtle()

#class for the player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("vanellope2424.gif")
        #self.color("white")
        self.penup()
        #fastest speed
        self.speed(0)
        self.gold = 0

    def goUp(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def goDown(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def goRight(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)

    def goLeft(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
    
    #this function is called if player is colliding with another element, e.g. enemy or treasure
    def isCollision (self, other):
        if self.xcor() == other.xcor() and self.ycor() == other.ycor():
            return True
        else:
            return False

#class definition for enemy
class Enemy(turtle.Turtle):
    def __init__(self, x, y):
        turtle.Turtle.__init__(self)
        self.shape("bowser2424.gif")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.direction = random.choice(["up", "down", "left", "right"])
    
    #definition for enemy movement 
    def move(self):
        if self.direction == "up":
            dx = 0
            dy = 24
        elif self.direction == "down":
            dx = 0
            dy = -24
        elif self.direction == "right":
            dx = 24
            dy = 0
        elif self.direction == "left":
            dx = -24
            dy = 0
        else:
            dx = 0
            dy = 0

        move_to_x = self.xcor() + dx
        move_to_y = self.ycor() + dy

        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
        else:
            self.direction = random.choice(["up", "down", "left", "right"])

        turtle.ontimer(self.move, t=random.randint(100,300))

#this function helps paint your level
def mazeSetup(level):
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]

            screen_x = -288 + (x * 24)
            screen_y = 240 - (y * 24)

            if character == "X":
                pen.goto(screen_x,screen_y)
                #puts square on the screen
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == "P":
                player.goto(screen_x,screen_y)
                #player.stamp()

            if character == "T":
                treasures.append(Treasure(screen_x, screen_y))

            if character == "E":
                enemies.append(Enemy(screen_x, screen_y))

            if character == "Y":
                exits.append((screen_x, screen_y))

#your level design                 
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXX",
    "P  XXXXXXX         XXXXX",
    "X  XXXXXXX  XXXXX  XXXXX",
    "X       XX  XXXXX  XXXXX",
    "XXXXXX  XX  XXX       XX",
    "XXXXXX  XX  XXX       XX",
    "XXXXXX  XX  XXXXXXE XXXX",
    "XXXXXX  XX     XXX  XXXX",
    "X  XX       X  XXXT XXXX",
    "X    XXXXXXXX   XX     X",
    "XXX  XXXXXXXX   XX   XXX",
    "XXT   XXXXX      XX XXXX",
    "XXXX  XXXXXXXXX  XXXXXXX",
    "XX      XXXXT      E   X",
    "XX  XXXXX     XX  XXXXXX",
    "XXE    XX   XXXX  XXXXXX",
    "XXXXXE XX  XXXX      XXX",
    "XXXXX  XX  XXXXXXXX  XXX",
    "XXXXX      XXX       XXX",
    "XXXXXXXXYYYXXXXXXXXXXXXX"
]

walls = []
treasures = []
enemies = []
exits = []

pen = Pen()
player = Player()

mazeSetup((level_1))

turtle.listen()
turtle.onkey(player.goLeft, "Left")
turtle.onkey(player.goRight, "Right")
turtle.onkey(player.goUp, "Up")
turtle.onkey(player.goDown, "Down")

for enemy in enemies:
    turtle.ontimer(enemy.move, t=250)

while True:
    for treasure in treasures:
        if player.isCollision(treasure):
            player.gold += treasure.gold
            treasure.destroy()
            treasures.remove(treasure)

    for enemy in enemies:
        if player.isCollision(enemy):
            screen_x = -288
            screen_y = 240 - (24)
            player.goto(screen_x, screen_y)

    for exit in exits:
        if player.position == exit:
            print("YEY")

    maze.update()
