from PIL import Image, ImageFilter
#Read image
im = Image.open( 'picture.JPG' )
#Display image
im.show()

box = (100, 100, 400, 400)
region = im.crop(box)

region.show()