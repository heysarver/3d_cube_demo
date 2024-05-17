from PyQt5.QtWidgets import QOpenGLWidget
from PyQt5.QtCore import QTimer
from OpenGL.GL import (
    glBegin, glEnd, glColor3f, glVertex3f, GL_QUADS,
    glClearColor, glEnable, glClear, glColorMaterial,
    glTranslatef, glRotatef, glViewport, glMatrixMode,
    glLoadIdentity, GL_COLOR_BUFFER_BIT, GL_DEPTH_BUFFER_BIT,
    GL_DEPTH_TEST, GL_LIGHT0, GL_LIGHTING, GL_FRONT_AND_BACK,
    GL_AMBIENT_AND_DIFFUSE, GL_PROJECTION, GL_MODELVIEW, GL_COLOR_MATERIAL
)
from OpenGL.GLU import gluPerspective
from functions.draw_cube import drawCube
import random


class GLWidget(QOpenGLWidget):
    def __init__(self, parent=None):
        super(GLWidget, self).__init__(parent)
        self.rotation_increment = 0.5
        self.rotation_axes = [1.0, 1.0, 1.0]
        self.target_rotation_axes = [1.0, 1.0, 1.0]
        self.xRotDeg = 0.0
        self.yRotDeg = 0.0
        self.zRotDeg = 0.0
        self.interpolation_steps = 200
        self.current_step = 0

        # Timer for updating the rotation. Slower interval = fewer updates = less CPU use
        self.timer = QTimer(self)
        self.timer.setInterval(33)  # Increasing this to about 30 FPS (approximately 33ms per frame)
        self.timer.timeout.connect(self.updateRotation)
        self.timer.start()

        # Timer for changing the rotation axis less frequently
        self.change_axis_timer = QTimer(self)
        self.change_axis_timer.setInterval(10000)  # Increasing this to every 10 seconds
        self.change_axis_timer.timeout.connect(self.prepareNewRotationAxis)
        self.change_axis_timer.start()

    def initializeGL(self):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_LIGHT0)
        glEnable(GL_LIGHTING)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        glEnable(GL_COLOR_MATERIAL)

    def resizeGL(self, width, height):
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(45.0, float(width) / height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()
        glTranslatef(0.0, 0.0, -5.0)
        glRotatef(self.xRotDeg, self.rotation_axes[0], 0.0, 0.0)
        glRotatef(self.yRotDeg, 0.0, self.rotation_axes[1], 0.0)
        glRotatef(self.zRotDeg, 0.0, 0.0, self.rotation_axes[2])
        drawCube()

    def updateRotation(self):
        self.xRotDeg += self.rotation_increment
        self.yRotDeg += self.rotation_increment
        self.zRotDeg += self.rotation_increment
        self.update()  # Triggers paintGL()

        if self.current_step < self.interpolation_steps:
            for i in range(3):
                self.rotation_axes[i] = self.lerp(self.rotation_axes[i], self.target_rotation_axes[i], 1 / (self.interpolation_steps - self.current_step))
            self.current_step += 1

    def prepareNewRotationAxis(self):
        new_target = [random.choice([0.0, 1.0]) for _ in range(3)]
        if all(axis == 0.0 for axis in new_target):
            new_target[random.randint(0, 2)] = 1.0
        self.target_rotation_axes = new_target
        self.current_step = 0

    @staticmethod
    def lerp(start, end, t):
        return (1 - t) * start + t * end
