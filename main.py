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

exif_dict["meta_text"] = "new value"

for v in exif_dict:
    print(v)
    #for k in exif_dict[v]:
     #   print(k, ':', exif_dict[v][k])


exif_bytes = piexif.dump(exif_dict)
im.save("new_file.jpg", "jpeg", exif=exif_bytes)

#region.show()