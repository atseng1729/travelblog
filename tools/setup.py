try:
    from StringIO import StringIO as sbIO
except ImportError:
    from io import BytesIO as sbIO
import json
import os
import struct


PATH = os.path.dirname(__file__) + '/../'
RELATIVE_PATH = 'photos'
PHOTO_PATH = PATH + RELATIVE_PATH
DESC_JSON_PATH = PATH + 'desc/desc.json'


def getImageInfo(data):
    size = len(data)
    height = -1
    width = -1
    content_type = ''

    # See PNG 2. Edition spec (http://www.w3.org/TR/PNG/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    if ((size >= 24) and data.startswith(b'\211PNG\r\n\032\n') and
       (data[12:16] == b'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)

    # Maybe this is for an older PNG version.
    elif (size >= 16) and data.startswith(b'\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)

    # handle JPEGs
    elif (size >= 2) and data.startswith(b'\xff\xd8'):
        content_type = 'image/jpeg'

        try:
            jpeg = sbIO(data)  # Python 3
        except:
            jpeg = sbIO(str(data))  # Python 2

        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF):
                    b = jpeg.read(1)
                while (ord(b) == 0xFF):
                    b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except struct.error:
            pass
        except ValueError:
            pass

    return content_type, width, height


def get_directories():
    items = os.listdir(PHOTO_PATH)
    return list(filter(lambda x: os.path.isdir(PHOTO_PATH + '/' + x), items))


def get_descriptions():
    with open(DESC_JSON_PATH) as f:
        return json.load(f)


def get_images(path, descriptions):
    images = list(sorted(os.listdir(PHOTO_PATH + '/' + path)))

    result = []
    for img in images:
        temp_path = './' + RELATIVE_PATH + '/' + path + '/' + img
        try:
            desc = descriptions[img].replace('\n', '<br>')
        except:
            desc = "Some<br>Text<br>Here"
        with open(temp_path, 'rb') as f:
            _, width, height = getImageInfo(f.read())
        result.append({
            'width': width,
            'height': height,
            'path': temp_path,
            'desc': desc
        })
    return result


def write_config(config):
    with open(PATH + 'config.json', 'w') as f:
        f.write(json.dumps(config, indent=2, separators=(',', ': ')))


if __name__=="__main__":
    config = {}
    directories = get_directories()
    data = get_descriptions()
    for path in directories:
        config[path] = get_images(path, data[path])
    write_config(config)
