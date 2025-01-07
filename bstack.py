"""
----------------------
Date: March 2, 2024
Author: Spencer Lukey
----------------------

Purpose: Implement the bounded stack ADT along with its various attributes and methods (imported to main.py)
"""


# Initialize the bounded stack:
class BStack:
  """
    This class is used for implementing a bounded stack into the main function in assignment3.py,
    allowing items to be added, removed, etc. as long as the stack's length > 0, and < max length
    """

  def __init__(self, size, full):
    """
        Creates a stack object with empty stack bounded by the size inputted from main, sets current size to 0

        Parameters: self (object), size (int), full (int)
        Returns: None
        """
    self.stack = []
    self.max_size = size
    self.full_size = full
    self.current_size = 0

  def push(self, item):
    """
        Checks length of stack before adding item to the top. Cannot exceed max_size without raising an error to function call

        Parameters: self (object), item (any)
        Returns: None
        """
    if (self.current_size < self.max_size):
      self.stack.append(item)
      self.current_size += 1
    else:
      raise Exception('Error: Cannot push, stack is full')

  def getItems(self):
    """
        Parameters: self -> object
        Returns: self.stack

        Returns the items in the stack to function call
        """
    return self.stack

  def pop(self):
    """
        Checks that stack isn't empty before popping the item off the top of the stack and returning it to the user

        Parameters: self (object)
        Returns: item (any); only if stack isn't empty
        """
    if (self.current_size != 0):
      self.current_size -= 1
      return self.stack.pop()

    else:
      raise Exception('Error: Cannot pop, stack is empty')

  def peek(self):
    """
        Returns the top item off of the stack without removing it

        Parameters: self (object)
        Returns: top_item (any or None)
        """
    try:
      top_item = self.stack[-1]
    except IndexError:
      top_item = None
    finally:
      return top_item

  def isEmpty(self):
    """
        Returns a boolean value whether the list is empty or not

        Parameters: self (object)
        Returns: True/False
        """
    return self.current_size == 0

  def isFull(self):
    """
        Returns a boolean value whether the list is full or not (4 items)

        Parameters: self (object)
        Returns: True/False
        """
    return self.current_size == self.max_size

  def size(self):
    """
        Parameters: self -> object
        Returns: self.current_size -> int

        Returns an integer value of the size of the stack 
        """
    return self.current_size

  def isComplete(self):
    """
      Returns a value of either True or False depending on if 
      the stack (flask) has all the same items, and is full

      Parameters: self -> object
      Returns: complete -> bool
      """
    complete = False
    if len(
        set(self.stack)
    ) == 1 and self.current_size == self.full_size:  # set of stack should only have one element and have three of the same
      complete = True

    return complete
