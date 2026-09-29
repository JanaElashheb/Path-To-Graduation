"""
Path to Graduation - WORLD AND PLAYER CLASSES
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Contains the world and player classes for the overall game. Associated classes such as enemy sprites, collectibles, and collision-tiles are also present.

History:
Jan 21, 2025: Date created
Mar 8, 2025: Added the enemies and the chest in the game map
Mar 9, 2025: Added collsions with the chest and enemies (opens up the question menu and deletes enemy)
May 4, 2025: Date completed
May 5, 2025: Added update_unit attribute to Player Class for unit requirement detection; moved UNIT_THRESHOLD individual gameplay files
"""

#===IMPORTS===
import pygame

#initalize pygame
pygame.init()
#initalize screen information
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
GRAVITY = 1
TILE_SIZE = 50
#player speed
SPEED = 5
#world scroll threshold
SCROLL = 300

#initalize screen (same as main) for display coherency
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#===CLASSES===

#===PLAYER CLASS===
class Player(pygame.sprite.Sprite):
    """
    This class represents a player.
    
    Reference: https://www.pygame.org/docs/ref/sprite.html#pygame.sprite.Sprite --> found from overall https://www.pygame.org/docs/index.html. Accessed: 2025/01/15
    
    Attributes:
        player_img (str) : name of player image
        username (str) : player username
        health (int) : default health value
        position (int, int) : position of player, from bottom left
        attack (int) : attack stat
        defense (int) : defense stat
        exp (int) : player experience (gained after each question)
        vel (int) : velocity
        jump (bool) : jump status
        enemy_collide (Sprite) : enemy player has collided with
        move_map (bool) : status if player is allowed to move up/down a tilemap
        collect_unit (bool) : status if player has collected a unit (aids in collision detection and notifying)
        collect_lesson (bool) : status if player has collected a lesson (aids in collision detection and notifying)
        update_unit (bool) : status is player can update their unit
    """
    
    def __init__(self, player_img, username, health, position, attack, defense, exp, velocity):
        """
        Initalizes the player.
        
        Args:
            player_img (str) : name of player image
            username (str) : player username
            health (int) : default health value
            position (int, int) : position of player, from bottom left
            attack (int) : attack stat
            defense (int) : defense stat
            exp (int) : player experience
            velocity (int) : positive height player can jump
        """
        #creates the player sprite
        pygame.sprite.Sprite.__init__(self)
        self.player_image = player_img
        #cretes the player sprite image
        self.load_image = pygame.image.load(self.player_image).convert_alpha()
        #scale image to tile size
        self.image = pygame.transform.scale(self.load_image, (TILE_SIZE, TILE_SIZE))
        #positions and gets the rect of the player
        self.rect = self.image.get_rect(bottomleft=(position[0], position[1]))
        
        #assigns player username
        self.user = username
        #assigns player health
        self.health = health
        
        #player stats and physics
        #assigns attack stat
        self.attack = attack
        #defense stat
        self.defense = defense
        #set player exp
        self.exp = exp
        #set value of velocity
        self.vel = 0
        #initalize to check if player is jumping
        self.jump = False
        #initalize velocity (positive)
        self.jump_height = velocity

        #initalize enemy collision
        self.enemy_collide = None
        #initalize ability to move tilemaps
        self.move_map = False

        #initalize unit and lesson collection (collision aid)
        self.collect_unit = False
        self.collect_lesson = False
        #initalize for if user has collected the unit
        self.update_unit = False
    
    def draw(self):
        """Draws player."""
        screen.blit(self.image, self.rect)
    
    def updateStats(self, stat, points):
        """
        Updates player stats.
        
        Args:
            stat (str) : type of stat
            points (int) : value to increase stat by
        """
        if stat.lower() == "attack":
            self.attack += points
        elif stat.lower() == "defense":
            self.defense += points

    def move(self, tilemap, tile_lst, scroll_bg, groups, player_inventory):
        """
        Updates player position.
        
        Args:
            tilemap (lst[lst]) : tilemap of world
            tile_lst (lst) : tile list of world for collision
            scroll_bg (int) : value of how much background has scrolled by
            groups ({dict[sprite]}) : dictionary of sprite groups player can collide with
        
        Returns:
            scroll_bg (int)
        """
        #references for jumping and collision: https://www.youtube.com/watch?v=WvcNfwIl2Jw. Accessed 2025/02/08
        #and: https://www.youtube.com/watch?v=s53T6eRdZpw&list=PLjcN1EyupaQlBSrfP4_9SdpJIcfnSJgzL&index=4. Accessed 2025/02/05
        #reference for world scrolling based on character position: https://www.youtube.com/watch?v=JTM8_pcQOUU. Accessed 2025/02/08
        
        #initalize variable for screen scrolling
        screen_scroll = 0
        #initalize variable for change in x,y position
        deltax = 0
        deltay = 0
        
        #gets dictionary of pressed keys
        press = pygame.key.get_pressed()
        #checks if user has clicked A
        if press[pygame.K_a]:
            #moves player to the left
            deltax += -SPEED
        #checks if user has clicked D
        if press[pygame.K_d]:
            #moves player right
            deltax += SPEED
        #if the player presses space and is not already jumping
        if press[pygame.K_SPACE] and not self.jump:
            #player jumps
            self.vel = -(self.jump_height)
            self.jump = True
            
        #constantly set gravity so player will always fall if not on a block
        self.vel += GRAVITY
        #always set velocity to 10
        if self.vel > 10:
            self.vel = 10
        #updates y value with velocity
        deltay+=self.vel
    
        for tile in tile_lst:
            #checks if player has collided with something in the y direction
            if tile[1].colliderect(self.rect.x, self.rect.y + deltay, self.rect.width, self.rect.height):
                #check if player is jumping
                if self.vel < 0:
                    #lets player fall onto tile
                    deltay = tile[1].bottom - self.rect.top
                elif self.vel > 0:
                    #allows player to stand on a block
                    deltay = tile[1].top - self.rect.bottom
                    #resets jump (on a block)
                    self.jump = False
            #checks if player has collided with something in the x direction
            if tile[1].colliderect(self.rect.x + deltax, self.rect.y, self.rect.width, self.rect.height):
                deltax = 0
        
        #check collisions for unique sprite groups      
        coin_col = pygame.sprite.spritecollideany(self, groups["coin"])
        enemy_col = pygame.sprite.spritecollideany(self, groups["enemy"])
        world_portal_col = pygame.sprite.spritecollideany(self, groups["portal"])
        health_col = pygame.sprite.spritecollideany(self, groups["health"])
        skip_col = pygame.sprite.spritecollideany(self, groups["skip"])
        hint_col = pygame.sprite.spritecollideany(self, groups["hint"])
        lesson_col = pygame.sprite.spritecollideany(self, groups["lesson"])
        wave_col = pygame.sprite.spritecollideany(self, groups["wave"])
        unit_col = pygame.sprite.spritecollideany(self, groups["unit portal"])

        #note: sprite positions in tilemap as (x,y) are (row, column)
        if coin_col:
            #initalize positions of coin in tilemap
            y = coin_col.column
            x = coin_col.row
            #removes from tilemap
            tilemap[x][y] = '0'
            #kills sprite
            coin_col.kill()
            player_inventory +=1
        elif enemy_col:
            #update enemy collision
            self.enemy_collide = enemy_col
        #if the player collides with a health potion
        elif health_col:
            #removes from tilemap
            tilemap[health_col.row][health_col.column] = '0'
            #kills sprite
            health_col.kill()
            player_inventory.updateItem("heal", 1)
        #if the player picks up a hint spell
        elif hint_col:
            #removes from tilemap
            tilemap[hint_col.row][hint_col.column] = '0'
            #kills sprite
            hint_col.kill()
            player_inventory.updateItem("hint", 1)
        #if the player picks up a skip stone
        elif skip_col:
            #removes from tilemap
            tilemap[skip_col.row][skip_col.column] = '0'
            #kills sprite
            skip_col.kill()
            player_inventory.updateItem("skip", 1)
        #if the player has collided with a lesson
        elif lesson_col:
            #updates the tilemap and kills the sprite
            tilemap[lesson_col.row][lesson_col.column] = '0'
            lesson_col.kill()
            #sets to true to indicate lesson collection
            self.collect_lesson = True
        elif wave_col:
            self.health = 0
        #if the player has collided with a world portal
        if world_portal_col:
            #set to true to indicate this
            self.move_map = True
        else:
            #otherwise false to indicate this
            self.move_map = False
        #if the player has collided with a unit portal; sets true/false to indicate this
        if unit_col:
            self.collect_unit = True
        else:
            self.collect_unit = False

        #if the player has updated their unit
        if self.update_unit:
            #removes unit portal from tilemap and replaces with a world portal
            tilemap[unit_col.row][unit_col.column] = '5'
            #kills sprite
            unit_col.kill()
            #update to end action
            self.update_unit = False
             
        #updates player position based on accepted change in (x,y) positions
        self.rect.x += deltax
        self.rect.y += deltay
        
        #keeps player within screen
        #stops player from exiting screen on left
        if self.rect.left < 0:
            self.rect.left = 0
        #keeps player from exiting screen on top
        if self.rect.top <= 0:
            self.rect.top = 0
        #keeps player from exiting screen on right
        if self.rect.right >= WIDTH:
            self.rect.right = WIDTH
            deltax = 0
        #keeps player on bottom of screen
        if self.rect.bottom >= HEIGHT:
            self.rect.bottom = HEIGHT
            deltay = 0
            #resets jump if player is on bottom of screen
            self.jump = False

        #scrolls background based off of player
        #checks if player hits the scroll threshold (SCROLL) and checks if they're at the edge of the map
        if (self.rect.right > WIDTH - SCROLL and scroll_bg < (len(tilemap[0]) * TILE_SIZE) - WIDTH) or (self.rect.left < SCROLL and  scroll_bg > abs(deltax)):
            #stops player from going forward if they've reached the scroll threshold (SCROLL)
            self.rect.x -= deltax
            #scrolls screen based on the deltax
            screen_scroll = -deltax
        
        return screen_scroll
    
    def __iadd__(self, plus_health):
        """
        Adds health.
        
        Args:
            plus_health (int)
        """
        if isinstance(plus_health, int):
            self.health += plus_health
            return self
        return NotImplemented
    
    def __isub__(self, sub_health):
        """
        Removes health.
        
        Args:
            sub_health (int)
        """
        if isinstance(sub_health, int):
            self.health -= sub_health
            return self
        return NotImplemented

    def get_dict(self):
        """Gets dictionary for saving."""
        player_dict = {
            "image" : self.player_image,
            "username" : self.user,
            "health" : self.health,
            "position" : (self.rect.x,self.rect.y),
            "attack" : self.attack,
            "defense" : self.defense,
            "experience" : self.exp,
            "velocity" : self.jump_height
            }
        
        return player_dict
        

