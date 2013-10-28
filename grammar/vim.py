from dragonfly import (Grammar, CompoundRule, Choice, Dictation, List, Optional, Literal, Context, MappingRule, IntegerRef, Pause)
import natlink, os, time

from proxy_nicknames import Key, Text, AppRegexContext, Events

from comsat import ComSat

from raul import SelfChoice, processDictation, NUMBERS as numbers

from keycodes import keycodes

import aenea

LEADER_KEY = "comma"

leader = Key(LEADER_KEY)
escape = Key("Escape")
escape_leader = escape + Pause("30") + leader

vim_context = aenea.global_context & AppRegexContext(name="iTerm")


grammar = Grammar("vim", context=vim_context)

escape = Events("key--code=53")


#class EasyMotion(MappingRule):
#  mapping = {"easy jump [start] [<place>]":escape_leader + leader + Key("W") + Text("%(place)s"),
#             "easy jump end [<place>]":escape_leader + leader + Key("E") + Text("%(place)s"),
#             "easy hop [start] [<place>]":escape_leader + leader + Key("w") + Text("%(place)s"),
#             "easy hop end [<place>]":escape_leader + leader + Key("e") + Text("%(place)s"),
#             "easy leap [start] [<place>]":escape_leader + leader + Key("B") + Text("%(place)s"),
#             "easy leap end [<place>]":escape_leader + leader + Key("g, E") + Text("%(place)s"),
#             "easy bounce [start] [<place>]":escape_leader + leader + Key("b") + Text("%(place)s"),
#             "easy bounce end [<place>]":escape_leader + leader + Key("g, e") + Text("%(place)s")}
#  extras = [Dictation("place")]
#  default = {"place":""}
#
## i guess if you write a vim plugin you get to name it but i can't claim to understand these two...
#class LustyJuggler(MappingRule):
#  mapping = {"jug | juggle":escape_leader + Text("lj"),
#             "(jug | juggle) <n>":escape_leader + Key("l, j, %(n)d") + Pause("20") + Key("Return") + Pause("20") + Key("i")}
#  extras = [IntegerRef("n", 0, 10)]
#
#class LustyExplorer(MappingRule):
#  mapping = {"rusty":escape_leader + Key("l, r"),
#             "rusty absolute":escape_leader + Key("r, f"),
#             "rusty <name>":escape_leader + Key("l, r") + Text("%(name)s"),
#             "rusty absolute <name>":escape_leader + Key("l, f") + Text("%(name)s")}
#  extras = [Dictation("name")]
#
#class CommandT(MappingRule):
#  mapping = {"command tea":escape_leader + Key("t"),
#             "command tea [<text>]":escape_leader + Key("t") + Pause("20") + Text("%(text)s\n"),
#             "command tea buffer":escape + Text(":CommandTBuffer\n"),
#             "command tea buffer [<text>]":escape_leader + Key("t") + Pause("20") + Text("%(text)s\n"),
#             "command tea (tags | tag)":escape + Text(":CommandTTag\n"),
#             "command tea jump":escape + Text(":CommandTJump\n")}
#  extras = [Dictation("text")]
#
#class Fugitive(MappingRule):
#  mapping = {"git status":escape + Text(":Gstatus\n"),
#             "git commit":escape + Text(":Gcommit\n"),
#             "git diff":escape + Text(":Gdiff\n"),
#             "git move":escape + Text(":Gmove\n"),
#             "git remove":escape + Text(":Gremove\n")}
#
#class VimCommand(MappingRule):
#  mapping = {
#      "vim query [<text>]":escape + Text("/%(text)sa"),
#      "vim query back [<text>]":escape + Text("?%(text)si"),
#      "vim search":escape + Text("/\na"),
#      "vim search back":escape + Text("?\ni"),
#
#      "vim write":escape + Text(":w\na"),
#      "vim write and quit":escape + Text(":wq\na"),
#      "vim quit bang":escape + Text(":q!\na"),
#      "vim quit":escape + Text(":q\na"),
#      "vim undo [<number>]":escape + Text("%(number)dua"),
#      "vim redo":escape + Text(":redo\na"),
#      "vim [buf] close":escape + Text(":bd\na"),
#      "vim [buf] close bang":escape + Text(":bd!\na"),
#      "<number> go":escape + Text("%(number)dGa"),
#    }
#  extras = [IntegerRef("number", 1, 1000), Dictation("text")]
#  defaults = {"text":"", "number":1}

