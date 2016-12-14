import unittest
import telegram
from bot import findBestPlayerID

class TestBot(unittest.TestCase):
	def tearDown(self):
		self.theBot = None
		pass

	def testBestPlayerID(self):
		arrivals = {}
		arrivals['1'] = 4
		arrivals['2'] = 5
		arrivals['3'] = 1
		arrivals['4'] = 12

		self.assertEqual(findBestPlayerID(arrivals), '3')

if __name__ == '__main__':
    unittest.main()