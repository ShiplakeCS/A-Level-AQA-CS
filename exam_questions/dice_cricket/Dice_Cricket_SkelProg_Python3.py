# Skeleton Program code for the AQA COMP1 Summer 2011 examination
# This code should be used in conjunction with the Preliminary Material
# Written by the AQA Programmer Team developed in the 
# Python 3.1 programming environment

import random

MAX_SIZE = 4

class TopScore():
  # Creates object with accessible Name and Score properties
  def __init__(self):
    self.Name = "-"
    self.Score = 0

def ResetTopScores(TopScores):
  # adds 4 blank TopScore objects to TopScores list, setting properties
  for Count in range(1,MAX_SIZE + 1):
    TopScores.append(TopScore())

def GetValidPlayerName():
  PlayerName = input()
  while (PlayerName == ""):
    PlayerName = input("That was not a valid name.  Please try again: ")
  return PlayerName

def DisplayMenu():
  print()
  print("Dice Cricket")
  print()
  print("1. Play game version with virtual dice")
  print("2. Play game version with real dice")
  print("3. Load top scores")
  print("4. Display top scores")
  print("5. Save top scores")
  print("9. Quit")
  print()

def GetMenuChoice():
  OptionChosen = int(input("Please enter your choice: "))
  if (OptionChosen < 1 or (OptionChosen > 5 and OptionChosen != 9)):
    print()
    print("That was not one of the allowed options. Please try again: ")
  return OptionChosen

def RollBowlDie(VirtualDiceGame):
  if VirtualDiceGame:
    BowlDieResult = random.randint(1,6)
  else:
    print("Please roll the bowling die and then enter your result.")
    print()
    print("Enter 1 if the result is a 1")
    print("Enter 2 if the result is a 2")
    print("Enter 3 if the result is a 4")
    print("Enter 4 if the result is a 6")
    print("Enter 5 if the result is a 0")
    print("Enter 6 if the result is OUT")
    print()

    BowlDieResult = int(input("Result: "))

    while BowlDieResult < 1 or BowlDieResult > 6:

      print("Please enter a value between 1 and 6 only.")
      BowlDieResult = int(input("Result: "))

    print()

  return BowlDieResult

def CalculateRunsScored(BowlDieResult):
  if BowlDieResult == 1:
    RunsScored = 1
  elif BowlDieResult == 2:
    RunsScored = 2
  elif BowlDieResult == 3:
    RunsScored = 4
  elif BowlDieResult == 4:
    RunsScored = 6
  elif BowlDieResult == 5 or 6:
    RunsScored = 0
  return RunsScored

def DisplayRunsScored(RunsScored):
  if RunsScored == 1:
    print("You got one run!")
  elif RunsScored == 2:
    print("You got two runs!")
  elif RunsScored == 4:
    print("You got four runs!")
  elif RunsScored == 6:
    print("You got six runs!")

def DisplayCurrentPlayerNewScore(CurrentPlayerScore):
  print("Your new score is: ", str(CurrentPlayerScore))

def RollAppealDie(VirtualDiceGame):
  if VirtualDiceGame:
    AppealDieResult = random.randint(1,5)
  else:
    print("Please roll the appeal die and then enter your result.")
    print()
    print("Enter 1 if the result is NOT OUT")
    print("Enter 2 if the result is CAUGHT")
    print("Enter 3 if the result is LBW")
    print("Enter 4 if the result is BOWLED")
    print("Enter 5 if the result is RUN OUT")
    print()
    AppealDieResult = int(input("Result: "))
    print()
  return AppealDieResult

def DisplayAppealDieResult(AppealDieResult):
  if AppealDieResult == 1:
    print("Not Out!")
  elif AppealDieResult == 2:
    print("Caught!")
  elif AppealDieResult == 3:
    print("LBW!")
  elif AppealDieResult == 4:
    print("Bowled!")
  elif AppealDieResult == 5:
    print("Run Out!")

def DisplayResult(PlayerOneName, PlayerOneScore, PlayerTwoName, PlayerTwoScore):
  print()
  print(PlayerOneName, "your score was:", PlayerOneScore) 
  print(PlayerTwoName, "your score was:", PlayerTwoScore)
  print()
  if PlayerOneScore > PlayerTwoScore:
    print(PlayerOneName, "wins!")
  elif PlayerTwoScore > PlayerOneScore:
    print(PlayerTwoName, "wins!")
  else:
    print("It's a draw!")
  print()

def UpdateTopScores(TopScores, PlayerName, PlayerScore):
  LowestCurrentTopScore = TopScores[1].Score
  PositionOfLowestCurrentTopScore = 1
  # Find the lowest of the current top scores
  for Count in range(2, MAX_SIZE + 1):
    if TopScores[Count].Score < LowestCurrentTopScore:
      LowestCurrentTopScore = TopScores[Count].Score
      PositionOfLowestCurrentTopScore = Count
  if PlayerScore > LowestCurrentTopScore:
    TopScores[PositionOfLowestCurrentTopScore].Score = PlayerScore
    TopScores[PositionOfLowestCurrentTopScore].Name = PlayerName
    print("Well done", PlayerName, "you have one of the top scores!")