class VimMovement(MappingRule):
  mapping = {
    #JUMP TO LINE
    "jump <text>": Events("number--%(text)s&modifiers=text;key--key=g&times=2;key--key=z&times=2"),
    #JUMP BACK
    "bump": Events("key--code=31&modifier=control"),
    #RIGHT
    "rip [<n>]": Events("key--code=4&times=%(n)d"),
    "will [<n>]": Events("key--code=13&times=%(n)d"),
    "wall [<n>]": Events("key--code=13&modifier=shift&times=%(n)d"),
    "whale": Events("key--code=21&modifier=shift"),
    #LEFT
    "lip [<n>]": Events("key--code=37&times=%(n)d"),
    "bill [<n>]": Events("key--code=11&times=%(n)d"),
    "ball [<n>]": Events("key--code=11&modifier=shift&times=%(n)d"),
    "bale": Events("key--code=22&modifier=shift"),
    #UP
    "tick [<n>]": Events("key--code=40&times=%(n)d"),
    "tack [<n>]": Events("key--code=33&modifier=shift&times=%(n)d"),
    "tow [<n>]": Events("key--code=32&modifier=control&times=%(n)d"),
    "top": Events("key--code=5&times=2"),
    #DOWN
    "bit [<n>]": Events("key--code=38&times=%(n)d"),
    "bat [<n>]": Events("key--cjde=30&modifier=shift&times=%(n)d"),
    "bot [<n>]": Events("key--code=2&modifier=control&times=%(n)d"),
    "bottom": Events("key--code=5&modifier=shift"),

    #FIND on line
    #------------------#
    "find [<n>]": Events("key--key=f;number--%(n)d"),
    "find [<text>]": Events("key--key=f;key--text=%(text)s"),
    "face [<text>]": Events("key--key=f;key--text=%(text)s&modifier=shift"),
    "bind [<n>]": Events("key--key=f&modifier=shift;number--%(n)d"),
    "bind [<text>]": Events("key--key=f&modifier=shift;key--text=%(text)s"),
    "base [<text>]": Events("key--key=f&modifier=shift;key--text=%(text)s&modifier=shift"),
    #CENTER
    "zip": Events("key--code=6&times=2"),
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 1000)]
  defaults = {"n":1, "text": ""}

class VimTextManipulation(MappingRule):
  mapping = {
    "undo": escape + Events("key--code=32"),
    "redo": Events("key--code=15&modifier=control"),

    #DELETION
    #------------------#
    #Command Mode
    "cut [<n>]": Events("number--%(n)d;key--code=7"),
    #DELETE till letter
    "dip [<n>]": Events("number--%(n)d;key--key=d;key--key=f"),
    "dip [<text>]": Events("key--key=d;key--key=f;text--%(text)s&modifiers=first,lower"),
    "dip case [<text>]": Events("key--key=d;key--key=f;text--%(text)s&modifiers=first,upper"),
    #Insert Mode
    "sip": Events("key--code=1"),
    #------------------#

    #DELETE line
    #------------------#
    "dine [<n>]": Events("number--%(n)d;key--key=d&times=2"),
    #Insert Mode
    "chop": Events("key--key=&times=2"),
    #------------------#

    #CUT text into insert mode
    #------------------#
    #CUT text -> insert mode
    "chip": Events("key--code=8;key--code=14"),
    "chap": Events("key--code=8;key--code=14&modifier=shift"),
    #Cut till letter
    "clip [<n>]": Events("key--key=c;key--key=f;number--%(n)d;"),
    "clip [<text>]": Events("key--key=c;key--key=f;text--%(text)s&modifiers=first,lower"),
    "clip case [<text>]": Events("key--key=c;key--key=f;text--%(text)s&modifiers=first,upper"),
    #---------------------#

    #INSERTION
    #---------------------#
    #Current Position
    "after": Events("key--key=a"),
    #End of Line
    "laughter": Events("key--key=a&modifier=shift"),
    #---------------------#

    #Add line
    #---------------------#
    #above
    "add above": Events("key--key=o&modifier=shift") + escape + Events("key--key=j"),
    #below
    "add below": Events("key--key=o") + escape + Events("key--key=k"),
    #---------------------#

    #Add line for insertion
    #---------------------#
    #above
    "open above": Events("key--key=o&modifier=shift"),
    #below
    "open below": Events("key--key=o"),
    #---------------------#

    #NATO (letter insersion)
    #---------------------#
    "nato [<text>]": Events("text--%(text)s&modifiers=first,lower"),
    "cato [<text>]": Events("text--%(text)s&modifiers=first,upper"),
    #---------------------#

    #COPY
    #---------------------#
    "copy [<n>]": Events("number--%(n)d;key--key=y&times=2"),
    #"yoink": Events("key--code=16&times=2"),
    #---------------------#

    #PASTE
    #---------------------#
    "paste": Events("key--code=35"),
    "pasta": Events("key--code=35&modifier=shift"),
    "[<text>]": Events("text--%(text)s")


  }
  extras = [Dictation("text"), IntegerRef("n", 1, 10)]
  defaults = {"n":1, "text":""}

class VimCommand(MappingRule):
  mapping = {
    "cape": escape,
    "save": Events("key--key=escape;key--code=41&modifier=shift;key--key=w;key--key=return"),
    "kwink": Events("key--code=32"),
    "insert": Events("key--key=i")
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 10)]
  defaults = {"n":1}

class VimVisual(MappingRule):
  mapping = {
    "vine": Events("key--key=v&modifier=shift")
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 10)]
  defaults = {"n":1}

class VimBuffer(MappingRule):
  mapping = {
    "buff left [<n>]": Events("key--key=h&modifier=control&times=%(n)d"),
    "buff right [<n>]": Events("key--key=l&modifier=control&times=%(n)d")
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 10)]
  defaults = {"n":1}


#grammar.add_rule(EasyMotion())
#grammar.add_rule(VimCommand())
#grammar.add_rule(LustyJuggler())
#grammar.add_rule(LustyExplorer())
#grammar.add_rule(CommandT())
#grammar.add_rule(Fugitive())
grammar.add_rule(VimMovement())
grammar.add_rule(VimTextManipulation())
grammar.add_rule(VimCommand())
grammar.add_rule(VimVisual())
grammar.add_rule(VimBuffer())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
