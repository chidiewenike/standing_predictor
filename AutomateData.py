import json
from shutil import copyfile

def Choices(seasonJson,standings):
    print("Standing #" + str(standings))
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Name"] = str(input("What is the team name? "))
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Place"] = str(standings)
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Wins"] = str(input("How many home wins? "))
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Draws"] = str(input("How many home draws? "))
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Losses"] = str(input("How many home losses? "))
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Wins"] = str(input("How many away wins? "))
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Draws"] = str(input("How many away draws? "))
    seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Losses"] = str(input("How many away losses? "))

    return seasonJson, standings

def Display(seasonJson, standings):
    print('\n')
    print("Club: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Name"])
    print("Standing: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Place"])
    print("\nHome Wins: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Wins"])
    print("Home Draws: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Draws"])
    print("Home Losses: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Losses"])
    print("Away Wins: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Wins"])
    print("Away Draws: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Draws"])
    print("Away Losses: " + seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Losses"])
    print('\n')
    try:
        homeGames = 0
        awayGames = 0
        homeGames += int(seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Wins"])
        homeGames += int(seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Draws"])
        homeGames += int(seasonJson["Season"]["Standing"]["Team"][standings-1]["Home_Losses"]) 
        awayGames += int(seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Wins"])
        awayGames += int(seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Draws"]) 
        awayGames += int(seasonJson["Season"]["Standing"]["Team"][standings-1]["Away_Losses"]) 
    except ValueError:
        print("Error. Enter valid integer values.")  
    print(homeGames)
    print(awayGames)
    print('\n')

    

nameCorrect = False

while not (nameCorrect):
    season = str(input("What is the season in question? "))
    league = str(input("Which league is it? "))
    print("\n")
    print("Season: " + season)
    print("League: " + league)
    print("\n")
    if (str(input("(y)es or (n)o? ")).lower() == "y"):
        nameCorrect = True

fileName = league + "_" + season
fileName = fileName.replace(" ","_")
fileName = fileName.replace("/","")

#copyfile('empty_standing.json',fileName + ".json")

with open("empty_standing.json") as json_data:
    seasonJson = json.load(json_data)

standings = 1
seasonJson["Season"]["id"] = season
seasonJson["Season"]["League"] = league
print("=================================================================")
previousStanding = 0

previousStanding = standings
seasonJson,standings = Choices(seasonJson,standings)
Display(seasonJson,standings) 

with open(fileName + '.json', 'w') as outfile:
    json.dump(seasonJson, outfile)

print("=================================================================")


while (standings <= 20):
 
    choice = str(input("(C)ontinue, (R)edo, or input an integer to return to that standing: "))
        
    if (choice.lower() == "r"):
        print ("Redo")
        seasonJson,standings = Choices(seasonJson,previousStanding)
        Display(seasonJson,standings) 
        print("=================================================================")


    elif (choice.isdigit()):
        standings=int(choice)
        previousStanding = standings
        seasonJson,standings = Choices(seasonJson,standings)
        Display(seasonJson,standings) 
        print("=================================================================")
    
    
    elif (choice.lower() == "c"):
        standings+=1
        previousStanding = standings
        seasonJson,standings = Choices(seasonJson,standings)
        Display(seasonJson,standings) 
        print("=================================================================")


    try:
        with open(fileName + '.json', 'w') as outfile:
            json.dump(seasonJson, outfile)
            print("=================================================================")
    except ValueError:
        print("Error. Enter valid integer values.")     

