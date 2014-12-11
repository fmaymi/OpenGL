#!/usr/bin/env python

# TODO:
#
# 1. Load the x-face of data, and plot both x-face and y-face intersecting
# 2. Write a camera function (mapped to keys) that uses glRotate DONE
# 3. Put in some pretty color bars


import sys
import numpy as np

from OpenGL.GLUT import *
from OpenGL.GL   import *
from OpenGL.GLU  import *

ESCAPE = '\033'
module_vars = { 'texture_X': 0,
                'texture_Y': 0,
                'texture_Z': 0,
                'window_id': 0,
                'xrot' : 0.0,
                'yrot' : 0.0,
                'zrot' : 0.0,
                'x' : 0.0,
                'y' : 0.0,
                'zoom' : -6.0,
                'bar_setting' : 0,
                'bar_quant' : 6,
                'log_scale' : True}
filename = sys.argv[1]

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
    glTranslatef(module_vars['x'], module_vars['y'], module_vars['zoom'])
    glRotatef(module_vars['xrot'], 1.0, 0.0, 0.0)
    glRotatef(module_vars['yrot'], 0.0, 1.0, 0.0)
    glRotatef(module_vars['zrot'], 0.0, 0.0, 1.0)

    wx = module_vars['x_width']
    hx = module_vars['x_height']
    wy = module_vars['y_width']
    hy = module_vars['y_height']
    wz = module_vars['z_width']
    hz = module_vars['z_height']

    # x-slice of 3D jet sim
    glEnable(GL_TEXTURE_2D)
    glBindTexture(GL_TEXTURE_2D, module_vars['texture_X'])

    glBegin(GL_QUADS)
    glTexCoord2d(0, 0)
    glVertex(-0.5*wx, -0.5*hx, 0.0)
    glTexCoord2d(1, 0)
    glVertex(+0.5*wx, -0.5*hx, 0.0)
    glTexCoord2d(1, 1)
    glVertex(+0.5*wx, +0.5*hx, 0.0)
    glTexCoord2d(0, 1)
    glVertex(-0.5*wx, +0.5*hx, 0.0)
    glEnd()

    # y-slice of 3D jet sim
    glBindTexture(GL_TEXTURE_2D, module_vars['texture_Y'])

    glBegin(GL_QUADS)
    glTexCoord2d(0, 0)
    glVertex(0.0, -0.5*hy, -0.5*wy)
    glTexCoord2d(1, 0)
    glVertex(0.0, -0.5*hy, +0.5*wy)
    glTexCoord2d(1, 1)
    glVertex(0.0, +0.5*hy, +0.5*wy)
    glTexCoord2d(0, 1)
    glVertex(0.0, +0.5*hy, -0.5*wy)
    glEnd()

    # z = 0 slice of 3D jet sim
    glBindTexture(GL_TEXTURE_2D, module_vars['texture_Z'])

    glBegin(GL_QUADS)
    glTexCoord2d(0, 0)
    glVertex(-0.5*hz, 0.0, -0.5*wz)
    glTexCoord2d(1, 0)
    glVertex(-0.5*hz, 0.0, +0.5*wz)
    glTexCoord2d(1, 1)
    glVertex(+0.5*hz, 0.0, +0.5*wz)
    glTexCoord2d(0, 1)
    glVertex(+0.5*hz, 0.0, -0.5*wz)
    glEnd()

    glBindTexture(GL_TEXTURE_2D, 0)
    glDisable(GL_TEXTURE_2D)

    glutSwapBuffers()


def keyPressed(*args): # Called when a key is pressed. If esc is pressed, kill everything.
    print "received keys:", args
    if args[0] == ESCAPE:
        glutDestroyWindow(module_vars['window_id'])
        glDeleteTextures(module_vars['texture_X'])
        glDeleteTextures(module_vars['texture_Y'])
        glDeleteTextures(module_vars['texture_Z'])
        exit()

    if args[0] == 'w':
        module_vars['y'] -= 0.1
    if args[0] == 's':
        module_vars['y'] += 0.1

    if args[0] == 'd':
        module_vars['x'] -= 0.1
    if args[0] == 'a':
        module_vars['x'] += 0.1

    # using alternate keys okl; for rotations till arrow keys can be used
    if args[0] == 'o':
        module_vars['xrot'] += 5.0
    if args[0] == 'l':
        module_vars['xrot'] -= 5.0

    if args[0] == 'k':
        module_vars['yrot'] += 5.0
    if args[0] == ';':
        module_vars['yrot'] -= 5.0

    # z and x zoom in and out
    if args[0] == 'z':
        module_vars['zoom'] += 0.5
    if args[0] == 'x':
        module_vars['zoom'] -= 0.5

    # iterates through color bars
    if args[0] == 'c':
        module_vars['bar_setting'] = (module_vars['bar_setting'] + 1) % module_vars['bar_quant']
        load_textures()

    # toggles log scale
    if args[0] == 'b':
        module_vars['log_scale'] = not module_vars['log_scale']
        load_textures()

