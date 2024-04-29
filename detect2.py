import subprocess
import cv2
import numpy as np
import keyboard
from flask import Flask, Response

app = Flask(__name__)

def check_brightness(image):
 avg_intensity = np.mean(image)
 if avg_intensity < 100:  # Adjust threshold as needed
  return 1
 elif avg_intensity > 200:  # Adjust threshold as needed
  return 2
 else:
  return 3

def check_contrast(image):
 std_dev = np.std(image)
 if std_dev < 20:  # Adjust threshold as needed
  return 1
 else:
  return 2

def check_saturation(image):
 hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
 avg_saturation = np.mean(hsv_image[:,:,1])
 if avg_saturation < 50:  # Adjust threshold as needed
  return 1
 else:
  return 2

def adjust_camera_settings(brightness, contrast, saturation):
 if brightness == 1:
  subprocess.run(['v4l2-ctl','-d','/dev/video1/', '-c', 'brightness=+10'])
 elif brightness == 2:
  subprocess.run(['v4l2-ctl','-d','/dev/video1', '-c', 'brightness=-10'])

 if contrast == 1:
  subprocess.run(['v4l2-ctl','-d','/dev/video1/', '-c', 'contrast=+5'])
 elif contrast == 2:
  pass  # Do nothing
    
 if saturation == 1:
  subprocess.run(['v4l2-ctl','-d','/dev/video1/', '-c', 'saturation=+5'])
 elif saturation == 2:
  pass


# Capture an image from camera
#cap = cv2.VideoCapture(1)
#cap.set(cv2.CAP_PROP_FPS, 15)
#cap.set(cv2.CAP_PROP_FRAME_WIDTH,800)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT,600)
#cap.set(cv2.CAP_PROP_CONVERT_RGB,1)
#cap.set(cv2.CAP_PROP_FOURCC,cv2.VideoWriter_fourcc('m','p','4','v'))
cmd = ['ffmpeg', '-f', 'v4l2', '-video_size', '640x480', '-input_format', 'mjpeg', '-i', '/dev/video0', '-vf', 'format=bgr24', '-f', 'rawvideo', '-']
process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def gen_frames():
    while True:
        #ret, frame = cap.read()  # Read the camera frame
        #if not ret:
        #    break
        #else:
            raw_frame = process.stdout.read(640 * 480 * 3)
            if len(raw_frame) == 0:
             break
    
            # Convert raw frame to numpy array
            frame = np.frombuffer(raw_frame, dtype=np.uint8).reshape((480, 640, 3))
            # Determine image settings
            brightness_level = check_brightness(frame)
            contrast_level = check_contrast(frame)
            saturation_level = check_saturation(frame)

            # Adjust camera settings based on image settings
            adjust_camera_settings(brightness_level, contrast_level, saturation_level)

            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)

#cap.release()
