import random
import time
from math import floor
from time import sleep
from os import system

debug = False
keydebug = False

def deck_build():
  full_deck = []
  suits = ['\u2660','\u2663','\u2666','\u2665'] #UTF-8 for S,C,D,H
  face_cards = ['A','J','Q','K']
  for suit in suits:
    for i in range(1,14):
      if not i == 1 and not i > 10:
        full_deck.append(str(i)+suit)
      elif i == 1:
        full_deck.append(face_cards[i-1]+suit)
      else:
        full_deck.append(face_cards[i-10]+suit)

  psuedoDeck = list(range(1,14))*2+list(range(101,114))*2
  return full_deck,psuedoDeck



#_________________________________________________________________________________________________

def playerCount():
  check = False
  while not check:
    players = input("How many people are playing? ")
    if not players.isnumeric():
      system('cls')
      print('9 LOCKS')
      
      print("Please enter a number")
    elif int(players) > 4 or int(players) <2:
      system('cls')
      print('9 LOCKS')
      
      print("Game must be played with 2 - 4 players")
    else:
      check = True
      players = int(players)
      print('dealing ' + str(players) + ' hands.')
##      sleep(0.8)




  return players

#_________________________________________________________________________________________________

def hand_build(numPlayers):
  handAll = []
  psuedoHandAll = []
  for players in range(numPlayers):
    handTemp = ['','','']
    psuedoHandTemp = ['','','']
    for cards in range(3):
      rand = random.randint(0,len(fullDeck)-1)
      handTemp[cards] = fullDeck.pop(rand)
      psuedoHandTemp[cards] = psuedoDeck.pop(rand)
      
    handAll.append(handTemp)
    psuedoHandAll.append(psuedoHandTemp)
  return (handAll,psuedoHandAll,psuedoDeck)

#_________________________________________________________________________________________________

def legal_play_list(psuedoVal):
  if psuedoVal >= 100:
    oppColourVal = psuedoVal-100
  else:
    oppColourVal = psuedoVal+100
  legal_left,legal_right=psuedoVal-1,psuedoVal+1
  if psuedoVal == 1 or psuedoVal == 101: 
    legal_left = psuedoVal+12
  if psuedoVal == 13 or psuedoVal == 113:
    legal_right = psuedoVal-12

  return [legal_left,legal_right,oppColourVal]

def field_build(psuedoDeck):
  gamePiles = []
  keydebug2=keydebug
  print(psuedoDeck)
  for pile in range(9):
    rand = random.randint(0,len(fullDeck)-1)
    pileStatus = 0 #=Face down
    pileVals = fullDeck.pop(rand)
    psuedoVals = psuedoDeck.pop(rand)
    if keydebug2:
      pileVals=fullDeck.pop(fullDeck.index('9S'))
      psuedoVals = psuedoDeck.pop(psuedoDeck.index(9))
      keydebug2 = False

    pileLegal = legal_play_list(psuedoVals)

    if pile == 4:#Unlock the middle pile by default
      pileStatus = 1
    if keydebug:
      print(pileVals)
    
    pileCount = 1 #Number of cards in pile
    gamePiles.append([pileVals,psuedoVals,pileLegal,pileStatus,pileCount])

  return gamePiles,psuedoDeck

#_________________________________________________________________________________________________

def turn_request(player):

  winCon = False


  if len(psuedoDeck)>0:
    pickup_legal = True
  else:
    pickup_legal = False

 
 #Loop to find if any players cards can be played
  playable_card_sum = 0
  playableList = []
  for pile in range(9):
    if gamePiles[pile][3] == 1:
      for i in range(3):
        playableList.append(gamePiles[pile][2][i])

  for card in range(len(psuedohVis[player])): #Check how many times players vis cards occur in the playable list
    playable_card_sum += playableList.count(psuedohVis[player][card])
      
  for card in range(len(psuedohInvis[player])): #Check how many times players invis cards occur in the playable list     
      playable_card_sum += playableList.count(psuedohInvis[player][card])                       

  if (not pickup_legal and playable_card_sum == 0) or debug == True: #If there are no cards left in the deck and the player cant play
    playerMove = 0
    finishedPlayersList[player] = True
    finishedPlayersScore[player] = len(hVis[player])
    print("There is no where to play and there are no cards left in the deck. Player " + str(player+1) +\
          " finishes with " + str(len(hVis[player])) + " visible cards")
    if not debug:
      sleep(4)
    return playerMove, finishedPlayersList, finishedPlayersScore, winCon


  check = False
  while not check:

    if playable_card_sum == 0 and pickup_legal: #if they cant play a card, force pick up move (move 2)
      playerMove = '2'
      check = True
      print("player " + str(player+1) + " has no cards than can be played, picking up a card.")
      sleep(2)
      continue
    
    playerMove = input("player " + str(player+1) + "'s turn, pick a move: 1 = play a card, 2 = pickup: ")
    if playerMove =="end": #End game
      winCon = True
      check = True
      break
    
    
    if playerMove.isnumeric():
      
      if int(playerMove) == 1:
        
        if playable_card_sum > 0:
          check = True
        else:
          print("You have no cards you can play, pick up instead.")

      elif int(playerMove) == 2:
        
        if pickup_legal:
          check = True
        else:
          gameScreen_print(player)
          print("There are no cards left in the deck, play a card instead.")
      else:
        gameScreen_print(player)
        print("Please pick 1 or 2")

    else:
      gameScreen_print(player)
      print("Please pick 1 or 2")
  

  return playerMove, finishedPlayersList, finishedPlayersScore, winCon

