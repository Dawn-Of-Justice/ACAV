from keras.models import load_model
import cv2
import numpy as np
import os
import warnings

np.set_printoptions(suppress=True)

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

np.set_printoptions(suppress=True)

class ProtectionSystem:
    def __init__(self, model_path, labels_path):
        self.model = load_model(model_path, compile=False)
        self.class_names = open(labels_path, "r").readlines()

    def predict(self, image):
        image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
        image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
        image = (image / 127.5) - 1
        prediction = self.model.predict(image)
        index = np.argmax(prediction)
        class_name = self.class_names[index]
        confidence_score = prediction[0][index]
        return class_name, confidence_score

if __name__ == "__main__":
    protection_system = ProtectionSystem("keras_Model.h5", "labels.txt")
    camera = cv2.VideoCapture(0)
    while True:
        ret, image = camera.read()
        cv2.imshow("Gesture Detection", image)
        class_name, confidence_score = protection_system.predict(image)
        print("Class:", class_name[2:], end="")
        print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
        keyboard_input = cv2.waitKey(1) & 0xFF
        if keyboard_input == 27:
            break
    camera.release()
    cv2.destroyAllWindows()