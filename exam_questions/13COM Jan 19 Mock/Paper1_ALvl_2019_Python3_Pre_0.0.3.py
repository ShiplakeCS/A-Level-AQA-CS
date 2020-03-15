#Skeleton Program code for the AQA A Level Paper 1 Summer 2019 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.5.1 programming environment

import random
import pickle
import os
import struct

INVENTORY = 1001
MINIMUM_ID_FOR_ITEM = 2001
ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS = 10000

class Place():
  def __init__(self):
    self.Description = ""
    self.ID = self.North = self.East = self.South = self.West = self.Up = self.Down = 0

class Character():
  def __init__(self):
    self.Name = self.Description = ""
    self.ID = self.CurrentLocation = 0

class Item():
  def __init__(self):
    self.ID = self.Location = 0
    self.Description = self.Status = self.Name = self.Commands = self.Results = ""

def GetInstruction():
  print(os.linesep)
  Instruction = input("> ").lower()
  return Instruction

def ExtractCommand(Instruction):
  Command = ""
  if " " not in Instruction:
    return Instruction, Instruction
  while len(Instruction) > 0 and Instruction[0] != " ":
    Command += Instruction[0]
    Instruction = Instruction[1:]
  while len(Instruction) > 0 and Instruction[0] == " ":
    Instruction = Instruction[1:]
  return Command, Instruction

def Go(You, Direction, CurrentPlace):
  Moved = True
  if Direction == "north":
    if CurrentPlace.North == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.North
  elif Direction == "east":
    if CurrentPlace.East == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.East
  elif Direction == "south":
    if CurrentPlace.South == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.South
  elif Direction == "west":
    if CurrentPlace.West == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.West
  elif Direction == "up":
    if CurrentPlace.Up == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.Up
  elif Direction == "down":
    if CurrentPlace.Down == 0:
      Moved = False
    else:
      You.CurrentLocation = CurrentPlace.Down
  else:
    Moved = False
  if not Moved:
    print("You are not able to go in that direction.")
  return You, Moved

def DisplayDoorStatus(Status):
  if Status == "open":
    print("The door is open.")
  else:
    print("The door is closed.")

def DisplayContentsOfContainerItem(Items, ContainerID):
  print("It contains: ", end = "")
  ContainsItem = False
  for Thing in Items:
    if Thing.Location == ContainerID:
      if ContainsItem:
        print(", ", end = "")
      ContainsItem = True
      print(Thing.Name, end = "")
  if ContainsItem:
    print(".")
  else:
    print("nothing.")

def Examine(Items, Characters, ItemToExamine, CurrentLocation, Places):
  Count = 0
  if ItemToExamine == "inventory":
    DisplayInventory(Items)
  elif ItemToExamine == "room":
    print(Places[CurrentLocation - 1].Description)
    DisplayGettableItemsInLocation(Items, CurrentLocation)
  else:
    IndexOfItem = GetIndexOfItem(ItemToExamine, -1, Items)
    if IndexOfItem != -1:
      if Items[IndexOfItem].Location == INVENTORY or Items[IndexOfItem].Location == CurrentLocation:
        print(Items[IndexOfItem].Description)
        if "door" in Items[IndexOfItem].Name:
          DisplayDoorStatus(Items[IndexOfItem].Status)
        if "container" in Items[IndexOfItem].Status:
          DisplayContentsOfContainerItem(Items, Items[IndexOfItem].ID)
        return
    while Count < len(Characters):
      if Characters[Count].Name == ItemToExamine and Characters[Count].CurrentLocation == CurrentLocation:
        print(Characters[Count].Description)
        return
      Count += 1
    print("You cannot find " + ItemToExamine + " to look at.")

def GetPositionOfCommand(CommandList, Command):
  Position = Count = 0
  while Count <= len(CommandList) - len(Command):
    if CommandList[Count:Count + len(Command)] == Command:
      return Position
    elif CommandList[Count] == ",":
      Position += 1
    Count += 1
  return Position

