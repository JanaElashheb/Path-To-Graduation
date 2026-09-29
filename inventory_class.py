"""
Path to Graduation - INVENTORY CLASS
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Contains the inventory class for the user.

History:
Mar 18, 2025: Date created
May 4, 2025: Date completed
"""

#===IMPORTS===
import pygame
from clickableClass import Text

#initalizes pygame
pygame.init()
#initalize screen information for display size
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
#tile size of world
TILE_SIZE = 50

#initalize screen (same as main)
screen = pygame.display.set_mode((WIDTH,HEIGHT))

class Inventory():
    """
    Creates the player inventory.
    
    Attributes:
        weapon_stats (lst[lst]) : list of weapons and their respective stats [name, attack, defense]
        image (Surface) : backpack inage
        rect (Rect) : rect of image
        weapon (str) : name of weapon
        attack (int) : attack stat of weapon
        defense (int) : defense stat of weapon
        heal (int) : amount of heal potions
        skip (int) : amount of skip stones
        hint (int) : amount of hint spells
    """
    
    weapons_stats = [["basic axe",10,1],["basic sword",8,3],["basic wand",5,2]]
    
    def __init__(self, inventory_image, weapon=None, heal=0, skip=0, hint=0, coins=0):
        """
        Creates an instance of an inventory.
        
        Args:
            inventory_image (str) : backpack inage
            weapon (str) : name of weapon
            attack (int) : attack stat of weapon
            defense (int) : defense stat of weapon
            heal (int) : amount of heal potions
            skip (int) : amount of skip stones
            hint (int) : amount of hint spells
            wpn_img (Surface) : image of weapon
            coin_img (Surface) : image of coin
            heal_img (Surface) : image of health potion
            hint_img (Surface) : image of hint spell
            skip_img (Surface) : image of skip stone
        """
        #loads inventory image
        load_image = pygame.image.load("assets/" + inventory_image).convert_alpha()
        #scales to tilesize
        self.image = pygame.transform.scale(load_image, (TILE_SIZE, TILE_SIZE))
        #positions at top of screen
        self.rect = self.image.get_rect(center = (30,30))
        
        #initalize weapon
        self.weapon = weapon
        
        #checks if the user already has a weapon and assigns their stats
        if self.weapon:
            for row in self.weapons_stats:
                if row[0] == self.weapon:
                    self.attack = row[1]
                    self.defense = row[2]
        else:
            #otherwise defaults stats to 0
            self.attack = 0
            self.defense = 0
        
        #initalize number of heal potions
        self.heal = heal
        #intialize number of skip stones
        self.skip = skip
        #initalize number of hint spells
        self.hint = hint
        #initalize number of coins collected
        self.coins = coins

        self.wpn_img = self.load_image(self.weapon)
        self.coin_img = self.load_image("coin")
        self.heal_img = self.load_image("healing potion")
        self.hint_img = self.load_image("hint spell")
        self.skip_img = self.load_image("skip stone")

    @property
    def coins(self):
        """Returns value of coins (int)."""
        return self._coins
    
    @coins.setter
    def coins(self, new_value):
        """
        Sets the value of the coins.

        Args:
            new_value (int) : new coin value
        """
        #checks if the value is less than 0, then sets it to exactly 0
        if new_value < 0:
            self._coins = 0
        #otherwise accepts new value as coin value
        else:
            self._coins = new_value

    def get_dict(self):
        """Creates and returns a dictionary of the inventory."""
        inventory_dict = {
            "weapon" : self.weapon,
            "items": {
                "heal": self.heal,
                "skip": self.skip,
                "hint": self.hint
                },
            "coins": self.coins
            }
        
        return inventory_dict

    @staticmethod
    def load_image(name):
        """
        Load items for display.

        Args:
            name (str) : name of item

        Returns:
            image (Surface) : adjusted image of item
            rect (Rect) : rect of image
        """
        load = pygame.image.load("assets/"+name+".png").convert_alpha()
        image = pygame.transform.scale(load, (TILE_SIZE, TILE_SIZE))
        rect = image.get_rect()

        return (image, rect)

    def updateWeapon(self, new_weapon):
        """
        Updates weapon acquisition.
        
        Args:
            new_weapon (str) : new weapon picked up
        """
        #updates stats based on weapons
        for weapons in self.weapons_stats:
            if weapons[0] == new_weapon:
                self.attack = weapons[1]
                self.defense = weapons[2]
        #updates weapon
        self.weapon = new_weapon
    
    def display(self):
        """Displays inventory."""
        screen.blit(self.image, self.rect)
    
    def __iadd__(self, profit):
        """
        Adds coins
        
        Args:
            profit (int) : coins added
        """
        if isinstance(profit, int):
            self.coins += profit
            return self
        return NotImplemented
        
    def __isub__(self, loss):
        """
        Adds coins

        Args:
            loss (int) : coins lost
        """
        if isinstance(loss, int):
            self.coins -= loss
            return self
        return NotImplemented

    def check_contain(self):
        """
        Checks if the inventory contains at least one of the items.

        Returns:
            has_list (lst) : list of items the inventory contains
        """
        #initalize list of items the inventory has
        has_list = []
        #if the item exists, adds the item to the has list 
        if self.heal > 0:
            has_list.append("heal")
        if self.skip > 0:
            has_list.append("skip")
        if self.hint > 0:
            has_list.append("hint")
        if self.coins > 0:
            has_list.append("coin")

        return has_list

    def updateItem(self, tag, amount):
        """
        Updates items.
        
        Args:
            tag (str) : type of item collected
            amount (int) : amount of item collected ((+)/(-))
        """
        #adds or subs from the heal potion
        if tag == "heal":
            self.heal += amount
            #ensures the amount never goes under 0
            if self.heal < 0:
                self.heal = 0
        #adds or subs from the skip potion
        elif tag == "skip":
            self.skip += amount
            #ensures the amount never goes under 0
            if self.skip < 0:
                self.skip = 0
        #adds or subs from the hint potion
        elif tag == "hint":
            self.hint += amount
            #ensures the amount never goes under 0
            if self.hint < 0:
                self.hint = 0
    
    def consume_health(self, player_health, level, maximun_health_value):
        """
        Consumes a health potion.
        
        Args:
            player_health (int) : current player health
            level (int) : level user has accessed
            maximun_health_value (int) : maximun health of player
        
        Returns:
            player_health (int) : health regained
        """
        if self.heal > 0:
            self.heal -= 1
            player_health += 15*level
            if player_health > maximun_health_value:
                player_health = maximun_health_value
                
        return player_health

    def toggle(self, mouse_pos):
        """
        Toggles the inventory hotbar if applicable.

        Args:
            mouse_pos ((x, y)) : player mouse position
        """

        latest_rect = self.rect
        
        #checks if the user has a weapon
        if self.weapon:
            #sets it to the left of the most previous item
            self.wpn_img[1].left = latest_rect.right
            #updates it to be the most previous item displayed
            latest_rect = self.wpn_img[1]
            #displays item
            screen.blit(self.wpn_img[0], self.wpn_img[1])
            #displays brief item information if user hovers over it
            self.hover_inventory(self.wpn_img[1], mouse_pos, self.weapon.upper())
        
        #checks if user has a coin
        if self.coins > 0:
            #sets it to the left of the most previous item
            self.coin_img[1].left = latest_rect.right
            #updates it to be the most previous item displayed
            latest_rect =  self.coin_img[1]
            #displays item
            screen.blit(self.coin_img[0], self.coin_img[1])
            #displays brief item information if user hovers over it
            self.hover_inventory(self.coin_img[1], mouse_pos, "Coins", self.coins)

        #checks if user has any health potions
        if self.heal > 0:
            #sets it to the left of the most previous item
            self.heal_img[1].left = latest_rect.right
            #updates it to be the most previous item displayed
            latest_rect = self.heal_img[1]
            #displays item
            screen.blit(self.heal_img[0], self.heal_img[1])
            #displays brief item information if user hovers over it
            self.hover_inventory(self.heal_img[1], mouse_pos, "Healing Potion", self.heal)
        
        #checks if user has any skip stones
        if self.skip > 0:
            #sets it to the left of the most previous item
            self.skip_img[1].left = latest_rect.right
            #updates it to be the most previous item displayed
            latest_rect = self.skip_img[1]
            #displays item
            screen.blit(self.skip_img[0], self.skip_img[1])
            #displays brief item information if user hovers over it
            self.hover_inventory(self.skip_img[1], mouse_pos, "Skip Stone", self.skip)

        #checks if user has any hint spells
        if self.hint > 0:
            #sets it to the left of the most previous item
            self.hint_img[1].left = latest_rect.right
            #updates it to be the most previous item displayed
            latest_rect = self.hint_img[1]
            #displays item
            screen.blit(self.hint_img[0], self.hint_img[1])
            #displays brief item information if user hovers over it
            self.hover_inventory(self.hint_img[1], mouse_pos, "Hint Spell", self.hint)
    
    def hover_inventory(self, rect, pos, name, number=1):
        """
        Displays the name of the item, if the user is hovering over it.

        Args:
            rect (pygame.Rect) : rect of item
            pos ((x, y)) : player mouse position
            name (str) : name of item
            number (int) : amount of item held
        """
        if rect.collidepoint(pos):
            #checks if the item is a weapon
            if name not in ["Healing Potion", "Skip Stone", "Hint Spell", "Coins"]:
                text = f"{name}; Attack; {self.attack}; Defense: {self.defense}"
            else:
                #if the item isn't a weapon, creates a 
                text = f"{name}: {number}"
            info = Text(text, "inkfree", 20, (255,255,255), (0,0))
            info.text_rect.left = rect.left
            info.text_rect.top = rect.bottom
            pygame.draw.rect(screen, (12, 13, 13), info.text_rect)
            info.display()
    
    def check_clicks(self, mouse_pos, player, player_level, maximum_health_val, battle=False):
        """
        Checks and reacts correspondingly if the inventory is being clicked.

        Args:
            mouse_pos ((int, int)) : (x, y) mouse position
            player (Player)
            player_level (int) : current unit player is on
            maximun_health (int) : maximum health for player
            battle (bool) : if the player is in a fight or not

        Returns:
            action (str) : what the user has done; primarily relevant for fighting
        """
        #initalize action message
        action = "none"

        #if the player has a health potion
        if self.heal > 0:
            #cehcks if they have clicked the item
            if self.heal_img[1].collidepoint(mouse_pos):
                #consumes a potion and updates the action message
                player.health = self.consume_health(player.health, player_level, maximum_health_val)
                action = "used heal"
        
        #if the user has a hint spell and they are fighting
        if self.hint > 0 and battle:
            #checks if they have clicked the item
            if self.hint_img[1].collidepoint(mouse_pos):
                #removes a hint and updates message
                self.updateItem("hint", (-1))
                action = "used hint"

        if self.skip > 0 and battle:
            #cehcks if they have clicked the item
            if self.skip_img[1].collidepoint(mouse_pos):
                #removes a skip and updates message
                self.updateItem("skip", (-1))
                action = "used skip"

        return action

