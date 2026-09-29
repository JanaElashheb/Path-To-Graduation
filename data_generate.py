"""
Path to Graduation - DATA PROBLEM GENERATIONS
ICS4U-01
Madeeha Syed, Jana Elashheb, Efua Amuah
Auto-generates Data Management problems, their answer, and their hints for user to solve.

History:
Apr 28, 2025: Date created
"""

#===IMPORTS===
import random
from fractions import Fraction
from file_handling import convert_to_uni

#===GENERATE FUNCTIONS===
def generate_data(enemy_difficulty, player_unit, player_lesson, subject):
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
        if enemy_difficulty != "hard":
            if select_lesson == 1:
                question_set = unit1_1(enemy_difficulty)
            elif select_lesson == 2:
                question_set = unit1_2(enemy_difficulty)
    
    formatted_set = convert_to_uni(question_set, subject)

    return formatted_set

def unit1_1(difficulty):
    """
    Generates random questions based on enemy difficulty.
    
    Args:
        enemy_difficulty (str) : enemy difficulty
        
    Returns:
        set (lst) : question set
    """
    
    # generate random numbers
    num1 = random.randint(1, 30)
    num2 = random.randint(1, 30)
    num3 = random.randint(1, 30)
    num4 = random.randint(1, 30)
    num5 = random.randint(1, 30)
    num6 = random.randint(20, 100)
    # num7 must be less than both num1 and num2, and in range 1 to 20
    upper_bound = min(num1, num2) - 1
    upper_bound = min(upper_bound, 20)  # num7 max is 20

    # Check for a valid range for num7
    if upper_bound >= 1:
        num7 = random.randint(1, upper_bound)
    else:
        # Regenerate num1 and num2 until num7 can exist in the valid range
        while upper_bound < 1:
            num1 = random.randint(1, 30)
            num2 = random.randint(1, 30)
            upper_bound = min(num1, num2) - 1
            upper_bound = min(upper_bound, 20)
        num7 = random.randint(1, upper_bound)
        
    #generation of fractions
    num_8 = random.randint(1, 9)
    den_8 = random.randint(num_8 + 1, 10)
    num8 = Fraction(num_8, den_8)

    num_9 = random.randint(1, 9)
    den_9 = random.randint(num_9 + 1, 10)
    num9 = Fraction(num_9, den_9)

    # Calculate upper bound for union
    max_union = min(Fraction(1), num8 + num9)
    num_10 = random.randint(1, max_union.numerator)
    den_10 = max_union.denominator
    num10 = Fraction(num_10, den_10)
    
    num11 = random.randint(20, 60)

    # Generate num12 randomly between 1 and num11 - 1
    num12 = random.randint(1, num11 - 1)

    # num13 is the remainder to make the sum equal to num11
    num13 = num11 - num12
    
    num14 = random.randint(20, 60)

    # Generate num15 randomly between 1 and num14 - 1
    num15 = random.randint(1, num14 - 1)

    # num16 is the remainder to make the sum equal to num14
    num16 = num14 - num15
    
    num17 = random.randint(100, 500)
    num18 = random.randint(100, 500)
    num19 = random.randint(100, 500)
    num20 = random.randint(100, 500)
    num21 = random.randint(20, 90)
    
    #grade list
    grade_lst = ["Grade 12", "Grade 11", "Grade 10", "Grade 9", "Seniors"]
    
    #generating a random grade
    grade_random = random.randint(0, len(grade_lst)-1)
    grade = grade_lst[grade_random]
    
    #sport team list
    sport_lst = ["Soccer Team", "Rugby Team", "Basketball Team", "Volleyball Team",  "Track and Field Team", "Cross Country Team", "Swimming Team", "Tennis Team", "Badminton Team", "Table Tennis Team", "Baseball Team", "Hockey Team", "Ultimate Frisbee Team"]
    
    #generating a random sport team
    sport_random = random.randint(0, len(sport_lst)-1)
    sport = sport_lst[sport_random]
    
    #colour list
    colour_lst = ["red", "blue", "green", "yellow", "orange", "purple", "pink", "brown", "black", "white", "gray", "cyan", "magenta", "turquoise", "lime", "navy", "maroon", "teal", "olive", "beige", "gold", "silver", "indigo", "violet", "coral"]
    
    #generating a random colour
    colour_random = random.randint(0, len(colour_lst)-1)
    colour = colour_lst[colour_random]
    
    #storm list
    storm_lst = ["there is a thunderstorm","there is a hailstorm","there is a snowstorm"," there is a blizzard","there is an ice storm","there is a dust storm","there is a sandstorm","there is a tornado","there is a hurricane","there is a cyclone", "there is a typhoon", "it rains"]
    
    #generating a random storm
    storm_random = random.randint(0, len(storm_lst)-1)
    storm = storm_lst[storm_random]
    
    #hair list
    hair_lst = ["short", "medium length", "long", "straight", "wavy", "curly"]
    
    #generating a random hair type
    hair_random = random.randint(0, len(hair_lst)-1)
    hair = hair_lst[hair_random]
    
    #sport people list one
    sport_people1_lst = ["runners", "jumpers", "swimmers", "cyclists", "skaters", "boxers", "wrestlers", "sprinters", "hurdlers", "rowers"]
    
    #generating random sport people
    sport_people1_random = random.randint(0, len(sport_people1_lst)-1)
    sport_people1 = sport_people1_lst[sport_people1_random]
    
    #sport people list 2
    sport_people2_lst = ["skiers", "snowboarders", "surfers", "climbers", "divers", "gymnasts", "weightlifters", "archers", "fencers", "martial artists"]
    
    #generating random sport people
    sport_people2_random = random.randint(0, len(sport_people2_lst)-1)
    sport_people2 = sport_people2_lst[sport_people2_random]
    
    # provide templates of qusetions
    if difficulty == "easy":
        templates = [
            [
                f"At Merivale HS there are: {num17} Gr12, {num18} Gr11, {num19} Gr10, {num20} Gr9, what is the probability of {grade} students? (n) Don't simplify answer",
                f"{theoretical_prob_grade(num17,num18,num19,num20,grade)}",
                f"P(A) = n(A)/n(S)"
                ],
            [
                f"There are {num11} students, {num12} are wearing {colour} shirts, what is the probability of students wearing {colour} shirts? (n) Don't simplify answer",
                f"{theoretical_prob_colour(num11,num12)}",
                f"P(A) = n(A)/n(S)"
                ],
            [
                f"There is a {num21}% chance {storm}, what is the probability of it NOT happening? (n) No units",
                f"{theoretical_prob_not('percent',num21)}",
                f"P(event not happening) = total - P(event happens)"
                ],
            [
                f"There are {num12} students in a class of {num11} with {hair} hair, what is the probability of students NOT having {hair} hair? (n) No units",
                f"{theoretical_prob_not('number',num12,num11)}",
                f"n(event not happening) = n(total) - n(event happens)"
                ],
            [
                f"{num8} of the class are wearing {colour} shirts, what is the probability of students NOT wearing {colour} shirts? (n) No units",
                f"{theoretical_prob_not('number',None,None,num8)}",
                f"P(event not happening) = total - P(event happens)"
                ],
            [
                f"There are {num1} boys on the {sport} and {num2} boys on the {sport}. {num7} students play on both teams. How many boys are on either of the two teams?",
                f"{union_count(num1,num2,num7)}",
                f"n(A (union) B) = n(A) + n(B) ‐ n(A (int) B)"
                ],
            [
                f"The probability of event A is {num8}, the probability of event B is {num9}. The probability of event A or B occurring is {num10}. Are these events mutually exclusive (yes/no)?",
                f"{is_mutually_exclusive(num8, num9, num10)}",
                f"n(A (union) B) = n(A) + n(B) - n(A (int) B)"
                ],
            [
                f"A school track team of {num11} students has {num12} {sport_people1} and {num13} {sport_people2}. How many are both {sport_people1} and {sport_people2}? (n) No units",
                f"{finding_intersection(num11,num12,num13)}",
                "n(A (union) B) = n(A) + n(B) ‐ n(A (int) B)"
                ]
        ]
    elif difficulty == "medium":
        templates = [
            [
                f"There are {num11} dogs at the PetSmart Pet Hotel ({num12} females, {num13} males) and {num14} cats ({num15} males, {num16} females). If the manager randomly selects a pet, what is the probability that it is a female or a cat? (n)Don't simplify answer",
                f"{prob_female_cat(num11,num12,num13,num14,num15,num16)}",
                f"P(A (union) B) = P(A) + P(B) - P(A (int) B)"
                ],
            [
                f"A Spotify playlist has {num1} rap songs, {num2} country songs, {num3} techno songs, {num4} classic rock songs, {num5} pop rock songs, and some punk rock. When your playlist is on shuffle,the theoretical probability of playing a rock song is {num6}%. Give the answer to the nearest whole number, and no units.",
                f"{theoretical_prob_x(num1, num2, num3, num4, num5, num6)}",
                f"Theoretical Probability Formula: P(A) = n(A)/n(S)"
                ]
            ]
    
    # get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    # get the template
    unformatted = templates[ran_index]
    
    return unformatted

