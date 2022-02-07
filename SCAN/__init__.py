"""Scan Records"""
import hashlib
import logging
from dataclasses import asdict, astuple, dataclass, fields
from pathlib import Path as P
from shutil import copyfile

import arrow as A
import numpy as np
