#!/usr/bin/env python
# vim: set fileencoding=utf-8 :
# Laurent El Shafey <Laurent.El-Shafey@idiap.ch>

"""Features for face recognition"""

import numpy
import math
import bob
from .. import utils

from .Extractor import Extractor

class DCTBlocks (Extractor):

  """Extracts DCT blocks"""
  def __init__(
      self,
      block_size = 12,    # 1 or two parameters for block size
      block_overlap = 11, # 1 or two parameters for block overlap
      number_of_dct_coefficients = 45,
      normalize_blocks = True,
      normalize_dcts = True,
      auto_reduce_coefficients = False
  ):

    # call base class constructor
    Extractor.__init__(
        self,

        block_size = block_size,
        block_overlap = block_overlap,
        number_of_dct_coefficients = number_of_dct_coefficients,
        normalize_blocks = normalize_blocks,
        normalize_dcts = normalize_dcts,
        auto_reduce_coefficients = auto_reduce_coefficients
    )

    # block parameters
    self.m_block_size = block_size if isinstance(block_size, (tuple, list)) else (block_size, block_size)
    self.m_block_overlap = block_overlap if isinstance(block_overlap, (tuple, list)) else (block_overlap, block_overlap)
    self.m_number_of_dct_coefficients = number_of_dct_coefficients
    self.norm_block = normalize_blocks
    self.norm_dct = normalize_dcts
    if self.m_block_size[0] < self.m_block_overlap[0] or self.m_block_size[1] < self.m_block_overlap[1]:
      raise ValueError("The overlap '%s' is bigger than the block size '%s'. This won't work. Please check your setup!"%(self.m_block_overlap, self.m_block_size))
    if self.m_block_size[0] * self.m_block_size[1] <= self.m_number_of_dct_coefficients:
      if auto_reduce_coefficients:
        self.m_number_of_dct_coefficients = self.m_block_size[0] * self.m_block_size[1] - 1
      else:
        raise ValueError("You selected more coefficients %d than your blocks have %d. This won't work. Please check your setup!"%(self.m_number_of_dct_coefficients, self.m_block_size[0] * self.m_block_size[1]))

  def __call__(self, image):
    """Computes and returns DCT blocks for the given input image"""

    # Initializes cropper and destination array
    extractor = bob.ip.DCTFeatures(self.m_block_size[0], self.m_block_size[1], self.m_block_overlap[0], self.m_block_overlap[1], self.m_number_of_dct_coefficients, self.norm_block, self.norm_dct)

    # Computes DCT features
    return extractor(image)


class DCTBlocksVideo(DCTBlocks):

  def __init__(self, **kwargs):
    # call base class constructor with its required parameters
    DCTBlocks.__init__(self, **kwargs)


  def read_feature(self, filename):
    """Read video.FrameContainer containing features extracted from each frame"""
    return utils.video.FrameContainer(str(filename))


  def __call__(self, frame_container):
    """Returns local DCT features computed from each frame in the input video.FrameContainer"""

    output_frame_container = utils.video.FrameContainer()
    for (frame_id, image, quality) in frame_container.frames():
      frame_dcts = DCTBlocks._dct_features(self,image)
      output_frame_container.add_frame(frame_id,frame_dcts,quality)

    return output_frame_container