def load_glut():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_ALPHA | GLUT_DEPTH)
    glutInitWindowSize(640, 480)
    glutInitWindowPosition(0, 0)
    module_vars['window_id'] = glutCreateWindow("practiceGL")
    glutDisplayFunc(DrawGLScene)
    glutIdleFunc(DrawGLScene)
    glutReshapeFunc(ReSizeGLScene)
    glutKeyboardFunc(keyPressed)
    glClearColor(0.0, 0.0, 0.0, 0.0) 
    glClearDepth(1.0)
    glDepthFunc(GL_LESS)
    glEnable(GL_DEPTH_TEST)
    glShadeModel(GL_SMOOTH)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)

def load_textures_test():
    Nx = 100
    Ny = 100
    texture_data = np.zeros([Nx, Ny, 3], dtype=np.float32)
    texture_data[:,:,0] = 1.0
    texture_data[:,:,1] = 0.0
    texture_data[:,:,2] = 0.0

    module_vars['texture_X'] = glGenTextures(1)

    glBindTexture(GL_TEXTURE_2D, module_vars['texture_X'])
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, Nx, Ny, 0, GL_RGB, GL_FLOAT, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)

def base_vals(vals, dmax, dmin):
    if module_vars['log_scale']:
        vals = np.log10(vals) # ranges from e.g. [-10,0]
        dmax = np.log10(dmax)
        dmin = np.log10(dmin)
    vals -= dmin
    vals /= (dmax - dmin) # scaled in [0,1]
    return vals

def load_textures():
    import h5py
    h5f = h5py.File(filename, 'r')
    nx, ny, nz = h5f['prim']['pre'].shape

    # loading x slice
    Bx = h5f['prim']['Bx'][:,ny/2,:]
    By = h5f['prim']['By'][:,ny/2,:]
    Bz = h5f['prim']['Bz'][:,ny/2,:]
    PbX = 0.5*(Bx**2 + By**2 + Bz**2) # magnetic pressure
    
    #initialize max and min for all slices
    dmax, dmin = PbX.max(), PbX.min()

    # loading y-slice
    Bx = h5f['prim']['Bx'][nx/2, :, :]
    By = h5f['prim']['By'][nx/2, :, :]
    Bz = h5f['prim']['Bz'][nx/2, :, :]
    PbY = 0.5*(Bx**2 + By**2 + Bz**2) # magnetic pressure
    if PbY.max() > dmax:
        dmax = PbY.max()
    if PbY.max() < dmin:
        dmax = PbY.min()

    # loading z = 0 slice
    Bx = h5f['prim']['Bx'][:, :, nz/2]
    By = h5f['prim']['By'][:, :, nz/2]
    Bz = h5f['prim']['Bz'][:, :, nz/2]
    PbZ = 0.5*(Bx**2 + By**2 + Bz**2) # magnetic pressure
    if PbZ.max() > dmax:
        dmax = PbZ.max()
    if PbZ.max() < dmin:
        dmax = PbZ.min()

    # building x-slice
    vals = base_vals(PbX, dmax, dmin)
    Nx, Ny = vals.shape
    bbb, ggg, rrr = build_textures(vals)

    texture_data = np.zeros([Nx, Ny, 3], dtype=np.float32)
    texture_data[:,:,0] = bbb
    texture_data[:,:,1] = ggg
    texture_data[:,:,2] = rrr

    module_vars['texture_X'] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, module_vars['texture_X'])
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, Ny, Nx, 0, GL_RGB, GL_FLOAT, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)

    module_vars['x_height'] = float(Ny) / Nx
    module_vars['x_width'] = 1.0
    
    # building y-slice
    vals = base_vals(PbY, dmax, dmin)
    Nx, Ny = vals.shape
    bbb, ggg, rrr = build_textures(vals)

    texture_data = np.zeros([Nx, Ny, 3], dtype=np.float32)
    texture_data[:,:,0] = bbb
    texture_data[:,:,1] = ggg
    texture_data[:,:,2] = rrr

    module_vars['texture_Y'] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, module_vars['texture_Y'])
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, Ny, Nx, 0, GL_RGB, GL_FLOAT, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)

    module_vars['y_height'] = float(Ny) / Nx
    module_vars['y_width'] = 1.0
    
    #building z-slice
    vals = base_vals(PbZ, dmax, dmin)
    Nx, Ny = vals.shape
    bbb, ggg, rrr = build_textures(vals)

    texture_data = np.zeros([Nx, Ny, 3], dtype=np.float32)
    texture_data[:,:,0] = bbb
    texture_data[:,:,1] = ggg
    texture_data[:,:,2] = rrr

    module_vars['texture_Z'] = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, module_vars['texture_Z'])
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
    glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
    glTexEnvf(GL_TEXTURE_ENV, GL_TEXTURE_ENV_MODE, GL_DECAL)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, Ny, Nx, 0, GL_RGB, GL_FLOAT, texture_data)
    glBindTexture(GL_TEXTURE_2D, 0)

    module_vars['z_height'] = float(Ny) / Nx
    module_vars['z_width'] = 1.0

