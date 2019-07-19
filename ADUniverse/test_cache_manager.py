"""Tests for the Cache Manager."""

import constants as cn
import cache_manager

import unittest



class TestCacheManager(unittest.TestCase):

  def setUp(self):
    self.manager = cache_manager.CacheManager(cn.CACHETEST_URL,
        filename="cachetest.zip")

  def testConstructor(self):
    self.assertGreater(len(self.manager.url), 0)

  def testGet(self):
    self.manager.get()
    import pdb; pdb.set_trace()
    


if __name__ == '__main__':
    unittest.main()
