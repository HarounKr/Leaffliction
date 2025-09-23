import argparse
import sys
import os
import cv2
import glob
import numpy as np


def args_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Img transformation program")
    parser.add_argument("img_path", nargs="?",
                        help="img source path (alternative to -src -dst)",
                        type=str)
    parser.add_argument("-src", help="source path", type=str)
    parser.add_argument("-dst", help="destination path", type=str)
    parser.add_argument("-gaussian", action="store_true")
    parser.add_argument("-mask", action="store_true")
    parser.add_argument("-roi_objects", action="store_true")
    parser.add_argument("-analyze_object", action="store_true")
    parser.add_argument("-pseudolandmarks", action="store_true")
    args = parser.parse_args()
    return args


# done - Gaussian blur
def gaussian(src, dst, is_file=False):
    # Création du dossier de sortie s'il n'existe pas
    os.makedirs(dst, exist_ok=True)

    # Récupère les fichiers images
    image_files = []
    for ext in ("*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"):
        image_files.extend(glob.glob(os.path.join(src, ext)))
    if is_file:
        image_files = [src]
    for img_file in image_files:
        # Lecture de l'image
        img = cv2.imread(img_file)
        if img is None:
            print(f"Erreur: impossible de lire l'image {img_file}")
            continue

        # Application du flou gaussien sur l'image noir et blanc
        blurred_img = cv2.GaussianBlur(img, (5, 5), 1)

        # Sauvegarde
        base, ext = os.path.splitext(os.path.basename(img_file))
        output_path = os.path.join(dst, f"{base}_gaussian{ext}")
        cv2.imwrite(output_path, blurred_img)

    return


# done - Mask
def mask(src, dst, is_file=False):
    os.makedirs(dst, exist_ok=True)

    image_files = []
    for ext in ("*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"):
        image_files.extend(glob.glob(os.path.join(src, ext)))
    if is_file:
        image_files = [src]
    for img_file in image_files:
        img = cv2.imread(img_file)
        if img is None:
            print(f"Erreur: impossible de lire l'image {img_file}")
            continue
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green = (30, 40, 40)
        upper_green = (80, 255, 255)
        mask = cv2.inRange(hsv, lower_green, upper_green)
        mask_inv = cv2.bitwise_not(mask)
        feuille = cv2.bitwise_and(img, img, mask=mask)
        blanc = np.full_like(img, 255)
        fond = cv2.bitwise_and(blanc, blanc, mask=mask_inv)
        result = cv2.add(feuille, fond)
        base, ext = os.path.splitext(os.path.basename(img_file))
        output_path = os.path.join(dst, f"{base}_mask{ext}")
        cv2.imwrite(output_path, result)
    return