def GetResultForCommand(Results, Position):
  Count = 0
  CurrentPosition = 0
  ResultForCommand = ""
  while CurrentPosition < Position and Count < len(Results):
    if Results[Count] == ";":
      CurrentPosition += 1
    Count += 1
  while Count < len(Results):
    if Results[Count] == ";":
      break
    ResultForCommand += Results[Count]
    Count += 1
  return ResultForCommand

def Say(Speech):
  print()
  print(Speech)
  print()

def ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand):
  Count = 0
  while Count < len(ResultForCommand) and ResultForCommand[Count] != ",":
    SubCommand += ResultForCommand[Count]
    Count += 1
  Count += 1
  while Count < len(ResultForCommand):
    if ResultForCommand[Count] != "," and ResultForCommand[Count] != ";":
      SubCommandParameter += ResultForCommand[Count]
    else:
      break
    Count += 1
  return SubCommand, SubCommandParameter

def ChangeLocationReference(Direction, NewLocationReference, Places, IndexOfCurrentLocation, Opposite):
  ThisPlace = Place()
  ThisPlace = Places[IndexOfCurrentLocation]
  if Direction == "north" and not Opposite or Direction == "south" and Opposite:
    ThisPlace.North = NewLocationReference
  elif Direction == "east" and not Opposite or Direction == "west" and Opposite:
    ThisPlace.East = NewLocationReference
  elif Direction == "south" and not Opposite or Direction == "north" and Opposite:
    ThisPlace.South = NewLocationReference
  elif Direction == "west" and not Opposite or Direction == "east" and Opposite:
    ThisPlace.West = NewLocationReference
  elif Direction == "up" and not Opposite or Direction == "down" and Opposite:
    ThisPlace.Up = NewLocationReference
  elif Direction == "down" and not Opposite or Direction == "up" and Opposite:
    ThisPlace.Down = NewLocationReference
  Places[IndexOfCurrentLocation] = ThisPlace
  return Places

def OpenClose(Open, Items, Places, ItemToOpenClose, CurrentLocation):
  Count = 0
  Direction = ""
  DirectionChange = ""
  ActionWorked = False
  if Open:
    Command = "open"
  else:
    Command = "close"
  while Count < len(Items) and not ActionWorked:
    if Items[Count].Name == ItemToOpenClose:
      if Items[Count].Location == CurrentLocation:
        if len(Items[Count].Commands) >= 4:
          if Command in Items[Count].Commands:
            if Items[Count].Status == Command:
              return -2, Items, Places
            elif Items[Count].Status == "locked":
              return -3, Items, Places
            Position = GetPositionOfCommand(Items[Count].Commands, Command)
            ResultForCommand = GetResultForCommand(Items[Count].Results, Position)
            Direction, DirectionChange = ExtractResultForCommand(Direction, DirectionChange, ResultForCommand)
            Items = ChangeStatusOfItem(Items, Count, Command)
            Count2 = 0
            ActionWorked = True
            while Count2 < len(Places):
              if Places[Count2].ID == int(CurrentLocation):
                Places = ChangeLocationReference(Direction, int(DirectionChange), Places, Count2, False)
              elif Places[Count2].ID == int(DirectionChange):
                Places = ChangeLocationReference(Direction, CurrentLocation, Places, Count2, True)
              Count2 += 1
            if Items[Count].ID > ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS:
              IndexOfOtherSideOfDoor = GetIndexOfItem("", Items[Count].ID - ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS, Items)
            else:
              IndexOfOtherSideOfDoor = GetIndexOfItem("", Items[Count].ID + ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS, Items)
            Items = ChangeStatusOfItem(Items, IndexOfOtherSideOfDoor, Command)
            Count = len(Items) + 1            
    Count += 1
  if not ActionWorked:
    return -1, Items, Places
  return int(DirectionChange), Items, Places

def GetIndexOfItem(ItemNameToGet, ItemIDToGet, Items):
  Count = 0
  StopLoop = False
  while not StopLoop and Count < len(Items):
    if (ItemIDToGet == -1 and Items[Count].Name == ItemNameToGet) or Items[Count].ID == ItemIDToGet:
      StopLoop = True
    else:
      Count += 1
  if not StopLoop:
    return -1
  else:
    return Count

