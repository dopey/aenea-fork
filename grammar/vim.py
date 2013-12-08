from dragonfly import Config, Section, Item, MappingRule, CompoundRule, Grammar, IntegerRef, Dictation, RuleRef, Alternative, Repetition, Literal, Sequence
import natlink, os, time

from proxy_nicknames import Key, Text, AppRegexContext, Events

from dictionary_grammars import DIGITS, SYMBOLS, ALPHABET, CASE_ALPHABET

from _mac import FormatRule

import aenea

escape = Key("Escape")

vim_context = aenea.global_context & AppRegexContext(name="iTerm")


grammar = Grammar("vim", context=vim_context)
escape = Events("key->key=escape")
save = escape + Events("text->:w\n")
_zip = Events("key->key=z&times=2")
jump = Events("number->%(text)s&modifiers=text;key->key=g&times=2") + _zip
finish = Events("key->key=4&modifier=shift")
match = Events("key->key=5&modifier=shift")
submit = Events("key->code=36")



def strip_number(words):
    '''remove trailing number that dictation sometimes adds'''
    return map((lambda word: word.split('\\')[0]), words)


class VimMovement(MappingRule):
  mapping = {
    #JUMP TO LINE
    "jump <text>": escape + jump,
    "jump <text> finish match": escape + jump + finish + match,
    #JUMP BACK
    "bump": Events("key->code=31&modifier=control"),
    #RIGHT
    "will [<n>]": Events("key->code=13&times=%(n)d"),
    "wall [<n>]": Events("key->code=13&modifier=shift&times=%(n)d"),
    "start": Events("key->key=6&modifier=shift"),
    #LEFT
    "bill [<n>]": Events("key->code=11&times=%(n)d"),
    "ball [<n>]": Events("key->code=11&modifier=shift&times=%(n)d"),
    "finish": finish,
    "finish match": finish + match,
    #UP
    "vim up [<n>]": Events("key->key=k&times=%(n)d"),
    "graph up [<n>]": Events("key->key=[&modifier=shift&times=%(n)d") + _zip,
    "page up [<n>]": Events("key->key=u&modifier=control&times=%(n)d") + _zip,
    "top": Events("key->code=5&times=2"),
    #DOWN
    "vim down [<n>]": Events("key->key=j&times=%(n)d"),
    "graph down [<n>]": Events("key->key=]&modifier=shift&times=%(n)d") + _zip,
    "page down [<n>]": Events("key->key=d&modifier=control&times=%(n)d") + _zip,
    "bottom": Events("key->code=5&modifier=shift"),

    #CENTER
    #------------------#
    "zip": _zip,

    #NEXT
    #------------------#
    "next [<n>]": Events("key->key=n&times=%(n)d"),
    "previous [<n>]": Events("key->key=n&modifier=shift&times=%(n)d"),
    "repeat": Events("key->key=.") + save,
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 100)]
  defaults = {"n":1, "text": ""}

