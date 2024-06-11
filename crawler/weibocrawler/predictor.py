import os
import torch
import numpy as np
import torch.nn as nn
from torchvision import transforms

model_path = "models"
model_name = "rotate_model_V2.pth"

# 定义图像的CNN模型
class ImageBranch(nn.Module):
    def __init__(self, in_channels=3, num_filters=32, kernel_size=5, padding=1):
        super(ImageBranch, self).__init__()
        
        self.cnn = nn.Sequential(
            nn.Conv2d(in_channels, num_filters, kernel_size, padding=padding),
            nn.BatchNorm2d(num_filters),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=2, stride=2),
            
            nn.Conv2d(num_filters, num_filters*2, kernel_size, padding=padding),
            nn.BatchNorm2d(num_filters*2),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=3, stride=2),
            
            nn.Conv2d(num_filters*2, num_filters*4, kernel_size, padding=padding),
            nn.BatchNorm2d(num_filters*4),
            nn.ReLU(),
            nn.MaxPool2d(kernel_size=5, stride=2),
        )
        self.flatten = nn.Flatten()

    def forward(self, x):
        x = self.cnn(x)
        x = self.flatten(x)
        return x

# 定义主模型
class RotationPredictor(nn.Module):
    def __init__(self):
        super(RotationPredictor, self).__init__()

        self.image_branch = ImageBranch()
        
        self.sigmoid = nn.Sigmoid()
        self.ReLU = nn.ReLU()
        
        self.LN1 = nn.Linear(8448,2112)
        self.norm1 = nn.BatchNorm1d(2112)
        
        self.LN2 = nn.Linear(2112, 528)
        self.norm2 = nn.BatchNorm1d(528)
        
        self.output_layer = nn.Linear(528, 360)

    def forward(self, image):
        features = self.image_branch(image)
        
        features = self.LN1(features)
        features = self.ReLU(features)
        features = self.norm1(features)
        
        features = self.LN2(features)
        features = self.ReLU(features)
        features = self.norm2(features)

        output = self.output_layer(features)
        output = self.sigmoid(output)
        return output

builtin_transformer = transforms.Compose([
                                  transforms.Resize((80, 120)),
                                  transforms.ToTensor()
                                  ])
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
default_model = RotationPredictor()

if os.path.exists(os.path.join(model_path, model_name)):
    default_model.load_state_dict(torch.load(os.path.join(model_path, model_name)))
    default_model.eval()
    default_model.to(device)
else:
    print("[W] Model not found. Check the model name if model does exist, or else use your own model.")

def predict_rotation_angle(image, model, device=device):
    # Make prediction
    with torch.no_grad():
        if len(image.shape) == 3:
            image = torch.reshape(image, (1, 3, 80, 120))
        image = image.to(device)
        output = model(image)
        output = list(map(lambda x: np.argmax(list(map(lambda y: y.detach().to('cpu'), x))), output))
    return output

def predict(background_image, center_image, model=default_model, x = 100, y = 0):
    """预测中心验证码的旋转角度

    Args:
        background_image ( `list[ Image ]` | `Image` ): 背景图片
        center_image ( `Image` ): 中心图片
        model ( `RotationPredictor`, optional ): 预测模型. 默认使用models文件夹下的模型.
        x ( `int`, optional ): 中心图片相对背景图片的x轴坐标. 默认为100.
        y ( `int`, optional ): 中心图片相对背景图片的y轴坐标. 默认为0.

    Returns:
        `list[ int ]`: 预测的角度
    """
    background_image = background_image.convert("RGBA")
    center_image = center_image.convert("RGBA")
    
    # 粘贴图像
    background_image.alpha_composite(center_image, (x, y))
    
    background_image = builtin_transformer(background_image.convert("RGB"))
    
    # 预测旋转角度
    return predict_rotation_angle(background_image, model)
