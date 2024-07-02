import cv2
import numpy as np
def enhance_image(image_path, alpha=1.2, beta=50):
    image = cv2.imread(image_path)
    enhanced_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
    return enhanced_image

# Example usage
image_path = 'input.jpg'
enhanced_image = enhance_image(image_path)
cv2.imwrite('enhanced_image.jpg', enhanced_image)
cv2.imshow('Enhanced Image', enhanced_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#object detection 
wget https://raw.githubusercontent.com/chuanqi305/MobileNet-SSD/deploy.prototxt
wget https://storage.googleapis.com/mobilenet_v1/SSD_MobileNet.caffemodel
def detect_objects(image_path):
    net = cv2.dnn.readNetFromCaffe('deploy.prototxt', 'SSD_MobileNet.caffemodel')
    
    image = cv2.imread(image_path)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)
    
    net.setInput(blob)
    detections = net.forward()

    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        
        if confidence > 0.2:
            idx = int(detections[0, 0, i, 1])
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            
            label = f"{confidence * 100:.2f}%"
            cv2.rectangle(image, (startX, startY), (endX, endY), (0, 255, 0), 2)
            y = startY - 15 if startY - 15 > 15 else startY + 15
            cv2.putText(image, label, (startX, y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return image

# Example usage
image_path = 'input.jpg'
detected_image = detect_objects(image_path)
cv2.imwrite('detected_objects.jpg', detected_image)
cv2.imshow('Detected Objects', detected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
#facial recognization
def detect_faces(image_path):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)
    
    return image

# Example usage
image_path = 'input.jpg'
faces_detected_image = detect_faces(image_path)
cv2.imwrite('faces_detected.jpg', faces_detected_image)
cv2.imshow('Faces Detected', faces_detected_image)
cv2.waitKey(0)
cv2.destroyAllWindows()

