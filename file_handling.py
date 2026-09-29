"""
Path to Graduation - TEXT FILE HANDLING
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
This file handles text file conversions and handling for display using the module Pygame.

History:
April 10, 2025: Date created
May 2, 2025: Date completed
"""

#===IMPORTS===
import pygame
import json
from clickableClass import Text

#initialize pygame
pygame.init()
#initalize screen information for display size
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h

#===FUNCTIONS====

#==LOADING AND SAVINGS===
def load_save(fileName):
    """
    Loads game save.
    
    Args:
        fileName (str) : name of save file
    
    Returns:
        save_file (dict) : dictionary of save file
    """
    
    with open(fileName) as file:
        save_file = json.load(file)
        
    return save_file

#===FILE CONVERSIONS===
def convert_to_string(set_question, strand):
    """
    Converts unicode in question lists to strings for saving.
    
    Args:
        set_question (str) : question set being converted
        strand (str) : subject
    """
    #initalize index counter
    count = 0
    for part in set_question:
        #checks for the unique strand and updates associated unicode character
        if strand == "vectors":
            if "\u2192" in part:
                #replaces the vector arrow character
                part = part.replace("\u2192", "(vec)")
        if "\u221a" in part:
            #replaces the square root character
            part = part.replace("\u221a", "(sqr)")
        if "\u00b2" in part:
            #replaces the superscript 2 character
            part = part.replace("\u00b2", "(ss2)")
        if "\u2082" in part:
            #replaces the subscript 2 character
            part = part.replace("\u2082", "(sb2)")
        if "\u21d2" in part:
            #reaplces the rightfacing double arrow character
            part = part.replace("\u21d2", "(rda)")
        if "\u00b0" in part:
            #reaplces the  degrees character
            part = part.replace("\u00b0", "(deg)")
        if "\u2081" in part:
            #reaplces the subscript 1 character
            part = part.replace("\u2081", "(sb1)")
        if "\u0394" in part:
            #reaplces the delta symbol
            part = part.replace("\u0394", "(delta)")
        if "\u00B3" in part:
            #reaplces the superscript 3 character
            part = part.replace("\u00B3", "(ss3)")
        if "\u03B2" in part:
            #reaplces the beta symbol
            part = part.replace("\u03B2", "(beta)")
        if "\u03B1" in part:
            #reaplces the alpha symbol
            part = part.replace("\u03B1", "(alpha)")
        if "\u03B3" in part:
            #reaplces the gamma symbol
            part = part.replace("\u03B3", "(gamma)")
        if "\u2264" in part:
            #reaplces the less than or equale to character
            part = part.replace("\u2264", "(le)")
        if "\u222A" in part:
            #reaplces the union symbol
            part = part.replace("\u222A", "(union)")
        if "\u2229" in part:
            #reaplces the intersection symbol
            part = part.replace("\u2229", "(int)")
        if "'" in part:
            #replaces the apostrophe (single quote) to avoid escape character issues with converting to a JSON file and back into a string
            part = part.replace("'", "(apos)")
        
        #updates question part
        set_question[count] = part
        #updates index counter
        count+=1
        
    return set_question

def convert_to_uni(set_question, strand):
    """
    Converts keywords in questions to unicode for proper display.
    
    Args:
        set_question (str) : question set being converted
        strand (str) : subject
        
    Returns:
        question_set
    """
    count = 0
    for part in set_question:
        if strand == "vectors":
            if "(vec)" in part:
                part = part.replace("(vec)", "\u2192")
        if "(sqr)" in part:
            part = part.replace("(sqr)", "\u221a")
        if "(ss2)" in part:
            part = part.replace("(ss2)", "\u00b2")
        if "(sb2)" in part:
            part = part.replace("(sb2)", "\u2082")
        if "(rda)" in part:
            part = part.replace("(rda)", "\u21d2")
        if "(deg)" in part:
            part = part.replace("(deg)", "\u00b0")
        if "(sb1)" in part:
            part = part.replace("(sb1)", "\u2081")
        if "(delta)" in part:
            part = part.replace("(delta)", "\u0394")
        if "(ss3)" in part:
            part = part.replace("(ss3)", "\u00B3")
        if "(beta)" in part:
            part = part.replace("(beta)", "\u03B2")
        if "(alpha)" in part:
            part = part.replace("(alpha)", "\u03B1")
        if "(gamma)" in part:
            part = part.replace("(gamma)", "\u03B3")
        if "(le)" in part:
            part = part.replace("(le)", "\u2264")
        if "(union)" in part:
            #replaces the union symbol
            part = part.replace("(union)", "\u222A")
        if "(int)" in part:
            #replaces the intersection symbol
            part = part.replace("(int)", "\u2229")
        if "(apos)" in part:
            part = part.replace("(apos)", "'")
        
        set_question[count] = part
        count+=1
        
    return set_question

