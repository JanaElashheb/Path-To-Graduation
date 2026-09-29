"""
Path to Graduation - VECTOR PROBLEM GENERATIONS
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Auto-generates Vector problems, their answer, and their hints for user to solve.

History:
Apr 28, 2025: Date created
"""
#===IMPORTS===
import random
import math
from file_handling import convert_to_uni

#===CONSTANTS===
PI = math.pi

#===GENERATE FUNCTIONS===
def generate_vectors(enemy_difficulty, player_unit, player_lesson, subject):
    """
    Generates a question set.

    Args:
        enemy_difficulty (str) : enemy difficulty
        player_unit (int)
        player_lesson (int) 
        subject (str) : subject
        
    Returns:
        formatted_set (lst) : question set containing question, answer, and hint
    """
    #checks the unit player is on
    if player_unit == 1:
        select_lesson = random.randint(1, player_lesson)
        #checks the lesson
        if select_lesson == 1:
            #gets the question set
            question_set = unit1_1(enemy_difficulty)
        elif select_lesson == 2:
            question_set = unit1_2(enemy_difficulty)
        elif select_lesson == 3:
            question_set = unit1_3(enemy_difficulty)
        elif select_lesson == 4:
            question_set = unit1_4(enemy_difficulty)
    elif player_unit == 2:
        select_lesson = random.randint(1, player_lesson)
        #checks the lesson
        if select_lesson == 1:
            #gets the question set
            question_set = unit2_1(enemy_difficulty)
        elif select_lesson == 2:
            question_set = unit2_2(enemy_difficulty)
        elif select_lesson == 3:
            question_set = unit2_3(enemy_difficulty)
        elif select_lesson == 4:
            question_set = unit2_4(enemy_difficulty)
        elif select_lesson == 5:
            question_set = unit2_5(enemy_difficulty)
    
    formatted_set = convert_to_uni(question_set, subject)

    return formatted_set