#===WORLD CLASS===
class World():
    """
    Creates the world.

    Attributes:
        subject_tag (str) : subject name
        file (str) : tilemap file name
        map_number (int) : tilemap number
        tile_list (lst[lst]) : list of tiles
        saved_world (dict) : dictionary of previous world save
        prev_world (lst[lst]) : tilemap of previous world save
        coin_grp (Sprite Group) : sprite group for coins
        enemy_grp (Sprite Group) : sprite group for enemies
        chest_grp (Sprite Group) : sprite group for chests
        portal_grp (Sprite Group) : sprite group for portals
        health_grp (Sprite Group) : sprite group for potions
        hint_grp (Sprite Group) : sprite group for hint spells
        skip_grp (Sprite Group) : sprite group for skip stones
        lesson_grp (Sprite Group) : sprite group for lessons
        unit_grp (Sprite Group) : sprite group for unit portals
        wave_grp (Sprite Group) : sprite group for waves
        groups (dict) : dictionary of sprite groups
    """
    
    def __init__(self, subject_tag, map_number=1, saved_world=None, prev_world=None):
        """
        Initalizes an instance of a world.
        
        Args:
            subject_tag (str) : subject name
            map_number (int) : tilemap number
            saved_world (dict) : dictionary of previous world save
            prev_world (lst[lst]) : tilemap of previous world save
        """
        #initalize subject tag
        self.subject_tag = subject_tag
        #initalize file name
        self.file = "tilemaps\\" + subject_tag + "_tilemap_" + str(map_number) + ".txt"
        #initalize map number
        self.map_number = map_number

        #load images
        #load specific images for vectors
        if subject_tag == "vectors":
            dirt_img = pygame.image.load("assets\dirt.png").convert_alpha()
            grass_img = pygame.image.load("assets\grass.png").convert_alpha()
            #initalize enemy file name for images, and also for enemy sprite creation
            e1_filename = "enemies\Buff Pig.png"
            e2_filename = "enemies\Little Demon.png"
            e3_filename = "enemies\Edward.png"
        #load specific images for data management
        elif subject_tag == "data":
            gravel_img = pygame.image.load("assets\gravel.png").convert_alpha()
            #initalize enemy file name for images, and also for enemy sprite creation
            e1_filename = "enemies\Alien Slime.png"
            e2_filename = "enemies\Mad Crab.png"
            e3_filename = "enemies\Seeing Eye.png"

        #loads enemies
        e1_img = pygame.image.load(e1_filename).convert_alpha()
        e2_img = pygame.image.load(e2_filename).convert_alpha()
        e3_img = pygame.image.load(e3_filename).convert_alpha()
        #loads general images
        coin_img = pygame.image.load("assets\coin.png").convert_alpha()
        wave_img = pygame.image.load("assets\wave.png").convert_alpha()
        water_img = pygame.image.load("assets\water.png").convert_alpha()
        chest_img = pygame.image.load("assets\Closed chest.png").convert_alpha()
        portal_img = pygame.image.load("assets\portal.png").convert_alpha()
        health_img = pygame.image.load("assets\healing potion.png").convert_alpha()
        spell_img = pygame.image.load("assets\hint spell.png").convert_alpha()
        stone_img = pygame.image.load("assets\skip stone.png").convert_alpha()
        lesson_img = pygame.image.load("assets\lesson icon.png").convert_alpha()
        unit_img = pygame.image.load("assets\Green Portal.png").convert_alpha()

        #create a list of tiles
        #checks if this is a completely new world
        if not saved_world and not prev_world:
            self.tile_map = self.readTilemap(self.file)
        else:
            #if it's the current world the player is on, gets that
            if prev_world:
                self.tile_map = prev_world
            #otherwise gets the tilemap from the saved worlds
            else:
                if isinstance(saved_world, list):
                    self.tile_map = saved_world
                else:
                    self.tile_map = saved_world["tilemap"]
        
        #create a list to add tiles to
        self.tile_list = []
    
        #initalize sprite groups
        #initalize coin group
        self.coin_grp = pygame.sprite.Group()
        #initalize enemy groups
        self.enemy_grp = pygame.sprite.Group()
        #initalize chest groups
        self.chest_grp = pygame.sprite.Group()
        #initalize portal group for world  (tilemap) movement
        self.portal_grp = pygame.sprite.Group()
        #initalize health potion group
        self.health_grp = pygame.sprite.Group()
        #initalize hint spell group
        self.hint_grp = pygame.sprite.Group()
        #initalize skip stone group
        self.skip_grp = pygame.sprite.Group()
        #initalize lesson group
        self.lesson_grp = pygame.sprite.Group()
        #initalize portal for units group
        self.unit_grp = pygame.sprite.Group()
        #initalize wave group
        self.wave_grp = pygame.sprite.Group()

        #checks if the tilemap isn't from a previous accessed save
        if not saved_world and not prev_world:
            #initalize a list for a single row of 0s
            single_row = []
            #for the number of columns in a single row of the map, add 0s
            for col in range(0, len(self.tile_map[0])):
                single_row.append('0')
            
            #get the initial number of rows within a map
            initial_rows = len(self.tile_map)

            #gets the full number of rows possible on the screen from the tile size
            full_rows = HEIGHT//TILE_SIZE
            if HEIGHT%TILE_SIZE !=0:
                full_rows +=1
            #updates rows
            for row in range(0, (full_rows - initial_rows)):
                self.tile_map.insert(0, single_row)
        
        #initalize row count
        row_count = 0
        for row in self.tile_map:
            #initalize column count
            col_count = 0
            for tile in row:
                #checks if the tile is DIRT
                if tile == "1" and subject_tag == "vectors":
                    #scales the image to the appropriate size
                    dirt_image = pygame.transform.scale(dirt_img, (TILE_SIZE, TILE_SIZE))
                    #gets rectangle of image
                    dirt_rect = dirt_image.get_rect()
                    #sets x and y values to proper coordinates
                    dirt_rect.x = col_count * TILE_SIZE
                    dirt_rect.y = row_count * TILE_SIZE
                    #creates a tile
                    dirt_tile = (dirt_image, dirt_rect)
                    #append to big tile list
                    self.tile_list.append(dirt_tile)
                #checks if the tile is GRASS
                elif tile == "2" and subject_tag == "vectors":
                    grass_image = pygame.transform.scale(grass_img, (TILE_SIZE, TILE_SIZE))
                    grass_rect = grass_image.get_rect()
                    grass_rect.x = col_count * TILE_SIZE
                    grass_rect.y = row_count * TILE_SIZE
                    grass_tile = (grass_image, grass_rect)
                    self.tile_list.append(grass_tile)
                #checks if the tile is a WAVE
                elif tile == "3":
                    wave = Wave(wave_img, col_count, row_count)
                    self.wave_grp.add(wave)
                #checks if the tile is WATER
                elif tile == "4":
                    water_image = pygame.transform.scale(water_img, (TILE_SIZE, TILE_SIZE))
                    water_rect = water_image.get_rect()
                    water_rect.x = col_count * TILE_SIZE
                    water_rect.y = row_count * TILE_SIZE
                    water_tile = (water_image, water_rect)
                    self.tile_list.append(water_tile)
                #checks if the tile is a WORLD PORTAL (PURPLE PORTAL)
                elif tile == "5":
                    portal = Portal(portal_img, col_count, row_count)
                    self.portal_grp.add(portal)
                #checks if the tile is GRAVEL
                elif tile == "6"  and subject_tag == "data":
                    gravel_image = pygame.transform.scale(gravel_img, (TILE_SIZE, TILE_SIZE))
                    gravel_rect = gravel_image.get_rect()
                    gravel_rect.x = col_count * TILE_SIZE
                    gravel_rect.y = row_count * TILE_SIZE
                    gravel_tile = (gravel_image, gravel_rect)
                    self.tile_list.append(gravel_tile)
                #checks if the tile is UNIT PORTAL (GREEN PORTAL)
                elif tile == "7":
                    unit_portal = UnitPortal(unit_img, col_count, row_count)
                    self.unit_grp.add(unit_portal)
                #checks if the tile is a COIN
                elif tile == "c":
                    #creates a sprite for the coins
                    coin = Coin(coin_img, col_count, row_count)
                    #adds to coin group
                    self.coin_grp.add(coin)
                #checks if the tile is an EASY ENEMY
                elif tile == "e":
                    enemy = Enemy(e1_filename, e1_img, col_count, row_count)
                    self.enemy_grp.add(enemy)
                #checks if the tile is an MEDIUM LEVEL ENEMY
                elif tile == "m":
                    enemy = Enemy(e2_filename, e2_img, col_count, row_count)
                    self.enemy_grp.add(enemy)
                #checks if the tile is a HARD ENEMY
                elif tile == "d":
                    enemy = Enemy(e3_filename, e3_img, col_count, row_count)
                    self.enemy_grp.add(enemy)
                #checks if the tile is a CHEST
                elif tile == "C":
                    chest = Chest(chest_img, col_count, row_count)
                    self.chest_grp.add(chest)
                #checks if the tile is a HEALTH POTION
                elif tile == "p":
                    health_potion = HPotion(health_img, col_count, row_count)
                    self.health_grp.add(health_potion)
                elif tile == "h":
                    hint_spell = Hint(spell_img, col_count, row_count)
                    self.hint_grp.add(hint_spell)
                elif tile == "s":
                    skip_stone = Hint(stone_img, col_count, row_count)
                    self.skip_grp.add(skip_stone)
                #check if the tile is a LESSON ICON
                elif tile == "l":
                    lesson = Lesson(lesson_img, col_count, row_count)
                    self.lesson_grp.add(lesson)

                #update column count for positioning
                col_count +=1
            #update row count for positioning
            row_count +=1
        
        #create dictionary for sprite groups for collisions
        self.groups = {
            "coin" : self.coin_grp,
            "enemy": self.enemy_grp,
            "chest": self.chest_grp,
            "portal" : self.portal_grp,
            "health" : self.health_grp,
            "hint" : self.hint_grp,
            "skip" : self.skip_grp,
            "lesson" : self.lesson_grp,
            "unit portal" : self.unit_grp,
            "wave" : self.wave_grp
            }
    
    @staticmethod
    def readTilemap(fileName):
        """
        Reads tilemap and converts into a list.
        
        Args:
            fileName (str) : name of tilemap file
            
        Returns:
            lst_of_tiles (lst) : list of world tiles
        """
        #opens file with tilemap
        infile = open(fileName, "r")
        
        #create new list to store tiles
        lst_of_tiles = []
        
        #loops through line in map file
        for lines in infile.readlines():
            #initalize list for every row of tiles
            new_line = []
            #loops through the columns of the row
            for data in lines:
                #checks to make sure the column is not a comma, space, or newline
                if data not in [" ",",","\n"]:
                    #adds number or letter tile to new_line
                    new_line.append(data)
            #adds tile row to tile list
            lst_of_tiles.append(new_line)
        
        #closes file
        infile.close()
        
        return lst_of_tiles
    
    def draw_tile(self, tiles, screen_scroll):
        """
        Draws tilemap.
        
        Args:
            tiles (lst[lst]) : list of tiles
        """
        #loops through tile list
        for tile in tiles:
            #offset x value of rectangle of tiles based on player position
            tile[1].x += screen_scroll
            #displays tile
            screen.blit(tile[0], tile[1])
        
        #offsets x values of rectangles in groups
        for groups, sprites in self.groups.items():
            for items in sprites:
                items.rect.x += screen_scroll
            #draws groups
            sprites.draw(screen)
    
    def get_dict(self):
        """
        Gets a dictionary of the world for saving purposes.

        Returns:
            dictionary (dict)
        """
        dictionary = {
            "subject" : self.subject_tag,
            "tilemap" : self.tile_map,
            "map" : self.map_number
            }
        
        return dictionary

