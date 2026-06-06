import cv2

# Open your Mac's webcam
camera = cv2.VideoCapture(0)

print("Camera online... press Esc to quit")

while True:
    # Read a frame from the camera
    ret, frame = camera.read()
    
    # Load face detection model
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces
    faces = face_detector.detectMultiScale(frame, 1.1, 4)
    
    # Draw a box around each face
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        print("Face detected!")
    
    # Show the camera feed
    cv2.imshow('Vector Eye', frame)
    
    # Press esc to quit
    if cv2.waitKey(1) & 0xFF == 27:
        break

camera.release()
cv2.destroyAllWindows()
print("Camera offline.")