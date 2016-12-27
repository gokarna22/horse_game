# Horse Race Betting game by Paul and Ben Barber
# Based on an original game for the BBC model B, by John Barber of Ipswich Town
# March 2016

# Python3, can be run from IDLE, developed under version 3.5.1

# TODO
# Write the Broke function to end the game (or end if 1 player left and have a winner?)
# Slow down the race
# Tidy up


from tkinter import *
#from winsound import *
from pygame import mixer as sounds
import random
import time
import tkinter.messagebox
import tkinter.simpledialog

tk = Tk()
sounds.init()

# make the window and canvas to draw on
tk.title("Horse Game")
#tk.resizable(False, False)
#tk.attributes("-topmost", True)
tk.attributes("-fullscreen", True)
tk.config(cursor='none')
tk.update()

screen_width = tk.winfo_width()   # 1280
screen_height = tk.winfo_height()   # 720
#screen_height = int(screen_width * 9 / 16)   # Make the screen the right shape for widescreen TV
print ("Screen: " + str(screen_width) + " by " + str(screen_height))

NumberofPunters = 0
keypressed = False
numberofLines = 32
numberofCols = 30

row_spacing = screen_height/numberofLines  #55  #75
#start_pos = screen_width - 200  # 1000
finish_pos = 200
horse_step = (screen_width - 400)/numberofCols    #50
horse_wait = 0.4

myfont = ("Fixedsys", str(int(row_spacing)))    #("Arial", "32")

# make empty lists
horselist = []
punterlist = []

# sounds
gunSound = sounds.Sound("gun.wav")
hoovesSound = sounds.Sound("hooves.wav")
brokeSound = sounds.Sound("broke.wav")
    
# make a horse class so it is easy to make many of them
class HorseSprite:
    def __init__(self, canvas, number, name, colour):
        self.canvas = canvas
        self.images = [PhotoImage(file="legsin.gif"), PhotoImage(file="legsout.gif")]
        # make the image bigger
        zoom_factor = 5
        self.images[0] = self.images[0].zoom(zoom_factor, zoom_factor)
        self.images[1] = self.images[1].zoom(zoom_factor, zoom_factor)
        # position it in the correct row
        self.number = number
        self.name = name
        self.colour = colour
        self.pos = 0 #start_pos
        self.current_image = 0
        self.price = 0

    def prepare_to_race(self):
        self.pos = finish_pos + (numberofCols - 6 + self.price/5)*horse_step   #start_pos
        self.current_image = 0
        row = self.number*row_spacing*2
        #canvas.create_rectangle(0, row-30, screen_width, row+30, fill='dark green')
        self.image = canvas.create_image(self.pos, row, image=self.images[0])
        self.bib = canvas.create_rectangle(self.pos-10, row-5, self.pos+10, row+5, fill=self.colour)
        
    def move(self):
        # change the image to make the horse gallop
        if self.current_image == 0:
            self.current_image = 1
        else:
            self.current_image = 0
        self.canvas.itemconfig(self.image, image=self.images[self.current_image])
        # move some amount
        self.canvas.move(self.image, -horse_step, 0)
        self.canvas.move(self.bib, -horse_step, 0)
        self.pos -= horse_step
        hoovesSound.play()

# make a punter (player) class, there will be a few of those
class Punter:
    def __init__(self, name):
        self.name = name
        self.total = 100   # how much money they have left # random.randint(0,100) #
        self.pick = -1     # which horse they have picked, 0-6, -1=not made a pick
        self.stake = 0     # how much they have bet on the horse

# keypress callback, just update some global variables
def KeyPress(event):
    global keypressed, keyevent
    keypressed = True
    keyevent = event

# Wait for any keypress
def WaitForKeyPress(canvas):
    global keypressed
    wait_text = canvas.create_text(screen_width/2, screen_height-50, text="Press any key to continue...", fill="cyan", font=myfont, justify="center")
    canvas.pack()
    keypressed = False
    while (keypressed == False):
        # wait for KeyPress to be called
        tk.update_idletasks()
        tk.update()
        time.sleep(0.01)
    if (keyevent.keysym == 'Escape'):
        exit(0)
    canvas.delete(wait_text)
    
