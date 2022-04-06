import cv2
import numpy as np
from deepface import DeepFace
import os

def load_images_from_folder(folder):
    images = []
    for filename in os.listdir(folder):
        img = cv2.imread(os.path.join(folder, filename))
        if img is not None:
            images.append(img)
    return images

def find_index_from_emotions(emotions):
    arr = np.array(emotions)
    largest = arr[0][0]
    index = 0
    largest_index = 0
    for i in arr[0]:
        index = index + 1
        if i > largest:
            largest = i
            largest_index = index

    return largest_index - 1

def emotions_in_order(path):
    images = load_images_from_folder(path)
    emotions = {"neutral": 0, "surprise": 0, "sad": 0, "happy": 0, "fear": 0, "disgust": 0, "angry": 0}
    for image in images:
        analyze = DeepFace.analyze(image, actions=('emotion',), enforce_detection=False)
        emotions[analyze["dominant_emotion"]] += 1

    return emotions

def find_emotion(index):
    switcher = {
        "neutral" : 0,
        1: "surprise",
        2: "sadness",
        3: "happiness",
        4: "fear",
        5: "disgust",
        6: "anger",
    }
