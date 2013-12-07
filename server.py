#!/usr/bin/python

import comsat, sys, os, time, random, applescript
from keycodes import keycodes


scpt = scpt = applescript.AppleScript('''
    on stroke(msg)
        tell application "System Events"
            keystroke msg
        end tell
    end stroke

    on code(theNum, mod1, mod2)
        set theNum to theNum as number
        tell application "System Events"
            if (mod1 is "") and (mod2 is "") then
                key code theNum
            else if (mod1 is "") and (mod2 is "command") then
                key code theNum using command down
            else if (mod1 is "") and (mod2 is "option") then
                key code theNum using option down
            else if (mod1 is "") and (mod2 is "control") then
                key code theNum using control down
            else if (mod1 is "") and (mod2 is "shift") then
                key code theNum using shift down
            else if (mod1 is "command") and (mod2 is "control") then
                key code theNum using {command down, control down}
            else if (mod1 is "command") and (mod2 is "option") then
                key code theNum using {command down, option down}
            else if (mod1 is "command") and (mod2 is "shift") then
                key code theNum using {command down, shift down}
            else if (mod1 is "control") and (mod2 is "option") then
                key code theNum using {control down, option down}
            else if (mod1 is "control") and (mod2 is "shift") then
                key code theNum using {control down, shift down}
            else if (mod1 is "option") and (mod2 is "shift") then
                key code theNum using {option down, shift down}
            end if
        end tell
    end code

    on getActiveWindow()
        tell application "System Events"
            set frontApp to first application process whose frontmost is true
            set frontAppName to name of frontApp
        end tell
        return frontAppName
    end getActiveWindow
''')

# to help see when the server has started while in a bash loop
for i in range(random.randint(1, 10)):
  print

XPROP_PROPERTIES = {
    "_NET_WM_DESKTOP(CARDINAL)":"desktop",
    "WM_WINDOW_ROLE(STRING)":"role",
    "_NET_WM_WINDOW_TYPE(ATOM)":"type",
    "_NET_WM_PID(CARDINAL)":"pid",
    "WM_LOCALE_NAME(STRING)":"locale",
    "WM_CLIENT_MACHINE(STRING)":"client_machine",
    "WM_NAME(STRING)":"name"
    }

XDOTOOL_COMMAND_BREAK = set(("type",))

