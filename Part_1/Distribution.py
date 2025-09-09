import os, sys, json
from collections import defaultdict
import matplotlib.pyplot as plt
from loguru import logger

colors = [
    "red", "blue", "green", "orange", "orange", "purple", "pink",
    "brown", "gray", "cyan", "magenta", "teal", "navy", "beige", "maroon", "olive",
    "turquoise", "gold", "silver", "lavender", "peach", "coral"
]

def get_percentage(value, total):
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
    
    data = {}
    for dir_name in os.listdir(root_dir):
        path = os.path.join(root_dir, dir_name)
        if os.path.isdir(path):
            nb_imgs = len(os.listdir(path))
            data[dir_name] = nb_imgs
    
    # Nombre d'images total par catégorie
    total_by_category = defaultdict(int)
    for dir_name, nb_imgs in data.items():
        category = extract_category(dir_name)
        total_by_category[category] += nb_imgs

    logger.debug(json.dumps(data, indent=2, sort_keys=True))
    logger.debug(json.dumps(total_by_category, indent=2, sort_keys=True))

    # {category: {dir_name: nb%}}
    new_data = defaultdict(dict)
    for dir_name, nb_imgs in data.items():
        category = extract_category(dir_name)
        new_data[category][dir_name] = (nb_imgs, get_percentage(nb_imgs, total_by_category[category]))
    
    logger.debug(json.dumps(new_data, indent=2, sort_keys=True))
    
    current_dir = os.getcwd()
    charts_dir = os.path.join(current_dir, r'charts')
    # pie chart
    try:
        for category, dir_name in new_data.items():
            labels = list(dir_name.keys())
            sizes = [dir_name[name][1] for name in dir_name]
            fig, ax = plt.subplots()
            pie_colors= colors[0:len(labels)]
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=pie_colors)
            if not os.path.exists(charts_dir):
                os.makedirs(charts_dir)
            pie_chart_path = os.path.join(charts_dir, f'{category}_pie.png')
            plt.savefig(pie_chart_path)
    except Exception as e:
        logger.error(e)
    
    # bar chart
    try:
        for category, dir_name in new_data.items():
            labels = list(dir_name.keys())
            values = [dir_name[name][0] for name in dir_name]
            fig, ax = plt.subplots()
            bar_colors = colors[0:len(labels)]
            ax.bar(labels, values, label=labels, color=bar_colors)
            if not os.path.exists(charts_dir):
                os.makedirs(charts_dir)
            bar_chart_path = os.path.join(charts_dir, f'{category}_chart.png')
            plt.savefig(bar_chart_path)
    except Exception as e:
        logger.error(e)

    #print(json.dumps(new_data, indent=2, ensure_ascii=False, sort_keys=True))
if __name__ == "__main__":
    main()