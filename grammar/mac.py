from dragonfly import Config, Section, Item, MappingRule, CompoundRule, Grammar, IntegerRef, Dictation, RuleRef, Alternative, Repetition, Literal, Sequence

from proxy_nicknames import Key, Text, Events

from dictionary_grammars import DIGITS, SYMBOLS, ALPHABET, CASE_ALPHABET
import aenea



mac_context = aenea.global_context
grammar = Grammar("mac", context=mac_context)

submit = Events("key->code=36")

clear = Events("key->code=51&modifier=command")
escape = Events("key->code=53")

def Nested(command):
  return Text(command) + Events("key->code=123&times=%i" % (len(command) / 2))


class MacCommand(MappingRule):
    mapping = {
        # Text entry/manipulation
        "submit": submit,
        "clear": clear,
        # Window Movement/manipulation
        "screen left [<n>]": Events("key->code=123&modifier=control&times=%(n)d"),
        "screen right [<n>]": Events("key->code=124&modifier=control&times=%(n)d"),
        "up [<n>]": Events("key->code=126&times=%(n)d"),
        "down [<n>]": Events("key->code=125&times=%(n)d"),
        "left [<n>]": Events("key->code=123&times=%(n)d"),
        "right [<n>]": Events("key->code=124&times=%(n)d"),

        #DELETION
        #------------------#
        "dell [<n>]": Events("key->code=51&times=%(n)d"),
        "doll [<n>]": Events("key->code=51&modifier=option&times=%(n)d"),
        #------------------#
        #### Various keys
        "betable [<n>]":        Events("key->key=space&times=%(n)d"),
        "cape":             escape,

        "dribble":          Events("key->key=,;key->key=space"),
        "colon equals":     Events("key->key=space;key->code=41&modifier=shift;key->code=24;key->key=space"),
        "plus equals":      Events("key->key=space;key->code=24&modifier=shift;key->code=24;key->key=space"),
        "equals [<n>]":     Events("key->key=space;key->code=24&times=%(n)d;key->key=space"),
        "not equals [<n>]": Events("text-> !;key->code=24&times=%(n)d;key->key=space"),
        "pipes":            Events("text-> || "),
        "greater":          Events('key->key=space;key->key=.&modifier=shift;key->key=space'),
        "geek":             Events('key->key=space;key->key=.&modifier=shift;key->code=24;key->key=space'),
        "less":             Events('key->key=space;key->key=,&modifier=shift;key->key=space'),
        "leak":             Events('key->key=space;key->key=,&modifier=shift;key->code=24;key->key=space'),
        "right arrow":      Events('text->-;text->>'),
        "left arrow":      Events('text-><;text->-'),

        "plus":             Events('key->key=space;key->code=24&modifier=shift;key->key=space'),
        "minus":             Events('key->key=space;key->code=27;key->key=space'),

        "hexy lines":       Nested("{}") + Events("text->\n;key->key=escape;key->key=o&modifier=shift"),
    }

    extras = [Dictation("text"), IntegerRef("n", 1, 50)]
    defaults = {"n":1, "text":""}


alphabet_rule = Sequence([Repetition(RuleRef(name="x", rule=MappingRule(name="t", mapping=ALPHABET)), min=1, max=20)])
case_alphabet_rule = Sequence([Repetition(RuleRef(name="w", rule=MappingRule(name="s", mapping=CASE_ALPHABET)), min=1, max=20)])
numbers_rule = Sequence([Repetition(RuleRef(name="y", rule=MappingRule(name="u", mapping=DIGITS)), min=1, max=20)])
symbols_rule = Sequence([Repetition(RuleRef(name="z", rule=MappingRule(name="v", mapping=SYMBOLS)), min=1, max=20)])
alphanumeric = [case_alphabet_rule, alphabet_rule, numbers_rule, symbols_rule]


def format_snakeword(text):
  return text[0][0].upper() + text[0][1:] + ("_" if len(text) > 1 else "") + format_score(text[1:])

def format_score(text):
  return "_".join(text)

def format_camel(text):
  return text[0] + "".join([word[0].upper() + word[1:] for word in text[1:]])

