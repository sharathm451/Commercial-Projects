from flask import Flask, Response, jsonify, make_response
import numpy as np
import cv2
import flask 

app = Flask(__name__)

def gen_frames():
    # cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID20220504120402.mp4")
    # cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID-20211003-WA0055.mp4")
    cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID20220506090717.mp4")
    # cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID20220506090849.mp4")

    def variance_of_laplacian(image):
        return cv2.Laplacian(image, cv2.CV_64F).var()   

    ret, frame = cap.read()
    kernel = np.ones((5,5), np.uint8)
    def rescaleFrame(frame, scale=0.25):
        width = int(frame.shape[1] * scale)
        height = int(frame.shape[0] * scale)
        
        dimensions = (width, height)
        return cv2.resize(frame, dimensions, interpolation=cv2.INTER_AREA)

    i =0 
    while(True):
        ret = cap.grab()
        i = i + 1
        if i%3==0:
            ret, frame = cap.read()
            if(frame is None):
                print("End of frame")
                break;
            else:
                resize = cv2.resize(frame, (480,640), interpolation=cv2.INTER_LINEAR)
                gray = cv2.cvtColor(resize, cv2.COLOR_BGR2GRAY)
                fm = variance_of_laplacian(gray)
                _,thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY )
                fgmask = cv2.dilate(thresh, kernel, iterations = 3)              
                fgmask= cv2.erode(fgmask, kernel, iterations=3)  
                frame_resized = rescaleFrame(frame)

                # cv2.imshow('video Resized', frame_resized)
                # cv2.imshow('Tampering frame',frame)
                # cv2.imshow('original',frame)  
                blank = np.zeros(gray.shape, dtype=np.uint8)
                rectangle = cv2.rectangle(blank.copy(), (0,60), (480,580), 255, -1) 
                thresh = cv2.bitwise_and(fgmask,fgmask,mask=rectangle)
                cv2.imshow('thresh',thresh)
                if cv2.countNonZero(thresh) == 0:
                    cv2.putText(frame,"TAMPERING DETECTED",(5,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)  
                    frame_resized = rescaleFrame(frame)
                    resp = {'Tampering Detection: Yes'}
                    yield  str(resp)                 
                elif fm < 15:
                    text = "Tampering Detection: Yes (blur)"
                    cv2.putText(frame,"{}: {:.2f}".format(text, fm), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,255), 2)
                    cv2.imshow('Tampering frame',frame)   
                    frame_resized = rescaleFrame(frame)
                    resp = {"{}: {:.2f}".format(text, fm)}
                    yield  str(resp)                 
                else:
                    resp ={'Tampering Detection: No'}
                    yield  str(resp)


                # try:
                #     ret, buffer = cv2.imencode('.jpg', frame)
                #     frame = buffer.tobytes()
                #     yield  (b'--frame\r\n'
                #         b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
                # except Exception as e:
                #     pass

@app.route('/')
def Tampering():
    return  Response(gen_frames())
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)  
