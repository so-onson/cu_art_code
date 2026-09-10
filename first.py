import turtle

# Настройка окна
screen = turtle.Screen()
screen.title("Фракталы")
screen.bgcolor("black")

t = turtle.Turtle()
t.speed(0)
t.color("white")
t.hideturtle()

# -------------------------------
# 1. Фрактальное дерево
# -------------------------------

def tree(length, angle, level):
    if level == 0:
        return

    t.forward(length)

    t.left(angle)
    tree(length * 0.7, angle, level - 1)

    t.right(angle * 2)
    tree(length * 0.7, angle, level - 1)

    t.left(angle)
    t.backward(length)


# -------------------------------
# 2. Кривая Коха
# -------------------------------

def koch(length, level):
    if level == 0:
        t.forward(length)
        return

    length /= 3

    koch(length, level - 1)

    t.left(60)
    koch(length, level - 1)

    t.right(120)
    koch(length, level - 1)

    t.left(60)
    koch(length, level - 1)


def snowflake(length, level):
    for _ in range(3):
        koch(length, level)
        t.right(120)


# -------------------------------
# 3. Треугольник Серпинского
# -------------------------------

def sierpinski(length, level):
    if level == 0:
        for _ in range(3):
            t.forward(length)
            t.left(120)
        return

    length /= 2

    sierpinski(length, level - 1)

    t.forward(length)

    sierpinski(length, level - 1)

    t.backward(length)
    t.left(60)
    t.forward(length)
    t.right(60)

    sierpinski(length, level - 1)

    t.left(60)
    t.backward(length)
    t.right(60)


# -------------------------------
# 4. Квадратный фрактал
# -------------------------------

def square_fractal(size, level):
    if level == 0:
        return

    for _ in range(4):
        t.forward(size)
        t.left(90)

    # Переходим к следующему уровню
    t.forward(size / 3)

    square_fractal(size / 3, level - 1)


# -------------------------------
# Меню
# -------------------------------

print("Выберите фрактал:")
print("1 — Фрактальное дерево")
print("2 — Снежинка Коха")
print("3 — Треугольник Серпинского")
print("4 — Квадратный фрактал")

choice = input("Ваш выбор: ")

t.penup()
t.goto(0, -250)
t.pendown()

if choice == "1":
    t.left(90)
    tree(150, 25, 8)

elif choice == "2":
    t.penup()
    t.goto(-250, 150)
    t.pendown()
    snowflake(500, 4)

elif choice == "3":
    t.penup()
    t.goto(-250, -200)
    t.pendown()
    sierpinski(500, 6)

elif choice == "4":
    t.penup()
    t.goto(-200, -200)
    t.pendown()
    square_fractal(400, 5)

else:
    print("Неверный выбор")

turtle.done()