import sys
import os
from PIL import Image, ImageEnhance, ImageFilter, ImageOps
import math
import random

# 1. Flip 
def flip_image(img):
    return ImageOps.mirror(img)

# 2. Rotate 
def rotate_image(img, angle=None):
    if angle is None:
        angle = random.randint(-30, 30)
    return img.rotate(angle, expand=True)
# 3. Crop 
def crop_image(img):
    width, height = img.size
    crop_size = 0.8
    left = int(width * (1 - crop_size) / 2)
    top = int(height * (1 - crop_size) / 2)
    right = int(width * (1 + crop_size) / 2)
    bottom = int(height * (1 + crop_size) / 2)
    return img.crop((left, top, right, bottom)).resize((width, height))

# 4. Distortion 
def distort_image(img):
    width, height = img.size
    new_width = int(width * 2)
    new_height = int(height * 2)
    
    distorted_img = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    
    offset_x = (new_width - width) // 2
    offset_y = (new_height - height) // 2
    distorted_img.paste(img, (offset_x, offset_y))
    
    coeffs = (1, -0.01, 0, -0.01, 1, 0, -0.001, 0.001)
    
    return distorted_img.transform((new_width, new_height), Image.PERSPECTIVE, coeffs, Image.BICUBIC)

# 5. Shear
def shear_image(img):
     width, height = img.size
     shear_factor = math.tan(math.radians(random.randint(-20, 20)))
     
     new_width = int(width * 2) 
     new_height = int(height * 1.5)
     
     sheared_img = Image.new('RGB', (new_width, new_height), (0, 0, 0))
     
     offset_x = (new_width - width) // 2
     offset_y = (new_height - height) // 2
     sheared_img.paste(img, (offset_x, offset_y))
     
     coeffs = (1, shear_factor, 0,
               0, 1, 0)
     return sheared_img.transform((new_width, new_height), Image.AFFINE, coeffs, Image.BICUBIC)

# 6. Skew
def skew_image(img):
    width, height = img.size
    skew_factor = math.tan(math.radians(20))
    
    new_width = int(width * 2)
    new_height = int(height * 2)
    
    skewed_img = Image.new('RGB', (new_width, new_height), (0, 0, 0))
    
    offset_x = (new_width - width) // 2
    offset_y = (new_height - height) // 2
    skewed_img.paste(img, (offset_x, offset_y))
    
    coeffs = (1, skew_factor, 0,
              0, 1, 0)
    return skewed_img.transform((new_width, new_height), Image.AFFINE, coeffs, Image.BICUBIC)

if __name__ == "__main__":
    type = [".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".webp", "tif"]
    if len(sys.argv) == 2:
        if len(sys.argv[1]) < 4:
            print("Error : Invalid file name.")
        elif sys.argv[1][-4:].lower() not in type and sys.argv[1][-5:].lower() not in type:
            print("Error : Invalid file type.")
        else:
            file_name = os.path.splitext(sys.argv[1])[0]
            print(file_name)
            image = Image.open(sys.argv[1])
            flipped_image = flip_image(image)
            flipped_image.save(f"{file_name}_Flip.jpg")
            rotated_image = rotate_image(image)
            rotated_image.save(f"{file_name}_Rotate.jpg")            
            cropped_image = crop_image(image)
            cropped_image.save(f"{file_name}_Crop.jpg")
            distorted_image = distort_image(image)
            distorted_image.save(f"{file_name}_Distortion.jpg")
            sheared_image = shear_image(image)
            sheared_image.save(f"{file_name}_Shear.jpg")
            skewed_image = skew_image(image)
            skewed_image.save(f"{file_name}_Skew.jpg")
            print("Augmented images saved successfully.")
    else:
        print("Error : Invalid number of arguments.")