#_________________________________________________________________________________________________

def pickUp(player):

#Picking up a new card
  rand = random.randint(0,len(fullDeck)-1)
  newCard = fullDeck.pop(rand)
  psuedonewCard = psuedoDeck.pop(rand)
  
  if len(hVis[player]) >= len(hInvis[player]):
    hInvis[player].append(newCard)
    psuedohInvis[player].append(psuedonewCard)


  else:
    hVis[player].append(newCard)
    psuedohVis[player].append(psuedonewCard)
    
  gameScreen_print(player)
  flipUnlock()
  

  return hVis, psuedohVis, hInvis, psuedohInvis, psuedoDeck
#_________________________________________________________________________________________________

def flipUnlock():
#Flipping/unlocking a pile (pile states: 0=facedown, 1= playable, 2 = locked)

  #check there is a flippable/unlockable pile
  faceDownIndex = []
  LockedIndex = []
  for i in range(9):
    if gamePiles[i][3] == 0:
      faceDownIndex.append(i)
    if gamePiles[i][3] == 2:
      LockedIndex.append(i)


  #Flip a card if posible
      
  if len(faceDownIndex)>0:
    check = False
    while not check:
      cardFlip = input("Select a pile to reveal: ")
      
      if not cardFlip.isnumeric():
        gameScreen_print(player)
        print("Please enter a pile number")
        continue
      cardFlip = int(cardFlip)
      flipCheck = faceDownIndex.count(int(cardFlip)-1)
      if flipCheck != 1:
        gameScreen_print(player)
        print("That pile is already flipped over or doesnt exist")
      else:
        check = True
        gamePiles[cardFlip-1][3]=1
        if gamePiles[cardFlip-1][1] == 9 or gamePiles[cardFlip-1][1] == 109:
          nine_key()
    
  #otherwise unlock a pile if possible
        
  elif len(LockedIndex)>0:
    check = False
    while not check:
      cardUnlock = input("Unlock a Pile: ")
      
      if not cardUnlock.isnumeric():
        gameScreen_print(player)
        print("Please enter a pile number")
        continue
      cardUnlock = int(cardUnlock)
      UnlockCheck = LockedIndex.count(int(cardUnlock)-1)
      if UnlockCheck != 1:
        gameScreen_print(player)
        print("That pile is not locked")
      else:
        check = True
        gamePiles[cardUnlock-1][3]=1

  #Otherwise end turn
        
  else:
    print("There are no piles to flip or unlock. Turn over")
  
  
  return hVis, psuedohVis, hInvis, psuedohInvis, psuedoDeck, gamePiles

#_________________________________________________________________________________________________
  
