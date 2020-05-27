import turtle

# Window
window = turtle.Screen()
window.bgcolor("black")
window.setup(width=1000, height=600)
window.tracer(0)
window.title("Pong")

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, -250)
pen.write("Left: 0          Right: 0", align="center", font=("Courier", 24, "normal"))

# Ball
ball = turtle.Turtle()
ball.speed(0)
ball.shape("square")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = .2
ball.dy = .2

window.listen()

# Left Racket
leftRacket = turtle.Turtle()
leftRacket.speed(0)
leftRacket.shape("square")
leftRacket.color("white")
leftRacket.shapesize(stretch_wid=5, stretch_len=1)
leftRacket.penup()
leftRacket.goto(-440, 0)


def leftRacketUp():
    y = leftRacket.ycor()
    y += 45
    leftRacket.sety(y)


def leftRacketDown():
    y = leftRacket.ycor()
    y -= 45
    leftRacket.sety(y)


window.onkeypress(leftRacketUp, "w")
window.onkeypress(leftRacketDown, "s")

# Right Racket
rightPaddle = turtle.Turtle()
rightPaddle.speed(0)
rightPaddle.shape("square")
rightPaddle.color("white")
rightPaddle.shapesize(stretch_wid=5, stretch_len=1)
rightPaddle.penup()
rightPaddle.goto(440, 0)


def rightRacketUp():
    y = rightPaddle.ycor()
    y += 45
    rightPaddle.sety(y)


def rightRacketDown():
    y = rightPaddle.ycor()
    y -= 45
    rightPaddle.sety(y)


window.onkeypress(rightRacketUp, "Up")
window.onkeypress(rightRacketDown, "Down")

leftScore = 0
rightScore = 0
while True:
    window.update()

    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Height Borders
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1


    elif ball.ycor() < -290:
        ball.sety(-290)
        ball.dy *= -1

    # Width Border
    if ball.xcor() > 450:
        leftScore += 1
        pen.clear()
        pen.write("Left: {}          Right: {}".format(leftScore, rightScore), align="center",
                  font=("Courier", 24, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1

    elif ball.xcor() < -450:
        rightScore += 1
        pen.clear()
        pen.write("Left: {}          Right: {}".format(leftScore, rightScore), align="center",
                  font=("Courier", 24, "normal"))
        ball.goto(0, 0)
        ball.dx *= -1

    if ball.xcor() < -440 and ball.ycor() < leftRacket.ycor() + 60 and ball.ycor() > leftRacket.ycor() - 60:
        ball.dx *= -1


    elif ball.xcor() > 440 and ball.ycor() < rightPaddle.ycor() + 60 and ball.ycor() > rightPaddle.ycor() - 60:
        ball.dx *= -1
