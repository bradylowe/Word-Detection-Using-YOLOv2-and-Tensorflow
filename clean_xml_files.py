import os



xml_dir = 'backup'

for xml_path in os.listdir(xml_dir):

    if '.xml' not in xml_path:
        continue
    else:
        xml_path = os.path.join(xml_dir, xml_path)

    with open(xml_path, 'r') as f:
        lines = f.readlines()
    
    output = lines[:9]
    last_line = lines[-1]

    for idx, line in enumerate(lines):
        if '<object>' in line:
            xmin = int(lines[idx + 7].strip()[6:-7])
            ymin = int(lines[idx + 8].strip()[6:-7])
            xmax = int(lines[idx + 9].strip()[6:-7])
            ymax = int(lines[idx + 10].strip()[6:-7])
            if abs(xmax - xmin) > 5 and abs(ymax - ymin) > 5:
                for i in range(13):
                    output.append(lines[idx + i])

    output.append(last_line)

    os.remove(xml_path)
    with open(xml_path, 'w+') as f:
        for line in output:
            f.write(line)