def unit1_2(difficulty):
    """
    Generates random questions based on enemy difficulty.
    
    Args:
        enemy_difficulty (str) : enemy difficulty
        
    Returns:
        set (lst) : question set
    """
    #generation of fractions
    num_1 = random.randint(1, 9)
    den_1 = random.randint(num_1 + 1, 10)
    num1 = Fraction(num_1, den_1)

    num_2 = random.randint(1, 9)
    den_2 = random.randint(num_2 + 1, 10)
    num2 = Fraction(num_2, den_2)
    
    
    num_3 = random.randint(1, 9)
    den_3 = random.randint(num_3 + 1, 10)
    num3 = Fraction(num_3, den_3)
    
    
    # Generate random numbers
    num4 = random.randint(500, 1000)

    # Pick num5 between 1 and num4 - 2
    num5 = random.randint(1, num4 - 2)

    # Pick num6 between 1 and num4 - num5 - 1
    num6 = random.randint(1, num4 - num5 - 1)

    # Calculate num7 so total equals num4
    num7 = num4 - num5 - num6
    
     # Generate random numbers
    num8 = random.randint(500, 1000)

    # Pick num9 between 1 and num8 - 2
    num9 = random.randint(1, num8 - 2)

    # Pick num10 between 1 and num8 - num9 - 1
    num10 = random.randint(1, num8 - num9 - 1)

    # Calculate num11 so total equals num8
    num11 = num8 - num9 - num10
    
    #generates random numbers
    num12 = random.randint(100, 500)
    
    num13 = random.randint(50, 350)
    
    num14 = random.randint(60, 95)
    
    num15 = num13 - random.randint(10, 40)
    
    num16 = random.randint(10, 55)
    
    #grade list
    grade_lst = ["Seniors","Juniors"]
    
    #generating a random grade
    grade_random = random.randint(0, len(grade_lst)-1)
    grade = grade_lst[grade_random]
    
    #choice list
    choice_lst = ["approves", "disapproves", "is neutral"]
    
    #generating a random choice
    choice_random = random.randint(0, len(choice_lst)-1)
    choice = choice_lst[choice_random]
    
    #sports list
    sport_lst = ["Soccer", "Basketball", "Baseball", "Volleyball", "Tennis", "Table Tennis", "Badminton", "Cricket", "Rugby", "American Football", "Hockey", "Golf", "Swimming", "Track and Field", "Gymnastics", "Wrestling", "Boxing", "Martial Arts", "Skiing", "Snowboarding", "Cycling", "Skateboarding", "Surfing", "Rowing", "Climbing"]
    
    #generating a random sport
    sport_random = random.randint(0, len(sport_lst)-1)
    sport = sport_lst[sport_random]
    
    #subjects list
    subject_lst = ["Mathematics", "English", "Biology", "Chemistry", "Physics", "History", "Geography", "Computer Science", "Art", "Music", "Physical Education", "Drama", "Economics", "Philosophy", "Environmental Science", "Business Studies", "Health Education", "Psychology", "Sociology", "French", "Spanish", "German", "Engineering", "Media Studies", "Design and Technology"]
    
    #generating a random subject
    subject_random = random.randint(0, len(subject_lst)-1)
    subject = subject_lst[subject_random]
    
    # provide templates of qusetions
    if difficulty == "easy":
        templates = [
            [
                f"The probability of event G is {num1}. The probability of event H is {num2} and the probability of both is {num3}. Determine the probability that of H given G? (n) Don't simplify answer",
                f"{conditional_prob(num1,num3)}",
                f"P(B|A) = P(A (int) B)/ P(A)"
                ],
            [
                f"Seniors: Approve - {num5} Disapprove - {num6} Neutral - {num7} Total - {num4} (n) Juniors: Approve - {num9} Disapprove - {num10} Neutral - {num11} Total - {num8} (n)Determine the probability that a student {choice} of the portables location given that they're a {grade}? (n) Don't simplify answer",
                f"{conditional_prob_grade(grade,choice,num4,num5,num6,num7,num8,num9,num10,num11)}",
                f"P(B|A) = n(A (int) B)/ n(A)"
                ],
            [
                f"Of {num8} MHS students, {num13} play {sport}, {num14} students had {sport} injuries and of these {num16} played {sport}.(n)Determine the probability of having a {sport} injury given that you don’t play {sport}.? (n) Don't simplify answer",
                f"{conditional_prob_grade(grade,choice,num4,num5,num6,num7,num8,num9,num10,num11)}",
                f"P(B|A) = n(A (int) B)/ n(A)"
                ],
        ]
    elif difficulty == "medium":
        templates = [
            [
                f"Out of {num12} Merivale grads, {num13} have an average of over {num14}% and of these, {num15} take at least one {subject} course. Determine the probability a student does not take {subject} given that they have an average of over {num14}%? (n)Don't simplify answer",
                f"{conditional_prob_challenge(num13,num15)}",
                f"P(B|A) = n(A (int) B)/ n(A)"
                ],
            ]
    
    # get a random index from the template
    ran_index = random.randint(0, len(templates)-1)
    
    # get the template
    unformatted = templates[ran_index]
    
    return unformatted

