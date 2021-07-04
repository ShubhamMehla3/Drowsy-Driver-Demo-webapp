from django.shortcuts import render
from django.http.response import StreamingHttpResponse
from livestream.camera import VideoCamera, eyedet
# Create your views here.
FRAME_COUNTER = 0

def index(request):
	return render(request, 'index.html')


def gen(camera):
	FRAME_COUNTER = 0
	while True:
		frame, FRAME_COUNTER = camera.get_frame(FRAME_COUNTER)
		yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def video_feed(request):
	return StreamingHttpResponse(gen(VideoCamera()), content_type='multipart/x-mixed-replace; boundary=frame')

def eyedet_feed(request):
	return StreamingHttpResponse(gen(eyedet()), content_type='multipart/x-mixed-replace; boundary=frame')