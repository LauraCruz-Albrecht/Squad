'''
score.py
--------
util functions for computing the score between a user and candidate
'''

def get_distance(user_rating, c_rating, offset, scale):
    '''
    Computes a score for distance between the user answer and candidate answer.
    Smaller distance leads to larger score.

    Arguments:
        user_rating (int): user answer for the question
        c_rating (int): candidate answer for the question
        offset (int): value we subtract from raw distance to center the values
        scale (float): normalization value

    Returns:
        score (float): normalized distance score between user answer and candidate answer
    '''
    dist = 5 - abs(user_rating - c_rating)
    return (dist + offset)/scale

def get_set_intersection_score(user_ans, c_ans):
    '''
    Computes a score between 0 and 1 representing similarity between user and candidate answer.
    Answers are treated as sets and we take set intersection to represent similarity.
    Normalize by the number of items in user's set. 

    Arguments:
        user_ans (string): user's set parsed as string
        c_ans (string): candidate's set parsed as string

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    user_set = set(''.join(user_ans.split()).split(','))
    c_set = set(''.join(c_ans.split()).split(','))
    return 1.0*len(user_set.intersection(c_set))/len(user_set)

def get_socioeconomic_score(user_info, c_info):
    '''
    Computes a score between 0 and 2 for socioecnomic question (weight is 2).
    If either user or candidate does not provide an answer, the score is 0.

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    question_idx = 12
    prefer_idx = 13
    class_idx = { "Lower class" : 0,
                  "Lower-middle class": 1,
                  "Middle class": 2,
                  "Middle-upper class": 3,
                  "Upper class": 4 }
    if user_info[question_idx] not in class_idx or c_info[question_idx] not in class_idx:
        return 0
    raw_score = get_distance(class_idx[user_info[question_idx]], class_idx[c_info[question_idx]], -3, 2.0)
    preference = (int(user_info[prefer_idx]) - 1)/4.0
    scaled_score = raw_score*preference
    return scaled_score*2

def get_schools(major):
    '''
    Returns set of schools corresponding to given major.
    0 : School of Earth, Energy & Environmental Sciences
    1 : School of Engineering
    2 : School of Medicine
    3 : School of Humanities & Sciences

    Arguments:
        major (string): major

    Returns:
        schools (set): set of indices correponding to the schools the major is part of
    '''
    school_idx = { "Aeronautics and Astronautics": 1,
                   "Anthropology": 2,
                   "Architectural Design": 1,
                   "Atmosphere/ Energy": 0,
                   "Biology": 2,
                   "Biomedical Computation": 1,
                   "Chemistry": 2,
                   "Community Health and Prevention Research": 2,
                   "Computer Science": 1,
                   "Earth Systems": 0,
                   "Energy Resources Engineering": 0,
                   "Geological Sciences": 0,
                   "Geophysics": 0,
                   "Honors in the Arts": 2,
                   "Laboratory Animal Science": 2,
                   "Mathematical and Computational Science": 1,
                   "Physics": 2,
                   "Product Design": 1,
                   "Public Policy": 2,
                   "Symbolic Systems": 1,
                   "Sustainability": 0 }
    if major in school_idx:
        return set([school_idx[major]])
    elif "Engineering" in major or "engineering" in major:
        return set([1])
    elif "CS" in major: #CS + X
        return set([1, 3])
    else:
        return set([3])