# done - ROI objects
def roi_objects(src, dst, is_file=False):
    os.makedirs(dst, exist_ok=True)

    image_files = []
    for ext in ("*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"):
        image_files.extend(glob.glob(os.path.join(src, ext)))
    if is_file:
        image_files = [src]
    for img_file in image_files:
        img = cv2.imread(img_file)
        if img is None:
            print(f"Erreur: impossible de lire l'image {img_file}")
            continue
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green = (30, 40, 40)
        upper_green = (80, 255, 255)
        mask = cv2.inRange(hsv, lower_green, upper_green)
        try:
            obj, obj_hierarchy = cv2.findContours(mask,
                                                  cv2.RETR_EXTERNAL,
                                                  cv2.CHAIN_APPROX_SIMPLE)
        except Exception as e:
            print(f"Erreur lors de la détection d'objets: {e}")
            obj = []
        if obj is not None and len(obj) > 0:
            filtered_obj = [contour for contour in obj if
                            cv2.contourArea(contour) > 100]
            if len(filtered_obj) > 0:
                largest_contour = max(filtered_obj, key=cv2.contourArea)
                roi_img = img.copy()
                x, y, w, h = cv2.boundingRect(largest_contour)
                cv2.rectangle(roi_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                roi_img = img.copy()
        else:
            roi_img = img.copy()
        base, ext = os.path.splitext(os.path.basename(img_file))
        output_path = os.path.join(dst, f"{base}_roi_objects{ext}")
        cv2.imwrite(output_path, roi_img)
    return


# done - Analyze object
def analyze_object(src, dst, is_file=False):
    os.makedirs(dst, exist_ok=True)

    # Récupère les fichiers images
    image_files = []
    for ext in ("*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"):
        image_files.extend(glob.glob(os.path.join(src, ext)))
    if is_file:
        image_files = [src]

    for img_file in image_files:
        img = cv2.imread(img_file)
        if img is None:
            print(f"Erreur: impossible de lire l'image {img_file}")
            continue
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_green = (30, 40, 40)
        upper_green = (80, 255, 255)
        mask = cv2.inRange(hsv, lower_green, upper_green)
        contours, hierarchy = cv2.findContours(mask,
                                               cv2.RETR_EXTERNAL,
                                               cv2.CHAIN_APPROX_SIMPLE)
        analyzed_img = img.copy()
        if contours:
            largest_contour = max(contours, key=cv2.contourArea)
            cv2.drawContours(analyzed_img,
                             [largest_contour],
                             -1, (0, 255, 0), 2)
            M = cv2.moments(largest_contour)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                cv2.circle(analyzed_img, (cx, cy), 8, (255, 0, 0), -1)
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            lower_sick = (10, 40, 50)
            upper_sick = (35, 200, 255)
            mask_sick = cv2.inRange(hsv, lower_sick, upper_sick)
            sick_contours, _ = cv2.findContours(mask_sick,
                                                cv2.RETR_EXTERNAL,
                                                cv2.CHAIN_APPROX_SIMPLE)
            if sick_contours:
                significant_sick = [c for c in sick_contours if
                                    cv2.contourArea(c) > 100]
                cv2.drawContours(analyzed_img,
                                 significant_sick,
                                 -1, (0, 0, 255), 2)
        else:
            print(f"Aucun objet détecté dans {img_file}")
        base, ext = os.path.splitext(os.path.basename(img_file))
        output_path = os.path.join(dst, f"{base}_analyze_object{ext}")
        cv2.imwrite(output_path, analyzed_img)
    return


# done - Pseudolandmarks
def pseudolandmarks(src, dst, is_file=False):
    os.makedirs(dst, exist_ok=True)

    # Récupère les fichiers images
    image_files = []
    for ext in ("*.jpg", "*.png", "*.jpeg", "*.JPG", "*.PNG", "*.JPEG"):
        image_files.extend(glob.glob(os.path.join(src, ext)))
    if is_file:
        image_files = [src]
    for img_file in image_files:
        # Lecture de l'image
        img = cv2.imread(img_file)
        if img is None:
            print(f"Erreur: impossible de lire l'image {img_file}")
            continue
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_healthy = (40, 80, 80)
        upper_healthy = (70, 255, 255)
        mask_healthy = cv2.inRange(hsv, lower_healthy, upper_healthy)
        lower_medium = (30, 40, 40)
        upper_medium = (80, 120, 200)
        mask_medium = cv2.inRange(hsv, lower_medium, upper_medium)
        lower_poor = (10, 40, 50)
        upper_poor = (33, 200, 255)
        mask_poor = cv2.inRange(hsv, lower_poor, upper_poor)
        out_img = img.copy()
        zones = [
            ("Bonne santé", mask_healthy, (255, 0, 0)),
            ("Santé moyenne", mask_medium, (128, 0, 128)),
            ("Mauvaise santé", mask_poor, (0, 0, 255))
        ]
        total_pixels = 0
        zone_stats = []
        for zone_name, mask, color in zones:
            contours, _ = cv2.findContours(mask,
                                           cv2.RETR_EXTERNAL,
                                           cv2.CHAIN_APPROX_SIMPLE)
            zone_area = 0
            landmarks_count = 0
            if contours:
                significant_contours = [c for c in contours if
                                        cv2.contourArea(c) > 50]
                for contour in significant_contours:
                    area = cv2.contourArea(contour)
                    zone_area += area
                    if area > 50:
                        M = cv2.moments(contour)
                        if M["m00"] != 0:
                            cx = int(M["m10"] / M["m00"])
                            cy = int(M["m01"] / M["m00"])
                            cv2.circle(out_img, (cx, cy), 5, color, -1)
                            landmarks_count += 1
                        contour_length = len(contour)
                        if contour_length > 10:
                            if area > 1000:
                                num_points = 12
                            elif area > 500:
                                num_points = 8
                            else:
                                num_points = 4
                            for i in range(num_points):
                                idx = int(i * contour_length / num_points)
                                if idx < contour_length:
                                    point = tuple(contour[idx][0])
                                    cv2.circle(out_img, point, 3, color, -1)
                                    landmarks_count += 1
                        if area > 200:
                            leftmost = tuple(contour[contour[:, :,
                                                             0].argmin()][0])
                            rightmost = tuple(contour[contour[:, :,
                                                              0].argmax()][0])
                            topmost = tuple(contour[contour[:, :,
                                                            1].argmin()][0])
                            bottommost = tuple(contour[contour[:, :,
                                                               1].argmax()][0])
                            cv2.circle(out_img, leftmost, 4, color, -1)
                            cv2.circle(out_img, rightmost, 4, color, -1)
                            cv2.circle(out_img, topmost, 4, color, -1)
                            cv2.circle(out_img, bottommost, 4, color, -1)
                            landmarks_count += 4
            total_pixels += zone_area
            zone_stats.append((zone_name, zone_area, landmarks_count))
        base, ext = os.path.splitext(os.path.basename(img_file))
        output_path = os.path.join(dst, f"{base}_pseudolandmarks{ext}")
        cv2.imwrite(output_path, out_img)
    return


if __name__ == '__main__':
    args = args_parser()

    exts = (".jpg", ".jpeg", ".png")
    transform_funcs = {
        'gaussian': lambda src, dst,
        is_file: gaussian(src, dst, is_file),
        'mask': lambda src, dst,
        is_file: mask(src, dst, is_file),
        'roi_objects': lambda src, dst,
        is_file: roi_objects(src, dst, is_file),
        'analyze_object': lambda src, dst,
        is_file: analyze_object(src, dst, is_file),
        'pseudolandmarks': lambda src, dst,
        is_file: pseudolandmarks(src, dst, is_file),
    }
    display_all = True

    if args.img_path:
        if not args.img_path.lower().endswith(exts):
            print("Error: Unsupported file format.")
            sys.exit(1)
        else:
            image_path = os.path.abspath(args.img_path)
            dst = os.path.dirname(os.path.abspath(__file__))
            for key in transform_funcs:
                transform_funcs[key](src=image_path, dst=dst, is_file=True)
    else:
        args_dict = vars(args)
        transformations = list(transform_funcs)
        if args.src and args.dst:
            if not os.path.isdir(args.src) or not os.path.isdir(args.dst):
                print("Error: invalid path.")
                sys.exit(1)
            for argv in args_dict:
                if argv in transform_funcs:
                    if args_dict[argv]:
                        display_all = False
                        transform_funcs[argv](src=args.src, dst=args.dst)
            if display_all:
                for func in transform_funcs:
                    transform_funcs[func](src=args.src, dst=args.dst)
        else:
            if not args.src:
                print("Error: missing -src option")
            else:
                print("Error: missing -dst option")
            sys.exit(1)
