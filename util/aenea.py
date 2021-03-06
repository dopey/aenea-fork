from dragonfly import AppContext
from proxy_contexts import AlwaysContext
from dragonfly import *
from proxy_nicknames import Text, Key
import os, shutil

global_context = AppContext(executable="notepad")

class DigitalInteger(Repetition):
  digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
  child = Choice("digit", dict(zip(digits, digits)))

  def __init__(self, name, min, max, *args, **kw):
    Repetition.__init__(self, self.child, min, max, name=name, *args, **kw)

  def value(self, node):
    return int("".join(Repetition.value(self, node)))

def Nested(command):
  return Text(command) + Key("Left:%i" % (len(command) / 2))

# TODO: clean up and generalize
def reload_aenea_configuration():
  for name in os.listdir("E:\\aenea\\grammar"):
    if name.endswith(".py"):
      with open("E:\\aenea\\grammar\\%s" % name) as infd:
        with open("C:\\NatLink\\NatLink\\MacroSystem\\_%s" % name, "w") as outfd:
          outfd.write(infd.read())
  for name in os.listdir("E:\\aenea\\util"):
    full_src = "E:\\aenea\\util\\" + name
    if name.endswith(".py") or name.endswith(".txt"):
      with open("E:\\aenea\\util\\%s" % name) as infd:
        with open("C:\\NatLink\\NatLink\\MacroSystem\\%s" % name, "w") as outfd:
          outfd.write(infd.read())
    if os.path.isdir(full_src) and os.path.exists("%s\\__init__.py" % full_src):
      try:
        assert name != ""
        shutil.rmtree("C:\\NatLink\\NatLink\\MacroSystem\\%s" % name)
      except Exception:
        pass
      shutil.copytree(full_src, "C:\\NatLink\\NatLink\\MacroSystem\\%s" % name)
