from dragonfly import (Grammar, Dictation, Context, MappingRule, Pause, IntegerRef)
from proxy_nicknames import Key, Text, Events, AppRegexContext

from raul import SelfChoice, processDictation, NUMBERS as numbers

import aenea

chrome_context = aenea.global_context & AppRegexContext(name="Google Chrome")
grammar = Grammar("chrome", context=chrome_context)

class ChromeCommand(MappingRule):
    mapping = {
        "new window": Events("key->code=45&modifier=command"),
        "incognito": Events("key->code=45&modifier=command&modifier=shift"),
        "new tab": Events("key->code=17&modifier=command"),
        "close tab": Events("key->code=13&modifier=command"),
        "close window": Events("key->code=13&modifier=command&modifier=shift"),
        "tab left [<n>]": Events("key->code=123&modifier=command&modifier=option&times=%(n)d"),
        "tab right [<n>]": Events("key->code=124&modifier=command&modifier=option&times=%(n)d"),
        "puke": Events("key->key=[&modifier=command"),
        "fluke": Events("key->key=]&modifier=command"),
        "address": Events("key->key=l&modifier=command"),
        "link": Events("key->key=f"),
        "downoloads": Events("key->key=j&modifier=command&modifier=shift"),
        "reload": Events("key->key=r&modifier=command"),
        "[<text>]": Events("text->%(text)s")
    }
    extras = [Dictation("text"), IntegerRef("n", 1, 10)]
    defaults = {"text":"", "n":1}

grammar.add_rule(ChromeCommand())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
