import cv2

def preprocess_image(image_path):
    # Rescale the image (2x) - improves OCR on small text
    img = cv2.imread(image_path)
    height, width = img.shape[:2]
    img = cv2.resize(img, (width * 2, height * 2), interpolation=cv2.INTER_CUBIC)

    # Convert to gray
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply adaptive thresholding - handles glare/shadows better than Otsu
    processed = cv2.adaptiveThreshold(
        gray, 255, 
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY, 
        31, 2
    )
    
    # Denoise slightly
    processed = cv2.medianBlur(processed, 3)
    
    return processed