# Wait for integer number to be typed, textitem is where it will be echoed as you type
def WaitForInteger(canvas, textitem):
    global keypressed, keyevent
    string = ""
    keypressed = False
    while True:
        while (keypressed == False):
            # wait for KeyPress to be called
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
        #print (keyevent.char)
        if (keyevent.keysym == 'Return'):
            if (len(string)>0):
                return int(string)
        elif (keyevent.keysym == 'BackSpace'):
            if (len(string)>0):
                string = string[:-1]
                canvas.itemconfig(textitem, text=string)
        elif (keyevent.char.isdigit()):
            string = string + keyevent.char
            #print (string)
            canvas.itemconfig(textitem, text=string)
        elif (keyevent.keysym == 'Escape'):
            exit(0)
        keypressed = False
    
# Wait for string to be typed, textitem is where it will be echoed as you type
def WaitForString(canvas, textitem):
    global keypressed, keyevent
    string = ""
    keypressed = False
    while True:
        while (keypressed == False):
            # wait for KeyPress to be called
            tk.update_idletasks()
            tk.update()
            time.sleep(0.01)
        if (keyevent.keysym == 'Return'):
            return string
        elif (keyevent.keysym == 'BackSpace'):
            if (len(string)>0):
                string = string[:-1]
                canvas.itemconfig(textitem, text=string)
        elif (keyevent.keysym == 'Escape'):
            exit(0)
        else:
            #print (keyevent.char)
            string = string + keyevent.char
            #print (string)
            canvas.itemconfig(textitem, text=string)
        keypressed = False

def Initialize_characters_variables(canvas):
    # create some horse sprites
    horse = HorseSprite(canvas, 1, "Redwold", "red")
    horselist.append(horse)
    horse = HorseSprite(canvas, 2, "Black Jet", "black")
    horselist.append(horse)
    horse = HorseSprite(canvas, 3, "Yellow Dog", "yellow")
    horselist.append(horse)
    horse = HorseSprite(canvas, 4, "Super Blue", "blue")
    horselist.append(horse)
    horse = HorseSprite(canvas, 5, "Hot Magenta", "magenta")
    horselist.append(horse)
    horse = HorseSprite(canvas, 6, "Cyan Runner", "cyan")
    horselist.append(horse)
    horse = HorseSprite(canvas, 7, "White Flash", "white")
    horselist.append(horse)


def DisplayCash(canvas, title="LEADER BOARD", wait=False):
    Broke = 0   # Count how many punters are broke
    # clear the scene
    canvas.delete("all")
    # draw the scene
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill="black")
    canvas.create_text(screen_width/2, row_spacing,  text="--------------------------------", fill="cyan", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*2, text="* " + title + " *", fill="magenta", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*3,  text="--------------------------------", fill="cyan", font=myfont, justify="center")
    pos = row_spacing*5
    for punter in sorted(punterlist, key=lambda punter: punter.total, reverse=True):
        message = punter.name + " has £" + str(punter.total)
        canvas.create_text(screen_width/2, pos, text=message, fill="Yellow", font=myfont, justify="center")
        pos = pos + row_spacing*2
        if (punter.total<=0):
            Broke = Broke+1
    canvas.pack()
    tk.update()
    if (wait):
        WaitForKeyPress(canvas)
    return Broke

def Punters(canvas):
    DisplayCash(canvas, title="HORSE RACING GAME")
    question = canvas.create_text(screen_width/2, screen_height-row_spacing*4, text="How many punters?", fill="red", font=myfont, justify="center")
    answer = canvas.create_text(screen_width/2, screen_height-row_spacing*2, text="", fill="orange", font=myfont, justify="center")
    n = 0
    while (n<1 or n>8):   # minimum 1 and maximum 8 players
        n = WaitForInteger(canvas, answer)
        canvas.itemconfig(answer, text="")
    canvas.delete(question, answer)

    for i in range(1, n+1):
        #name = tkinter.simpledialog.askstring("Punter " + str(i), "What is your name?")
        question = canvas.create_text(screen_width/2, screen_height-row_spacing*4, text="Punter " + str(i) + ", what is your name?", fill="red", font=myfont, justify="center")
        answer = canvas.create_text(screen_width/2, screen_height-row_spacing*2, text="", fill="orange", font=myfont, justify="center")
        name = WaitForString(canvas, answer)
        punter = Punter(name)
        punterlist.append(punter)
        canvas.delete(question, answer)
        DisplayCash(canvas, title="HORSE RACING GAME")

