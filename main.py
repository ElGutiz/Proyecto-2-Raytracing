from raytracing import *
import winsound

r = Raytracer(1000, 1000)
triangles_vertex = []
scene_figures = []

r.light = Light(
        position=V3(-5, -20, 10),
        intensity=2,
        color=color(255, 255, 200)
    )

white_cement = Material(diffuse=color(255, 255, 255), albedo=[0.9, 0.1, 0.0, 0], spec=10)
grey_cement = Material(diffuse=color(74, 73, 73), albedo=[0.9, 0.1, 0.0, 0], spec=10)
rock = Material(diffuse=color(54, 54, 54), albedo=[0.9, 0.1, 0, 0], spec=10)
colored_glass = Material(diffuse=color(54, 54, 54), albedo=[0.6, 0.3, 0.4, 0], spec=1500, refractive_index = 1.5)
wood = Material(diffuse=color(166, 108, 36), albedo=[0.9, 0.1, 0, 0], spec=10)
bush = Material(diffuse=color(45, 115, 24), albedo=[0.9, 0.1, 0, 0], spec=10)
grass = Material(diffuse=color(25, 54, 7), albedo=[0.9, 0.1, 0, 0], spec=10)

triangles_vertex = r.Load('./models/RockF.obj', (4.5, -14, -15), (1, 1, 1))

for triangle_vertex in triangles_vertex:
    scene_figures.append(Triangle(triangle_vertex, rock))

#PARTE SUPERIOR IZQUIERDO (RECTANGULO BLANCO)
for i in range(-7, -1):
    scene_figures.append(Cube(V3(i, 0, -10), 1, white_cement))
    scene_figures.append(Cube(V3(i, 0, -11), 1, white_cement))
    if i == -7:
        for j in range(-12, -9):
            scene_figures.append(Cube(V3(i, -1, j), 1, white_cement))
            scene_figures.append(Cube(V3(i, -2, j), 1, white_cement))
    else:
        scene_figures.append(Cube(V3(i, -1, -10), 1, glass))
        scene_figures.append(Cube(V3(i, -2, -10), 1, glass))             
                
    scene_figures.append(Cube(V3(i, -3, -10), 1, white_cement))

#PARTE INFERIOR IZQUIERDO (MADERA Y VIDRIOS)
for i in range(-6, -1):
    if i == -6 or i == -4 or i == -2:
        scene_figures.append(Cube(V3(i, 1, -11), 1, wood))
        scene_figures.append(Cube(V3(i, 2, -11), 1, wood))
        
    else:
        scene_figures.append(Cube(V3(i, 1, -11), 1, grey_cement))
        scene_figures.append(Cube(V3(i, 2, -11), 1, grey_cement))
      
#PARTE SUPERIR DERECHA (BALCON)
for i in range(3, 9):
    scene_figures.append(Cube(V3(i, 0, -10), 1, white_cement))

    if i == 8:
        scene_figures.append(Cube(V3(i, 1, -11), 1, wood))
        scene_figures.append(Cube(V3(i, 2, -11), 1, wood))
        scene_figures.append(Cube(V3(i, 3, -11), 1, wood))
        
for i in range(-16, -8):
    for j in range(4, 9):
        scene_figures.append(Cube(V3(j, 4, i), 1, rock))


#PARTE DE EN MEDIO (RECTANGULO GRIS OSCURO)
for i in range(-3, 4):
    scene_figures.append(Cube(V3(-1, i, -9), 1, grey_cement))
    scene_figures.append(Cube(V3(-1, i, -10), 1, grey_cement))
    scene_figures.append(Cube(V3(-1, i, -11), 1, grey_cement))
    if i == -3:
        scene_figures.append(Cube(V3(0, i, -9), 1, grey_cement))
        scene_figures.append(Cube(V3(1, i, -9), 1, grey_cement))
        scene_figures.append(Cube(V3(0, i, -10), 1, grey_cement))
        scene_figures.append(Cube(V3(1, i, -10), 1, grey_cement))
        scene_figures.append(Cube(V3(0, i, -11), 1, grey_cement))
        scene_figures.append(Cube(V3(1, i, -11), 1, grey_cement))
        
    scene_figures.append(Cube(V3(2, i, -9), 1, grey_cement))
    scene_figures.append(Cube(V3(2, i, -10), 1, grey_cement))
    scene_figures.append(Cube(V3(2, i, -11), 1, grey_cement))

for i in range(-3, 4):
    scene_figures.append(Cube(V3(0, i, -12), 1, grey_cement))
    scene_figures.append(Cube(V3(1, i, -12), 1, grey_cement))

for i in range(-12, -8):
    scene_figures.append(Cube(V3(0, 4, i), 1, wood))
    scene_figures.append(Cube(V3(1, 4, i), 1, wood))

#ARBUSTOS
for i in range(-7, -1):
    scene_figures.append(Cube(V3(i, 3, -10), 1, bush))
    if i == -7:
        scene_figures.append(Cube(V3(i, 3, -11), 1, bush))

scene_figures.append(Cube(V3(3, 3, -8), 1, bush))
scene_figures.append(Cube(V3(3, 3, -9), 1, bush))
scene_figures.append(Cube(V3(3, 3, -10), 1, bush))

for i in range(-16, -8):
    scene_figures.append(Cube(V3(9, 3, i), 1, bush))

#CALLE
for i in range(-8, -5):
    scene_figures.append(Cube(V3(0, 4, i), 1, rock))
    scene_figures.append(Cube(V3(1, 4, i), 1, rock))
    
for i in range(-6, 10):
    scene_figures.append(Cube(V3(i, 4, -5), 1, rock))
    scene_figures.append(Cube(V3(i, 4, -4), 1, rock))


r.scene = scene_figures

r.render()
r.write('Minecraft_Modern_House_Example.bmp')

duration = 2000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)