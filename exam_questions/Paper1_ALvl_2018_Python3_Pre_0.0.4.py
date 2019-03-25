# Skeleton Program code for the AQA A Level Paper 1 2018 examination
# this code should be used in conjunction with the Preliminary Material
# written by the AQA Programmer Team
# developed using Python 3.5.1

import random

class QueueOfTiles():
  def __init__(self, MaxSize):
    self._Contents = []
    self._Rear = -1
    self._MaxSize = MaxSize
    for Count in range(self._MaxSize):
      self._Contents.append("")
      self.Add()
      
  def IsEmpty(self):
    if self._Rear == -1:
      return True
    else:
      return False

  def Remove(self):
    if self.IsEmpty():
      return None
    else:
      Item = self._Contents[0]
      for Count in range (1, self._Rear + 1):
        self._Contents[Count - 1] = self._Contents[Count]
      self._Contents[self._Rear] = ""
      self._Rear -= 1
      return Item

  def Add(self):
    if self._Rear < self._MaxSize - 1:
      RandNo = random.randint(0, 25)
      self._Rear += 1
      self._Contents[self._Rear] = chr(65 + RandNo)

  def Show(self):
    if self._Rear != -1:
      print()
      print("The contents of the queue are: ", end="")
      for Item in self._Contents:
        print(Item, end="")
      print()

def CreateTileDictionary():
  TileDictionary = dict()
  for Count in range(26):
    if Count in [0, 4, 8, 13, 14, 17, 18, 19]:
      TileDictionary[chr(65 + Count)] = 1
    elif Count in [1, 2, 3, 6, 11, 12, 15, 20]:
      TileDictionary[chr(65 + Count)] = 2
    elif Count in [5, 7, 22]:
      TileDictionary[chr(65 + Count)] = 3
    elif Count in [10, 21, 24]:
      TileDictionary[chr(65 + Count)] = 4
    else:
      TileDictionary[chr(65 + Count)] = 5
  return TileDictionary
    
def DisplayTileValues(TileDictionary, AllowedWords):
  print()
  print("TILE VALUES")
  print()  
  for Letter, Points in TileDictionary.items():
    print("Points for " + Letter + ": " + str(Points))
  print()

def GetStartingHand(TileQueue, StartHandSize):
  Hand = ""
  for Count in range(StartHandSize):
    Hand += TileQueue.Remove()
    TileQueue.Add()
  return Hand

def LoadAllowedWords():
  AllowedWords = []
  try:
    WordsFile = open("aqawords.txt", "r")
    for Word in WordsFile:
      AllowedWords.append(Word.strip().upper())
    WordsFile.close()
  except:
    pass
  return AllowedWords

def CheckWordIsInTiles(Word, PlayerTiles):
  InTiles = True
  CopyOfTiles = PlayerTiles
  for Count in range(len(Word)):
    if Word[Count] in CopyOfTiles:
      CopyOfTiles = CopyOfTiles.replace(Word[Count], "", 1)
    else:
      InTiles = False
  return InTiles 

def CheckWordIsValid(Word, AllowedWords):
  ValidWord = False
  Count = 0
  while Count < len(AllowedWords) and not ValidWord:
    if AllowedWords[Count] == Word:
      ValidWord = True
    Count += 1
  return ValidWord

def AddEndOfTurnTiles(TileQueue, PlayerTiles, NewTileChoice, Choice):
  if NewTileChoice == "1":
    NoOfEndOfTurnTiles = len(Choice)
  elif NewTileChoice == "2":
    NoOfEndOfTurnTiles = 3    
  else:
    NoOfEndOfTurnTiles = len(Choice) + 3
  for Count in range(NoOfEndOfTurnTiles):
    PlayerTiles += TileQueue.Remove()
    TileQueue.Add()
  return TileQueue, PlayerTiles  

def FillHandWithTiles(TileQueue, PlayerTiles, MaxHandSize):
  while len(PlayerTiles) <= MaxHandSize:
    PlayerTiles += TileQueue.Remove()
    TileQueue.Add()
  return TileQueue, PlayerTiles  

def GetScoreForWord(Word, TileDictionary):
  Score = 0
  for Count in range (len(Word)):
    Score += TileDictionary[Word[Count]]
  if len(Word) > 7:
    Score += 20
  elif len(Word) > 5:
    Score += 5
  elif len(Word) < 4:
    Score -= 1
  return Score
  
