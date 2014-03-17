import stegwrapper
import argparse

MODE_SHOW = 'show'
MODE_HIDE = 'hide'

parser = argparse.ArgumentParser(description='Hide or extract a file in/from a jpg.')
parser.add_argument('mode', choices=[MODE_SHOW, MODE_HIDE], help="Hide or extract a file.")
parser.add_argument('-f', help="The file to hide or to write into.")
parser.add_argument('image', nargs=1, help='A jpg file')

arg = parser.parse_args()

imageFile = str(arg.image[0])
mode = arg.mode
datei = str(arg.f)

if mode == MODE_HIDE:
    if not datei:
        print "Please specify a file to hide."
        sys.exit(1)

    p = stegwrapper.picture.open(imageFile, "w")
    print "Enter some characters to hide to hide:"
    a = raw_input()
    print "Please wait"
    p.write(a)
    p.save(datei)

else:
    p = stegwrapper.picture.open(imageFile)
    print "Read how many bytes?"
    a = int(raw_input())
    print repr(p.read(a))

#im = Image.open(imageFile)
#im.getdata()