def playCard(player):
  successful_play = False
  winCon = False
  while not successful_play:
    #Selecting the hand to play from
    check = False
    while not check:

      if len(hInvis[player])<1:
        selected_hand = 1
        psuedo_selected_hand = psuedohVis[player]
        print("You only have table cards left, playing from table hand")
        check = True
        sleep(2)
      else:
        selected_hand = input("Which hand are you playing from? (1 = table hand, 2 = hidden hand): ")
        if not selected_hand.isnumeric():
          gameScreen_print(player)
          print("Please enter 1 or 2")
          continue
        elif int(selected_hand) !=1 and int(selected_hand) !=2:
          gameScreen_print(player)
          print("Please enter 1 or 2")
          continue
        else:
          check = True

      selected_hand_index = int(selected_hand)

      if selected_hand_index == 1: #assign temporary hand lists to existing visible hands
        hand_str = "table hand"
        selected_hand = hVis[player] #Ive changed what this variable is used for which is bad but ohwell
        psuedo_selected_hand = psuedohVis[player]
      else: #Assign temporary hand lists to existing invisible hands
        hand_str = "hidden hand"
        selected_hand = hInvis[player]
        psuedo_selected_hand = psuedohInvis[player]

    #Selecting the card to play

      gameScreen_print(player)
      selected_card = input("Pick a card to play from your " + hand_str + " (as a number as it appears in your hand): ")

      if not selected_card.isnumeric():
        gameScreen_print(player)
        print("Please enter a number")
        continue
      elif int(selected_card) > len(psuedo_selected_hand) or int(selected_card) <1:
        gameScreen_print(player)
        print("You don't have that many cards")
        continue
      else:
        selected_card = int(selected_card)
        psuedo_selected_card = psuedo_selected_hand[selected_card-1]
        
      #Selecting a pile to play on

      gameScreen_print(player)
      selected_pile = input("Pick a pile to play " + str(selected_hand[selected_card-1]) + " on (enter 1-9): ")
      if selected_pile.isnumeric():
        selected_pile = int(selected_pile)
        if selected_pile > 0 and selected_pile <= 9:
        
          if gamePiles[selected_pile-1][3] == 1:
            if gamePiles[selected_pile-1][2].count(psuedo_selected_card)>0:

              check = True #Successful card play
              successful_play = True

              played_card = selected_hand.pop(selected_card-1)
              psuedo_played_card = psuedo_selected_hand.pop(selected_card-1)
              
              gamePiles[selected_pile-1][0] = played_card #Replace top card with played card
              gamePiles[selected_pile-1][1] = psuedo_played_card #Replace top psuedo card
              gamePiles[selected_pile-1][4] +=1 #Add one card to the total pile count for selected pile


              #UPDATE THE PLAYABLE CARDS LISTS in psuedo cards legal list
              
              gamePiles[selected_pile-1][2] = legal_play_list(psuedo_played_card)

              #CHECK IF A PLAYER WINS THE GAME
              if len(hVis[player])==0:
                winCon = True               

              if gamePiles[selected_pile-1][4] == lock_condition: #lock condition is 5 generally. Could vary depending on numPlayers to balance game (lock earlier with fewer players)
                gamePiles[selected_pile-1][3] = 2 #Lock the pile if it is the fifth card to be played

              #Check if the new top card is a 9 (9 was just played), if so use key
              if gamePiles[selected_pile-1][1] == 9 or gamePiles[selected_pile-1][1] == 109:
                nine_key()

            #Error messages for invalid inputs        
            else:
              gameScreen_print(player)
              print("That card can't be played on that pile")
          else:
            gameScreen_print(player)
            print("That pile is facedown or locked and can't be played on")
      
        else:
          gameScreen_print(player)
          print("There aren't that many game piles, select pile number 1-9")
      else:
        gameScreen_print(player)
        print("Please enter a number")

    #Asign the real hands to the new temp hands
    if selected_hand_index == 1: #if selected hand was table hand (hVis)
      hVis[player] = selected_hand
      psuedohVis[player] = psuedo_selected_hand
    else:
      hInvis[player] = selected_hand
      psuedohInvis[player] = psuedo_selected_hand

  return hVis, psuedohVis, hInvis, psuedohInvis, gamePiles, winCon

#_________________________________________________________________________________________________
  

def gameScreen_print(player):

  #Find a constant value to offset the index of the player whos turn it is to the index of the player that should be displayed accross the table.
  #This is to account for the fact that games can have a differing number of players and the postition each hand is prtined depends on this number of players
  horiz_player_index = floor(numPlayers/2)
  

  #Build vis & invis hand displays
  hInvis_display = []
  hVis_display = []
  for i in range(numPlayers):
    hInvis_display.append([])
    hVis_display.append([])

  for i in range(numPlayers):
    for card in range(len(hInvis[i])):
      if player == i:
        hInvis_display[i].append(" " + hInvis[i][card] + " ")
      else:
        hInvis_display[i].append(' XX ')

  for i in range(numPlayers):
    for card in range(len(hVis[i])):
        hVis_display[i].append(" " + hVis[i][card] + " ")

  
  #Build gamescreens
  system('cls')
  gamescreen=[]
  statescreen=[]
  psuedogamescreen = []
  for i in range(9):
    gamescreen.append(gamePiles[i][0])
    statescreen.append(gamePiles[i][3])
    psuedogamescreen.append(gamePiles[i][1])

  #Build game pile displays

  for i in range(9):
    if gamePiles[i][3] == 0: #Print XX if the game pile has not been revealed
      
      gamescreen[i] = ' XX '
    elif gamePiles[i][3] == 2:
      gamescreen[i] = "("+gamePiles[i][0]+")" #Print the pile in brackets to represent that it is locked
    else:
      gamescreen[i] = " "+gamePiles[i][0]+" "



  #Print the board
  print("player " + str(player+1) + "'s Turn")
  print('\n')
  print("                                       " + str(hInvis_display[player-horiz_player_index]))
  print("                                       " + str(hVis_display[player-horiz_player_index]))
  print('\n')

  if numPlayers == 3:
    print("  " + str(hInvis_display[player-2]))
    print("  " + str(hVis_display[player-2]))
    print('\n')

  if numPlayers == 4:
    print("  " + str(hInvis_display[player-3]) + "                                                     " + str(hInvis_display[player-1]))
    print("  " + str(hVis_display[player-3]) + "                                                     " + str(hVis_display[player-1]))
    print('\n')
  
  print("                                       " + str(gamescreen[:3]))
  print("                                       " + str(gamescreen[3:6]))
  print("                                       " + str(gamescreen[6:9]))
  print('\n')

  print('\n')
  print("                         Hidden Hand:  " + str(hInvis_display[player]))
  print("                          Table Hand:  " + str(hVis_display[player]))
  print('\n')

