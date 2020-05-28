from firebase import firebase
from tkinter import *
from threading import Thread
from tkinter import simpledialog
from tkinter import messagebox
import pygame
import keyboard

SOUND_FILE = 'noti.wav'
DATABASE = "YOUR PATH HERE"

pygame.mixer.init()
sound = pygame.mixer.Sound(SOUND_FILE)

firebase = firebase.FirebaseApplication(DATABASE, None)
firebase.delete("Messages", '')
firebase.put("Messages", "AUTOMATED", "This online chat was made by Arnav Arora. Enjoy chatting with others on this server!")

nameOfChatter = None
root = Tk()
root.title("Online Chat")

def checkForEnter ():
    while True:
        if keyboard.is_pressed('enter'):
            verifyMessage(entry.get())

def changeName():
    global nameOfChatter
    firebase.delete("Messages", nameOfChatter)
    dialog = simpledialog.askstring("Change Your Name!", "What would you like your name to be changed to?")

    if dialog == None or dialog == "":
        nameOfChatter = "Guest User"
    else:
        nameOfChatter = dialog

def chatInfo():
    global nameOfChatter
    clientCount = 0
    result = firebase.get('Messages', '')
    clientList = list(result.keys())
    for client in clientList:
        if client == "AUTOMATED":
            clientList.remove(client)

    if clientList == None or clientList == []:
        messagebox.showinfo("Chatroom Information", "Only you are online on this chat server as of right now.\n\nClients:\n1. " + nameOfChatter)
    else:
        if nameOfChatter not in clientList:
            clientList.append(nameOfChatter)
        clientLabel = "Clients:"
        for client in clientList:
            clientCount += 1
            clientLabel = clientLabel + "\n" + str(clientCount) + ". " + client

        showLabel = "There are " + str(clientCount) + " number of people online on this chat server as of right now.\n\n"
        messagebox.showinfo("Chatroom Information", showLabel + clientLabel)

def verifyMessage (message):
    if message == "" or message == None:
        messagebox.showerror("Alert", "Please enter something in the chat...")
    else:
        entry.delete(0, 'end')
        firebase.put("Messages", nameOfChatter, message)

def clearChat ():
    label['text'] = ""
 

canvas = Canvas(root, height = 500, width = 1000)
canvas.pack()

frame = Frame(root, bg = '#80c1ff', bd = 10)
frame.place(relwidth = 0.75, relheight = 0.15, relx = 0.5, rely = 0.1, anchor = 'n')

topLabel = Label(frame, text = "Welcome to Online Chat", font = ('AvenirNext-Regular', 30))
topLabel.place(relheight = 1, relwidth = 1)

label = Label(root, text = "", font = ('AvenirNext-Regular', 18))
wraplength = label.winfo_width()
label.place(relwidth = 1, rely = 0.25)

frame2 = Frame(root, bg = '#80c1ff', bd = 10)
frame2.place(relx = 0.5, relwidth = 1, relheight = 0.1, rely = 0.8, anchor = 'n')

entry = Entry(frame2, font = ('AvenirNext-Regular', 18))
entry.place(relx = 0.23, relwidth = 0.55, relheight = 1)

button = Button(frame2, text= "Send", highlightbackground= 'lightgray', font = ('AvenirNext-Regular', 16), command = lambda: verifyMessage(entry.get()))
button.place(relx = 0.8, relwidth = 0.1, relheight = 1)

otherButton = Button(frame2, text= "Clear Chat", highlightbackground= 'lightgray', font = ('AvenirNext-Regular', 16), command = lambda: clearChat())
otherButton.place(relx = 0.9, relwidth = 0.1, relheight = 1)

changeNameButton = Button(frame2, text= "Change Name", highlightbackground= 'lightgray', font = ('AvenirNext-Regular', 16), command = lambda: changeName())
changeNameButton.place(relwidth = 0.12, relheight = 1)

changeNameButton = Button(frame2, text= "Chat Info", highlightbackground= 'lightgray', font = ('AvenirNext-Regular', 16), command = lambda: chatInfo())
changeNameButton.place(relx = 0.12, relwidth = 0.1, relheight = 1)


def askForName():
    dialog = simpledialog.askstring("Welcome!", "Please enter your first name below to enter the chatroom.")
    global nameOfChatter
    if dialog == None or dialog == "":
        nameOfChatter = "Guest User"
    else:
        nameOfChatter = dialog

    Thread(target=checkForEnter).start()
    Thread(target=getMessages).start()
    start()

def start ():
    root.mainloop()

def getMessages ():
    
    serverMessages = []
    while True:
        result = firebase.get('Messages', '')
        messageList = []

        try:
            messageList = list (result.items())
        except Exception:
            print (f"[EXCEPTION] Trying to reconnect...")

        if serverMessages != messageList:
            uniques = set(messageList) - set(serverMessages)
            uniques = list(uniques)
            for item in uniques:
                stringToAdd = str(item[0]) + ": " + str(item[1])
                uniques [uniques.index(item)] = stringToAdd
            
            for item in uniques:
                label['text'] = label['text'] + "\n" + item
            root.update()

            if all(char in stringToAdd for char in nameOfChatter):
                pass
            else:
                sound.play()
            serverMessages = messageList
askForName()