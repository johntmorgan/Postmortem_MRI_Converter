# This is the main program for processing of postmortem brain scans. 
# It has no external library dependencies, allowing it to be run under the 
# PyPy interpreter, which produces a >100x performance increase, decreasing
# run times from hours to a few minutes. NiBabel (and by extension Numpy) 
# library dependencies are offloaded into NiftiLoad.py and NiftiSave.py.
 
# As a tradeoff, you must run NiftiLoad.py before using this script to 
# generate temp files that the script will operate on, and NiftiSave.py after 
# running this script to convert back into .nii.

# Note that temp files (-tmp) are generated but not deleted during this 
# process. This allows the user to test variable settings without needing
# to reload each time. However, you will need to delete the -tmp files 
# manually when you are satisfied with the output.

##############################################################################
# Setting up your computer to run this program

# This program is written in Python 2.7. Please ensure that all installed 
# libraries are up to date but not using Python 3+!

# Step 1: Install Python 2.7.3 from here: 
# http://www.python.org/download/releases/2.7.3/
# On the page, select the Windows MSI installer (x86 if you have 32-bit 
# Windows installed, x86-64 if you have 64-bit Windows installed.)
# I suggest using the default option, which will install Python to c:/Python27

# Step 2: Install PyPy from here: http://pypy.org/download.html

# Step 3: Install NumPy to your python directory from here: 
# http://sourceforge.net/projects/numpy/files/NumPy/

# Step 4: Install NiBabel to your python directory from here:
# http://nipy.org/nibabel/

# Step 5: Copy the programs in this folder into the c:/Python27 directory
# You can also put them into another directory that is added to the Python & 
# PyPy PATHs.

##############################################################################
# Steps to process a scan

# Pre-run: If possible, load the image and strip it using a program like FSL. 
# This is likely to greatly improve results. *If the brain was embedded in 
# gelatin, this program will handle it very poorly unless the gelatin has 
# already been removed somehow!* 

# Step 1: Load the .nii file and convert it into a format that PyPy can handle
# using NiftiLoad.py. From the command line, enter the directory where the 
# programs are stored and type "python NiftiLoad.py" and hit enter.

# Step 2 (optional): Run NiftiMirror if only a single hemisphere was scanned.
# You will probably need to run NiftiMirror and then save and check the file
# several times until you find settings that produce a good mirror. From the 
# command line, enter the directory where the programs are stored and type 
# "python NiftiMirror.py" and hit enter.

# Step 3: Set variables below.

# Step 4: Run this program from the command line by entering the directory 
# where this file is saved and typing "pypy PostmortemMRIConvert.py"

# Step 5: Save the .nii file to a new filename using NiftiSave.py. From the 
# command line, enter the directory where the programs are stored and type 
# "python NiftiSave.py" and hit enter.

##############################################################################
# Variables for user control.
# Each of the following steps is laid out in the order they are executed by 
# the program. 

# Input the directory of file storage and the name of the input file.
directory = r"C:/NiftiSubjects/MIND Cases/JohnTest/"
file_in = "UMB-4226_L_01.nii"
 
# If you're running a case that was not scanned using standard M.I.N.D. 
# Institute parameters, set this to True, and set the white matter and gray 
# matter cutoff values via manual inspection of the case.
adjust_intensity = False
wm_max_start = 1700
wm_min_start = 500
gm_max_start = 3000
gm_min_start = 1700

# This setting attempts to detect background pixels near the surface of the 
# brain with values above zero that have not been removed by pre-processing. 
clean_up_background = True

# This setting normalizes data with inconsistent scan brightness within a 
# scan.
normalize_slices = True 

# This setting normalizes the image intensity to a standard value across 
# images of differing brightness. If set to false, you will need to play with 
# your gray and white matter cutoffs below to get good results
normalize_image = True

# Tell the program whether to invert the slice values around a threshold 
# (wm_max, see below). This is the main step that inverts gray and white 
# intensities.
intensity_correct = True

# This setting removes the bright "rind" artifact produced by inverting 
# dim voxels (half brain/half background) on the surface of the brain. 
remove_wm_rind = True

