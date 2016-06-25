from PIL import Image
import os
import io
import piexif
import sys


def split_image(im):
    """
    Funkce split_imaVrací levou polovinu vstupního obrázku.
    """
    box = (0, 0, im.size[0] // 2, im.size[1])
    return im.crop(box)


def add_metadata(im):
    meta_text = input('Zadejte textová metadata '
                      '(pokud nechcete pridavat, ponechte prazdne): ')
    if meta_text == "":
        print("Textova metadata nepripojena.")
    exif_dict = piexif.load(im.info["exif"])
    exif_dict['Exif'][37510] = meta_text

    path = input('Zadejte cestu k obrazovym metadatum '
                 '(pokud nechcete pridavat, ponechte prazdne): ')
    while True:
        if path == "":
            print("Obrazova metadata nepripojena.")
            exif_bytes = piexif.dump(exif_dict)
            return exif_bytes
        try:
           with open(path, "rb") as imageFile:
               f = imageFile.read()
        except FileNotFoundError:
            print("Na zadane ceste:", path,
                  "neexistuje obrazek. Zadejte novou cestu:")
            path = input()
        else:
            if os.stat(path).st_size > 56000:
                print("Obrazek na ceste:", path,
                      "je prilis velky. Zadejte novou cestu:")
                path = input()
            else:
                break

    byte_image = bytearray(f)
    exif_dict['Exif'][37500] = byte_image

    exif_bytes = piexif.dump(exif_dict)
    return exif_bytes


def retrieve_metadata(im2):
    exif_dict2 = piexif.load(im2.info["exif"])
    print("Textová metadata:",
          exif_dict2['Exif'][37510][0:].decode("utf-8"))

    retrieved_image = Image.open(io.BytesIO(exif_dict2['Exif'][37500]))
    print ("Obrazova metadata zobrazena v samostatnem okne.")
    retrieved_image.show()


def image_loading(path):
    while True:
        try:
            im = Image.open(path)
        except Exception:
            print("Na zadane ceste:", path,
                  "neexistuje obrazek. Zadejte novou cestu:")
            path = input()
        else:
            print("Obrazek:", path, "nacten.")
            return im


def image_saving(path, exif_bytes, im2):
    while True:
        try:
            im2.save(path, "jpeg", exif=exif_bytes)
        except OSError as ex:
            print("Behem ukladani obrazku na ceste", path,
                  " doslo k chybe:", type(ex))
            sys.exit()
        except IOError:
            print("Na zadane ceste:", path,
                  "nelze provest zapis. Zadejte novou cestu:")
            path = input()
        else:
            print("Obrazek ulozen na ceste:", path)
            break


def metadata_handling():
    option = input('Chcete obrazek editovat (e) nebo'
                   ' nacist metadata (n)? ')
    while (option != "e"
           and option != "n") :
        option = input('Napiste "n" nebo "e":')

    if option == "e":
        path = input('Zadejte cestu k stereoskopickemu obrazku: ')
        im = image_loading(path)
        im2 = split_image(im)
        print("Obrazek oriznut na polovinu.")
        exif_bytes = add_metadata(im)
        path = input('Zadejte cestu k vyslednemu obazku: ')
        image_saving(path, exif_bytes, im2)

    else:
        path = input('Zadejte cestu k obazku,'
                     ' z ktereho chcete nacist metadata: ')
        im = image_loading(path)
        retrieve_metadata(im)

    print("Konec")


if __name__ == "__main__":
    metadata_handling()