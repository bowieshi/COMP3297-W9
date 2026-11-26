# Gift kiosk — what the canteen asked for

Members of the canteen loyalty scheme collect points and swap them for gifts
at a self-service kiosk.

R1  Only a VALID user may redeem.
R2  A user may redeem when their points are AT LEAST the gift's cost.
R3  The kiosk asks the user to confirm BEFORE taking any points.
R4  Only the answer "yes" confirms. Anything else cancels.
R5  On success the points are reduced by the cost, and the user record is
    updated.
R6  In every other case nothing changes and the kiosk reports failure.

That is the whole brief. Anything not written here has not been asked for.
