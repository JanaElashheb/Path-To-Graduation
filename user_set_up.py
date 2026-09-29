"""
Path to Graduation - USER SET UP
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Allows user to set up a new save file and get started.

History:
Feb 25, 2025: Date created
Mar 7, 2025: Added the close button to the name, choose_player and weapon screens
Mar 31, 2025: Added the beginning of a storyline and NPC Dialogue
Apr 10, 2025: Added the beginning of the stoyline for vectors and data 
May 4, 2025: Date completed
"""

#===IMPORTS===
import pygame
from clickableClass import Text, Button
import random

#intialize pygame
pygame.init()
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
CENTERED = (WIDTH//2, HEIGHT//2)

#===GAME VARIABLES===
screen = pygame.display.set_mode((WIDTH,HEIGHT))
clock = pygame.time.Clock()

def handle_set_up(current_status, topic):
    name_player = None
    player_image = None
    basic_weapon = None
    while current_status != "QUIT GAME" and current_status != "COMPLETED SET UP":
        if current_status == "CHOOSE NAME":
            name_player, current_status = name(current_status)
        elif current_status == "GET PLAYER IMAGE":
            player_image, current_status = choose_player(current_status)
        elif current_status == "GET WEAPON":
            current_status, basic_weapon = weapon(current_status)
        elif current_status == "STORYLINE":
            if topic == "vectors":
                current_status = storyline_vectors(current_status)
            if topic == "data":
                current_status = storyline_data(current_status)
            
            
    
    return name_player, player_image, current_status, basic_weapon

#fuction for the users username
def name(status):
    """
    Gets username.
    
    Args:
        status (str) : state of game
    
    Returns:
        username (str)
        status (str)
    """
    # Timer for error message
    message_timer = 0
    #giving user the ability to type their username
    username_input = Text("", "colonna", 36, (255, 255, 255), (WIDTH * (3/8), HEIGHT *(9/16)))
    
    #Creating button for exiting game
    close = pygame.image.load("assets\Close Button.png").convert_alpha()
    #changes the size of the image
    close = pygame.transform.scale(close, (50, 50))
    #creates a rectangle for the image
    rect_close = close.get_rect(center = (WIDTH - 40,HEIGHT - HEIGHT + 20))
    
    while status == "CHOOSE NAME":
        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if ready.back.collidepoint(pos):
                    if username != "":
                        status = "GET PLAYER IMAGE"
                    else:
                        #setes the timer for the error message
                        message_timer = pygame.time.get_ticks()
                elif rect_close.collidepoint(pos):
                        status = "QUIT GAME"
                        
            #apart of the writing of the username    
            username_input.write(events)
        
        else:
            #getting mouse potion
            pos = pygame.mouse.get_pos()
            
            screen.fill((23, 23, 23))
            
            #printing the error message
            if message_timer and pygame.time.get_ticks() - message_timer < 1000:
                error_text = Text("You must enter a username!", "Rage", 50, (255, 0, 0), (WIDTH // 2, HEIGHT * (2 / 8)))
                error_text.display()
                
            else:
                message_timer = 0  # Reset timer after message disappears
            
            #displays the close button on screen
            screen.blit(close, rect_close)
            
            #args: text, font, size, f_colour, position
            text = Text("Enter your username: ", "stencil",50,(255, 255, 255), (WIDTH //2, HEIGHT *(3/8)))
            #displays button
            text.display()
            
            #ready button
            ready = Button("Ready", "onyx", 40, (0,0,0), (WIDTH //2, HEIGHT *(10/16)), (64, 224, 208), (5, 5), 5)
            ready.hover((255, 253, 208), pos)
            ready.display()

            #Displays text on screen
            username_input.display()
            #need to give the acctual username value to a variable to work
            username = username_input.text_value()

            pygame.display.update()
            clock.tick(30)
    
    return username, status
        
#function for the users player image            
def choose_player(status):
    """
    Allows user to select their character.
    
    Args:
        status (str) : state of game
        
    Returns:
        player
        status (str)
    """
    #setting run to true
    #run = True
    #setting player chose to False
    player_chosen = False
    # Track selected player
    selected_player = None
    # Timer for error message
    message_timer = 0  
    
    #setting the normal and enlarged size of the images
    normal_size = (150, 150)
    enlarged_size = (180, 180)
    
    #Creating button for exiting game
    close = pygame.image.load("assets\Close Button.png").convert_alpha()
    #changes the size of the image
    close = pygame.transform.scale(close, (50, 50))
    #creates a rectangle for the image
    rect_close = close.get_rect(center = (WIDTH - 40,HEIGHT - HEIGHT + 20))
    
    while status == "GET PLAYER IMAGE":
        for events in pygame.event.get():
            if events.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                        
                if rect_player1.collidepoint(pos):
                    selected_player = "player1"
                    player = "sprites/Player 1.png"
                    player_chosen = True
                elif rect_player2.collidepoint(pos):
                    selected_player = "player2"
                    player = "sprites/Player 2.png"
                    player_chosen = True
                
                if ready.back.collidepoint(pos):
                    if player_chosen:
                        status = "GET WEAPON"
                    else:
                        message_timer = pygame.time.get_ticks()
                        
                elif rect_close.collidepoint(pos):
                    player = None 
                    status = "QUIT GAME"
                        
        screen.fill((23, 23, 23))
        pos = pygame.mouse.get_pos()
        
        #displays the close button on screen
        screen.blit(close, rect_close)
            
        #making text on the screen
        text = Text("Choose your player: ", "stencil", 50, (255, 255, 255), (WIDTH // 2, HEIGHT * (3 / 8)))
        text.display()
        
        # Load and scale player images
        player1_img = pygame.image.load("sprites\Player 1.png").convert_alpha()
        player2_img = pygame.image.load("sprites\Player 2.png").convert_alpha()
        
        size1 = enlarged_size if selected_player == "player1" else normal_size
        size2 = enlarged_size if selected_player == "player2" else normal_size
        
        player1_img = pygame.transform.scale(player1_img, size1)
        player2_img = pygame.transform.scale(player2_img, size2)
        
        rect_player1 = player1_img.get_rect(center=(WIDTH//2*(3/4), HEIGHT//2))
        rect_player2 = player2_img.get_rect(center=(WIDTH//2*(20/16), HEIGHT//2))
        
        screen.blit(player1_img, rect_player1)
        screen.blit(player2_img, rect_player2)
        
        #making the ready button
        ready = Button("Ready", "onyx", 40, (0, 0, 0), (WIDTH // 2, HEIGHT * (10 / 16)), (64, 224, 208), (5, 5), 5)
        ready.hover((255, 253, 208), pos)
        ready.display()
               
        #printing the error message
        if message_timer and pygame.time.get_ticks() - message_timer < 1000:
            error_text = Text("You must select a player!", "Rage", 50, (255, 0, 0), (WIDTH // 2, HEIGHT * (2 / 8)))
            error_text.display()
        else:
            message_timer = 0  # Reset timer after message disappears
        
        pygame.display.update()
        clock.tick(30)
    
    return player, status
         
        
#function for the users weapon        
def weapon(status):
    """
    Gives beginner weapon.
    
    Args:
        status (str) : state of game
        
    Returns:
        status (str)
    """
    #setting chest opned to False
    chest_opened = False
    #setting recieved weapon to false
    received_weapon = False
    
    weapon_img = None
    received_message = ""
    
    # Timer for error message
    message_timer = 0  
    
    #setting the normal size of the image
    normal_size = (150, 150)
    
    #making a list on ONLY the basic weapons user can get in the begining
    basic_weapons = ["basic sword", "basic wand", "basic axe"]
    
    #Creating button for exiting game
    close = pygame.image.load("assets\Close Button.png").convert_alpha()
    #changes the size of the image
    close = pygame.transform.scale(close, (50, 50))
    #creates a rectangle for the image
    rect_close = close.get_rect(center = (WIDTH - 40,HEIGHT - HEIGHT + 20))
    
    
    while status == "GET WEAPON":
        screen.fill((23, 23, 23))
        pos = pygame.mouse.get_pos()
        
        for events in pygame.event.get():
            if events.type == pygame.KEYDOWN:
                if events.key == pygame.K_ESCAPE:
                    status = "QUIT GAME"
            if events.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if rect_chest.collidepoint(pos) and not chest_opened:
                    chest = pygame.image.load("assets\Open chest.png").convert_alpha()
                    chest = pygame.transform.scale(chest, normal_size)
                    
                    weapon = random.choice(basic_weapons)
                    file_name = "assets/" + weapon.lower() + ".png"
                    weapon_img = pygame.image.load(file_name).convert_alpha()
                    weapon_img = pygame.transform.scale(weapon_img, normal_size)            
                    rect_weapon_img = weapon_img.get_rect(center=(CENTERED))            
                    chest_opened = True
                    received_weapon = True
                    received_message = f"You have received the {weapon}!"
                
                if start.back.collidepoint(pos):
                    if not received_weapon:
                        message_timer = pygame.time.get_ticks()
                    else:
                        status = "STORYLINE"
        
                elif rect_close.collidepoint(pos):
                        status = "QUIT GAME"
        
        #displays the close button on screen
        screen.blit(close, rect_close)
            
        text = Text("Open chest: ", "stencil", 50, (255, 255, 255), (WIDTH // 2, HEIGHT * (3 / 8)))
        text.display()
        
        chest_image = "assets\Open chest.png" if chest_opened else "assets\Closed chest.png"
        chest = pygame.image.load(chest_image).convert_alpha()
        chest = pygame.transform.scale(chest, normal_size)            
        rect_chest = chest.get_rect(center=(CENTERED))            
        screen.blit(chest, rect_chest)
        
        if chest_opened and weapon_img:
            screen.blit(weapon_img, rect_weapon_img)
            received_text = Text(received_message, "script", 50, (0, 255, 0), (WIDTH // 2, HEIGHT * (4.5 / 8)))
            received_text.display()
        #the start button
        start = Button("Start Game", "onyx", 40, (0, 0, 0), (WIDTH // 2, HEIGHT * (10 / 16)), (64, 224, 208), (5, 5), 5)
        start.hover((255, 253, 208), pos)
        start.display()
        
        #printing teh error message
        if message_timer and pygame.time.get_ticks() - message_timer < 1000:
            error_text = Text("You must open the chest first!", "Rage", 50, (255, 0, 0), (WIDTH // 2, HEIGHT * (2 / 8)))
            error_text.display()
        else:
            message_timer = 0  # Reset timer after message disappears
        
        pygame.display.update()
        clock.tick(30)
    
    return status, weapon

def wrap_text(text, font, max_width):
    words = text.split(" ")
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        if font.size(test_line)[0] > max_width:  # Check if line width exceeds box
            lines.append(current_line)
            current_line = word + " "
        else:
            current_line = test_line

    lines.append(current_line)  # Add the last line
    return lines


def storyline_vectors(status):
    dialogue = [
    "Hi! My name is Kai and it's great that you're joining our team!                                                                                                                                             (Press SPACE to continue)", 
    "We've been trying for weeks to stop the evil Thorne Blackwater.",
    "He's taken our little series of islands and destroyed them.",
    "See how dark and grey they are? We're working to get that back to normal.",
    "And you got here just in time. We're about to go out to see him.", 
    "But BE CAREFUL!! Blackwater has a hoard of helpers trying to stop us.", 
    "To defeat them we need to work through some Calculus and Vectors questions.", 
    "But don't worry, I'll be there along the way to help you.",
    "To move left and right use the 'A' and 'D' keys and 'SPACE' to jump.", 
    "C'mon, Lets go!!"
    
    ]
    current_line = 0

    #load NPC image
    npc_image = pygame.image.load("sprites\Kai.png")
    vectors_start_map = pygame.image.load("maps\Vectors Start Map.png")

    dialogue_box = pygame.Rect(WIDTH/5, HEIGHT/5, WIDTH/2, HEIGHT/4)
    dialogue_box.center=((WIDTH/2),(HEIGHT/2 + HEIGHT/3))
    text_margin = 20  # Space around text inside the box
    max_text_width = dialogue_box.width - 2 * text_margin
    max_text_height = dialogue_box.height - 2 * text_margin

    FONT = pygame.font.Font(None, 56)

    # Main loop
    while status == "STORYLINE":
        screen.fill((225, 208, 253))
        background = pygame.image.load("backgrounds\Dialogue Background Vectors.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0,0))
        

        # Draw NPC image
        screen.blit(npc_image, (WIDTH/4, HEIGHT/1.8, WIDTH/3, HEIGHT/5))
        
        # Draw dialogue box
        pygame.draw.rect(screen, (0, 0, 0), dialogue_box)
        pygame.draw.rect(screen, (255, 255, 255), dialogue_box, 5)  # Border

        wrapped_lines = wrap_text(dialogue[current_line], FONT, max_text_width)

        # Render and display text inside the box
        y_offset = dialogue_box.y + text_margin
        for line in wrapped_lines:
            if y_offset + FONT.get_height() > dialogue_box.y + dialogue_box.height - text_margin:
                break  # Stop rendering if text exceeds box height

            text_surface = FONT.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (dialogue_box.x + text_margin, y_offset))
            y_offset += FONT.get_height() + 5  # Move down for next line
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Move to the next dialogue line
                    current_line += 1
                    if current_line >= len(dialogue):  # Reset dialogue loop
                        status = "COMPLETED SET UP"
                        
        if current_line == 3:
            
            background = pygame.image.load("maps\Vectors Start Map.png")
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            screen.blit(background, (0,0))
            
            # Draw NPC image
            screen.blit(npc_image, (WIDTH/4, HEIGHT/1.8, WIDTH/3, HEIGHT/5))

            # Draw dialogue box
            pygame.draw.rect(screen, (0, 0, 0), dialogue_box)
            pygame.draw.rect(screen, (255, 255, 255), dialogue_box, 5)  # Border
            
            wrapped_lines = wrap_text(dialogue[current_line], FONT, max_text_width)

            # Render and display text inside the box
            y_offset = dialogue_box.y + text_margin
            for line in wrapped_lines:
                if y_offset + FONT.get_height() > dialogue_box.y + dialogue_box.height - text_margin:
                    break  # Stop rendering if text exceeds box height

                text_surface = FONT.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (dialogue_box.x + text_margin, y_offset))
                y_offset += FONT.get_height() + 5  # Move down for next line

    
        pygame.display.update()
        clock.tick(60)
    return status



def storyline_data(status):
    dialogue = [
    "Hi! My name is Elysia and it's great that you're joining our team!                                                                                                                                             (Press SPACE to continue)", 
    "We've been trying for weeks to stop the evil Cassian Drai.",
    "He's taken our island and is destroying it.",
    "See all those black lines going through our island? We're working to get that back to normal.",
    "And you got here just in time. We're about to go out to see him.", 
    "But BE CAREFUL!! Drai has a hoard of helpers trying to stop us.", 
    "To defeat them we need to work through some Data management questions.", 
    "But don't worry, I'll be there along the way to help you.",
    "To move left and right use the 'A' and 'D' keys and 'SPACE' to jump.",
    "C'mon, Lets go!!"
    
    ]
    current_line = 0

    #load NPC image
    npc_image = pygame.image.load("sprites\Elysia.png")
    data_start_map = pygame.image.load("maps\Data Start Map.png")

    dialogue_box = pygame.Rect(WIDTH/5, HEIGHT/5, WIDTH/2, HEIGHT/4)
    dialogue_box.center=((WIDTH/2),(HEIGHT/2 + HEIGHT/3))
    text_margin = 20  # Space around text inside the box
    max_text_width = dialogue_box.width - 2 * text_margin
    max_text_height = dialogue_box.height - 2 * text_margin

    FONT = pygame.font.Font(None, 56)

    # Main loop
    while status == "STORYLINE":
        screen.fill((225, 208, 253))
        background = pygame.image.load("backgrounds\Dialogue Background Data.png")
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
        screen.blit(background, (0,0))
        

        # Draw NPC image
        screen.blit(npc_image, (WIDTH/4, HEIGHT/1.8, WIDTH/3, HEIGHT/5))
        
        # Draw dialogue box
        pygame.draw.rect(screen, (0, 0, 0), dialogue_box)
        pygame.draw.rect(screen, (255, 255, 255), dialogue_box, 5)  # Border

        wrapped_lines = wrap_text(dialogue[current_line], FONT, max_text_width)

        # Render and display text inside the box
        y_offset = dialogue_box.y + text_margin
        for line in wrapped_lines:
            if y_offset + FONT.get_height() > dialogue_box.y + dialogue_box.height - text_margin:
                break  # Stop rendering if text exceeds box height

            text_surface = FONT.render(line, True, (255, 255, 255))
            screen.blit(text_surface, (dialogue_box.x + text_margin, y_offset))
            y_offset += FONT.get_height() + 5  # Move down for next line
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  # Move to the next dialogue line
                    current_line += 1
                    if current_line >= len(dialogue):  # Reset dialogue loop
                        status = "COMPLETED SET UP"
                        
        if current_line == 3:
            
            background = pygame.image.load("maps\Data Start Map.png")
            background = pygame.transform.scale(background, (WIDTH, HEIGHT))
            screen.blit(background, (0,0))
            
            # Draw NPC image
            screen.blit(npc_image, (WIDTH/4, HEIGHT/1.8, WIDTH/3, HEIGHT/5))

            # Draw dialogue box
            pygame.draw.rect(screen, (0, 0, 0), dialogue_box)
            pygame.draw.rect(screen, (255, 255, 255), dialogue_box, 5)  # Border
            
            wrapped_lines = wrap_text(dialogue[current_line], FONT, max_text_width)

            # Render and display text inside the box
            y_offset = dialogue_box.y + text_margin
            for line in wrapped_lines:
                if y_offset + FONT.get_height() > dialogue_box.y + dialogue_box.height - text_margin:
                    break  # Stop rendering if text exceeds box height

                text_surface = FONT.render(line, True, (255, 255, 255))
                screen.blit(text_surface, (dialogue_box.x + text_margin, y_offset))
                y_offset += FONT.get_height() + 5  # Move down for next line

    
        pygame.display.update()
        clock.tick(60)
    return status