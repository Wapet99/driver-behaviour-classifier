import torch
import torch.nn as nn
from torchvision import models

## A custom mini CNN
class MiniCNN(nn.Module):
    def __init__(self, num_classes=10):
        super().__init__()

        def dw_sep(in_ch, out_ch, stride):
            return nn.Sequential(
                nn.Conv2d(in_ch, in_ch, 3, stride=stride, padding=1, groups=in_ch, bias=False),
                nn.BatchNorm2d(in_ch),
                nn.ReLU(inplace=True),

                nn.Conv2d(in_ch, out_ch, 1, bias=False),
                nn.BatchNorm2d(out_ch),
                nn.ReLU(inplace=True),
            )

        self.features = nn.Sequential(
            dw_sep(3, 16, stride=2),
            dw_sep(16, 32, stride=2),
            dw_sep(32, 64, stride=2),
            dw_sep(64, 96, stride=1),
            dw_sep(96, 128, stride=1),
            nn.AdaptiveAvgPool2d((1, 1)),
        )
        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(128, num_classes),
        )

    def forward(self, x):
        x = self.features(x)
        x = x.flatten(1)
        return self.classifier(x)
    
## MobileNetV3-Small
def mobilenet_v3_small(num_classes=10):
    m = models.mobilenet_v3_small(weights=None)
    m.classifier[3] = nn.Linear(m.classifier[3].in_features, num_classes)
    return m

## Efficientnet-b0
def efficientnet_b0(num_classes=10):
    m = models.efficientnet_b0(weights="IMAGENET1K_V1")
    m.classifier[1] = nn.Linear(m.classifier[1].in_features, num_classes)
    return m

## Shufflenet-v2
def shufflenet_v2(num_classes=10):
    m = models.shufflenet_v2_x1_0(weights="IMAGENET1K_V1")
    m.fc = nn.Linear(m.fc.in_features, num_classes)
    return m

## Resnet18
def resnet18(num_classes=10):
    m = models.resnet18(weights="IMAGENET1K_V1")
    m.fc = nn.Linear(m.fc.in_features, num_classes)
    return m


def get_model(name: str, num_classes: int=10):
    name = name.lower()

    if name == "minicnn":
        return MiniCNN(num_classes)
    if name == "mobilenet_v3_small":
        return mobilenet_v3_small(num_classes)
    if name == "shufflenet":
        return shufflenet_v2(num_classes)
    if name == "resnet18":
        return resnet18(num_classes)
    if name == "efficientnet_b0":
        return efficientnet_b0(num_classes)
    
    raise ValueError(f"Unknown model name: {name}") # if requested model isn't in project models