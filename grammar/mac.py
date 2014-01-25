from dragonfly import Config, Section, Item, MappingRule, CompoundRule, Grammar, IntegerRef, Dictation, RuleRef, Alternative, Repetition, Literal, Sequence

from proxy_nicknames import Key, Text, Events

from dictionary_grammars import DIGITS, SYMBOLS, ALPHABET, CASE_ALPHABET
import aenea



mac_context = aenea.global_context
grammar = Grammar("mac", context=mac_context)

submit = Events("key->code=36")

clear = Events("key->code=51&modifier=command")
escape = Events("key->code=53")

sequence_command_table = {
    "up [<n>]": Events("key->code=126&times=%(n)d"),
    "down [<n>]": Events("key->code=125&times=%(n)d"),
    "left [<n>]": Events("key->code=123&times=%(n)d"),
    "right [<n>]": Events("key->code=124&times=%(n)d"),
    "space [<n>]": Events("key->key=space&times=%(n)d"),
    "dribble":          Events("key->key=,;key->key=space"),
    "colon equal":     Events("key->key=space;key->code=41&modifier=shift;key->code=24;key->key=space"),
    "equal [<n>]":     Events("key->key=space;key->code=24&times=%(n)d;key->key=space"),
    "not equal [<n>]": Events("text-> !;key->code=24&times=%(n)d;key->key=space"),
    "pipes":            Events("text-> || "),
    "greater":          Events('key->key=space;key->key=.&modifier=shift;key->key=space'),
    "greater equal":             Events('key->key=space;key->key=.&modifier=shift;key->code=24;key->key=space'),
    "less":             Events('key->key=space;key->key=,&modifier=shift;key->key=space'),
    "less equal":             Events('key->key=space;key->key=,&modifier=shift;key->code=24;key->key=space'),
    "right arrow":      Events('text->-;text->>'),
    "left arrow":      Events('text-><;text->-'),
    "escape":             escape,
    "plus":             Events('key->key=space;key->code=24&modifier=shift;key->key=space'),
    "plus equal":      Events("key->key=space;key->code=24&modifier=shift;key->code=24;key->key=space"),
    "minus":             Events('key->key=space;key->code=27;key->key=space'),
    "minus equal":      Events("key->key=space;key->code=27;key->code=24;key->key=space"),

    "times":             Events('key->key=space;key->code=28&modifier=shift;key->key=space'),
    "times equal":      Events("key->key=space;key->code=28&modifier=shift;key->code=24;key->key=space"),

    "times":             Events('key->key=space;key->code=28&modifier=shift;key->key=space'),
    "times equal":      Events("key->key=space;key->code=28&modifier=shift;key->code=24;key->key=space"),
    "circle":           Events('text->()'),
    "nest circle":      Events('text->();key->code=123'),
    "diamond":          Events('text-><>'),
    "nest diamond":     Events('text-><>;key->code=123'),
    "box":              Events('text->[]'),
    "nest box":         Events('text->[];key->code=123'),
    "hexy":             Events('text->{}'),
    "nest hexy":        Events('text->{};key->code=123'),
    "ticks":            Events("text->''"),
    "nest ticks":       Events("text->'';key->code=123"),
    "quotes":           Events('text->""'),
    "nest quotes":      Events('text->"";key->code=123'),
    "backticks":        Events("text->``"),
    "nest backticks":   Events("text->``;key->code=123"),
    "hexy lines":       Events("text->{}") + Events("text->\n;key->key=escape;key->key=o&modifier=shift"),
}

#---------------------------------------------------------------------------
# Here we define the keystroke rule.

# This rule maps spoken-forms to actions.  Some of these
#  include special elements like the number with name "n"
#  or the dictation with name "text".  This rule is not
#  exported, but is referenced by other elements later on.
#  It is derived from MappingRule, so that its "value" when
#  processing a recognition will be the right side of the
#  mapping: an action.
# Note that this rule does not execute these actions, it
#  simply returns them when it's value() method is called.
#  For example "up 4" will give the value Key("up:4").
# More information about Key() actions can be found here:
#  http://dragonfly.googlecode.com/svn/trunk/dragonfly/documentation/actionkey.html
class KeystrokeRule(MappingRule):
  exported = False

  extras = [
    IntegerRef("n", 1, 10),
    Dictation("text"),
    Dictation("text2"),
    ]
  defaults = {
    "n": 1,
    }

#---------------------------------------------------------------------------
class MacCommand(MappingRule):
    mapping = {
        # Text entry/manipulation
        "submit [<n>]": Events('key->code=36&times=%(n)d'),
        "clear": clear,
        # Window Movement/manipulation
        "screen left [<n>]": Events("key->code=123&modifier=control&times=%(n)d"),
        "screen right [<n>]": Events("key->code=124&modifier=control&times=%(n)d"),

        #DELETION
        #------------------#
        "dell [<n>]": Events("key->code=51&times=%(n)d"),
        "doll [<n>]": Events("key->code=51&modifier=option&times=%(n)d"),

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

def format_dotword(text):
  return ".".join(text)

def format_dashword(text):
  return "-".join(text)

def format_slashes(text):
  return "/".join(text)

def format_natural(text):
  return " ".join(text)

def format_broodingnarrative(text):
  return ""

class FormatRule(CompoundRule):
    spec = ("[upper | lower] ( proper | camel | rel-path | abs-path | score | "
            "scope-resolve | jumble | dotword | dashword | natural | snakeword | brooding-narrative | capword | caplock | slashes | number) [<dictation>]")

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
alternatives = [
    RuleRef(rule=KeystrokeRule(mapping=sequence_command_table, name="c")),
    format_rule,
]
single_action = Alternative(alternatives)

# create a repetition of keystroke elements.
#  This element will match anywhere between 1 and 16 repetitions
#  of the keystroke elements.  Note that we give this element
#  the name "sequence" so that it can be used as an extra in
#  the rule definition below.
# Note: when processing a recognition, the *value* of this element
#  will be a sequence of the contained elements: a sequence of
#  actions.
sequence = Repetition(single_action, min=1, max=16, name="sequence")

# This is the rule that actually handles recognitions.
#  When a recognition occurs, it's _process_recognition()
#  method will be called.  It receives information about the
#  recognition in the "extras" argument: the sequence of
#  actions and the number of times to repeat them.
class RepeatRule(CompoundRule):
    # Here we define this rule's spoken-form and special elements.
    spec = "seek <sequence>"

    extras = [
        sequence, # Sequence of actions defined above.
    ]
    defaults = {
      "n": 1, # Default repeat count.
    }

    # This method gets called when this rule is recognized.
    # Arguments:
    #  - node -- root node of the recognition parse tree.
    #  - extras -- dict of the "extras" special elements:
    #   . extras["sequence"] gives the sequence of actions.
    #   . extras["n"] gives the repeat count.
    def _process_recognition(self, node, extras):
      words = node.words()
      print words
      sequence = extras.get("sequence", [])
      for action in sequence:
        action.execute()


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


grammar.add_rule(MacCommand())
grammar.add_rule(MultipleSymbolsRule())
grammar.add_rule(RepeatRule())


grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
