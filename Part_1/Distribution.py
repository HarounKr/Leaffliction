import os
import sys
from collections import defaultdict
import matplotlib.pyplot as plt

colors = [
    "red", "blue", "green", "orange", "purple", "pink",
    "brown", "gray", "cyan", "magenta", "teal", "navy",
    "beige", "maroon", "olive", "turquoise", "gold",
    "silver", "lavender", "peach", "coral"
]


def get_percentage(value, total) -> float:
    if total == 0:
        return 0.0
    return round((value * 100) / total, 1)


def extract_category(name: str) -> str:
    return name.split('_')[0]


def create_pie_chart(sizes, labels, charts_dir, category) -> None:
    fig, ax = plt.subplots()
    labels_len = len(labels)
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors[:labels_len])
    plt.savefig(os.path.join(charts_dir, f'{category}_pie.png'))
    plt.tight_layout()
    plt.close(fig)


def create_bar_chart(labels, values, charts_dir, category) -> None:
    fig, ax = plt.subplots()
    ax.bar(labels, values, color=colors[:len(labels)])
    plt.savefig(os.path.join(charts_dir, f'{category}_bar.png'))
    plt.tight_layout()
    plt.close(fig)


def handle_subdirs(subdirs, root_dir, exts, charts_dir):
    data = {}
    # Compter les fichiers dans chaque sous dossier (catégorie)
    for dir_name in subdirs:
        path = os.path.join(root_dir, dir_name)
        nb_imgs = 0
        for file in os.listdir(path):
            if file.lower().endswith(exts):
                nb_imgs += 1
        data[dir_name] = nb_imgs

    # Totaux par sous dossier (catégorie)
    total_by_category = defaultdict(int)
    for dir_name, nb_imgs in data.items():
        category = extract_category(dir_name)
        total_by_category[category] += nb_imgs

    # {category: {dir_name: (count, percent)}}
    new_data = defaultdict(dict)
    for dir_name, nb_imgs in data.items():
        category = extract_category(dir_name)
        percentage = get_percentage(nb_imgs, total_by_category[category])
        new_data[category][dir_name] = (nb_imgs, percentage)

    # Pie charts
    for category, entries_dict in new_data.items():
        labels = list(entries_dict.keys())
        percentages = [entries_dict[name][1] for name in labels]
        create_pie_chart(percentages, labels, charts_dir, category)

    # Bar charts
    for category, entries_dict in new_data.items():
        labels = list(entries_dict.keys())
        values = [entries_dict[name][0] for name in labels]
        create_bar_chart(labels, values, charts_dir, category)


def handle_files(entries, root_dir, exts, charts_dir) -> None:
    files_name = []
    for f in entries:
        if os.path.isfile(os.path.join(root_dir, f)):
            if f.lower().endswith(exts):
                files_name.append(f)
    files = defaultdict(int)
    for f in files_name:
        name, _ = os.path.splitext(f)
        version = name.rsplit('_', 1)[-1]
        files[version] += 1
    labels = list(files.keys())
    values = [files[k] for k in labels]
    total = sum(values)
    percentages = [get_percentage(v, total) for v in values]

    # Nommer les fichirs charts avec le nom du dossier
    dir_name = os.path.basename(os.path.normpath(root_dir))

    # Pie chart
    create_pie_chart(percentages, labels,  charts_dir, dir_name)

    # Bar chart
    create_bar_chart(labels, values, charts_dir, dir_name)


def main():
    if len(sys.argv) != 2:
        print("Usage: python Distribution.py <directory>")
        sys.exit(1)

    root_dir = sys.argv[1]
    if not os.path.isdir(root_dir):
        print("Error: invalid path.")
        sys.exit(1)

    exts = (".jpg", ".jpeg", ".png")
    entries = os.listdir(root_dir)
    subdirs = [d for d in entries if os.path.isdir(os.path.join(root_dir, d))]

    charts_dir = os.path.join(os.getcwd(), "charts")
    os.makedirs(charts_dir, exist_ok=True)

    if subdirs:
        handle_subdirs(subdirs, root_dir, exts, charts_dir)
    else:
        handle_files(entries, root_dir, exts, charts_dir)


if __name__ == "__main__":
    main()
