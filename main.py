"""
---------------------
Date: March 11, 2024
Author: Spencer Lukey
---------------------

Program Purpose: Import the files 'bstack.py' and 'bqueue.py', and implement the functionality of the game
"""

import os
from bstack import BStack
from bqueue import BQueue

# set constants for later use
STACK_AND_QUEUE_SIZE = 4
CHEMICAL_UNITS = 3
FOUR_FLASKS = 'chemicals1.txt'
EIGHT_FLASKS = 'chemicals2.txt'

ANSI = {
    "RED": "\033[31m",
    "GREEN": "\033[32m",
    "BLUE": "\033[34m",
    "HRED": "\033[41m",
    "HORANGE": "\033[48;5;208m",
    "HYELLOW": "\033[43m",
    "HGREEN": "\033[42m",
    "HBLUE": "\033[44m",
    "HMAGENTA": "\033[48;5;198m",
    "UNDERLINE": "\033[4m",
    "RESET": "\033[0m",
    "CLEARLINE": "\r\033[0K"
}

CHEMICAL_DICT = {
    "AA": ANSI['HRED'],
    "BB": ANSI['HBLUE'],
    "CC": ANSI['HGREEN'],
    "DD": ANSI['HORANGE'],
    "EE": ANSI['HYELLOW'],
    "FF": ANSI['HMAGENTA']
}


def unload_data(filename, size):
  """
  Parameters: filename -> str
  Returns: chemicals_list -> list

  Unloads all chemicals from 'filename' into a list stripped of its \n characters
  """
  with open(filename, 'r') as file:
    chemicals_list = file.readlines()
    chemicals_list = [chemicals.strip() for chemicals in chemicals_list]  # becomes ['AA', 'BB', ... '3F2', 'BB', ...]

  return chemicals_list


def get_flask_data(chemicals_list):
  """
  Parameters: chemicals_list -> list
  Returns: flask_data -> int, int

  Returns a dictionary with a key 1 to max flasks, value BStack object
  """
  flask_data = chemicals_list.pop(0).split(' ')
  return int(flask_data[0]), int(flask_data[1])


def init_flasks(num_flasks, capacity, full):
  """
  Parameters: num_flasks -> int, capacity -> int, full ->
  Returns: flasks_dict -> dict 

  Initializes and returns a dictionary with key-value pairs of flask number and object
  """
  flasks_dict = {}
  for flask in range(num_flasks):
    flaskStack = BStack(capacity, full)
    flasks_dict[flask + 1] = {
        'flask_obj': flaskStack,
        'flask_data': flaskStack.getItems(),
        'flask_complete': flaskStack.isComplete(),
        'flask_from': False,
        'flask_to': False
    }

  return flasks_dict


def print_flask_nums(start_num, end_num, flasks_dict):
  """
  Parameters: start_num -> int, end_num -> int, flasks_dict -> dict
  Returns: None

  Prints out all nums from start_num to end_num at the end of printing out the flasks
  """

  for flask_num in range(start_num, end_num + 1):
    if flasks_dict[flask_num]['flask_from']:
      print(f"  {ANSI['RED']}{flask_num}{ANSI['RESET']} ", end=' ')
    elif flasks_dict[flask_num]['flask_to']:
      print(f"  {ANSI['GREEN']}{flask_num}{ANSI['RESET']} ", end=' ')
    else:
      print(f"  {flask_num} ", end=' ')


def load_flasks(chemicals, capacity, flasks_dict):
  """
  Parameters: chemicals -> list, capacity -> int, flasks_dict -> dict
  Returns: loaded_flasks -> dict

  Creates a BQueue object to load chemicals into each designated flask before returning
  all loaded flasks to main()
  """
  # create queue object to load flasks
  loadQ = BQueue(capacity)
  # load BQueue until we get to something that starts with a number
  for item in chemicals:
    if item[0].isnumeric():  # means we need to dequeue some # of elements into a flask
      num_items = int(item[0])
      flask_num = int(item[-1])
      # unload certain num of items into the queue
      for chem_index in range(num_items):
        chemical = loadQ.dequeue()
        flasks_dict[flask_num]['flask_obj'].push(
            f"{CHEMICAL_DICT[chemical]}{chemical}{ANSI['RESET']}"
        )  # WILL RAISE ERROR IF loadQ IS EMPTY!!!
    else:
      loadQ.enqueue(item)

  return flasks_dict


