import cv2
from PIL import Image
import time
import os
os.chdir('C:\\Users\\**')
#conda activate --stack collab-project
from keras.models import model_from_json
from pathlib import Path
import numpy as np

from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.image import resize


from telegrambot import *



# Open a camera for video capturing.
video = cv2.VideoCapture(0)

# import face detection classifier
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 
                                     "haarcascade_frontalface_alt.xml")

#phone ip location
address = 'https://192.168.43.246:8080/video'

#initial camera with ip address
video.open(address)




# load a trained model 
f = Path('./Deep_0852.json')
model_structure = f.read_text()
model = model_from_json(model_structure)
# #input 48*48*1
model.load_weights('Deep_0852.h5')
emotion_map = {0: 'Neutral', 1: 'Happy', 2: 'Pain'}
negative_emotion = {'Pain'}

# image dimension for prediction
prediction_input_size =48


# mark down start time
start = time.time()
l = 0
emotion_list = []
emotion_image = []
gap_time = time.time()



while True:
    #read the image from camera
    video.open(address)
    check, frame = video.read()
    
    # convert the frame into grey for face detection
    frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    #  improves the contrast of the image
    frame_gray = cv2.equalizeHist(frame_gray)
        
    #-- Detect faces
    faces = face_cascade.detectMultiScale(frame_gray, minSize=(80,80))
    
    for (x,y,w,h) in faces:
        
        # prepare face for input
        frame_face = frame[y:y+h,x:x+w]
        RGB_face = Image.fromarray(cv2.cvtColor(frame_face, cv2.COLOR_BGR2RGB))
        grey_face = RGB_face.convert('L')
        grey_face = grey_face.resize((prediction_input_size,
                                      prediction_input_size))
        face_array = img_to_array(grey_face)
        face_array = face_array.reshape(1,prediction_input_size,prediction_input_size,1)

        #predict with pretrained model
        expression_predict = model.predict(face_array)[0]
        
        #emotion in string
        emotion = emotion_map[expression_predict.argmax()]
        
        
        print(emotion)
        if emotion in negative_emotion:
            emotion = 'negative'
        else:
            emotion = 'normal'
        emotion_list.append(emotion)
        emotion_image.append(frame)
        
        
        # save emotion record
        if len(emotion_list) > 40:
            emotion_list.pop(0)
            emotion_image.pop(0)
            
        # send the telegram message to chatbot if requirement fulfill
        if emotion_list.count('negative') > 5 and time.time() - gap_time > 5:
            telegram_send_text('Target need help! ')
            emg_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            emg_image.save('emg.jpg')
            telegram_send_image('emg.jpg')
            gap_time = time.time()
            emotion_list = []
            emotion_image = []
            
        
        
        #draw rectangle and text on the frame
        frame = cv2.cv2.rectangle(frame, (x,y), (x+w,y+h), (0, 255, 0), 4)
        frame = cv2.putText(frame,
                            emotion,
                            (x,y),
                            cv2.FONT_HERSHEY_SIMPLEX, 
                            fontScale=1,
                            color = (0, 255, 0),
                            thickness = 2)
        
    #show image in window
    cv2.imshow('frame2',frame)
    
    #detect if user need to exit the video window
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break
    l += 1
    
    
end = time.time()
print(end - start, 'sec, there are ', l, 'frame capturedd')
video.release()
cv2.destroyAllWindows()
