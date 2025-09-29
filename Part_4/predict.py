import fastai.vision.all as fv
import sys
import os
import matplotlib.pyplot as plt

learn = fv.load_learner("result/model.pkl")


def predict_image(img_file):
    img = fv.PILImage.create(img_file)
    pred, _, _ = learn.predict(img)
    return img, pred


if __name__ == '__main__':
    argv = sys.argv[1]
    paths = []
    os.makedirs('predict', exist_ok=True)
    if os.path.isfile(argv):
        paths.append(argv)
    else:
        for root, _, files in os.walk(argv, topdown=False):
            for name in files:
                if not name.lower().endswith(('.png', '.jpg', '.jpeg')):
                    print("Error: Unsupported file format.")
                    sys.exit(1)
                paths.append(os.path.join(root, name))
    paths.sort()
    for i, path in enumerate(paths, 1):
        fig, ax = plt.subplots(figsize=(5, 5))
        img, pred = predict_image(path)

        ax.imshow(img)
        ax.axis('off')

        fig.patch.set_facecolor('black')
        plt.subplots_adjust(bottom=0.25)

        txt = f"Class predicted : {pred}"
        ha = "center"
        va = "center"
        fig.text(0.5, 0.15, txt, ha=ha, va=va, fontsize=14, color="lightgreen")

        out_path = os.path.join('predict', f'{pred}_{i}.png')
        plt.savefig(out_path)
        print(f"Résultat enregistré dans : {out_path}")
