from dragonfly import (Grammar, Dictation, Context, MappingRule, Pause, IntegerRef)
from proxy_nicknames import Key, Text, Events, AppRegexContext

from raul import SelfChoice, processDictation, NUMBERS as numbers

import aenea

mac_context = aenea.global_context
grammar = Grammar("mac", context=mac_context)

submit = Events("key--code=36")
clear = Events("key--code=51&modifier=command")

class MacCommand(MappingRule):
    mapping = {
        # Text entry/manipulation
        "submit": submit,
        "clear": clear,
        #"dip": Events("key--code=51"),
        #"dap [<n>]": Events("key--code=51&modifier=option&times=%(n)d"),
        # Window Movement/manipulation
        "left screen [<n>]": Events("key--code=123&modifier=control&times=%(n)d"),
        "right screen[<n>]": Events("key--code=124&modifier=control&times=%(n)d"),
        "up": Events("key--code=126"),
        "down": Events("key--code=125"),
        "left": Events("key--code=123"),
        "right": Events("key--code=124")
    }
    extras = [Dictation("text"), IntegerRef("n", 1, 10)]
    defaults = {"n":1}

grammar.add_rule(MacCommand())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
