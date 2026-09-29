"""
Path to Graduation - CLICKABLE CLASSES
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Contains interactible classes for navigation, functionality, and display of game, such as Buttons and Text.

History:
Jan 21, 2025: Date created
Jan 23, 2025: Created the Text class
Feb 5, 2025: Added the write method the the Text class
May 2, 2025: Date completed
"""

#===IMPORTS===
import pygame
pygame.init()
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
TILE_SIZE = 50

#initalize screen (same as main)
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#===CLASSES===
class Button():
    """
    Creates a button.

    Attributes:
        text (str) : content of button
        font (str) : text font (system fonts)
        size (int) : size of text
        f_colour ((int, int, int)) : RGB colour of font
        display_text (Surface) : rendering of text
        text_rect (Rect) : text rect
        b_colour ((int, int, int)) : RGB colour of background rect
        padding ((int, int)) : inflate button rect
        rounding (int) : default 0; rounds corners
        border (int) : default 0; if > 0 then outlines button, rather than filled
        current_col ((int, int, int)) : RGB value of current background colour
        back (Rect) : background rect for display
    """
    
    def __init__(self, text, font, size, f_colour, position, b_colour, padding, rounding, border=0):
        """
        Initalizes a button.
        
        Args:
            text (str) : content of button
            font (str) : text font (system fonts)
            size (int) : size of text
            f_colour ((int, int, int)) : RGB colour of font
            pos ((int, int)) : (x, y) position of button (centered)
            b_colour ((int, int, int)) : RGB colour of background rect
            padding ((int, int)) : inflate button rect
            rounding (int) : default 0; rounds corners
            border (int) : default 0; if > 0 then outlines button, rather than filled
        """
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.f_colour = f_colour
        
        #renders the text on the button
        self.display_text = self.font.render(self.text, True, self.f_colour)
        
        #gets the rect of the button
        self.text_rect = self.display_text.get_rect()
        #positions the rectangle using the center point
        self.text_rect.center = position[0], position[1]
        
        self.b_colour = b_colour
        self.padding = padding
        self.border = border
        self.rounding = rounding
        self.current_col = self.b_colour
        #draws the back rectangle for background colour and hovering
        self.back = pygame.draw.rect(screen, self.b_colour, self.text_rect.inflate(self.padding), self.border, self.rounding)
        
    def display(self):
        """Displays button."""
        self.back = pygame.draw.rect(screen, self.current_col, self.text_rect.inflate(self.padding), self.border, self.rounding)
        screen.blit(self.display_text, self.text_rect)
        
    def hover(self, hover_col, mouse_pos):
        """
        When user hovers over button, changes colour.
        
        Args:
            hover_col ((int, int, int)) : hover colour of button
            mouse_pos ((int, int)) : current (x, y) position of cursor 
        """
        #if mouse is hovering on button
        if self.back.collidepoint(mouse_pos):
            #changes current colour to indicate button
            self.current_col = hover_col
        else:
            #otherwise changes back to normal colour
            self.current_col = self.b_colour
            
class Text():
    """
    Creates a button.

    Attributes:
        text (str) : content of text
        font (str) : text font (system fonts)
        f_colour ((int, int, int)) : RGB colour of font
        x (int) : x position of text
        y (int) : y position of text
        display_text (Surface) : rendered text
        text_rect (Rect) : text rect
    """
    
    def __init__(self, text, font, size, f_colour, position):
        """
        Initalizes a button.
        
        Args:
            text (str) : content of text
            font (str) : text font (system fonts)
            size (int) : size of text
            f_colour ((int, int, int)) : RGB colour of font
            pos ((int, int)) : (x, y) position of button (centered)

        """
        self.font = pygame.font.SysFont(font, size)
        self.text = text
        self.f_colour = f_colour
        
        #gets position of text
        self.x = position[0]
        self.y = position[1]

        #renders the text on the button
        self.display_text = self.font.render(self.text, True, self.f_colour)
        
        #gets the rect of the button
        self.text_rect = self.display_text.get_rect()
        #positions the rectangle using the center point
        self.text_rect.center = self.x, self.y
        
    def display(self):
        """Displays button."""
        screen.blit(self.display_text, self.text_rect)
    
    def write(self, event, ans_limit=None):
        #REFERENCE: https://www.youtube.com/watch?v=Rvcyf4HsWiw
        """
        Handles user typing input
        
        Args:
            event (pygame.Event) : Pygame event for keyboard input
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]  # Remove last character
            else:
                if ans_limit:
                    if len(self.text+event.unicode) < ans_limit+1:
                        self.text += event.unicode  # Add typed character
                else:
                    self.text+=event.unicode
                
            # Re-render the text to update it on screen
            self.display_text = self.font.render(self.text, True, self.f_colour)
            #gets the rect of the button
            self.text_rect = self.display_text.get_rect()
            #positions the rectangle using the center point
            self.text_rect.center = self.x, self.y
    
    def text_value(self):
        """
        Assingns the text proportion an actual value.

        Returns:
            value (str)
        """
        value = self.text

        return value

    def erase(self):
        """Erases text."""
        #erases text 
        self.text = ""
        #re-render text for display
        self.display_text = self.font.render(self.text, True, self.f_colour)

class Close():
    """
    Creates a close button.

    Attributes:
        close (Surface) : image of close button
        rect (Rect) : rect of close button
    """

    def __init__(self):
        """Initalizes a close button."""
        #Creating button for exiting game
        close = pygame.image.load("assets\Close Button.png").convert_alpha()
        #changes the size of the image
        self.close = pygame.transform.scale(close, (TILE_SIZE, TILE_SIZE))
        #creates a rectangle for the image
        self.rect = self.close.get_rect(center = (WIDTH - 40, HEIGHT - HEIGHT + 20))
    
    def display(self):
        """Displays the close button."""
        screen.blit(self.close, self.rect)

class Setting():
    """
    Creates a setting icon.

    Attributes:
        gear (Surface) : image of setting gear
        rect (Rect) : rect of setting gear
    """

    def __init__(self):
        """Initalizes a setting icon."""
        #loads and scales image of setting gear
        setting_img = pygame.image.load("assets\setting gear.png").convert_alpha()
        self.gear = pygame.transform.scale(setting_img, (TILE_SIZE, TILE_SIZE))
        #gets rect of image
        self.rect = self.gear.get_rect(center = (WIDTH-40, HEIGHT-HEIGHT+40))
    
    def display(self):
        """Displays the setting icon button."""
        screen.blit(self.gear, self.rect)