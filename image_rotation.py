# -*- coding: utf-8 -*-
import cv2
import argparse
import numpy as np

from transformers import imageRotation, polygonRotation, getMask


def parse_args():
    
    parser = argparse.ArgumentParser(description='Image 3D rotation')
    
    parser.add_argument('image', type=str, help='Imput image name.')
    parser.add_argument('out', type=str, help='Output image name.')
   
    parser.add_argument('--theta',
                        type=int,
                        default=0,
                        help='Rotation angle around the x axis.')
    parser.add_argument('--phi',
                        type=int,
                        default=0,
                        help='Rotation angle around the y axis.')
    parser.add_argument('--gamma',
                        type=int,
                        default=0,
                        help='Rotation angle around the z axis.')
    
    parser.add_argument('--mask',
                        type=str,
                        default=None,
                        help='Output mask name.')
    
    parser.add_argument('--labels',
                        type=str,
                        default=None,
                        help='imput labels text name.')
    
    parser.add_argument('--labels-out',
                        type=str,
                        default='image_rotate_labels.txt',
                        help='output labels name.')
    
    parser.add_argument('--image-label',
                        type=str,
                        default=None,
                        help='output labeled image name.')
    
    args = parser.parse_args()
    return args


def main():
    
    args = parse_args()
    dicRotation = {'theta':args.theta, 'phi':args.phi, 'gamma':args.gamma}

    image = cv2.imread(args.image)
    if image is None:
        raise ValueError(f'Can not find : {args.image}')

    image = imageRotation(dicRotation, image)
    cv2.imwrite(args.out, image)
    
    if args.mask is not None:
        mask = getMask()
        cv2.imwrite(args.mask, mask)
        pass
    
    if args.labels is not None:
        with open(args.labels) as f:
            labels = f.readlines()
        poly_rotate_txt = []
        poly_rotate = []
        for polygon in labels:
            polygon = [int(i) for i in polygon.split(',')]
            polygon = polygonRotation(polygon)
            poly_rotate.append(polygon[0])
            poly_rotate_txt.append(', '.join([str(k) for k in polygon[0]]))
        
        np.savetxt(args.labels_out, poly_rotate_txt, delimiter=',', fmt='%s')
        
    if args.image_label is not None:
        for pts in poly_rotate:
            pts = np.array(pts).reshape((-1,1,2))
            image = cv2.polylines(image,[pts],True,(255,0,0),3)
        cv2.imwrite(args.image_label, image)
        
    print('Done')
        
if __name__ == '__main__':
    main()
