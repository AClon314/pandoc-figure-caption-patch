#!/bin/env python
import os
from typing import Sequence
import panflute as pan
DEBUG = os.environ.get("DEBUG", None)
if DEBUG:
    def Log(*args, **kwargs):
        """Same as print, but prints to stderr (which is not intercepted by Pandoc)."""
        pan.debug(*args, **kwargs)
else:
    Log = lambda *args, **kwargs: None


def _overflow(text: str, half_len=128): return text if len(text) < half_len * 2 else text[:half_len] + '...' + text[-half_len:]


def get_siblings(elem: pan.Element) -> tuple[Sequence[pan.Element], int]:
    """
    Get the siblings of an element, and its index in the siblings list.
    Returns:
      (siblings, index)
    elem.parent.content[elem.parent.index(elem)+offset]
    """
    parent = elem.parent
    if not parent or not hasattr(parent, 'content'):
        raise ValueError(f'Element {elem} has no parent or content')
    siblings = parent.content
    index: int = siblings.index(elem)
    return siblings, index
