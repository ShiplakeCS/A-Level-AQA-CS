#Skeleton Program code for the AQA A Level Paper 1 Summer 2020 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.5.1 programming environment

import math
import random

class Household:
  _NextID = 1

  def __init__(self, X, Y):
    self._XCoord = X
    self._YCoord = Y
    self._ChanceEatOutPerDay = random.random()
    self._ID = Household._NextID
    Household._NextID += 1

  def GetDetails(self):
    Details = str(self._ID) + "     Coordinates: (" + str(self._XCoord) + ", " + str(self._YCoord) + ")     Eat out probability: " + str(self._ChanceEatOutPerDay)
    return Details

  def GetChanceEatOut(self):
    return self._ChanceEatOutPerDay

  def GetX(self):
    return self._XCoord

  def GetY(self):
    return self._YCoord

class Settlement:
  def __init__(self):
    self._XSize = 1000
    self._YSize = 1000
    self._StartNoOfHouseholds = 250
    self._Households = []
    self._CreateHouseholds()

  def GetHouseholds(self):
    return self._Households

  def GetNumberOfHouseholds(self):
    return len(self._Households)

  def GetXSize(self):
    return self._XSize

  def GetYSize(self):
    return self._YSize

  def GetRandomLocation(self):

    X = random.randint(0, self._XSize - 1)
    Y = random.randint(0, self._YSize - 1)

    for house in self._Households:
      if house.GetX() == X and house.GetY() == Y:
        X, Y = self.GetRandomLocation()
        break

    return X, Y



  def _CreateHouseholds(self):
    for Count in range (0, self._StartNoOfHouseholds):
      self.AddHousehold()

  def AddHousehold(self):
    X, Y = self.GetRandomLocation()
    Temp = Household(X, Y)
    self._Households.append(Temp)

  def RemoveHousehold(self):
    removeHouseholdNumber = random.randint(0, len(self._Households) - 1)
    del self._Households[removeHouseholdNumber]


  def DisplayHouseholds(self):
    print("\n**********************************")
    print("*** Details of all households: ***")
    print("**********************************\n")
    for H in self._Households:
      print(H.GetDetails())
    print()

  def FindOutifHouseholdEatsOut(self, HouseholdNo):
    EatOutRNo = random.random()
    X = self._Households[HouseholdNo].GetX()
    Y = self._Households[HouseholdNo].GetY()
    if EatOutRNo < self._Households[HouseholdNo].GetChanceEatOut():
      return True, X, Y
    else:
      return False, X, Y

class LargeSettlement(Settlement):
  def __init__(self, ExtraXSize, ExtraYSize, ExtraHouseholds):
    super(LargeSettlement, self).__init__()
    self._XSize += ExtraXSize
    self._YSize += ExtraYSize
    self._StartNoOfHouseholds += ExtraHouseholds
    for Count in range (1, ExtraHouseholds + 1):
      self.AddHousehold()

class Outlet:
  def __init__(self, XCoord, YCoord, MaxCapacityBase, ParentCompay):
    self._XCoord = XCoord
    self._YCoord = YCoord
    self._Capacity = int(MaxCapacityBase * 0.6)
    self._MaxCapacity = MaxCapacityBase + random.randint(0, 49) - random.randint(0, 49)
    self._DailyCosts = MaxCapacityBase * 0.2 + self._Capacity * 0.5 + 100
    self._DeliveryCosts = 0.0
    self._ParentCompany = ParentCompay
    self.NewDay()

  def GetCapacity(self):
    return self._Capacity

  def GetX(self):
    return self._XCoord

  def GetY(self):
    return self._YCoord

  def AlterDailyCost(self, Amount):
    self._DailyCosts += Amount

  def AlterCapacity(self, Change):
    OldCapacity = self._Capacity
    self._Capacity += Change
    if self._Capacity > self._MaxCapacity:
      self._Capacity = self._MaxCapacity
      return self._MaxCapacity - OldCapacity
    elif self._Capacity < 0:
      self._Capacity = 0
    self._DailyCosts = self._MaxCapacity * 0.2 + self._Capacity * 0.5 + 100
    return Change

  def IncrementVisits(self):
    if self._VisitsToday < self._Capacity:
      self._VisitsToday += 1
    else:
      self._ParentCompany.AlterReputation(-0.05)

      print(f"Cannot visit outlet, daily capacity reached: {self._Capacity}")


  def NewDay(self):
    self._VisitsToday = 0
    self._DeliveryCosts = 0.0

  def CalculateDailyProfitLoss(self, AvgCostPerMeal, AvgPricePerMeal):
    return (AvgPricePerMeal - AvgCostPerMeal) * self._VisitsToday - self._DailyCosts - self._DeliveryCosts

  def GetDetails(self):
    Details = "Coordinates: (" + str(self._XCoord) + ", " + str(self._YCoord) + ")     Capacity: " + str(self._Capacity) + "      Maximum Capacity: "
    Details += str(self._MaxCapacity) + "      Daily Costs: " + str(self._DailyCosts) + "      Visits today: " + str(self._VisitsToday)
    Details += "\tDelivery Costs: " + str(self._DeliveryCosts)
    return Details

  def AddDelivery(self, Distance, FuelCost):
    self.IncrementVisits()
    self._DeliveryCosts += Distance * FuelCost