def StartingPrices(canvas):
    # clear the scene
    canvas.delete("all")
    # draw the scene
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill="dark green")
    canvas.create_text(screen_width/2, row_spacing,  text="--------------------------------", fill="red", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*2, text="* STARTING PRICES *", fill="yellow", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*3,  text="--------------------------------", fill="red", font=myfont, justify="center")
    pos = row_spacing*5
    i = 1
    for horse in horselist:
        horse.price = random.randint(1,6)*5
        message = str(i) + ") " + horse.name + " " + str(horse.price) + "/1"
        canvas.create_text(screen_width/2, pos, text=message, fill=horse.colour, font=myfont, justify="center")
        pos = pos + row_spacing*2
        i = i + 1
    canvas.create_text(screen_width/2, pos,                text="================================", fill="red", font=myfont, justify="center")
    canvas.create_text(screen_width/2, pos+row_spacing,    text="PLACE YOUR BETS", fill="yellow", font=myfont, justify="center")
    canvas.create_text(screen_width/2, pos+row_spacing*2,  text="================================", fill="red", font=myfont, justify="center")
    canvas.pack()
    tk.update()

    # ask punters one by one for their bets
    for punter in punterlist:
        if punter.total <= 0:
            sorry = canvas.create_text(screen_width/2, pos+row_spacing*4, text=punter.name + ", you are BROKE. NO BETS!!!!", fill="dark red", font=myfont, justify="center")
            punter.pick = -1
            punter.stake = 0
            tk.update()
            brokeSound.play()
            time.sleep(3)
            canvas.delete(sorry)
        else:
            punter.pick=-1
            punter.stake=-1
            while (punter.pick<0 or punter.pick>6):
                question = canvas.create_text(screen_width/2, pos+row_spacing*4, text=punter.name + ", you have £" + str(punter.total) + ". Pick a horse 1-7", fill="white", font=myfont, justify="center")
                answer = canvas.create_text(screen_width/2, pos+row_spacing*6, text="", fill="orange", font=myfont, justify="center")
                punter.pick = WaitForInteger(canvas, answer) - 1
                canvas.delete(question, answer)
            while (punter.stake<0 or punter.stake>punter.total):
                question = canvas.create_text(screen_width/2, pos+row_spacing*4, text="How much on " + horselist[punter.pick].name + "?", fill="white", font=myfont, justify="center")
                answer = canvas.create_text(screen_width/2, pos+row_spacing*6, text="", fill="orange", font=myfont, justify="center")
                punter.stake = WaitForInteger(canvas, answer)
                if punter.stake > punter.total:
                    sorry = canvas.create_text(screen_width/2, pos+row_spacing*8, text="SORRY NO CREDIT!", fill="dark blue", font=myfont, justify="center")
                    tk.update()
                    time.sleep(3)
                    canvas.delete(sorry)
                canvas.delete(question, answer)
            punter.total = punter.total - punter.stake
            print (punter.name + " placed £" + str(punter.stake) + " on " + horselist[punter.pick].name + " and now has £" + str(punter.total))
        
 
