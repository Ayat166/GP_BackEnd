import numpy as np
import cv2
import torch
import albumentations as albu
from iglovikov_helper_functions.utils.image_utils import pad, unpad
from iglovikov_helper_functions.dl.pytorch.utils import tensor_from_rgb_image
from cloths_segmentation.pre_trained_models import create_model
import warnings
import os

warnings.filterwarnings("ignore")

def segment_cloth(input_image):
    model = create_model("Unet_2020-10-30")
    model.eval()

    transform = albu.Compose([albu.Normalize(p=1)], p=1)

    image = cv2.resize(input_image, (768, 1024))

    padded_image, pads = pad(image, factor=32, border=cv2.BORDER_CONSTANT)

    x = transform(image=padded_image)["image"]
    x = torch.unsqueeze(tensor_from_rgb_image(x), 0)

    with torch.no_grad():
        prediction = model(x)[0][0]

    mask = (prediction > 0).cpu().numpy().astype(np.uint8)
    mask = unpad(mask, pads)

    img = np.full((1024,768,3), 255)
    seg_img = np.full((1024,768), 0)

    b_img = mask * 255

    if image.shape[1] <= 600 and image.shape[0] <= 500:
        image = cv2.resize(image, (int(image.shape[1]*1.2),int(image.shape[0]*1.2)))
        b_img = cv2.resize(b_img, (int(b_img.shape[1]*1.2),int(b_img.shape[0]*1.2)))

    shape = b_img.shape
    img[int((1024-shape[0])/2): 1024-int((1024-shape[0])/2),int((768-shape[1])/2):768-int((768-shape[1])/2)] = image
    seg_img[int((1024-shape[0])/2): 1024-int((1024-shape[0])/2),int((768-shape[1])/2):768-int((768-shape[1])/2)] = b_img

    return {"cloth_mask_image": seg_img}

''' 
# Example usage:
input_image_path = "D:/fcai/GP/VITON_HD/VITON-HD/datasets/test/cloth/08348_00.jpg"
input_image = cv2.imread(input_image_path)
result = segment_cloth(input_image)

cloth_image = result["cloth_image"]
cloth_mask_image = result["cloth_mask_image"]

# Save the images
output_folder = "output"
os.makedirs(output_folder, exist_ok=True)

cloth_image_path = os.path.join(output_folder, "cloth_image.jpg")
cloth_mask_image_path = os.path.join(output_folder, "cloth_mask_image.jpg")

cv2.imwrite(cloth_image_path, cloth_image)
cv2.imwrite(cloth_mask_image_path, cloth_mask_image)
'''
