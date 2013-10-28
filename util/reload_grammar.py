import os


def reload_grammar():
  for name in os.listdir("Z:\\aenea\\grammar"):
    if name.endswith(".py"):
      with open("Z:\\aenea\\grammar\\%s" % name) as infd:
        with open("C:\\NatLink\\NatLink\\MacroSystem\\_%s" % name, "w") as outfd:
          outfd.write(infd.read())


if __name__ == '__main__':
    reload_grammar()
