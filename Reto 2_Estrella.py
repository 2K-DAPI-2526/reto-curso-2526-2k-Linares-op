import turtle

def estrella(n, lado):
    t = turtle.Turtle()
    t.speed(3)

    angulo = 180 - 180/n

    for i in range(n):
        t.forward(lado)
        t.right(angulo)

pantalla = turtle.Screen()

estrella(9, 200)

turtle.done()