class Handler(object):
  def __init__(self):
    self.state = {}

  @staticmethod
  def runCommand(command, executable="xdotool"):
    command_string = "%s %s" % (executable, command)
    sys.stderr.write(command_string + "\n")
    os.system(command_string)

  @staticmethod
  def readCommand(command, executable="xdotool"):
    with os.popen("%s %s" % (executable, command), "r") as fd:
      rval = fd.read()
    sys.stderr.write("%s %s > %s\n" % (executable, command, rval))
    return rval

  @staticmethod
  def writeText(message, executable="xdotool"):
    print "writeText: %s" % message
    scpt.call('stroke', message)

  @staticmethod
  def writeKey(keyCode, mods=['', '']):
    scpt.call('code', keyCode, mods[0], mods[1])


  def callEvents(self, events):
    """Call each event in order"""
    print "EVENTS"
    print events
    for event in events.split(';'):
      print event
      eventType, args = event.split('->')
      if eventType == 'key':
        self.callKey(args)
      elif eventType == 'text':
        self.callText(args)
      elif eventType == 'number':
        self.callNumber(args)


  def callNumber(self, events):
    """Call number using keystrokes"""
    print events
    try:
        args = events.split('&')
        number = args[0]
        for arg in args[1:]:
            name, value = arg.split('=')
            if name == 'modifiers':
                mods = value.split(',')
                for mod in mods:
                    if mod == 'text':
                        print number
                        number = number.replace('zero', '0')
                        number = number.replace('one', '1')
                        number = number.replace('to', '2')
                        number = number.replace('for', '4')
                        number = number.replace('.\\point', '.')
                        number = number.replace(' ', '')
                        print number

        for num in list(number):
            self.writeKey(keycodes[num])

    except:
        return


  def callText(self, events):
    """Types a string as is."""
    if events:
      print events
      args = events.split('&')
      if len(args) == 0 or args[0] == '':
        return

      message = args[0]
      first = False
      for arg in args[1:]:
        name, value = arg.split('=')
        if name == 'modifiers':
          mods = value.split(',')
          for mod in mods:
            if mod == 'lower':
              message = message.lower()
            elif mod == 'first':
              words = message.split(' ')
              message = "".join([word[0] for word in words])
            elif mod == 'upper':
              message = message.upper()

      print message
      self.writeText(message)


  def callKey(self, event):
    """Call key with given modifiers and extras"""
    keyCode = ''
    mods = ['' for x in range(2)]
    num_mods = 0
    text = ''
    times = 1
    repeat = 1

    for arg in event.split('&'):
      name, value = arg.split('=')
      if name == 'code':
        keyCode = value
      elif name == 'key':
        keyCode = keycodes[value]
      elif name == 'modifier':
        mods[num_mods] = value
        num_mods += 1
      elif name == 'times':
        times = int(value)
      elif name == 'repeat':
        repeat = int(value)
      elif name == 'text':
        text = value

    if text:
      keyCode = keycodes[text[0].lower()]

    mods.sort()
    for i in xrange(repeat):
      for j in xrange(times):
        self.writeKey(keyCode, mods)


  def callGetCurrentWindowProperties(self):
    """Get a dictionary of properties about the currently active window"""
    name = self.callGetActiveWindow()
    print 'NAME: %s' % name
    if name:
      properties = {}
      properties['name'] = name
      return properties
    else:
      return {}

  def callLog(self, message):
    sys.stderr.write(message + "\n")

  def callMouse(self, x, y, absolute=True):
    """Moves the mouse to the specified coordinates."""
    if absolute:
      self.runCommand("mousemove %i %i" % (x, y))
    else:
      self.runCommand("mousemove_relative %i %i" % (x, y))

  def callKeyStack(self, keys):
    """Presses keys in the order specified, then releases them in the opposite order."""
    if isinstance(keys, basestring):
      keys = keys.split()
    push = ["keydown %s" % key for key in keys]
    pop = ["keyup %s" % key for key in reversed(keys)]
    self.callRaw(push + pop)

  def callKeys(self, keys):
    """Presses keys in sequence."""
    if isinstance(keys, basestring):
      keys = keys.split()
    self.runCommand(' '.join("key %s" % key for key in keys))


  def callGetActiveWindow(self):
    """Returns the window id and title of the active window."""
    name = scpt.call('getActiveWindow')
    if name:
      return name
    else:
      return None

  def callSetIonWorkspace(self, workspace):
    """Set the current ion workspace to a number from 1 to 6"""
    mapping = [1, 2, 3, "apostrophe", "comma", "period", "space"]
    self.callModifiedKeys(["&" + str(mapping[workspace - 1])])

  def callSetIonTab(self, tab):
    self.callModifiedKeys(["&k", str(tab)])

  def callPhantomClick(self, x, y, button=1, phantom=True):
    phantom = "mousemove restore" if phantom else ""
    self.runCommand("mousemove %i %i click %i %s" % (x, y, button, phantom))

  def callClick(self, button=1):
    self.runCommand("click %i" % button)

  def callModifiedKeys(self, keys):
    if isinstance(keys, basestring):
      keys = keys.split()

    command = []

    for key in keys:
      if key.startswith("^"):
        command.extend(("keydown Shift", "key " + key[1:], "keyup Shift"))
      elif key.startswith("&"):
        command.extend(("keydown Alt_L", "key " + key[1:], "keyup Alt_L"))
      elif key.startswith("*"):
        command.extend(("keydown Control_L", "key " + key[1:], "keyup Control_L"))
      else:
        command.append("key " + key)

    self.runCommand(' '.join(command))

  def callRaw(self, arguments):
    print arguments
    return self.readCommand(' '.join(arguments))

  def callReloadConfiguration(self):
    pass
#    self.callRaw(["keydown Alt_L", "key space", "keyup Alt_L",
#                           "sleep 0.05",
#                           "keydown Alt_L", "key k", "keydown Alt_L", "key 1"])

  def callGetState(self):
    state = self.state.copy()
    active_id, active_title = self.callGetActiveWindow()

    state["active_id"] = active_id
    state["active_title"] = active_title

    if active_id:
      try:
        active_pid = int(self.callRaw(["getwindowpid %i" % active_id]))
      except:
        active_pid = -1
      psocks = self.readCommand("aux | grep %i" % active_pid, executable="ps")
      state["in_terminal"] = ("urxvt" in psocks or "xfce4-terminal" in psocks)
    else:
      state["in_terminal"] = False

    return state

  def callGetGeometry(self, window_id=None):
    if window_id is None:
      window_id, _ = self.callGetActiveWindow()
    geo = dict([val.lower() for val in line.split("=")]
               for line in self.readCommand(("getwindowgeometry --shell %i"
                                             % window_id)).strip().split("\n"))
    geo = dict((key, int(value)) for (key, value) in geo.iteritems())
    return geo["x"], geo["y"], geo["width"], geo["height"], geo["screen"]

  def _transform_relative_mouse_event(self, event):
    x, y, width, height, screen = self.callGetGeometry()
    dx, dy = map(int, map(float, event.split()[1:]))
    return ["mousemove %i %i" % (x + dx, y + dy)]

  def callReadRawCommand(self, event, command="xdotool"):
    return self.readCommand(event, command)

cs = comsat.ComSat()
cs.handlers.append(Handler())

loop = cs.serverMainLoop()
while 1:
  loop.next()
