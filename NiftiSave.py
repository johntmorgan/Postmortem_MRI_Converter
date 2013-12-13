# This saves data processed by PostmortemMRIConvert back to the .nii format 
# for viewing or entry into the Freesurfer pipeline.
# Please do *not* save "file out" to the same name as file in, or you will
# overwrite the original file.
 
# This program requires the NumPy and NiBabel libraries.
# Please refer to the main PostmortemMRIConvert.py file for full setup and 
# usage instructions.

directory = r"C:/NiftiSubjects/MIND Cases/JohnTest/"
file_in = "UMB-4226_L_01.nii"
file_out = "UMB-4226_L_01-convertertest.nii"

##############################################################################

# add a temp_file name if you *don't* want to use the input name plus 
# "-tmpdata" and "-tmpaffine"
# you will need to edit the save and processing files as well
proc_data_suffix = "-tmpprocdata"
affine_suffix= "-tmpaffine"
zoom_suffix = "-tmpzoom"


import marshal
import nibabel as nib
import numpy as np


def save_file(directory, file_out, img_data, img_affine):
    save_image = nib.Nifti1Image(img_data, img_affine)
    path = directory + file_out
    nib.save(save_image, path)


def raw_name(file_in):
    file_cutoff = file_in.find(".")
    raw_name = file_in[:file_cutoff]
    return raw_name


raw_in = raw_name(file_in)
raw_out= raw_name(file_out)

print "Loading raw data."
datafile = open((directory + raw_in + proc_data_suffix), 'rb')
affinefile = open((directory + raw_in + affine_suffix), 'rb')

img_data = marshal.load(datafile)
img_affine = marshal.load(affinefile)

print "Converting lists into arrays."
img_data = np.array(img_data)
img_affine = np.array(img_affine)

print "Saving " + file_out + "."
save_file(directory, file_out, img_data, img_affine)

print "Done."

# save mask data if you are testing the mask settings
#print "Saving mask data."
#maskfile = open((directory + raw_in + "-imgmask"), 'rb')
#img_mask = marshal.load(maskfile)
#img_mask = np.array(img_mask)
#mask_name = raw_out + "-mask.nii"
#save_file(directory, mask_name, img_mask, img_affine)

