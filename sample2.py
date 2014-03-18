import stegwrapper
import math
import os
import argparse

MODE_SHOW = 'show'
MODE_HIDE = 'hide'

parser = argparse.ArgumentParser(description='Hide or extract a file in/from a jpg.')
parser.add_argument('mode', choices=[MODE_SHOW, MODE_HIDE], help="Hide or extract a file.")
parser.add_argument('-f', help="The file to hide or to write into.")
parser.add_argument('image', nargs=1, help='A jpg file')

arg = parser.parse_args()


def integer_to_binary(integer, bytes):
    representation = ""

    for i in range(bytes*8):
        remainder = integer % (2**(bytes*8 - 1 - i))
        bit = 0

        if remainder != integer:
            bit = 1
            integer = remainder

        representation = representation + str(bit) 

    return representation

def binary_to_hex(some_binary):
    i = 0
    hexer = ""
    while i < len(some_binary)/8:
        tmp = some_binary[i*8:(i*8)+8]
        hexer = hexer + chr(int(tmp, 2)) 
        i+=1
    return hexer

def hex_to_integer(hexxer):
    i = 0
    inter = ""
    while i < len(hexxer):
        inter = inter + integer_to_binary(ord(hexxer[i]),1)
        i+=1
    return int(inter, 2)


imageFile = str(arg.image[0])
mode = arg.mode
datei = str(arg.f)

if mode == MODE_HIDE:
    if not datei:
        print "Please specify a file to hide."
        sys.exit(1)

    p = stegwrapper.picture.open(imageFile, "w")

    # we need some bytes to store the length of the file
    size_buffer = int(math.ceil((math.ceil(math.log(p.length * 8,2))) / 8))

    max_size = p.length - size_buffer

    size = os.path.getsize(datei)

    filesize_as_hex = binary_to_hex(integer_to_binary(size, size_buffer))

    if size > max_size:
        raise Exception("File is too big to store in this image.")

    #print repr(filesize_as_hex)
    p.write(filesize_as_hex)

    f = open(datei, "rb")
    try: 
        byte = f.read(1)
        while byte != "":
            p.write(byte)
            byte = f.read(1)
    finally:
        f.close()

    p.save(imageFile + "_out")

else:
    p = stegwrapper.picture.open(imageFile)

    size_buffer = int(math.ceil((math.ceil(math.log(p.length * 8,2))) / 8))
    filesize =  hex_to_integer(p.read(size_buffer))
    f = open(datei, "wb")

    for i in range(filesize):
        #print p.read()
        f.write(bytearray(p.read()))
    f.close()

#im = Image.open(imageFile)
#im.getdata()