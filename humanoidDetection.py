# import the necessary packages
from imutils.object_detection import non_max_suppression
import numpy as np
import cv2
from flask import Flask, Response, jsonify, make_response


app = Flask(__name__)

def gen_frames():
    cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\Pedestrian.mp4")
    ret,frame = cap.read()
    # initialize the HOG descriptor/person detector
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    i = 0
    while(True):
        ret = cap.grab()
        i = i + 1
        if i%4==0: 
            ret, frame = cap.read()
            if(frame is None):
                print("End of frame")
                break;
            else:            
                frame = cv2.resize(frame, (640, 480))
                orig = frame.copy()
                (rects, weights) = hog.detectMultiScale(frame, winStride=(4, 4),
                    padding=(8, 8), scale=1.05)
                if rects.any()> 1:       
                    rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
                    pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)        
                    for (xA, yA, xB, yB) in pick:
                        cv2.rectangle(frame, (xA, yA), (xB, yB), (0, 255, 0), 2)
                        print('yes')
                        resp = {'Human Detection: Yes'}
                        yield  str(resp)                 

                
                # try:
                #     ret, buffer = cv2.imencode('.jpg', frame)
                #     frame = buffer.tobytes()
                #     # yield str(resp).decode('utf-8') 
                #     yield  (b'--frame\r\n'
                #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                # except Exception as e:
                #     pass
                
@app.route('/')
def Tampering():
    return Response(gen_frames())
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)  

