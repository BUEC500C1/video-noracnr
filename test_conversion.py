#!/usr/bin/env python3

import pytest
from summarizer import Summarizer
from os import path 

def test_run():
    existOrNot = path.exists("keys")
    if existOrNot:
      api = Summarizer("Manchester City","manchester","./keys")
      assert api.keyToVideo() == 0
    else:
      return