#FUCTIONS FOR THE MATH FORMULAS
def theoretical_prob_x(num1, num2, num3, num4, num5, num6):
    """
    Gets the answer for a experimental probabilty question when looking for an x- value
    
    Args:
        num1 (int)
        num2 (int)
        num3 (int)
        num4 (int)
        num5 (int)
        num6 (int)
        
    Returns:
        anwer (int)
    
    """
    #truning the percent into a decimal
    probability = num6/100
    
    non_punk_total = num1 + num2 + num3 + num4 + num5  
    rock_total_fixed = num4 + num5  


    answer = (probability * non_punk_total - rock_total_fixed) / (1 - probability)

    return int(round(answer))

def union_count(num1, num2, num3):
    """
    Calculate n(A ∪ B) using the formula: n(A ∪ B) = n(A) + n(B) - n(A ∩ B)
    
    Args:
        num1 (int)
        num2 (int)
        num3 (int)

    Returns:
        answer (int)
        
    """
    return num1 + num2 - num3

def is_mutually_exclusive(num1, num2, num3):
    """
    Calculate n(A ∩ B) using the formula: n(A ∪ B) = n(A) + n(B) - n(A ∩ B), to check if it is mutually exclusive
    
    Args:
        num1 (Fraction)
        num2 (Fraction)
        num3 (Fraction)
        
    Returns:
        answer (str)
        
    """
    # Use additive principle to compute P(A ∩ B)
    intersection = num1 + num2 - num3
    # True if mutually exclusive
    intersection == 0
    #checking to see if it is mutually exclusive or not
    if not(intersection):
        answer = "yes"
    else:
        answer = "no"
        
    return answer

