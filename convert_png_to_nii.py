import glob, os, sys
import imageio
import numpy as np
import nibabel as nib
import natsort

def convert(path_to_png_dir, outPath):
    # get all files in directory in sorted format
    files = natsort.natsorted(glob.glob(path_to_png_dir + "/*.png"))

    # initialize new numpy array
    # get shape of first png file
    first = True
    for im_path in files:
         print(im_path)
         im = imageio.imread(im_path)
         if first:
             print(im.shape)
             print(type(im))
             first = False
             volume = np.zeros((im.shape))
         else:
             volume = np.dstack((volume, np.array(im)))

    nii_img = nib.Nifti1Image(volume, np.eye(4))
    nii_img.get_data_dtype() == np.dtype(np.int16)
    nii_img.header.get_xyzt_units()
    nib.save(nii_img, os.path.join(outPath,'all.nii.gz'))


# Process inputs
# Requires input file path,
# Optional output path
args = sys.argv[1:]
if len(args) < 2:
    print("Expects at least 1 argument: input file path and (optional) output directory, \n EXAMPLE: python convert_png_to_nii.py . ./output ")
inPath = args[0]
outPath = args[1]
convert(inPath, outPath)