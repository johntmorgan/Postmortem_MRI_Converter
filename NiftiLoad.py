# This prepares .nii data to be processed by PostmortemMRIConvert. 
# It requires the NumPy and NiBabel libraries.
# Please refer to the main PostmortemMRIConvert.py file for full setup and 
# usage instructions.


import marshal
import nibabel as nib
import numpy as np

directory = r"C:/NiftiSubjects/MIND Cases/JohnTest/"
file_in = "UMB-4226_L_01.nii"

# Add a temp_file name if you *don't* want to use the input name plus 
# "-tmpdata" and "-tmpaffine".
# You will need to edit the save and processing files as well.
raw_data_suffix = "-tmprawdata"
proc_data_suffix = "-tmpprocdata"
affine_suffix = "-tmpaffine"
zoom_suffix = "-tmpzoom"

def load_file(directory, file_in):
    path = directory + file_in
    img = nib.load(path)
    img_header = img.get_header()
    return img.get_data(), img.get_affine(), img_header.get_zooms()


def raw_name(file_in):
    file_cutoff = file_in.find(".")
    raw_name = file_in[:file_cutoff]
    return raw_name


def make_copy(img_data):
    """
    This is the equivalent of the copy.deepcopy function for the MRI images, 
    but much faster because it's tailored to this data type. Using deepcopy 
    instead costs an extra ~5 seconds/copy on my machine with a data set 
    this large.
    """
    img_out = ([[[int(e) for e in sag_row] for sag_row in ax_row] 
                for ax_row in img_data])
    return img_out


print "Reading files."
img_data, img_affine, img_zoom = load_file(directory, file_in)
raw_name = raw_name(file_in)

print "Converting arrays and tuples to lists."
img_data = img_data.tolist()
img_affine = img_affine.tolist()
img_zoom = np.array(img_zoom)
img_zoom = img_zoom.tolist()

if not isinstance(img_data[0][0], int):
    # necessary to avoid memory errors when making lists, which are common if 
    # 32-bit floats or above are used for storage.
    print "Converting to int storage."
    img_data = make_copy(img_data)
                
print "Storing data using marshal format."
datafile = open((directory + raw_name + raw_data_suffix), 'w+b')
marshal.dump(img_data, datafile)

procdatafile = open((directory + raw_name + proc_data_suffix), 'w+b')
marshal.dump(img_data, procdatafile)

affinefile = open((directory + raw_name + affine_suffix), 'w+b')
marshal.dump(img_affine, affinefile)

zoomfile = open((directory + raw_name + zoom_suffix), 'w+b')
marshal.dump(img_zoom, zoomfile)

print "Done."