'''
	orig author: Igor Maculan - n3wtron@gmail.com
	A Simple mjpg stream http server
'''
import cv2
from http.server import BaseHTTPRequestHandler,HTTPServer
import time

capture=None
imgN1=None
imgN2=None

def diffImg(t0, t1, t2):
    d1 = cv2.absdiff(t2, t1)
    d2 = cv2.absdiff(t1, t0)
    return cv2.bitwise_and(d1, d2)

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        print(self.path)
        if self.path.endswith('.mjpg'):
            self.send_response(200)
            self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
            self.end_headers()
            while True:
                try:
                    rc,img = capture.read()
                    if not rc:
                        continue
                    #global imgN1
                    #global imgN2
                    #if imgN1 is not None and imgN2 is not None:
                    #    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                        #result = diffImg(imgN2, imgN1, img)
                    #    result = img
                    #else:
                    #    result = img
                    #    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                    #imgN2 = imgN1
                    #imgN1 = img
                    #cv2.circle(img, (320,240),100,255,-1)
                    #imgRGB = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
                    r, buf = cv2.imencode(".jpg",img)
                    self.wfile.write(bytes("--jpgboundary\r\n",'utf-8'))
                    self.send_header('Content-type','image/jpeg')
                    self.send_header('Content-length',str(len(buf)))
                    self.end_headers()
                    self.wfile.write(bytearray(buf))
                    self.wfile.write(bytes('\r\n', 'utf-8'))
                    time.sleep(0.05)
                except KeyboardInterrupt:
                    break
            return
        if self.path.endswith('.html') or self.path=="/":
            self.send_response(200)
            self.send_header('Content-type','text/html')
            self.end_headers()
            self.wfile.write(bytes('<html><head></head><body>', 'utf-8'))
            self.wfile.write(bytes('<img src="./cam.mjpg" />', 'utf-8'))
            self.wfile.write(bytes('</body></html>', 'utf-8'))
            return

def main():
    global capture
    capture = cv2.VideoCapture(0)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, 1080); 
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 720);
    try:
        server = HTTPServer(('0.0.0.0',8080),CamHandler)
        print("server started")
        server.serve_forever()
    except KeyboardInterrupt:
        capture.release()
        server.socket.close()

if __name__ == '__main__':
    main()

