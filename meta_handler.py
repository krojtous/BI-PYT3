#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Skript meta_handler.py slouží k úpravě stereoskopického obrázku, z kterého
vyřezává levou polovinu a dále k připojení nestandardních metadat k obrázku.
Metadata jsou textová a obrazová a jsou připojována do formátu exif.Skript
také umožňuje dříve připojená data načíst a zobrazit.

Skript nepřijímá žádné argumenty na vstupu. Běh je řízen průběžnými
uživatelskými vstupy. Na začátku si uživatel vybere, zda chce upravovat
obrázek nebo načíst metadata z již vytvořeného obrázku. Následně je vyzýván
k zadávání uživatelských vstupů, kterými dále řídí běh skriptu.
"""
from PIL import Image
import os
import io
import piexif
import sys


def split_image(im):
    """
    Funkce split_image vrací levou polovinu vstupního obrázku im.
    """

    box = (0, 0, im.size[0] // 2, im.size[1])
    return im.crop(box)


def add_metadata(im):
    """
    Funkce add_metadata vrací exif vstupniho obrazku im obohaceného o
    textová a obrazová metadata v bytové podobě. Na uživatelském vstupu
    jsou očekávány text a cesta k obrázku k připojení. Pokud cesta neexistuje
    neboje obrazek příliš velký, je uživatel vyzván k opětovnému zadání.

    Textová data jsou ukládána do exifu pod klíčem 37510 a obrazová
    pod kódem 37500.
    """

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
    """
    Funkce retrieve_metadata nacte z obrazku v argumentu im2
    nestandardni textova a obrazova metadata a zobrazi je.
    """

    exif_dict2 = piexif.load(im2.info["exif"])
    print("Textová metadata:",
          exif_dict2['Exif'][37510][0:].decode("utf-8"))

    retrieved_image = Image.open(io.BytesIO(exif_dict2['Exif'][37500]))
    print ("Obrazova metadata zobrazena v samostatnem okne.")
    retrieved_image.show()


def image_loading(path):
    """
    Funkce image_loading nacte obtazek na ceste path.
    Pokud se obrazek nedari otevrit, je uzivatel vyzvan
    k novemu zadani.
    """

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
    """
    Funkce image_saving připojí exif v bytove podobě (exif_bytes)
    k obrazku (im2) a ulozi ho na zadanou cestu (path). Pokud
    pri ukladani dojde k vyjimce IOError (například soubor existuje
    a nelze přepsat) je uživatel vyzván k novému vstupu.
    """

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
    """
    Funkce metadata_handling je hlavní funkcí skriptu. Uživatel
    si na začátku zvolí, zda chce editovat obrázek (vyříznou polovinu)
    a připojovat metadata nebo metadata neopak načítat. Následně je
    vyzván k zadání dalších informací, na jejichž základě je řízen
    běh programu.
    """

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