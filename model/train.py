import os
import argparse
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
from torch.utils.tensorboard import SummaryWriter
#from torchvision import models
from pathlib import Path

import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from model.dataset import DriverDataset, get_transforms
from model.projectmodels import get_model

# use an argument parser to minimise hardcoding
def parse_args():
    parser = argparse.ArgumentParser(description="Train driver behaviour classifier")
    parser.add_argument("--data_dir", type=str, required=True, help="Path to training images")
    parser.add_argument("--epochs", type=int, default=10)
    parser.add_argument("--batch_size", type=int, default=32)
    parser.add_argument("--lr", type=int, default=1e-3)
    parser.add_argument("--model", type=str, default="mobilenet_v3_small") #mostly redundant but worth keeping for future projects that might use multiple models or ensembles
    parser.add_argument("--num_workers", type=int, default=4)
    parser.add_argument("--checkpoint_dir", type=str, default="model/checkpoints") #to store training checkpoints, especially for long training or high epochs
    parser.add_argument("--seed", type=int, default=501) # for reproducibility

    return parser.parse_args()

def set_seed(seed):
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

def create_dataloaders(data_dir, batch_size, num_workers):
    full_ds = DriverDataset(data_dir, transform=None)
    train_tf, val_tf = get_transforms()
    train_size = int(0.8 * len(full_ds))
    val_size = len(full_ds) - train_size

    train_ds, val_ds = random_split(full_ds, [train_size, val_size])
    train_ds.dataset.transform = train_tf
    val_ds.dataset.transform = val_tf

    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=num_workers, persistent_workers=True)
    val_loader   = DataLoader(val_ds, batch_size=batch_size, shuffle=False, num_workers=num_workers, persistent_workers=True)

    return train_loader, val_loader

# def build_model():
#     m = models.mobilenet_v3_small(weights="IMAGENET1K_V1")
#     m.classifier[3] = nn.Linear(m.classifier[3].in_features, 10)
#     return m

def train_epoch(model, loader, loss_fn, opt, device):
    model.train()
    running_loss = 0
    correct = 0
    total = 0

    for imgs, labels in loader:
        imgs, labels = imgs.to(device), labels.to(device)
        opt.zero_grad()
        out = model(imgs)
        loss = loss_fn(out, labels)
        loss.backward()
        opt.step()

        running_loss += loss.item() * imgs.size(0)
        preds = out.argmax(1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

    return running_loss / total, correct / total

def validate(model, loader, loss_fn, device):
    model.eval()
    running_loss = 0
    correct = 0
    total = 0

    with torch.no_grad():
        for imgs, labels in loader:
            imgs, labels = imgs.to(device), labels.to(device)
            
            out = model(imgs)
            loss = loss_fn(out, labels)

            running_loss += loss.item() * imgs.size(0)
            preds = out.argmax(1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)

    return running_loss / total, correct / total

def main():
    args = parse_args()
    set_seed(args.seed)

    device = "cuda" if torch.cuda.is_available() else "cpu"

    train_loader, val_loader = create_dataloaders(args.data_dir, args.batch_size, args.num_workers)
    model = get_model(args.model).to(device)

    opt = torch.optim.AdamW(model.parameters(), lr=args.lr)
    loss_fn = nn.CrossEntropyLoss()

    writer = SummaryWriter(log_dir="model/runs")

    os.makedirs(args.checkpoint_dir, exist_ok=True)
    best_val_acc = 0
    patience = 5
    patience_counter = 0

    print(f"Beginning training for model: {args.model} on {device}")
    for epoch in range(args.epochs):
        train_loss, train_acc = train_epoch(model, train_loader, loss_fn, opt, device)
        val_loss, val_acc = validate(model, val_loader, loss_fn, device)

        writer.add_scalars("Loss", {"train": train_loss, "val": val_loss}, epoch)
        writer.add_scalars("Accuracy", {"train": train_acc, "val": val_acc}, epoch)

        print(f"Epoch {epoch+1}/{args.epochs} "
              f"Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f} "
              f"Val Loss: {val_loss:.4f} | Val Acc: {val_acc:.4f}")

        # early stop and checkpoint
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            ckpt_path = Path(args.checkpoint_dir) / f"{args.model}_best.pth"
            torch.save(model.state_dict(), ckpt_path)
            print(f"Saved checkpoint: {ckpt_path}")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping triggered")
                break

    writer.close()

if __name__ == "__main__":
    main()
