# word-detection-with-conv-net

**Collection of code for detecting and interpreting text from images**

This directory houses code, data, and neural network models
for the automation of parsing input text files such as pdfs, 
screenshots, or images of text. The word_detection.ipynb is 
not finished or working, but is available for viewing. All 
other files contain working code and are described below.

The gif seen here demonstrates the
use of the annotation tool image_labeler.py (OpenCV).

![](using_image_labeler.gif)

## Installation

**Dependencies:**
 - jupyter, matplotlib, tensorflow, numpy, scipy
 - sklearn (On Linux:  pip install scikit-learn)
 - cv2 (On Linux: pip install opencv-python)
 - time, datetime, math, os

After cloning the repo and installing the dependencies,
you can perform one of the following tasks:
 - python image_labeler.py
   * This is an image annotation tool for labeling object
     detection datasets.
   * To use this, you must have a directory with images of
     objects. 
   * Modify the *setup.py* file to point to the image 
     directory or move your images into ./data/documents
   * This program outputs two files:
      * imagefile_boxes.png:  Image with boxes drawn on it
      * imagefile.xml:        Annotations stored in this file
   * Controls:
      * Drag and drop with the left mouse to define bounding boxes.
      * Use number 0-9 to choose the class of the current bounding box.
      * Use "awsd" for panning the image left, right, up and down.
      * Use +/- keys for zooming in and out.
      * Use ESC key to exit without saving.
      * Use ENTER key to save the current boxes.
      * Use SPACE BAR to save and load the next image.
      * Use BACKSPACE to delete the previous bounding box.

**NOTE: Looking at the .ipynb files will give in depth examples/explanations.**

## List of files and directories

**Files**
 - **char_recognition.ipynb**:  ipython notebook environment for
                            training and testing neural networks
                            for classifying ascii characters.
 - **detection_utils.py**:  This file houses functions for reading
                            and writing bounding box and class info to
                            and from csv and xml files.
 - **digit_recognition.ipynb**:  Just a classifier for digits 0-9.
 - **image_labeler.py**:  A command-line program for annotating images
                          for creating dataset for detection systems. 
 - **make_xml_from_csv.py**:  A small script for creating xml files from
                              csv files (bounding box info).
 - **setup.cfg**:  Used for specific automated testing (pytest)
 - **teset_detection_utils.py**:  List of code test case implementation
                                  using pytest.

**Directories**
 - **data**:  Directory storing training and testing data for various models.
   * Chars74 (not included):  Stores dataset for classification of alpha-numeric chars.
      * This dataset is described in the following publication:  T. E. de Campos, B. R. Babu and M. Varma. Character recognition in natural images. In Proceedings of the International Conference on Computer Vision Theory and Applications (VISAPP), Lisbon, Portugal, February 2009. 
   * MNIST (not included):  Stores the MNIST 0-9 digit dataset
   * documents:  Stores images of documents and annotation files containing
                 bounding box information for detection system.
 - **models**:  Stores trained models such as character classifiers and 
            text detection models.