# Force pixels into a binary gray/white mask? This is to produce better 
# freesurfer output if Freesurfer is still having a problem with gray/white
# boundaries. Everything that's above wm_min gets one value, and everything 
# below it gets another.
convert_to_mask = False

# If making a mask, we need to a series of blurs and sharpens to remove 
# occasional misidentified, isolated pixels? How many times should this be 
# performed? More than two repetitions is recommended.
# This variable has no effect if convert_to_mask is False.
cleanup_reps = 5

# Freesurfer likes bright images. How much should the image be brightened vs. 
# background, as a percent? This variable has no effect if convert_to_mask
# is True.
brighten_image = True
bright_pct = .20


##############################################################################
# Preset variables. 
# It is strongly suggested that these variables not be altered unless you 
# know exactly what you are doing!

# Set your target intensity values manually here.
wm_max = 1700
wm_min = 300
gm_max = 3000
gm_min = 1700
background = 0

# Normalization intensity, generally best to put ~5% above wm_max/gm_min 
# cutoff
norm_intens = 1785

# The intensity we will set our mask at. Don't overlap this with voxel values!
mask_set = 10000

# How far away should I check for isolation? If a pixel below the minimum wm 
# threshhold encounters nothing but space in both directions in all 3 
# dimensions, it will be deleted.
# This step is performed because otherwise lots of background becomes bright 
# during normalization.
search_dist = 5

# How many pixels need to be seen, total, in all 3 axes, with a blur of one 
# pixel from the search destination, for the pixel to be included? 
inclusion_req = 3

# How many slices away in a rostral-caudal axis should sections be averaged?
# If you see an occasional section that sticks out in intensity, try 
# increasing this distance.
slice_list = (0, 1, 3)

# Normalization point used to compare slices
norm_intens_pt = 200 

# How thick is the typical rind, in mm?
rind_thickness = 0.7

# How far beyond the rind should we look for open space, in mm?
# Note that exploration distance is thickness + exploration divided by pixel 
# size in each dimension, then rounded *down* (because that is how Python 2 
# handles integers.
rind_explore = 1.3

# How many bg voxels need to be found in this space for it to count as a 
# border cell?
rind_cutoff = 4

# How far from cortical surfacet to place protective mask, in mm?
mask_dist = 2.0

# Blur settings: this is how far away voxels draw information from while 
# fixing the rind, in mm
blur_range = 2.5

# the first file is unchanged, so you can try multiple processing approaches
# without reloading from the raw file.
raw_data_suffix = "-tmprawdata"
proc_data_suffix = "-tmpprocdata"
zoom_suffix = "-tmpzoom"

##############################################################################
# Program begins here
# Note: I'm using marshal instead of the more standard pickle to move files 
# around because pickle appears to be incompatible with the current release of 
# PyPy.
import time
import marshal


def raw_name(file_in):
    """
    Takes an input filename and cuts off the extension so that there is a 
    string that can be used for various input and output files.
    """
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


def remove_boundaries(img_data, pct_border, background):
    """
    Removes artifacts around the border of the image that are very common
    with postmortem MRI images. If a final data set is being run, it might be 
    preferable to manually delete these artifacts in each picture, and skip
    this step. 
    """
    for ax_ind, ax_row in enumerate(img_data):
        for sag_ind, sag_row in enumerate(ax_row):
            for cor_ind, voxel in enumerate(sag_row):
                if (ax_ind < pct_border * len(img_data) or ax_ind > 
                    (len(img_data) - pct_border * len(img_data))):
                    sag_row[cor_ind] = background
                if (sag_ind < pct_border * len(img_data) or sag_ind > 
                    (len(img_data) - pct_border * len(img_data))):
                    sag_row[cor_ind] = background
        print ("border_strip row " + str(ax_ind) + " done" + " time: " + 
               str(time.clock()))
    return img_data


def adjust_intens(img_data, wm_max_start, wm_min_start, gm_max_start, 
                  gm_min_start, wm_max, wm_min, gm_max, gm_min):
    for ax_row in img_data:
        for sag_row in ax_row:
            for cor_ind, voxel in enumerate(sag_row):
                if wm_max_start >= voxel > wm_min_start:
                    sag_row[cor_ind] = wm_min + ((wm_max - wm_min) * 
                                                 ((voxel - wm_min_start) / 
                                                  float(wm_max_start - 
                                                        wm_min_start)))
                elif gm_max_start > voxel > gm_min_start:
                    sag_row[cor_ind] = gm_min + ((gm_max - gm_min) * 
                                                 ((voxel - gm_min_start) / 
                                                  float(gm_max_start - 
                                                        gm_min_start)))
    return img_data


