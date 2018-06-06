import picamera
import time

#Settup the camera
camera = picamera.PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
camera.preview_fullscreen = False
camera.preview_window = (40,40, 680, 520)
camera.start_preview()

#Preview running at this point
while True:
    try:
        # Sleep the cpu, wait for a keyboard interrupt.
        time.sleep(0.1)
    #Press CTRL+C to stop the preview and take a picture
    except KeyboardInterrupt:
        camera.capture ('test.jpg')
        camera.stop_preview()
        camera.close()
        break

print("Captured test.jpg")
