"""
Path to Graduation - DATA
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
This file allows the user to play through the math strand of Data Management.

History:
Mar 23, 2025: Date created
May 5, 2025: Date completed
May 5, 2025: Created function assign_lesson_max to account for if user has the required exp to move onto next level; 
             updated main() to account for restrictions on if a user can move to the next unit
"""

#===IMPORTS===
import pygame
import json
from world_player_class import Player, World
from clickableClass import Text, Button, Close, Setting
import random
from user_set_up import handle_set_up
from inventory_class import Inventory
from fighting_system import fight
from question_interactions import nav_question_menu
from file_handling import load_save

#initalize pygame
pygame.init()
#get screen information
screen_info = pygame.display.Info()

#===CONSTANTS===
#initalize screen height and width
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
#initialize tile size of map
TILE_SIZE = 50
#initalize max number of tilemaps
MAX_MAPS = 5
#initalize subject
SUBJECT = "data"
#initalize scroll threshold
SCROLL_THRES = 300
#exp needed to continue to next unit
UNIT_THRESHOLD = 100
#initalize max levels for units
U1_MAX = 2
#initalize total unit max
UNIT_MAX = 1

#===LOAD BACKGROUND IMAGES===
#initalize background images
clouds_image = pygame.image.load("backgrounds\\data\\clouds.png").convert_alpha()
CLOUDS_IMG = pygame.transform.scale(clouds_image, (WIDTH, HEIGHT))

#initalize win screen image
win_image = pygame.image.load("backgrounds\win_screen.png").convert_alpha()
WIN_IMG = pygame.transform.scale(win_image, (WIDTH, HEIGHT))
#initalize lose screen image
lose_image = pygame.image.load("backgrounds\lose_screen.png").convert_alpha()
LOSE_IMAGE = pygame.transform.scale(lose_image, (WIDTH, HEIGHT))
#initalize death screen image
death_image = pygame.image.load("backgrounds\death_screen.png").convert_alpha()
DEATH_IMG = pygame.transform.scale(death_image, (WIDTH, HEIGHT))
#initalize skip screen image
skip_image = pygame.image.load("backgrounds\skip_background.png").convert_alpha()
SKIP_SCREEN = pygame.transform.scale(skip_image, (WIDTH, HEIGHT))
#initalize give up screen image
giveup_image = pygame.image.load("backgrounds\give_up.png").convert_alpha()
GIVEUP_SCREEN = pygame.transform.scale(giveup_image, (WIDTH, HEIGHT))
#initalize settings background
setting_image = pygame.image.load("backgrounds\settings_background.png").convert_alpha()
SETTING_BG = pygame.transform.scale(setting_image, (WIDTH, HEIGHT))

#===GAME VARIABLES===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

pygame.display.set_caption("PATH TO GRADUATION: "+SUBJECT.upper())

#===FUNCTIONS===

#==GAME HANDLING==
def save_game(player, world, inventory, num_save, maps_collection, bg_scroll, farthest_unit, farthest_lesson):
    """
    Saves game.
    
    Args:
        player (Player)
        world (World)
        inventory (Inventory)
        num_save (int) : save file number
        collection (dict) : collection of saved maps
    """
    save_dictionary = {
        "subject" : SUBJECT,
        "player" : player.get_dict(),
        "world" : world.get_dict(),
        "inventory" : inventory.get_dict(),
        "scroll" : bg_scroll,
        "saved_maps" : maps_collection,
        "unit" : farthest_unit,
        "lesson" : farthest_lesson
        }
    
    with open(f"save_{num_save}.txt", "w") as save_file:
        json.dump(save_dictionary, save_file)

