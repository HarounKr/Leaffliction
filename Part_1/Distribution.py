import os, sys, json
from collections import defaultdict
import matplotlib.pyplot as plt

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
            imgs_nbr = len(os.listdir(path))
            data[dir_name] = imgs_nbr
    
    # Nombre d'images total par catégorie
    total_by_category = defaultdict(int)
    for dir_name, nb_imgs in data.items():
        category = extract_category(dir_name)
        total_by_category[category] += nb_imgs

    print(json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True))
    print(json.dumps(total_by_category, indent=2, ensure_ascii=False, sort_keys=True))

    # {category: {dir_name: nb%}}
    new_data = defaultdict(dict)
    for dir_name, nb_imgs in data.items():
        category = extract_category(dir_name)
        new_data[category][dir_name] = (nb_imgs, get_percentage(nb_imgs, total_by_category[category]))
    print(json.dumps(new_data, indent=2, ensure_ascii=False, sort_keys=True))
    
    # pie chart
    for category, dir_name in new_data.items():
        labels = list(dir_name.keys())
        sizes = [dir_name[name][1] for name in dir_name]
        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%')
        plt.savefig(f'{category}.png')
    
    # bar chart
    

    #print(json.dumps(new_data, indent=2, ensure_ascii=False, sort_keys=True))
if __name__ == "__main__":
    main()