def UpdateAfterAllowedWord(Word, PlayerTiles, PlayerScore, PlayerTilesPlayed, TileDictionary, AllowedWords):
  PlayerTilesPlayed += len(Word)
  for Letter in Word:
    PlayerTiles = PlayerTiles.replace(Letter, "", 1)
  PlayerScore += GetScoreForWord(Word, TileDictionary)
  return PlayerTiles, PlayerScore, PlayerTilesPlayed
      
def UpdateScoreWithPenalty(PlayerScore, PlayerTiles, TileDictionary):
  for Count in range (len(PlayerTiles)):
    PlayerScore -= TileDictionary[PlayerTiles[Count]]  
  return PlayerScore

def GetChoice():
  print()
  print("Either:")
  print("     enter the word you would like to play OR")
  print("     press 1 to display the letter values OR")
  print("     press 4 to view the tile queue OR")
  print("     press 7 to view your tiles again OR")
  print("     press 0 to fill hand and stop the game.")
  Choice = input(">")
  print()
  Choice = Choice.upper()
  return Choice

def GetNewTileChoice():
  NewTileChoice = ""
  while NewTileChoice not in ["1", "2", "3", "4"]:
    print("Do you want to:")
    print("     replace the tiles you used (1) OR")
    print("     get three extra tiles (2) OR")
    print("     replace the tiles you used and get three extra tiles (3) OR")
    print("     get no new tiles (4)?")
    NewTileChoice = input(">")
  return NewTileChoice

def DisplayTilesInHand(PlayerTiles, TileDictionary):
  print()
  print("Your current hand:", PlayerTiles)
  for tile in PlayerTiles:
    print("{}({})".format(tile, TileDictionary[tile]), end=" ")

  
def HaveTurn(PlayerName, PlayerTiles, PlayerTilesPlayed, PlayerScore, TileDictionary, TileQueue, AllowedWords, MaxHandSize, NoOfEndOfTurnTiles):
  print()
  print(PlayerName, "it is your turn.")
  DisplayTilesInHand(PlayerTiles, TileDictionary)
  NewTileChoice = "2"
  ValidChoice = False
  while not ValidChoice:
    Choice = GetChoice()
    if Choice == "1":
      DisplayTileValues(TileDictionary, AllowedWords)
    elif Choice == "4":
      TileQueue.Show()
    elif Choice == "7":
      DisplayTilesInHand(PlayerTiles)      
    elif Choice == "0":
      ValidChoice = True
      TileQueue, PlayerTiles = FillHandWithTiles(TileQueue, PlayerTiles, MaxHandSize)
    else:
      ValidChoice = True
      if len(Choice) == 0:
        ValidWord = False
      else:
        ValidWord = CheckWordIsInTiles(Choice, PlayerTiles)
      if ValidWord:
        ValidWord = CheckWordIsValid(Choice, AllowedWords)
        if ValidWord:
          print()
          print("Valid word. {} scores {} points".format(Choice, GetScoreForWord(Choice, TileDictionary)))
          print()
          PlayerTiles, PlayerScore, PlayerTilesPlayed = UpdateAfterAllowedWord(Choice, PlayerTiles, PlayerScore, PlayerTilesPlayed, TileDictionary, AllowedWords)
          NewTileChoice = GetNewTileChoice()
      if not ValidWord:
        print()
        print("Not a valid attempt, you lose your turn.")
        print()
      if NewTileChoice != "4":
        TileQueue, PlayerTiles = AddEndOfTurnTiles(TileQueue, PlayerTiles, NewTileChoice, Choice)
      print()
      print("Your word was:", Choice)
      print("Your new score is:", PlayerScore)
      print("You have played", PlayerTilesPlayed, "tiles so far in this game.")
  return PlayerTiles, PlayerTilesPlayed, PlayerScore, TileQueue  

def DisplayWinner(PlayerOneScore, PlayerTwoScore, PlayerThreeScore):
  print()
  print("**** GAME OVER! ****")
  print()
  print("Player One your score is", PlayerOneScore)
  print("Player Two your score is", PlayerTwoScore)
  print("Player Three your scrore is", PlayerThreeScore)
  if PlayerOneScore > PlayerTwoScore and PlayerOneScore > PlayerThreeScore:
    print("Player One wins!")
  elif PlayerTwoScore > PlayerOneScore and PlayerTwoScore > PlayerThreeScore:
    print("Player Two wins!")
  elif PlayerThreeScore > PlayerOneScore and PlayerThreeScore > PlayerTwoScore:
    print("Player Three wins!")
  elif PlayerOneScore == PlayerTwoScore or PlayerOneScore == PlayerThreeScore or PlayerTwoScore == PlayerThreeScore:
    print("No clear winner")
  print()
  
