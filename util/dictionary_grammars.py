DIGITS = ["zero", "one", "to", "3", "for", "5", "6", "7", "8", "nine"]
DIGITS = dict(zip(DIGITS, (chr(ord("0") + i) for i in range(10))))
DIGITS["niner"] = "9"
DIGITS["ate"] = "8"
DIGITS["won"] = "1"
