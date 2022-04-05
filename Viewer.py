import cv2
import zmq
import base64
import numpy as np

context = zmq.Context()
footage_socket = context.socket(zmq.SUB)
footage_socket2 = context.socket(zmq.PUB)
footage_socket2.connect('tcp://172.20.10.7:5555')
footage_socket.bind('tcp://*:5555')
footage_socket.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))
camera = cv2.VideoCapture(0)

while True:
    try:
        grabbed, myframe = camera.read()  # grab the current frame
        myframe = cv2.resize(myframe, (640, 480))  # resize the frame
        encoded, buffer = cv2.imencode('.jpg', myframe)
        jpg_as_text = base64.b64encode(buffer)
        footage_socket2.send(jpg_as_text)

        frame = footage_socket.recv_string()
        img = base64.b64decode(frame)
        npimg = np.fromstring(img, dtype=np.uint8)
        source = cv2.imdecode(npimg, 1)

        horizontal_image = cv2.hconcat([myframe, source])

        cv2.imshow("Stream", horizontal_image)
        cv2.waitKey(1)

    except KeyboardInterrupt:
        cv2.destroyAllWindows()
        break