#_________________________________________________________________________________________________


def nine_key(): #Function to call when a 9 is played or flipped to allow a player to lok or unlock piles
  activating_nine=[] 
  while not activating_nine == 'y' and not activating_nine == 'n':
    gameScreen_print(player)
    activating_nine = input('9 played/flipped. Would you like to use the key?: y/n')
    if activating_nine == 'y':
      gameScreen_print(player)
      nine_pile_choice = input('Pick a pile to use your key on: ')
        
      if not nine_pile_choice.isnumeric():
        gameScreen_print(player)
        activating_nine=[]
        print("Please enter a pile number")
        continue
      nine_pile_choice = int(nine_pile_choice)
      if nine_pile_choice > 9 or nine_pile_choice < 1:
        gameScreen_print(player)
        activating_nine=[]
        print("Please enter a pile number (1-9)")
        continue

      if gamePiles[nine_pile_choice-1][3] == 1:
        gamePiles[nine_pile_choice-1][3] = 2
      else:
        print(gamePiles[nine_pile_choice-1][0])
        print(type(gamePiles[nine_pile_choice-1][0]))
        if gamePiles[nine_pile_choice-1][3] == 0 and gamePiles[nine_pile_choice-1][1] %100 == 9:
          gamePiles[nine_pile_choice-1][3] = 1
          nine_key()
          
        gamePiles[nine_pile_choice-1][3] = 1
        


#_________________________________________________________________________________________________




    
winCon = False
lock_condition = 5 #Number of cards that can be played on a pile before it is locked
winner_string = "None" #Initiate winner_string incase game is ended with 'end' input on player move 
print("9 LOCKS \n")

numPlayers = playerCount()

#Create an empty list to store when players can no longer move and their final score
finishedPlayersList = []
finishedPlayersScore = []
for i in range(numPlayers):
  finishedPlayersList.append([])
  finishedPlayersScore.append([])


#Generate deck of cards
fullDeck,psuedoDeck = deck_build()


#Generate visible hand
hVis,psuedohVis,psuedoDeck = hand_build(numPlayers)

#Generate invisibile hand
hInvis,psuedohInvis,psuedoDeck = hand_build(numPlayers)
#Generate game board
gamePiles,psuedoDeck = field_build(psuedoDeck)

if keydebug:
  print(fullDeck)
  print(hVis)
  print(hInvis)
  print(gamePiles)
  input()

while not winCon:

  for player in range(numPlayers):
    system('cls')
    gameScreen_print(player)

    if not finishedPlayersList[player]:
      playerMove, finishedPlayersList, finishedPlayersScore, winCon = turn_request(player)

      if playerMove == str(2):
        hVis, psuedohVis, hInvis, psuedohInvis, psuedoDeck = pickUp(player)

      if playerMove == str(1):
        hVis, psuedohVis, hInvis, psuedohInvis, gamePiles, winCon = playCard(player)
        winner = player+1
        winner_string=str(winner)
      if finishedPlayersList.count(True) == len(finishedPlayersList):
        winCon = True
        winning_score = min(finishedPlayersScore) #Find what the lowest number of cards in visible hands is, this is the winning hand(s)
        winner_list = [] #Create an empty list to store the players that have the wining hand length
        for player in range(numPlayers):
          if finishedPlayersScore[player] == winning_score:
            winner_list.append(player+1) #Add players to a list of winners based on their hand length
        winner_string = str(winner_list[0])
        if len(winner_list)>1: #If there is a tie, create a string to display each winner
          for winner in winner_list[1:]:
            winner_string+= " & {}".format(winner)
      if winCon:
        break
  
system('cls')
print("game over")
print("Player " + (winner_string) + " wins.")

input()
system('cls')

#Form of game piles: ([pileVals,psuedoVals,pileLegal,pileStatus,pileCount])
#pile status: 0-face down, 1-playable, 2-locked


  
#Save check