def DisplayTopScores(TopScores):
  print("The current top scores are: ")
  print()
  for Count in range(1, MAX_SIZE + 1):
    print(TopScores[Count].Name, TopScores[Count].Score)
  print()
  input("Press the Enter key to return to the main menu")
    

def LoadTopScores(TopScores):
  CurrentFile = open("HiScores.txt","r")
  for Count in range (1, MAX_SIZE + 1):
    ValuesOnLine = [None, "", ""]
    LineFromFile = CurrentFile.readline()
    Count2 = 0
    while LineFromFile[Count2] != ",":
      ValuesOnLine[1] += LineFromFile[Count2]
      Count2 += 1
    Count2 += 1
    while Count2 < len(LineFromFile):
      ValuesOnLine[2] += LineFromFile[Count2]
      Count2 += 1
    TopScores[Count].Name = ValuesOnLine[1]
    TopScores[Count].Score = int(ValuesOnLine[2])
  CurrentFile.close()

def PlayDiceGame(PlayerOneName, PlayerTwoName, VirtualDiceGame, TopScores):
  for PlayerNo in [1,2]:
    CurrentPlayerScore = 0
    PlayerOut = False
    if PlayerNo == 1:
      print(PlayerOneName, "is batting")
    else:
      print(PlayerTwoName, "is batting")
    print()
    input("Press the Enter key to continue")
    print()
    while not PlayerOut:
      BowlDieResult = RollBowlDie(VirtualDiceGame)
      if BowlDieResult in [1,2,3,4]:
        RunsScored = CalculateRunsScored(BowlDieResult)
        DisplayRunsScored(RunsScored)
        CurrentPlayerScore += RunsScored
        print("Your new score is:", CurrentPlayerScore)
      if BowlDieResult == 5:
        print("No runs scored this time. Your score is still:", CurrentPlayerScore)
      if BowlDieResult == 6:
        input("This could be out... press the Enter key to find out.")
        print()
        AppealDieResult = RollAppealDie(VirtualDiceGame)
        DisplayAppealDieResult(AppealDieResult)
        if AppealDieResult >= 2:
          PlayerOut = True
        else:
          PlayerOut = False
      print()
      input("Press the Enter key to continue")
      print()
    print("You are out. Your final score was:", CurrentPlayerScore)
    print()
    input("Press the Enter key to continue")
    print()
    if PlayerNo == 1:
      PlayerOneScore = CurrentPlayerScore
    else:
      PlayerTwoScore = CurrentPlayerScore
  DisplayResult(PlayerOneName, PlayerOneScore, PlayerTwoName, PlayerTwoScore)
  if PlayerOneScore >= PlayerTwoScore:
    UpdateTopScores(TopScores, PlayerOneName, PlayerOneScore)
    UpdateTopScores(TopScores, PlayerTwoName, PlayerTwoScore)
  else:
    UpdateTopScores(TopScores, PlayerTwoName, PlayerTwoScore)
    UpdateTopScores(TopScores, PlayerOneName, PlayerOneScore)
  print()
  input("Press the Enter key to continue")
                  

def SaveTopScores(TopScores):
  with open("HiScores.txt", "w") as scores_file:
    for i in range(1, MAX_SIZE + 1):
      scores_file.write("{},{}\n".format(TopScores[i].Name, TopScores[i].Score))
    #for score in TopScores:
    #  scores_file.write("{},{}\n".format(score.Name, score.Score))


if __name__ == "__main__":
  TopScores = [None] # list structure with index 0 set to "None" as this will not be used
  ResetTopScores(TopScores)
  print("What is player one's name? ")
  PlayerOneName = GetValidPlayerName()
  print("What is player two's name? ")
  PlayerTwoName = GetValidPlayerName()
  OptionSelected = 0
  while OptionSelected != 9:
    DisplayMenu()
    OptionSelected = GetMenuChoice()
    while OptionSelected not in [1,2,3,4,5,9]:
      DisplayMenu()
      OptionSelected = GetMenuChoice()
    print()
    if OptionSelected in [1,2,3,4,5]:
      if OptionSelected == 1:
        PlayDiceGame(PlayerOneName, PlayerTwoName, True, TopScores)
      elif OptionSelected == 2:
        PlayDiceGame(PlayerOneName, PlayerTwoName, False, TopScores)
      elif OptionSelected == 3:
        LoadTopScores(TopScores)
      elif OptionSelected == 5:
        SaveTopScores(TopScores)
      else:
        DisplayTopScores(TopScores)