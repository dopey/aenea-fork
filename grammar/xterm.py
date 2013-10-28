from dragonfly import (Grammar, Dictation, Context, MappingRule, Pause)
from proxy_nicknames import Key, Text, Events, AppRegexContext

from raul import SelfChoice, processDictation, NUMBERS as numbers

import aenea


xterm_context = aenea.global_context & AppRegexContext(name="xterm")
grammar = Grammar("xterm", context=xterm_context)

class ItermCommand(MappingRule):
    mapping = {
        "dear": Events("text--cd\n"),
        "dear work": Events("text--cd $WORK\n"),
        "dear games": Events("text--cd $GAMES\n"),
        "dear grammar": Events("text--cd $GRAMMAR\n"),
        "dear back": Events("text--cd ../\n"),
        "dear [<text>]": Events("text--cd %(text)s"),
        "list": Events("text--ls -la\n"),
        "v [<text>]": Events("text--vi %(text)s\n"),
        "left tab": Events("key--code=123&modifier=command"),
        "right tab": Events("key--code=124&modifier=command")
    }
    extras = [Dictation("text")]
    defaults = {"text":"", "number":1}

grammar.add_rule(ItermCommand())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
