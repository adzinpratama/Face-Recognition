import os
import numpy as np
from PIL import Image
import cv2
import pickle

class Train():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    image_dir = os.path.join(BASE_DIR, "dataset")

    face_cascade = cv2.CascadeClassifier('models/haarcascade_frontalface_default.xml')
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    current_id = 0
    label_ids = {}
    y_label = []
    x_train = []

    def __init__(self):
        for root, dirs, files in os.walk(self.image_dir):
            for file in files:
                if file.endswith("png") or file.endswith("jpg"):
                    self.path = os.path.join(root, file)
                    self.label = os.path.basename(root).replace("", "").upper()
                    print(self.label, self.path)

                    if self.label in self.label_ids:
                        pass
                    else:
                        self.label_ids[self.label] = self.current_id
                        self.current_id += 1
                    self.id_ = self.label_ids[self.label]
                    print(self.label_ids)

                    self.pil_image = Image.open(self.path).convert("L")
                    self.image_array = np.array(self.pil_image, "uint8")
                    print(self.image_array)
                    self.faces = self.face_cascade.detectMultiScale(self.image_array, scaleFactor=1.5, minNeighbors=5)

                    for (x, y, w, h) in self.faces:
                        self.roi = self.image_array[y:y+h, x:x+w]
                        self.x_train.append(self.roi)
                        self.y_label.append(self.id_)
        print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
        with open("labels.pickle", "wb") as f:
            pickle.dump(self.label_ids, f)

        self.recognizer.train(self.x_train, np.array(self.y_label))
        self.recognizer.save("trainer/train.yml")
        print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(self.label_ids))))


if __name__ == "__main__":
    Train()