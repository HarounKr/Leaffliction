import argparse
import sys
import os

def args_parser() ->  argparse.Namespace:
    parser = argparse.ArgumentParser(description="Image transformation program: applies multiple processing steps (Gaussian blur, mask, ROI, object analysis, pseudolandmarks, color histogram).")
    parser.add_argument("img_path", nargs="?", help="img source path (alternative to -src -dst)", type=str)
    parser.add_argument("-src", help="source path", type=str)
    parser.add_argument("-dst", help="destination path", type=str)
    parser.add_argument("-gaussian", action="store_true")
    parser.add_argument("-mask", action="store_true")
    parser.add_argument("-roi_objects", action="store_true")
    parser.add_argument("-analyze_object", action="store_true")
    parser.add_argument("-pseudolandmarks", action="store_true")


    args = parser.parse_args()
    return args

def gaussian(src, dst):
    print('gaussian')
    print(src, dst)
    return

def mask(src, dst):
    print('mask')

    return

def roi_objects(src, dst):
    print('roi_objects')

    return

def analyze_object(src, dst):
    print('analyze_object')

    return

def pseudolandmarks(src, dst):
    print('pseudolandmarks')
    
    return

if __name__ == '__main__':
    args = args_parser()

    exts = (".jpg", ".jpeg", ".png")
    transform_funcs = {
        'gaussian': lambda src, dst: gaussian(src, dst),
        'mask': lambda src, dst: mask(src, dst),
        'roi_objects': lambda src, dst: roi_objects(src, dst),
        'analyze_object': lambda src, dst: analyze_object(src, dst),
        'pseudolandmarks': lambda src, dst: pseudolandmarks(src, dst),
    }
    display_all = True

    if args.img_path:
        if not args.img_path.lower().endswith(exts):
            print("Error: Unsupported file format. Please use a .png, .jpg, or .jpeg image.")
            sys.exit(1)
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