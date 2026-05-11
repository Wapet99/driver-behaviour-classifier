import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import models
import json
from pathlib import Path

from dataset import DriverDataset, get_transforms

def build_model():
    m = models.mobilenet_v3_small(weights="IMAGENET1K_V1")
    m.classifier[3] = nn.Linear(m.classifier[3].in_features, 10)
    return m

def train():
    train_tf, val_tf = get_transforms()

    train_ds = DriverDataset("data/imgs", transform=train_tf)
    val_ds   = DriverDataset("data/imgs", transform=val_tf)

    train_loader = DataLoader(train_ds, batch_size=32, shuffle=True, num_workers=4)
    val_loader   = DataLoader(val_ds, batch_size=32, shuffle=False, num_workers=4)

    device = "cuda" if torch.cuda.is_available() else "cpu"
    model = build_model().to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=1e-3)
    loss_fn = nn.CrossEntropyLoss()

    best_acc = 0
    metrics = {}

    for epoch in range(10):
        model.train()
        for imgs, labels in train_loader:
            imgs, labels = imgs.to(device), labels.to(device)
            opt.zero_grad()
            out = model(imgs)
            loss = loss_fn(out, labels)
            loss.backward()
            opt.step()

        # validation
        model.eval()
        correct = 0
        total = 0
        with torch.no_grad():
            for imgs, labels in val_loader:
                imgs, labels = imgs.to(device), labels.to(device)
                preds = model(imgs).argmax(1)
                correct += (preds == labels).sum().item()
                total += labels.size(0)

        acc = correct / total
        metrics[epoch] = acc
        print(f"Epoch {epoch}: val_acc={acc:.4f}")

        if acc > best_acc:
            best_acc = acc
            torch.save(model.state_dict(), "model.pt")

    with open("metrics.json", "w") as f:
        json.dump(metrics, f)

if __name__ == "__main__":
    train()
