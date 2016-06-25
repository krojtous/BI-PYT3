from PIL import Image
from PIL.ExifTags import TAGS
import piexif

#Read image
im = Image.open( 'picture.JPG' )
#Display image
#im.show()

box = (0, 0, im.size[0] // 2, im.size[1])
region = im.crop(box)


w, h = im.size

exif_dict = piexif.load(im.info["exif"])
for v in exif_dict:
     print (v)


print ("--------------------------")



for v in exif_dict:
    print(v)

with open("picture.JPG", "rb") as imageFile:
  f = imageFile.read()
  byte_image = bytearray(f)

exif_dict['Exif'][37500] = b'a'
exif_dict['Exif'][37510] = "neco"

exif_bytes = piexif.dump(exif_dict)
im.save("new_file.jpg", "jpeg", exif=exif_bytes)

im2 = Image.open( 'new_file.jpg' )
exif_dict2 = piexif.load(im2.info["exif"])

print ("--------------------------")
print(exif_dict2['Exif'][37510])
print(exif_dict2['Exif'][37500])
#region.show()



image_int = list(byte_image)