#===CLASSES FOR GROUND TILES THAT KILL PLAYER===
class Wave(pygame.sprite.Sprite):
    """
    Creates a Wave.
    
    Attributes:
        image (Surface) : image of wave
        rect (Rect) : rect of wave
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """
    
    def __init__(self, img, column, row):
        """
        Initalizes a wave.
        
        Args:
            img (str) : image of a wave
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position wave on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

#===CLASSES FOR COLLECTIBLE ITEMS===

class Coin(pygame.sprite.Sprite):
    """
    Creates a coin.
    
    Attributes:
        image (Surface) : image of coin
        rect (Rect) : rect of coin
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """
    
    def __init__(self, img, column, row):
        """
        Initalizes a coin.
        
        Args:
            img (str) : image of a coin
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position coin on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)
                
class Chest(pygame.sprite.Sprite):
    """
    Creates a chest.
    
    Attributes:
        image (Surface) : image of chest
        rect (Rect) : rect of chest
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """
    
    def __init__(self, img, column, row):
        """
        Initalizes a chest.
        
        Args:
            img (str) : image of a chest
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position chest on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

class Portal(pygame.sprite.Sprite):
    """
    Creates a world portal.

    Attributes:
        image (Surface) : image of world portal
        rect (Rect) : rect of world portal
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """

    def __init__(self, img, column, row):
        """
        Initalizes a portal.
        
        Args:
            img (str) : image of a chest
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position portal on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

