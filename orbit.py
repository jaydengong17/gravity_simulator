import tkinter
import random
import math
import tkinter.font as tkFont

WIDTH = 1200
HEIGHT = 900

root = tkinter.Tk()
root.title('nothing')

canvas = tkinter.Canvas(root,
                        bg='light slate gray',
                        height=HEIGHT,
                        width=WIDTH)
canvas.pack()

π = 3.1415926535
#grav_const = 0.02478287949
grav_const = 6

zoom = 1

helv36 = tkFont.Font(family='Apple Symbols', size=36)

timetext = canvas.create_text(10,
                              0,
                              anchor = tkinter.NW,
                              fill = "black",
                              text = "Days: 0",
                              font = helv36)
time = 0

# Format of the planet data:
#[id, x velocity, y velocity, x position, y position, mass, stationary, size]
objects = []  # A list of planets.


def createPlanet(
    x_position,
    y_position,
    x_velocity,
    y_velocity,
    mass,
    color,
    stationary,
    size
):
  global zoom

  id = canvas.create_oval((x_position - 600) / zoom + 600 + size,
                          (y_position - 450) / zoom + 450 + size,
                          (x_position - 600) / zoom + 600 - size,
                          (y_position - 450) / zoom + 450 - size,
                          fill = color)
  info = [id, x_velocity, y_velocity, x_position, y_position, mass, stationary]
  objects.append(info)


arrow_ids = []
def drawArrow(x0, y0, x_to, y_to, arrow_color):
  temporary_id = canvas.create_line(x0,
                                    y0,
                                    x0 + x_to,
                                    y0 + y_to,
                                    fill = str(arrow_color),
                                    arrow = tkinter.LAST,
                                    width = 3)
  arrow_ids.append(temporary_id)


# This is the setup that creates the solar system (up to jupiter).
# You can change the setup here.
createPlanet(600, 450, 0, 0, 333000, "yellow", 1, 13)
createPlanet(720, 450, 0, 8.1216, 0.0553, "gray", 0, 1)
createPlanet(810, 450, 0, -6.051456, 0.815, "orange", 0, 4)
createPlanet(900, 450, 0, 5.184, 1, "blue", 0, 5)
createPlanet(1050, 450, 0, 4.161024, 0.107, "red", 0, 2)
createPlanet(2160, 450, 0, 2.256768, 317.83, "beige", 0, 11)

# For debugging code (It creates a lot of planets inside a circle of radius 500)
#
# amount = 100
# for create in range(amount):
#   angle = random.uniform(-π, π)
#   radius = random.randint(-500, 500)
#   createPlanet(math.cos(angle) * radius + 600,
#                math.sin(angle) * radius + 450,
#                math.sin(angle) * radius / -100,
#                math.cos(angle) * radius / 100,
#                10, "gray", 0, 5)


def UpdateUniverse():
  global grav_const
  global time
  global zoom


  # clear all arrows from screen
  for id in arrow_ids:
    canvas.delete(id)

  for target in range(len(objects)):
    # Makes sure it isn't a stationary object
    if objects[target][6] == 0:
      # Collects data for accelearation arrows
      total_accel_x = 0
      total_accel_y = 0

      for others in range(len(objects)):

        distance_squared = (
          objects[others][3] - objects[target][3]) ** 2 + (
          objects[others][4] - objects[target][4]) ** 2

        # Gravitational acceleration
        if distance_squared != 0:
          # F_g = G * m1 * m2 / d^2, but we want the acceleration,
          # so we can divide both sides by m1 (if m1 is the object's mass)
          # because F = ma.
          accel_both = grav_const * objects[others][5] / distance_squared
          accel_x = (
            accel_both * (objects[others][3] - objects[target][3]) /
            math.sqrt(distance_squared)
          )
          accel_y = (
            accel_both * (objects[others][4] - objects[target][4]) /
            math.sqrt(distance_squared)
          )

          # Add acceleration to velocity
          objects[target][1] += accel_x
          objects[target][2] += accel_y

          total_accel_x += accel_x
          total_accel_y += accel_y

      # Draws acceleration arrow & velocity arrow for debugging
      #
      # drawArrow((objects[target][3] + objects[target][1] - 600) / zoom + 600,
      #           (objects[target][4]  + objects[target][2] - 450) / zoom + 450,
      #            total_accel_x * 1000,
      #            total_accel_y * 1000,
      #            "blue")
      # drawArrow(objects[target][3] + objects[target][1],
      #           objects[target][4] + objects[target][2],
      #           objects[target][1], objects[target][2], "red")

  # Update positions after all distances are calculated
  for target_2 in range(len(objects)):
    if objects[target_2][6] == 0:

      # Add velocity to position
      objects[target_2][3] += objects[target_2][1]
      objects[target_2][4] += objects[target_2][2]

      # Change the object's position (first argument is the id)
      canvas.moveto(objects[target_2][0],
                    (objects[target_2][3] - 600) / zoom + 600,
                    (objects[target_2][4] - 450) / zoom + 450)

  time += 1
  canvas.itemconfig(timetext, text = "Days: " + str(time))
  root.after(20, UpdateUniverse)


canvas.focus_set()

# This stuff is for UI. Not used right now.
# canvas.bind('<ButtonPress-1>', pressed)
# canvas.bind('<Motion>', tracker)
# canvas.bind('<ButtonRelease-1>', newObject)

# Update every 50ms.
root.after(50, UpdateUniverse)

# Start the main loop.
root.mainloop()
