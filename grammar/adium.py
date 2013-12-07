from dragonfly import (Grammar, Dictation, Context, MappingRule, Pause)
from proxy_nicknames import Key, Text, Events, AppRegexContext

from raul import SelfChoice, processDictation, NUMBERS as numbers

from _mac import *

import aenea

adium_context = aenea.global_context & AppRegexContext(name="Adium")
grammar = Grammar("adium", context=adium_context)

class AlfredCommand(MappingRule):
    mapping = {
        "search": Events("key->code=44&modifier=command"),
        "[<text>]": Events("text->%(text)s")
    }
    extras = [Dictation("text")]
    defaults = {"text":"", "n":1}

grammar.add_rule(AlfredCommand())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None