def format_number(words):
    print 'FORMAT NUMBER'
    print words
    text = ''.join(words)
    text = text.replace('zero', '0')
    text = text.replace('one', '1')
    text = text.replace('to', '2')
    text = text.replace('two', '2')
    text = text.replace('three', '3')
    text = text.replace('thirty', '3')
    text = text.replace('for', '4')
    text = text.replace('four', '4')
    text = text.replace('fourty', '4')
    text = text.replace('five', '5')
    text = text.replace('six', '6')
    text = text.replace('seven', '7')
    text = text.replace('eight', '8')
    text = text.replace('ate', '8')
    text = text.replace('nine', '9')
    text = text.replace('divide', '/')
    text = text.replace('negative', '-')
    return text

def format_proper(text):
  return "".join(word.capitalize() for word in text)

def format_capword(text):
  return " ".join(word.capitalize() for word in text)

def format_caplock(text):
  return " ".join(word.upper() for word in text)

def format_relpath(text):
  return "/".join(text)

def format_abspath(text):
  return "/" + format_relpath(text)

def format_scoperesolve(text):
  return "::".join(text)

def format_jumble(text):
  return "".join(text)

def format_dots(text):
  return ".".join(text)

def format_dashes(text):
  return "-".join(text)

def format_slashes(text):
  return "/".join(text)

def format_natural(text):
  return " ".join(text)

def format_broodingnarrative(text):
  return ""

class FormatRule(CompoundRule):
    spec = ("[upper | lower] ( proper | camel | rel-path | abs-path | score | "
            "scope-resolve | jumble | dots | dashes | natural | snakeword | brooding-narrative | capword | caplock | slashes | number) [<dictation>]")

    extras = [Dictation(name="dictation")]

    def value(self, node):
        words = node.words()
        print words

        uppercase = words[0] == "upper"
        lowercase = words[0] != "lower"

        if lowercase:
            words = [word.lower() for word in words]
        if uppercase:
            words = [word.upper() for word in words]

        words = [word.split("\\", 1)[0].replace("-", "") for word in words]
        if words[0].lower() in ("upper", "lower"):
            del words[0]

        function = globals()["format_%s" % words[0].lower()]
        formatted = function(words[1:])

        if words[0].lower() == 'number':
            return Events("number->%s" % formatted)
        else:
            return Events('text->%s' % formatted)


format_rule = RuleRef(name="format_rule", rule=FormatRule(name="f"))


enclosures = {}
enclosures['circle'] = '()'
enclosures['box'] = '[]'
enclosures['diamond'] = '<>'
enclosures['hexy'] = '{}'
enclosures['quotes'] = '""'
enclosures['ticks'] = "''"
enclosures['backticks'] = '``'


class NestRule(CompoundRule):
    spec = ("[nest] (circle | box | ticks | quotes | hexy | backticks) [<format_rule>]")
    extras = [format_rule]

    def _process_recognition(self, node, extras):
        words = node.words()
        print words

        if words[0] == 'nest':
            closure = enclosures[words[1]]
            event = Events("text->%s;key->code=123" % closure)
            if 'format_rule' in extras:
                event += extras['format_rule']
        else:
            closure = enclosures[words[0]]
            event = Events("text->%s" % closure)

        event.execute()


class MultipleSymbolsRule(CompoundRule):
    spec = ("[aces] <symbols_letters> [<n>]")
    extras = [Alternative([case_alphabet_rule, alphabet_rule, symbols_rule], name="symbols_letters"), IntegerRef("n", 1, 10)]
    defaults = {"n":1}

    def _process_recognition(self, node, extras):
        words = node.words()
        symbol = extras['symbols_letters'][0][0]
        events = Events("text->")
        times = extras['n']

        for i in xrange(times):
            events += symbol

        if words[0] == 'aces':
            events = Events("key->key=space") + events + Events("key->key=space")

        events.execute()


class LiteralRule(CompoundRule):
  spec = "<format_rule>"

  extras = [format_rule]

  def _process_recognition(self, node, extras):
    extras["format_rule"].execute()


grammar.add_rule(MacCommand())
grammar.add_rule(MultipleSymbolsRule())
grammar.add_rule(LiteralRule())
grammar.add_rule(NestRule())


grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
