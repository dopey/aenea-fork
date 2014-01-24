from dragonfly import (Grammar, Dictation, Context, MappingRule, Pause, IntegerRef)
from proxy_nicknames import Key, Text, Events, AppRegexContext

from raul import SelfChoice, processDictation, NUMBERS as numbers

import aenea


iterm_context = aenea.global_context & AppRegexContext(name="iTerm")
grammar = Grammar("iTerm", context=iterm_context)

submit = Events("key->code=36")


class ItermCommand(MappingRule):
    mapping = {
        "dear": Events("text->cd\n"),
        "dear work": Events("text->cd $WORK\n"),
        "dear games": Events("text->cd $GAMES\n"),
        "dear id": Events("text->cd $ID\n"),
        "dear grammar": Events("text->cd $GRAMMAR\n"),
        "dear back": Events("text->cd ../\n"),
        "dear [<text>]": Events("text->cd %(text)s"),
        "make dear": Events("text->mkdir "),
        "list [<text>]": Events("text->ls -la %(text)s"),
        "tab left [<n>]": Events("key->code=123&modifier=command&times=%(n)d"),
        "tab right [<n>]": Events("key->code=124&modifier=command&times=%(n)d"),
        "make test": Events("text->make test\n"),
        "integrate": Events("text->bin/integrate\n"),
        "exec above": Events("key->code=126;key->code=36"),
        "exec left": Events("key->code=123&modifier=command&times=%(n)d") + Events("key->code=126;key->code=36"),
        "exec right": Events("key->code=124&modifier=command&times=%(n)d") + Events("key->code=126;key->code=36"),

        # GIT
        #---------------------------#
        "get status": Events("text->git status\n"),
        "get pull": Events("text->git pull --rebase origin master\n"),
        "get push": Events("text->git push origin master\n"),
        "get diff [<text>]": Events("text->git diff %(text)s\n"),
        "get add ": Events("text->git add "),
        "get commit ": Events("text->git commit -m \"\";key->code=123"),
        "get log": Events("text->git log\n"),

        # EXECUTION
        #---------------------------#
        "kill": Events("key->key=c&modifier=control"),
        "stop": Events("key->key=d&modifier=control"),

        #COPY
        #---------------------#
        "tmux start": Events("text->tmux-all start\n"),
        "tmux stop": Events("text->tmux-all stop\n"),
        "tmux detach": Events("key->key=b&modifier=control;key->key=d"),
        "tmux attach": Events("text->tmux attach -tall\n"),
        #---------------------------#
        "[<text>]": Events("text->%(text)s&modifiers=lower")
    }
    extras = [Dictation("text"), IntegerRef("n", 1, 10)]
    defaults = {"text":"", "n":1}

grammar.add_rule(ItermCommand())

grammar.load()

def unload():
  global grammar
  if grammar: grammar.unload()
  grammar = None
