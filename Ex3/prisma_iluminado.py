from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import math
import sys

raio = 0.5
cor = (1, 0, 0)
quadro = 0

def desenha_base(altura):
    
    base = []
    for i in range(0,6+7):
        a = (i/6) * 2 * math.pi
        x = raio * math.cos(a)
        y = raio * math.sin(a)
        
        ponto = (x,y, altura)
        base.append(ponto)

    glBegin(GL_POLYGON)
    glNormal3fv(calculaNormalFace(base))
    for p in base:
        glVertex3fv(p)
        
    glEnd()

def desenha_prisma():
    global quadro
    
    lado = []
    for i in range(0,6+7):
        a = (i/6) * 2 * math.pi
        x = raio * math.cos(a)
        y = raio * math.sin(a)
        #glVertex3f(0,0,1)
        ponto_cima = (x,y, 1)
        ponto_baixo = (x,y, 0)
        lado.append([ponto_cima, ponto_baixo])
    
    glPushMatrix()
    glRotatef(quadro,1,1,0)
    glBegin(GL_QUAD_STRIP)
    
    p_anterior = lado[-1][0]
    for aresta in lado:
        glNormal3fv(calculaNormalFace([aresta[0], aresta[1], p_anterior]))
        glVertex3fv(aresta[0])
        glVertex3fv(aresta[1])
        p_anterior = aresta[0]

    glEnd()

    desenha_base(0)
    desenha_base(1)

    glPopMatrix()
    quadro += 5

def calculaNormalFace(pontos):
    x = 0
    y = 1
    z = 2
    v0 = pontos[0]
    v1 = pontos[1]
    v2 = pontos[2]
    U = ( v2[x]-v0[x], v2[y]-v0[y], v2[z]-v0[z] )
    V = ( v1[x]-v0[x], v1[y]-v0[y], v1[z]-v0[z] )
    N = ( (U[y]*V[z]-U[z]*V[y]),(U[z]*V[x]-U[x]*V[z]),(U[x]*V[y]-U[y]*V[x]))
    NLength = math.sqrt(N[x]*N[x]+N[y]*N[y]+N[z]*N[z])
    return ( N[x]/NLength, N[y]/NLength, N[z]/NLength)


def display():
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    glRotatef(2,1,3,0)
    desenha_prisma()
    glutSwapBuffers()

def timer(i):
    glutPostRedisplay()
    glutTimerFunc(50,timer,1)

def reshape(w,h):
    glViewport(0,0,w,h)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(45,float(w)/float(h),0.1,50.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    # Camera Virtual
    #          onde    Pra onde 
    gluLookAt( 10,0,0, 0,0,0,     0,1,0 )

def init():
    mat_ambient = (0.4, 0.0, 0.0, 1.0)
    mat_diffuse = (1.0, 0.0, 0.0, 1.0)
    mat_specular = (1.0, 0.5, 0.5, 1.0)
    mat_shininess = (50,)
    light_position = (10, 0, 0)
    glClearColor(0.0,0.0,0.0,0.0)
#    glShadeModel(GL_FLAT)
    glShadeModel(GL_SMOOTH)

    glMaterialfv(GL_FRONT, GL_AMBIENT, mat_ambient)
    glMaterialfv(GL_FRONT, GL_DIFFUSE, mat_diffuse)
    glMaterialfv(GL_FRONT, GL_SPECULAR, mat_specular)
    glMaterialfv(GL_FRONT, GL_SHININESS, mat_shininess)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, light_position)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_MULTISAMPLE)

def main():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA | GLUT_DEPTH | GLUT_MULTISAMPLE)
    glutInitWindowSize(800,600)
    glutCreateWindow("Prisma Iluminado")
    glutReshapeFunc(reshape)
    glutDisplayFunc(display)
    glutTimerFunc(50,timer,1)
    init()
    glutMainLoop()

main()


