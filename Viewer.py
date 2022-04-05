import cv2
import zmq
import base64
import numpy as np
import tkinter

root = tkinter.Tk()
root.geometry("200x80")

text = tkinter.Text(root, height = 1, width = 22)

def start():
    ip = "tcp://" + text.get("1.0", "end-1c") + ":5555"

    context = zmq.Context()

    socket1 = context.socket(zmq.SUB)
    socket1.bind('tcp://*:5555')
    socket1.setsockopt_string(zmq.SUBSCRIBE, np.unicode(''))

    socket2 = context.socket(zmq.PUB)
    socket2.connect(ip)

    camera = cv2.VideoCapture(0)

    root.destroy()

    while True:
        try:
            grabbed, myframe = camera.read()  # grab the current frame
            myframe = cv2.resize(myframe, (640, 480))  # resize the frame
            encoded, buffer = cv2.imencode('.jpg', myframe)
            jpg_as_text = base64.b64encode(buffer)
            socket2.send(jpg_as_text)

            frame = socket1.recv_string()
            img = base64.b64decode(frame)
            npimg = np.fromstring(img, dtype=np.uint8)
            source = cv2.imdecode(npimg, 1)

            horizontal_image = cv2.hconcat([myframe, source])
            cv2.imshow("Stream", horizontal_image)

            key = cv2.waitKey(1)

            if key == 27:
                raise KeyboardInterrupt

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break


button = tkinter.Button(root, text ="Submit", command=start)
button.config(width=20, height=2)

text.pack()
button.pack()
root.mainloop()