def ChangeLocationOfItem(Items, IndexOfItem, NewLocation):
  ThisItem = Item()
  ThisItem = Items[IndexOfItem]
  ThisItem.Location = NewLocation
  Items[IndexOfItem] = ThisItem
  return Items

def ChangeStatusOfItem(Items, IndexOfItem, NewStatus):
  ThisItem = Item()
  ThisItem = Items[IndexOfItem]
  ThisItem.Status = NewStatus
  Items[IndexOfItem] = ThisItem
  return Items

def GetRandomNumber(LowerLimitValue, UpperLimitValue):
  return random.randint(LowerLimitValue, UpperLimitValue)
      
def RollDie(Lower, Upper): 
  LowerLimitValue = 0
  if Lower.isnumeric():
    LowerLimitValue = int(Lower)
  else:
    while LowerLimitValue < 1 or LowerLimitValue > 6:
      try:
        LowerLimitValue = int(input("Enter minimum: "))
      except:
        pass
  UpperLimitValue = 0
  if Upper.isnumeric():
    UpperLimitValue = int(Upper)
  else:
    while UpperLimitValue < LowerLimitValue or UpperLimitValue > 6:
      try:
        UpperLimitValue = int(input("Enter maximum: "))
      except:
        pass
  return GetRandomNumber(LowerLimitValue, UpperLimitValue)

def ChangeStatusOfDoor(Items, CurrentLocation, IndexOfItemToLockUnlock, IndexOfOtherSideItemToLockUnlock):
  if CurrentLocation == Items[IndexOfItemToLockUnlock].Location or CurrentLocation == Items[IndexOfOtherSideItemToLockUnlock].Location:
    if Items[IndexOfItemToLockUnlock].Status == "locked":
      Items = ChangeStatusOfItem(Items, IndexOfItemToLockUnlock, "close")
      Items = ChangeStatusOfItem(Items, IndexOfOtherSideItemToLockUnlock, "close")
      Say(Items[IndexOfItemToLockUnlock].Name + " now unlocked.")
    elif Items[IndexOfItemToLockUnlock].Status == "close":
      Items = ChangeStatusOfItem(Items, IndexOfItemToLockUnlock, "locked")
      Items = ChangeStatusOfItem(Items, IndexOfOtherSideItemToLockUnlock, "locked")
      Say(Items[IndexOfItemToLockUnlock].Name + " now locked.")
    else:
      Say(Items[IndexOfItemToLockUnlock].Name + " is open so can't be locked.")
  else:
    Say("Can't use that key in this location.")
  return Items

def UseItem(Items, ItemToUse, CurrentLocation, Places):
  StopGame = False
  SubCommand = ""
  SubCommandParameter = ""
  IndexOfItem = GetIndexOfItem(ItemToUse, -1, Items)
  if IndexOfItem != -1:
    if Items[IndexOfItem].Location == INVENTORY or (Items[IndexOfItem].Location == CurrentLocation and "usable" in Items[IndexOfItem].Status):
      Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "use")
      ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
      SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
      if SubCommand == "say":
        Say(SubCommandParameter)
      elif SubCommand == "lockunlock":
        IndexOfItemToLockUnlock = GetIndexOfItem("", int(SubCommandParameter), Items)
        IndexOfOtherSideItemToLockUnlock = GetIndexOfItem("", int(SubCommandParameter) + ID_DIFFERENCE_FOR_OBJECT_IN_TWO_LOCATIONS, Items)
        Items = ChangeStatusOfDoor(Items, CurrentLocation, IndexOfItemToLockUnlock, IndexOfOtherSideItemToLockUnlock)
      elif SubCommand == "roll":
        Say("You have rolled a " + str(RollDie(ResultForCommand[5], ResultForCommand[7])))
      return StopGame, Items
  print("You can't use that!")
  return StopGame, Items

def ReadItem(Items, ItemToRead, CurrentLocation):
  SubCommand = ""
  SubCommandParameter = ""
  IndexOfItem = GetIndexOfItem(ItemToRead, -1, Items)
  if IndexOfItem == -1:
    print("You can't find " + ItemToRead + ".")
  elif not "read" in Items[IndexOfItem].Commands:
    print("You can't read " + ItemToRead + ".")
  elif Items[IndexOfItem].Location != CurrentLocation and Items[IndexOfItem].Location != INVENTORY:
    print("You can't find " + ItemToRead + ".")
  else:
    Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "read")
    ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
    SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
    if SubCommand == "say":
      Say(SubCommandParameter)
      
