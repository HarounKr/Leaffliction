import os
import sys
import fastai.vision.all as fv
from pathlib import Path
import matplotlib.pyplot as plt
import shutil

# https://www.machinelearningexpedition.com/image-classification-using-fastai/


def save_batch(batch, data, path, cols=12):
    imgs, labels = batch
    n = len(labels)  # Nombre d'images dans le batch

    rows = (n + cols - 1) // cols
    fig, ax = plt.subplots(rows, cols, figsize=(cols*2, rows*2))
    ax = ax.flatten()

    sorted_idx = labels.argsort()

    for i, idx in enumerate(sorted_idx):
        img = imgs[idx].permute(1, 2, 0).cpu()
        lab = labels[idx].item()
        ax[i].imshow(img)
        ax[i].set_title(data.vocab[lab])
        ax[i].axis('off')

    for j in range(n, len(ax)):  # masquer cases vides
        ax[j].axis('off')

    plt.tight_layout()
    plt.savefig(path)
    plt.close(fig)


def main():
    if len(sys.argv) != 2:
        print("Usage: python Distribution.py <directory>")
        sys.exit(1)

    root_dir = Path(sys.argv[1])
    if not os.path.isdir(root_dir):
        print("Error: invalid path.")
        sys.exit(1)

    result_dir_path = os.path.join(os.getcwd(), 'result')
    os.makedirs(result_dir_path, exist_ok=True)

    item_tfms = fv.RandomResizedCrop(224, min_scale=0.5)
    batch_tfms = [
                fv.Contrast(max_lighting=0.2, p=0.75),
                fv.Brightness(max_lighting=0.4, p=0.75),
                *fv.aug_transforms(size=224, min_scale=0.75),
                fv.Normalize.from_stats(*fv.imagenet_stats)
            ]

    data = fv.ImageDataLoaders.from_folder(
        root_dir,
        valid_pct=0.2,
        seed=42,
        bs=64,
        num_workers=2,
        persistent_workers=True,
        item_tfms=item_tfms,
        batch_tfms=batch_tfms
    )

    train_batch = data.train.one_batch()
    batch_file_path = os.path.join(result_dir_path, 'batch.png')

    save_batch(batch=train_batch, data=data, path=batch_file_path)

    learn = fv.vision_learner(data, fv.resnet18, metrics=fv.accuracy)
    learn.fine_tune(2)

    model_file_path = os.path.join(result_dir_path, 'model.pkl')
    learn.export(model_file_path)

    shutil.make_archive(result_dir_path, 'zip', result_dir_path)


if __name__ == "__main__":
    main()
