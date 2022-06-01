from flask import Flask, Response, jsonify, make_response
import numpy as np
import cv2
import flask 

app = Flask(__name__)

def gen_frames():
    static_back=None
    cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID20220504120402.mp4")
    # cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID-20211003-WA0055.mp4")
    # cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID20220506090717.mp4")
    # cap = cv2.VideoCapture(r"C:\Users\Asus\Downloads\videos\VID20220506090849.mp4")


    ret,frame = cap.read()
    kernel = np.ones((5,5), np.uint8)
    avg1 = np.float32(frame)


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
                cv2.accumulateWeighted(frame,avg1,0.1)
                res1 = cv2.convertScaleAbs(avg1)
                _,res1 = cv2.threshold(res1, 155, 255, cv2.THRESH_BINARY)
                res1 = cv2.dilate(res1, (5,5), iterations=3)
                res1 = cv2.erode(res1, (5,5), iterations =3)  
                if static_back is None:
                    static_back = res1
                    height,width,channel = static_back.shape
                    continue
                errorL2 = cv2.norm( static_back, res1, cv2.NORM_L2 )
                similarity = 1 - errorL2 / ( height * width )
                blank = np.zeros(frame.shape,dtype='uint8')
                
                frame_resized = rescaleFrame(frame)

                if(similarity<=0.84):
                    cv2.putText(frame,"TAMPERING DETECTED",(5,30),cv2.FONT_HERSHEY_SIMPLEX,1,(0,255,255),2)  
                    frame_resized = rescaleFrame(frame)
                    resp = {'Tampering Detection: Yes'}
                    yield  str(resp)                 
                else:
                    resp ={'Tampering Detection: No'}
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
    return  Response(gen_frames())
    # return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(debug=True)  