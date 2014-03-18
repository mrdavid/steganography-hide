Steganography - Hide
------------- 

I am just playing around with ideas from steganography. Right now, all this does is hide bytes in the least significant bits of an image. Images are saved as 100% quality PNGs - there is no protection against compression (yet). PIL is required.

### Hiding Text

To use the sample and hide some text in a file type

    python sample.py -f out hide path/to/source/image.jpg

(will save in out.png) and

    python sample.py show out.png

### Hiding files

To use the sample and hide some text in a file type

    python sample2.py -f <file_to_hide> hide path/to/source/image.jpg

This will create path/to/source/image.jpg_out.png. To extract a file from such a generated
PNG file, use

    python sample2.py show path/to/source/image.jpg_out.png -f <filename>

and the hidden file will be written to <filename>