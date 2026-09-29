"""
Path to Graduation - QUESTION INTERACTIONS
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Allows user to navigate previously completed/uncompleted questions, and look through collected lessons per unit.

History:
Apr 4, 2025: Date created
May 4, 2025: Date completed
"""

#===IMPORTS===
import pygame
from clickableClass import Text, Button
from file_handling import update_whole, update_book, retrieve_lesson, retrieve_questions

#initalizations
#initialize pygame
pygame.init()
#initalize screen information for display size
screen_info = pygame.display.Info()

#===CONSTANTS===
WIDTH = screen_info.current_w
HEIGHT = screen_info.current_h
TILE_SIZE = 50
#max exp required to continue to next unit
UNIT_THRESHOLD = 100

#===GAME VARIABLES===
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

#=====FUNCTIONS=====

#===FORMAT AND DISPLAY (BOOK/BANK SPECIFIC)===
def format_single(single_question, recent_rect=None, text_size=30, position="under", threshold=0):
    """
    Formats question for display.
    
    Args:
        single_question (str) : question
        recent_rect (Rect) : rect for initial positioning, but optional (default sets position at half the height)
        position (str) : position over or under rect; default 'under'
        threshold (int) : positioning threshold to be above a certain object; default 0
        
    Returns:
        formatted (lst) : list of question rects to display
    """

    #converts the string into a list to display 
    if "(n)" in single_question:
        single_question = single_question.split("(n)") 
    else:
        single_question = [single_question]

    #initalize list for final format
    formatted = []
    for line in single_question:
        #checks if the recent rect already exists/has already existed
        if recent_rect and position == "under" or position == "over initial":
            #sets the text to a little under the previous
            height = recent_rect.bottom+recent_rect.height
        elif recent_rect and position == "over":
            height = (recent_rect.top-threshold)+(recent_rect.height-threshold)
            position = "over initial"
        else:
            #if this is the first line, then sets iniital height
            height = HEIGHT//2-100
        #creates new line
        n_line = Text(line, "cambriamath", text_size, (0,0,0), (WIDTH//2, height))
        #adds to final list
        formatted.append(n_line)
        #updates latest rect
        recent_rect = n_line.text_rect
        
    return formatted

def question_format_display(lst):
    """
    Displays the questions for selection on the question book and challenge bank.
    
    Args:
        lst (lst[lst]) : question list
    
    Returns:
        display_lst (lst[lst]) : big list of questions in groups to display
    """
    #initalize initial height
    height = HEIGHT*(1/16)
    #creates the big display list
    display_lst = []
    #creates a new group
    group = []
    #initalize question count
    question_count = 1
    for i in lst:
        #if the height is greater than the maximun height permissible
        if height > HEIGHT-90:
            #adds the group to the big group
            display_lst.append(group)
            #re-sets the height
            height = HEIGHT*(1/16)
            #re-sets the group
            group = []
        #if there are more than one line in the question
        if "(n)" in i[0]:
            #split up and only display the first line
            get_text = i[0].split("(n)")
            text = get_text[0] + "..."
        else:
            #otherwise display the entire question
            text = i[0]
        #creates the question object for display
        new_question = Text(f"{question_count}: {text}", "cambriamath", 30, (90,90,90), (WIDTH*(1/16), height))
        #sets the x position
        new_question.text_rect.left = WIDTH*(1/16)
        #adds question to group
        group.append(new_question)
        #if the question is the last item in the list, adds the group to the display list
        if i == lst[len(lst)-1]:
            display_lst.append(group)
        #updates question count
        question_count+=1
        #updates height
        height+=90
    
    return display_lst

#===BOOK AND BANK FUNCTIONS===
def question_book(status, topic, save_file_number):
    """
    Opens and displays question book.
    
    Args:
        status (str) : state of game
        topic (str) : subject
        save_file_number (int) : save file number

    Returns:
        status (str)
    """
    
    #initalize for if there are no questions
    no_questions = None
    #initalize to display the user information
    display_information = False
    #initalize for keeping track of the user 'scrolling' through the questions
    scroll_count = 0
    #initilize for if the user wants to input and check thier question
    input_question = False
    #initalize for the list of questions
    question_list = None
    #gets any questions
    question_lst = retrieve_questions(1, "vectors", "book")
    #initalize to indicate questions can be shown/exist
    show_questions = False
    #initalize to switch between displaying all questions vs one
    display_question = False
    #checks if there is a question list
    if not question_lst:
        #if there are no questions, displays that
        no_questions = Text("You have no collected questions.", "cambriamath", 30, (90,90,90), (WIDTH//2, HEIGHT//2))
    else:
        #otherwise gets the formatted list
        question_list = question_format_display(question_lst)
        #initalize to indicate if need to show message
        show_questions = True

        #initalize list for removed questions
        removed_questions = []
        #initalize text to let user know they can't access a question anymore
        no_access = None

        #creates textbox for inputting question
        textbox = pygame.Rect((WIDTH//2, HEIGHT//2), (WIDTH//2, HEIGHT//2))
        textbox.center = (WIDTH//2, HEIGHT//2)
        text_input = Text("", "Arial", 35, (255,255,255), (WIDTH//2, HEIGHT//2))
        
        #creates buttn for entering question number
        enter_question = Button("Enter", "cambriamath", 20, (0,0,0), (WIDTH//2, textbox.bottom), (100, 204, 180), (5,5), 5)
   
    #creates info button
    info_rect = Button("i", "cambriamath", 20, (255,255,255), (WIDTH-100, HEIGHT-100), (69,91,128), (5,5), 10)
    
    #creates text for information
    move_info = Text("Click up/down arrows to scroll.", "cambriamath", 10, (0,0,0), (WIDTH-100, info_rect.back.top-60))
    enter_info = Text("Click 'e' to enter question.", "cambriamath", 10, (0,0,0), (WIDTH-100, info_rect.back.top-40))
    
    #initalize return to menu button
    return_to_menu = pygame.image.load("assets\Return Button.png").convert_alpha()
    return_to_menu = pygame.transform.scale(return_to_menu, (TILE_SIZE, TILE_SIZE))
    return_rect = return_to_menu.get_rect(center = (WIDTH - 40, HEIGHT - HEIGHT + 20))

    #sets screen caption 
    pygame.display.set_caption("QUESTION BOOK: "+topic)
    
    while status == "QUESTION BOOK":
        #event handler
        for event in pygame.event.get():
            #if user clicks the x button of the window
            if event.type == pygame.QUIT:
                status = "QUIT GAME"

            #IF USER HAS CLICKED A KEY
            if event.type == pygame.KEYDOWN:
                #if user clicks the q key, quits game
                if event.key == pygame.K_q:
                    status = "QUIT GAME"
                #if there are questions to display
                if question_list and show_questions:
                    #if the user clicks the down arrow key
                    if event.key == pygame.K_DOWN:
                        #scrolls question list down by 1
                        if scroll_count < len(question_list)-1:
                            scroll_count +=1
                    #if user clicks the up arrow key
                    elif event.key == pygame.K_UP:
                        #scrolls question list up by 1
                        if scroll_count > 0:
                            scroll_count -=1
                    #if user clicks 'e' button
                    if event.key == pygame.K_e:
                        #if user has opened the input box, closes it
                        if input_question:
                            input_question = False
                        else:
                            #otherwise opens the input box
                            input_question = True
                    #if the user is typing a question
                    if input_question:
                        text_input.write(event, 4)
                if display_question:
                    #if the user has opened a question and has clicked 'b' to go back
                    if event.key == pygame.K_b:
                        #switch to show all questions and not just the one
                        show_questions = True
                        display_question = False

            #IF THE USER HAS CLICKED A MOUSE BUTTON
            if event.type == pygame.MOUSEBUTTONDOWN:
                #gets cursor position
                pos = pygame.mouse.get_pos()
                #if user has clicked info button
                if info_rect.back.collidepoint(pos):
                    #checks if information is already being displays, closes it
                    if display_information:
                        display_information = False
                    else:
                        #otherwise opens information
                        display_information = True
                #if user clicks the back to menu button
                elif return_rect.collidepoint(pos):
                    status = "QUESTION MENU"
                #if the user has clicked the enter button
                elif enter_question.back.collidepoint(pos) and question_lst:
                    #if the question is in the removed questions
                    if int(answer)-1 in removed_questions:
                        #updates and initializes to display no access message
                        no_access = Text("You cannot access this question anymore.", "cambriamath", 20, (0,0,0), (WIDTH//2, enter_question.text_rect.bottom+enter_question.text_rect.height))
                    elif int(answer)-1 >= 0 and int(answer)-1 <= len(question_lst)-1:
                        #gets question if: 0 <= answer <= maximun questions in list
                        completed_question = question_lst[int(answer)-1]
                        
                        #gets proper format for single question
                        show_question = format_single(completed_question[0])
                        #initalizes answer based off of last line in question
                        show_ans = Text("Ans: " + completed_question[1].upper(), "cambriamath", 40, (0,0,0), (WIDTH//2, show_question[len(show_question)-1].text_rect.bottom+show_question[len(show_question)-1].text_rect.height))
                        #initalize return button
                        back = Button("Return to questions", "cambriamath", 20, (255,255,255), (WIDTH*(1/8), HEIGHT*(7/8)), (100, 204, 180), (5,5), 5)
                        #initalize button to delete question
                        del_question = Button("Delete question", "cambriamath", 20, (255,255, 255), (WIDTH*(1/8), HEIGHT*(1/8)), (100, 204, 180), (5,5), 5)

                        #switch the following to empty the screen and display only the question
                        display_information = False
                        input_question = False
                        show_questions = False
                        display_question = True
                
                #if the user is clicking a button while having an individual question open
                if display_question:
                    if back.back.collidepoint(pos):
                        #switch to show all questions and not just the one
                        show_questions = True
                        display_question = False
                    #if the user has clicked the button to delete the question
                    elif del_question.back.collidepoint(pos):
                        question_lst.remove(completed_question)
                        removed_questions.append(int(answer)-1)
                        #switch to show all questions and not just the one
                        show_questions = True
                        display_question = False

        else:
            #fills screen with white
            screen.fill((201, 199, 197))
        
            #gets mouse position
            pos = pygame.mouse.get_pos()
            #display info button
            info_rect.hover((101, 132, 184), pos)
            info_rect.display()

            #displays return to menu button
            screen.blit(return_to_menu, return_rect)
            
            #if the user has no questions, displays that
            if no_questions:
                no_questions.display()
            
            #if the user does have questions
            if question_list and show_questions:
                #displays a group of questions on the screen
                for question in question_list[scroll_count]:
                    question.display()
            
            #displays information about how to use the book
            if display_information:
                move_info.display()
                enter_info.display()
            
            #if the user is trying input a question
            if input_question:
                #draws the textbox
                pygame.draw.rect(screen, (5, 5, 46), textbox)
                #displays the 'enter' button
                enter_question.hover((48, 89, 156), pos)
                enter_question.display()
                #displays the user's text and gets their input
                text_input.display()
                answer = text_input.text_value()
                #if user cannot access question, displays that
                if no_access:
                    no_access.display()
            
            #displays the chosen and its answer itself
            if display_question:
                for line in show_question:
                    line.display()
                #displays answer
                show_ans.display()
                #displays back button
                back.display()
                back.hover((48, 89, 156), pos)
                #displays button to delete question
                del_question.display()
                del_question.hover((48, 89, 156), pos)
            
            #updates screen and framerate 
            pygame.display.update()
            clock.tick(60)
    
    #updates question book
    update_whole(save_file_number, question_lst, "book", topic)

    return status

def challenge_bank(status, topic, save_file_number):
    """
    Opens and displays challenge bank.

    Args:
        status (str) : state of game
        topic (str) : subject
        save_file_number (int) : save file number

    Returns:
        status (str)
    """
    #initalize for if there are no questions
    no_questions = None
    #initalize to display the user information
    display_information = False
    
    #initalize for keeping track of the user 'scrolling' through the questions
    scroll_count = 0
    #initilize for if the user wants to input and check thier question
    input_question = False
    #initalize for the list of questions
    question_list = None
    #gets any questions
    question_lst = retrieve_questions(1, "vectors", "bank")
    
    #initalize to indicate questions can be shown/exist
    show_questions = False
    #initalize to switch between displaying all questions vs one
    display_question = False

    #checks if there is a question list
    if not question_lst:
        #if there are no questions, displays that information
        no_questions = Text("You have no collected questions.", "cambriamath", 30, (90,90,90), (WIDTH//2, HEIGHT//2))
    else:
        #otherwise gets the formatted list
        question_list = question_format_display(question_lst)
        #update to show the questions
        show_questions = True

        #creates textbox for inputting question
        textbox = pygame.Rect((WIDTH//2, HEIGHT//2), (WIDTH//2, HEIGHT//2))
        textbox.center = (WIDTH//2, HEIGHT//2)
        #initalize inputs for entering question number and answer
        question_input = Text("", "Arial", 35, (255,255,255), (WIDTH//2, HEIGHT//2))
        
        #creates buttn for entering question number
        enter_question = Button("Enter", "cambriamath", 20, (0,0,0), (WIDTH//2, textbox.bottom), (100, 204, 180), (5,5), 5)

        #initalize to save index of questions already removed
        removed_questions = []

        #initalize text to let user know they can't access a question anymore
        no_access = None
    
    #creates info button
    info_rect = Button("i", "cambriamath", 20, (255,255,255), (WIDTH-100, HEIGHT-100), (69,91,128), (5,5), 10)
    
    #creates text for information
    move_info = Text("Click up/down arrows to scroll.", "cambriamath", 10, (0,0,0), (WIDTH-100, info_rect.back.top-60))
    enter_info = Text("Click 'e' to enter question.", "cambriamath", 10, (0,0,0), (WIDTH-100, info_rect.back.top-40))

    #initalize return to menu button
    return_to_menu = pygame.image.load("assets\Return Button.png").convert_alpha()
    return_to_menu = pygame.transform.scale(return_to_menu, (TILE_SIZE, TILE_SIZE))
    return_rect = return_to_menu.get_rect(center = (WIDTH - 40, HEIGHT - HEIGHT + 20))

    #sets screen caption
    pygame.display.set_caption("QUESTION BOOK: "+topic)
    
    while status == "CHALLENGE BANK":
        #event handler
        for event in pygame.event.get():
            #if user clicks the x button of the window
            if event.type == pygame.QUIT:
                status = "QUIT GAME"

            #IF USER HAS CLICKED A KEY
            if event.type == pygame.KEYDOWN:
                #if user clicks the q key, quits game
                if event.key == pygame.K_q:
                    status = "QUIT GAME"
                #if there are questions to display
                if question_list and show_questions:
                    #if the user clicks the down arrow key
                    if event.key == pygame.K_DOWN:
                        #scrolls question list down by 1
                        if scroll_count < len(question_list)-1:
                            scroll_count +=1
                    #if user clicks the up arrow key
                    elif event.key == pygame.K_UP:
                        #scrolls question list up by 1
                        if scroll_count > 0:
                            scroll_count -=1
                    #if user clicks 'e' button
                    if event.key == pygame.K_e:
                        #if user has opened the input box, closes it
                        if input_question:
                            input_question = False
                            #if there is a no access message, gets rid of it
                            if no_access:
                                no_access = None
                        else:
                            #otherwise opens the input box
                            input_question = True
                    #if the user is typing a question
                    if input_question:
                        question_input.write(event, 4)
                if display_question:
                    #allows user to input question
                    answer_input.write(event, len(question_uncomplete[1]))

            #IF USER HAS CLICKED THE MOUSE BUTTON
            if event.type == pygame.MOUSEBUTTONDOWN:
                #gets cursor position
                pos = pygame.mouse.get_pos()
                #if user has clicked info button
                if info_rect.back.collidepoint(pos):
                    #checks if information is already being displays, closes it
                    if display_information:
                        display_information = False
                    else:
                        #otherwise opens information
                        display_information = True
                #if user returns to main screen
                elif return_rect.collidepoint(pos):
                    if display_question:
                        #switch to show all questions and not just the one
                        show_questions = True
                        display_question = False
                    else:
                        status = "QUESTION MENU"
                if show_questions:
                    #if the user has clicked the enter button to input their choice of question to view
                    if enter_question.back.collidepoint(pos):
                        #checks if this is a question they have already opened and removed
                        if int(question_number)-1 in removed_questions:
                            #initalize text to display that they cannot access question anymore
                            no_access = Text("You cannot access this question anymore.", "cambriamath", 20, (0,0,0), (WIDTH//2, enter_question.text_rect.bottom+enter_question.text_rect.height))
                        #checks if the question is greater than or equal to 0 and in the max number possible
                        elif int(question_number)-1 >= 0 and int(question_number)-1 <= len(question_lst)-1:
                            #if there is a no access message, gets rid of it
                            if no_access:
                                no_access = None

                            #gets the question the user selected
                            question_uncomplete = question_lst[int(question_number)-1]
                            
                            #gets proper format for single question
                            show_question = format_single(question_uncomplete[0])
                            
                            #initalize buttons to give up and check answer
                            give_up = Button("Give up", "cambriamath", 20, (255,255,255), (WIDTH*(1/8), HEIGHT*(1/8)), (100, 204, 180), (5,5), 5)
                            check_ans = Button("Check ans.", "cambriamath", 20, (255,255,255), (WIDTH*(1/8), give_up.text_rect.bottom+give_up.text_rect.height), (100, 204, 180), (5,5), 5)
                            #if the question has a hint, initializes the hint button
                            if len(question_uncomplete) > 2:
                                show_hint = Button("Show hint", "cambriamath", 20, (255,255,255), (WIDTH*(1/8), check_ans.text_rect.bottom+check_ans.text_rect.height), (100, 204, 180), (5,5), 5)

                            #creates the input box
                            input_box = pygame.Rect((0,0), (100, 40))
                            input_box.center = (WIDTH//2, show_question[len(show_question)-1].text_rect.bottom+show_question[len(show_question)-1].text_rect.height)
                            #creates input text
                            answer_input = Text("", "Arial", 35, (255,255,255), (WIDTH//2, show_question[len(show_question)-1].text_rect.bottom+show_question[len(show_question)-1].text_rect.height))

                            #switch the following to empty the screen and display only the question
                            display_information = False
                            input_question = False
                            show_questions = False
                            display_question = True

                            #initalize for displaying hints, answer, and feedback
                            question_hint = None
                            show_answer = None
                            feedback = None
                            
                            #initalize to check if user hasn't given up
                            gave_up = False
                
                #checks if an individual question is being displayed - IF USER HAS CLICKED A BUTTON
                if display_question:
                    #gets mouse position
                    pos = pygame.mouse.get_pos()
                    #checks if the user is clicking the give up button
                    if give_up.back.collidepoint(pos):
                        #initalizes the answer for display
                        show_answer = Text(question_uncomplete[1], "cambriamath", 20, (0,0,0), (WIDTH//2, show_question[0].text_rect.top-show_question[0].text_rect.height))
                        gave_up = True
                    #checks if the user is trying to check their answer
                    elif check_ans.back.collidepoint(pos):
                        #checks if something is already being displayed and gets rid of it
                        if question_hint:
                            question_hint = None
                        #checks if the answers match up
                        if ans.lower() == question_uncomplete[1].lower():
                            #if the answer is correct, adjusts feedback accordingly
                            feedback = Text("YOU HAVE COMPLETED THIS QUESTION. It will be added to the concept book, and removed the next time you visit the challenge bank.", "cambriamath", 20, (0,0,0), (WIDTH//2, show_question[0].text_rect.top-show_question[0].text_rect.height))
                            #update concept book
                            update_book(save_file_number, question_uncomplete, topic)
                            #removes from initial question list
                            question_lst.remove(question_uncomplete)
                            removed_questions.append(int(question_number)-1)
                        else:
                            #if answer is incorrect, adjusts feedback accordingly
                            feedback = Text("SORRY! Try again, or re-visit it later!", "cambriamath", 20, (0,0,0), (WIDTH//2, show_question[0].text_rect.top-show_question[0].text_rect.height))
                    #checks if the question has a hint
                    elif len(question_uncomplete) > 2:
                        #checks if the user is trying to access a hint
                        if show_hint.back.collidepoint(pos):
                            #if there is already something there, gets rid of it
                            if feedback:
                                feedback = None
                            #creates the hint list to display
                            question_hint = format_single(question_uncomplete[2], show_question[0].text_rect, 20, "over", 100)
        else:
            #fills screen with gray
            screen.fill((201, 199, 197))
        
            #gets mouse position
            pos = pygame.mouse.get_pos()
            #display info button
            info_rect.hover((101, 132, 184), pos)
            info_rect.display()
            
            #display return to menu button
            screen.blit(return_to_menu, return_rect)

            #if the user has no questions, displays that
            if no_questions:
                no_questions.display()
            
            #if the user does have questions
            if question_list and show_questions:
                #displays a group of questions on the screen
                for question in question_list[scroll_count]:
                    question.display()
            
            #displays information about how to use the book
            if display_information:
                move_info.display()
                enter_info.display()
            
            #if the user is trying to input a question
            if input_question:
                #draws the textbox
                pygame.draw.rect(screen, (5, 5, 46), textbox)
                #displays the 'enter' button
                enter_question.hover((48, 89, 156), pos)
                enter_question.display()
                #displays the user's text and gets their input
                question_input.display()
                question_number = question_input.text_value()
                #if the user cannot access the question, display that
                if no_access:
                    no_access.display()
            
            #if the user is trying to see an individual question
            if display_question:
                #displays the question
                for line in show_question:
                    line.display()

                #if the user hasn't given up
                if not gave_up:
                    #draws the input box for inputting their answer
                    pygame.draw.rect(screen, (5, 5, 46), input_box)
                    answer_input.display()
                    #gets their answer
                    ans = answer_input.text_value()
                    input_box.width, input_box.height = answer_input.text_rect.width, answer_input.text_rect.height
                    input_box.center=(WIDTH//2, show_question[len(show_question)-1].text_rect.bottom+show_question[len(show_question)-1].text_rect.height)
                    #displays the give up button
                    give_up.display()
                    give_up.hover((101, 132, 184), pos)
                    #displays the check answer button
                    check_ans.display()
                    check_ans.hover((101, 132, 184), pos)
                    #checks if the question contains a hint
                    if len(question_uncomplete) > 2:
                        #displays the hint
                        show_hint.display()
                        show_hint.hover((101, 132, 184), pos)
                    #shows the hint
                    if question_hint:
                        for line in question_hint:
                            line.display()
                    #shows feedback
                    elif feedback:
                        feedback.display()
                #if the has given up
                else:
                    #user has given up, so shows the answer
                    show_answer.display()
                
            #updates screen and framerate
            pygame.display.update()
            clock.tick(60)
    
    #automatically updates entire challenge bank
    update_whole(save_file_number, question_lst, "bank", topic)

    return status

def concept_book(status, topic, farthest_unit, farthest_lesson):
    """
    Opens and displays question book.

    Args:
        status (str) : state of game
        topic (str) : subject
        farthest_unit (int) : farthest unit
        farthest_lesson (int) : farthest lesson in current unit. All lessons/units before will have been unlocked.
    
    Returns:
        status (str)
    """

    #initalize to display units and lessons
    display_units = []
    display_lessons = []

    #initalize for if the units or a specific lesson is being displayed
    unit_display = True
    show_lesson = False
    lesson_error = False

    #collects content list for appropriate subject
    #content = [["Level #: Unit Name", "Lesson 1", "Etc..."]]
    if topic == "vectors":
        contents = [["Level 1: Introduction to Vectors", "Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4"], ["Level 2: Application of Vectors", "Lesson 1", "Lesson 2", "Lesson 3", "Lesson 4", "Lesson 5"]]
    elif topic == "data":
        contents = [["Level 1: Probability", "Lesson 1", "Lesson 2"]]
        
    #create a list of the unit headings
    for i in range(0, len(contents)):
        #if the current unit is less than the farthest unit reached, makes it a text without a lock
        if i <= farthest_unit:
            unit = Text(contents[i][0], "segoeuisymbol", 40, (0,0,0), (WIDTH//2, HEIGHT*(2/8)))
        #makes the locked units a text with a lock symbol
        else:
            unit = Text(contents[i][0]+u"\U0001F512", "segoeuisymbol", 40, (0,0,0), (WIDTH//2, HEIGHT*(2/8)))
        #add the current unit heading to the display list
        display_units.append(unit)

    #create a list of the locked/unlocked lessons
    for i in range(0, len(contents)):
        #initalize subgroup for lessons per unit
        sub_group = []
        #initalize the most recent rect for display from the unit heading
        recent_rect = display_units[i].text_rect
        #if the lesson value is exactly the last lesson reached (within the farthest unit)
        if i == farthest_unit-1:
            #initalize j to loop through the lessons
            j = 1
            #as lesson is less than or is the farthest lesson reached, makes it a button with appropriate positioning
            while j <= farthest_lesson:
                lesson = Button(contents[i][j], "segoeuisymbol", 30, (255,255,255), (WIDTH*(2/8), recent_rect.bottom+recent_rect.height), (100, 204, 180), (5,5), 5)
                recent_rect = lesson.text_rect
                #add to sub group and update j
                sub_group.append(lesson)
                j+=1
            #for the rest of the locked lessons, create a corresponding text object with a lock symbol with appropriate positioning
            while j <= len(contents[i])-1:
                lesson = Text(contents[i][j]+u"\U0001F512", "segoeuisymbol", 30, (0,0,0), (WIDTH*(2/8), recent_rect.bottom+recent_rect.height))
                recent_rect = lesson.text_rect
                #add to sub group and update j
                sub_group.append(lesson)
                j+=1
            #update display lesson with updated sub group
            display_lessons.append(sub_group)
        #if the lesson value is unlocked
        elif i < farthest_unit:
            #gets the lessons from the contents list
            for j in contents[i]:
                #if the item isn't the unit heading from the overall content list
                if j != contents[i][0]:
                    #creates a button of the lesson and adds to the sub group
                    lesson = Button(j, "segoeuisymbol", 30, (255,255,255), (WIDTH*(2/8), recent_rect.bottom+recent_rect.height), (100, 204, 180), (5,5), 5)
                    recent_rect = lesson.text_rect
                    sub_group.append(lesson)
            #updates the display list for lessons with the updated sub group
            display_lessons.append(sub_group)
        #for all locked lessons (not in the farthest unit, but beyond)
        else:
            #gets the lessons from the content list
            for j in contents[i]:
                #if the item isn't the unit heading from the overall content list
                if j != contents[i][0]:
                    #creates a text of the lesson and adds to sub group
                    lesson = Text(j+u"\U0001F512", "segoeuisymbol", 30, (0,0,0), (WIDTH*(2/8), recent_rect.bottom+recent_rect.height))
                    recent_rect = lesson.text_rect
                    sub_group.append(lesson)
            #updates the display list for lessons with the updated sub group
            display_lessons.append(sub_group)

    #initalize return to menu button
    return_to_menu = pygame.image.load("assets\Return Button.png").convert_alpha()
    return_to_menu = pygame.transform.scale(return_to_menu, (TILE_SIZE, TILE_SIZE))
    return_rect = return_to_menu.get_rect(center = (WIDTH - 40, HEIGHT - HEIGHT + 20))

    pygame.display.set_caption("CONCEPT BOOK: "+topic)

    #initalize the page number to move through the units
    turn_page = 0

    while status == "CONCEPT BOOK":
        for event in pygame.event.get():
            #if the user clicks the x button of the window
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            #IF THE USER CLICKS THE MOUSEBUTTON
            if event.type == pygame.MOUSEBUTTONDOWN:
                #gets mouse position
                pos = pygame.mouse.get_pos()
                #if the user clicks the return to menu button
                if return_rect.collidepoint(pos):
                    #if an error message is being displayed, return to units page
                    if lesson_error:
                        lesson_error = False
                        unit_display = True
                    #if a lesson is being displayed, return to units page
                    elif show_lesson:
                        show_lesson = False
                        unit_display = True
                    #if the user is on the units page, return to the question menu
                    else:
                        status = "QUESTION MENU"
                #if the units are being displayed
                if unit_display:
                    #checks the lessons within the page
                    for i in display_lessons[turn_page]:
                        #if the object hovered is a button
                        if isinstance(i, Button):
                            #checks if it's been pressed
                            if i.back.collidepoint(pos):
                                #gets the lesson
                                lesson_content = retrieve_lesson(turn_page+1, i.text[len(i.text)-1:], topic)
                                #if no list of the lesson has been returned
                                if not lesson_content:
                                    #sets to true to indicate there has been an eror with the lesson
                                    lesson_error = True
                                    unit_display = False
                                    #initalize an error message
                                    no_lesson = Text("Sorry, an error has occured with the lesson.", "cambriamath", 40, (0,0,0), (WIDTH//2, HEIGHT//2))
                                else:
                                    #otherwise change the following to indicate a lesson is to be displayed
                                    unit_display = False
                                    show_lesson = True
                                    #initalize a page count to move through the lesson
                                    page=0
                                    #initalize a page number display to let the user know how many pages are left
                                    pg_number = Text(f"Page {page+1} of {len(lesson_content)}. Click side arrow keys to flip.", "cambriamath", 10, (0,0,0), (0,0))
                                    pg_number.text_rect.right = WIDTH-40
                                    pg_number.text_rect.bottom = HEIGHT
            #IF THE USER CLICKS A KEY ON THE KEYBAORD
            elif event.type == pygame.KEYDOWN:
                #if the units are being displayed
                if unit_display:
                    #if the user clicks the right arrow button, turns the page if it's less than the maximun display units
                    if event.key == pygame.K_RIGHT and turn_page < len(display_units)-1:
                        turn_page+=1
                    #if the user clicks the left arrow button, turns the page the value is greater than 0
                    elif event.key == pygame.K_LEFT and turn_page > 0:
                        turn_page-=1
                #if the lesson is being displayed
                elif show_lesson:
                    #if the user clicks the right arrow button, turns the page if it isn't the last page of the lesson
                    if event.key == pygame.K_RIGHT and page < len(lesson_content)-1:
                        #updates page number and associated text 
                        page+=1
                        pg_number = Text(f"Page {page+1} of {len(lesson_content)}. Click side arrow keys to flip.", "cambriamath", 10, (0,0,0), (0,0))
                        pg_number.text_rect.right = WIDTH-40
                        pg_number.text_rect.bottom = HEIGHT
                    #if the user clicks the left arrow button, turns the page if the value is greater than 0
                    elif event.key == pygame.K_LEFT and page > 0:
                        #updates page number and associated text
                        page-=1
                        pg_number = Text(f"Page {page+1} of {len(lesson_content)}. Click side arrow keys to flip.", "cambriamath", 10, (0,0,0), (0,0))
                        pg_number.text_rect.right = WIDTH-40
                        pg_number.text_rect.bottom = HEIGHT
        else:
            #fill screen with gray
            screen.fill((201, 199, 197))
            #gets mouse position
            pos = pygame.mouse.get_pos()
            #displays return to menu button
            screen.blit(return_to_menu, return_rect)

            #if the user is looking at the overall unit and lesson lists
            if unit_display:
                #displays the unit heading
                display_units[turn_page].display()
                #displays the lessons in the unit
                for lessons in display_lessons[turn_page]:
                    lessons.display()
                    #if the lesson is a button, tracks the ability to hover over it
                    if isinstance(lessons, Button):
                        lessons.hover((101, 132, 184), pos)
            
            #if an individual lesson has been accessed
            if show_lesson:
                pg_number.display()
                #displays the text and images in the lesson
                for i in lesson_content[page]:
                    if isinstance(i, Text):
                        i.display()
                    else:
                        screen.blit(i[0], i[1])
            
            #if there has been an error with accessing the lesson, displays that
            if lesson_error:
                no_lesson.display()

            #updates screen and framerate
            pygame.display.update()
            clock.tick(60)

    return status

#===NAVIGATION AND MENU===
def question_menu(status, experience):
    """
    Menu for question interactions.

    Args:
        status (str) : state of game
        experience (int) : user experience needed to continue

    Returns:
        status (str)
    """

    #initalize title
    title = Text("Select any of the following to continue:", "cambriamath", 40, (0,0,0), (WIDTH//2, HEIGHT*(3/8)))
    #initalize buttons to direct user to each of the books
    challenge_bank = Button("Challenge Bank", "cambriamath", 40, (255,255,255), (WIDTH//2, title.text_rect.bottom+title.text_rect.height), (100, 204, 180), (5,5), 5)
    question_book = Button("Question Book", "cambriamath", 40, (255,255,255), (WIDTH//2, challenge_bank.text_rect.bottom+challenge_bank.text_rect.height), (100, 204, 180), (5,5), 5)
    concept_book = Button("Concept Book", "cambriamath", 40, (255,255,255), (WIDTH//2, question_book.text_rect.bottom+question_book.text_rect.height), (100, 204, 180), (5,5), 5)
    back_to_game = Button("Return to Game", "cambriamath", 40, (255,255,255), (WIDTH//2, concept_book.text_rect.bottom+concept_book.text_rect.height), (100, 204, 180), (5,5), 5)
    display_experience = Text(f"Experience: {experience}/{UNIT_THRESHOLD}","cambriamath", 40, (0,0,0), (WIDTH//2, back_to_game.text_rect.bottom+back_to_game.text_rect.height))

    while status == "QUESTION MENU":
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                status = "QUIT GAME"
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if challenge_bank.back.collidepoint(pos):
                    status = "CHALLENGE BANK"
                elif question_book.back.collidepoint(pos):
                    status = "QUESTION BOOK"
                elif concept_book.back.collidepoint(pos):
                    status = "CONCEPT BOOK"
                elif back_to_game.back.collidepoint(pos):
                    status = "GAMEPLAY"
        else:
            #fill screen with gray
            screen.fill((201, 199, 197))
            pos = pygame.mouse.get_pos()

            #displays the buttons to direct user to the books, bank, or back to the game + title
            title.display()

            challenge_bank.display()
            challenge_bank.hover((101, 132, 184), pos)

            question_book.display()
            question_book.hover((101, 132, 184), pos)

            concept_book.display()
            concept_book.hover((101, 132, 184), pos)

            back_to_game.display()
            back_to_game.hover((101, 132, 184), pos)

            display_experience.display()

            #updates screen and frame rate
            pygame.display.update()
            clock.tick(60)
    
    return status

def nav_question_menu(current_state, game_subject, file_save, save_unit, save_lesson, player_experience):
    """
    Menu navigations for question interactions.

    Args:
        current_state (str) : state of game
        game_subject (str) : subject
        file_save (int) : save file number
        save_unit (int) : farthest unit user has reached
        save_lesson (int) : farthest lesson user has reached (in farthest unit)
        player_experience (int) : user's current experience

    Returns:
        current_state (str)
    """
    
    while current_state != "QUIT GAME" and current_state != "GAMEPLAY":
        if current_state == "QUESTION MENU":
            #sends user to the question menu
            current_state = question_menu(current_state, player_experience)
        elif current_state == "QUESTION BOOK":
            #sends user to the question book
            current_state = question_book(current_state, game_subject, file_save)
        elif current_state == "CHALLENGE BANK":
            #sends user to the challenge bank
            current_state = challenge_bank(current_state, game_subject, file_save)
        elif current_state == "CONCEPT BOOK":
            #sends user to the concept book
            current_state = concept_book(current_state, game_subject, save_unit, save_lesson)

    return current_state