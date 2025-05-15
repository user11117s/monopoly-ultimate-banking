gameEnd = False
class Property:
    def __init__(self, number):
        self.rentLevel = 1
        self.owner = None
        self.number = number
class Player:
    def __init__(self, name):
        self.name = name
        self.properties = []
        self.money = 1500
    def payDebt(self, owner=None):
        global gameEnd
        gameEnd = sum([prices[prop.number] for prop in self.properties]) < -self.money
        if(not gameEnd):
            if(owner):
                while(self.money < 0):
                    prop = input(f"Balance is -${-self.money}. Give property: ")
                    if(properties[prop] in self.properties):
                        self.properties.remove(properties[prop])
                        properties[prop].owner = owner
                        owner.properties.append(properties[prop])
                        self.money += prices[prop]
                    else:
                        print("Property not yours")
            else:
                while(self.money < 0):
                    prop = input(f"Balance is -${-self.money}. Give property: ")
                    if(properties[prop] in self.properties) :
                        self.properties.remove(properties[prop])
                        properties[prop].owner = None
                        self.money += prices[prop]
                    else:
                        print("Property not yours")
class ColorSet:
    def __init__(self, color, properties_):
        self.color = color
        self.properties = [properties[i] for i in properties_]
        self.allBought = False
player = {i : Player(i) for i in input("Enter players: ").split(" ")}
prices = {"1": 60, "2": 60, "3": 100, "4": 100, "5": 120, "6": 140, "7": 140, "8": 160, "9": 180, "10": 180, "11": 200, "12": 220, "13": 220, "14": 240, "15": 260, "16": 260, "17": 280, "18": 300, "19": 300, "20": 320, "21": 350, "22": 400}
rents = {"1": [70, 130, 220, 370, 750], "2": [70, 130, 220, 370, 750], "3": [80, 140, 220, 410, 800], "4": [80, 140, 220, 410, 800], "5": [100, 160, 260, 440, 860], "6": [110, 180, 290, 460, 900], "7": [110, 180, 290, 460, 900], "8": [130, 200, 310, 490, 980], "9": [140, 210, 330, 520, 1000], "10": [140, 210, 330, 520, 1000], "11": [160, 230, 350, 550, 1100], "12": [170, 250, 380, 580, 1160], "13": [170, 250, 380, 580, 1160], "14": [190, 270, 400, 610, 1200], "15": [200, 280, 420, 640, 1300], "16": [200, 280, 420, 640, 1300], "17": [220, 300, 440, 670, 1340], "18": [230, 320, 460, 700, 1400], "19": [230, 320, 460, 700, 1400], "20": [250, 340, 480, 730, 1440], "21": [270, 360, 510, 740, 1500], "22": [300, 400, 560, 810, 1600]}
properties = {str(i) : Property(str(i)) for i in range(1, 23)}
colorsets = [ColorSet("brown", ["1", "2"]), ColorSet("lightblue", ["3", "4", "5"]), ColorSet("pink", ["6", "7", "8"]), ColorSet("orange", ["9", "10", "11"]), ColorSet("red", ["12", "13", "14"]), ColorSet("yellow", ["15", "16", "17"]), ColorSet("green", ["18", "19", "20"]), ColorSet("blue", ["21", "22"])]
# Each turn
while(not gameEnd):
    try:
        command = input(">>> ").split(" ")
        if(command[0] == "Go"): # Go money
            player[command[1]].money += 200
            print("$200 successfully added")
        if(command[0] in ["Jail", "Location"]): # Get out of jail / go somewhere
            player[command[1]].money -= 100
            if(player[command[1]].money < 0):
                player[command[1]].payDebt()
            if(not gameEnd):
                print("$100 successfully subtracted")
        if(command[0] == "Buy"): # Buy a property
            if(properties[command[1]].owner is None):
                player[command[2]].money -= prices[command[1]]
                if(player[command[2]].money < 0):
                    player[command[2]].payDebt()
                player[command[2]].properties.append(properties[command[1]])
                properties[command[1]].owner = player[command[2]]
                properties[command[1]].rentLevel = 1
                if(not gameEnd):
                    colorset = colorsets[int(command[1]) // 3]
                    if(not colorset.allBought and [bool(i.owner) for i in colorset.properties] == [True for i in colorset.properties]):
                        for i in colorset.properties:
                            i.rentLevel += 1
                        if([i.owner for i in colorset.properties] == [colorset.properties[0].owner] * len(colorset.properties)):
                            for i in colorset.properties:
                                i.rentLevel += 1
                        print("Color set bought")
                        for i in colorset.properties:
                            if(i.rentLevel > 5):
                                i.rentLevel = 5
                            print(f"{i.number}: {i.rentLevel}")
                        colorset.allBought = True # In the unit, this "upgrade" can happen only once (per color set), and when a property becomes unowned there is no "downgrade", and the "upgrade" doesn't happend if someone buys it again
                    print(f"Property successfully bought for ${prices[command[1]]}")
                    
            else:
                print("Property already owned. Use 'Rent <property number> <player name>' to pay rent.")
        if(command[0] == "Rent"): # Solution for the issue "Gimme rent"
            if(properties[command[1]].owner and properties[command[1]].owner != player[command[2]]):
                rent = rents[command[1]][properties[command[1]].rentLevel - 1]
                properties[command[1]].owner.money += rent
                player[command[2]].money -= rent
                if(player[command[2]].money < 0):
                    player[command[2]].payDebt(properties[command[1]].owner)
                properties[command[1]].rentLevel += 1
                if(properties[command[1]].rentLevel == 6):
                    properties[command[1]].rentLevel = 5
                if(not properties[command[1]].rentLevel):
                    properties[command[1]].rentLevel = 1
                if(not gameEnd):
                    print("Player successfully paid owner rent")
            else:
                print("Property unowned / owner is asked to pay rent (illegal)")
        if(command[0] == "Check"): # Check rent level and owner
            try:
                print(f"Rent level of {command[1]} is {properties[command[1]].rentLevel}.\nOwner is {properties[command[1]].owner.name}")
            except(AttributeError):
                print("Property unowned")
        if(command[0] in ["Increase", "Decrease"]): # Change rent levels (for event cards or landing on your own property)
            if(properties[command[1]].owner):
                print(f"{command[1]} : {properties[command[1]].rentLevel} -> ", end="")
                properties[command[1]].rentLevel += (1 if command[0] == "Increase" else -1)
                if(properties[command[1]].rentLevel == 6):
                    properties[command[1]].rentLevel = 5
                if(not properties[command[1]].rentLevel):
                    properties[command[1]].rentLevel = 1
                print(properties[command[1]].rentLevel)
            else:
                print("Property unowned")
        if(command[0] == "Auction"): # Auction a property
            if(properties[command[1]].owner is None):
                bid = 20
                try:
                    bid = int(input("Start bidding: "))
                    while(True):
                        prevBid = bid
                        bid = int(input("Keep on bidding: "))
                        if(prevBid >= bid):
                            print("You should bid more than the last player")
                            bid = prevBid
                        del prevBid
                except(ValueError):
                    newowner = player[input(f"Price is ${bid}. Who bid last? ")]
                    newowner.money -= bid
                    if(newowner.money < 0):
                        newowner.payDebt()
                    newowner.properties.append(properties[command[1]])
                    properties[command[1]].owner = newowner
                    if(not gameEnd):
                        print("Property successfully bought")
            else:
                print("Property already owned. Use 'Rent <property number> <player name>' to pay rent.")
        if(command[0] == "Money"): # Check money
            for i in player:
                print(f"{i} has ${player[i].money}")
        if(command[0] == "Tax"): # Highway Tax event card
            player[command[1]].money -= 50 * len(player[command[1]].properties)
            if(player[command[1]].money < 0):
                player[command[1]].payDebt()
            if(not gameEnd):
                print("Highway tax successfully paid.")
        if(command[0] == "Swap"):
            if(properties[command[1]].owner != properties[command[2]] and properties[command[1]].owner and properties[command[2]].owner):
                properties[command[1]].owner.properties.append(properties[command[2]])
                properties[command[2]].owner.properties.append(properties[command[1]])
                properties[command[1]].owner.properties.remove(properties[command[1]])
                properties[command[2]].owner.properties.remove(properties[command[2]])
                p1 = properties[command[1]].owner.name
                p2 = properties[command[2]].owner.name
                properties[command[1]].owner = player[p2]
                properties[command[2]].owner = player[p1]
                print("Successfully swapped properties.")
            else:
                print("Please ensure that the properties are owned and have different owners")
    except(KeyError, IndexError, ValueError, TypeError):
        print("Error occured (probably typo or you are trying to cheat the unit)")
print("#########################")
print("         GAME END        ")
print("#########################\n")
for i in player:
    print(f"{i} has ${player[i].money + sum([prices[prop.number] for prop in player[i].properties])}" if player[i].money > -1 else f"{i} is bankrupt")
