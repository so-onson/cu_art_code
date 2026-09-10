import turtle
import math

screen = turtle.Screen()
screen.setup(800, 800)
screen.title("16: волны Райли")
screen.tracer(0)                 # рисуем всё сразу

t = turtle.Turtle()
t.hideturtle()
t.pensize(2)

LINES = 144                      # сколько волн одна над другой
STEP = 5                         # расстояние между волнами
AMPLITUDE = 25                   # высота волны

for i in range(LINES):
    # 1) тон: светлый -> тёмный -> светлый, пока i идёт от 0 до 143
    angle = i * 2.5 + 90         # 144 линий * 2.5° = 360°: один цикл; +90 ставит тёмную полосу в середину
    g = 0.6 + 0.35 * math.sin(math.radians(angle))
    t.pencolor(g, g, g)

    # 2) сама волна: как в примере 15, только поднята на высоту этой линии
    base_y = -360 + i * STEP
    t.penup()
    for x in range(-360, 361, 1):
        y = base_y + AMPLITUDE * math.sin(math.radians(x * 2))
        t.goto(x, y)
        t.pendown()

screen.update()
# Попробуй: STEP = 3 и LINES = 240 (плотнее); i * 5 (тон гаснет дважды);
# x * 2 -> x * 3 (волны чаще); angle = i * 2.5 + 90 + x
# внутри цикла по x — тон поплывёт и по горизонтали.
screen.exitonclick()
turtle.done()