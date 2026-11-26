class Kiosk:
  def redeem(self, user, gift):
    if gift.stock <= 0:              # R7: nothing left to give
      return False

    if user.isValid():
      if user.points >= gift.points:
        confirm = input(f'Redeem {gift.name} for {gift.points} points?')
        if confirm.strip().lower() == "yes":
          # R5: take the points and update the record
          user.points -= gift.points
          user.update()
          gift.stock -= 1            # R7: one fewer on the shelf
          return True

    return False