def isolation_check(search_dist, inclusion_req, ax_ind, sag_ind, 
                    cor_ind, wm_min):
    """
    This function examines pixels to determine whether they are isolated 
    noise. It looks in all 3 axes at a distance of search_dist plus or minus
    a voxel. If more than inclusion_req points are found with a brightness
    indicating tissue, the voxel is retained. Otherwise, it is deleted.
    """
    for search_loc in range(search_dist - 1, search_dist + 2):
        inclusion_count = 0
        if inclusion_count < inclusion_req:
            try:
                if (img_data[ax_ind + search_loc][sag_ind][cor_ind] > 
                    wm_min):
                    inclusion_count +=1
            except:
                pass
        if inclusion_count < inclusion_req:
            try:
                if (img_data[ax_ind][sag_ind + search_loc][cor_ind] > 
                    wm_min):
                    inclusion_count +=1
            except:
                pass
        if inclusion_count < inclusion_req:
            try:
                if (img_data[ax_ind][sag_ind][cor_ind + search_loc] > 
                    wm_min):
                    inclusion_count +=1
            except:
                pass
    return inclusion_count


def iso_px_check(voxel, ax_ind, sag_ind, cor_ind):
    iso_count = 0
    for ax_loc in range(ax_ind - 1, ax_ind + 2):
        for sag_loc in range(sag_ind - 1, sag_ind + 2):
            for cor_loc in range(cor_ind - 1, cor_ind + 2):
                try:
                    if (img_data[ax_loc][sag_loc][cor_loc] == background):
                        iso_count += 1
                except:
                    pass
    return iso_count


def clean_bg(img_data, search_dist, inclusion_req, background, wm_min):
    """
    This function cleans isolated pixels in the background prior to image 
    normalization.
    """
    # delete blobs that are not attached to the main brain mass
    for ax_ind, ax_row in enumerate(img_data):
        for sag_ind, sag_row in enumerate(ax_row):
            for cor_ind, voxel in enumerate(sag_row):
                if wm_min > voxel > background:
                    inclusion_count = isolation_check(search_dist, 
                                                      inclusion_req, ax_ind, 
                                                      sag_ind, cor_ind, 
                                                      wm_min)
                    if inclusion_count < inclusion_req:
                        sag_row[cor_ind] = background
    # delete isolated pixels surrounded by background                    
    for ax_ind, ax_row in enumerate(img_data):
        for sag_ind, sag_row in enumerate(ax_row):
            for cor_ind, voxel in enumerate(sag_row):
                if voxel > background: 
                    iso_count = iso_px_check(voxel, ax_ind, sag_ind, 
                                             cor_ind)
                    if iso_count >= 26:
                        sag_row[cor_ind] = background
        if ax_ind % 50 == 0:                     
            print("Background clean row " + str(ax_ind) + " complete. " + 
                  "Time: " + str(time.clock())) 
    return img_data


def intensity_norm_calc(intensity_list, slice_loc, slice_dist, gm_max):
    """
    Calculates the average intensity of a coronal section and its neighbors 
    within slice_dist. The neighboring slices are included to prevent 
    artifacts from producing lots of noise in slices with limited data points
    (i.e., the rostral and caudal poles of the brain).
    """
    intensity_num = 1
    intensity_sum = intensity_list[slice_loc]
    for near_slice in range(-(slice_dist), slice_dist + 1):
        try:
            if intensity_list[slice_loc + near_slice] < gm_max:
                intensity_sum = intensity_sum + intensity_list[slice_loc + 
                                                               near_slice]
                intensity_num += 1
        except:
            pass
    intensity_avg = intensity_sum / intensity_num
    return intensity_avg