def prob_female_cat(num1,num2,num3,num4,num5,num6):
    """
    Calculates the probability of getting a female or a cat
    
    Args:
        num1 (int)
        num2 (int)
        num3 (int)
        num4 (int)
        num5 (int)
        num6 (int)
        
    Returns:
        answer (Fraction)
        
    """
    #getting total number of females
    female = num2 + num6
    
    #total number of pets
    total = num1 + num4
    
    #getting the union value
    union = female + num4 - num6
    
    answer = Fraction(union, total)
    
    return answer

def finding_intersection(num1,num2,num3):
    """
    Calculate n(A ∩ B) using the formula: n(A ∪ B) = n(A) + n(B) - n(A ∩ B)
    
    Args:
        num1 (int)
        num2 (int)
        num3 (int)
        
    Returns:
        answer (int)
    """
    #finding the answer 
    answer = (num2 + num3) - num1
    
    return answer
            
def theoretical_prob_grade(num1,num2,num3,num4,grade):
    """
    Gets the probability of studenst depending on grade
    
    Args:
        num1 (int)
        num2 (int)
        num3 (int)
        num4 (int)
        garde (str)
        
    Returns:
        answer (Fraction)
        
    """
    #getthing the total number of students
    total = num1 + num2 + num3 + num4
    
    #getting the answer depending on grade
    if grade == "Grade 12":
        answer = Fraction (num1, total)
    elif grade == "Grade 11":
        answer = Fraction (num2, total)
    elif grade == "Grade 10":
        answer = Fraction (num3, total)
    elif grade == "Grade 9":
        answer = Fraction (num4, total)
    else:
        answer = Fraction ((num1 + num2), total)
    
    return answer