class VimTextManipulation(MappingRule):
  mapping = {
    "undo": escape + Events("key->key=u") + save,
    "redo": Events("key->code=15&modifier=control") + save,

    #DELETION
    #------------------#
    #Command Mode
    "cut [<n>]": Events("number->%(n)d;key->code=7") + save,
    #Insert Mode
    "sip [<n>]": Events("number->%(n)d;key->key=s"),
    #------------------#

    #DELETE line(s)
    #------------------#
    "delete [<n>]": escape + Events("number->%(n)d;key->key=d&times=2") + save,
    "delete above [<n>]": escape + Events("key->code=126&times=%(n)d;number->%(n)d;key->key=d&times=2") + save,
    "delete below [<n>]": escape + Events("key->code=125;number->%(n)d;key->key=d&times=2") + save,
    "delete line [<text>]": escape + jump + Events("number->%(n)d;key->key=d&times=2") + save,
    #Insert Mode"
    "chop": escape + Events("key->key=c&times=2"),
    "chop line [<text>]": escape + jump + Events("key->key=c&times=2"),
    #------------------#

    #INSERTION
    #---------------------#
    #Current Position
    "after": Events("key->key=a"),
    #End of Line
    "laughter": escape + Events("key->key=a&modifier=shift"),
    #---------------------#

    #Add line
    #---------------------#
    #above
    "add above": escape + Events("key->key=o&modifier=shift") + escape + Events("key->key=j") + save,
    "add above line [<text>]": escape + jump + Events("key->key=o&modifier=shift") + escape + Events("key->key=j") + save,
    #below
    "add below": escape + Events("key->key=o") + escape + Events("key->key=k") + save,
    "add below line [<text>]": escape + jump + Events("key->key=o") + escape + Events("key->key=k") + save,
    #---------------------#

    #Add line for insertion
    #---------------------#
    #above
    "open above": escape + Events("key->key=o&modifier=shift"),
    #below
    "open below": escape + Events("key->key=o"),
    #open below specific
    "open below <text>": escape + jump + Events("key->key=o"),
    #---------------------#

    #COPY
    #---------------------#
    "copy [<n>]": Events("number->%(n)d;key->key=y&times=2"),
    "copy line [<text>]": jump + Events("key->key=y&times=2"),
    "from [<text>] copy [<n>]": jump + Events("number->%(n)d;key->key=y&times=2"),
    "from [<text>] copy jump [<text2>]": jump + Events("key->key=v&modifier=shift") + Events("number->%(text2)s&modifiers=text;key->key=g&times=2") + Events("key->key=y"),
    "from [<text>] delete [<n>]": jump + Events("number->%(n)d;key->key=d&times=2") + save,
    "from [<text>] delete jump [<text2>]": jump + Events("key->key=v&modifier=shift") + Events("number->%(text2)s&modifiers=text;key->key=g&times=2") + Events("key->key=x") + save,
    "from [<text>] replace [<n>]": jump + Events("key->key=v&modifier=shift;key->code=125&times=%(n)d;key->code=126") + Events("key->key=p"),

    #---------------------#

    #PASTE
    #---------------------#
    "paste": Events("key->code=35"),
    "paste below [<text>]": jump + Events("key->key=p"),
    "replace line [<text>]": jump + Events("key->key=v&modifier=shift") + Events("key->key=p"),
    "pasta": Events("key->code=35&modifier=shift"),
    "select pasted": Events("text->gp"),

    #SQUISH lines
    #---------------------#
    "squish": Events("key->key=j&modifier=shift"),

    #SEARCH
    #---------------------#
    #"search pause": Events("key->key=/"),
    #"search [<text>]": Events("key->key=/;text->%(text)s&modifiers=lower") + submit,

    #SNIPPET
    #---------------------#
    "snip [<text>]": Events("text->%(text)s;key->key=tab"),

    #ALL TEXT
    #---------------------#
    "[<text>]": Events("text->%(text)s&modifiers=lower")
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 50), Dictation("text2")]
  defaults = {"n":1, "text":"", "text2":""}

class VimCommand(MappingRule):
  mapping = {
    "cape": escape,
    "save": save,
    "quit": Events("key->key=escape;key->code=41&modifier=shift;key->key=q;key->key=return"),
    "insert": Events("key->key=i")
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 10)]
  defaults = {"n":1}

class VimVisual(MappingRule):
  mapping = {
    "visual line": Events("key->key=v&modifier=shift"),
    "visual block": Events("key->key=v&modifier=control")
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 10)]
  defaults = {"n":1}

class VimBuffer(MappingRule):
  mapping = {
    "buff left [<n>]": Events("key->key=h&modifier=control&times=%(n)d"),
    "buff right [<n>]": Events("key->key=l&modifier=control&times=%(n)d"),
    "fuzzy buff [<text>]": Events("key->key=p&modifier=control;text->%(text)s&modifiers=first"),
    "vertical": Events("key->key=v&modifier=control")
  }
  extras = [Dictation("text"), IntegerRef("n", 1, 10)]
  defaults = {"n":1, "text":""}



alphabet_rule = Sequence([Repetition(RuleRef(name="x", rule=MappingRule(name="t", mapping=ALPHABET)), min=1, max=20)])
case_alphabet_rule = Sequence([Repetition(RuleRef(name="w", rule=MappingRule(name="s", mapping=CASE_ALPHABET)), min=1, max=20)])
numbers_rule = Sequence([Repetition(RuleRef(name="y", rule=MappingRule(name="u", mapping=DIGITS)), min=1, max=20)])
symbols_rule = Sequence([Repetition(RuleRef(name="z", rule=MappingRule(name="v", mapping=SYMBOLS)), min=1, max=20)])
alphanumeric = [case_alphabet_rule, alphabet_rule, numbers_rule, symbols_rule]

