import cv2
from PyQt5.QtWidgets import (QWidget, QPushButton, QApplication, QLabel)
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import sys


class Interface(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # --------------------------------------#
        # -----Creates a play/pause button------#
        # --------------------------------------#
        button_width = 80
        button1 = QPushButton(self)
        button1.setIcon(QtGui.QIcon('pause.png'))
        button1.setStyleSheet("background-color: red")
        button1.setCheckable(True)
        button1.move(720,0)
        button1.setFixedWidth(button_width)
        button1.clicked.connect(self.setState)


        #---------------------------------- ----#
        #-----Danger Level ---------------------#
        #---------------------------------------#


        #--------------------------------------#
        #-List of filtered objects for testing-#
        #--------------------------------------#
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 720, 480)
        objects = []
        values = ['car', 100, 100, 10, 10, 0]  # X,Y,Width, Height, Probability
        for i in range(4):
            objects.append(values)
            values = ['car', values[1] + 30, values[2] + 30, values[3] + 30, values[4] + 30, values[5] + 10]

        self.label.setPixmap(QPixmap.fromImage(self.getImage('car.png', objects)))
        #---------------------------------------#
        #---- Creates and Displays an image ----#
        #---------------------------------------#


        self.setGeometry(300, 300, 800, 480)
        self.setWindowTitle('Interface')
        self.show()

    def setState(self, pressed):
        source = self.sender()
        if pressed:
            print('PAUSED')
            source.setIcon(QtGui.QIcon('play.png'))
            source.setStyleSheet("background-color: green")
            self.label.setPixmap(QtGui.QPixmap('car.png').scaled(720, 480))

        else:
            print('PLAYING')
            source.setIcon(QtGui.QIcon('pause.png'))
            source.setStyleSheet("background-color: red")
            objects = []
            values = ['car', 100, 100, 10, 10, 0]  # X,Y,Width, Height, Probability
            for i in range(4):
                objects.append(values)
                values = ['car', values[1] + 30, values[2] + 30, values[3] + 30, values[4] + 30, values[5] + 10]

            self.label.setPixmap(QPixmap.fromImage(self.getImage('car.png', objects)))

    def paintEvent(self, e):
        #Needs update function
        paint = QPainter(self)
        gradient = QLinearGradient(730, 50, 790, 400)
        gradient.setColorAt(0.0, QColor(255, 0, 0))
        gradient.setColorAt(0.5, QColor(255, 255, 0))
        gradient.setColorAt(1.0, QColor(0, 255, 0))
        paint.fillRect(QRect(730, 50, 60, 350), gradient)

    def getImage(self, image, filtered_objects):
        source_image_width = 720;
        source_image_height = 480;
        cvImage = cv2.imread(image)
        cvImage = cv2.resize(cvImage,(720,480), cv2.INTER_LINEAR)
        height, width, byteValue = cvImage.shape
        byteValue = byteValue * width
        cv2.cvtColor(cvImage, cv2.COLOR_BGR2RGB, cvImage)
        x_ratio = float(cvImage.shape[1]) / source_image_width
        y_ratio = float(cvImage.shape[0]) / source_image_height
        for obj_index in range(len(filtered_objects)):
            center_x = int(filtered_objects[obj_index][1] * x_ratio)
            center_y = int(filtered_objects[obj_index][2] * y_ratio)
            half_width = int(filtered_objects[obj_index][3] * x_ratio) // 2
            half_height = int(filtered_objects[obj_index][4] * y_ratio) // 2
            # calculate box (left, top) and (right, bottom) coordinates
            box_left = max(center_x - half_width, 0)
            box_top = max(center_y - half_height, 0)
            box_right = min(center_x + half_width, source_image_width)
            box_bottom = min(center_y + half_height, source_image_height)
            cv2.rectangle(cvImage, (box_left, box_top-20), (box_right, box_bottom), (0, 255, 0), 1)
            cv2.putText(cvImage,filtered_objects[obj_index][0] + ' : %.2f' % filtered_objects[obj_index][5], (box_left+5, box_top-7), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 1)
        myQImage = QImage(cvImage, width, height, byteValue, QImage.Format_RGB888)
        return myQImage

if __name__ == '__main__':
    app = QApplication(sys.argv)
    Gui = Interface()
    sys.exit(app.exec_())