def cor_slice_normalization(img_data, slice_dist, wm_min, wm_max, gm_min, 
                            gm_max, norm_intens_pt):
    """
    Normalize the image intensity across coronal sections (most nested level 
    in MRI data). First, this function identifies the 10th brightest pixel in 
    each section. Then, it identifies the average of this value across 
    sections. It then takes the average intensity of the section and its 
    neighbors. It then corrects all voxels in the section via a ratio of the 
    section intensity vs. the average intensity.
    """
    all_intensity_list = []
    rep_intensity_list = []
    # make a list of all voxels in a coronal slice
    for cor_loc in range(len(img_data[0][0])):
        cor_list = []
        for ax_ind, ax_row in enumerate(img_data):
            for sag_ind, sag_row in enumerate(ax_row):
                if img_data[ax_ind][sag_ind][cor_loc] > wm_min:
                    cor_list.append(img_data[ax_ind][sag_ind][cor_loc])
        # find the xth brightest voxel in the slice
        if cor_list and len(cor_list) > norm_intens_pt:
            cor_list.sort()
            max_intensity = cor_list[-(norm_intens_pt)]
            rep_intensity_list.append(max_intensity)
        else:
            max_intensity = gm_max
        all_intensity_list.append(max_intensity)
    # find the average bright intensity in slices with brain tissue 
    avg_intensity_loc = (len(rep_intensity_list) / 2)
    avg_high_intensity = rep_intensity_list[avg_intensity_loc]
    # find the relative intensity of a slice and its neighbors
    for cor_loc in range(len(img_data[0][0])):
        slice_intensity_avg = intensity_norm_calc(all_intensity_list, cor_loc, 
                                                  slice_dist, gm_max)
        # adjust the brightness in the slice based on the difference between
        # local slice intensity and average intensity
        for ax_ind, ax_row in enumerate(img_data):
            for sag_ind, sag_row in enumerate(ax_row):

                img_data[ax_ind][sag_ind][cor_loc] = (
                    int(img_data[ax_ind][sag_ind][cor_loc] 
                    * float(avg_high_intensity) / float(slice_intensity_avg)))
    print ("Coronal section normalization distance " + str(slice_dist) + 
           " done" + " time: " + str(time.clock()))
    return img_data  


def find_peak_diff(img_raw, norm_intens):
    bin_size = 5
    bin_min = 0
    bin_max = 10000
    bin_list = [0] * ((bin_max - bin_min) / bin_size)
    for voxel in img_raw:
        binselect = int(float(voxel) / bin_size - bin_min)
        try:
            bin_list[binselect] = bin_list[binselect] + 1
        except:
            pass
    max_bin_val, max_bin_loc = 0, 0
    # look for the mode in the raw data, excluding background
    for binlist_bin in range(int(wm_min / bin_size), bin_max, bin_size):
        if bin_list[binlist_bin / bin_size] > max_bin_val:
            max_bin_val = bin_list[binlist_bin / bin_size]
            max_bin_loc = binlist_bin
    print "max bin loc is: " + str(max_bin_loc)
    # find the difference between the mode and the target peak
    peak_diff = max_bin_loc - norm_intens
    print "peak diff is: " + str(peak_diff)
    peak_ratio = norm_intens / max_bin_loc
    return peak_diff


def image_normalization(img_data, norm_intens, background):
    """
    Normalize the brightness of the image between subjects. The most common 
    intensity (the gray matter peak) is identified with a granularity of 5. 
    All voxels are then shifted so that the subject has a peak intensity of
    1785. This baseline was selected in an arbitrary fashion because the pilot
    cases were around this level and suggested  
    """
    img_raw = []
    for ax_row in img_data:
        for sag_row in ax_row:
            for voxel in sag_row:
                # Selective to reduce memory usage by this variable.
                if voxel > background:
                    img_raw.append(voxel)      
    peak_diff = find_peak_diff(img_raw, norm_intens)
    # Huge memory overhead on this variable.
    del img_raw
    # Adjust all voxels based on the peak difference.
    for ax_ind, ax_row in enumerate(img_data):
        for sag_ind, sag_row in enumerate(ax_row):
            for cor_ind, voxel in enumerate(sag_row):
                if voxel > 0:
                    sag_row[cor_ind] = (voxel - peak_diff)
    return img_data


