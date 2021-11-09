from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import png
import math



# Some api in the chain is translating the keystrokes to this octal string
# so instead of saying: ESCAPE = 27, we use the following.
ESCAPE = b'\033'

# Number of the glut window.
window = 0

# Rotations for cube. 
xrot = yrot = zrot = 0
dx = 0.9
dy = 0.9
dz = 0

N=50
asol = alua = aterra = 0
dsol = 1
dlua = 1
dterra = 1

atranslua = atransterra = 0
dtranslua = 1
dtransterra = 1

def f(u, v, R):
    theta = v*(math.pi)/(N-1) - math.pi/2
    phi = u*(2*math.pi)/(N-1)

    x = R*math.cos(theta)*math.cos(phi)
    y = R*math.cos(theta)*math.sin(phi)
    z = R*math.sin(theta)
    return x, y, z

# texture = []

def LoadTextures():
    global texture
    texture = glGenTextures(3) 

    glBindTexture(GL_TEXTURE_2D, texture[0])
    reader = png.Reader(filename='mapa.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    ################################################################################
    glBindTexture(GL_TEXTURE_2D, texture[1])
    reader = png.Reader(filename='sun2.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    ################################################################################
    glBindTexture(GL_TEXTURE_2D, texture[2])
    reader = png.Reader(filename='moon.png')
    w, h, pixels, metadata = reader.read_flat()
    if(metadata['alpha']):
        modo = GL_RGBA
    else:
        modo = GL_RGB
    glPixelStorei(GL_UNPACK_ALIGNMENT,1)
    glTexImage2D(GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL_UNSIGNED_BYTE, pixels.tolist())
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    ################################################################################


def InitGL(Width, Height):             
    LoadTextures()
    glEnable(GL_TEXTURE_2D)
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)               
    glEnable(GL_DEPTH_TEST)            
    glShadeModel(GL_SMOOTH)            
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
    if Height == 0:                        
        Height = 1
    glViewport(0, 0, Width, Height)      
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
    global xrot, yrot, zrot, texture, atransterra, atranslua, alua, asol, aterra

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)    
    glLoadIdentity()                   
    glClearColor(0.0,0.0,0.0,0.0)            
    glTranslatef(0.0,0.0,-7.0)
    glRotatef(xrot,1.0,0.0,0.0)          
    glRotatef(yrot,0.0,1.0,0.0)           
    glRotatef(zrot,0.0,0.0,1.0) 

    #-SOL  
    glRotatef(asol,0,-1,0)

    glBindTexture(GL_TEXTURE_2D, texture[1])
    draw_esfera(1)

    #-TERRA
    glRotatef(atransterra,0,1,0,)
    glTranslatef(2,0,0)
    glRotatef(aterra,0,1,0,)
    glPushMatrix()
    glRotatef(90,1,0,0,)

    glBindTexture(GL_TEXTURE_2D, texture[0])
    draw_esfera(0.5)
    glPopMatrix()

    #-LUA
    glRotatef(atranslua,0,1,0,)
    glTranslatef(1 ,0,0)
    glRotatef(alua,0,1,0,)

    glBindTexture(GL_TEXTURE_2D, texture[2])
    draw_esfera(0.2)

    xrot = xrot + 0.01                # X rotation
    yrot = yrot + 0.01                 # Y rotation
    zrot = zrot + 0.01                 # Z rotation

    asol += dsol
    alua += dlua
    aterra += dterra

    atranslua += dtranslua
    atransterra += dtransterra

    glutSwapBuffers()


def draw_esfera(R):
        glBegin(GL_TRIANGLE_STRIP)
        for i in range(N):
            for j in range(N):
                glTexCoord2f(i/(N-1), j/(N-1))
                glVertex3fv(f(i,j,R))
                glTexCoord2f((i+1)/(N-1), j/(N-1))
                glVertex3fv(f(i+1,j,R))
        glEnd()

def keyPressed(tecla, x, y):
    global dx, dy, dz
    if tecla == ESCAPE:
        glutLeaveMainLoop()
    elif tecla == b'x' or tecla == b'X':
        dx = 1.0
        dy = 0
        dz = 0   
    elif tecla == b'y' or tecla == b'Y':
        dx = 0
        dy = 1.0
        dz = 0   
    elif tecla == b'z' or tecla == b'Z':
        dx = 0
        dy = 0
        dz = 1.0

def teclaEspecialPressionada(tecla, x, y):
    global xrot, yrot, zrot, dx, dy, dz
    if tecla == GLUT_KEY_LEFT:
        print ("ESQUERDA")
        yrot += dy                 # Y rotation               
    elif tecla == GLUT_KEY_RIGHT:
        print ("DIREITA")
        yrot -= dy                 # Y rotation                   
    elif tecla == GLUT_KEY_UP:
        print ("CIMA")
        xrot -= dx                # X rotation  
    elif tecla == GLUT_KEY_DOWN:
        print ("BAIXO")
        xrot += dx                # X rotation
         

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)    
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    glutCreateWindow("MiniSistema")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glutSpecialFunc(teclaEspecialPressionada)
    InitGL(640, 480)
    glutMainLoop()


main()