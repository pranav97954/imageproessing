from django.shortcuts import render
from django.http import JsonResponse
import cv2
import numpy as np


def upload_image(request):
    if request.method == 'POST':
        image_file = request.FILES.get('image')
        if image_file:
            # Load the image and convert it to RGB
            img = cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            # Define the color ranges to be extracted
            colors = {
                'URO': [[0, 0, 0], [183, 172, 152]],
                'BIL': [[191, 174, 0], [255, 255, 146]],
                'KET': [[164, 134, 69], [174, 165, 148]],
                'BLD': [[166, 0, 0], [255, 55, 0]],
                'PRO': [[119, 102, 85], [158, 161, 128]],
                'NIT': [[210, 195, 120], [255, 255, 146]],
                'LEU': [[168, 149, 81], [172, 164, 144]],
                'GLU': [[118, 102, 59], [158, 163, 133]],
                'SG': [[166, 153, 51], [175, 174, 140]],
                'PH': [[149, 112, 0], [169, 154, 117]]
            }
            # Extract the color regions using color thresholding
            color_regions = {}
            for color, (lower, upper) in colors.items():
                mask = cv2.inRange(img, np.array(lower), np.array(upper))
                color_regions[color] = cv2.bitwise_and(img, img, mask=mask)

            # Extract the RGB values of each color region
            color_values = {}
            for color, region in color_regions.items():
                pixels = np.float32(region.reshape(-1, 3))
                n_pixels = pixels.shape[0]
                color_values[color] = np.sum(pixels, axis=0) / n_pixels

            # Convert the RGB values to integers
            color_values = {color: list(map(int, values)) for color, values in color_values.items()}

            # Return the color values as JSON
            return JsonResponse(color_values)
        else:
            # Display error message to the user
            message = "Please upload an image file."
            return JsonResponse({"error": message})
    else:
        return render(request, "index.html")
