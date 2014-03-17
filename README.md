Steganography - Hide
------------- 

I am just playing around with ideas from steganography. Right now, all this does is hide bytes in the least significant bits of an image. Images are saved as 100% quality PNGs - there is no protection against compression (yet). PIL is required.

To use the sample type

    python sample.py -f out hide path/to/source/image.jpg

(will save in out.png) and

    python sample.py show path/to/source/image.png

