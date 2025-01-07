"""
---------------------
Author: Spencer Lukey
Date: March 11, 2024
---------------------

Purpose: Implements the ADT Bounded Queue to use later on in 'main.py'
"""


class BQueue:
  """
    This class is used for implementing a bounded queue into the main function in assignment3.py
    to unload each chemical from the text data into a flask
    """

  def __init__(self, size):
    # items enqueued at back of stack, dequeued from beginning
    self.__capacity = size
    self.queue = []
    self.__size = 0  # set another var in memory to avoid calculating len(self.queue)

  def enqueue(self, item):
    """
        Parameters: self -> object, item -> string
        Returns: None
        Enqueues an item to the end of the queue if room exists
        """
    if self.__size < self.__capacity:
      self.queue.append(item)
      self.__size += 1

  def dequeue(self):
    """
        Parameters: self -> object
        Returns: self.queue.pop(0)
        If queue is not empty then it returns the first item in queue
        """
    if self.__size > 0:
      self.__size -= 1
      return self.queue.pop(0)

  def peek(self):
    """
        Parameters: self -> object
        Returns: front item of queue
        Returns the first item in the queue next to be dequeued
        """
    return self.queue[0]

  def isEmpty(self):
    """
        Parameters: self -> object
        Returns: bool
        Returns T or F whether the queue is empty or no
        """
    return self.__size == 0

  def isFull(self):
    """
        Parameters: self -> object
        Returns: bool
        Returns whether or not the queue is full
        """
    return self.__size == self.__capacity

  def size(self):
    """
        Parameters: self -> object
        Returns: current_size -> int
        Returns the current size of the list
        """
    return self.__size

  def capacity(self):
    """
        Parameters: self -> object
        Returns: capacity -> int
        Returns the capacity of the list
        """
    return self.__capacity

  def clear(self):
    """
        Parameters: self -> object
        Returns: None
        Empty the queue
        """
    self.queue = []
    self.__size = 0

  def __str__(self):
    """
        Parameters: self -> object
        Returns: string -> str
        Returns a string representation of the bqueue
        """
    string = '['
    for element in self.queue:
      string += (element + ' ')

    if string != '[':
      string = string[:-1] + ']'
    else:
      string += ']'

    return string
