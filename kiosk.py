class Kiosk:
  def redeem(self, user, gift):
    if user.isValid():
      if user.points >= gift.points:
        confirm = input(f'Redeem {gift.name} for {gift.points} points?')
        if confirm == "yes":
          # R5: take the points and update the record
          user.points -= gift.points
          user.update()
          return True

    return False
