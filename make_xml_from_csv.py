
import detection_utils as utils
import os
import config

for csv_file in os.listdir(config.im_dir):

    if not csv_file.endswith('.csv'):
        continue

    xml_file = os.path.splitext(csv_file)[0][:-6] + '.xml'

    csv_file = os.path.join(config.im_dir, csv_file)
    xml_file = os.path.join(config.im_dir, xml_file)

    contents = utils.get_csv_contents(csv_file)
    size = (contents[0][5], contents[0][6])
    if len(contents) == 0:
        continue

    utils.initialize_xml_file(xml_file, size)
    utils.add_objects_to_xml_file(xml_file, contents)
