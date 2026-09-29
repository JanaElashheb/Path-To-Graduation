"""
Path to Graduation - MENU
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
This file handles user navigation and interaction with the menu.

History:
Jan 21, 2025: Date created
Jan 23, 2025: Added the new game and information button, added the title path 2 grad
Jan 27, 2025: Added the change of screens for the main menu
Feb 5, 2025: Added the screen to choose a math option, add some titles to the other screens, added temproray buttons to the maths on main screen for easy accesss
Feb 12, 2025: Added another screen when pressed on calc and vectors it takes right away to the function calculus and vectors, to get the username and choose their player
Feb 13, 2025: Edited the name, and player function, and added the the weapon function, added the start_game function, which allows the user to play in the world (all under the calculus and vectors function)
Feb 24, 2025: Added and updated save system; changed to menu.py and added main.py
Feb 25, 2025: Added user set up file
March 3, 2025: Added backgrounds and updated asthetic
Mar 18, 2025: Added the close buttons
May 4, 2025: Date completed
"""

#===IMPORTS===
import pygame
import os
from clickableClass import Button, Text, Close

#initialize pygame
pygame.init()
#initalize screen information for display size
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
CENTERED = (WIDTH//2, HEIGHT//2)
TILE_SIZE = 50

#===GAME VARIABLES===
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("PATH TO GRADUATION: MENU")

def home_screen(state):
    """
    Displays menu screen.
    
    Args:
        state (str) : current status of game
    
    Returns:
        state (str)
    """
    
    #Creating button for exiting game
    close = Close()
    
    #initalize homescreen background
    home_screen = pygame.image.load("backgrounds\home screen.png")
    home_screen = pygame.transform.scale(home_screen, (WIDTH, HEIGHT))

    #initalize play button
    play = Button("Play", "Rage", 40, (0,0,0), CENTERED, (64, 224, 208), (5, 5), 5)
    #initalize info button
    info = Button("Information", "rage", 40, (0,0,0), (WIDTH // 2, HEIGHT * (10/16)), (64, 224, 208), (5,5), 5)
    #display title
    title = Text("Path 2 Grad", "Rage",100,(255, 255, 255), (WIDTH // 2, HEIGHT *(3/8)))
    
    while state == "MENU":
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                state = "QUIT GAME"
            if events.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play.back.collidepoint(pos):
                    state = "SAVES"
                elif info.back.collidepoint(pos):
                    state = "INFO"
                elif close.rect.collidepoint(pos):
                    state = "QUIT GAME"
        else:
            pos = pygame.mouse.get_pos()
            
            screen.blit(home_screen, (0,0))
            close.display()

            play.hover((255, 253, 208), pos)
            play.display()
            
            info.hover((255, 253, 208), pos)
            info.display()
            
            pygame.draw.rect(screen, (0,0,0), title.text_rect)
            title.display()

            pygame.display.update()
            clock.tick(30)
        
    return state

#==SAVE FILE HANDLING FUNCTIONS (MENU SPECIFIC)==
def check_for_saves():
    """
    Checks for any existing save files.
    
    Returns:
        save1 (str) : displays load or new game if or if does not exist
        save2 (str) : displays load or new game if or if does not exist
        save3 (str) : displays load or new game if or if does not exist
        list_saves (lst) : list of booleans if a save is new or not
    """
    list_saves = [True, True, True]
    save1 = "New Game"
    save2 = "New Game"
    save3 = "New Game"
    
    #checks if the save 1 file exists
    if os.path.exists("save_1.txt"):
        save1 = "Load Game"
        list_saves[0] = False
    #checks if the save 2 file exists
    if os.path.exists("save_2.txt"):
        save2 = "Load Game"
        list_saves[1] = False
    #checks if the save 3 file exists
    if os.path.exists("save_3.txt"):
        save3 = "Load Game"
        list_saves[2] = False
    
    return save1, save2, save3, list_saves

def delete_save(text, list_saves, save_num):
    """
    Deletes a save file.
    
    Args:
        text (str) : save file status
        list_saves (lst) : bools telling if save file is a new game or not
        save_num (int) : save file number
    
    Returns:
        text (str)
        list_saves (lst)
    """
    #checks if file exists in first place
    if os.path.exists(f"save_{save_num}.txt"):
        if os.path.exists(f"saved_questions_{save_num}.txt"):
            os.remove(f"saved_questions_{save_num}.txt")
        if os.path.exists(f"challenge_bank_{save_num}.txt"):
            os.remove(f"challenge_bank_{save_num}.txt")
        #removes file
        os.remove(f"save_{save_num}.txt")
        #changes text status of save to denote this
        text = "New Game"
        #changes new game status to true
        list_saves[save_num-1] = True
    
    return text, list_saves

def saves(state, num_save):
    """
    Loads existing saves.
    
    Args:
        state (str) : state of game
    
    Returns:
        state (str)
    """

    #checks saves and initalizes if they are new games or not
    s1Text, s2Text, s3Text, save_lists = check_for_saves()
    
    #create close button
    close = Close()
    
    #initalize back to menu button
    backToMenu = Button("Back to Menu", "Onyx", 25, (0,0,0), (WIDTH // 2, HEIGHT * (14/16)), (255,255,255), (5,5), 5)
    #initalize background
    background = pygame.image.load("backgrounds\play_button_background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    #create and display text for instructions to delete a save
    delSave = Text("Click 'D' AND simultaneously the # of save (1-3) you wish to delete.", "cambriamath",20,(255, 255, 255),(WIDTH//2, HEIGHT*(1/4)))
    #initalize title text
    title = Text("Path 2 Grad", "Rage",100,(255, 255, 255), (WIDTH // 2, HEIGHT *(3/8)))

    while state == "SAVES":
        #checks if user has clicked X
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                state = "QUIT GAME"
            #checks if user has clicked the mouse
            if events.type == pygame.MOUSEBUTTONDOWN:
                #gets mouse position
                pos = pygame.mouse.get_pos()
                #returns user to menu
                if backToMenu.back.collidepoint(pos):
                    state = "MENU"
                #checks if user has clicked a save button
                if save1.back.collidepoint(pos):
                    #checks if user has a new game here
                    if save_lists[0]:
                        state = "NEW GAME"
                    #otherwise loads existing save
                    else:
                        state = "LOAD SAVE"
                    #sets save number to corresponding save file
                    num_save = 1
                elif save2.back.collidepoint(pos):
                    if save_lists[1]:
                        state = "NEW GAME"
                    else:
                        state = "LOAD SAVE"
                    num_save = 2
                elif save3.back.collidepoint(pos):
                    if save_lists[2]:
                        state = "NEW GAME"
                    else:
                        state = "LOAD SAVE"
                    num_save = 3
                elif close.rect.collidepoint(pos):
                        state = "QUIT GAME"
                        
            #checks if user clicked a button
            elif events.type == pygame.KEYDOWN:
                #checks if the user has clicked any of the following keys
                if events.key in [pygame.K_d, pygame.K_1, pygame.K_2, pygame.K_3]:
                    #gets a dictionary of all pressed keys
                    keys = pygame.key.get_pressed()
                    #checks if user has clicked d and 1 at same time
                    if keys[pygame.K_d] and keys[pygame.K_1]:
                        #deletes corresponding save file
                        s1Text, save_lists = delete_save(s1Text, save_lists, 1)
                    elif keys[pygame.K_d] and keys[pygame.K_2]:
                        s2Text, save_lists = delete_save(s2Text, save_lists, 2)
                    elif keys[pygame.K_d] and keys[pygame.K_3]:
                        s3Text, save_lists = delete_save(s3Text, save_lists, 3)
        else:
            pos = pygame.mouse.get_pos()
            screen.fill((191,148,228))
            screen.blit(background, (0,0))
            
            #displays the close button on screen
            close.display()
            
            #initalize game buttons
            save1 = Button(f"{s1Text}", "Rage", 40, (0,0,0), CENTERED, (64, 224, 208), (5, 5), 5)
            #when mouse hovers over button, changes colour
            save1.hover((255, 253, 208), pos)
            #displays button
            save1.display()

            #creates and displays button for save button 2
            save2 = Button(f"{s2Text}", "Rage", 40, (0,0,0), (WIDTH // 2, HEIGHT * (10/16)), (64, 224, 208), (5,5), 5)
            save2.hover((255, 253, 208), pos)
            save2.display()

            #creates and displays button for save button 3
            save3 = Button(f"{s3Text}", "Rage", 40, (0,0,0), (WIDTH // 2, HEIGHT * (12/16)), (64, 224, 208), (5,5), 5)
            save3.hover((255, 253, 208), pos)
            save3.display()
            
            
            pygame.draw.rect(screen, (0,0,0), delSave.text_rect)
            delSave.display()
            
            backToMenu.hover((0,0,255), pos)
            backToMenu.display()
            
            pygame.draw.rect(screen, (0,0,0), title.text_rect)
            title.display()
            
            pygame.display.update()
            clock.tick(30)
    
    return state, num_save

def new_game(state):
    """
    Creates a new game based on the math chosen.
    
    Args:
        state (str) : state of game
        
    Returns:
        state (str)
    """
    
    #create close button
    close = Close()
    
    while state == "NEW GAME":
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                state = "QUIT GAME"
            if events.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if backToSaves.back.collidepoint(pos):
                    state = "SAVES"
                elif calc.back.collidepoint(pos):
                    state = "NEW_CALC"
                elif data.back.collidepoint(pos):
                    state = "NEW_DATA"
                elif close.rect.collidepoint(pos):
                        state = "QUIT GAME"
        else:
            #gets mouse position
            pos = pygame.mouse.get_pos()
            #fills screen with background
            screen.fill((191,148,228))
            background = pygame.image.load("backgrounds\play_button_background.png")
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            screen.blit(background, (0,0))
            
            #displays the close button on screen
            close.display()
            
            #see class for more details
            calc = Button("Calculus and Vectors", "colonna", 40, (0,0,0), CENTERED, (64, 224, 208), (5, 5), 5)
            #when mouse hovers over button, changes colour
            calc.hover((255, 253, 208), pos)
            #displays button
            calc.display()
            
            functions = Button("Advanced Functions", "colonna", 40, (0,0,0), (WIDTH // 2, HEIGHT * (9/16)), (64, 224, 208), (5,5), 5)
            functions.hover((255, 253, 208), pos)
            functions.display()
            
            data = Button("Data Management", "colonna", 40, (0,0,0), (WIDTH // 2, HEIGHT * (10/16)), (64, 224, 208), (5,5), 5)
            data.hover((255, 253, 208), pos)
            data.display()
            
            #args: text, font, size, f_colour, position, b_colour, padding, rounding 
            backToSaves = Button("Back to Saves", "Onyx", 25, (0,0,0), (WIDTH // 2, HEIGHT * (13/16)), (255,255,255), (5,5), 5)
            backToSaves.hover((0,0,255), pos)
            backToSaves.display()
            
            #args: text, font, size, f_colour, position
            text = Text("Choose your math", "Rage",100,(255, 255, 255), (WIDTH // 2, HEIGHT *(3/8)))
            pygame.draw.rect(screen, (0,0,0), text.text_rect)
            #displays button
            text.display()
                            
            pygame.display.update()
            clock.tick(30)
        
    return state
    
def information(state):
    """
    Information screen.
    
    Args:
        state (str) : state of game
        
    Returns:
        state (str)
    """
    
    #create close button
    close = Close()
    
    #load the background
    background = pygame.image.load("backgrounds\play_button_background.png")
    background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    
    #initalize text for instructions
    title = Text("Information", "Rage",100,(255, 255, 255), (WIDTH // 2, HEIGHT *(3/8)))
    details = Text("This is an educational game. Controls:", "onyx", 35, (255, 255, 255), (CENTERED))
    controls = Text("AD for movement. Space for jump.", "onyx", 35, (255, 255, 255), (WIDTH // 2, HEIGHT * (9/16)))
    
    #initalize button to return to menu
    backToMenu = Button("Back to Menu", "Onyx", 25, (0,0,0), (WIDTH // 2, HEIGHT * (10/16)), (255,255,255), (5,5), 5)
    
    while state == "INFO":
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                state = "QUIT GAME"
            if events.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if backToMenu.back.collidepoint(pos):
                    state = "MENU"
                elif close.rect.collidepoint(pos):
                        state = "QUIT GAME"
        else:
            pos = pygame.mouse.get_pos()
            screen.blit(background, (0,0))
            
            #displays the close button on screen
            close.display()
            
            #displays the following instructions
            pygame.draw.rect(screen, (0,0,0), title.text_rect)
            title.display()
            
            pygame.draw.rect(screen, (0,0,0), details.text_rect)
            details.display()
            
            pygame.draw.rect(screen, (0,0,0), controls.text_rect)
            controls.display()
            
            #displays the back to menu button and its hover colour
            backToMenu.hover((0,0,255), pos)
            backToMenu.display()
            
            pygame.display.update()
            clock.tick(30)
            
    return state

def navigate_menu():
    """
    Navigates menu.
    
    Returns:
        status (str) : state of game
        save_num (int) : save file number
    """
    status = "MENU"
    save_num = None

    while status not in ["NEW_CALC", "FUNCTIONS", "NEW_DATA", "LOAD SAVE","QUIT GAME"]:
        if status == "MENU":
            status = home_screen(status)
        elif status == "INFO":
            status = information(status)
        elif status == "SAVES":
            status, save_num = saves(status, save_num)
        elif status == "NEW GAME":
            status = new_game(status)
            
    return status, save_num