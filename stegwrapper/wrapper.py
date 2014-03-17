import Image
import os
import math

class wrapper(object):

    unimplemented_exception = Exception('Unimplemented')
    trying_to_save_non_writeable_exception= Exception('Trying to save a file that is not writeable.')
    file_is_closed_exception = ValueError('File is closed.')

    bits_per_pixel = 3
    bits_per_byte = 8

    @staticmethod
    def open(filename, mode='r'):
        mode = mode.lower()
        msg = ''
        an_error_occured = False
        
        if os.path.isfile(filename):
            #an_error_occured = True
            msg = "%s is not a file." % (filename)
        
        if mode != 'r' and mode != 'w':
            an_error_occured = True
            msg = "Unkown mode - must be 'w' or 'r'."

        if an_error_occured:
            raise Exception(msg)
        
        return wrapper(filename, mode)

    def __init__(self, filename, mode):
        self.closed = False
        self.mode = mode
        self.name = filename
        self.is_writable = False

        self.encoding = None
        self.name = filename
        self.newlines = None
        self.softspace = None

        # Open the image
        self.image  = Image.open(self.name)
        #self.original_data   = list(self.image.getdata())
        self.data = list(self.image.getdata())

        # Bytes that can be stored in this image 
        self.length = self.compute_length()
        self.max_index = self.length - 1
        # Remember where we are in the stream
        self.index  = 0

        if self.mode == 'w':
            self.is_writable = True



    # Compute the number of bytes that can be stored in the image.
    # Assume 3 bit per pixel (least significant bit for each color)
    def compute_length(self):
        if(self.image != None):
            return math.floor((self.image.size[0] * self.image.size[1] * wrapper.bits_per_pixel) / wrapper.bits_per_byte)
        return None

    # calculates the position of a byte in the image as a pair
    # of the form (# of pixel in image, number of color)
    def get_position_from_index(self, index):
        return int(index * wrapper.bits_per_byte / wrapper.bits_per_pixel), (index * wrapper.bits_per_byte) % wrapper.bits_per_pixel

    def get_bit_from_color_value(self, color_value):
        return color_value % 2

    def set_color_value_to_bit(self, color_value, set_bit):
        return color_value - color_value % 2 + set_bit

    def read_one_byte(self):
        if (self.index < self.max_index) and not self.closed:
            integer_sum = 0
            pixel_position, color_position = self.get_position_from_index(self.index)
            for i in range(wrapper.bits_per_byte):
                value = self.data[pixel_position][color_position]
                bit = self.get_bit_from_color_value(value)

                integer_sum = integer_sum + 2**(wrapper.bits_per_byte - 1 - i) * bit
                
                color_position = color_position + 1
                if color_position > 2:
                    color_position = 0
                    pixel_position = pixel_position + 1

        return chr(integer_sum)

    def write_one_byte(self, byte):
        if (self.index < self.max_index) and self.is_writable and not self.closed:
            integer = ord(byte)

            pixel_position, color_position = self.get_position_from_index(self.index)
            for i in range(wrapper.bits_per_byte):
                remainder = integer % (2**(wrapper.bits_per_byte - 1 - i))
                bit = 0

                if remainder != integer:
                    bit = 1
                    integer = remainder

                tmp = list(self.data[pixel_position])
                tmp[color_position] = self.set_color_value_to_bit(self.data[pixel_position][color_position], bit)
                self.data[pixel_position] = tuple(tmp)

                color_position = color_position + 1
                if color_position > 2:
                    color_position = 0
                    pixel_position = pixel_position + 1

    def advance(self):
        self.index = self.index + 1
        if self.index > self.max_index:
            self.index = self.max_index

    def has_more_bytes(self):
        return self.index < self.max_index

    # save the image
    def save(self, filename=''):
        if self.is_writable:
            self.image.putdata(self.data)
            if filename == '':
                filename = self.name
            self.image.save(filename + ".png", quality=100)
        else:
            raise wrapper.trying_to_save_non_writeable_exception

    #
    # File object interface
    #
    def close(self):
        if self.is_writable:
            self.save()

        self.closed = True
        self.is_writable = False


    def flush(self):
        raise wrapper.unimplemented_exception

    def fileno(self):
        raise wrapper.unimplemented_exception

    def isatty(self):
        return False

    def next(self):
        return self.read(1)

    def read(self, size=1):
        if self.closed:
            raise file_is_closed_exception
        buffer_ = ""
        while(self.has_more_bytes() and len(buffer_) < size):
            buffer_ += self.read_one_byte()
            self.advance()
        return buffer_

        raise wrapper.unimplemented_exception

    def readline(self):
        raise wrapper.unimplemented_exception

    def readlines(self):
        raise wrapper.unimplemented_exception

    def seek(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self.index = offset
        elif whence == os.SEEK_CUR:
            self.index = self.index + offset
        elif whence == os.SEEK_END:
            self.index = self.max_index + offset

        if self.index < 0:
            self.index = 0
        if self.index > self.max_index:
            self.index = self.max_index

    def tell(self):
        return self.index

    def truncate(self):
        raise wrapper.unimplemented_exception

    def write(self, string):
        if self.closed:
            raise file_is_closed_exception
        if not self.is_writable:
            raise trying_to_save_non_writeable_exception

        while self.has_more_bytes() and len(string) > 0:
            self.write_one_byte(string[0])
            string = string[1:]
            self.advance()

    def writelines(self):
        raise wrapper.unimplemented_exception