#===RETRIEVAL===
def retrieve_questions(num_save, subject, bank_book):
    """
    Gets the questions from the save file.
    
    Args:
        num_save (int) : save number
        subject (str)
    
    Returns:
        big_list (lst[lst]) : list of questions
    """
    if bank_book == "bank":
        destination = "challenge_bank"
    elif bank_book == "book":
        destination = "saved_questions"
    try:
        file = open(f"{destination}_{num_save}.txt", "r")
        infile = file.readlines()
        #sets big list to an empty list
        big_list = []
        for line in infile:
            #strips the newline character from the line
            line = line.strip("\n")
            #removes the outer brackets and quotes from the line
            line = line[2:len(line)-2]
            #splits the string into a list at every
            line = line.split("', '")
            line = convert_to_uni(line, subject)
            #adds to big list
            big_list.append(line)
        #closes the file
        file.close()
    except:
        big_list = None
    
    return big_list

def retrieve_lesson(selected_unit, selected_lesson, strand_subject):
    """
    Retrieves the lesson for output.

    Args:
        selected_unit (int) : unit number
        selected_lesson (int) : lesson number
        strand_subject (str) : subject
    
    Returns:
        lst (lst) : list of lines and potentially images to display
    """

    try:
        #initalize for lst
        lst = []
        sub_group=[]
        
        #open lesson file
        question_file = open(f"{strand_subject}_lessons\\unit{selected_unit}\\lesson{selected_lesson}.txt")
        #get list of question file
        infile = question_file.readlines()
        #initalize height
        height = HEIGHT*(1/16)
        for initial_line in infile:
            #strips newline in line
            line = initial_line.strip("\n")
            #if the line isn't empty space
            if line != "":
                #checks if the line is a picture
                if ".png" in line:
                    #removes brackets enclosing picture name
                    name = line.strip("()")
                    #gets the image and loads it
                    img = pygame.image.load(f"{strand_subject}_lessons\\unit{selected_unit}\\{name}").convert_alpha()
                    #creates image rect
                    rect = img.get_rect()
                    rect.left = WIDTH*(1/8)
                    rect.top = height
                    #adds it to the list
                    sub_group.append((img, rect))
                else:
                    #otherwise converts it to a readable format in pygame
                    line = convert_to_uni([line], strand_subject)
                    #creates a text object
                    line = Text(line[0], "cambriamath", 20, (0,0,0), (WIDTH*(1/8), height))
                    #adjusts the x positioning
                    line.text_rect.left = WIDTH*(1/8)
                    #adds it to main list
                    sub_group.append(line)
                #checks if the last item in the subgroup is a text object
                if isinstance(sub_group[len(sub_group)-1], Text):
                    #updates height
                    height += 50
                else:
                    #if the last object is not a Text object, gets the height from the picture's rect
                    height += sub_group[len(sub_group)-1][1].bottom+sub_group[len(sub_group)-1][1].height
                #checks if the height is greater than the threshold
                if height > HEIGHT*(7/8):
                    #updates the sub group to the list
                    lst.append(sub_group)
                    #resets the subgroup and the height
                    sub_group=[]
                    height = HEIGHT*(1/16)
                #if the line is the last from the iniital list, appends the subgroup to the final list
                elif initial_line == infile[len(infile)-1]:
                    lst.append(sub_group)
            else:
                #if the line is empty space, updates the height to provide the proper line break
                height+=20
    except:
        #sets the list to None if the file doesn't exist or an error has occured
        lst = None

    return lst

#===UPDATE BOOKS AND BANKS===
def update_book(num_save, new_question, strand_subject):
    """
    Updates question book with a single question.
    
    Args:
        num_save (int) : save file number
        new_question (lst) : question list
        strand_subject (str) : subject
    """
    new_question = convert_to_string(new_question, strand_subject)
    with open(f"saved_questions_{num_save}.txt", "a") as question_file:
        print(new_question, file=question_file)
        
def update_bank(num_save, new_question, strand_subject):
    """
    Updates challenge bank with a single question.
    
    Args:
        num_save (int) : save file number
        new_question (lst) : question list
        strand_subject (str) : subject
    """
    new_question = convert_to_string(new_question, strand_subject)
    with open(f"challenge_bank_{num_save}.txt", "a") as question_file:
        print(new_question, file=question_file)

def update_whole(num_save, lst_questions, bank_book, strand_subject):
    """
    Updates either the question book or the challenge bank entirely with a list of questions.

    Args:
        num_save (int) : save file number
        new_question (lst) : question list
        bank_book (str) : bank or book
        strand_subject (str) : subject
    """
    if bank_book == "book":
        bank_book = "saved_questions"
    elif bank_book == "bank":
        bank_book = "challenge_bank"
    if lst_questions:
        with open(f"{bank_book}_{num_save}.txt", "w") as question_file:
            for i in lst_questions:
                i = convert_to_string(i, strand_subject)
                print(i, file=question_file)
