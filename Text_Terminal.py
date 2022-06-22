"""
Made in python3.10
should be used only for unix based operating systems
"""

import sys, tty

""" Terminal Should Be Used As A Text Editor/Language Terminal Base"""
class Terminal:
  @staticmethod
  def print_(text):
    """ write text to stdout and flush """
    sys.stdout.write(text)
    sys.stdout.flush()
  
  @staticmethod
  def cache_print_(text):
    """ print to terminal without flushing """
    sys.stdout.write(text)

  @staticmethod
  def bright_background(code):
    """ print the given code as a bright background,
    if code is invalid errors may occur """
    Terminal.print_("\u001b[{};1m".format(code))
  
  @staticmethod
  def force_position(line, column):
    """ force cursor to line and column """
    Terminal.print_(f"\033[{line};{column}H")

  @staticmethod
  def force_up(amt):
    """ force cursor up amt lines """
    if amt > 0: Terminal.print_("\033[{}A".format(amt))

  @staticmethod
  def force_down(amt):
    """ force cursor down amt lines """
    if amt > 0: Terminal.print_("\033[{}B".format(amt))

  @staticmethod
  def force_right(amt):
    """ force cursor to the right by amt """
    if amt > 0: Terminal.print_("\033[{}C".format(amt))

  @staticmethod
  def force_left(amt):
    """ force cursor to the left by amt """
    if amt > 0: Terminal.print_("\033[{}D".format(amt))

  @staticmethod
  def normal_background(code):
    """ print the given code as a background
    if code is invalid side effects may occur """
    Terminal.print_("\u001b[{}m".format(code))

  @staticmethod
  def color(code):
    """ print the given code as a color
    if code is invalid side effects may occur """
    Terminal.print_("\u001b[38;5;{}m".format(code))
  
  @staticmethod
  def reset():
    """ resets text to default """
    Terminal.print_("\u001b[0m")
  
  @staticmethod
  def bold():
    """ bold text """
    Terminal.print_("\u001b[1m")
  
  @staticmethod
  def underline():
    """ underline text """
    Terminal.print_("\u001b[4m")
  
  @staticmethod
  def inverse():
    """ invert text color and background """
    Terminal.print_("\u001b[7m")
  
  @staticmethod
  def demo_colors():
    """ demo color codes """
    for i in range(256):
      Terminal.color(i)
      Terminal.print_(f"{i}\t")
    Terminal.print_("\n")
  
  @staticmethod
  def clear_line():
    """ erase currend line under 10k length """
    Terminal.print_(u"\u001b[10000D")
    Terminal.print_("\u001b[0K")
  
  @staticmethod
  def clear_line_by_amt(amt):
    """ erase currend line under amt length """
    Terminal.print_(f"\u001b[{amt}D")
    Terminal.print_("\u001b[0K")

  @staticmethod
  def clear():
    """ clear terminal """
    Terminal.print_("\033[2J")
  
  def __init__(self):
    """ initalize the Terminal object """
    self.horizontal_index = 0
    self.vertical_index = 0
    self.line_log = [""]
    
    self.max_length = 1

    self.regex_colors = {}
    
    self._left_binds = []
    self._right_binds = []
    self._up_binds = []
    self._down_binds = []
    self._interrupt_binds = []
    self._EOF_binds = []
    self._escape_binds = []

  def move_up(self, amt):
    """ safely move up by amt """
    if self.vertical_index - amt < 0:
      pass
    else:
      self.vertical_index -= amt
      if self.horizontal_index > len(self.line_log[self.vertical_index]):
        self.horizontal_index = len(self.line_log[self.vertical_index])
      Terminal.force_up(amt)

  def move_down(self, amt):
    """ safely move down by amt """
    if self.vertical_index + amt >= len(self.line_log):
      pass
    else:
      self.vertical_index += amt
      if self.horizontal_index > len(self.line_log[self.vertical_index]):
        self.horizontal_index = len(self.line_log[self.vertical_index])
      Terminal.force_down(amt)

  def move_right(self, amt):
    """ safely move right by amt """
    if self.horizontal_index + amt > len(self.line_log[self.vertical_index]):
      pass
    else:
      Terminal.force_right(amt)
      self.horizontal_index += amt

  def move_left(self, amt):
    """ safely move left by amt """
    if self.horizontal_index - amt <= 0:
      Terminal.force_left(self.horizontal_index)
      self.horizontal_index = 0
    else:
      self.horizontal_index -= amt
      Terminal.force_left(amt)

  def _on_left_arrow(self):
    """ triggers left binds on left arrow key """
    for i in self._left_binds:
      i()
  
  def _on_right_arrow(self):
    """ triggers right binds on right arrow key """
    for i in self._right_binds:
      i()

  def _on_up_arrow(self):
    """ triggers up binds on up arrow key """
    for i in self._up_binds:
      i()

  def _on_down_arrow(self):
    """ triggers down binds on down arrow key """
    for i in self._down_binds:
      i()

  def _on_interrupt(self):
    """ triggers interrupt binds on interrupt ie Ctrl+C """
    for i in self._interrupt_binds:
      i()

  def _on_EOF(self):
    """ triggers interrupt binds on EOF ie Ctrl+D """
    for i in self._EOF_binds:
      i()

  def _on_escape(self):
    """ triggers escape binds on esc """
    for i in self._escape_binds:
      i()
  
  def bind_left_arrow(self, func):
    """ adds a func to left arrow binds """
    self._left_binds.append(func)

  def bind_right_arrow(self, func):
    """ adds a func to right arrow binds """
    self._right_binds.append(func)

  def bind_up_arrow(self, func):
    """ adds a func to up arrow binds """
    self._up_binds.append(func)

  def bind_down_arrow(self, func):
    """ adds a func to down arrow binds """
    self._down_binds.append(func)

  def bind_interrupt(self, func):
    """ adds a func to interrupt binds"""
    self._interrupt_binds.append(func)

  def bind_escape(self, func):
    """ adds a func to escape arrow binds """
    self._escape_binds.append(func)
  
  def get_char(self):
    """ get char from stdin """
    char_in = sys.stdin.read(1)
    return ord(char_in)
  
  def handle_arrow_or_escape(self):
    """ handle an arrow key or escape key """
    next1 = self.get_char()
    next2 = self.get_char()
    if next1 == 91:
      if next2 == 65:
        self._on_up_arrow() #up
      elif next2 == 66:
        self._on_down_arrow() #down
      elif next2 == 67:
        self._on_right_arrow() #right
      elif next2 == 68:
        self._on_left_arrow() #left
    else:
      self._on_escape()
  
  def print_remainder(self):
    for i in self.line_log[self.vertical_index + 1:]:
        Terminal.print_('\n')
        Terminal.clear_line_by_amt(self.max_length)
        Terminal.print_(i)
        
    Terminal.force_up((len(self.line_log) - 1) - self.vertical_index)

  def handle_newline(self):
    """ handles a newline, in the even that one is half way through a line
    push the text after the cursor onto the next line"""

    first, second = self.line_log[self.vertical_index][:self.horizontal_index], self.line_log[self.vertical_index][self.horizontal_index:]
 
    self.line_log.pop(self.vertical_index)

    self.line_log.insert(self.vertical_index, first)
    self.vertical_index += 1

    Terminal.clear_line_by_amt(self.max_length)
    Terminal.print_(self.line_log[self.vertical_index - 1])
    Terminal.force_left(self.max_length)
    
    self.print_('\n')

    self.line_log.insert(self.vertical_index, second)

    self.print_remainder()
    self.horizontal_index = 0

  def handle_printable_input_character(self, input_):
    self.line_log[self.vertical_index] = self.line_log[self.vertical_index][:self.horizontal_index] + input_ + self.line_log[self.vertical_index][self.horizontal_index:]
    self.horizontal_index += 1

  def handle_del_in(self):
    if self.horizontal_index - 1 >= 0:
      self.line_log[self.vertical_index] = self.line_log[self.vertical_index][:self.horizontal_index - 1] + self.line_log[self.vertical_index][self.horizontal_index:]
      self.horizontal_index -= 1

  def handle_character(self):
    char_in = ord(sys.stdin.read(1))
    if char_in == 3:
      self._on_interrupt()
    elif char_in == 27:
      self.handle_arrow_or_escape()
    elif chr(char_in) in '\r':
      self.handle_newline()
    elif 32 <= char_in and char_in <= 126:
      self.handle_printable_input_character(chr(char_in))
    elif char_in == 127:
      self.handle_del_in()

    self.max_length += 1 #this is fine

    Terminal.clear_line_by_amt(self.max_length)
    Terminal.print_(self.line_log[self.vertical_index])
    Terminal.force_left(self.max_length)
    Terminal.force_right(self.horizontal_index)

  def main_loop(self):
    """ triggers main loop allowing for user_input """
    tty.setraw(sys.stdin)

    while True:
      self.handle_character()

def main():
    t = Terminal()

    t.bind_left_arrow(lambda: t.move_left(1))
    t.bind_right_arrow(lambda: t.move_right(1))
    t.bind_down_arrow(lambda: t.move_down(1))
    t.bind_up_arrow(lambda: t.move_up(1))
    t.bind_interrupt(exit)

    t.main_loop()

if __name__ == '__main__':
    main()
