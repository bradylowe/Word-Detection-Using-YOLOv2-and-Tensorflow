
import pytest
import os
import detection_utils as utils

def test_returns_none_when_file_not_exist():
    ret = utils.get_csv_contents('foofoo.csv')
    assert ret is None

def test_can_get_csv_contents():
    ret = utils.get_csv_contents('foo.csv')
    assert ret[0][1] == 89 and ret[2][4] == 524

def annotation_tags_exist():
    lines = []
    with open('foo.xml', 'r') as f:
        line = f.readline()
        while line:
            lines.append(line)
            line = f.readline()
    return lines[0] == "<annotation>\n" and lines[-1] == "</annotation>\n"

def test_can_write_annotation_tags():
    utils.initialize_xml_file('foo.png', (0, 0))
    assert annotation_tags_exist()

def test_can_write_annotation_tags_without_extension():
    utils.initialize_xml_file('foo', (0, 0))
    assert annotation_tags_exist()

def line_written_properly_to_xml(tag, value):
    found_line = False
    with open('foo.xml', 'r') as f:
        line = f.readline()
        while line:
            if '<{}>'.format(tag) in line:
                if line.strip() == "<{}>{}</{}>".format(tag, value, tag):
                    return True
                else:
                    return False
            line = f.readline()
    return False

def test_can_write_folder_line():
    utils.initialize_xml_file('foo.png', (0, 0))
    assert line_written_properly_to_xml('folder', 'data/documents')

def test_can_write_filename_line():
    utils.initialize_xml_file('foo.png', (0, 0))
    assert line_written_properly_to_xml('filename', 'foo.png')

def test_can_write_size():
    utils.initialize_xml_file('foo.png', (1234, 2345, 3))
    assert line_written_properly_to_xml('width', '1234')
    assert line_written_properly_to_xml('height', '2345')
    assert line_written_properly_to_xml('depth', '3')

def test_can_add_objects_to_xml():
    utils.initialize_xml_file('foo.png', (123, 234))
    boxes = []
    boxes.append([0, (17, 29), (420, 69)])
    boxes.append([0, (27, 19), (230, 45)])
    utils.add_objects_to_xml_file('foo', boxes)
    assert line_written_properly_to_xml('xmin', '17')
