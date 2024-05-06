import cv2
import os
from Person_and_Hand import Preprocessor
from cvlib import object_detection

image = cv2.imread(r"C:\Users\rahul\Desktop\Hand\547.jpg")
object_detection.detect_common_objects(image)


# directory= 'SignImage/'
# print(os.getcwd())

# if not os.path.exists(directory):
#     os.mkdir(directory)
# if not os.path.exists(f'{directory}/blank'):
#     os.mkdir(f'{directory}/blank')
    

# for i in range(2):
#     if i==0:
#         sign="okay"
#     else:
#         sign="stop"
#     if not os.path.exists(f'{directory}/{sign}'):
#         os.mkdir(f'{directory}/{sign}')




# import os
# import cv2
# cap=cv2.VideoCapture(0)
# while True:
#     _,frame=cap.read()
#     count = {
#              'okay': len(os.listdir(directory+"/okay")),
#              'stop': len(os.listdir(directory+"/stop")),
#              'blank': len(os.listdir(directory+"/blank"))
#              }

#     row = frame.shape[1]
#     col = frame.shape[0]
#     cv2.rectangle(frame,(0,40),(400,400),(255,255,255),2)
#     cv2.imshow("data",frame)
#     frame=frame[40:400,0:400]
#     cv2.imshow("ROI",frame)
#     frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
#     frame = cv2.resize(frame,(512,343))
#     interrupt = cv2.waitKey(10)
#     if interrupt & 0xFF == ord('0'):
#         processor = Preprocessor()
#         cropped_image = processor.process(frame)
#         cv2.imwrite(os.path.join(directory+'okay/'+str(count['okay']))+'.jpg',cropped_image)
#     if interrupt & 0xFF == ord('1'):
#         processor = Preprocessor()
#         cropped_image = processor.process(frame)
#         cv2.imwrite(os.path.join(directory+'stop/'+str(count['stop']))+'.jpg',cropped_image)
#     if interrupt & 0xFF == ord('.'):
#         processor = Preprocessor()
#         cropped_image = processor.process(frame)
#         cv2.imwrite(os.path.join(directory+'blank/' + str(count['blank']))+ '.jpg',cropped_image)