def Race(canvas):
    global keypressed, keyevent
    # clear the scene
    canvas.delete("all")
    # draw the scene
    canvas.create_rectangle(0, 0, screen_width, 7*2*row_spacing+65, fill="green")

    canvas.create_line(finish_pos-horse_step, 1*2*row_spacing-30, finish_pos-horse_step, 7*2*row_spacing+65, width=5, fill="black")
    canvas.create_oval(finish_pos-horse_step-8, 0, finish_pos-horse_step+8, 16, width=5, fill="", outline="gold")
    canvas.create_line(finish_pos-horse_step, 16, finish_pos-horse_step, 1*2*row_spacing-20, width=5, fill="gold")
    canvas.create_oval(finish_pos-horse_step-8, 7*2*row_spacing+30, finish_pos-horse_step+8, 7*2*row_spacing+30+16, width=5, fill="", outline="gold")
    canvas.create_line(finish_pos-horse_step, 7*2*row_spacing+30+16, finish_pos-horse_step, 7*2*row_spacing+65, width=5, fill="gold")

    canvas.create_rectangle(0, 8*2*row_spacing, screen_width, screen_height, fill="dark green")
    pos = row_spacing*17
    canvas.create_text(screen_width/2, pos,                text="================================", fill="red", font=myfont, justify="center")
    canvas.create_text(screen_width/2, pos+row_spacing, text="LET'S RACE", fill="yellow", font=myfont, justify="center")
    canvas.create_text(screen_width/2, pos+row_spacing*2,  text="================================", fill="red", font=myfont, justify="center")
    pos = pos + row_spacing * 3
    for punter in punterlist:
        if punter.pick > -1:
            canvas.create_text(screen_width/2, pos, text=punter.name +" bet £"+ str(punter.stake) +" on "+ horselist[punter.pick].name +" at "+ str(horselist[punter.pick].price) +"/1",
                           fill=horselist[punter.pick].colour, font=myfont, justify="center")
            pos = pos + row_spacing * 1.2

    for h in horselist:
        h.prepare_to_race()

    canvas.pack()
    tk.update()
    random.seed()

    WaitForKeyPress(canvas)
    gunSound.play()
    time.sleep(0.5)
    keypressed = False

    # main race loop
    while True:
        # pick a random horse
        h = random.randint(0,6)
        horse = horselist[h]
        # move that horse
        horse.move()
        #print("Horse ", horse.number, " pos ", horse.pos)
        # update the screen
        tk.update_idletasks()
        tk.update()
        # check for the winner, break from the race loop if we have one
        if horse.pos < finish_pos:
            break
        # Check for Esc
        if keypressed == True:
            if (keyevent.keysym == 'Escape'):
                exit(0)            
        # wait for some time
        time.sleep(horse_wait)

    # announce the winner
    winner_text = horse.name + " is the winner!"
    #canvas.create_text(screen_width/2, (h+1)*row_spacing, text=winner_text)
    #canvas.create_text(screen_width/2, screen_height-200, text=winner_text, fill="dark blue", font=myfont, justify="center")
    canvas.create_text(screen_width/2, 4*row_spacing, text=winner_text, fill="dark blue", font=myfont, justify="center")
    WaitForKeyPress(canvas)

    # return the number of the winning horse so we can calculate punter winnings next
    return h

def Results(canvas, winning_horse_index):
    # clear the scene
    canvas.delete("all")
    # draw the scene
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill="dark green")
    canvas.create_text(screen_width/2, row_spacing,  text="--------------------------------", fill="red", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*2, text="* RESULTS *", fill="yellow", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*3,  text="--------------------------------", fill="red", font=myfont, justify="center")
    pos = row_spacing*5
    i = 1
    winning_horse = horselist[winning_horse_index]
    for punter in punterlist:
        #print("Horse index " + str(winning_horse_index) + " punter pick " + str(punter.pick))
        if punter.pick == winning_horse_index:
            winnings = punter.stake * winning_horse.price
            punter.total = punter.total + winnings + punter.stake
            message = punter.name + " wins £" + str(winnings) + " on " + winning_horse.name
            canvas.create_text(screen_width/2, pos, text=message, fill=winning_horse.colour, font=myfont, justify="center")
            pos = pos + row_spacing*2
            i = i + 1

    sounds.music.load("yankee.mp3")
    sounds.music.play()
    WaitForKeyPress(canvas)
    sounds.music.fadeout(2000)

def Broke(canvas):
    # clear the scene
    canvas.delete("all")
    # draw the scene
    canvas.create_rectangle(0, 0, screen_width, screen_height, fill="black")
    canvas.create_text(screen_width/2, row_spacing,  text="--------------------------------", fill="cyan", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*2, text="* GAME OVER *", fill="magenta", font=myfont, justify="center")
    canvas.create_text(screen_width/2, row_spacing*3,  text="--------------------------------", fill="cyan", font=myfont, justify="center")
    sounds.music.load("yankee_slow.mp3")
    sounds.music.play()
    WaitForKeyPress(canvas)
    

# HORSE-RACE MAIN CODE

# setup a callback on any keypress for keyboard entry
tk.bind_all('<Key>', KeyPress)

# setup a canvas to draw on
canvas = Canvas(tk, width=screen_width, height=screen_height, highlightthickness=0)

# setup horses and punters
Initialize_characters_variables(canvas)
Punters(canvas)

# main game loop
while True:
    numberbroke = DisplayCash(canvas, wait=True)
    print(str(numberbroke)+" punters are broke out of "+str(len(punterlist)))
    if numberbroke == len(punterlist):    # if everyone broke, end the game by breaking out of the game loop
        break
    StartingPrices(canvas)
    winning_horse = Race(canvas)
    print("Horse index ", winning_horse, " ", horselist[winning_horse].name, " is the winner.")
    Results(canvas, winning_horse)

# end the game
Broke(canvas)

