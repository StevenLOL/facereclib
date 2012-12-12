#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>
# Roy Wallace <roy.wallace@idiap.ch>

import video
import histogram
import tests
import resources
from logger import add_logger_command_line_option, set_verbosity_level, add_bob_handlers, debug, info, warn, error
from annotations import read_annotations

import os
import bob

def ensure_dir(dirname):
  """ Creates the directory dirname if it does not already exist,
      taking into account concurrent 'creation' on the grid.
      An exception is thrown if a file (rather than a directory) already
      exists. """
  bob.io.create_directories_save(dirname)


def gray_channel(image, channel = 'gray'):
  """Returns the desired channel of the given image. Currently, gray, red, green and blue channels are supported."""
  if image.ndim == 2:
    if channel != 'gray':
      raise ValueError("There is no rule to extract a " + channel + " image from a gray level image!")
    return image

  if channel == 'gray':
    return bob.ip.rgb_to_gray(image)
  if channel == 'red':
    return image[0,:,:]
  if channel == 'green':
    return image[1,:,:]
  if channel == 'blue':
    return image[2,:,:]

  raise ValueError("The image channel " + channel + " is not known or not yet implemented")