class HPotion(pygame.sprite.Sprite):
    """
    Creates a health potion.

    Attributes:
        image (Surface) : image of health potion
        rect (Rect) : rect of potion
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """

    def __init__(self, img, column, row):
        """
        Initalizes a health potion.
        
        Args:
            img (str) : image of the health potion
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position health potion on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

class Hint(pygame.sprite.Sprite):
    """
    Creates a health potion.

    Attributes:
        image (Surface) : image of hint spell
        rect (Rect) : rect of hint spell
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """

    def __init__(self, img, column, row):
        """
        Initalizes a hint spell.
        
        Args:
            img (str) : image of the hint spell.
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position hint spell on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

class Skip(pygame.sprite.Sprite):
    """
    Creates a skip stone.

    Attributes:
        image (Surface) : image of stone
        rect (Rect) : rect of skip stone
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """

    def __init__(self, img, column, row):
        """
        Initalizes a skip stone.
        
        Args:
            img (str) : image of the skip stone
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position skip stone on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

class Lesson(pygame.sprite.Sprite):
    """
    Creates a lesson icon to collect.

    Attributes:
        image (Surface) : image of lesson 
        rect (Rect) : rect of lesson
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """

    def __init__(self, img, column, row):
        """
        Initalizes a collectible lesson.
        
        Args:
            img (str) : image of the lesson icon
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position lesson icon on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

