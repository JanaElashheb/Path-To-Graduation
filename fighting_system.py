"""
Path to Graduation - FIGHTING SYSTEM
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Allows the user to battle enemies and solve math problems with turn-based fighting system.

History:
Mar 23, 2025: Date created
May 4, 2025: Date completed
"""

#===IMPORTS===
import pygame
import random
from clickableClass import Text, Button
from file_handling import update_book, update_bank
from vectors_generate import generate_vectors
from data_generate import generate_data

#initalize pygame
pygame.init()
#get screen information
screen_info = pygame.display.Info()

#===CONSTANTS===
#initalize screen height and width
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
TILE_SIZE = 50
TEXT_THRESHOLD = HEIGHT*(2/8)

#initalize background
fight_image = pygame.image.load("backgrounds\\fighting_screen.png").convert_alpha()
FIGHT_IMG = pygame.transform.scale(fight_image, (WIDTH, HEIGHT))

#===GAME VARIABLES===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("PATH TO GRADUATION")

#=====FUNCTIONS=====
def fight(status, player, inventory, save_number, fight_subject, unit, lesson, max_health):
    """
    Allows player to fight.

    Args:
        status (str) : status of game
        player (Player) : player sprite
        questions_lst (lst[lst])
        inventory (Inventory)
        unit (int)
        lesson (int)

    Returns:
        status (str)
        player (Player)
        inventory (Inventory)
    """
    
    #initalize instructions
    instructions = Text("Click 'attack' when ready.","twcen",30,(0, 0, 0),(WIDTH//2, TEXT_THRESHOLD))

    #initalizes a timer for an error message
    msg_timer = 0

    #initalize the player to have the first turn
    turn = "player"
    
    #initalize to know if the hint should be displayed
    display_hint = False
    
    #gets enemy health and name
    enemy_name = player.enemy_collide.name
    enemy_health = player.enemy_collide.health*unit

    #gets and loads enemy image
    enemy_img = pygame.image.load("enemies/" + enemy_name + ".png")
    enemy_rect = enemy_img.get_rect()
    enemy_rect.x = WIDTH*(3/4)
    enemy_rect.y = HEIGHT//2
    #gets the min/max attack threshold for the enemy
    max_attack = player.enemy_collide.max_attack*unit
    min_attack = player.enemy_collide.min_attack*unit
    difficulty = player.enemy_collide.difficulty

    #gets and loads player image
    player_img = player.load_image
    player_rect = player_img.get_rect()
    player_rect.x = WIDTH*(1/6)
    player_rect.y = HEIGHT//2

    #generates a random number within the question list for the specified topic
    if fight_subject == "vectors":
        set = generate_vectors(difficulty, unit, lesson, fight_subject)
    elif fight_subject == "data":
        set = generate_data(difficulty, unit, lesson, fight_subject)
    
    #formats question and gets the last line
    question = format_question(set[0], instructions.text_rect)
    last_line = len(question)-1
    
    #creates textbox for input and create text for input 
    text_input = Text("", "Arial", 35, (0, 0, 0), (WIDTH//2, question[last_line].text_rect.height+question[last_line].text_rect.bottom)) 
    textbox = pygame.Rect((0, 0), (text_input.text_rect.width,text_input.text_rect.height))
    textbox.center = (WIDTH//2, question[last_line].text_rect.height+question[last_line].text_rect.bottom)

    #initalize buttons and text
    give_up = Button("Give up", "bell",20,(0,0,0),(player_rect.x, player_rect.bottom-20),(197, 237, 219),(10,10),10)
    attack = Button("ATTACK","bell",20,(0,0,0),(WIDTH//2, textbox.height+textbox.bottom),(197, 237, 219),(10,10),10)

    #initalizes the hint button
    hint_button=None
    #initalize the skip button
    skip_button = None
    #initalize for any items consumed
    item_consumed = "none"

    #initalize incorrect message and switch turn button
    incorrect = Text("MISSED!", "twcen", 30, (0,0,0),(player_rect.left, player_rect.top - 60))
    switch = Button("Click for Turn", "bell",20,(0,0,0),(WIDTH//2, HEIGHT//2+120),(197, 237, 219),(10,10),10)

    #initalize the value the player's experience will rise by
    exp_rise = 1
    #change it according to the difficulty level based on lesson number
    if difficulty == "hard":
        exp_rise = 2+lesson
        #create hint and skip button if the question is hard
        hint_button = Button("HINT","bell",20,(0,0,0),(WIDTH//2, attack.text_rect.height+attack.text_rect.bottom),(197, 237, 219),(10,10),10)
        skip_button = Button("SKIP","bell",20,(0,0,0),(player_rect.x, give_up.text_rect.height+give_up.text_rect.bottom),(197, 237, 219),(10,10),10)
    elif difficulty == "medium":
        exp_rise = 2

    while status == "FIGHT": 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if give_up.back.collidepoint(pos):
                    status = "GAVE UP"
                #if it's the player's turn
                if turn == "player":
                    if attack.back.collidepoint(pos):
                        #if the answer is correct
                        if answer.lower() == set[1].lower():
                            #gets player's attack value against enemy
                            attack_value = player_attack(player, inventory)
                            enemy_health -= attack_value
                            player.exp += exp_rise
                            update_book(save_number, set, fight_subject)
                        else:
                            msg_timer = pygame.time.get_ticks()
                            update_bank(save_number, set, fight_subject)

                        #generates a random number within the question list for the specified topic
                        if fight_subject == "vectors":
                            set = generate_vectors(difficulty, unit, lesson, fight_subject)
                        elif fight_subject == "data":
                            pass
                        #formats question and gets the last line
                        question = format_question(set[0], instructions.text_rect)
                        last_line = len(question)-1

                        #updates position of textbox and correspondingly the other buttons
                        text_input.text_rect.center = (WIDTH//2, question[last_line].text_rect.height+question[last_line].text_rect.bottom)
                        textbox.center = (WIDTH//2, question[last_line].text_rect.height+question[last_line].text_rect.bottom)
                        attack.text_rect.center=(WIDTH//2, textbox.height+textbox.bottom)
                        
                        #checks the difficulty level and gives a hint
                        if difficulty != "easy" and difficulty != "medium":
                            hint_button = Button("HINT","bell",20,(0,0,0),(WIDTH//2, attack.text_rect.height+attack.text_rect.bottom),(197, 237, 219),(10,10),10)
                        else:
                            hint_button = None
                        display_hint = False

                        #gets random attack from enemy
                        random_attack = random.randint(min_attack, max_attack)
                        #gets defense
                        enemy_attack, defense = player_defense(player, inventory, random_attack)
                        #updates player health
                        player.health -= enemy_attack
                        
                        #update defense and health loss texts
                        hit = Text(f"The enemy has launched an attack of {random_attack} damage!", "twcen",30,(0,0,0),(WIDTH//2, HEIGHT//2))
                        lost_health = Text(f"You have lost -{enemy_attack} health (defended +{defense})!", "twcen",30,(0,0,0),(WIDTH//2, hit.text_rect.bottom+hit.text_rect.height))
                        #sets turn to enemy's
                        turn = "enemy"
                    #if player has a hint available and has pressed for hint
                    if hint_button:
                        if hint_button.back.collidepoint(pos):
                            hint = Text(f"Hint: {set[2]}", "cambriamath", 30, (0,0,0), (WIDTH//2, hint_button.text_rect.bottom+hint_button.text_rect.height + 40))
                            display_hint = True
                    #if the player has clicked the skip button
                    if skip_button:
                        if skip_button.back.collidepoint(pos):
                            #skips enemy
                            status = "SKIPPED"
                    #checks if the user has clicked anything in the inventory
                    item_consumed = inventory.check_clicks(pos, player, unit, max_health, True)
                    
                    #checks if the user has used a hint spell
                    if item_consumed == "used hint":
                        #creates the hint button
                        hint_button = Button("HINT","bell",20,(0,0,0),(WIDTH//2, attack.text_rect.height+attack.text_rect.bottom),(197, 237, 219),(10,10),10)
                        item_consumed = "none"
                    #if the player has used the skip item
                    elif item_consumed == "used skip":
                        status = "SKIPPED"
                #if it's the enemies turn
                else:
                    #if the player clicks the switch button
                    if switch.back.collidepoint(pos):
                        turn = "player"
            
            #if the player is attempting to write something during their turn
            if event.type == pygame.KEYDOWN and turn == "player":
                text_input.write(event, len(set[1]))

        else:
            screen.blit(FIGHT_IMG, (0,0))
            
            #gets cursour position
            pos = pygame.mouse.get_pos()
            
            #displays the enemy and their health
            screen.blit(enemy_img, enemy_rect)
            enemy_life = Text(f"HEALTH: {enemy_health}", "bell", 20, (0,0,0), (enemy_rect.x, enemy_rect.top - 40))
            pygame.draw.rect(screen, (160,242,248), enemy_life.text_rect)
            enemy_life.display()
            
            screen.blit(player_img, player_rect)
            player_life = Text(f"HEALTH: {player.health}", "bell", 20, (0,0,0), (player_rect.x, player_rect.top - 40))
            pygame.draw.rect(screen, (160,242,248), player_life.text_rect)
            player_life.display()

            #display give up button
            give_up.hover((149, 199, 177),pos)
            give_up.display()

            if turn == "player":
                inventory.display()
                inventory.toggle(pos)
                
                display_question(question)

                pygame.draw.rect(screen, (160,242,248), instructions.text_rect)
                instructions.display()

                #display attack button
                attack.hover((149, 199, 177),pos)
                attack.display()

                #display hint button if exists
                if hint_button:
                    hint_button.hover((149, 199, 177), pos)
                    hint_button.display()

                #displays the skip button if it exists
                if skip_button:
                    skip_button.hover((149, 199, 177), pos)
                    skip_button.display()

                #display hint if allowed
                if display_hint:
                    pygame.draw.rect(screen, (160,242,248), hint.text_rect)
                    hint.display()
                
                pygame.draw.rect(screen, (160,242,248), textbox)
                #updates position where user inputs
                text_input.text_rect.center = (WIDTH//2, question[last_line].text_rect.height+question[last_line].text_rect.bottom)
                #display's user input
                text_input.display()
                answer = text_input.text_value()
                #updates associated textbox
                textbox.width, textbox.height = text_input.text_rect.width, text_input.text_rect.height
                textbox.center = (WIDTH//2, question[last_line].text_rect.height+question[last_line].text_rect.bottom)

                if item_consumed == "used skip":
                    #sets turn to skipped and sets empties answer to ensure user doesn't even accidentally win question
                    status = "SKIPPED"
            
            elif turn == "enemy":
                if msg_timer and pygame.time.get_ticks() - msg_timer < 2000:
                    pygame.draw.rect(screen, (160,242,248), incorrect.text_rect)
                    incorrect.display()
                #creates the rects for the messages to be displayed against the background
                pygame.draw.rect(screen, (160,242,248), hit.text_rect)
                pygame.draw.rect(screen, (160,242,248), lost_health.text_rect)
                #display enemy attack and health loss messages
                hit.display()
                lost_health.display()
                #display switch button
                switch.hover((149, 199, 177),pos)
                switch.display()
            
            #if the enemy has been defeated, sends player to win screen
            if enemy_health <= 0:
                status = "WON"
            #if the player has been defeated, sends player to death screen
            if player.health <= 0:
                status = "DEATH"
            
            #update display and frame
            pygame.display.update()
            clock.tick(60)
            #print(status)
            #print(item_consumed)
    
    return status, player, inventory

#===FORMAT AND DISPLAY FUNCTIONS===
def format_question(unformatted, reference_rect):
    """
    Formats question for display (specific to the turn-based fighting system).
    
    Args:
        unformatted (str) : question
        reference_rect (Rect) : reference rect for positioning
        
    Returns:
        formatted (lst) : list of question rects to display
    """

    #converts the string into a list to display 
    if "(n)" in unformatted:
        unformatted = unformatted.split("(n)")
    else:
        unformatted = [unformatted]

    #initalize list for final format
    formatted = []
    #initalize list for the most recent rect for positioning 
    recent_rect = None
    for line in unformatted:
        #checks if this isn't the first line
        if recent_rect:
            #sets the text to a little under the previous
            height = recent_rect.bottom+40
        else:
            #if this is the first line, then sets a little under the given rect
            height = reference_rect.bottom+40
        #creates new line
        n_line = Text(line, "cambriamath", 30, (0,0,0), (WIDTH//2, height))
        #adds to final list
        formatted.append(n_line)
        #updates latest rect
        recent_rect = n_line.text_rect
        
    return formatted

def display_question(content):
    """
    Displays question.
    
    Args:
        content (lst) : list of question's lines, as Text instances
    """
    for line in content:
        pygame.draw.rect(screen, (160,242,248), line.text_rect)
        line.display()

#===PLAYER ATTCK/DEFENSE===
def player_attack(player, inventory):
    """
    Gets player's attack.
    
    Args:
        player (Player)
        inventory (Inventory)
        
    Returns:
        full_attack (int) : full attack
    """
    full_attack = player.attack + inventory.attack
    
    return full_attack

def player_defense(player, inventory, enemy_attack):
    """
    Gets player's defense.

    Args:
        player (Player)
        inventory (Inventory)
        enemy_attack (int) : enemy attack value
        
    Returns:
        enemy_attack (int) 
        defense_value (int) : negated effect of enemy's attack
    """
    defense_value = inventory.defense + player.defense
    enemy_attack -= defense_value
    if enemy_attack < 0:
        enemy_attack = 0

    return enemy_attack, defense_value