def get_majors_score(user_info, c_info):
    '''
    Computes a score between 0 and 2 for socioecnomic question (weight is 2).
    
    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    question_idx = 14
    prefer_idx = 15
    user_major = user_info[question_idx]
    c_major = c_info[question_idx]
    preference = int(user_info[prefer_idx])
    if preference == 3: # no preference
        return 1
    elif preference == 5: # only major
        return 2 if user_major == c_major else 0
    elif preference == 1: # only not major
        return 2 if user_major != c_major else 0
    user_schools = get_schools(user_major)
    c_schools = get_schools(c_major)
    if preference == 4: # at least one same school
        return 2 if len(user_schools.intersection(c_schools)) > 0 else 0
    else: # at least one different school
        return 2 if len(user_schools.intersection(c_schools)) != len(user_schools) else 0

def get_intelligence_score(user_info, c_info):
    '''
    Computes a score between -2 and 2 for intelligence questions (weight is 2).

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    question_idx = 19
    prefer_idx = 20
    raw_score = 1 if int(user_info[question_idx]) <= int(c_info[question_idx]) else -1
    preference = (int(user_info[prefer_idx]) - 3)/2.0
    scaled_score = raw_score*preference
    return scaled_score*2

def get_hangout_frequency_score(user_info, c_info):
    '''
    Computes a score between 0 and 2 for hangout frequency question (weight is 2).

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    question_idx = 36
    category_idx = { "Every meal" : 0,
                     "Once a day": 1,
                     "Couple times a week": 2,
                     "Every weekend": 3,
                     "Couple times a month": 4 } 
    return get_distance(category_idx[user_info[question_idx]], category_idx[c_info[question_idx]], -1, 4.0)*2

def get_music_score(user_info, c_info):
    '''
    Computes a score between 0 and 1 for music question.

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    question_idx = 43
    return get_set_intersection_score((user_info[question_idx]).lower(), (c_info[question_idx]).lower())

def get_enjoy_talking_score(user_info, c_info):
    '''
    Computes a score between 0 and 2 for I enjoy talking about... question (weight is 2).

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    question_idx = 44
    return get_set_intersection_score((user_info[question_idx]).lower(), (c_info[question_idx]).lower())*2

def get_chill_score(user_info, c_info):
    '''
    Computes a score between -1 and 1 for chill question.

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answer
    '''
    question_idx = 45
    category_idx = { "Literally down to do anything anytime anywhere anyhow anywhy." : 0,
                     "Almost always down to go to L&L at 3am on a Wednesday.": 1,
                     "\"I'm good with anything.\"": 2,
                     "I get tilted when people flake on me.": 3,
                     "I get pissed off when my roommate uses my tissue box without asking.": 4, 
                     "I freak out when the utensils aren't exactly where they should be on the dinner table.": 5 }
    return get_distance(category_idx[user_info[question_idx]], category_idx[c_info[question_idx]], -3, 2.0)

def get_similarity_score(user_info, c_info):
    '''
    Computes cumulative score of all similarity questions between user and candidate.
    Multiplies sum by how similar or dissimilar user wants the match to be. 
    Large positive score indicates high similarity, large negative score indicates high dissimilarity. 

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answers
    '''
    question_idx = [16, 17, 21, 23, 27, 28, 34, 35, 37, 38, 39, 41, 42]
    similarity_idx = 22
    similarity_weight = (int(user_info[similarity_idx]) - 3)/2.0
    score = sum([get_distance(int(user_info[idx]), int(c_info[idx]), -3, 2.0) for idx in question_idx])
    score += get_music_score(user_info, c_info)
    score += get_chill_score(user_info, c_info)
    return score*similarity_weight

def get_activity_score(user_info, c_info):
    '''
    Computes cumulative score of all activity questions between user and candidate.
    Large score means user and candidate like to do similar activities with friends.

    Arguments:
        user_info (list): complete user response
        c_info (list): complete candidate reponse

    Returns:
        score (float): normalized score between user answer and candidate answers
    '''
    question_idx = [18, 24, 25, 26, 29, 30, 31, 32, 33]
    score = sum([get_distance(int(user_info[idx]), int(c_info[idx]), -1, 4.0) for idx in question_idx])
    contact_idx = 40
    score += get_distance(int(user_info[contact_idx]), int(c_info[contact_idx]), -1, 4.0)*2
    score += get_hangout_frequency_score(user_info, c_info)
    return score
