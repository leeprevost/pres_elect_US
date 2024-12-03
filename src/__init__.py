from pathlib import Path

ROOTPATH = Path(__file__).parent.parent
ROOT = ROOTPATH.as_posix()
DB = ROOTPATH / 'db'
IMG = ROOTPATH / 'img'
DOCS = ROOTPATH / 'doc'
CACHE = DB / 'cache.h5'
