import base64
import cv2
import zmq
import numpy as np
from Helper import *

import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QFormLayout, QLabel, QSplashScreen
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtCore import Qt

path = "D:/Projects/idsproject/images/"


def start(ip, port):
    connect_ip = "tcp://" + ip + ":" + port

    context = zmq.Context()

    socket1 = context.socket(zmq.SUB)
    socket1.bind('tcp://*:5555')
    socket1.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    socket2 = context.socket(zmq.PUB)
    socket2.connect(connect_ip)

    camera = cv2.VideoCapture(0)

    count = 0
    speed = 5

    while True:
        try:
            grabbed, myframe = camera.read()  # grab the current frame
            myframe = cv2.resize(myframe, (640, 480))  # resize the frame

            encoded, buffer = cv2.imencode('.jpg', myframe)  # encode the image into streaming data
            jpg_as_text = base64.b64encode(buffer)  # encode the image as base64 string
            socket2.send(jpg_as_text)  # send the encoded base64 string over tcp

            frame = socket1.recv_string()  # receive the encoded base64 string over tcp
            img = base64.b64decode(frame)  # decode the base64 string
            npimg = np.fromstring(img, dtype=np.uint8)  # convert string to numpy array
            source = cv2.imdecode(npimg, 1)  # convert numpy array to image format

            count += 1
            if count % speed == 0:  # Every {speed} frame:
                cv2.imwrite(path + str(count / speed) + '.jpg', source)  # Save the current image to the disk

            horizontal_image = cv2.hconcat([myframe, source])  # combine two frames horizontally
            cv2.imshow("Stream", horizontal_image)  # show the combined image with opencv

            key = cv2.waitKey(1)

            if key == 27:  # On user input ESC keypress, raise exception
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            cv2.destroyAllWindows()

            emotions = emotions_in_order(path)

            global total
            total = 0

            for emotion in emotions:
                total += emotions[emotion]

            dominant = max(emotions, key=emotions.get)

            print("dominant emotion: " + dominant)

            wind.updateLabels(emotions)
            wind.show()
            break

class widget(QWidget):
    def __init__(self, parent=None):
        self.ip = "192.168.188.197"
        self.port = "5555"

        super().__init__(parent)

        button1 = QPushButton()
        button1.setText("Connect")
        button1.clicked.connect(self.onconnect)

        iptext = QLineEdit()
        iptext.setMaxLength(15)
        iptext.setFont(QFont("Arial", 20))
        iptext.textChanged.connect(self.ipchanged)

        porttext = QLineEdit()
        porttext.setMaxLength(5)
        porttext.setFont(QFont("Arial", 20))
        porttext.textChanged.connect(self.portchanged)

        form = QFormLayout()
        form.addRow("IP", iptext)
        form.addRow("Port", porttext)
        form.addRow("Connect", button1)

        self.setLayout(form)
        self.setWindowTitle("IDS")

    def ipchanged(self, text):
        self.ip = text

    def portchanged(self, text):
        self.port = text

    def onconnect(self):
        self.hide()
        start(self.ip, self.port)


class emotionWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.neutrall = QLabel()
        self.surprisel = QLabel()
        self.sadl = QLabel()
        self.happyl = QLabel()
        self.fearl = QLabel()
        self.disgustl = QLabel()
        self.angryl = QLabel()

        form = QFormLayout()
        form.addRow("Neutral: ", self.neutrall)
        form.addRow("Surprise: ", self.surprisel)
        form.addRow("Sad: ", self.sadl)
        form.addRow("Happy: ", self.happyl)
        form.addRow("Fear: ", self.fearl)
        form.addRow("Disgust: ", self.disgustl)
        form.addRow("Angry: ", self.angryl)

        self.setLayout(form)
        self.setWindowTitle("Emotions")

    def updateLabels(self, emotions):
        self.neutrall.setText(str(round(emotions["neutral"]/total * 100)) + "%")
        self.surprisel.setText(str(round(emotions["surprise"] / total * 100)) + "%")
        self.sadl.setText(str(round(emotions["sad"] / total * 100)) + "%")
        self.happyl.setText(str(round(emotions["happy"] / total * 100)) + "%")
        self.fearl.setText(str(round(emotions["fear"] / total * 100)) + "%")
        self.disgustl.setText(str(round(emotions["disgust"] / total * 100)) + "%")
        self.angryl.setText(str(round(emotions["angry"] / total * 100)) + "%")


#  Create connection UI
app = QApplication(sys.argv)
win = widget()
win.show()
wind = emotionWidget()
sys.exit(app.exec_())