def smart_voxel_flip(img_data, wm_min, wm_max, gm_min, gm_max):
    """
    Flip the voxel intensity of voxels that fall within the white
    and gray matter intensity bands.
    """
    wm_range = float(wm_max - wm_min)
    gm_range = float(gm_max - gm_min)
    for ax_ind, ax_row in enumerate(img_data):
        for sag_row in ax_row:
            for cor_ind, voxel in enumerate(sag_row):
                if voxel >= wm_min and voxel < wm_max:
                    intensity_rating = (wm_max - voxel) / wm_range 
                    sag_row[cor_ind] = int(gm_min + gm_range * 
                                             (intensity_rating))
                elif voxel >= gm_min and voxel < gm_max:
                    intensity_rating = (voxel-gm_min) / gm_range 
                    sag_row[cor_ind] = int(wm_max - wm_range * 
                                             (intensity_rating))
                else: 
                    sag_row[cor_ind] = int(background)
    print ("Voxel flip complete. " + " Time: " + str(time.clock()))
    return img_data


def row_search(row, mask_dist, img_zoom, axis):
    """
    Determines the start and stop points of brain tissue for a mask within a
    row. This may be confounded by large artifacts. It is strongly recommended
    to delete any such artifacts before running them.
    """
    start_mask_track, stop_mask_track = 0, 0
    start_mask, stop_mask = False, False
    for row_ind, voxel in enumerate(row):
        if not start_mask and voxel > gm_min:
            start_mask_track += 1
        if not start_mask and start_mask_track >= mask_dist/img_zoom[axis]:
            start_mask = row_ind
    row.reverse()
    for row_ind, voxel in enumerate(row):
        if not stop_mask and voxel > gm_min:
            stop_mask_track += 1
        if not stop_mask and stop_mask_track >= mask_dist/img_zoom[axis]:
            stop_mask = len(row)- row_ind
    return start_mask, stop_mask


def brain_mask_cor(img_mask, img_data, img_zoom, mask_set, gm_min, background, 
                   mask_dist=mask_dist):
    """
    Generates a coronal mask of voxels in the interior of the brain so that
    removal of the bright white matter rind does not affect voxels neighboring
    ventricles deep within the brain.
    """
    for ax_ind, ax_row in enumerate(img_mask):
        for sag_ind, sag_row in enumerate(ax_row):
            start_mask, stop_mask = row_search(sag_row, mask_dist, img_zoom, 
                                               axis=2)
            if start_mask and stop_mask:
                for cor_ind, voxel in enumerate(sag_row):
                    if cor_ind > start_mask and cor_ind < stop_mask:
                        sag_row[cor_ind] = mask_set                    
        if ax_ind % 50 == 0:                     
            print("Coronal mask row " + str(ax_ind) + " complete. " + 
                  "Time: " + str(time.clock())) 
    return img_mask


def brain_mask_ax(img_mask, img_data, img_zoom, mask_set, gm_min, background, 
                  mask_dist=mask_dist):
    """
    Same function as brain_mask_cor, but in the axial axis. All 3 axes must be
    examined to produce an accurate mask.
    """
    for cor_loc in range(len(img_data[0][0])):
        cor_grid = [[img_data[ax_entry][sag_entry][cor_loc] 
                     for sag_entry in xrange(len(img_data[0]))] 
                    for ax_entry in xrange(len(img_data))]
        for ax_ind, ax_row in enumerate(cor_grid):
            start_mask, stop_mask = row_search(ax_row, mask_dist, img_zoom, 
                                               axis=0)
            if start_mask and stop_mask:
                for sag_ind, voxel in enumerate(ax_row):
                    if (sag_ind > start_mask and 
                        sag_ind < stop_mask and 
                        img_mask[ax_ind][sag_ind][cor_loc] == mask_set):
                        pass
                    else:
                        # looking for a formatting/refactoring suggestion here 
                        img_mask[ax_ind][sag_ind][cor_loc] = (
                            img_data[ax_ind][sag_ind][cor_loc])                  
        if cor_loc % 20 == 0:                     
            print("Axial mask row " + str(cor_loc) + " complete. " + 
                  "Time: " + str(time.clock()))   
    return img_mask
    return img_mask
 
 
