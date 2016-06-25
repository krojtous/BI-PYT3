from PIL import Image
#Read image
im = Image.open( 'picture.JPG' )
#Display image
im.show()
box = (0, 0, im.size[0]//2, im.size[1])
region = im.crop(box)

region.show()