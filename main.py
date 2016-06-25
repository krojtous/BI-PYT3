from PIL import Image
import io
import piexif

path = input('Zadej cestu k stereoskopickemu obrazku: ')

#Read image
im = Image.open( path )
#Display image
#im.show()

open_image()
split_image()
add_metadata()
save_image()




box = (0, 0, im.size[0] // 2, im.size[1])
region = im.crop(box)


w, h = im.size

exif_dict = piexif.load(im.info["exif"])
for v in exif_dict:
     print (v)


print ("--------------------------")



for v in exif_dict:
    print(v)

with open("small.JPG", "rb") as imageFile:
  f = imageFile.read()
  byte_image = bytearray(f)


exif_dict['Exif'][37500] = byte_image
exif_dict['Exif'][37510] = "neco2"

exif_bytes = piexif.dump(exif_dict)
im.save("new_file.jpg", "jpeg", exif=exif_bytes)

im2 = Image.open( 'new_file.jpg' )
exif_dict2 = piexif.load(im2.info["exif"])

print ("--------------------------")
print(exif_dict2['Exif'][37510])
print(exif_dict2['Exif'][37500])

retrieved_image = Image.open(io.BytesIO(exif_dict2['Exif'][37500]))
retrieved_image.show()


