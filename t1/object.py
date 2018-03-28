#!/usr/bin/python3.5

import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.misc import imshow, imread, imsave
import os
import sys
import optparse

def edges(image, save, dest_dir, name):

    #Canny filter returns binary image with object perimeter in black
    edges = cv2.Canny(image, 9000, 12000, apertureSize = 5)

    #Initializes output image with zeros
    edges_rgb = np.zeros(shape=(edges.shape[0], edges.shape[1], 3))

    #Makes object perimeter red and remaining image white.
    for i in range(edges.shape[0]):
        for j in range(edges.shape[1]):
            if edges[i][j] == 0:
                edges_rgb[i][j][:] = [255, 255, 255]
            else:
                edges_rgb[i][j][0] = 255


    if save:
        imsave(os.path.join(dest_dir, name+"_edge.png"), edges_rgb)
    else:
        imshow(edges_rgb)

    return edges

def obj_properties(image, save, dest_dir, name):
    area_list = []
    height = image.shape[0]
    width = image.shape[1]

    #If user chooses to pass another three channel image, cvtColor will distort it.
    #Verifies image is either RGB or monocromatic
    if image.shape.__len__() == 3 and image.shape[2] == 3:
        gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    elif image.shape.__len__() == 2:
        gray = image
    else:
        print("Image colorspace has to be either RGB or monocromatic")
        exit(1)

    #Threshold image to binary values then find contours.
    #Canny image makes opencv find two contours for each object.
    thresh, bin_img = cv2.threshold(gray, thresh=250, maxval=255, type=cv2.THRESH_BINARY)
    _, contours, _ = cv2.findContours(bin_img, 1, 2)


    #Define text properties
    font = cv2.FONT_HERSHEY_COMPLEX
    font_color = (0,0,0)
    thickness = 1
    font_scale = 0
    bottomLeftCornerOfText = (0, 0)

    #Ignore any boundary contours. Here we consider no object lies in the boundary of image frame.
    contour_final = []
    for i, cnt in enumerate(contours):
        rect = cv2.boundingRect(cnt)
        if rect[0] > 0 and rect[1] > 0 and rect[1] < width and rect[3] < height:
            contour_final.append(cnt)

    #Process output image
    out_img = np.zeros((height, width, 3), dtype=np.uint8)
    for i in range(height):
        for j in range(width):
            if bin_img[i][j] == 0:
                out_img[i][j][:] = [255, 50, 50]
            else:
                out_img[i][j][:] = [255, 255, 255]


    #Iterate over every contour printing it's region number, perimeter and area.
    print("número de regiões: {}".format(contour_final.__len__()))
    for i, cnt in enumerate(contour_final):

        #Find centroid of contour
        M = cv2.moments(cnt)
        cx = M['m10']/M['m00']
        cy = M['m01']/M['m00']

        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, closed=True)
        area_list.append(int(area))

        #Change fontscale according to contour area
        if area >= 1500: font_scale = 0.7
        else: font_scale = 0.4

        text_size, _ = cv2.getTextSize(str(i), font, font_scale, thickness)

        tx = text_size[0]/2
        ty = text_size[1]/2

        bottomLeftCornerOfText = (int(cx-tx), int(cy+ty))

        #Write region number in the center of contour
        cv2.putText(out_img, str(i), bottomLeftCornerOfText, font, font_scale, font_color, thickness)

        print("região:{:>3}   perímetro:{:>4}    área:{:>5}".format(i, int(perimeter), int(area)))

    if save:
        imsave(os.path.join(dest_dir, name+"_objp.png"), out_img)
    else:
        imshow(out_img)

    return out_img, area_list

def histogram(area_list, save, dest_dir, name):

    #Defines bins according to specified intervals:
    # small = [0, 1500)
    # medium = [1500, 3000)
    # maximum = [3000, area_list.max()]
    max_area = np.max(area_list)
    if max_area < 1500:
        bins = [0, 1500]
    elif max_area < 3000:
        bins = [0, 1500, 3000]
    else:
        bins = [0, 1500, 3000, max_area]

    #Plots histogram
    plt.hist(area_list, bins=bins, color="r", rwidth=0.5)
    print(bins)
    print(np.diff(bins))
    print(bins[:-1])
    plt.xlabel("Área")
    plt.ylabel("Número de Objetos")
    plt.title("Histograma de Área dos Objetos")

    if save:
        plt.savefig(os.path.join(dest_dir, name+"_hist"))
    else:
        plt.show()
    plt.close()

    return

def main(filenames, save=False, dest_dir="out"):

    for fn in filenames:
        if not os.path.isfile(fn):
            print("Image {} doesn't exist.".format(fn))
            exit(1)
        if fn.split('.')[-1] != "png":
            print("Invalid image file: {}. Image must be in PNG format.".format(fn))
            exit(1)
    #Creates directory to save image files
    if save:
        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)

    for fn in filenames:
        name = fn.split('/')[-1].split('.')[-2]
        img = imread(fn)
        edges(img, save, dest_dir, name)
        _, area_list = obj_properties(img, save, dest_dir, name)
        histogram(area_list, save, dest_dir, name)




if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option("-s", "--save",
                    action="store_true", dest="save",
                    help="Save all generated images into DEST_DIR directory. By default this is ./out")

    parser.add_option("-d", "--dest_dir",
                        action="store", type="string", dest="dest_dir",
                        help="Directory to place image files. If save is False, this option is ignored.",
                        default="out")

    options, args = parser.parse_args()

    for fn in args:
        if fn.split('.')[-1] != "png":
            print("Image file argument must be in PNG format.")
            exit(1)
            
    main(args, options.save, options.dest_dir)
