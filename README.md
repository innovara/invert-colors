# invert-colors.py

INCOMPLETE, more to come

## Introduction

invert-colors.py inverts colors of a given image or channels.

The file formats supported are JPG, PNG and TGA.

Other formats may or may not work but you are free to try.

## How to use it

Use:
```shell
 ./invert-colors.py -s /path/to/image [-c | -r | -g | -b] [-l]
 ```

Where:
 - c inverts all colors
 - r inverts the red channel
 - g inverts the green channel
 - b inverst the blue channel

If you want information displayed on screen and logged to a log file use -l.

invert-colors.py will create a new file. If the inverted file already exists, it will ask for confirmation before it overwrites it.
