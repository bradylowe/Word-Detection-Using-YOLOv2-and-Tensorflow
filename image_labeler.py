
import os
import cv2
import detection_utils as utils
import config

#########################################################
### Define class boxes 
#############################################
colors = [(0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 255, 0), 
          (255, 0, 255), (0, 255, 255), (0, 0, 0), (0, 0, 0), 
          (0, 0, 0), (0, 0, 0)]

cur_class = 0
num_classes = 5
boxes = []              # List of all bounding boxes [class, TL, BR]
box_start = None        # First selected corner of current box
selecting_box = False   # Only true if left mouse is held down

##########################################################
### Define the user interface environment
##############################################
window = cv2.namedWindow("window", cv2.WINDOW_NORMAL)
screen_size = (1850, 980)            # Full resolution of user's screen
window_size = screen_size            # Desired resolution of display window
cursor_pos = (0, 0)                  # Current location of cursor in orig_image

image = None            # Reference to original image
image_boxes = None      # Reference to image with boxes drawn
view_step = 100         # Step size for translations with awsd
view_zoom = 1.0
view_pos = None

quit_program = False


###########################################################
### Functions for mouse click events (selecting box)
######################################################
def get_abs_coords(x, y):
    """ This function takes in mouse click location inside
        of the display window and returns the absolute 
        coordinates in the original image corresponding to 
        the click location. """
    global view_zoom, view_pos
    x_abs = (view_pos[0] + x) / view_zoom
    y_abs = (view_pos[1] + y) / view_zoom
    return int(x_abs), int(y_abs)

def select_box(event, x, y, flags, param):
    """ Use selecting_box flag to help control state. Left
        mouse down event begins the box selection, left mouse
        up completes the box select and stores info."""
    global selecting_box, box_start
    if selecting_box and box_start is not None:
        if event == cv2.EVENT_LBUTTONUP:
            box_end = get_abs_coords(x, y)
            add_box(box_start, box_end)
            box_start = None
            selecting_box = False
            update_image()
    else:
        if event == cv2.EVENT_LBUTTONDOWN:
            box_start = get_abs_coords(x, y)
            selecting_box = True

########################################################
### Functions for adjusting displayed image
##################################################

###  Adjust window size  ###

def set_full_screen():
    global window_size, screen_size
    window_size = screen_size
    update_image()

def set_half_screen():
    global window_size, screen_size
    window_size = (int(screen_size[0] / 2), screen_size[1])
    update_image()

def set_mini_screen():
    global window_size
    window_size = (600, 400)
    update_image()


###  Adjust image view (visible portion of image)  ###

def move_cursor(delta):
    """ Move cursor within original image. """
    global cursor_pos, width, height
    new_x = cursor_pos[0] + delta[0]
    new_x = min(new_x, width - 1)
    new_x = max(0, new_x)

    new_y = cursor_pos[1] - delta[1]
    new_y = min(new_y, height - 1)
    new_y = max(0, new_y)

    cursor_pos = (new_x, new_y)
    update_image()


def zoom_image_view(scale = 1):
    global view_zoom
    view_zoom += scale * 0.1
    if view_zoom < 0.1:
        view_zoom = 0.1
    update_image()


def update_image(unmodified=False):
    """ This function copies the original image, draws the bounding
        boxes, resizes the new image, and crops it to fit the current 
        display box. The image is displayed and returned. 

        If unmodified = True, then set zoom to zero and window size
        to full image. 

        The cursor position is adjusted to correspond to the top-left
        corner of the view (depends on window size).
    """

    global image, boxes, view_zoom, colors, view_pos, cursor_pos

    image_view = image.copy()
    for box in boxes:
        cur_class = box[0]
        cur_color = colors[cur_class]
        cur_size = max(1, int(2 / view_zoom))
        cv2.rectangle(image_view, box[1], box[2], cur_color, cur_size)

    if unmodified:
        cv2.imshow("window", image_view)
        return image_view

    new_size = (int(width * view_zoom), int(height * view_zoom))
    image_view = cv2.resize(image_view, new_size, interpolation = cv2.INTER_AREA) 

    zoom_cursor_x = int(cursor_pos[0] * view_zoom)
    zoom_cursor_y = int(cursor_pos[1] * view_zoom)
    start_x = max(0, min(new_size[0] - window_size[0], zoom_cursor_x))
    start_y = max(0, min(new_size[1] - window_size[1], zoom_cursor_y))
    end_x = max(window_size[0], min(start_x + window_size[0], new_size[0]))
    end_y = max(window_size[1], min(start_y + window_size[1], new_size[1]))
    image_view = image_view[start_y:end_y, start_x:end_x]     
    view_pos = (start_x, start_y)
    cursor_pos = (int(view_pos[0] / view_zoom), int(view_pos[1] / view_zoom))

    cv2.imshow("window", image_view)

