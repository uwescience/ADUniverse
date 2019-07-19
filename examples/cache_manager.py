"""Manage Caching of External Files."""

import constants as cn

import os
import urllib3
import zipfile


README_FILE = "README.md"

class CacheManager(object):

  def __init__(self, url, filename=None):
    """
    :param str url: URL to retrieve
    :param str filename: name of the file to create
    """
    self.url = url
    if filename is None:
      self.filename = url.split('/')[-1]
    else:
      self.filename = filename
    self.path = self._makePath(self.filename)

  def _makePath(self, filename):
    return os.path.join(cn.DATACACHE_DIR, filename)

  def get(self):
    """
    Retreives the file into the datacache if it is not present.
    """
    if os.path.isfile(self.path):
      return
    # Retrive the file
    http = urllib3.PoolManager()
    request = http.request('GET', self.url)
    with open(self.path, "wb") as fd:
      fd.write(request.data)
    # Handle zipfiles
    try:
      zip_object = zipfile.ZipFile(self.path)
      rc = zip_object.testzip()
      with zipfile.ZipFile(path_to_zip_file, 'r') as zip_ref:
        zip_ref.extractall(cn.DATACACHE_DIR)
    except:
      pass
    import pdb; pdb.set_trace()

  def flush(self):
    """
    Removes all files from the cache
    """
    for filename in os.listdir(cn.DATACACHE_DIR):
      if filename != README_FILE:
        path = self._makePath(filename)
        os.remove(path)