class Company:
  def __init__(self, Name, Category, Balance, X, Y, FuelCostPerUnit, BaseCostOfDelivery, Settlement):
    self._Outlets = []
    self._SimulationSettlement = Settlement
    self._FamilyOutletCost = 1000
    self._FastFoodOutletCost = 2000
    self._NamedChefOutletCost = 15000
    self._FamilyFoodOutletCapacity = 150
    self._FastFoodOutletCapacity = 200        
    self._NamedChefOutletCapacity = 50
    self._Name = Name
    self._Category = Category
    self._Balance = Balance
    self._FuelCostPerUnit = FuelCostPerUnit
    self._BaseCostOfDelivery = BaseCostOfDelivery
    self._ReputationScore = 100
    self._DailyCosts = 100
    if self._Category == "fast food":
      self._AvgCostPerMeal = 5
      self._AvgPricePerMeal = 10
      self._ReputationScore += random.random() * 10 - 8
    elif self._Category == "family":
      self._AvgCostPerMeal = 12
      self._AvgPricePerMeal = 14
      self._ReputationScore += random.random() * 30 - 5
    else:
      self._AvgCostPerMeal = 20
      self._AvgPricePerMeal = 40
      self._ReputationScore += random.random() * 50
    self.OpenOutlet(X, Y)

  def GetName(self):
    return self._Name

  def GetNumberOfOutlets(self):
    return len(self._Outlets)

  def GetReputationScore(self):
    return self._ReputationScore

  def AlterDailyCosts(self, Change):
    self._DailyCosts += Change

  def AlterAvgCostPerMeal(self, Change):
    self._AvgCostPerMeal += Change
        
  def AlterFuelCostPerUnit(self, Change):
    self._FuelCostPerUnit += Change

  def AlterReputation(self, Change):
    self._ReputationScore += Change

  def NewDay(self):
    for O in self._Outlets:
      O.NewDay()
           
  def AddVisitToNearestOutlet(self, X, Y):
    o, distance = self.GetNearestOutlet(X, Y)
    o.IncrementVisits()

  def CloseAllOutlets(self):
    AllClosed = False
    while not AllClosed:
      AllClosed = self.CloseOutlet(0)


  def GetDetails(self):
    Details = ""
    Details += "Name: " + self._Name + "\nType of business: " + self._Category + "\n"
    Details += "Current balance: " + str(self._Balance) + "\nAverage cost per meal: " + str(self._AvgCostPerMeal) + "\n"
    Details += "Average price per meal: " + str(self._AvgPricePerMeal) + "\nDaily costs: " + str(self._DailyCosts) + "\n"
    Details += "Delivery costs: " + str(self.CalculateDeliveryCost()) + "\nReputation: " + str(self._ReputationScore) + "\n\n"
    Details += "Number of outlets: " + str(len(self._Outlets)) + "\nOutlets\n"
    for Current in range (1, len(self._Outlets) + 1):
      Details += str(Current) + ". " + self._Outlets[Current - 1].GetDetails() + "\n"
    return Details

  def ProcessDayEnd(self):
    Details = ""
    ProfitLossFromOutlets = 0
    ProfitLossFromThisOutlet = 0
    if len(self._Outlets) > 1:
      DeliveryCosts = self._BaseCostOfDelivery + self.CalculateDeliveryCost()
    else:
      DeliveryCosts = self._BaseCostOfDelivery
    Details += "Daily costs for company: " + str(self._DailyCosts) + "\nCost for delivering produce to outlets: " + str(DeliveryCosts) + "\n"
    for Current in range (0, len(self._Outlets)):
      ProfitLossFromThisOutlet = self._Outlets[Current].CalculateDailyProfitLoss(self._AvgCostPerMeal, self._AvgPricePerMeal)
      Details += "Outlet " + str(Current + 1) + " profit/loss: " + str(ProfitLossFromThisOutlet) + "\n"
      ProfitLossFromOutlets += ProfitLossFromThisOutlet
    Details += "Previous balance for company: " + str(self._Balance) + "\n"
    self._Balance += ProfitLossFromOutlets - self._DailyCosts - DeliveryCosts
    Details += "New balance for company: " + str(self._Balance)
    if self._Balance < 0:
      self.CloseAllOutlets()

    return Details
      
  def CloseOutlet(self, ID):
    CloseCompany = False
    del(self._Outlets[ID])
    if len(self._Outlets) == 0:
      CloseCompany = True
    if self._Category == "fast food":
      self._Balance -= (75 * self._Outlets[ID].GetCapacity())
    elif self._Category == "family":
      self._Balance -= (50 * self._Outlets[ID].GetCapacity())
    else:
      self._Balance -= (150 * self._Outlets[ID].GetCapacity())
    return CloseCompany
      
  def ExpandOutlet(self, ID):
    Change = int(input("Enter amount you would like to expand the capacity by: "))
    Result = self._Outlets[ID].AlterCapacity(Change)
    if Result == Change:
      print("Capacity adjusted.")
    else:
      print("Only some of that capacity added, outlet now at maximum capacity.")
        
  def OpenOutlet(self, X, Y):
    if self._Category == "fast food":
      self._Balance -= self._FastFoodOutletCost
      self._Capacity = self._FastFoodOutletCapacity
    elif self._Category == "family":
      self._Balance -= self._FamilyOutletCost
      self._Capacity = self._FamilyFoodOutletCapacity
    else:
      self._Balance -= self._NamedChefOutletCost
      self._Capacity = self._NamedChefOutletCapacity
    NewOutlet = Outlet(X, Y, self._Capacity, self)
    NewFoodTruck = FoodTruck(X, Y, self._SimulationSettlement.GetXSize(),
                             self._SimulationSettlement.GetYSize(), self)
    self._Outlets.append(NewOutlet)
    self._Outlets.append(NewFoodTruck)

  def GetOutlets(self):
    return self._Outlets

  def GetNearestOutlet(self, X, Y):
    NearestOutlet = 0
    NearestOutletDistance = math.sqrt((self._Outlets[0].GetX() - X) ** 2 + (self._Outlets[0].GetY() - Y) ** 2)
    for Current in range (1, len(self._Outlets)):
      CurrentDistance = math.sqrt((self._Outlets[Current].GetX() - X) ** 2 + (self._Outlets[Current].GetY() - Y) ** 2)
      if CurrentDistance < NearestOutletDistance:
        NearestOutletDistance = CurrentDistance
        NearestOutlet = Current
    return self._Outlets[NearestOutlet], NearestOutletDistance

  def __GetListOfOutlets(self):
    Temp = []
    for Current in range (0, len(self._Outlets)):
      Temp.append(Current)
    return Temp

  def __GetDistanceBetweenTwoOutlets(self, Outlet1, Outlet2):
    return math.sqrt((self._Outlets[Outlet1].GetX() - self._Outlets[Outlet2].GetX()) ** 2 + (self._Outlets[Outlet1].GetY() - self._Outlets[Outlet2].GetY()) ** 2)

  def CalculateDeliveryCost(self):
    ListOfOutlets = self.__GetListOfOutlets()
    TotalDistance = 0.0
    for Current in range (0, len(ListOfOutlets) - 1):
      TotalDistance += self.__GetDistanceBetweenTwoOutlets(ListOfOutlets[Current], ListOfOutlets[Current + 1])
    TotalCost = TotalDistance * self._FuelCostPerUnit
    return TotalCost

