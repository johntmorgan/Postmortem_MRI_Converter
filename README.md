This is a collection of several scripts that handle scanned .nii images from 
 postmortem brains (including single hemispheres), converting them into full 
 brains with coloration equivalent to a T1-weighted structural image from a 
 living brain for further processing and analysis. We have successfully tested 
 the outputs from this program on a recent version of Freesurfer.
 
 The main program, PostmortemMRIConverter.py, has no external library 
 dependencies, allowing it to be run under the PyPy interpreter, which 
 produces a >100x performance increase, decreasing run times from several 
 hours to a few minutes. NiBabel (and by extension Numpy) library 
 dependencies are offloaded into NiftiLoad.py and NiftiSave.py.
 
 As a tradeoff, you must run NiftiLoad.py before using this script to 
 generate temp files that the script will operate on, and NiftiSave.py after 
 running this script to convert back into .nii.

 Note that temp files (-tmp) are generated but not deleted during this 
 process. This allows the user to test variable settings without needing
 to reload each time. However, you will need to delete the -tmp files 
 manually when you are satisfied with the output.

#############################################################################
 Setting up your computer to run this program

 This program is written in Python 2.7. Please ensure that all installed 
 libraries are up to date but not using Python 3+!

 Step 1: Install Python 2.7.3 from here: 
 http://www.python.org/download/releases/2.7.3/
 On the page, select the Windows MSI installer (x86 if you have 32-bit 
 Windows installed, x86-64 if you have 64-bit Windows installed.)
 I suggest using the default option, which will install Python to c:/Python27

 Step 2: Install PyPy from here: http://pypy.org/download.html

 Step 3: Install NumPy to your python directory from here: 
 http://sourceforge.net/projects/numpy/files/NumPy/

 Step 4: Install NiBabel to your python directory from here:
 http://nipy.org/nibabel/

 Step 5: Copy the programs in this folder into the c:/Python27 directory
 You can also put them into another directory that is added to the Python & 
 PyPy PATHs.

#############################################################################
 Steps to process a scan

 Pre-run: If possible, load the image and strip it using a program like FSL. 
 This is likely to greatly improve results. *If the brain was embedded in 
 gelatin, this program will handle it very poorly unless the gelatin has 
 already been removed somehow!* 

 Step 1: Load the .nii file and convert it into a format that PyPy can handle
 using NiftiLoad.py. From the command line, enter the directory where the 
 programs are stored and type "python NiftiLoad.py" and hit enter.

 Step 2 (optional): Run NiftiMirror if only a single hemisphere was scanned.
 You will probably need to run NiftiMirror and then save and check the file
 several times until you find settings that produce a good mirror. From the 
 command line, enter the directory where the programs are stored and type 
 "python NiftiMirror.py" and hit enter.

 Step 3: Set variables below.

 Step 4: Run this program from the command line by entering the directory 
 where this file is saved and typing "pypy PostmortemMRIConvert.py"

 Step 5: Save the .nii file to a new filename using NiftiSave.py. From the 
 command line, enter the directory where the programs are stored and type 
 "python NiftiSave.py" and hit enter.