def setting(status, player, current_map, inventory, file_save_num, prior_maps, bg_scroll, unit, lesson):
    """
    Opens the settings for the player.

    Args:
        status (str)

    Returns:
        status (str)
    """

    save = Button("SAVE GAME", "twcen", 50, (0,0,0), (WIDTH//2, HEIGHT*(2/8)), (100, 204, 180), (5,5), 5)
    menu_return = Button("Return to Menu", "twcen", 50, (0,0,0), (WIDTH//2, save.text_rect.bottom+save.text_rect.height), (100, 204, 180), (5,5), 5)
    exit = Button("Exit Game", "twcen", 50, (0,0,0), (WIDTH//2, menu_return.text_rect.bottom+menu_return.text_rect.height), (100, 204, 180), (5,5), 5)
    return_game = Button("RETURN TO GAME", "twcen", 50, (0,0,0), (WIDTH//2, HEIGHT*(6/8)), (100, 204, 180), (5,5), 5)

    while status == "SETTINGS":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if exit.back.collidepoint(pos):
                    status = "QUIT GAME"
                elif save.back.collidepoint(pos):
                    #saves the game
                    save_game(player, current_map, inventory, file_save_num, prior_maps, bg_scroll, unit, lesson)
                    save.b_colour = (101, 132, 184)
                elif menu_return.back.collidepoint(pos):
                    status = "RETURN TO MENU"
                elif return_game.back.collidepoint(pos):
                    status = "GAMEPLAY"
        else:
            pos = pygame.mouse.get_pos()
            screen.blit(SETTING_BG, (0,0))

            save.hover((101, 132, 184), pos)
            save.display()
            
            menu_return.hover((101, 132, 184), pos)
            menu_return.display()

            exit.hover((101, 132, 184), pos)
            exit.display()

            return_game.hover((101, 132, 184), pos)
            return_game.display()
            
            pygame.display.update()
            clock.tick(60)

    return status

def revive(num_save):
    """
    Reloads last checkpoint.

    Args:
        save_num (int) : save number
    
    Returns:
        bg_scroll (int) : culmative background scroll
        world_map (World)
        prior_maps (dict{dict}) : dictionary of previously attained and changed maps
        player_position (int, int) : (x, y) position of player
        playe_velocity (int) : player's velocity
    """
    saveFile = load_save(f"save_{num_save}.txt")

    #gets the culmative scroll background from previous save
    bg_scroll = saveFile["scroll"]
    #initalizes from current map number and current tilemap so items collected are not reloaded
    world_map = World(saveFile["world"]["subject"], saveFile["world"]["map"], saveFile["world"])
    #gets all the prior accessed maps so player is reset
    prior_maps = saveFile["saved_maps"]
    #gets the player position and velocity
    player_position = saveFile["player"]["position"]
    player_velocity = saveFile["player"]["velocity"]

    #sets status back to gameplay
    status = "GAMEPLAY"

    return status, bg_scroll, world_map, prior_maps, player_position, player_velocity

#===UNIT (LEVEL)/LESSON AND FEEDBACK FUNCTIONS===
def item_draw(player_inventory, max, impact, loss_gain):
    """
    Randomizes the items the user loses or gains.

    Args:
        player_inventory (Inventory)
        max (int) : max items the player can lose/gain for every occurance of item lost/gained. The item being selected twice does not apply to this limit.
        impact (int) : likelihood of player losing/gaining how many items
        loss_gain (str) : if the user is gaining or losing items
    
    Returns:
        player_inventory (Inventory)
        message (str) : message of items lost or gained
    """
    #initalize list for items that will be lost
    final_items = []

    sign = 1
    if loss_gain == "loss":
        sign = (-1)
        #initalize list for all items potentially affected
        items = player_inventory.check_contain()
    else:
        items = ["coin", "heal", "hint", "skip"]

    message = ""

    if items:
        for i in range(0, impact):
            #gets an item by index that will be imapacted
            get_item = random.randint(0, len(items)-1)
            #gets actual item
            affected = items[get_item]
            #generates random number for items lost/gained
            value = random.randint(0, max)
            if affected != "coin":
                player_inventory.updateItem(affected, (sign*value))
            else:
                player_inventory+=(sign*value)
            #initalize item loss message
            msg = [affected, str(value)]
            
            #check in case item has already been affected
            found = False
            cont = 0
            #checks list of items until list runs out or item is found
            while cont!=len(final_items) and not found:
                #if the item is found, denotes that
                if final_items[cont][0] == affected:
                    found=True
                #otherwise updates counter and continues
                else:
                    cont+=1
            #if the item was indeed found, updates message at that index
            if found:
                new_loss = int(final_items[cont][1]) + value
                msg[1] = str(new_loss)
                final_items[cont] = msg
            #otherwise just adds it to the end
            else:
                final_items.append(msg)
        #formats final message
        for i in final_items:
            add_item = i[0]+" : "+i[1]+"; "
            message+=add_item
            #removes '; ' from final message
            message = message[:-2]
    #if the user has no items to lose in the first place
    else:
        if loss_gain == "loss":
            message = "Wow, you actually don't have anything to lose...or you lost nothing!"
        else:
            message = "Erm...guess there's nothing for Mother Luck to give?"
    
    return message, player_inventory

def won(status, player, inventory):
    """
    Screen that plays if user completes question.
    
    Args:
        status (str) : state of game
        player (Player)
        inventory (Inventory)
        
    Returns:
        status (str)
        player (Player)
    """

    if player.enemy_collide.difficulty == "hard":
        amount_gained = 4
        max_gain = 3
    else:
        amount_gained = 2
        max_gain = 2

    gain_msg, inventory = item_draw(inventory, max_gain, amount_gained, "gain")

    text = Text("You won the battle! Click 'c' to continue. You picked up:","inkfree",40,(0,0,0),(WIDTH//2,HEIGHT//2))
    text2 = Text(gain_msg, "inkfree",40,(0,0,0),(WIDTH//2,text.text_rect.bottom+text.text_rect.height))

    #removes the enemy from player collision
    defeated_enemy = player.enemy_collide
    defeated_enemy.kill()

    while status == "WON":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    status = "GAMEPLAY"
        else:
            screen.blit(WIN_IMG, (0,0))
            
            pygame.draw.rect(screen, (255, 255, 255), text.text_rect)
            pygame.draw.rect(screen, (255, 255, 255), text2.text_rect)
            text.display()
            text2.display()
            
            pygame.display.update()
            clock.tick(60)
    
    return status, player

def give_up(status, player, inventory, unit, lesson):
    """
    If player gives up battle.

    Args:
        status (str)
        player (Player)
        inventory (Inventory)
    
    Returns:
        status (str)
        player (Player)
        inventory (Inventory)
    """
    #removes the enemy from player collision
    defeated_enemy = player.enemy_collide
    defeated_enemy.kill()

    #initalize max number of items user can lose at a specific occurance
    maximun = unit*2+lesson-1
    lose_chances = 2

    #lose items and get message telling user which ones they lost
    lost_items, inventory = item_draw(inventory, maximun, lose_chances, "loss")
    
    #initalize text to alert user to what they lost and to continue after giving up
    gave_up = Text("YOU GAVE UP!", "inkfree", 30, (0,0,0), (WIDTH//2, HEIGHT*(2/5)))
    its_okay = Text("But that's okay! You can utilize your resources to tackle any questions that challenged you, and always view them in your challenge bank.", "cambriamath", 20, (0,0,0), (WIDTH//2, gave_up.text_rect.bottom+gave_up.text_rect.height))
    lost = Text("You still lost the following:", "cambriamath", 20, (0,0,0), (WIDTH//2, its_okay.text_rect.bottom+its_okay.text_rect.height))
    display_items = Text(lost_items, "cambriamath", 20, (0,0,0), (WIDTH//2, lost.text_rect.bottom+lost.text_rect.height))
    cont = Text("Click 'c' to continue back to your game.", "cambriamath", 20, (0,0,0), (WIDTH//2, display_items.text_rect.bottom+display_items.text_rect.height))

    close = Close()

    while status == "GAVE UP":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    status = "GAMEPLAY"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if close.rect.collidepoint(pos):
                    status = "QUIT GAME"
        else:
            screen.blit(GIVEUP_SCREEN, (0,0))
            close.display()
            
            #create text backgrounds and display associated text
            pygame.draw.rect(screen, (255,255,255), gave_up.text_rect)
            pygame.draw.rect(screen, (255,255,255), its_okay.text_rect)
            pygame.draw.rect(screen, (255,255,255), lost.text_rect)
            pygame.draw.rect(screen, (255,255,255), display_items.text_rect)
            pygame.draw.rect(screen, (255,255,255), cont.text_rect)
            gave_up.display()
            its_okay.display()
            lost.display()
            display_items.display()
            cont.display()
            
            pygame.display.update()
            clock.tick(60)

    return status, player, inventory

def skipped_screen(status, player):
    """
    Player's skip screen.

    Args:
        status (str)
        player (Player)

    Returns:
        status (str)
        player (Player)
    """
    #removes the enemy from player collision
    defeated_enemy = player.enemy_collide
    defeated_enemy.kill()

    skipped = Text("YOU SKIPPED!", "inkfree", 30, (0,0,0), (WIDTH//2, HEIGHT*(2/5)))
    cont = Text("Nothing happens now. Carry on with by clicking 'c'.", "inkfree", 30, (0,0,0), (WIDTH//2, skipped.text_rect.bottom+skipped.text_rect.height))

    #initalize close button
    close = Close()

    while status == "SKIPPED":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    status = "GAMEPLAY"
        else:
            screen.blit(SKIP_SCREEN, (0,0))
            close.display()

            #draws text background and display text
            pygame.draw.rect(screen, (255,255,255), skipped.text_rect)
            pygame.draw.rect(screen, (255,255,255), cont.text_rect)
            skipped.display()
            cont.display()
            
            pygame.display.update()
            clock.tick(60)

    return status, player


def death_screen(status, num_save, player, inventory, unit, lesson, maximun_health, current_world, prior_status):
    """
    Player's death screen.

    Args:
        status (str)
        player (Player)
        inventory (Inventory)
        unit (int)
        lesson (int)
        maximun_health (int) : player's maximum health value
        current_world (lst) : tilemap of current world
        prior_status (str) : prior status of game

    Returns:
        status (str)
        player (Player)
        inventory (Inventory)
        bg_scroll (int) : culmative background scroll
        world_map (World)
        prior_maps (dict{dict}) : dictionary of previously attained and changed maps
        prior_status (str) : prior status of game
    """

    #initalize death message and continue screen
    death_message = Text("YOU DIED!!", "inkfree", 30, (0,0,0), (WIDTH//2, HEIGHT*(2/8)))
    restart = Text("You will now restart from the last checkpoint.", "cambriamath", 30, (0,0,0), (WIDTH//2, death_message.text_rect.bottom+death_message.text_rect.height))
    cont = Button("RESTART", "cambriamath", 40, (0,0,0), (WIDTH//2, HEIGHT*(6/8)), (100, 204, 180), (5,5), 5)

    #if player dies to an enemy
    if player.enemy_collide:
        #removes the enemy from player collision
        defeated_enemy = player.enemy_collide
        defeated_enemy.kill()
        maximun_lose = unit*2+lesson
        lose_chances = 3
        lost_message, inventory = item_draw(inventory, maximun_lose, lose_chances, "loss")
        lost_items = Text("YOU HAVE LOST THE FOLLOWING:", "cambriamath", 20, (0,0,0), (WIDTH//2, restart.text_rect.bottom+restart.text_rect.height))
        display_lost = Text(lost_message, "cambriamath", 20, (0,0,0), (WIDTH//2, lost_items.text_rect.bottom+lost_items.text_rect.height))
        
    else:
        lost_items = None
        display_lost = None
        prior_status = "death by other"

    #loads the last checkpoint/save
    saveFile = load_save(f"save_{num_save}.txt")

    #gets the culmative scroll background from previous save
    bg_scroll = saveFile["scroll"]
    #initalizes world from previous save and gets prior accessed worlds as well
    world_map = World(saveFile["world"]["subject"], saveFile["world"]["map"], current_world)
    prior_maps = saveFile["saved_maps"]
    playerDict = saveFile["player"]
    #reintalizes player for positioning
    player = Player(playerDict["image"],playerDict["username"],playerDict["health"],playerDict["position"],playerDict["attack"],playerDict["defense"],playerDict["experience"],playerDict["velocity"])
    player.health = maximun_health//2

    while status == "DEATH":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if cont.back.collidepoint(pos):
                    status = "GAMEPLAY"
        else:
            pos = pygame.mouse.get_pos()
            screen.blit(DEATH_IMG, (0,0))
            
            #draws backgrounds for texts
            pygame.draw.rect(screen, (255,255,255), death_message.text_rect)
            pygame.draw.rect(screen, (255,255,255), restart.text_rect)
            #displays text 
            death_message.display()
            
            #displays items lost if any
            if display_lost and lost_items:
                pygame.draw.rect(screen, (255,255,255), lost_items.text_rect)
                pygame.draw.rect(screen, (255,255,255), display_lost.text_rect)
                display_lost.display()
                lost_items.display()

            #displays text and continue button
            restart.display()
            cont.hover((101, 132, 184), pos)
            cont.display()

            pygame.display.update()
            clock.tick(60)
    
    return status, player, inventory, bg_scroll, world_map, prior_maps, prior_status

#===WORLD HANDLING FUNCTIONS===
def update_world(current_world, increment, saved_maps, scroll):
    """
    Updates world.
    
    Args:
        current_world (World)
        increment (int) : (+) or (-) value depending on if user is going back or ahead a map
        save_maps (dict) : dictionary of saved maps
        scroll (int) : background scroll

    Returns:
        new_world (World)
        saved_maps (dict{dict})
        new_scroll (int) : updated scroll value
    """

    #checks if the current world map number is less than the max number of maps and over (or) 0
    if current_world.map_number <= MAX_MAPS and current_world.map_number > 0:
        #gets the map number
        map_num = current_world.map_number + increment
        #checks if the map has already been accessed before
        if saved_maps["amount"] >= map_num:
            #gets tilemap of world
            previous_world = saved_maps["tilemap_"+str(map_num)]["map"]
            #creates world
            new_world = World(SUBJECT, map_num, None, previous_world)
            #updates background scroll
            new_scroll = saved_maps["tilemap_"+str(map_num)]["bg_scroll"]
        #otherwise creates new map
        else:
            new_world = World(SUBJECT, map_num)
            #this line is possibly redundant, but need it for return value: MAKE N/OTE TO POTENTIALLY REMOVE
            new_scroll = scroll
        #checks if current map is already in saved maps
        if "tilemap_"+str(current_world.map_number) not in saved_maps:
            #creates a subdict for the map
            saved_maps["tilemap_"+str(current_world.map_number)] = {}
            #updates saved maps
            saved_maps["amount"] +=1
        #updates dictionary with current world information
        saved_maps["tilemap_"+str(current_world.map_number)]["map"] = current_world.tile_map
        saved_maps["tilemap_"+str(current_world.map_number)]["bg_scroll"] = scroll
        #deletes current world
        del current_world
    else:
        #if user isn't going anywhere new, change nothing (case of errors)
        new_world = current_world
        new_scroll = scroll

    return new_world, saved_maps, new_scroll

#==MAIN GAME FUNCTIONS==

def draw_bg(culmative_scroll):
    """
    Draws the background.

    Args:
        culmative_scroll (int) : culmative background scroll
    """
    width = CLOUDS_IMG.get_width()
    for image in range(5):
        screen.blit(CLOUDS_IMG, ((image * width) - culmative_scroll, 0))

def assign_lesson_max(player_unit):
    """
    Assigns maximun lessons.
    
    Args:
        player_unit (int) : current unit
    
    Returns:
        max_lessons (int) : max lessons in unit
    """
    if player_unit == 1:
        max_lessons = U1_MAX

    return max_lessons

def main(world_map, bg_scroll, player, inventory, prev_maps, unit, lesson, status, num_save, prior_status, maximun_health, current_lesson_max):
    """
    Main game loop.
    
    Args:
        world_map (World)
        bg_scroll (int) : background scroll
        player (Player)
        inventory (Inventory)
        prev_maps (dict{dict}) : dictionary of previous world saves
        unit (int) : current unlocked unit
        lesson (int) : farthest lesson unlocked in current unit
        status (str) : status of game
        num_save (int) : save file number
        prior_status (str) : prior (game) status of user
        maximun_health (int) : maximun possible health
        current_lesson_max (int) : current lesson max possible
        
    Returns:
        status (str)
        bg_scroll (int)
        player (Sprite)
        world_map (World)
        prev_maps (dict{dict})
        unit (int)
        lesson (int)
        maximun_health (int)
        current_lesson_max (int)
    """
    #initalize setting button
    setting = Setting()
    #initalize for if user is checking inventory
    seeInventory = False

    #initalize book icon
    book_img = pygame.image.load("assets\\book icon.png").convert_alpha()
    book_icon = pygame.transform.scale(book_img, (TILE_SIZE, TILE_SIZE))
    book_rect = book_icon.get_rect()
    #sets the icon right underneath the inventory icon
    book_rect.left = inventory.rect.left
    book_rect.top = inventory.rect.bottom + 30

    #checks if the user wasn't just fighting with an enemy or returning from another screen
    if not player.enemy_collide and prior_status != "screen":
        #checks if there is a bg_scroll value
        if bg_scroll:
            #updates scroll and draws world map earlier for correct display
            scroll=0
            scroll-=bg_scroll
            world_map.draw_tile(world_map.tile_list, scroll)
            prior_status = "gameplay"
    else:
        #resets collision detection of enemy
        player.enemy_collide = None

    #initalize timer for lesson message
    lesson_msg_timer = 0
    unit_msg_timer = 0
    continue_unit_timer = 0
    
    show_x = Text("CLICK X", "cambriamath", 20, (0,0,255), (40, HEIGHT-20))
    collected_lesson_msg = Text("YOU HAVE COLLECTED A LESSON!!!", "cambriamath", 20, (0,0,255), (40, HEIGHT-20))
    collected_lesson_msg.text_rect.left = 40
    collected_unit_msg = Text("UNIT COLLECTED! Save your game - next time you enter, you'll be able to move to the next map!!", "cambriamath", 20, (0,0,255), (40, HEIGHT-20))
    collected_unit_msg.text_rect.left = 40
    contiue_unit_msg = Text("You need at least 100 EXP and all lessons in order to move on to the next unit! Solve questions correctly!", "cambriamath", 20, (0,0,255), (40, HEIGHT-20))
    contiue_unit_msg.text_rect.left = 40

    while status == "GAMEPLAY":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            #if user clicks a key
            if event.type == pygame.KEYDOWN:
                #checks if the player can move through the tilemap and if they are clicking x
                if player.move_map:
                    player.move_map = False
                    if event.key == pygame.K_x:
                        #checks if the background scroll is greater than the scroll threshold (if player is on rightmost side of map)
                        if bg_scroll > SCROLL_THRES:
                            #updates tilemap up 1
                            world_map, prev_maps, bg_scroll = update_world(world_map, 1, prev_maps, bg_scroll)
                            #sets player rect to 0 to appear on left side of screen
                            player.rect.x = 0
                            #resets bg_scroll
                            bg_scroll = 0
                            #auto saves the game
                            save_game(player, world_map, inventory, num_save, prev_maps, bg_scroll, unit, lesson)
                        #checks if the background scroll is less than the scroll threshold (player is on the leftmost side of the map)
                        elif bg_scroll < SCROLL_THRES:
                            #updates tilemap down 1
                            world_map, prev_maps, bg_scroll = update_world(world_map, (-1), prev_maps, bg_scroll)
                            #sets player rect to right side of screen
                            player.rect.x = WIDTH
                            #updates scroll and draws tilemap to appear on correct position
                            scroll-=bg_scroll
                            world_map.draw_tile(world_map.tile_list, scroll)
                            #auto saves the game
                            save_game(player, world_map, inventory, num_save, prev_maps, bg_scroll, unit, lesson)
                
            #if the player has clicked the mouse
            if event.type == pygame.MOUSEBUTTONDOWN:
                    #gets mouse position
                    pos = pygame.mouse.get_pos()
                    #if the inventory is open
                    if seeInventory:
                        #checks if the user is attempting to close the inventory and updates accordingly
                        if inventory.rect.collidepoint(pos):
                            seeInventory = False
                        else:
                            #checks if a user has clicked an item on the inventory hotbar for corresponding actions
                            inventory.check_clicks(pos, player, unit, maximun_health)
                    #if the inventory is closed and the user clicked the inventory icon
                    elif inventory.rect.collidepoint(pos) and not seeInventory:
                        seeInventory = True
                    #checks if the user has clicked the book icon
                    if book_rect.collidepoint(pos):
                        status = "QUESTION MENU"
                    #checks if the user has clicked the settings
                    if setting.rect.collidepoint(pos):
                        status = "SETTINGS"
        
        else:
            #fills screen with sky blue
            screen.fill((103, 192, 240))
            draw_bg(bg_scroll)
            #gets mouse position
            pos = pygame.mouse.get_pos()

            #display setting
            setting.display()

            #update player movement and get the culmative background scroll
            scroll = player.move(world_map.tile_map, world_map.tile_list, bg_scroll, world_map.groups, inventory)
            #update culmative background scroll
            bg_scroll -= scroll

            #if the player has collided with an enemy
            if player.enemy_collide:
                #sends user to question screen
                status = "FIGHT"
            
            if seeInventory:
                #turns inventory on
                inventory.toggle(pos)

            #draws world
            world_map.draw_tile(world_map.tile_list, scroll)
            
            #draws the player
            player.draw()
            #if the player is on a world portal, display the sign to display x
            if player.move_map:
                pygame.draw.rect(screen, (255,255,255), show_x.text_rect)
                show_x.display()

            #update timers and associted messages
            if lesson_msg_timer and pygame.time.get_ticks() - lesson_msg_timer < 1000:
                pygame.draw.rect(screen, (255,255,255), collected_lesson_msg.text_rect)
                collected_lesson_msg.display()
            else:
                lesson_msg_timer = 0
            if unit_msg_timer and pygame.time.get_ticks() - unit_msg_timer < 10000:
                pygame.draw.rect(screen, (255,255,255), collected_unit_msg.text_rect)
                collected_unit_msg.display()
            else:
                unit_msg_timer = 0
            if continue_unit_timer and pygame.time.get_ticks() - continue_unit_timer < 10000:
                pygame.draw.rect(screen, (255,255,255), contiue_unit_msg.text_rect)
                contiue_unit_msg.display()
            else:
                continue_unit_timer = 0
            
            #displays the inventory
            inventory.display()
            #display the book icon
            screen.blit(book_icon, book_rect)

            #if the player collects a lesson, updates the lesson
            if player.collect_lesson:
                lesson+=1
                player.collect_lesson = False
                lesson_msg_timer = pygame.time.get_ticks()
            #if the player has touched a unit portal
            if player.collect_unit:
                #if they can access the unit portal
                if (unit+1) <= UNIT_MAX and lesson == current_lesson_max and player.exp >= UNIT_THRESHOLD:
                    unit +=1
                    current_lesson_max = assign_lesson_max(unit)
                    #updates stats
                    maximun_health = maximun_health*unit
                    player.updateStats("attack", 10)
                    player.updateStats("defense", 10)
                    #resets player health
                    player.health = maximun_health
                    #gives first lesson but resets experience
                    lesson = 1
                    player.exp = 0
                    #gets timer for unit message to display
                    unit_msg_timer = pygame.time.get_ticks()
                    #set to true to remove unit portal and update tilemap with world portal in world player class
                    player.update_unit = True
                    #set to false to indicate actions have been completed
                    player.collect_unit = False
                else:
                    if not unit_msg_timer:
                        #gets timer for message telling user what to do to continue
                        continue_unit_timer = pygame.time.get_ticks()

            if player.health == 0:
                status = "DEATH"

            #updates screen and framerate
            pygame.display.update()
            clock.tick(60)

    return status, bg_scroll, player, world_map, prev_maps, unit, lesson, maximun_health, current_lesson_max

#==NAVIGATE FUNCTION==
def play_data(save_num, saveFile=None):
    """
    Plays game.
    
    Args:
        save_num (int) : save file number
        saveFile (dict{dict}) : dictionary of save file information

    Returns:
        state (str)
    """
    #initalize state
    state = "GAMEPLAY"
    
    #checks if user has a savefile already
    if saveFile:
        #gets the culmative scroll background from previous save
        scroll_background = saveFile["scroll"]
        #initalizes world from previous save
        map = World(saveFile["world"]["subject"], saveFile["world"]["map"], saveFile["world"])
        previous_maps = saveFile["saved_maps"]
        #gets player dictionary
        playerDict = saveFile["player"]
        #re-initalize player
        player = Player(playerDict["image"],playerDict["username"],playerDict["health"],playerDict["position"],playerDict["attack"],playerDict["defense"],playerDict["experience"],playerDict["velocity"])
        #gets inventory dictionary
        pack = saveFile["inventory"]
        #re-initalize inventory
        player_inventory = Inventory("Backpack.png", pack["weapon"], pack["items"]["heal"], pack["items"]["skip"], pack["items"]["hint"], pack["coins"])
        #get farthest unit and lesson attained
        recent_unit = saveFile["unit"]
        recent_lesson = saveFile["lesson"]
        max_health = 40*recent_unit
        lesson_max = assign_lesson_max(recent_unit)
    #if the user is opening a savefile for the very first time
    else:
        #change state to send user to player set up
        state = "CHOOSE NAME"
        #gets username, design, and base weapon
        player_name, player_design, state, base_weapon = handle_set_up(state, SUBJECT)
        if state != "QUIT GAME":
            max_health = 40
            #initalizes player for first time
            player = Player(player_design,player_name, max_health, (300,HEIGHT), 7, 7, 0, 20)
            #creates world map starting from tilemap 1
            map = World(SUBJECT, 1)
            #initalize dictionary for unlocked maps
            previous_maps = {
                "amount" : 0
            }
            #initalize inventory
            player_inventory = Inventory("Backpack.png", base_weapon)
            #sets background scroll to 0
            scroll_background = 0
            #initalize unit and lesson
            recent_unit = 1
            recent_lesson = 0 # user must collect first lesson in-game
            lesson_max = U1_MAX #intialize current lesson max
            #auto saves the initial spawn
            save_game(player, map, player_inventory, save_num, previous_maps, scroll_background, recent_unit, recent_lesson)
            #change state to start game
            state = "GAMEPLAY"
    
    #initalize the previous state variable to aid in keeping background scroll consistent and functional for movement across tilemaps
    prev_state = "gameplay"

    #if the user doesn't quit the game
    while state != "QUIT GAME" and state != "RETURN TO MENU":
        #if the user is playing within the map
        if state == "GAMEPLAY":
            #sends user to main screen
            state, scroll_background, player, map, previous_maps, recent_unit, recent_lesson, max_health, lesson_max = main(map, scroll_background, player, player_inventory, previous_maps, recent_unit, recent_lesson, state, save_num, prev_state, max_health, lesson_max)
        #if the user is answering a question, sends to question screen
        elif state == "FIGHT":
            state, player, player_inventory = fight(state, player, player_inventory, save_num, SUBJECT, recent_unit, recent_lesson, max_health)
        #if the user has won their fight, sends to win screen
        elif state == "WON":
            state, player = won(state, player, player_inventory)
        #if the user gave up the fight, sends to give up screen
        elif state == "GAVE UP":
            state, player, player_inventory = give_up(state, player, player_inventory, recent_unit, recent_lesson)
        #if the user is trying to access the settings
        elif state == "SETTINGS":
            prev_state = "screen"
            state = setting(state, player, map, player_inventory, save_num, previous_maps, scroll_background, recent_unit, recent_lesson)
        #if the user died, displays the death screen
        elif state == "DEATH":
            state, player, player_inventory, scroll_background, map, previous_maps, prev_state = death_screen(state, save_num, player, player_inventory, recent_unit, recent_lesson, max_health, map.tile_map, prev_state)
        elif state == "SKIPPED":
            state, player = skipped_screen(state, player)
        #if the user is trying to access the books and banks
        elif state == "QUESTION MENU":
            prev_state = "screen"
            state = nav_question_menu(state, SUBJECT, save_num, recent_unit, recent_lesson, player.exp)

    return state