def GetItem(Items, ItemToGet, CurrentLocation):
  SubCommand = ""
  SubCommandParameter = ""
  CanGet = False
  IndexOfItem = GetIndexOfItem(ItemToGet, -1, Items)
  if IndexOfItem == -1:
    print("You can't find " + ItemToGet + ".")
  elif Items[IndexOfItem].Location == INVENTORY:
    print("You have already got that!")
  elif not "get" in Items[IndexOfItem].Commands:
    print("You can't get " + ItemToGet + ".")
  elif Items[IndexOfItem].Location >= MINIMUM_ID_FOR_ITEM and Items[GetIndexOfItem("", Items[IndexOfItem].Location, Items)].Location != CurrentLocation:
    print("You can't find " + ItemToGet + ".")
  elif Items[IndexOfItem].Location < MINIMUM_ID_FOR_ITEM and Items[IndexOfItem].Location != CurrentLocation:
    print("You can't find " + ItemToGet + ".")
  else:
    CanGet = True
  if CanGet:
    Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "get")
    ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
    SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
    if SubCommand == "say":
      Say(SubCommandParameter)
    elif SubCommand == "win":
      Say("You have won the game")
      return True, Items
    if "gettable" in Items[IndexOfItem].Status:
      Items = ChangeLocationOfItem(Items, IndexOfItem, INVENTORY)
      print("You have got that now.")
  return False, Items

def CheckIfDiceGamePossible(Items, Characters, OtherCharacterName):
  PlayerHasDie = False
  PlayersInSameRoom = False
  IndexOfPlayerDie = -1
  IndexOfOtherCharacter = -1
  IndexOfOtherCharacterDie = -1
  OtherCharacterHasDie = False
  for Thing in Items:
    if Thing.Location == INVENTORY and "die" in Thing.Name:
      PlayerHasDie = True
      IndexOfPlayerDie = GetIndexOfItem("", Thing.ID, Items)
  Count = 1
  while Count < len(Characters) and not PlayersInSameRoom:
    if Characters[0].CurrentLocation == Characters[Count].CurrentLocation and Characters[Count].Name == OtherCharacterName:
      PlayersInSameRoom = True
      for Thing in Items:
        if Thing.Location == Characters[Count].ID and "die" in Thing.Name:
          OtherCharacterHasDie = True
          IndexOfOtherCharacterDie = GetIndexOfItem("", Thing.ID, Items)
          IndexOfOtherCharacter = Count
    Count += 1
  return PlayerHasDie and PlayersInSameRoom and OtherCharacterHasDie, IndexOfPlayerDie, IndexOfOtherCharacter, IndexOfOtherCharacterDie

def TakeItemFromOtherCharacter(Items, OtherCharacterID):
  ListOfIndicesOfItemsInInventory = []
  ListOfNamesOfItemsInInventory = []
  Count = 0
  while Count < len(Items):
    if Items[Count].Location == OtherCharacterID:
      ListOfIndicesOfItemsInInventory.append(Count)
      ListOfNamesOfItemsInInventory.append(Items[Count].Name)
    Count += 1
  Count = 1
  print("Which item do you want to take?  They have:", end = "")
  print(ListOfNamesOfItemsInInventory[0], end = "")
  while Count < len(ListOfNamesOfItemsInInventory) - 1:
    print(",", ListOfNamesOfItemsInInventory[Count], end = "")
    Count += 1
  print(".")
  ChosenItem = input()
  if ChosenItem in ListOfNamesOfItemsInInventory:
    print("You have that now.")
    Pos = ListOfNamesOfItemsInInventory.index(ChosenItem)
    Items = ChangeLocationOfItem(Items, ListOfIndicesOfItemsInInventory[Pos], INVENTORY)
  else:
    print("They don't have that item, so you don't take anything this time.")
  return Items

