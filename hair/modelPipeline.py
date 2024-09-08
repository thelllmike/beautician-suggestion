import os
import torch
import torchvision
import torch.nn as nn
from torchvision.models.detection import maskrcnn_resnet50_fpn
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import torchvision.transforms as T
from transformers import ViTForImageClassification

# Get the current directory of the file
current_dir = os.path.dirname(os.path.abspath(__file__))

# Model paths are now relative to the current directory
mask_model_path = os.path.join(current_dir, "hair_maskrcnn.pth")
transformer_modelPath = os.path.join(current_dir, "haiClassification_mask.pth")

def display_binary_hair_mask(image, predictions, hair_label=1, threshold=0.3):
    image = image.permute(1, 2, 0).cpu().numpy()
    labels = predictions[0]['labels'].cpu().numpy()
    scores = predictions[0]['scores'].cpu().numpy()
    masks = predictions[0]['masks'].cpu().numpy()
    keep = (scores >= threshold) & (labels == hair_label)
    masks = masks[keep]

    if len(masks) == 0:
        print("No hair detected.")
        return None

    hair_mask = masks[0, 0]
    binary_mask = (hair_mask >= threshold).astype(np.uint8)
    plt.imshow(binary_mask, cmap='gray')
    plt.axis('off')
    maskName = os.path.join(current_dir, "Hair_mask.png")  # Save the mask relative to the current directory
    plt.savefig(maskName, bbox_inches='tight', pad_inches=0)
    plt.close()
    return maskName

def preprocess_image(image_path):
    image = Image.open(image_path).convert("RGB")
    preprocess = T.Compose([
        T.Resize((224, 224)),
        T.ToTensor(),
    ])
    image = preprocess(image).unsqueeze(0)
    return image

def preprocess_image_mask(image_path):
    image = Image.open(image_path).convert("RGB")
    preprocess = T.Compose([T.ToTensor()])
    image = preprocess(image).unsqueeze(0)
    return image

def load_mask_rcnn_model(model_path):
    num_classes = 2
    model = maskrcnn_resnet50_fpn(pretrained=True)
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = torchvision.models.detection.faster_rcnn.FastRCNNPredictor(in_features, num_classes)

    in_features_mask = model.roi_heads.mask_predictor.conv5_mask.in_channels
    hidden_layer = 256
    model.roi_heads.mask_predictor = torchvision.models.detection.mask_rcnn.MaskRCNNPredictor(in_features_mask, hidden_layer, num_classes)

    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def load_vit_model(model_path, num_labels=4):
    model = ViTForImageClassification.from_pretrained('google/vit-base-patch16-224-in21k', num_labels=num_labels)
    model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu')))
    model.eval()
    return model

def Pipeline(image_path_url):
    mask_model = load_mask_rcnn_model(mask_model_path)
    vit_model = load_vit_model(transformer_modelPath)

    device = torch.device('cpu')
    mask_model.to(device)
    vit_model.to(device)

    image = preprocess_image_mask(image_path_url).squeeze(0)
    with torch.no_grad():
        predictions = mask_model([image.to(device)])
    maskName = display_binary_hair_mask(image, predictions, hair_label=1, threshold=0.5)

    if maskName is None:
        raise ValueError("No hair detected")

    image = preprocess_image(maskName)
    with torch.no_grad():
        predictions = vit_model(image.to(device))

    result = np.array(predictions.logits)[0]
    return result