def PlayGame(AllowedWords, TileDictionary, RandomStart, StartHandSize, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles):
  PlayerOneScore = 50
  PlayerTwoScore = 50
  PlayerThreeScore = 50
  PlayerOneTilesPlayed = 0
  PlayerTwoTilesPlayed = 0
  PlayerThreeTilesPlayed = 0
  TileQueue = QueueOfTiles(20)
  if RandomStart:
    PlayerOneTiles = GetStartingHand(TileQueue, StartHandSize)
    PlayerTwoTiles = GetStartingHand(TileQueue, StartHandSize)
    PlayerThreeTiles = GetStartingHand(TileQueue, StartHandSize)
  else:
    PlayerOneTiles = "BTAHANDENONSARJ"
    PlayerTwoTiles = "CELZXIOTNESMUAA"
    PlayerThreeTiles = "ABCDEFGHIJKLMNO"
  while PlayerOneTilesPlayed <= MaxTilesPlayed and PlayerTwoTilesPlayed <= MaxTilesPlayed and PlayerThreeTilesPlayed <= MaxTilesPlayed and len(PlayerOneTiles) < MaxHandSize and len(PlayerTwoTiles) < MaxHandSize and len(PlayerThreeTiles) < MaxHandSize:
    PlayerOneTiles, PlayerOneTilesPlayed, PlayerOneScore, TileQueue = HaveTurn("Player One", PlayerOneTiles, PlayerOneTilesPlayed, PlayerOneScore, TileDictionary, TileQueue, AllowedWords, MaxHandSize, NoOfEndOfTurnTiles)
    print()
    input("Press Enter to continue")
    print()
    PlayerTwoTiles, PlayerTwoTilesPlayed, PlayerTwoScore, TileQueue = HaveTurn("Player Two", PlayerTwoTiles, PlayerTwoTilesPlayed, PlayerTwoScore, TileDictionary, TileQueue, AllowedWords, MaxHandSize, NoOfEndOfTurnTiles)
    print()
    input("Press Enter to continue")
    print()
    PlayerThreeTiles, PlayerThreeTilesPlayed, PlayerThreeScore, TileQueue = HaveTurn("Player Three", PlayerThreeTiles, PlayerThreeTilesPlayed, PlayerThreeScore, TileDictionary, TileQueue, AllowedWords, MaxHandSize, NoOfEndOfTurnTiles)

  PlayerOneScore = UpdateScoreWithPenalty(PlayerOneScore, PlayerOneTiles, TileDictionary)
  PlayerTwoScore = UpdateScoreWithPenalty(PlayerTwoScore, PlayerTwoTiles, TileDictionary)
  PlayerThreeScore = UpdateScoreWithPenalty(PlayerThreeScore, PlayerThreeTiles, TileDictionary)
  DisplayWinner(PlayerOneScore, PlayerTwoScore, PlayerThreeScore)

def DisplayMenu():
  print()
  print("=========")
  print("MAIN MENU")
  print("=========")
  print()
  print("1. Play game with random start hand")
  print("2. Play game with training start hand")
  print("9. Quit")
  print()
  
def Main():
  print("++++++++++++++++++++++++++++++++++++++")
  print("+ Welcome to the WORDS WITH AQA game +")
  print("++++++++++++++++++++++++++++++++++++++")
  print()
  print()
  AllowedWords = LoadAllowedWords()
  TileDictionary = CreateTileDictionary()
  MaxHandSize = 20
  MaxTilesPlayed = 50
  NoOfEndOfTurnTiles = 3
  StartHandSize = 15
  Choice = ""
  while Choice != "9":
    DisplayMenu()
    Choice = input("Enter your choice: ")
    if Choice == "1":
      PlayGame(AllowedWords, TileDictionary, True, StartHandSize, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles)
    elif Choice == "2":
      PlayGame(AllowedWords, TileDictionary, False, 15, MaxHandSize, MaxTilesPlayed, NoOfEndOfTurnTiles)
      
if __name__ == "__main__":
  Main()