def brain_mask_sag(img_mask, img_data, img_zoom, mask_set, gm_min, background, 
                   mask_dist=mask_dist):
    """
    Same function as brain_mask_cor, but in the sagittal axis.
    """         
    for cor_loc in range(len(img_data[0][0])):
        # make an array containing the contents of each coronal slice
        cor_grid = [[img_data[ax_entry][sag_entry][cor_loc] 
                     for ax_entry in xrange(len(img_data))] 
                    for sag_entry in xrange(len(img_data[0]))]    
        for sag_ind, sag_row in enumerate(cor_grid):
            start_mask, stop_mask = row_search(sag_row, mask_dist, img_zoom, 
                                               axis=1)
            if start_mask and stop_mask:
                for ax_ind, voxel in enumerate(sag_row):
                    if (ax_ind > start_mask and 
                        ax_ind < stop_mask and 
                        img_mask[ax_ind][sag_ind][cor_loc] == mask_set):
                        pass
                    else:
                        img_mask[ax_ind][sag_ind][cor_loc] = (
                            img_data[ax_ind][sag_ind][cor_loc])
        if cor_loc % 20 == 0:                     
            print("Sagittal mask row " + str(cor_loc) + " complete. " + 
                  "Time: " + str(time.clock()))   
    return img_mask


def bound_check(img_data, ax_ind, r_dist_ax, sag_ind, r_dist_sag, 
                cor_ind, r_dist_cor, background):
    """
    Check whether the voxel in question is at a boundary with background 
    (in other words, if it is at the surface of the brain.)
    """
    boundary_load = 0
    for ax_loc in range(ax_ind - r_dist_ax, 
                         ax_ind + r_dist_ax + 1):
        for sag_loc in range(sag_ind - r_dist_sag, 
                            sag_ind + r_dist_sag + 1):
            for cor_loc in range(cor_ind - r_dist_cor, 
                                 cor_ind + r_dist_cor + 1):
                try:
                    if (img_data[ax_loc][sag_loc][cor_loc] == 
                        background):
                        boundary_load += 1         
                except:
                    pass
    return boundary_load


def rind_vox_calc(img_data, img_mask, ax_ind, r_blur_ax, sag_ind, r_blur_sag, 
                   cor_ind, r_blur_cor):
    voxel_tot, voxel_add = 0, 0 
    #gm_max_temp = gm_max
    # examine neighboring voxels to produce an average 
    # used as the replacement intensity.
    #while not voxel_add:
    for ax_loc in range(ax_ind - r_blur_ax, ax_ind + r_blur_ax + 1):
        for sag_loc in range(sag_ind - r_blur_sag, sag_ind + r_blur_sag + 1):
            for cor_loc in range(cor_ind - r_blur_cor, cor_ind + 
                                 r_blur_cor + 1):
                try:
                    voxel_iter = img_data[ax_loc][sag_loc][cor_loc]
                    if (voxel_iter > gm_min and 
                        img_mask[ax_ind][sag_ind][cor_ind] == mask_set):
                        voxel_tot = voxel_tot + voxel_iter
                        voxel_add += 1
                    elif gm_max > voxel_iter > gm_min:
                        voxel_tot = voxel_tot + voxel_iter
                        voxel_add += 1
                except:
                    pass
    if voxel_tot:
        return int(float(voxel_tot)/float(voxel_add))
    else:
        return None


