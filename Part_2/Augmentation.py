import os
import sys
from pathlib import Path
from PIL import Image

def get_new_file_path(augmented_directory, file_path, type) -> str:

    filepath_wo_ext = Path(file_path).with_suffix('')
    filename = filepath_wo_ext.stem
    file_suffix = Path(file_path).suffix
    new_file_path = os.path.join(augmented_directory, f'{filename}_{type}{file_suffix}')

    return new_file_path


def flip_image(augmented_directory, file_path) -> None:

    img = Image.open(file_path)

    flip_img = img.transpose(Image.FLIP_LEFT_RIGHT)

    new_file_path = get_new_file_path(augmented_directory=augmented_directory, file_path=file_path, type='flip')

    flip_img.save(new_file_path)


def main():
    if len(sys.argv) != 2:
        print("Usage: python Augmentation.py <filename>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    if not os.path.isfile(file_path):
        print(f"Error: <{sys.argv[1]}> is not a valid file")
        sys.exit(1)
    
    if not file_path.lower().endswith(('.png', '.jpg', '.jpeg')):
        print("Error: Unsupported file format. Please use a .png, .jpg, or .jpeg image.")
        sys.exit(1)

    current_dir = os.getcwd()
    augmented_directory = os.path.join(current_dir, 'augmented_directory')
    if not os.path.exists(augmented_directory):
        os.makedirs(augmented_directory)

    flip_image(augmented_directory=augmented_directory, file_path=file_path)


if __name__ == "__main__":
    main()
