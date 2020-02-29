#!/usr/bin/env python3
import pytest
from summarizer import Summarizer
from os import path 
import json

def test_run():
    if path.exists("keys"):
      api = Summarizer("Manchester","manchester","keys")
      assert api.keyToVideo() == 0
    else:
      with open("data.json","r") as f:
        return json.load(f)