def remove_rind(img_data, img_zoom, pre_flip, gm_min, gm_max, wm_min, wm_max, 
                background, img_mask, mask_set, rind_thickness, 
                rind_explore, rind_cutoff):
    """
    Removes very bright voxels that are right on the boundary of the brain. 
    These voxels are artifacts of intensity inversion; borderline GM/BG voxels
    will appear very bright.
    The function targets all bright voxels neighboring background. Voxels deep
    inside the brain are protected with a mask.
    """
    # make a copy of img_data so that data can be changed one voxel at a time
    # without affecting future calculations
    img_chg = make_copy(img_data)
    
    # calculate distance search and blur settings outside of loops for 
    # major improvement in efficiency
    r_dist_ax = int((rind_thickness + rind_explore)/img_zoom[0])
    r_dist_sag = int((rind_thickness + rind_explore)/img_zoom[1])
    r_dist_cor = int((rind_thickness + rind_explore)/img_zoom[2])
    r_blur_ax = int(blur_range/img_zoom[0])
    r_blur_sag = int(blur_range/img_zoom[1])
    r_blur_cor = int(blur_range/img_zoom[2])
  
    outer_rind_list = []
    for ax_ind, ax_row in enumerate(img_data):
        for sag_ind, sag_row in enumerate(ax_row):
            for cor_ind, voxel in enumerate(sag_row):
                # I'm looking at voxels on the high end of the gray matter 
                # range as well as white matter to prevent a banding pattern 
                # with a "high gray" band basally to the rind, which could 
                # could fool freesurfer.
                if sag_row[cor_ind] > (wm_min * .90):
                    boundary_load = bound_check(img_data, ax_ind, r_dist_ax, 
                                                sag_ind, r_dist_sag, 
                                                cor_ind, r_dist_cor, 
                                                background)
                    if boundary_load >= rind_cutoff:
                        voxel_val = rind_vox_calc(img_data, img_mask, ax_ind,
                                                  r_blur_ax, sag_ind, 
                                                  r_blur_sag, cor_ind, 
                                                  r_blur_cor)
                        if voxel_val:
                            img_chg[ax_ind][sag_ind][cor_ind] = voxel_val     
                        else:
                            img_chg[ax_ind][sag_ind][cor_ind] = (gm_min + 
                                                                 ((gm_max - 
                                                                   gm_min) 
                                                                  * .50))
                        if img_mask[ax_ind][sag_ind][cor_ind] != mask_set:
                            outer_rind_list.append((ax_ind, sag_ind, cor_ind))
        if ax_ind % 20 == 0:                     
            print("Rind removal row " + str(ax_ind) + " complete. " + 
                  "Time: " + str(time.clock()))     
    return img_chg


def bright_image(img_data, bright_pct):
    """
    Brighten the image up from its natural levels to improve freesurfer's 
    ability to read it 
    """
    return [[[voxel * (1 + bright_pct)
            for voxel in sag_row]
                for sag_row in ax_row]
                    for ax_row in img_data]


def force_mask(img_data, gm_min, gm_max, wm_min, wm_max, background):
    """
    Force the image into a gray/white binary mask; this may help if your
    program is having problems with gray/white boundaries.
    """
    for ax_row in img_data:
        for sag_row in ax_row:
            for cor_ind, voxel in enumerate(sag_row):
                if voxel > wm_min:
                    sag_row[cor_ind] = wm_max
                elif voxel > background:
                    sag_row[cor_ind] = gm_min
                else:
                    sag_row[cor_ind] = background
    return img_data


def pixel_cleanup(img_data, img_zoom, gm_min, gm_max, wm_min, wm_max, 
                  background):
    """
    Pixels are averaged with their neighbors across the blur_dist in each
    axis. This improves the regularity of the image prior to applying force 
    mask and also cleans up stray pixels that were misidentified during 
    force_mask and are surrounded by pixels of the opposing tissue type. 
    """
    # The distance across which pixels are averaged. You may want to adjust 
    # this depending on your scan parameters. Our scans have 5x resolution
    # in the ax/sag axes compared to coronal.    
    blur_ax = int(blur_range / 2 / img_zoom[0])
    blur_sag = int(blur_range / 2 / img_zoom[1])
    blur_cor = int(blur_range / img_zoom[2])
    
    for ax_ind, ax_row in enumerate(img_data):
        for sag_ind, sag_row in enumerate(ax_row):
            for cor_ind, voxel in enumerate(sag_row):
                if voxel > background:
                    voxel_sum, voxel_num = 0, 0
                    for ax_loc in range(ax_ind - blur_ax, 
                                        ax_ind + blur_ax + 1):
                        for sag_loc in range(sag_ind - blur_sag, 
                                             sag_ind + blur_sag + 1):
                            for cor_loc in range(cor_ind - blur_cor, 
                                                 cor_ind + blur_cor + 1):
                                voxel_sum = (voxel_sum + 
                                    img_data[ax_loc][sag_loc][cor_loc])
                                voxel_num += 1 
    return img_data


