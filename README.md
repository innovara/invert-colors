# Summary

With invert-colors.py, you can invert the colors or channels of a given image.

It is obviously a Python script and it supports JPG, PNG and TGA images.

Other formats may or may not work, but you are free to try.

## How to use it

Use:
```shell
 ./invert-colors.py -s /path/to/image [-c | -r | -g | -b] [-l]
 ```

Where:
 - -c inverts all the colors
 - -r inverts the red channel
 - -g inverts the green channel
 - -b inverts the blue channel

The optional switch -l displays some logs on screen which are also saved to a file.

invert-colors.py will create a new file. If the inverted file already exists, it will ask for confirmation before it overwrites it.
