Steganography - Hide
------------- 

I am just playing around with ideas from steganography. Right now, all this does is hide bytes in the least significant bits of an image. Images are saved as 100% quality PNGs - there is no protection against compression (yet). PIL is required.

### Hiding Text

To use the sample and hide some text in a PNG image type

    python sample.py -f out hide path/to/source/image.jpg

(will save in out.png) and

    python sample.py show out.png

### Hiding files

To use the sample and hide an arbitrary file in a PNG image type

    python sample2.py -f <file_to_hide> hide path/to/source/image.jpg

This will create path/to/source/image.jpg_out.png. To extract a file from such a generated
PNG file, use

    python sample2.py show path/to/source/image.jpg_out.png -f <filename>

and the hidden file will be written to &lt;filename&gt;

### Getting a file-like object

The following code

    import stegwrapper

    p = stegwrapper.picture.open("filename", "w")

creates an object *p* much like the file objects in python. You can use *read(n)* and *write(str)*
to read and write bytes from/to the image. *seek*, *tell* and *close* are implemented as well. The idea
is that you can (steganographically) save what you have read from a file directly into the picture:

    file = open('some_binary_file', 'rb')
    pic  = stegawrapper.picture.open('hide_stuff_here.png', 'w')

    byte = file.read(1)
    pic.write(byte)

The overhead in *sample2.py* is just to give it a command line interface and to save the size of the
hidden file into the first few steganographic bytes as well.