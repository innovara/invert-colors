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
  image.putpalette(inv_palette)
  return image


def invert_color(path, image, format, mode):
  log('color inversion started')
  root, extension = os.path.splitext(path)
  suffix = '_invert'
  dest_image = root + suffix + extension
  log('destination: \'' + str(dest_image) + '\'')
  if os.path.isfile(dest_image) is True:
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


def invert_green_ch(image):
  log('green channel inversion started')
  log('source: \'' + str(image) + '\'')
  root, extension = os.path.splitext(image)
  suffix = '_invert_green'
  dest_image = root + suffix + extension
  log('destination: \'' + str(dest_image) + '\'')
  if os.path.isfile(dest_image) is True:
    log('destination file already exists')
    message = '\033[31mWARNING:\033[0m Existing file will be overwritten.\nType yes to continue or Ctrl+c to cancel: '
    confirm = ask_user(message)
    while confirm != "yes":
      confirm = ask_user(message)
  file_obj = Image.open(image)
  png = False
  alpha = None
  log('format: ' + file_obj.format.lower())
  if file_obj.format.lower() == 'png':
    png = True
    if len(file_obj.getbands()) == 4:
      alpha = file_obj.split()[3]
      file_obj = file_obj.convert('RGB')
  red, green, blue = file_obj.split()[0:3]
  green_inv = ImageChops.invert(green)
  inv_image = Image.merge('RGB', [red, green_inv, blue])
  #inv_image = green_ch_inv
  if png == True and alpha != None:
    inv_image.putalpha(alpha)
  inv_image.save(dest_image)
  log('green channel inversion finished')


def main():
  '''Inverts color or green channel of a given image.
  Supported formats are .PNG. JPG and .TGA
  Any other format may or may not work but you are free to try.'''
  parser = argparse.ArgumentParser(description='Inverts colors or a color channel of an image.')
  required = parser.add_argument_group('required arguments')
  exclusive = parser.add_mutually_exclusive_group()
  required.add_argument('-s', metavar='<src>', required=True, help='<src> image', type=str) #Source image path
  exclusive.add_argument('-c', help='Inverts color', action='store_true') #Flag to invert color
  exclusive.add_argument('-r', help='Inverts red channel', action='store_true') #Invert red channel
  exclusive.add_argument('-g', help='Inverts green channel', action='store_true') #Invert green channel
  exclusive.add_argument('-b', help='Inverts blue channel', action='store_true') #Invert blue channel
  parser.add_argument('-l', help='Produces a log file', action='store_true') #Log file creation flag
  args = parser.parse_args()
  global logging
  if args.l == True:
    logging = True
  else:
    logging = False
  log('conversion started')
  if args.c == False and args.g == False: #Exits graciously if no conversion argument has been passed
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
    invert_color(args.s, image, format, mode)
  elif args.g == True:
    invert_green_ch(args.s)
  log('conversion finished')


if __name__ == '__main__':
  main()
