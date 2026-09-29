"""
Path to Graduation - MAIN
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
This is the main file that handles overall navigation for the game Path to Graduation.

History:
Feb 24, 2025: Date created
May 4, 2025: Date completed
"""

#===IMPORTS===
import pygame
from menu import navigate_menu
from vectors import play_vec
from data import play_data
from file_handling import load_save

#initalize pygame
pygame.init()

#get screen information
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
CENTERED = (WIDTH//2, HEIGHT//2)

#lets user access menu
current_state, num_save = navigate_menu()

while current_state != "QUIT GAME":
    #checks if the user is starting a new vectors file
    if current_state == "NEW_CALC":        
        current_state = play_vec(num_save)
    #checks if user is starting a new data file
    elif current_state == "NEW_DATA":
        current_state = play_data(num_save)
    #checks if user is loading a save
    elif current_state == "LOAD SAVE" and num_save:
        #loads save file
        saved_game = load_save(f"save_{num_save}.txt")     
        #checks which subject the save file is in
        #loads vector world
        if saved_game["subject"] == "vectors":
            current_state = play_vec(num_save, saved_game)
        #loads data world
        elif saved_game["subject"] == "data":
            current_state = play_data(num_save, saved_game)
    elif current_state == "RETURN TO MENU":
        #lets user access menu
        current_state, num_save = navigate_menu()

#quits pygame
pygame.quit()