def TakeRandomItemFromPlayer(Items, OtherCharacterID):
  ListOfIndicesOfItemsInInventory = []
  Count = 0
  while Count < len(Items):
    if Items[Count].Location == INVENTORY:
      ListOfIndicesOfItemsInInventory.append(Count)
    Count += 1
  rno = GetRandomNumber(0, len(ListOfIndicesOfItemsInInventory) - 1)
  print("They have taken your " + Items[ListOfIndicesOfItemsInInventory[rno]].Name + ".")
  Items = ChangeLocationOfItem(Items, ListOfIndicesOfItemsInInventory[rno], OtherCharacterID)
  return Items

def PlayDiceGame(Characters, Items, OtherCharacterName):
  PlayerScore = 0
  OtherCharacterScore = 0
  DiceGamePossible, IndexOfPlayerDie, IndexOfOtherCharacter, IndexOfOtherCharacterDie = CheckIfDiceGamePossible(Items, Characters, OtherCharacterName)
  if not DiceGamePossible:
    print("You can't play a dice game.")
  else:
    Position = GetPositionOfCommand(Items[IndexOfPlayerDie].Commands, "use")
    ResultForCommand = GetResultForCommand(Items[IndexOfPlayerDie].Results, Position)
    PlayerScore = RollDie(ResultForCommand[5], ResultForCommand[7])
    print("You rolled a " + str(PlayerScore) + ".")
    Position = GetPositionOfCommand(Items[IndexOfOtherCharacterDie].Commands, "use")
    ResultForCommand = GetResultForCommand(Items[IndexOfOtherCharacterDie].Results, Position)
    OtherCharacterScore = RollDie(ResultForCommand[5], ResultForCommand[7])
    print("They rolled a " + str(OtherCharacterScore) + ".")
    if PlayerScore > OtherCharacterScore:
      print("You win!")
      Items = TakeItemFromOtherCharacter(Items, Characters[IndexOfOtherCharacter].ID)
    elif PlayerScore < OtherCharacterScore:
      print("You lose!")
      Items = TakeRandomItemFromPlayer(Items, Characters[IndexOfOtherCharacter].ID)
    else:
      print("Draw!")
  return Items
      
def MoveItem(Items, ItemToMove, CurrentLocation):
  SubCommand = ""
  SubCommandParameter = ""
  IndexOfItem = GetIndexOfItem(ItemToMove, -1, Items)
  if IndexOfItem != -1:
    if Items[IndexOfItem].Location == CurrentLocation:
      if len(Items[IndexOfItem].Commands) >= 4:
        if "move" in Items[IndexOfItem].Commands:
          Position = GetPositionOfCommand(Items[IndexOfItem].Commands, "move")
          ResultForCommand = GetResultForCommand(Items[IndexOfItem].Results, Position)
          SubCommand, SubCommandParameter = ExtractResultForCommand(SubCommand, SubCommandParameter, ResultForCommand)
          if SubCommand == "say":
            Say(SubCommandParameter)
          else:
            print("You can't move " + ItemToMove + ".")
        else:
          print("You can't move " + ItemToMove + ".")
      return
  print("You can't find " + ItemToMove + ".")

def DisplayInventory(Items):
  print()
  print("You are currently carrying the following items:")
  for Thing in Items:
    if Thing.Location == INVENTORY:
      print(Thing.Name)
    
def DisplayGettableItemsInLocation(Items, CurrentLocation):
  ContainsGettableItems = False
  ListOfItems = "On the floor there is: "
  for Thing in Items:
    if Thing.Location == CurrentLocation and "gettable" in Thing.Status:
      if ContainsGettableItems:
        ListOfItems += ", "
      ListOfItems += Thing.Name
      ContainsGettableItems = True
  if ContainsGettableItems:
    print(ListOfItems + ".")
    
def DisplayOpenCloseMessage(ResultOfOpenClose, OpenCommand):
  if ResultOfOpenClose >= 0:
    if OpenCommand:
      Say("You have opened it.")
    else:
      Say("You have closed it.")
  elif ResultOfOpenClose == -3:
    Say("You can't do that, it is locked.")
  elif ResultOfOpenClose == -2:
    Say("It already is.")
  elif ResultOfOpenClose == -1:
    Say("You can't open that.")
       
