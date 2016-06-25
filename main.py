from PIL import Image
from PIL.ExifTags import TAGS

#Read image
im = Image.open( 'picture.JPG' )
#Display image
im.show()
box = (0, 0, im.size[0]//2, im.size[1])
region = im.crop(box)


ret = {}
info = im._getexif()
for tag, value in info.items():
    decoded = TAGS.get(tag, tag)
    ret[decoded] = value

print (ret)

region.show()