class FindRule(CompoundRule):
    spec = ("[clip | dip | visual] (bind | find | tail | bale) <alphanumeric> [<n>]")
    extras = [IntegerRef("n", 1, 10), Alternative(alphanumeric, name="alphanumeric")]
    defaults = {"n": 1}

    def value(self, node, extras):
        words = node.words()
        times = extras["n"]

        if words[0] == 'clip':
            initial_action = Events('key->key=c')
            rule = words[1]
        elif words[0] == 'dip':
            initial_action = Events('key->key=c')
            rule = words[1]
        elif words[0] == 'visual':
            initial_action = Events('key->key=c')
            rule = words[1]
        else:
            initial_action = Events('text->')
            rule = words[0]

        print words
        print "Times: %d" % times


        find = escape + initial_action + Events('key->key=%d;key->key=f' % times)
        bind = escape + initial_action + Events('key->key=%d;key->key=f&modifier=shift' % times)
        bale = escape + initial_action + Events('key->key=%d;key->key=t&modifier=shift' % times)
        tail = escape + initial_action + Events('key->key=%d;key->key=t' % times)

        search = extras["alphanumeric"][0][0]
        if rule == 'bind':
            return (bind + search)
        elif rule == 'find':
            return (find + search)
        elif rule == 'bale':
            return (bale + search)
        elif rule == 'tail':
            return (tail + search)

    def _process_recognition(self, node, extras):
        self.value(node, extras).execute()

find_rule = RuleRef(name="find_rule", rule=FindRule(name="i"))
format_rule = RuleRef(name="format_rule", rule=FormatRule(name="k"))


## Here we define a rule that will allow us to cut or delete to specific places in a line
class ClipRule(CompoundRule):
    spec = ("(visual | clip | dip) <alphanumeric> [<format_rule>] [copy | delete | paste]")
    extras = [Alternative(alphanumeric, name="alphanumeric"), format_rule]

    def _process_recognition(self, node, extras):
        words = node.words()
        symbol = extras['alphanumeric'][0][0]

        print words
        print extras

        if words[0] == 'clip':
            if extras['format_rule']:
                (Events('key->key=c') + symbol + extras['format_rule']).execute()
            else:
                (Events('key->key=c') + symbol).execute()
        elif words[0] == 'dip':
            (Events('key->key=d') + symbol + save).execute()
        elif words[0] == 'visual':
            events = Events('key->key=v') + symbol
            if words[-1] == 'copy':
                events += Events('key->key=y')
            if words[-1] == 'paste':
                events += Events('key->key=p')
            if words[-1] == 'delete':
                events += Events('key->key=x')
            events.execute()


class ReplaceRule(CompoundRule):
    spec = ("change <alphanumeric>")
    extras = [Alternative(alphanumeric, name="alphanumeric")]

    def _process_recognition(self, node, extras):
        words = node.words()
        print words
        action = Events('key->key=r')
        change = extras['alphanumeric'][0][0]

        (action + change + save).execute()


class SearchRule(CompoundRule):
    spec = ("search [<format_rule>] [ <dictation>]")
    extras = [Dictation(name="dictation"), format_rule]

    def _process_recognition(self, node, extras):
        words = node.words()
        print words
        print extras

        search = Events('key->key=/')

        if len(words) == 1:
            action = search
        else:
            if 'format_rule' in extras:
                action = search + extras['format_rule'] + submit
            else:
                search_string = 'text->' + ' '.join(words[1:])
                print search_string
                action = search + Events(search_string) + submit

        action.execute()


class RepeatRule(CompoundRule):
    spec = ("repeat next [<n>]")
    extras = [IntegerRef("n", 1, 100)]
    defaults = {"n":1}

    def _process_recognition(self, node, extras):
        words = node.words()
        print words
        times = extras['n']
        for i in xrange(times):
            Events("key->key=n;key->key=.").execute()

        save.execute()


class MacroRule(CompoundRule):
    spec = ("macro <alphanumeric> [<n>]")
    extras = [Alternative(alphanumeric, name="alphanumeric"), IntegerRef("n", 1, 100)]
    defaults = {"n":1}

    def _process_recognition(self, node, extras):
        words = node.words()
        print words

        times = Events('key->key=%d' % extras['n'])
        action = Events('key->key=2&modifier=shift')
        symbol = extras['alphanumeric'][0][0]

        (times + action + symbol + save).execute()

grammar.add_rule(VimMovement())
grammar.add_rule(VimTextManipulation())
grammar.add_rule(VimCommand())
grammar.add_rule(VimVisual())
grammar.add_rule(VimBuffer())
grammar.add_rule(FindRule())
grammar.add_rule(ClipRule())
grammar.add_rule(ReplaceRule())
grammar.add_rule(RepeatRule())
grammar.add_rule(MacroRule())
grammar.add_rule(SearchRule())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