def PlayGame(Characters, Items, Places):
  StopGame = False
  Moved = True
  while not StopGame:
    if Moved:
      print()
      print()
      print(Places[Characters[0].CurrentLocation - 1].Description)
      DisplayGettableItemsInLocation(Items, Characters[0].CurrentLocation)
      Moved = False
    Instruction = GetInstruction()
    Command, Instruction = ExtractCommand(Instruction)
    if Command == "get":
      StopGame, Items = GetItem(Items, Instruction, Characters[0].CurrentLocation)
    elif Command == "use":
      StopGame, Items = UseItem(Items, Instruction, Characters[0].CurrentLocation, Places)
    elif Command == "go":
      Characters[0], Moved = Go(Characters[0], Instruction, Places[Characters[0].CurrentLocation - 1])
    elif Command == "read":
      ReadItem(Items, Instruction, Characters[0].CurrentLocation)
    elif Command == "examine":
      Examine(Items, Characters, Instruction, Characters[0].CurrentLocation, Places)
    elif Command == "open":
      ResultOfOpenClose, Items, Places = OpenClose(True, Items, Places, Instruction, Characters[0].CurrentLocation)
      DisplayOpenCloseMessage(ResultOfOpenClose, True)
    elif Command == "close":
      ResultOfOpenClose, Items, Places = OpenClose(False, Items, Places, Instruction, Characters[0].CurrentLocation)
      DisplayOpenCloseMessage(ResultOfOpenClose, False)
    elif Command == "move":
      MoveItem(Items, Instruction, Characters[0].CurrentLocation)
    elif Command == "say":
      Say(Instruction)
    elif Command == "playdice":
      Items = PlayDiceGame(Characters, Items, Instruction)
    elif Command == "quit":
      Say("You decide to give up, try again another time.")
      StopGame = True
    elif Command == "help":
      ShowHelp()
    else:
      print("Sorry, you don't know how to " + Command + ".")
  input()

def LoadGame(Filename, Characters, Items, Places):
  try:
    f = open(Filename, "rb")
    NoOfCharacters = pickle.load(f)
    for Count in range(NoOfCharacters):
      TempCharacter = Character()
      TempCharacter.ID = pickle.load(f)
      TempCharacter.Name = pickle.load(f)
      TempCharacter.Description = pickle.load(f)
      TempCharacter.CurrentLocation = pickle.load(f)
      Characters.append(TempCharacter)
    NoOfPlaces = pickle.load(f)
    for Count in range(0, NoOfPlaces):
      TempPlace = Place()
      TempPlace.ID = pickle.load(f)
      TempPlace.Description = pickle.load(f)
      TempPlace.North = pickle.load(f)
      TempPlace.East = pickle.load(f)
      TempPlace.South = pickle.load(f)
      TempPlace.West = pickle.load(f)
      TempPlace.Up = pickle.load(f)
      TempPlace.Down = pickle.load(f)
      Places.append(TempPlace)
    NoOfItems = pickle.load(f)
    for Count in range(0, NoOfItems):
      TempItem = Item()
      TempItem.ID = pickle.load(f)
      TempItem.Description = pickle.load(f)
      TempItem.Status = pickle.load(f)
      TempItem.Location = pickle.load(f)
      TempItem.Name = pickle.load(f)
      TempItem.Commands = pickle.load(f)
      TempItem.Results = pickle.load(f)
      Items.append(TempItem)
    return True, Characters, Items, Places
  except:
    return False, Characters, Items, Places

def Main():
  Items = []
  Characters = []
  Places = []
  Filename = input("Enter filename> ") + ".gme"
  print()
  GameLoaded, Characters, Items, Places = LoadGame(Filename, Characters, Items, Places)
  if GameLoaded:
    PlayGame(Characters, Items, Places)
  else:
    print("Unable to load game.")
    input()


def ShowHelp():
  print("You can enter one of the following commands:")
  print("go, get, use, examine, say, quit, read, move, open, close and playdice")


if __name__ == "__main__":
  Main()