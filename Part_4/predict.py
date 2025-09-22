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
    file_path = sys.argv[1]

    if not os.path.isfile(file_path):
        print(f"Error: <{file_path}> is not a valid file")
        sys.exit(1)

    if not file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        print("Error: Unsupported file format.")
        sys.exit(1)

    os.makedirs('predict', exist_ok=True)
    img, pred = predict_image(file_path)

    fig, ax = plt.subplots(figsize=(5, 5))

    ax.imshow(img)
    ax.axis('off')

    fig.patch.set_facecolor('black')
    plt.subplots_adjust(bottom=0.25)

    txt = f"Class predicted : {pred}"
    ha = "center"
    va = "center"
    fig.text(0.5, 0.15, txt, ha=ha, va=va, fontsize=14, color="lightgreen")

    out_path = os.path.join('predict', f'{pred}.png')
    plt.savefig(out_path)
    print(f"Résultat enregistré dans : {out_path}")
