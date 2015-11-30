import os
import unittest

import taxonomy

class TestTaxonomyFunction(unittest.TestCase):

  def test_noPuncuation(self):
      real = 'some string'
      test = 's!o@,m$e%% s^&*t(r):;i,.n\'\"g<>.,'
      res = taxonomy.noPuncuation(test)
      self.assertEqual(res, real)

  def test_sanitize(self):
      real = 'some string'
      test = 'S!O@,M$E%% S^&*T(R):;I,.N\'\"G<>.,'
      res = taxonomy.sanitize(test)
      self.assertEqual(res, real)

  def test_outdir(self):
      real = os.path.join('out', 'fileName')
      test = 'fileName'
      res = taxonomy.outdir(test)
      self.assertEqual(res, real)

if __name__ == '__main__':
    unittest.main()