#################################################################
### Define functions for creating bounding box labels
#########################################################
def change_class(change = 0):
    global cur_class, num_classes
    if change < 0:
        cur_class = 0
    elif change >= num_classes:
        cur_class = num_classes - 1
    else:
        cur_class = change
    print("Current class:  " + config.class_names[cur_class])

def add_box(start, end):
    """ Add class, top-left, and bottom-right points to list 
        of boxes if the dimensions are large enough. """
    global boxes, cur_class
    min_size = 5
    p1 = (min(start[0], end[0]), min(start[1], end[1]))
    p2 = (max(start[0], end[0]), max(start[1], end[1]))
    if abs(start[0] - end[0]) > min_size and abs(start[1] - end[1]) > min_size:
        boxes.append((cur_class, p1, p2))

################################################################################
################################################################################
########  MAIN PROGRAM LOOP  ::  LOOP OVER ALL IMAGES IN im_dir  ###############
################################################################################
################################################################################
##  
##  If there is an xml file already, load the image with boxes drawn on it.
##  Don't double count images with a corresponding image_boxes.png file.
##  Gather all bounding boxes for each image and write them to xml file.
##
################################################################################

cv2.namedWindow("window")
cv2.setMouseCallback("window", select_box)

for orig_image_path in os.listdir(config.im_dir):
    
    # Skip all files that are not original, boxless images
    if '_boxes' in orig_image_path:
        continue
    elif orig_image_path.endswith(('.xml', '.csv')):
        continue
    else:
        new_path = os.path.splitext(orig_image_path)[0]
        image_ext = os.path.splitext(orig_image_path)[1]

    # Build all necessary file names
    orig_image_path = os.path.join(config.im_dir, orig_image_path)
    im_path = os.path.join(config.im_dir, new_path + '_boxes' + image_ext)
    xml_path = os.path.join(config.im_dir, new_path + '.xml')

    # If there are already some labels for this box, load that image
    if os.path.exists(im_path):
        image = cv2.imread(im_path)
    else:
        image = cv2.imread(orig_image_path)
    
    # Grab the image size (very important) and draw
    height, width = image.shape[:2]
    update_image()

    # If there is not an xml file for this image, initialize one
    if not os.path.exists(xml_path):
        utils.initialize_xml_file(xml_path, (width, height))


    ### USER INPUT LOOP ###
    #######################
    # In a loop, check for any keys of interest pressed as well as
    # mouse clicks. The left mouse button is used for drag-and-drop
    # selection of box vertices, the right mouse button deletes the
    # last box.  
    #
    # "ESC" is for abort             # "BACKSPACE" is for DELETE LAST
    # "R" is for RESTART IMAGE       # "0-9" is for CLASS selection
    # "SPACE" is for NEXT IMAGE      # "ENTER" is for SAVING CURRENT
    # "awsd" is for MOVING display   # -/+ keys for ZOOM

    while True:
        key = cv2.waitKey(1) & 0xFF

        # Abort  
        # Press ESC key
        if key == 27:
            quit_program = True
            break

        # Delete the previous box
        # Press BACKSPACE key
        elif key == 8:
            boxes = boxes[:-1]
            box_start = None
            update_image()

        # Delete all boxes (cur image)
        elif key == ord("R"):
            boxes = []
            box_start = None
            cur_class = 0
            update_image()

        # Change the class
        # Numerical keys
        elif key >= ord("0") and key <= ord("9"):
            change_class(int(chr(key)))

        # Change the display
        elif key == ord("a"):
            move_cursor((-view_step, 0))
        elif key == ord("w"):
            move_cursor((0, view_step))
        elif key == ord("d"):
            move_cursor((view_step, 0))
        elif key == ord("s"):
            move_cursor((0, -view_step))
        elif key == ord("f"):
            set_full_screen()
        elif key == ord("h"):
            set_half_screen()
        elif key == ord("m"):
            set_mini_screen()
        # Zoom in
        elif key == ord("=") or key == ord("+"):
            zoom_image_view()
        # Zoom out
        elif key == ord("-"):
            zoom_image_view(-1)

        # ENTER key simply dumps current list of boxes to file
        # SPACE key dumps current boxes to file and loads next image
        elif key == 13 or key == 32:
            # Write the boxes to file
            utils.add_objects_to_xml_file(xml_path, boxes)
            # Write the labeled image to file (!! UNMODIFIED !!)
            unmod_image = update_image(unmodified=True)
            cv2.imwrite(im_path, unmod_image)
            image = unmod_image
            # Delete current list items
            boxes = []
            box_start = None
            # Next image
            if key == 32:
                cur_class = 0
                break
                

    # If quitting, exit 'for' loop
    if quit_program:
        cv2.destroyAllWindows()
        break