class Simulation:
  def __init__(self):
    self._Companies = []
    self._FuelCostPerUnit = 0.0098
    self._BaseCostforDelivery = 100
    Choice = input("Enter L for a large settlement, anything else for a normal size settlement: ")
    if Choice == "L":
      ExtraX = int(input("Enter additional amount to add to X size of settlement: "))
      ExtraY = int(input("Enter additional amount to add to Y size of settlement: "))
      ExtraHouseholds = int(input("Enter additional number of households to add to settlement: "))
      self._SimulationSettlement = LargeSettlement(ExtraX, ExtraY, ExtraHouseholds)
    else:
      self._SimulationSettlement = Settlement()            
    Choice = input("Enter D for default companies, anything else to add your own start companies: ")
    if Choice == "D":
      self._NoOfCompanies = 3
      Company1 = Company("AQA Burgers", "fast food", 100000, 200, 203, self._FuelCostPerUnit, self._BaseCostforDelivery, self._SimulationSettlement)
      self._Companies.append(Company1)
      self._Companies[0].OpenOutlet(300, 987)
      self._Companies[0].OpenOutlet(500, 500)
      self._Companies[0].OpenOutlet(305, 303)
      self._Companies[0].OpenOutlet(874, 456)
      self._Companies[0].OpenOutlet(23, 408)
      self._Companies[0].OpenOutlet(412, 318)
      Company2 = Company("Ben Thor Cuisine", "named chef", 100400, 390, 800, self._FuelCostPerUnit, self._BaseCostforDelivery, self._SimulationSettlement)
      self._Companies.append(Company2)
      Company3 = Company("Paltry Poultry", "fast food", 25000, 800, 390, self._FuelCostPerUnit, self._BaseCostforDelivery, self._SimulationSettlement)
      self._Companies.append(Company3)
      self._Companies[2].OpenOutlet(400, 390)
      self._Companies[2].OpenOutlet(820, 370)
      self._Companies[2].OpenOutlet(800, 600)
    else:
      self._NoOfCompanies = int(input("Enter number of companies that exist at start of simulation: "))
      for Count in range (1, self._NoOfCompanies + 1):
        self.AddCompany()
            
  def DisplayMenu(self):
    print("\n*********************************")
    print("**********    MENU     **********")
    print("*********************************")
    print("1. Display details of households")
    print("2. Display details of companies")
    print("3. Modify company")
    print("4. Add new company")
    print("5. Remove company")
    print("6. Advance to next day")
    print("Q. Quit")
    print("\nEnter your choice: ", end = "")

  def __DisplayCompaniesAtDayEnd(self):
    print("\n**********************")
    print("***** Companies: *****")
    print("**********************\n")
    for C in self._Companies:
      print(C.GetName())
      print()
      Details = C.ProcessDayEnd()
      print(Details + "\n")

  def __ProcessAddRemoveHouseholdsEvent(self):

    NoOfHouseholds = random.randint(1, 4)
    AddRemoveChance = random.random()

    for Count in range(1, NoOfHouseholds + 1):
        if AddRemoveChance > 0.3:
          self._SimulationSettlement.AddHousehold()
        else:
          self._SimulationSettlement.RemoveHousehold()

    if AddRemoveChance > 0.3:
      print(str(NoOfHouseholds) + " new households have been added to the settlement.")
    else:
      print(str(NoOfHouseholds) + " households have been removed from the settlement.")

  def __ProcessCostOfFuelChangeEvent(self):
    FuelCostChange = random.randint(1, 9) / 10.0
    UpOrDown = random.randint(0, 1)
    CompanyNo = random.randint(0, len(self._Companies) - 1)
    if UpOrDown == 0:
      print("The cost of fuel has gone up by " + str(FuelCostChange) + " for " + self._Companies[CompanyNo].GetName())
    else:
      print("The cost of fuel has gone down by " + str(FuelCostChange) + " for " + self._Companies[CompanyNo].GetName())
      FuelCostChange *= -1
    self._Companies[CompanyNo].AlterFuelCostPerUnit(FuelCostChange)
        
  def __ProcessReputationChangeEvent(self):
    ReputationChange = random.randint(1, 9) / 10.0
    UpOrDown = random.randint(0, 1)
    CompanyNo = random.randint(0, len(self._Companies) - 1)
    if UpOrDown == 0:
      print("The reputation of " + self._Companies[CompanyNo].GetName() + " has gone up by " + str(ReputationChange))
    else:
      print("The reputation of " + self._Companies[CompanyNo].GetName() + " has gone down by " + str(ReputationChange))
      ReputationChange *= -1
    self._Companies[CompanyNo].AlterReputation(ReputationChange)
        
  def __ProcessCostChangeEvent(self):
    CostToChange = random.randint(0, 1)
    UpOrDown = random.randint(0, 1)
    CompanyNo = random.randint(0, len(self._Companies) - 1)
    AmountOfChange = 0.0
    if CostToChange == 0:
      AmountOfChange = random.randint(1, 19) / 10.0
      if UpOrDown == 0:
        print("The daily costs for " + self._Companies[CompanyNo].GetName() + " have gone up by " + str(AmountOfChange))
      else:
        print("The daily costs for " + self._Companies[CompanyNo].GetName() + " have gone down by " + str(AmountOfChange))
        AmountOfChange *= -1
      self._Companies[CompanyNo].AlterDailyCosts(AmountOfChange)
    else:
      AmountOfChange = random.randint(1, 9) / 10.0
      if UpOrDown == 0:
        print("The average cost of a meal for " + self._Companies[CompanyNo].GetName() + " has gone up by " + str(AmountOfChange))
      else:
        print("The average cost of a meal for " + self._Companies[CompanyNo].GetName() + " has gone down by " + str(AmountOfChange))
        AmountOfChange *= -1
      self._Companies[CompanyNo].AlterAvgCostPerMeal(AmountOfChange)
        
  def __DisplayEventsAtDayEnd(self):
    print("\n***********************")
    print("*****   Events:   *****")
    print("***********************\n")
    EventRanNo = random.random()
    if EventRanNo < 0.25:
      self.__ProcessAddRemoveHouseholdsEvent()
    else:
      EventRanNo = random.random()
      if EventRanNo < 0.5:
        self.__ProcessCostOfFuelChangeEvent()
      else:
        EventRanNo = random.random()
        if EventRanNo < 0.5:
          self.__ProcessReputationChangeEvent()
        else:
          EventRanNo = random.random()
          if EventRanNo >= 0.5:
            self.__ProcessCostChangeEvent()
          else:
            print("No events")

  def ProcessDayEnd(self):
    TotalReputation = 0.0
    Reputations = []
    for C in self._Companies:
      C.NewDay()
      TotalReputation += C.GetReputationScore()
      Reputations.append(TotalReputation)
    LoopMax = self._SimulationSettlement.GetNumberOfHouseholds() - 1
    for Counter in range (0, LoopMax + 1):
      EatsOut, X, Y = self._SimulationSettlement.FindOutifHouseholdEatsOut(Counter)
      #EatsOut = True # Used to force household to eat out
      if EatsOut:
        CompanyRNo = random.randint(1, int(TotalReputation))
        Current = 0
        while Current < len(Reputations):
          if CompanyRNo < Reputations[Current]:
            self._Companies[Current].AddVisitToNearestOutlet(X, Y)
            break
          Current += 1
      else:
        chance = random.random()
        if chance < 0.5:
          nearest_restaurant = None
          nearest_restaurant_distance = None
          for c in self._Companies:
            nr, nrd = c.GetNearestOutlet(X, Y)
            if nearest_restaurant_distance is None or nrd < nearest_restaurant_distance:
              nearest_restaurant_distance = nrd
              nearest_restaurant = nr
            nearest_restaurant.AddDelivery(nearest_restaurant_distance, self._FuelCostPerUnit)

    self.__DisplayCompaniesAtDayEnd()
    self.__DisplayEventsAtDayEnd()
        
  def AddCompany(self):
    CompanyName = input("Enter a name for the company: ")
    Balance = int(input("Enter the starting balance for the company: "))
    TypeOfCompany = ""
    while not(TypeOfCompany == "1" or TypeOfCompany == "2" or TypeOfCompany == "3"):
      TypeOfCompany = input("Enter 1 for a fast food company, 2 for a family company or 3 for a named chef company: ")
    if TypeOfCompany == "1":
      TypeOfCompany = "fast food"
    elif TypeOfCompany == "2":
      TypeOfCompany = "family"
    else:
      TypeOfCompany = "named chef"
    X, Y = self._SimulationSettlement.GetRandomLocation()
    NewCompany = Company(CompanyName, TypeOfCompany, Balance, X, Y, self._FuelCostPerUnit, self._BaseCostforDelivery, self._SimulationSettlement)
    self._Companies.append(NewCompany)
        
  def GetIndexOfCompany(self, CompanyName):
    Index = -1

    matches = []

    for Current in range (0, len(self._Companies)):
      if CompanyName.lower() in self._Companies[Current].GetName().lower():
        matches.append((self._Companies[Current].GetName(), Current))

    if len(matches) == 1:
      return matches[0][1] # Return the index of the first item in the matches list

    elif len(matches) > 1:
      print("Multiple matches found: ")
      for c in matches:
        print("\t" + c[0])

      CompanyName = input("Please enter company name in full: ")

      for Current in range(0, len(self._Companies)):
        if CompanyName.lower() == self._Companies[Current].GetName().lower():
          return Current

    else:
      return -1





  def ModifyCompany(self, Index):

    print("\n*********************************")
    print("*******  MODIFY COMPANY   *******")
    print("*********************************")
    print("1. Open new outlet")
    print("2. Close outlet")
    print("3. Expand outlet")
    print("C. Cancel")
    Choice = input("\nEnter your choice: ")

    print()
    if Choice == "2" or Choice == "3":
      OutletIndex = int(input("Enter ID of outlet: "))
      if OutletIndex > 0 and OutletIndex <= self._Companies[Index].GetNumberOfOutlets():
        if Choice == "2":
          CloseCompany = self._Companies[Index].CloseOutlet(OutletIndex - 1)
          if CloseCompany:
            print("That company has now closed down as it has no outlets.")
            del(self._Companies[Index])
        else:
          self._Companies[Index].ExpandOutlet(OutletIndex - 1)
      else:
          print("Invalid outlet ID.")
    elif Choice == "1":
      X = int(input("Enter X coordinate for new outlet: "))
      Y = int(input("Enter Y coordinate for new outlet: "))
      if X >= 0 and X < self._SimulationSettlement.GetXSize() and Y >= 0 and Y < self._SimulationSettlement.GetYSize():
        self._Companies[Index].OpenOutlet(X, Y)
      else:
        print("Invalid coordinates.")
    elif Choice == "C":
      print("Operation Cancelled")
      return
    else:
      self.ModifyCompany(Index)
      print()

  def DisplayCompanies(self):
    print("\n*********************************")
    print("*** Details of all companies: ***")
    print("*********************************\n")
    for C in self._Companies:
      print(C.GetDetails() + "\n")
    print()
        
  def Run(self):
    Choice = ""
    while Choice != "Q":
      self.DisplayMenu()
      Choice = input()
      if Choice == "1":
        self._SimulationSettlement.DisplayHouseholds()
      elif Choice == "2":
        self.DisplayCompanies()
      elif Choice == "3":
        Index = -1
        while Index == -1:
          CompanyName = input("Enter company name: ")
          Index = self.GetIndexOfCompany(CompanyName)
        self.ModifyCompany(Index)
      elif Choice == "4":
        self.AddCompany()

      elif Choice == "5":
        Index = -1
        CompanyName = ""

        while Index == -1 and CompanyName.lower() != "cancel":
          CompanyName = input("Enter company name TO REMOVE: ")
          Index = self.GetIndexOfCompany(CompanyName)

        if CompanyName.lower() != "cancel":
          del(self._Companies[Index])

      elif Choice == "6":
        self.ProcessDayEnd()
      elif Choice == "Q":
        print("Simulation finished, press Enter to close.")
        input()

class FoodTruck(Outlet):

  def __init__(self, XCoord, YCoord, XSize, YSize, ParentCompany):
    self._SettlementYSize = YSize
    self._SettlementXSize = XSize
    super(FoodTruck, self).__init__(XCoord, YCoord, 10, ParentCompany)

  def Move(self):
    direction = random.randint(1,4)
    if direction == 1 and self._XCoord < self._SettlementXSize:
      self._XCoord +=1
    elif direction == 2 and self._XCoord > 0:
      self._XCoord -= 1
    elif direction == 3 and self._YCoord < self._SettlementYSize:
      self._YCoord += 1
    elif direction == 4 and self._YCoord > 0:
      self._YCoord -= 1

  def NewDay(self):
    super(FoodTruck, self).NewDay()
    self.Move()






def Main():
  ThisSim = Simulation()
  ThisSim.Run()

if __name__ == "__main__":
  Main()
