import os
import sys
from fastai.vision.all import *
from pathlib import Path
import cv2
import matplotlib.pyplot as plt

# https://www.machinelearningexpedition.com/image-classification-using-fastai/

def train_transform_data():

    train_item_tfms = RandomResizedCrop(224, min_scale=0.5)
    train_batch_tfms = aug_transforms(min_scale=0.75) + [Normalize.from_stats(*imagenet_stats)]

    return train_item_tfms, train_batch_tfms

def validation_transform_data():

    val_item_tfms   = Resize(224, method=ResizeMethod.Crop)
    val_batch_tfms  = [Normalize.from_stats(*imagenet_stats)]

    return val_item_tfms, val_batch_tfms

def save_batch(batch, data):
    imgs, labels = batch
    n = len(labels)   # nombre d'images dans le batch

    cols = 12
    rows = (n + cols - 1) // cols   # arrondi pour couvrir toutes les images

    fig, ax = plt.subplots(rows, cols, figsize=(cols*2, rows*2))
    ax = ax.flatten()

    for i in range(n):
        img = imgs[i].permute(1,2,0).cpu()
        lab_i = labels[i].item()
        ax[i].imshow(img)
        ax[i].set_title(data.vocab[lab_i])
        ax[i].axis('off')

    plt.tight_layout()
    plt.savefig('batch.png')

def main():
    if len(sys.argv) != 2:
        print("Usage: python Distribution.py <directory>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])
    if not os.path.isdir(root_dir):
        print("Error: invalid path.")
        sys.exit(1)

    train_item_tfms, train_batch_tfms = train_transform_data()
    val_item_tfms, val_batch_tfms = validation_transform_data()
  
    data = ImageDataLoaders.from_folder(
        root_dir,
        valid_pct=0.2,
        seed=42,
        bs=32,
        item_tfms=(train_item_tfms, val_item_tfms),
        batch_tfms=(train_batch_tfms, val_batch_tfms)
    )

    train_batch = data.train.one_batch()

    save_batch(batch=train_batch, data=data)


    #learn = vision_learner(dls, resnet18, metrics=accuracy)
    #learn.fine_tune(2)

    #learn.export('dataset/model.pkl')

if __name__ == "__main__":
    main()