def update_flasks(flasks_dict, fromFlask, toFlask):
  """
  Parameters: flasks_dict -> dict, fromFlask -> str, toFlask -> str
  Returns: flasks_dict -> dict

  Update items and if the stack is complete or not, returns updated dict
  """
  for index in flasks_dict.keys():
    # set object:
    flask_obj = flasks_dict[index]['flask_obj']

    # reset all from and to to False, then set to True if from and complete
    flasks_dict[index]['flask_from'] = False
    flasks_dict[index]['flask_to'] = False

    # update items representation
    flasks_dict[index]['flask_data'] = flask_obj.getItems()

    # update completion status
    flasks_dict[index]['flask_complete'] = flask_obj.isComplete()

  if fromFlask != 0:
    flasks_dict[int(fromFlask)]['flask_from'] = True

  if toFlask != 0:
    flasks_dict[int(toFlask)]['flask_to'] = True

  return flasks_dict


def set_colors(flasks_dict, fromFlask, toFlask):
  """
  Parameters: flasks_dict -> dict, fromFlask -> str, toFlask -> str
  Returns flasks_dict -> dict

  Sets the colors attribute of each flask to true if flask is chosen
  """
  flasks_dict[int(fromFlask)]['flask_from'] = True
  flasks_dict[int(toFlask)]['flask_to'] = True


def print_updated_flasks(flasks_dict, stack_size, num_flasks):
  """
  Parameters: flasks_dict -> dict
  Returns: None

  Prints out the correct representation of the flasks as vertical stacks
  """
  if num_flasks == 4:
    current_start = 1
    current_end = 4
    for index in range(stack_size - 1, -1, -1):
      for flask_index in range(current_start, current_end + 1):
        try:
          item = flasks_dict[flask_index]['flask_data'][index]
          
        except IndexError:
          if flasks_dict[flask_index]['flask_complete']:
            print('+--+', end=' ')
          else:
            print('|  |', end=' ')
            
        else:
          print(f'|{item}|', end=' ')
      print('\n', end='')

    
    print('+--+ ' * 4)
    print_flask_nums(current_start, current_end, flasks_dict)
    print('\033[7A')

  else:  # num_flasks = 8, need to print first four and then second four below
    current_start = 1
    current_end = 4
    for index in range(stack_size - 1, -1, -1):
      for flask_index in range(current_start, current_end + 1):
        try:
          item = flasks_dict[flask_index]['flask_data'][index]
        except IndexError:
          if flasks_dict[flask_index]['flask_complete']:
            print('+--+', end=' ')
          else:
            print('|  |', end=' ')
        else:
          print(f'|{item}|', end=' ')
      print('\n', end='')
    print('+--+ ' * 4)
    print_flask_nums(current_start, current_end, flasks_dict)

    current_start = 5
    current_end = 8
    print('\n', end='')
    for index in range(stack_size - 1, -1, -1):
      for flask_index in range(current_start, current_end + 1):
        try:
          item = flasks_dict[flask_index]['flask_data'][index]
        except IndexError:
          if flasks_dict[flask_index]['flask_complete']:
            print('+--+', end=' ')
          else:
            print('|  |', end=' ')
        else:
          print(f'|{item}|', end=' ')
      print('\n', end='')
    print('+--+ ' * 4)
    print_flask_nums(current_start, current_end, flasks_dict)
    print('\033[13A')


def check_complete(flasks_dict, num_complete_flasks):
  """
  Parameters: flasks_dict -> dict, num_complete_flasks -> int
  Returns: allComplete -> bool

  Checks all flasks to see if they're complete
  """
  allComplete = False
  full_flasks = 0

  # loop through all flasks and check each complete
  for flask in flasks_dict.keys():
    if flasks_dict[flask]['flask_complete']:
      full_flasks += 1

  # only change to True if all chemicals are sorted in flasks
  if full_flasks == num_complete_flasks:
    allComplete = True

  return allComplete


def make_move(fromFlask, toFlask, flasks_dict):
  """
  Parameters: fromFlask -> int, toFlask -> int, flasks_dict -> dict
  Returns: flasks_dict -> dict

  Moves a chemical from the top of fromFlask to the top of toFlask
  """
  flasks_dict[toFlask]['flask_obj'].push(
      flasks_dict[fromFlask]['flask_obj'].pop())
  return flasks_dict


