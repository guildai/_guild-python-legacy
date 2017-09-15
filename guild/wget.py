import os
import urllib

import tqdm

import guild.util

# Code adopted from tqdm wget example:
# https://github.com/tqdm/tqdm/blob/master/examples/tqdm_wget.py

class FileDownload(tqdm.tqdm):

    def __init__(self):
        super(FileDownload, self).__init__(
            unit='B',
            unit_scale=True,
            unit_divisor=1024,
            miniters=1
        )
        
    def update(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        super(FileDownload, self).update(b * bsize - self.n)

def get_to_file(url, filename):
    guild.util.ensure_dir(os.path.dirname(filename))
    with FileDownload() as dl:
        dl.write("Downloading %s" % os.path.basename(filename))
        urllib.urlretrieve(
            url,
            filename=filename,
            reporthook=dl.update,
            data=None)
