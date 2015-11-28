import unittest

import taxonomy

class TestTaxonomyFunction(unittest.TestCase):

  def test_noPuncuation(self):
      real = 'some string'
      test = 's!o@,m$e%% s^&*t(r):;i,.n\'\"g<>.,'
      res = taxonomy.noPuncuation(test)
      self.assertEqual(res, real)

if __name__ == '__main__':
    unittest.main()
