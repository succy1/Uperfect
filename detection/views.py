from django.shortcuts import render
from django.conf import settings  
from .forms import ImageUploadForm
from ultralytics import YOLO
from PIL import Image
import numpy as np
import cv2
import os

model = YOLO('model/ACNE8M.pt')

def preprocess_image(image):
    size = (800, 800)
    image.thumbnail(size, Image.Resampling.LANCZOS)
    return image

def draw_bounding_boxes(image, result):
    img = np.array(image.convert('RGB'))  
    
    for box in result.boxes:
        cords = [int(x) for x in box.xyxy[0].tolist()]  
        class_id = result.names[box.cls[0].item()]       
        conf = f"{box.conf[0].item() * 100:.0f}%"        

        # Draw bounding box
        cv2.rectangle(img, (cords[0], cords[1]), (cords[2], cords[3]), (0, 255, 0), 2)

        # Create label
        label = f"{class_id} {conf}"
        (label_width, label_height), baseline = cv2.getTextSize(
            label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1
        )
        label_y = max(cords[1] - 10, 0)

        # Draw label background
        cv2.rectangle(img, (cords[0], label_y - label_height - baseline), 
                      (cords[0] + label_width, label_y), (0, 255, 0), -1)

        # Draw label text
        cv2.putText(img, label, (cords[0], label_y - baseline),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 1, cv2.LINE_AA)

    # Convert numpy array to PIL Image
    return Image.fromarray(img)

def detect_acne(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            image = Image.open(form.cleaned_data['image'])
            processed_image = preprocess_image(image)

            # Predict
            results = model.predict(processed_image, conf=0.5)
            result = results[0]

            # Draw bounding boxes
            result_image = draw_bounding_boxes(processed_image, result)

            # Save result image
            result_image_path = os.path.join(settings.MEDIA_ROOT, 'result_image.jpg')
            result_image.save(result_image_path)

            # Return result page
            return render(request, 'result.html', {
                'image_url': settings.MEDIA_URL + 'result_image.jpg',
                'detected_acnes': len(result.boxes),
            })

    else:
        form = ImageUploadForm()
    return render(request, 'upload.html', {'form': form})
