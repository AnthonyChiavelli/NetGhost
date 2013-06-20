import random
import requests
from socket import *
import string


def load_words():
    """
    Returns a list of valid lowercase words

    """
    wordlist = []
    url = "http://ocw.mit.edu/courses/electrical-engineering-and-computer-science/6-00-introduction-to-computer-science-and-programming-fall-2008/assignments/words.txt"
    # Gets wordslist from URL
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

def get_public_ip():
    """ Determines user's public IP address to share with client"""
    try:
        response = requests.get("http://icanhazip.com")
        assert response.status_code == 200
        return response.content
    except requests.ConnectionError, AssertionError: #If the connection was refused or an error code was returned
        return None
        
def get_client_socket():
    sock = socket(AF_INET, SOCK_STREAM)
    sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1) #Reuse connections
    
    #My local IP address
    ip = '192.168.0.100'

    print ip
    sock.bind((ip, 8002))
    sock.listen(2)
    print "Connecting to client... ",
    client_sock, client_addr = sock.accept()
    print "Connected to {0}\n".format(client_addr[0])
    return client_sock, client_addr      

def is_valid_word(word, word_list):
    return (len(word) > 3 and word.lower() in word_list)

def get_first_player():
    return random.randrange(1,3)

def swap_names(client):
    your_name = raw_input("Enter your name: ")
    print ("Waiting for opponent's name...")
    opponent_name = client.recv(1024)
    client.send(your_name)
    return your_name, opponent_name

def setup_game():
    """Pregame setup """
    print("NetGhost V0.1 by Anthony Reid\n")
    word_list = load_words() #Load the words
    
    #Get the public IP and show it
    public_ip = get_public_ip()
    if public_ip:
        print("For your convenience, your IP address is {0}".format(public_ip))
        
    #Accept the client request and get a connection going
    raw_input("Press enter to begin waiting for a connection")
    client, client_addr = get_client_socket()

    #Exchange names
    your_name, opponent_name = swap_names(client)
    print("Playing against {0}".format(opponent_name))

    #Determine who goes first
    player = get_first_player()
    client.send(str(3-player))

    #Start the game
    start(player, client, word_list, opponent_name, your_name)
    
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
                    break
                elif is_valid_word(word, word_list): #If the word is valid
                    print "\"{0}\" is a valid word. {1} wins!".format(word, opponent_name)
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
            #print("\nCurrent word: {0}".format(word))
            player = abs(3-player) #Swap players



if __name__ == "__main__":
    setup_game()













        
        
