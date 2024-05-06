from keras.models import load_model
import cv2
import numpy as np
import os
import warnings
from server import VideoReceiver
from obj_det import objDet
from datacollector import Preprocessor

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

    receiver = VideoReceiver()
    receiver.accept_connection()

    processor = Preprocessor()
    protection_system = ProtectionSystem("code/server-pc/keras_Model.h5", "code/server-pc/labels.txt")

    while True:
        frame = receiver.receive_frame()
        if frame is None:
            continue
        if not receiver.display_frame(frame):
            break
        try:
            image = cv2.resize(frame,(640, 430))
            masked_image = processor.process(image)

            if masked_image is not None:
                cv2.imshow('Skelton', masked_image)

            class_name, confidence_score = protection_system.predict(masked_image)
            print("Class:", class_name[2:], end="")
            print("Confidence Score:", str(np.round(confidence_score * 100))[:-2], "%")
            keyboard_input = cv2.waitKey(1) & 0xFF
            if keyboard_input == 27:
                break

        except Exception as e:
            pass

    cv2.destroyAllWindows()
    receiver.close_connection()