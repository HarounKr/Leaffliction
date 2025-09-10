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
            fig, ax = plt.subplots()
            ax.pie(percentages, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)])
            plt.tight_layout()
            plt.savefig(os.path.join(charts_dir, f'{category}_pie.png'))
            plt.close(fig)

        # Bar charts
        for category, entries_dict in new_data.items():
            labels = list(entries_dict.keys())
            values = [entries_dict[name][0] for name in labels]
            fig, ax = plt.subplots()
            ax.bar(labels, values, color=colors[:len(labels)])
            plt.xticks(rotation=45, ha="right")
            plt.tight_layout()
            plt.savefig(os.path.join(charts_dir, f'{category}_chart.png'))
            plt.close(fig)

    else:
        files = [f for f in entries if os.path.isfile(os.path.join(root_dir, f)) and f.lower().endswith(exts)]
        counts = defaultdict(int)
        for f in files:
            name, _ = os.path.splitext(f)
            version = name.rsplit('_', 1)[-1]
            counts[version] += 1

        labels = list(counts.keys())
        values = [counts[k] for k in labels]
        total = sum(values)
        percentages = [get_percentage(v, total) for v in values]

        # Nommer les fichirs charts avec le nom du dossier
        category_name = os.path.basename(os.path.normpath(root_dir))

        # Pie chart
        fig, ax = plt.subplots()
        ax.pie(percentages, labels=labels, autopct='%1.1f%%', colors=colors[:len(labels)])
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, f'{category_name}_pie.png'))
        plt.close(fig)

        # Bar chart
        fig, ax = plt.subplots()
        ax.bar(labels, values, color=colors[:len(labels)])
        plt.xticks(rotation=45, ha="right")
        plt.tight_layout()
        plt.savefig(os.path.join(charts_dir, f'{category_name}_chart.png'))
        plt.close(fig)

if __name__ == "__main__":
    main()