def theoretical_prob_colour(num1,num2):
    """
    Gets the probability of studenst wearing a coloured shirt
    
    Args:
        num1 (int)
        num2 (int)
        
    Returns:
        answer (Fraction)
    """
    #getting the answer
    answer = Fraction (num2, num1)
    
    return answer

def theoretical_prob_not(type_, num1 = None,num2 = None, num3 = None):
    """
    Gets the probability of a complementary event
    
    Args:
        num1 (int)
        num2 (int)
        num3 (Fraction)
        type_ (str)
    
    Returns:
        answer(int) or (Fraction)
    """
    #finding the answer depending on the type_
    if type_ == "percent" and num1:
        #getting the answer
        answer = 100 - num1
    elif type_ == "fraction" and num3:
        answer = 1 - num3
    else:
        if num2 and num1:
            #getting the answer
            answer = num2 - num1
        else:
            answer = "na"
    
    return answer

def conditional_prob(num1,num2):
    """
    Gets the conditional probability
    
    Args:
        num1 (Fraction)
        num2 (Fraction)
        
    Returns:
        answer (Fraction)
        
    """
    answer = num2/num1
    return answer

def conditional_prob_grade(grade,choice,num4,num5,num6,num7,num8,num9,num10,num11):
    """
    Gets the conditional probability for grade related questions
    
    Args:
        num4 (int)
        num5 (int)
        num6 (int)
        num7 (int)
        num8 (int)
        num9 (int)
        num10 (int)
        num11 (int)
        grade (str)
        choice (str)
    
    Returns:
        answer (Fraction)
    
    """
    #Getting the answer depending on grade and choice
    if grade == "Seniors":
        if choice == "approves":
            answer = Fraction (num5,num4)
        elif choice == "disapproves":
            answer = Fraction (num6,num4)
        else:
            answer = Fraction (num7,num4)
    elif grade == "Juniors":
        if choice == "approves":
            answer = Fraction (num9,num8)
        elif choice == "disapproves":
            answer = Fraction (num10,num8)
        else:
            answer = Fraction (num11,num8)
    
    return answer

def conditional_prob_challenge(num1,num2):
    """
    Gets the conditional Probaility
    
    Args:
        num1 (int)
        num2 (int)
    
    Returns:
        answer (Fraction)
        
    """
    #getting the naser
    answer = Fraction((num1-num2),num1)
    
    return answer