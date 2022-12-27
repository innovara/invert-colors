# Summary

With invert-colors.py, you can invert the colors or channels of a given image.

It is obviously a Python script and it supports JPG, PNG and TGA images.

Other formats may or may not work, but you are free to try.

RGB and RGBA mode images can be color inverted and channel inverted.

L, LA, P and PA mode images can only be color inverted.

## How to use it

Use:
```shell
 ./invert-colors.py -s /path/to/image [-c | -r | -g | -b] [-y] [-l]
 ```

Where:
 - -c inverts all colors
 - -r inverts red channel
 - -g inverts green channel
 - -b inverts blue channel

The optional switch -y overwrites an existing output file. If you don't use the switch, you will have to confirm that you want to overwrite it.

Lastly, the switch -l shows logs on screen and it also saves them to a text file.
