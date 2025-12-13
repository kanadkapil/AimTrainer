from ursina import *

app = Ursina()
e = Entity(model="cube", color=color.red)


def update():
    e.rotation_y += 1


app.run()