time.clock()
print "Loading data."
raw_name = raw_name(file_in)
datafile = open((directory + raw_name + proc_data_suffix), 'rb')
img_data = marshal.load(datafile)
zoomfile = open((directory + raw_name + zoom_suffix), 'rb')
img_zoom = marshal.load(zoomfile)

##############################################################################
# Functions that remove crud from the image are in this section. 

# These functions are left in as an option for users who have some crud in the 
# background of their image. We remove this crud using a strip in FSL, which
# also improves the coronal slice normalization procedures below dramatically.

if adjust_intensity:
    print "Adjusting image intensity."
    img_data = adjust_intens(img_data, wm_max_start, wm_min_start, 
                             gm_max_start, gm_min_start, wm_max, wm_min, 
                             gm_max, gm_min)

if clean_up_background:
    print "Zeroing dark background prior to normalization."
    img_data = clean_bg(img_data, search_dist, inclusion_req, background, 
                        wm_min)

##############################################################################
# Functions that normalize section and image intensity and then flip pixel 
# intensity are in this section

# This step normalizes the image by evening out the intensity of coronal 
# sections.
if normalize_slices: 
    for slice_dist in slice_list:
        img_data = cor_slice_normalization(img_data, slice_dist, wm_min, 
                                           wm_max, gm_min, gm_max, 
                                           norm_intens_pt)

# This step normalizes the overall image intensity level.    
if normalize_image:
    img_data = image_normalization(img_data, norm_intens, background)

# This step flips the pixel intensity within the brain to make the white 
# matter look gray and vice versa.
pre_flip = make_copy(img_data)
if intensity_correct:
    img_data = smart_voxel_flip(img_data, wm_min, wm_max, gm_min, gm_max)

##############################################################################
# Functions that broadly maintain pixel intensity while cleaning up image or 
# producing alternate outputs are in this section. Note that these functions 
# assume flipped (corrected) pixel values.

wm_min, gm_min = gm_min, wm_min
wm_max, gm_max = gm_max, wm_max

# This step removes the rinds of light pixels that appear around ventricles
# in the brain after the flip
if remove_wm_rind:  
    img_mask = make_copy(img_data)
    img_mask = brain_mask_cor(img_mask, img_data, img_zoom, mask_set, gm_min, 
                              background, mask_dist=mask_dist)
    img_mask = brain_mask_ax(img_mask, img_data, img_zoom, mask_set, gm_min, 
                             background, mask_dist=mask_dist)
    img_mask = brain_mask_sag(img_mask, img_data, img_zoom, mask_set, gm_min, 
                              background, mask_dist=mask_dist)

    img_data = remove_rind(img_data, img_zoom, pre_flip, gm_min, gm_max, 
                           wm_min, wm_max, background, img_mask, mask_set, 
                           rind_thickness, rind_explore, rind_cutoff)

# This step brightens the image if requested by the user.
if not convert_to_mask and brighten_image:   
    img_data = bright_image(img_data, bright_pct)

# This step converts the image to a mask in which all gray and white matter 
# are assigned the same intensity value. Appears to result in poorer results 
# in the Freesurfer pipeline, but may be worth testing in other processing 
# pipelines if the program is having a hard time detecting the gray/white 
# matter boundary.
if convert_to_mask:
    img_data = pixel_cleanup(img_data, img_zoom, gm_min, gm_max, wm_min, 
                             wm_max, background)
    
    for _ in xrange(cleanup_reps):
        img_data = force_mask(img_data, gm_min, gm_max, wm_min, wm_max, 
                              background)
        
        img_data = pixel_cleanup(img_data, img_zoom, gm_min, gm_max, wm_min, 
                                 wm_max, background)
    

    img_data = force_mask(img_data, gm_min, gm_max, wm_min, wm_max, 
                          background)


print "Saving raw data, use NiftiSave.py to convert to .nii."
datafile = open((directory + raw_name + proc_data_suffix), 'w+b')
marshal.dump(img_data, datafile)
print "Done, final time " + str(time.clock()) + " seconds"

# I've left these lines in should you want to save the mask used in the 
# wm_rind step and examine it for troubleshooting purposes.
# I've commented them out because going through mask saving adds significant
# time to the program.
#print "Saving mask data."
#imagemask = open((directory + raw_name + "-imgmask"), 'w+b')
#marshal.dump(img_mask, imagemask)

