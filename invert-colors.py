#!/usr/bin/env python3
import argparse
import os.path
from datetime import datetime
from PIL import Image
from PIL import ImageChops


def log(message):
  '''Logs to screen and file if -l is used.'''
  if logging == True:
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(now + ': ' + message + '.')
    log_file = 'convert.log'
    with open(log_file, 'a', encoding='utf-8') as log:
      log.write(now + ': ' + message + '.\n')
  else:
    pass


def ask_user(message):
  '''Prompts an input message on screen'''
  try:
    answer = input(message)
    if answer == 'yes':
      log("user continued")
  except KeyboardInterrupt:
    log('user interrupted. Aborting conversion')
    exit()
  return answer


def invert_color_rgba(image):
  '''Inverts color of an image object with RGBA mode.'''
  alpha = image.getchannel('A')
  image = image.convert('RGB')
  inv_image = ImageChops.invert(image)
  inv_image.putalpha(alpha)
  return inv_image


def invert_color_p(image):
  '''Inverts color of an image object with P mode.'''
  palette = image.getpalette()
  I_max = 255
  inv_palette = [I_max - x for x in palette]
  inv_image = image
  inv_image.putpalette(inv_palette)
  return inv_image


def invert_color(path, image, mode):
  log('color inversion started')
  root, extension = os.path.splitext(path)
  suffix = '_inv'
  dest_image = root + suffix + extension
  log('destination: \'' + dest_image + '\'')
  if os.path.isfile(dest_image) is True:
    if overwrite == True:
      pass
    else:
      log('destination file already exists')
      message = '\033[31mWARNING:\033[0m Existing file will be overwritten.\nType yes to continue or Ctrl+c to cancel: '
      confirm = ask_user(message)
      while confirm != "yes":
        confirm = ask_user(message)
  if mode == 'RGBA':
    inv_image = invert_color_rgba(image)
  elif mode == 'P':
    inv_image = invert_color_p(image)
  else:
    inv_image = ImageChops.invert(image)
  inv_image.save(dest_image)
  log('color inversion finished')


def invert_channel_rgb(image, channel):
  red, green, blue = image.split()[0:3]
  if channel == 'red':
    inv_channel = ImageChops.invert(red)
    inv_image = Image.merge('RGB', [inv_channel, green, blue])
  if channel == 'green':
    inv_channel = ImageChops.invert(green)
    inv_image = Image.merge('RGB', [red, inv_channel, blue])
  if channel == 'blue':
    inv_channel = ImageChops.invert(blue)
    inv_image = Image.merge('RGB', [red, green, inv_channel])
  return inv_image


def invert_channel_rgba(image, channel):
  alpha = image.getchannel('A')
  image = image.convert('RGB')
  inv_image = invert_channel_rgb(image, channel)
  inv_image.putalpha(alpha)
  return inv_image


def invert_channel(path, image, mode, channel):
  log(channel + ' channel inversion started')
  root, extension = os.path.splitext(path)
  suffix = '_inv_' + channel
  dest_image = root + suffix + extension
  log('destination: \'' + dest_image + '\'')
  if os.path.isfile(dest_image) is True:
    log('destination file already exists')
    if overwrite == True:
      pass
    else:
      message = '\033[31mWARNING:\033[0m Existing file will be overwritten.\nType yes to continue or Ctrl+c to cancel: '
      confirm = ask_user(message)
      while confirm != "yes":
        confirm = ask_user(message)
  log('format: ' + image.format.lower())
  if mode == 'RGBA':
    inv_image = invert_channel_rgba(image, channel)
  elif mode == 'RGB':
    inv_image = invert_channel_rgb(image, channel)
  elif mode == 'L' or mode == 'LA':
    log(path + ' doesn\'t have RGB channels.')
    print(path + ' doesn\'t have RGB channels.')
    return
  elif mode == 'P' or mode == 'PA':
    log('inverting RGB channels of palettised images is not supported.')
    print('Inverting RGB channels of palettised images is not supported.')
    return
  else:
    log('can\'t invert channel. Unsupported image mode \'' + mode + '\'.')
    print('Can\'t invert channel. Unsupported image mode \'' + mode + '\'.')
    return
  inv_image.save(dest_image)
  log(channel + ' channel inversion finished')


def main():
  '''Inverts colors, or red, or green, or red channel of a given image.
  Supported formats are .PNG. JPG and .TGA
  Any other format may or may not work but you are free to try.'''
  parser = argparse.ArgumentParser(description='Inverts colors or a color channel of an image.')
  required = parser.add_argument_group('required arguments')
  exclusive = parser.add_mutually_exclusive_group()
  optional = parser.add_argument_group('optional arguments')
  required.add_argument('-s', metavar='<src>', required=True, help='<src> image', type=str) #Source image path
  exclusive.add_argument('-c', help='Inverts color', action='store_true') #Flag to invert color
  exclusive.add_argument('-r', help='Inverts red channel', action='store_true') #Invert red channel
  exclusive.add_argument('-g', help='Inverts green channel', action='store_true') #Invert green channel
  exclusive.add_argument('-b', help='Inverts blue channel', action='store_true') #Invert blue channel
  optional.add_argument('-y', help='Overwrite existing file', action='store_true') #Overwrites the output file if it exists
  optional.add_argument('-l', help='Produces a log file', action='store_true') #Log file creation flag
  # TODO: Destination folder
  args = parser.parse_args()
  global overwrite
  if args.y == True:
    overwrite = True
  else:
    overwrite = False
  global logging
  if args.l == True:
    logging = True
  else:
    logging = False
  log('conversion started')
  if True not in [args.c, args.r, args.g, args.b]: #Exits graciously if no conversion argument has been passed
    log('no conversion arguments. Nothing to do')
    exit()
  if os.path.isfile(args.s) != True: #Exits graciously if file doesn't exist
    log('file does not exist')
    exit()
  log('source: \'' + str(args.s) + '\'')
  image = Image.open(args.s)
  format = image.format
  log('format: ' + format)
  mode = image.mode
  log('mode: ' + mode)
  if args.c == True:
    invert_color(args.s, image, mode)
  elif args.r == True:
    invert_channel(args.s, image, mode, 'red')
  elif args.g == True:
    invert_channel(args.s, image, mode, 'green')
  elif args.b == True:
    invert_channel(args.s, image, mode, 'blue')
  log('conversion finished')


if __name__ == '__main__':
  main()
