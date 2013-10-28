from dragonfly import (Grammar, Dictation, Context, MappingRule, Pause)
from proxy_nicknames import Key, Text, Events, AppRegexContext

from raul import SelfChoice, processDictation, NUMBERS as numbers

from _mac import *

import aenea

alfred_context = aenea.global_context
grammar = Grammar("alfred", context=alfred_context)

class AlfredCommand(MappingRule):
    mapping = {
        "open web":Events("key--code=49&modifier=control") + Pause("20") + Events("text--chrome") + submit,
        "open talk":Events("key--code=49&modifier=control") + Pause("20") + Events("text--adium") + submit,
        "open [<text>]":Events("key--code=49&modifier=control") + Pause("20") + Events("text--%(text)s"),
    }
    extras = [Dictation("text")]
    defaults = {"text":"", "n":1}

grammar.add_rule(AlfredCommand())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
