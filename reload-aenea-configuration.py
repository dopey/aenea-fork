import os

for name in os.listdir("Z:\\aenea\\grammar"):
  if name.endswith(".py"):
    with open("Z:\\aenea\\grammar\\%s" % name) as infd:
      with open("C:\\NatLink\\NatLink\\MacroSystem\\_%s" % name, "w") as outfd:
        outfd.write(infd.read())
for name in os.listdir("Z:\\aenea\\util"):
  if name.endswith(".py"):
    with open("Z:\\aenea\\util\\%s" % name) as infd:
      with open("C:\\NatLink\\NatLink\\MacroSystem\\%s" % name, "w") as outfd:
        outfd.write(infd.read())