class UnitPortal(pygame.sprite.Sprite):
    """
    Creates a unit portal to collect.

    Attributes:
        image (Surface) : image of unit portal
        rect (Rect) : rect of unit portal
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
    """

    def __init__(self, img, column, row):
        """
        Initalizes a unit portal (level up).
        
        Args:
            img (str) : image of the green portal
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.column = column
        self.row = row
        self.rect = self.image.get_rect()
        #position dirt on appropiate tile
        self.rect.x = column * TILE_SIZE
        self.rect.y = row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)

#===ENEMY CLASS===
class Enemy(pygame.sprite.Sprite):
    """
    Creates an enemy.
    
    Attributes:
        image (Surface) : image of enemy
        rect (Rect) : rect of enemy
        column (int) : tilemap column
        row (int) : tilemap row
        tile (Surface, Rect) : associated tile
        name (str) : enemy name
        health (int) : enemy health
        max_attack (int) : enemy's max attack threshold
        min_attack (int) : enemy's min attack threshold
        difficulty (str) : enemy difficulty
    """
    
    def __init__(self, file_name, img, column, row):
        """
        Initalizes an enemy.
        
        Args:
            file_name (str) : file name of enemy
            img (Surface) : image of an enemy
            column (int)
            row (int)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.column = column
        self.row = row
        #position dirt on appropiate tile
        self.rect.x = self.column * TILE_SIZE
        self.rect.y = self.row * TILE_SIZE
        #create tile
        self.tile = (self.image, self.rect)
        
        image_name = file_name[0:len(file_name)-4]
        self.name = image_name[len("enemies/"):len(image_name)]

        #if the enemy is buff pig
        if self.name == "Buff Pig" or self.name == "Alien Slime":
            #assigns health
            self.health = 20
            #assigns initial max and minimun attack threshold
            self.max_attack = 15
            self.min_attack = 2
            self.difficulty = "easy"
        elif self.name == "Little Demon" or self.name == "Mad Crab":
            self.health = 30
            self.max_attack = 15
            self.min_attack = 9
            self.difficulty = "medium"
        elif self.name == "Edward" or self.name == "Seeing Eye":
            self.health = 40
            self.max_attack = 30
            self.min_attack = 10
            self.difficulty = "hard"