def process_from(fromFlask, flasks_dict, amount_flasks):
  """
  Parameters: fromFlask -> str, flasks_dict -> dict, amount_flasks -> int
  Returns: None

  Checks if the user's inputted data is valid, flasks full, empty, etc. and raises an error if encountered
  """
  assert fromFlask.isnumeric(), 'Please input an integer        '
  assert (int(fromFlask) > 0 and int(fromFlask) <= amount_flasks), f'Flask must be within range 1-{amount_flasks} '
  assert not flasks_dict[int(fromFlask)]['flask_obj'].isEmpty(), 'Please pour from a filled flask'
  assert not flasks_dict[int(fromFlask)]['flask_complete'], 'Cannot pour from complete flask'


def process_to(toFlask, fromFlask, flasks_dict, amount_flasks):
  """
  Parameters: toFlask -> str, fromFlask -> str, flasks_dict -> dict, amount_flasks -> int
  Returns: None

  Checks if the user's inputted data is valid, flasks full, empty, etc. and raises an error if encountered
  """
  assert toFlask.isnumeric(), 'Please input an integer              '
  assert int(toFlask) != int(fromFlask), "Can't pour into same flask           "
  assert (int(toFlask) > 0 and int(toFlask) <= amount_flasks), f'Flask # must be within range 1-{amount_flasks}      '
  assert not flasks_dict[int(toFlask)]['flask_obj'].isFull(), 'Cannot pour into a full flask        '
  assert not flasks_dict[int(toFlask)]['flask_complete'], 'Cannot pour into a complete flask'


def print_resetted(flasks_dict, size, num_flasks):
  """
  Parameters: flasks_dict -> dict, size -> int, num_flasks -> int
  Returns: None

  Resets the screen and prints out all of the text for the terminal
  """
  if os.name == "nt":  # for Windows
    os.system("cls")
  else:  # for Mac/Linux
    os.system("clear")

  print('Magical Flask Game\n')
  print('Select a flask to pour from: ')
  print('Select a flask to pour into: \n')
  print_updated_flasks(flasks_dict, size, num_flasks)


def main():
  """
  Parameters: None
  Returns: None

  Implements the main logic of the program, calls helper functions to compile data to be used 
  later on in the program
  """
  # unload data from file
  chemicals_list = unload_data(EIGHT_FLASKS, STACK_AND_QUEUE_SIZE)
  # set to constants from file
  NUM_FLASKS, NUM_CHEMICALS = get_flask_data(chemicals_list)

  # initialize all flasks
  flasks_dict = init_flasks(NUM_FLASKS, STACK_AND_QUEUE_SIZE, CHEMICAL_UNITS)
  flasks_dict = load_flasks(chemicals_list, STACK_AND_QUEUE_SIZE, flasks_dict)
  flasks_dict = update_flasks(flasks_dict, 0, 0)

  # start game!
  os.system("")  # Enables ANSI escape codes in terminal

  # print out start
  print_resetted(flasks_dict, STACK_AND_QUEUE_SIZE, NUM_FLASKS)

  allComplete = False
  notQuit = True
  while not allComplete and notQuit:

    try:
      fromFlask = input('\033[2A' + '\033[29C')
      if fromFlask.lower() == 'quit':
        notQuit = False
      process_from(fromFlask, flasks_dict, NUM_FLASKS)

    except AssertionError as e:
      print('\033[A' + ANSI['CLEARLINE'] + 'Select a flask to pour from: ' + '\033[B')
      print(e.args[0])
      print('\033[2A')

    else:
      print('\033[B')
      print('\033[A' + ANSI['CLEARLINE'] + '\033[2A')
      badAnswer = True
      while badAnswer:
        try:

          toFlask = input('\033[29C')
          if toFlask.lower() == 'quit':
            notQuit = False
          process_to(toFlask, fromFlask, flasks_dict, NUM_FLASKS)
        except AssertionError as e:
          print('\033[A' + ANSI['CLEARLINE'] + 'Select a flask to pour into: ')
          print(e.args[0])
          print('\033[3A')
        else:
          badAnswer = False
          # check if the number of flasks full = NUM_CHEMICALS
          make_move(int(fromFlask), int(toFlask), flasks_dict)
          flasks_dict = update_flasks(flasks_dict, fromFlask, toFlask)
          allComplete = check_complete(flasks_dict, NUM_CHEMICALS)
          print_resetted(flasks_dict, STACK_AND_QUEUE_SIZE, NUM_FLASKS)

  if notQuit:
    if os.name == "nt":  # for Windows
      os.system("cls")
    else:  # for Mac/Linux
      os.system("clear")
    print("You win!")
  else:
    if os.name == "nt":  # for Windows
      os.system("cls")
    else:  # for Mac/Linux
      os.system("clear")
    print('Exiting...')


if __name__ == "__main__":
  main()
