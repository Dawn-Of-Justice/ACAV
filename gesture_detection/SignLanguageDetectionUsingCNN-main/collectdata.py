import cv2
import os


directory= 'SignImage48x48/'
print(os.getcwd())

if not os.path.exists(directory):
    os.mkdir(directory)
if not os.path.exists(f'{directory}/blank'):
    os.mkdir(f'{directory}/blank')
    

for i in range(2):
    if i==0:
        sign="okay"
    else:
        sign="stop"
    if not os.path.exists(f'{directory}/{sign}'):
        os.mkdir(f'{directory}/{sign}')




import os
import cv2
cap=cv2.VideoCapture(0)
while True:
    _,frame=cap.read()
    count = {
             'okay': len(os.listdir(directory+"/okay")),
             'stop': len(os.listdir(directory+"/stop")),
             'blank': len(os.listdir(directory+"/blank"))
             }

    row = frame.shape[1]
    col = frame.shape[0]
    cv2.rectangle(frame,(0,40),(300,300),(255,255,255),2)
    cv2.imshow("data",frame)
    frame=frame[40:300,0:300]
    cv2.imshow("ROI",frame)
    frame = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    frame = cv2.resize(frame,(48,48))
    interrupt = cv2.waitKey(10)
    if interrupt & 0xFF == ord('0'):
        cv2.imwrite(os.path.join(directory+'okay/'+str(count['okay']))+'.jpg',frame)
    if interrupt & 0xFF == ord('1'):
        cv2.imwrite(os.path.join(directory+'stop/'+str(count['stop']))+'.jpg',frame)
    if interrupt & 0xFF == ord('.'):
        cv2.imwrite(os.path.join(directory+'blank/' + str(count['blank']))+ '.jpg',frame)