
import cv2
import numpy as np
import colorsys

def detect_color(image):
    # Convert image from BGR to HSV color space
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
    # Define the range of colors you want to detect
    lower_color = np.array([hue_min, saturation_min, value_min])
    upper_color = np.array([hue_max, saturation_max, value_max])
    
    # Threshold the HSV image to get only the specified colors
    mask = cv2.inRange(hsv_image, lower_color, upper_color)
    
    # Bitwise-AND mask and original image
    result = cv2.bitwise_and(image, image, mask=mask)
    
    return result, hsv_image

def closest_color_name(rgb_color):
    # Predefined color names and their RGB values
    color_names = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        # Add more color names and RGB values as needed
    }
    
    # Calculate Euclidean distance between the detected color and predefined colors
    distances = {name: np.linalg.norm(np.array(rgb_color) - np.array(value)) for name, value in color_names.items()}
    
    # Get the name of the closest color
    closest_color = min(distances, key=distances.get)
    
    return closest_color

# Define the color range you want to detect (e.g., blue color)
hue_min = 100
saturation_min = 50
value_min = 50
hue_max = 140
saturation_max = 255
value_max = 255

# Open the camera
cap = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    
    if not ret:
        break
    
    # Detect color
    color_detected, hsv_image = detect_color(frame)
    
    # Get the average HSV values of the detected region
    avg_hue = np.mean(hsv_image[:,:,0])
    avg_saturation = np.mean(hsv_image[:,:,1])
    avg_value = np.mean(hsv_image[:,:,2])
    
    # Convert HSV values to RGB
    rgb_color = tuple(map(int, colorsys.hsv_to_rgb(avg_hue / 179.0, avg_saturation / 255.0, avg_value / 255.0)))
    
    # Get the color name of the detected region
    color_name = closest_color_name(rgb_color)
    
    # Display the original and detected color images
    cv2.imshow('Original Image', frame)
    cv2.imshow('Detected Color', color_detected)
    print("Detected Color Name:", color_name)
    
    # Break the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close all windows
cap.release()
cv2.destroyAllWindows()
