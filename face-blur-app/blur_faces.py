import cv2

# Load the pre-trained face detection model
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# Load the image
img = cv2.imread('group_photo.jpg')

# Convert to grayscale (Haar cascade works better on grayscale)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect faces
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

print(f"Detected {len(faces)} face(s).")

# Blur each detected face region
for (x, y, w, h) in faces:
    face_region = img[y:y+h, x:x+w]
    # Apply Gaussian blur
    blurred_face = cv2.GaussianBlur(face_region, (99, 99), 30)
    img[y:y+h, x:x+w] = blurred_face

# Display the result
cv2.imshow('Blurred Faces', img)

cv2.waitKey(0)
cv2.destroyAllWindows()

# Optionally save the output
cv2.imwrite('blurred_output.jpg', img)
print("✅ Blurred image saved as blurred_output.jpg")