def build_textures(val):    
    Nx, Ny = val.shape
    bbb = np.zeros([Nx, Ny], dtype=np.float32)
    ggg = np.zeros([Nx, Ny], dtype=np.float32)
    rrr = np.zeros([Nx, Ny], dtype=np.float32)

    if module_vars['bar_setting'] == 0:        
        bbb = val
        ggg = val
        rrr = val

    elif module_vars['bar_setting'] == 1:
        rrr = 2.*val
        ggg = 1.2*val
        bbb = .8*val
        
    elif module_vars['bar_setting'] == 2:
        for i in range (Nx):
            for j in range (Ny):
                if val[i][j] < .1:
                    bbb[i][j] = 4.*(val[i][j]-.125)
                    ggg[i][j] = 0.0
                    rrr[i][j] = 0.0
                elif val[i][j] < .375:
                    bbb[i][j] = 1.0
                    ggg[i][j] = 4.*(val[i][j]-.125)
                    rrr[i][j] = 0.0
                elif val[i][j] < .625:
                    bbb[i][j] = 4.*(.625-val[i][j])
                    rrr[i][j] = 4.*(val[i][j]-.375)
                    ggg[i][j] = bbb[i][j]
                    if rrr[i][j] > bbb[i][j]:
                        ggg[i][j] = rrr[i][j]
                elif val[i][j] < .875:
                    bbb[i][j] = 0.0
                    ggg[i][j] = 4.*(.875-val[i][j])
                    rrr[i][j] = 1.
                else:
                    bbb[i][j] = 0.0
                    ggg[i][j] = 0.0
                    rrr[i][j] = 4.*(1.125-val[i][j])
                    
    elif module_vars['bar_setting'] == 3:
        hi = .8
        lo = .1
        gam = 0.8
        for i in range (Nx):
            for j in range (Ny):
                if val[i][j] > hi:
                    Amp = .3 + .7*(1.-val[i][j])/(1.-hi)
                elif val[i][j] < lo:
                    Amp = .3 + .7*(val[i][j])/(lo)
                else:
                    Amp = 1.0;
                    
                x1 = .5;
                x2 = .325;
                x3 = .15;
                x4 = 0.;
                
                if val[i][j] > x1:
                    r0 = 1.
                elif val[i][j] > x2:
                    r0 = (val[i][j]-x2)/(x1-x2)
                elif val[i][j] > x3:
                    r0 = 0.
                elif val[i][j] > x4:
                    r0 = (val[i][j]-x3)/(x4-x3)
                else:
                    r0 = 1.
                    
                x1 = .6625;
                x2 = .5;
                x3 = .275;
                x4 = .15;
                
                if val[i][j] > x1:
                    g0 = 0.
                elif val[i][j] > x2:
                    g0 = (val[i][j]-x1)/(x2-x1)
                elif val[i][j] > x3:
                    g0 = 1.
                elif val[i][j] > x4:
                    g0 = (val[i][j]-x4)/(x3-x4)
                else:
                    g0 = 0.
                    
                x1 = .325;
                x2 = .275;

                if val[i][j] > x1:
                    b0 = 0.
                elif val[i][j] > x2:
                    b0 = (val[i][j]-x1)/(x2-x1)
                else:
                    b0 = 1.

                rrr[i][j] = pow(Amp*r0,gam);
                ggg[i][j] = pow(Amp*g0,gam);
                bbb[i][j] = pow(Amp*b0,gam);

    elif module_vars['bar_setting'] == 4:
        nexp = 8.0
        rrr = np.exp(-nexp*pow(val-5./6.,2.0)) + .25*np.exp(-nexp*pow(val+1./6.,2.0))
        ggg = np.exp(-nexp*pow(val-3./6.,2.0))
        bbb = np.exp(-nexp*pow(val-1./6.,2.0)) + .25*np.exp(-nexp*pow(val-7./6.,2.0))

    elif module_vars['bar_setting'] == 5:
        for i in range(Nx):
            for j in range(Ny):
                if val[i][j] < .1:
                    bbb = 4.*(val[i][j]+.15)
                    ggg = 0.0
                    rrr = 0.0
                elif val[i][j] < .35:
                    bbb = 1.0
                    ggg = 4.*(val[i][j]-.1)
                    rrr = 0.0;
                elif val[i][j] < .6:
                    bbb = 4.*(.6-val[i][j])
                    ggg = 1.
                    rrr = 4.*(val[i][j]-.35)
                elif val[i][j] < .85:
                    bbb = 0.0
                    ggg = 4.*(.85-val[i][j])
                    rrr = 1.
                else:
                    bbb = 0.0;
                    ggg = 0.0;
                    rrr = 4.*(1.1-val[i][j]);
    else:
        bbb, ggg, rrr = 1.0, 1.0, 1.0
        print "somthings gone horribly wrong!"

    return bbb, ggg, rrr
    
if __name__ == '__main__':
    print "Use wasd to navigate and okl; to rotate"
    print "Hit ESC key to quit."
    load_glut()
    load_textures()
    glutMainLoop()
