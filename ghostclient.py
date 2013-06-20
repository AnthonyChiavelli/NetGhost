import requests
import random
from socket import *
from time import sleep



def load_words():
    """
    Returns a list of valid lowercase words

    """
    wordlist = []
    url = "http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00-introduction-to-computer-science-and-programming-fall-2008/assignments/words.txt"
    # Gets wordslist from internet
    req = requests.get(url)
    for word in req.content.split():
        wordlist.append(word.strip().lower())
    return wordlist


def is_invalid_frag(frag, word_list):
    """
    Returns True if the string passed cannot be built on to create a valid word,
    returns False otherwise
    """
    for word in word_list:
        if word.startswith(frag.lower()):
            return False
    return True
        
def connect_to_server(ip, port=8002):
    client = socket(AF_INET, SOCK_STREAM)
    code = 111
    print "Connecting to server... ",
    for tick in range(0,2000):
        sleep(.001)
        code = client.connect_ex((ip, port))
        if code == 0:
            break
    if code != 0:
        return None
    print "Connected to {0}\n".format(ip)
    return client

def is_valid_word(word, word_list):
    return (len(word) > 3 and word.lower() in word_list)

def get_first_player():
    return random.randrange(1,3)

def swap_names(client):
    your_name = raw_input("Enter your name: ")
    print ("Waiting for opponent's name...")
    client.send(your_name)
    opponent_name = client.recv(1024)
    return your_name, opponent_name

def setup_game():
    """Pregame setup """
    print("NetGhost V0.1 by Anthony Reid\n")
    word_list = load_words() #Load the words
            
    #Connect to server
    ip = raw_input("Enter IP address of server: ")
    client = connect_to_server(ip)
    if client:
        #Exchange names
        your_name, opponent_name = swap_names(client)
        print("Playing against {0}".format(opponent_name))

        #Determine who goes first
        player = int(client.recv(1024))
        print "Player = {0}".format(player)

        #Start the game
        start(player, client, word_list, opponent_name, your_name)
    else:
        return False
    
def start(player, client, word_list, opponent_name, your_name):
    """Starts a good old-fashioned game of ghost!"""
    word = ""
    while True: #Main loop of the game
        if word: #Only display the word if it is not empty
            print("\nCurrent word: {0}".format(word))
        if player == 1: #If it is your turn
            letter = raw_input("Your Turn! Enter a letter: ")
            if letter == ".": #Safely close the connection when . is entered
                client.shutdown(SHUT_RDWR)
                client.close()
                break
            if len(letter) == 1 and letter.isalpha(): #If the letter is a letter
                word += letter.upper() #Update the word
                client.send(word)
                if is_invalid_frag(word, word_list): #If the word is an illegal fragment
                    print "\"{0}\" is an invalid word fragment. {1} wins!".format(word, opponent_name)
                    raw_input("Enter any key to exit")
                    break  
                if is_valid_word(word, word_list): #If the word is valid
                    print "\"{0}\" is a valid word. {1} wins!".format(word, opponent_name)
                    raw_input("Enter any key to exit")
                    break   
                player = abs(3-player) #After updating the word, switch players
            else:
                print "Please enter a valid letter"
        elif player == 2: #If it is their turn
            print "Waiting for {0}".format(opponent_name)
            word = client.recv(1024) #Update the word
            if not word: #If the connection is closed, word will be an empty string
                client.close
            print "{0} chose {1}!".format(opponent_name,word[-1]) #Show what the other player chose as a letter
            if is_invalid_frag(word, word_list): #If the word is an illegal fragment
                print "\"{0}\" is an invalid word fragment. You win!".format(word)
                raw_input("Enter any key to exit")
                break                    
            if is_valid_word(word, word_list): #If the word is valid
                print "\"{0}\" is a valid word. You win!".format(word)
                raw_input("Enter any key to exit")
                break            
            player = abs(3-player) #Swap players



if __name__ == "__main__":
    setup_game()













        
        
