import os
import glob
from PIL import Image
from torch.utils.data import Dataset
from torchvision import transforms

class DriverDataset(Dataset):
    def __init__(self, root, transform=None):
        self.root = root
        self.transform = transform
        
        self.samples = []
        classes = sorted(os.listdir(root))
        self.class_to_idx = {c: i for i, c in enumerate(classes)}
        
        for c in classes:
            paths = glob.glob(os.path.join(root, c, "*.jpg"))
            for p in paths:
                self.samples.append((p, self.class_to_idx[c]))

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, idx):
        path, label = self.samples[idx]
        img = Image.open(path).convert("RGB")
        
        if self.transform:
            img = self.transform(img)
        
        return img, label


def get_transforms():
    train_tf = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.RandomHorizontalFlip(),
        transforms.ColorJitter(brightness=0.3, contrast=0.3),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    val_tf = transforms.Compose([
        transforms.Resize((224,224)),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406],
                             std=[0.229, 0.224, 0.225])
    ])

    return train_tf, val_tf