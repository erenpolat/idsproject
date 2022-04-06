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


def emotions_in_order(path):
    images = load_images_from_folder(path)
    emotions = {"neutral": 0, "surprise": 0, "sad": 0, "happy": 0, "fear": 0, "disgust": 0, "angry": 0}
    for image in images:
        analyze = DeepFace.analyze(image, actions=('emotion',), enforce_detection=False)
        for emotion in analyze["emotion"]:
            emotions[emotion] += analyze["emotion"][emotion]

    return emotions
