
import csv
import os


def get_csv_contents(filename):
    if not os.path.exists(filename):
        return
    contents = []
    with open(filename) as f:
        reader = csv.reader(f, delimiter=',')
        next(reader)
        for row in reader:
            int_row = [int(value) for value in row]
            contents.append(int_row)
    return contents

def strip_filename(fname):
    if fname.lower().endswith(('.png', '.csv', '.xml')):
        return os.path.splitext(fname)[0]
    return fname

def initialize_xml_file(fname, size):

    if len(size) == 2:
        depth = '1'
    elif len(size) == 3:
        depth = str(size[2])
    else:
        return

    width = str(size[0])
    height = str(size[1])

    fname = strip_filename(fname)
    with open(fname + ".xml", 'w+') as f:
        f.write("<annotation>\n")
        f.write("    <folder>data/documents</folder>\n")
        f.write("    <filename>{}.png</filename>\n".format(fname))
        f.write("    <size>\n")
        f.write("        <width>{}</width>\n".format(width))
        f.write("        <height>{}</height>\n".format(height))
        f.write("        <depth>{}</depth>\n".format(depth))
        f.write("    </size>\n")
        f.write("    <segmented>0</segmented>\n")
        f.write("</annotation>\n")

def add_objects_to_xml_file(fname, contents):
    
    if len(contents) == 0:
        return

    fname = strip_filename(fname)
    with open(fname + '.xml', 'r') as f:
        lines = f.readlines()

    last_line = lines[-1]
    lines = lines[:-1]

    class_names = ['section', 'header', 'word', 'bullet', 'page', 
                   'unk', 'unk', 'unk', 'unk', 'unk']
    
    for box in contents:
        cur_class = class_names[box[0]]
        xmin, ymin = box[1][0], box[1][1]
        xmax, ymax = box[2][0], box[2][1]
        lines.append("    <object>\n")
        lines.append("        <name>{}</name>\n".format(cur_class))
        lines.append("        <pose>Unspecified</pose>\n")
        lines.append("        <truncated>0</truncated>\n")
        lines.append("        <occluded>0</occluded>\n")
        lines.append("        <difficult>0</difficult>\n")
        lines.append("        <bndbox>\n")
        lines.append("            <xmin>{}</xmin>\n".format(xmin))
        lines.append("            <ymin>{}</ymin>\n".format(ymin))
        lines.append("            <xmax>{}</xmax>\n".format(xmax))
        lines.append("            <ymax>{}</ymax>\n".format(ymax))
        lines.append("        </bndbox>\n")
        lines.append("    </object>\n")

    lines.append(last_line)
    
    with open(fname + '.xml', 'w') as f:
        for line in lines:
            f.write(line)
            
def write_labels_to_csv(csv_file, labels):
    if len(labels) == 0:
        return
    with open(csv_file, 'a+') as f:
        if not os.path.exists(csv_file):
            f.write('class,x1,y1,x2,y2,xmax,ymax\n')
        for label in labels:
            out_line = str(label[0]) + ',' + str(label[1][0]) + ',' + str(label[1][1])
            out_line += ',' + str(label[2][0]) + ',' + str(label[2][1]) + ','
            out_line += str(label[3][0]) + ',' + str(label[3][1])
            f.write(out_line + '\n')