def unit1_1(difficulty):
    """
    Generates random questions for Unit 1, Lesson 1 for the Vector unit.
    
    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """
    
    #create lists of any necessary information
    vectors_lst = ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV", "WX", "YZ"]
    #general directions
    directions = ["north", "south", "west", "east"]
    #acute angles
    acute_angle = [60, 50, 30, 40, 20]
    
    #generate the random information
    vector_random = random.randint(0, len(vectors_lst)-1)
    vector = vectors_lst[vector_random]
    vectors_lst.remove(vector)
    
    vector2_random = random.randint(0, len(vectors_lst)-1)
    vector2 = vectors_lst[vector2_random]

    #generate 2 random acute angles
    acute_index = random.randint(0, len(acute_angle)-1)
    acute = acute_angle[acute_index]
    acute_angle.remove(acute)
    acute_index = random.randint(0, len(acute_angle)-1)
    acute2 = acute_angle[acute_index]
    
    #generate random numbers
    #generate random positive numbers that are small
    small_pos = random.randint(1, 10)
    small_pos2 = random.randint(1, 7)
    # generate random positive numbers that are large
    big_pos = random.randint(70, 100)
    big_pos2 = random.randint(50, 300)
    big_pos3 = random.randint(100, 400)
    # generate numbers who can be either negative or positive
    mid_num = random.randint(-10, 20)
    mid_num2 = random.randint(-15, 15)
    mid_num3 = random.randint(-8, 4)
    # generate negative numbers that are small
    small_neg = random.randint(-20, -1)

    # generate random singular direction if the difficulty is over easy
    if difficulty != "easy":
        # initalize singular directions
        north_south = ["N", "S"]
        east_west = ["W", "E"]
        # gets singular direction
        ran_dir = random.randint(0, 1)
        n_s = north_south[ran_dir]
        north_south.remove(n_s)
        n_s_2 = north_south[0]

        dir2_index = random.randint(0, 1)
        e_w = east_west[dir2_index]
    #if the difficulty is easy, get general directions
    else:
        # generate random directions
        dir1_index = random.randint(0, len(directions)-1)
        dir1 = directions[dir1_index]
        directions.remove(dir1)

        dir2_index = random.randint(0, len(directions)-1)
        dir2 = directions[dir2_index]
        directions.remove(dir2)
    
    #templates order: [["question", "answer", "hint"]]
    #provide templates of qusetions
    
    #gets a template of easy level questions
    if difficulty == "easy":
        templates = [
            [
                f"Calculate the magnitude for (vec){vector}: ({small_pos}, {mid_num}). (n)If needed, round to the nearest WHOLE NUMBER. (n)In real life, you'd leave it as an exact value (square root)!", 
                f"{round(pythag(small_pos, mid_num))}", 
                "Think about the distance formula!"
                ],
            [
                f"{vector2} has a tail at ({small_pos}, {mid_num}) and a head at ({small_neg}, {mid_num2}).(n)Determine COORDINATES of point {vector[0]} on {vector}, (n)if {vector[1]}({mid_num3}, {small_pos2}) and {vector} = {vector2}.", 
                f"({mid_num3 + (small_neg-small_pos)}, {small_pos2 + (mid_num2-mid_num)})", 
                f"Find change in {vector2}. {vector[0]} = {vector2[0]} and {vector[1]} = {vector2[1]}"
                ],
            [
                f"If (vec){vector} has a magnitude of {mid_num}, what is the magnitude of its opposite vector {vector2}?", 
                f"{-mid_num}", 
                f"Opposite vectors are always parallel..."
                ],
            [
                f"(vec){vector} has a magnitude of {small_pos+1} and faces {dir1}. (vec){vector2} has a magnitude of {small_pos2} and faces {dir1}. Are they equal?", 
                f"{check_similar(small_pos+1, small_pos2)}", 
                "What's the difference between a vector and a scalar?"
                ],
            [
                f"(vec){vector} has a magnitude of {small_pos2} and faces {dir1}. (vec){vector2} has a magnitude of {small_pos2} and faces {dir1}. Are they equal?", 
                "yes", 
                "What's the difference between a vector and a scalar?"
                ]
            ]
    #gets a template of medium level questions
    elif difficulty == "medium":
        templates = [
            [
                f"You walk due {n_s} {big_pos2}m, then due {e_w} {big_pos3}m. Calculate the magnitude of the resultant.(n)Round to one decimal place.",
                f"{round(abs(pythag(big_pos2, big_pos3)), 1)}",
                "They form a right angle triangle!"
            ],
            [
                f"(vec)a = [{small_pos}, {mid_num}] and (vec)b = [{small_neg}, {big_pos}]. Find the |resultant| of (vec)a + (vec)b.(n)Round to one decimal place.",
                f"{round(pythag((small_pos+small_neg), (mid_num+big_pos)))}",
                "(x(sb1) + x(sb2), y(sb1) + y(sb2))"
            ],
            [
                f"(vec)a = [{small_pos}, {mid_num}] and (vec)b = [{small_neg}, {big_pos}]. Find the |resultant| of (vec)a - (vec)b.(n)Round to one decimal place.",
                f"{round(pythag((small_pos-small_neg), (mid_num-big_pos)))}",
                "(x(sb1) - x(sb2), y(sb1) - y(sb2))"
            ]
        ]
    #gets a template of hard level questions
    elif difficulty == "hard":
        templates = [
            [
                f"A person walks {big_pos}m due {e_w}, then {n_s}{acute}(deg){e_w} for {small_pos}m.(n)How far are they from their starting point? What's the bearing of the resultant?(n)Round everything to the nearest integter for correct answer.(n)Format your answer as:(n)num, num",
                f"{round(cos_law(big_pos, small_pos, (90+acute)))}, {round(bearing_from_due_eastwest(e_w, n_s, (sin_law(small_pos, round(cos_law(big_pos, small_pos, (90+acute))), None, (90+acute)))))}",
                "Create a diagram, keeping vector addition in mind. Consider sin/cos law."
            ],
            [
                f"A plane flies at a velocity of {big_pos2} km/h {n_s}{acute}{e_w} when it encounters a wind with a velocity of {big_pos} km/h {n_s_2}{acute2}{e_w}.(n)What is the magnitude of the airplane (ground velocity)?(n)ANSWER FORMAT:(n)1 decimal place, whole number",
                f"{round(cos_law(big_pos2, big_pos, (acute + acute2)), 1)}, {round(bearing_same_eastwest(e_w, round(cos_law(big_pos2, big_pos, (acute + acute2))), big_pos, (acute + acute2)))}",
                "Draw out the diagram! Use the z-rule for angles and get remember sin/cos law."
            ]
        ]
    
    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit1_2(difficulty):
    """
    Generates a random question for Unit 1, Lesson 2 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    #create lists of any necessary information
    vectors_lst = ["AB", "CD", "EF", "GH", "IJ", "KL", "MN", "OP", "QR", "ST", "UV", "WX", "YZ"]
    #general directions
    directions = ["north", "south", "west", "east"]
    #list of letters
    letters = ["a", "b", "c", "d", "e", "f", "g", "h", "l", "v", "w", "x", "y", "z"]
    #acute angles
    acute_angle = [60, 50, 30, 40, 20]
    
    #generate the random information
    vector_random = random.randint(0, len(vectors_lst)-1)
    vector = vectors_lst[vector_random]
    vectors_lst.remove(vector)
    
    vector2_random = random.randint(0, len(vectors_lst)-1)
    vector2 = vectors_lst[vector2_random]

    #generate 2 random acute angles
    acute_index = random.randint(0, len(acute_angle)-1)
    acute = acute_angle[acute_index]
    acute_angle.remove(acute)
    acute_index = random.randint(0, len(acute_angle)-1)
    acute2 = acute_angle[acute_index]
    
    #generate random numbers
    #generate random positive numbers that are small
    small_pos = random.randint(1, 10)
    small_pos2 = random.randint(1, 7)
    small_pos3 = random.randint(4, 9)
    small_pos4 = random.randint(2, 10)
    # generate random positive numbers that are large
    big_pos = random.randint(70, 100)
    big_pos2 = random.randint(50, 300)
    big_pos3 = random.randint(100, 400)
    # generate numbers who can be either negative or positive
    mid_num = random.randint(-10, 20)
    mid_num2 = random.randint(-15, 15)
    mid_num3 = random.randint(-8, 4)
    # generate negative numbers that are small
    small_neg = random.randint(-20, -1)

    if difficulty == "easy":
        num = []
        for i in range(0, 8):
            num.append(random.randint(-20, 10))
        letters = ["a", "b", "c", "d", "e", "f", "g", "h", "l", "v", "w", "x", "y", "z"]
        lett = []
        for i in range(0, 6):
            if len(letters) > 0:
                ran_int = random.randint(0, len(letters)-1)
                lett.append(letters[ran_int])
                letters.remove(letters[ran_int])
        #initalize templates for easy questions
        templates = [
            [
                f"(vec)a = [{num[0]}, {num[1]}, {num[2]}] and (vec)b = [{num[3]}, {num[4]}, {num[5]}].(n)Write ({num[6]}a) + ({num[7]}b) in terms of (vec)i, (vec)j, (vec)k.(n)Add no space in between signs.",
                f"{simplify_ijk_simple([num[0], num[1], num[2]], [num[3], num[4], num[5]], num[6], num[7])}",
                f"[x, y, z] = i, j, k"
            ],
            [
                f"(vec)a = [{num[0]}, {num[1]}, {num[2]}] and (vec)b = [{num[3]}, {num[4]}, {num[5]}].(n)Write ({num[6]}a {small_neg}b) in terms of (vec)i, (vec)j, (vec)k.(n)Add no space in between signs.",
                f"{simplify_ijk_simple([num[0], num[1], num[2]], [num[3], num[4], num[5]], num[6], small_neg)}",
                f"[x, y, z] = i, j, k"
            ],
            [
                f"Determine: (vec){lett[1].upper()}{lett[2].upper()} + (vec){lett[2].upper()}{lett[3].upper()} + (vec){lett[3].upper()}{lett[4].upper()} + (vec){lett[4].upper()}{lett[5].upper()}",
                f"{lett[1].upper()}{lett[5].upper()}",
                f"Think about what cancels..."
            ]
        ]
    elif difficulty == "medium":
        num = []
        for i in range(0, 15):
            num.append(random.randint(-20, 10))
        templates = [
            [
                f"(vec)a = [{num[0]}, {num[1]}, {num[2]}] and (vec)b = [{num[3]}, {num[4]}, {num[5]}].(n)Write ({num[6]}({num[7]}a + {num[8]}b) + {num[9]}({num[10]}a + {num[11]}b)) in terms of (vec)i, (vec)j, (vec)k.(n)Add no space in between signs.",
                f"{simplify_ijk_complex([num[0], num[1], num[2]], [num[3], num[4], num[5]], [num[7], num[8]], [num[10], num[11]], num[6], num[9])}"
                f"[x, y, z] = i, j, k"
            ],
            [
                f"(vec)a = [{num[0]}, {num[1]}, {num[2]}] and (vec)b = [{num[3]}, {num[4]}, {num[5]}].(n)Write ({num[6]}({num[7]}a + {num[8]}b) {small_neg}({num[10]}a + {num[11]}b)) in terms of (vec)i, (vec)j, (vec)k.(n)Add no space in between signs.",
                f"{simplify_ijk_complex([num[0], num[1], num[2]], [num[3], num[4], num[5]], [num[7], num[8]], [num[10], num[11]], num[6], small_neg)}"
                f"[x, y, z] = i, j, k"
            ],
            [
                f"(vec)x and (vec)y are unit vectors with {acute}(deg) in between them. (n)Calculate |{small_pos}x + {small_pos2}y| to two decimal places. Determine direction to one decimal place.(n)Ans format: 0.00, 0.0",
                f"{angle_unit_vectors(small_pos, small_pos2, acute, 'addition', (2, 1))}",
                f"They start with the angle BETWEEN THEM. That means they are tail to tail..."
            ]
        ]
    else:
        templates = [
            [
                f"this is a hard question",
                f"ans"
                f"the hint is a joke: the joke is us"
            ]
        ]

    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit1_3(difficulty):
    """
    Generates a random question for Unit 1, Lesson 3 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    if difficulty == "easy":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    else:
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]

    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit1_4(difficulty):
    """
    Generates a random question for Unit 1, Lesson 4 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    if difficulty == "easy":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    else:
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
        
    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

#===UNIT 2 LESSONS===
def unit2_1(difficulty):
    """
    Generates a random question for Unit 1, Lesson 3 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    if difficulty == "easy":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    else:
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]

    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit2_2(difficulty):
    """
    Generates a random question for Unit 1, Lesson 3 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    if difficulty == "easy":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    else:
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]

    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit2_3(difficulty):
    """
    Generates a random question for Unit 1, Lesson 3 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    if difficulty == "easy":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    else:
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]

    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit2_4(difficulty):
    """
    Generates a random question for Unit 1, Lesson 3 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    if difficulty == "easy":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    else:
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]

    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit2_5(difficulty):
    """
    Generates a random question for Unit 1, Lesson 3 of the Vector unit.

    Args:
        difficulty (str) : enemy difficulty
        
    Returns:
        unformatted (lst) : question set
    """

    if difficulty == "easy":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]
    else:
        templates = [
            [
                "Beep boop this is a question with no answer",
                "no answer",
                "the hint is a joke: the joke is us"
            ]
        ]

    #get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    #get the template
    unformatted = templates[ran_index]
    
    return unformatted

#===HELPER FUNCTIONS===
def check_similar(val1, val2):
    """
    Checks if two values are the same.

    Args:
        val1 (int)
        val2 (int)
    """
    ans = "no"
    if val1 == val2:
        ans = "yes"
    
    return ans

def pythag(number1, number2, c=True):
    """
    Calculates the pythagorean theorem.

    Args:
        number1 (int)
        number2 (int)
        c (bool) : by default, True. Indicates if the hypothenuse is what's being found.
    
    Returns:
        final (int) : answer
    """
    if c:
        #finds the hypotenuse
        final = ((number1)**2 + (number2)**2)**(1/2)
    else:
        #checks which numbers if the hypotenuse
        if number1 > number2:
            final = ((number1)**2 - (number2)**2)**(1/2)
        else:
            final = ((number2)**2 - (number1)**2)**(1/2)
    
    return final

def sin(value):
    """Returns the sin value from degrees in degrees."""
    return math.sin(math.radians(value))

def cos(value):
    """Returns the cos value from degrees in degrees."""
    return math.cos(math.radians(value))

def sin_law(a, b, angleA, angleB):
    """
    Calculates sine law based on the value required. Note side lengths and angles with same letters correspond to each other in the actual equation.
    
    Args:
        a (int) : side length
        b (int) : side length
        angleA (int) : angle opposite side a
        angleB (int) : angle opposite side b

    Returns:
        final (int)
    """
    if not angleA:
        final = math.asin((a*sin(angleB))/b)*(180/PI)
    elif not angleB:
        final =  math.asin(b*sin(angleA)/a)*(180/PI) 
    elif not a:
        final = (b*sin(angleA))/sin(angleB)
    elif not b:
        final = (a*sin(angleB))/sin(angleA)

    return final

def cos_law(a, b, angleA):
    """
    Calculates the cosine law given SAS.

    Args:
        a (int)
        b (int)
        angleA (int)

    Returns:
        final (int) : final answer
    """
    final = (((a)**2 + (b)**2) - 2*a*b*(math.cos(math.radians(angleA))))**(1/2)
    
    return final

def bearing_from_due_eastwest(eastwest, northsouth, given_angle):
    """
    Calculates the bearing of the RESULTANT there is a right angle and a vector that goes due east/west.

    Args:
        eastwest (str) : east or west direction
        northsouth (str) : north or south direction

    Returns:
        bearing (int)
    """
    #calculates the bearing of resultant
    #if the direction is east
    if eastwest == "E":
        #if the direction is northeast
        if northsouth == "N":
            bearing = 90 - given_angle
        else:
            #if the direction is southeast
            bearing = 90 + given_angle
    #if the direction is west
    else:
        #if the direction is northwest
        if northsouth == "N":
            bearing = 360 - given_angle
        #if the direction is southwest
        else:
            bearing = 270 - given_angle

    return bearing

def bearing_same_eastwest(eastwest, resultant_mag, side_length, theta):
    """
    Calculates the bearing for a question with one south or east direction, but contain both north and south.
    Used for a medium level question in Unit 1, Lesson 1.

    Args:
        eastwest (str) : if the direction of the initial directions are east (E) or west (W)
        resultant_mag (int) : magnitude of the resultant
        side_length (int) : known side length for sine law
        theta (int) : known angle (of the resultant) for sine law.

    Returns:
        bearing (int)
    """

    unknown_angle = sin_law(resultant_mag, side_length, theta, None)
    if eastwest == "W":
        bearing = unknown_angle + 20 + 180
    else:
        bearing = 180 - (20 + unknown_angle)
    
    return bearing

def simplify_ijk_simple(a, b, amult, bmult):
    """
    Solves simple write in terms of i, j, k questions. Always a (+)/(-) b. Simple questions such as 2a +/- 3b.
    
    Args:
        a (lst) : list of i, j, k values, correspondingly
        b (lst) : list of i, j, k values, correspondingly
        amult (int) : value a has been multiplied by
        bmult (int) : value b has been multiplied by
    
    Returns:
        final (str) : final answer in a string
    """
    
    ijk = ["i", "j", "k"]
    
    index = 0
    for number in a:
        a[index] = number*amult
        index+=1
    
    index = 0
    for number in b:
        b[index] = number*bmult
        index+=1
    
    final = ""
    for i in range(0, len(a)):
        value = a[i] + b[i]
        if value != 0:
            if value != 0:
                if value > 0 and i > 0:
                    add_value = "+"+str(value)
                    final+=add_value
                else:
                    final+=str(value)
                final+=ijk[i]
                
    return final

def simplify_ijk_complex(a_lst, b_lst, bracket_mult1, bracket_mult2, term1_mult, term2_mult):
    """
    Simplifies/solves simple write in terms of i, j, k questions. Always a (+)/(-) b. 

    Args:
        a_lst (lst) : list of values of original a
        b_lst (lst) : list of values of original b
        bracket_mult1 (lst) : list of values in inner bracket of term one a and b values are multiplied by
        bracket_mult2 (lst) : list of values in inner bracket of term two a and b values are multiplied by
        term1_mult (int) : value term 1 is multiplied by
        term2_mult (int) : value term 2 is multiplied by

    Returns:
        solved (str) : final answer
    """

    index = 0
    for number in bracket_mult1:
        bracket_mult1[index] = number*term1_mult
        index+=1
    
    index = 0
    for number in bracket_mult2:
        bracket_mult2[index] = number*term2_mult
        index+=1
    
    mid_value = []
    for i in range(0, len(bracket_mult1)):
        mid_value.append(bracket_mult1[i]+bracket_mult2[i])
    
    solved = simplify_ijk_simple(a_lst, b_lst, mid_value[0], mid_value[1])
    
    return solved

def angle_unit_vectors(opposite_resultant, number2, angle, operation, round_ans):
    """
    Solves for the resultant and angle between two unit vectors.

    Args:
        opposite_resultant (int) : mag of vector opposite resultant
        number2 (int) : mag of second vector
        angle (int) : actue angle between vectors
        operation (str) : if they are being added or subtracted
        round_ans (tuple) : value answers should be rounded by

    Returns:
        resultant (int) : magnitude of resultant
        direction (int) : direction of resultant
    """

    if operation == "addition":
        resultant_angle = 180 - angle
    else:
        resultant_angle = angle

    resultant = cos_law(opposite_resultant, number2, resultant_angle)
    direction = sin_law(opposite_resultant, resultant, None, resultant_angle)

    resultant = round(resultant, round_ans[0])
    direction = round(resultant, round_ans[1])

    return resultant, direction