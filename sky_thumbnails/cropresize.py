
"""
The following code comes from cropresize, and is frozen here due to issues with PIL dependency:

NOTE: Updated to handle iOS photos wrt rotation. See http://stackoverflow.com/a/11543365/931277.

Metadata-Version: 1.0
Name: cropresize
Version: 0.1.6
Summary: crop and resize an image without doing the math yourself
Home-page: http://pypi.python.org/pypi/cropresize
Author: Jeff Hammel
Author-email: k0scist@gmail.com
License: GPL
Description: cropresize
        ==========

        cropresize uses `PIL <http://www.pythonware.com/products/pil/>`_
        to crop and resize an image as appropriate for web
        presentation. cropresize is a convenience package that allows image
        resizing without aspect ratio distortion.

        API
        ---

        cropresize contains one useful function, ``cropresize.crop_resize``.
        The function takes three arguments:

            * image: a `PIL image <http://www.pythonware.com/library/pil/handbook/image.htm>`_ object
            * size: a 2-tuple of (width,height);  at least one must be specified
            * exact_size: whether to scale up for smaller images

        See ``cropresize.crop_resize.__doc__`` for the function
        documentation.  ``crop_resize`` returns the cropped and resized PIL image.


        Command Line
        ------------

        The command line program, ``crop-resize``, is included in this python
        package.  The help for the program is displayed by running
        ``crop-resize`` with no arguments or ``crop-resize --help``.


        Future Work
        -----------

        cropresize is written as a convenience function to PIL as this
        methodology for cropping and resizing images is often desired for
        presentation, particularly on the web.  Since the utility is in
        demand, the functionality should be ported upstream to PIL.

        --

        http://k0s.org/portfolio/software.html#cropresize

Keywords: image
Platform: UNKNOWN
"""

import sys
try:
    import Image
except ImportError:
    from PIL import Image, ExifTags

def crop_resize(image, size, exact_size=False):
    """
    Crop out the proportional middle of the image and set to the desired size.
    * image: a PIL image object
    * size: a 2-tuple of (width,height);  at least one must be specified
    * exact_size: whether to scale up for smaller images
    If the image is bigger than the sizes passed, this works as expected.
    If the image is smaller than the sizes passed, then behavior is dictated
    by the ``exact_size`` flag.  If the ``exact_size`` flag is false,
    the image will be returned unmodified.  If the ``exact_size`` flag is true,
    the image will be scaled up to the required size.
    """
    assert size[0] or size[1], "Must provide a width or a height"

    size = list(size)

    try:
        for orientation in list(ExifTags.TAGS.keys()):
            if ExifTags.TAGS[orientation] == 'Orientation':
                break
        exif = dict(list(image._getexif().items()))

        if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass

    image_ar = image.size[0]/float(image.size[1])
    crop = size[0] and size[1]
    if not size[1]:
        size[1] = int(image.size[1]*size[0]/float(image.size[0]) )
    if not size[0]:
        size[0] = int(image.size[0]*size[1]/float(image.size[1]) )
    size_ar = size[0]/float(size[1])

    if size[0] > image.size[0]:
        if size[1] > image.size[1]:
            if not exact_size:
                return image
        else:
            pass
            # raise NotImplementedError
    elif size[1] > image.size[1]:
        pass

    if crop:
        if image_ar > size_ar:
            # trim the width
            xoffset = int(0.5*(image.size[0] - size_ar*image.size[1]))
            image = image.crop((xoffset, 0, image.size[0]-xoffset, image.size[1]))
        elif image_ar < size_ar:
            # trim the height
            yoffset = int(0.5*(image.size[1] - image.size[0]/size_ar))
            image = image.crop((0, yoffset, image.size[0], image.size[1] - yoffset))

    try:
        # For Pillow 9.1+
        resampling = Image.Resampling.LANCZOS
    except AttributeError:
        # For Pillow 9.0.1 and earlier
        resampling = Image.ANTIALIAS

    return image.resize(size, resampling)

def main():
    from optparse import OptionParser
    parser = OptionParser('%prog [options] image1.png [image2.jpg] [...]')
    parser.add_option('-W', '--width',
                      help="desired width of image in pixels")
    parser.add_option('-H', '--height',
                      help="desired height of image in pixels")
    parser.add_option('-e', '--exact-size', dest='exact',
                      action='store_true', default=False,
                      help="scale up images smaller than specified")
    parser.add_option('-d', '--display', dest='display',
                      action='store_true', default=False,
                      help="display the resized images (don't write to file)")
    parser.add_option('-O', '--file', dest='output',
                      help="output to a file, stdout otherwise [1 image only]")
    (options, args) = parser.parse_args()

    # print arguments if files not given
    if not args:
        parser.print_help()
        sys.exit()

    # get the desired size
    try:
        width = int(options.width)
    except TypeError:
        width = None
    try:
        height = int(options.height)
    except TypeError:
        height = None

    # asser that we have something to do with the image
    if not options.display:
        if len(args) > 1:
            raise NotImplementedError # XXX

    # resize the images
    for arg in args:
        image = Image.open(arg)
        new_image = crop_resize(image, (width, height), options.exact)
        if options.display:
            new_image.show()
        else:
            if len(args) == 1:
                # output
                if options.output:
                    new_image.save(options.output)
                else:
                    sys.stdout.write(new_image.tostring(image.format))

if __name__ == '__main__':
    main()
