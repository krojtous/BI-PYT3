from PIL import Image
import io
import piexif


def split_image(im):
    box = (0, 0, im.size[0] // 2, im.size[1])
    return im.crop(box)


def add_metadata(im):
    # meta_text = input('Zadejte textová metadata (pokud nechcete pridavat, ponechte prazdne): ')
    meta_text = 'Toto je zkusebni meta text.'
    exif_dict = piexif.load(im.info["exif"])
    exif_dict['Exif'][37510] = meta_text

    # path = input('Zadejte cestu k obrazovym metadatum (ne vetsi nez 10 kB;pokud nechcete pridavat, ponechte prazdne): ')
    with open("small.JPG", "rb") as imageFile:
        f = imageFile.read()
        byte_image = bytearray(f)

    exif_dict['Exif'][37500] = byte_image

    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes



def retrieve_metadata(im2):
    exif_dict2 = piexif.load(im2.info["exif"])
    print("Textová metadata: ", exif_dict2['Exif'][37510][0:])

    retrieved_image = Image.open(io.BytesIO(exif_dict2['Exif'][37500]))
    retrieved_image.show()


option = input('Chcete obrazek editovat (e) nebo nacist metadata (n)? ')
while option != "e" and option != "n":
    option = input('Napiste "n" nebo "e":')

if option == "e":
    #path = input('Zadej cestu k stereoskopickemu obrazku: ')
    path = 'picture2.JPG'
    while True:
        try:
            im = Image.open( path ) #Read image
        except FileNotFoundError:
            print("Na zadane ceste:",path,"neexistuje obrazek. Zadejte novou cestu:")
            path = input()
        else:
            print("Obrazek:", path, " nacten.")
            break
    im2 = split_image(im)
    exif_bytes = add_metadata(im)
    im2.save("new_file.jpg", "jpeg", exif=exif_bytes)
else:
    path2 = "new_file.jpg"
    im = Image.open(path2)
    im.show()
    retrieve_metadata(im)
















