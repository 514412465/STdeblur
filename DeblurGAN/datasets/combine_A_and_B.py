from pdb import set_trace as st
import os
import numpy as np
import cv2
import argparse
import re

def sorted_nicely( l ):
    convert = lambda text: int(text) if text.isdigit() else text
    alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
    return sorted(l, key = alphanum_key)

parser = argparse.ArgumentParser('create image pairs')
parser.add_argument('--fold_A', dest='fold_A', help='input directory for image A', type=str, default='../dataset/50kshoes_edges')
parser.add_argument('--fold_B', dest='fold_B', help='input directory for image B', type=str, default='../dataset/50kshoes_jpg')
parser.add_argument('--fold_AB', dest='fold_AB', help='output directory', type=str, default='../dataset/test_AB')
parser.add_argument('--num_imgs', dest='num_imgs', help='number of images',type=int, default=1000000)
parser.add_argument('--use_AB', dest='use_AB', help='if true: (0001_A, 0001_B) to (0001_AB)',action='store_true')
args = parser.parse_args()

for arg in vars(args):
    print('[%s] = ' % arg,  getattr(args, arg))

splits = os.listdir(args.fold_A)

for sp in splits:
    img_fold_A = os.path.join(args.fold_A, sp)
    img_fold_B = os.path.join(args.fold_B, sp)
    img_list = sorted_nicely(os.listdir(img_fold_A))
    print(img_list)
    if args.use_AB: 
        img_list = [img_path for img_path in img_list if '_A.' in img_path]

    num_imgs = min(args.num_imgs, len(img_list))
    print('split = %s, use %d/%d images' % (sp, num_imgs, len(img_list)))
    img_fold_AB = os.path.join(args.fold_AB, sp)
    if not os.path.isdir(img_fold_AB):
        os.makedirs(img_fold_AB)
    print('split = %s, number of images = %d' % (sp, num_imgs))
    for n in range(2, num_imgs-3):
        name_A = img_list[n]
        path_A = os.path.join(img_fold_A, name_A)
        if args.use_AB:
            name_B = name_A.replace('_A.', '_B.')
        else:
            name_B = name_A
        path_B = os.path.join(img_fold_B, name_B)
        if os.path.isfile(path_A) and os.path.isfile(path_B):
            name_AB = img_list[n]
            if args.use_AB:
                name_AB = name_AB.replace('_A.', '.') # remove _A
            path_AB = os.path.join(img_fold_AB, name_AB)
            path_AB = path_AB[:-4]+".npy"
            print path_AB
            im_A1 = cv2.imread(path_A, 0)
            im_A_1 = cv2.imread(os.path.join(img_fold_A, img_list[n-1]),0);
            im_A_2 = cv2.imread(os.path.join(img_fold_A, img_list[n-2]),0);
            im_A2 = cv2.imread(os.path.join(img_fold_A, img_list[n+1]),0);
            im_A3 = cv2.imread(os.path.join(img_fold_A, img_list[n+2]),0);
            im_B = cv2.imread(path_B, 0)
            im_Apack = np.dstack([im_A_2, im_A_1, im_A1, im_A2, im_A3]);
            im_Bpack = np.dstack([im_B, im_B, im_B, im_B, im_B])
            print im_Apack.shape, im_Bpack.shape
            im_AB = np.concatenate([im_Apack, im_Bpack])
            #cv2.imwrite(path_AB, im_AB)
            np.save(path_AB, im_AB)
