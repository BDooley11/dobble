import emoji,random
from random import choice

# initialises dictionary
imageDict = dict()
# opens file emoji.txt and reads it 
fin = open('emoji_names.txt',"r")
lines = fin.readlines()
# iterates through lines and adds emjois to a dictionary key 1-58 with one emoji as each value
for i, el in enumerate(lines):
    imageDict[i+1] = emoji.emojize(el.strip())

def dobbleGenerator():
    
    # sets variables require nim is num of images required on card. initialises myDict to store dictionary and si set
    # to store the images as values in the dictionary
    nIm = 8
    n = nIm - 1
    r = range(n)
    rp1 = range(n+2)
    c = 0
    myDict = dict()
    si = set([])

    # for loop which generates card number 1 in the set of 57
    c += 1
    for i in rp1:
        for key, values in imageDict.items():
            if key == i:
                si.add(values)
    myDict[c] = si
    si = set([])

    # the below two for loops generate the rest of the cards and add symbols to them using the
    # image dictionary created in the first section.
    for j in r:
        c = c+1
        for k in r:
            for key, values in imageDict.items():
                if key == 1:
                    si.add(values)
                if key == (n+2 + n*j +k):
                    si.add(values)
        myDict[c] = si
        si = set([])
    
    for i in r:
        for j in r:
            c = c+1
            for k in r:
                for key, values in imageDict.items():
                    if key == (i+2):
                        si.add(values)
                    if key == ((n+1 +n*k + (i*k+j) % n)+1):
                        si.add(values)
            myDict[c] = si
            si = set([])
            
    return myDict

globalDictionary = dobbleGenerator()

def check_validity(deck, verbose = False):
    
    # for look iterates through the values in the dictionary passed
    for value in deck.values():
        check = value
    # vaid counter set to 0
        valid = 0
    # use lambda function to create a new dictionary minus the value store in var check
        newDict = dict(filter(lambda elem: elem[1] != check,deck.items()))
    # for loop iterates through checking common values in the check v and all the values in the new dictionary
        for value in newDict.values():
            result=check.intersection(value)
    # if len of result equals 1 meaning only on symbol in common then valid counter +1 and if verbose is true
    # it also prints more details.
            if len(result) ==1:
                if verbose == True:
                    print(check)
                    print(value)
                    print(result,"is the only common value in the above cards")
                    print()
                    valid +=1
                else:
                    valid +=1
    # after iterating through if valid counter equals 56 then the dictionary is valid and if not a not valid messages is
    # echoed.
    if valid == 56:
        print("The dictionary is valid")
    else:
        print("The dictionary not valid")

class DobbleCard():
    
    def generate_card(self):
        # the below line takes a random card from the global dictionary variable
        card = random.choice(list(globalDictionary.items()))
        # the below lines pops the card from the global dictionary, card index 0 being the key.
        globalDictionary.pop(card[0])
        # card index 1 which is the 8 symbols is returned when called.
        return card[1]

class DobbleDeck():
    
    def __init__(self):
        # initialising gamedeck list
        self.gamedeck = []

    def add_card(self,number):
        # for loop iterates through the number of cards the user requests and creates Dobble Card instances
        # which are subsequently appended to a DobbleDeck gamedeck as per the requirement.
        for x in range(number+1):
            instance= DobbleCard()
            self.gamedeck.append(instance.generate_card())
                
    def play_card(self):
        # playedCard variable calls index 0 of the gamedeck created (8 symbols) and stores the result as a list
        # I do a random suffle as list items are in order in python so two pandas would appear at the same index on
        # cards if this was not done.
        playedCard = list(self.gamedeck[0])
        random.shuffle(playedCard)
        
        def remove_card():
        # As soon as the card is played I call remove deck which removes index 0 from the deck so no chance of duplicate
        # cards being played
             self.gamedeck.remove(self.gamedeck[0])
        remove_card() 
        return playedCard

def DobbleGame():
    # I ask the user to input the length of the game and then use a try except to make sure the value entered is valid
    cardNum = input("How many cards (<56)? ")
    while True:
            try:
                cardNum = int(cardNum)
                if cardNum <56:
                    break
                else:
                    cardNum = input("How many cards (<56)? ")
            except ValueError:
                    cardNum = input("How many cards (<56)? ")

    # The below section sets up a game counter for player A & B and also passing the length
    # of the game to DobbleDeck in order to create a deck of cards required to play.
    print("If you want to record a draw type 'd' or 'D'.")
    countA=0
    countB=0
    play = DobbleDeck()
    createGameDeck = play.add_card(cardNum) 
    
    #for loop iterates through the length of the game
    for x in range(cardNum):
        
    # if statement here calls a card for card 1 in the first round only as every other round card 1
    # will be replaced by card 2. play card also called for card 2
        if x < 1:
            card1 = play.play_card()
        card2 = play.play_card()
        
    # below section is just formatting the print as required in the brief by printing index of a list
        print(card1[0],card1[1],card1[2], "\t", card2[0],card2[1],card2[2])
        print(card1[3],card1[4],card1[5], "\t", card2[3],card2[4],card2[5])
        print(card1[6],card1[7], "\t\t", card2[6],card2[7])      
        
    # ask the user to enter who won A or B and will also accept d if draw. If another character enterer will
    # ask user to enter again. Result counters updated if a or b entered.
        result=input("Who wins (A or B)? ").lower()
        while result not in 'abd':
            result = input("Must enter either A or B, or D for a draw: ").lower()
        if result == 'a':
            countA +=1
        elif result == 'b':
            countB +=1
            
    # card1 is set to equal card 2 to as this is the first card always in the next round.
        card1 = card2
    
    # print statements to print the overall score at the end of the game
    print()
    print("Score")
    print("A: ",countA)
    print("B: ",countB)
    
    # Dobble generator called to replenish global dictionary deck of cards at the end of the game.
    global globalDictionary
    globalDictionary = dobbleGenerator()

check_validity(globalDictionary, verbose = False)
DobbleGame()
