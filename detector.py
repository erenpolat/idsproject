import cv2
frame = cv2.imread('sad.jpg')
from feat import Detector
#vid = cv2.VideoCapture(0)
detector = Detector()
#while True:
#    ret, frame = vid.read()
detected_faces = detector.detect_faces(frame)
detected_landmarks = detector.detect_landmarks(frame, detected_faces)
print(detector.detect_emotions(frame, detected_faces, detected_landmarks))
    # cv2.imshow('frame', frame)
    # if cv2.waitKey(1) & 0xFF == ord('q'):
    #     break
# After the loop release the cap object
#vid.release()
# Destroy all the windows
#cv2.destroyAllWindows()

