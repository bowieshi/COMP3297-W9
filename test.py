import unittest
import io, sys
from user import User
from gift import Gift
from kiosk import Kiosk

# How many of this gift the canteen has on the shelf.
MYSTOCK = 25

class TestUser(unittest.TestCase):
  def testUser(self):
    user = User('056B15E3247C81', '2024-04-01', 100)
    self.assertEqual(user.userID, '056B15E3247C81')
    self.assertEqual(user.points, 100)
    self.assertEqual(user.joinDate, '2024-04-01')

class TestGift(unittest.TestCase):
  def testGift(self):
    gift = Gift('ruler', 25)
    self.assertEqual(gift.name, 'ruler')
    self.assertEqual(gift.points, 25)

# A stand-in for User. The kiosk only ever reads .points and calls
# .isValid() and .update(), so anything with those three will do.
class FakeUser:
  def __init__(self, points, valid=True):
    self.points = points
    self.valid = valid
    self.saved = False        # records that update() was called

  def isValid(self):
    return self.valid

  def update(self):
    self.saved = True

class TestKiosk(unittest.TestCase):
  def setUp(self):
    self.realStdin = sys.stdin      # remember the keyboard

  def tearDown(self):
    sys.stdin = self.realStdin      # and always put it back

  def answer(self, text):
    sys.stdin = io.StringIO(text + '\n')

  # R2, R5 - enough points, and the user says yes.
  def testRedeem(self):
    self.answer('yes')
    user = FakeUser(100)
    result = Kiosk().redeem(user, Gift('ruler', 25))
    self.assertTrue(result)
    self.assertEqual(user.points, 75)
    self.assertTrue(user.saved)

  # R1, R6 - an invalid user is refused and nothing changes.
  def testRedeemInvalid(self):
    self.answer('yes')
    user = FakeUser(100, valid=False)
    result = Kiosk().redeem(user, Gift('ruler', 25))
    self.assertFalse(result)
    self.assertEqual(user.points, 100)
    self.assertFalse(user.saved)

  # R2, R6 - not enough points: refused, and nothing changes.
  def testNotEnoughPoints(self):
    self.answer('yes')
    user = FakeUser(10)
    result = Kiosk().redeem(user, Gift('ruler', 25))
    self.assertFalse(result)
    self.assertEqual(user.points, 10)
    self.assertFalse(user.saved)

  # R3, R4, R6 - the user says no: nothing is taken.
  def testAnswerIsNotYes(self):
    self.answer('no')
    user = FakeUser(100)
    result = Kiosk().redeem(user, Gift('ruler', 25))
    self.assertFalse(result)
    self.assertEqual(user.points, 100)
    self.assertFalse(user.saved)

  # R2 - AT LEAST means exactly enough is enough.
  def testExactlyEnoughPoints(self):
    self.answer('yes')
    user = FakeUser(25)
    result = Kiosk().redeem(user, Gift('ruler', 25))
    self.assertTrue(result)
    self.assertEqual(user.points, 0)

  # R7 - no stock left: refused, and nothing changes.
  def testGiftOutOfStock(self):
    self.answer('yes')
    user = FakeUser(100)
    result = Kiosk().redeem(user, Gift('ruler', 25, stock=0))
    self.assertFalse(result)
    self.assertEqual(user.points, 100)
    self.assertFalse(user.saved)

  # R7 - a successful redemption takes one off the shelf.
  def testStockGoesDown(self):
    self.answer('yes')
    user = FakeUser(100)
    gift = Gift('ruler', 25, stock=MYSTOCK)
    Kiosk().redeem(user, gift)
    self.assertEqual(gift.stock, MYSTOCK - 1)

if __name__ == '__main__':
  unittest.main()
