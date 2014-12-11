from OpenGL.GLUT import *
from OpenGL.GL   import *
from OpenGL.GLU  import *

import numpy as np
import sys

ESCAPE     = '\033'
window     = 0 #number of glut window

def InitGL(Width, Height): 
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)

def ReSizeGLScene(Width, Height):
    if Height == 0:
        Height == 1

    glViewport(0, 0, Width, Height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

def DrawGLScene():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glTranslatef(-1.5, 0.0, -6.0)   

    glBegin(GL_TRIANGLES)

    glColor3f(1.0, 0.0, 0.0)    # Red
    glVertex3f(0.0, 1.0, 0.0)   # Top of Triangle (Front)
    glColor3f(0.0, 1.0, 0.0)    # Green
    glVertex3f(-1.0, -1.0, 1.0) # Left of Triangle (Front)
    glColor3f(0.0, 0.0, 1.0)    # Blue
    glVertex3f(1.0, -1.0, 1.0)  # Right of Triangle (Front)

    glColor3f(1.0, 0.0, 0.0)    # Red
    glVertex3f(0.0, 1.0, 0.0)   # Top of Triangle (Right)
    glColor3f(0.0, 1.0, 0.0)    # Green
    glVertex3f(1.0, -1.0, 1.0)  # Left of Triangle (Right)
    glColor3f(0.0, 0.0, 1.0)    # Red
    glVertex3f(1.0, -1.0, -1.0) # Right of Triangle (Right)

    glColor3f(1.0, 0.0, 0.0)     # Red
    glVertex3f(0.0, 1.0, 0.0)    # Top of Triangle (Back)
    glColor3f(0.0, 1.0, 0.0)     # Green
    glVertex3f(1.0, -1.0, -1.0)  # Left of Triangle (Back)
    glColor3f(0.0, 0.0, 1.0)     # Red
    glVertex3f(-1.0, -1.0, -1.0) # Right of Triangle (Back)

    glColor3f(1.0, 0.0, 0.0)     # Red
    glVertex3f(0.0, 1.0, 0.0)    # Top of Triangle (Left)
    glColor3f(0.0, 1.0, 0.0)     # Green
    glVertex3f(-1.0, -1.0, -1.0) # Left of Triangle (Left)
    glColor3f(0.0, 0.0, 1.0)     # Red
    glVertex3f(-1.0, -1.0, 1.0)  # Right of Triangle (Left)

    glEnd()
    glutSwapBuffers()

def keyPressed(*args): # Called when a key is pressed. If esc is pressed, kill everything.
    if args[0] == ESCAPE:
        glutDestroyWindow(window)
        sys.exit()

    print args

def main():
    global window

    glutInit(sys.argv)

    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)

    glutInitWindowSize(640, 480)

    glutInitWindowPosition(0, 0)

    window = glutCreateWindow("practice on python")

    glutDisplayFunc(DrawGLScene)

#    glutFullScreen() # Eventually adding keyboard command

    glutIdleFunc(DrawGLScene) # When we are doing nothing redraw the scene. (?)

    # Register User Functions
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)

    InitGL(640, 480)

print "Hit ESC key to quit."

if __name__ == '__main__':
    try: 
        GLU_VERSION_1_2
    except:
        print "Error in weird try except statement.  If you don't get this error, comment out later"

    main()
    glutMainLoop()
