from scipy.misc import imread, imshow, imsave
import matplotlib.pyplot as plt
from tensorflow.python.platform import gfile
import numpy as np

import sys
import os

image_dir = "./data"
file_type = "png"
save_dir = "./out"
save = False

def histogram(image, save, name):
    """Prints histogram of raw pixel values.

    @param: image numpy array representing image (2D for grayscale and 3D for RGB)."""

    bins = [x for x in range(256)]

    plt.hist(image.flatten(), bins=bins, color="g")
    plt.xlabel("Níveis de Cinza")
    plt.ylabel("Frequência")

    if save:
        plt.savefig(os.path.join(save_dir, name+"_hist"))
    else:
        plt.show()
    plt.close()


def stats(image):
    """Prints image stats: height, width, max intensity, min intensity and mean intensity.

    @param: image numpy array representing image (2D for grayscale and 3D for RGB)."""

    height = image.shape[0]
    width = image.shape[1]
    min_int = np.min(image)
    max_int = np.max(image)
    mean_int = np.mean(image)

    print ("Propriedades:\n"
            "  largura: {}\n"
            "  altura: {}\n"
            "  intensidade mínima: {}\n"
            "  intensidade máxima: {}\n"
            "  intensidade média: {:.2f}\n"
            .format(width, height, min_int, max_int, mean_int))

def invert(image, save, name):
    """Inverts pixel intensities according to function abs(x-255).

    @param: image numpy array representing image (2D for grayscale and 3D for RGB)."""

    inv_img = np.abs(image.astype(np.int32)-255)
    if save:
        imsave(os.path.join(save_dir, name+"_inv.png"), inv_img)
    else:
        imshow(inv_img)

    return inv_img

def normalize(image, min_int, max_int, save, name):
    """Rescales image pixel values to range [min, max], assuming its an 8-bit depth image.

    @param: image numpy array representing image (2D for grayscale and 3D for RGB)."""

    norm_img = (image*((max_int-min_int)/255)+min_int).astype(np.uint8)

    if save:
        imsave(os.path.join(save_dir, name+"_norm.png"), norm_img)
    else:
        imshow(norm_img)

    return norm_img

def main(image_dir=image_dir, file_type=file_type, save=save):
    """Shows image data and transformations for every image specified including:
    histogram: graph of pixel value frequencies (pyplot)
    stats: image statistics such as height, width, mean pixel value, etc...
    invert: inverts pixel values using equation abs(x-255)
    rescale: rescales pixel values to range [120, 180]

    Warning: if image_dir is a directory, the function only supports the file_type specified.
    If image_dir is a filename, any valid image file type will work. By default the function
    only supports .png images, displays images and looks for data in directory "./data/".

    @param: image_dir directory or filename with images to be processed.
    @param: file_type if image_dir is a directory, only file_type images within image_dir will be processed.
    @param: save if True saves images to default save_dir "./out", else plots images and graphs"""

    if (os.path.isdir(image_dir)):
        path = os.path.join(image_dir, "*."+file_type)
        image_filenames = gfile.Glob(path)
    elif os.path.isfile(image_dir):
        image_filenames = [image_dir]
    else:
        raise ValueError("Image_dir specified isn't a file nor a directory.")

    if save == "True":
        save = True
    if save == "False":
        save = False

    if not isinstance(save, bool):
        raise ValueError("Save argument must be a python Boolean (True or False).")

    if save:
        if not os.path.isdir(save_dir):
            os.mkdir(save_dir)

    if not image_filenames:
        raise ValueError("Specified filename or directory doesn't match any images!")
    for img in image_filenames:
        print("Para a imagem '{}' temos:".format(img))
        name = img.split('/')[-1].split('.')[-2]
        img_array = imread(img)
        # stats(img_array)
        histogram(img_array, save, name)
        # invert(img_array, save, name)
        # normalize(img_array, 120, 180, save, name)

if __name__ == "__main__":
    #User can optionally specify arguments through command line:
    # python basic.py [image_dir,[file_type, [save]]]
    try:
        if len(sys.argv) == 1:
            main()
        elif len(sys.argv) == 2:
            main(sys.argv[1])
        elif len(sys.argv) == 3:
            if (os.path.isfile(sys.argv[1])):
                main(sys.argv[1], None, sys.argv[2])
            else:
                main(sys.argv[1], sys.argv[2])
        elif len(sys.argv) == 4:
            main(sys.argv[1], sys.argv[2], sys.argv[3])
        else:
            raise ValueError("Too many arguments passed. Refer to main documentation for details.")
    except Exception as e:
        print(e)
