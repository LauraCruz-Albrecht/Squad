import os
import re
import csv
import math
import pandas as pd
import numpy as np
from score import *

'''
squad.py
--------
Authors: Laura Cruz-Albrecht, Tara Iyer, Eric Yanmin Xu, Glenn Yu | 2018

This program implements the Squad friendship-recommendation algorithm.
It takes as input a csv with responses to a questionnaire, and outputs
3-6 friend suggestions for each user in the system.
'''

# Read the form responses into a matrix
# See indices.txt for quick reference on index for each question/field
RESPONSES_CSV = 'First_343_Responses_Manually_Parsed.csv'
parsed_csv = [row for row in csv.reader(open(RESPONSES_CSV, 'r'))]
responses_header = parsed_csv[0]

# Note: can use subset, ie [1:k], while testing/debugging, but for final
# run should use all, ie: `parsed_csv[1:]`
responses = parsed_csv[1:]  

N_users = len(responses)
MIN_MATCHES = 3
MATCH_THRESHOLD = 5

# CSV to write the recommendation results to
RESULTS_CSV = 'Results.csv'

def is_gender_conflict(user_id, c_id):
    '''
    Returns whether user user_id, and candidate c_id conflict with
    regards to user_id's preference for gender.

    Arguments:
        user_id (int): id (index) of user we are trying to get matches for
        c_id (int): id (index) of candidate user

    Returns:
        is_conflict (boolean): True if c_id is not a valid candidate
            for user_id, False otherwise
    '''
    gender_idx = 6
    gender_preference_idx = 7

    u_gender = responses[user_id][gender_idx]
    c_gender = responses[c_id][gender_idx]
    u_gender_preference = responses[user_id][gender_preference_idx]

    # if 'Any/all of the above' in u's preferences, then c is valid candidate (no conflict)
    if 'Any/all of the above' in u_gender_preference:
        return False

    # if c's gender is in u's preferences, then c is valid candidate (no conflict)
    if c_gender in u_gender_preference:
        return False

    # otherwise, there's a conflict
    return True

def is_religion_conflict(user_id, c_id):
    '''
    Returns whether user user_id, and candidate c_id conflict with
    regards to user_id's preference for religion.

    Arguments:
        user_id (int): id (index) of user we are trying to get matches for
        c_id (int): id (index) of candidate user

    Returns:
        is_conflict (boolean): True if c_id is not a valid candidate
            for user_id, False otherwise
    '''
    religion_idx = 8
    religion_preference_idx = 9

    u_religion = responses[user_id][religion_idx]
    c_religion = responses[c_id][religion_idx]
    u_religion_preference = responses[user_id][religion_preference_idx]

    # if 'Any/all of the above' in u's preferences, then c is valid candidate (no conflict)
    if 'Any/all of the above' in u_religion_preference:
        return False

    # if c's religion is in u's preferences, then c is valid candidate (no conflict)
    if c_religion in u_religion_preference:
        return False

    # otherwise, there's a conflict
    return True

def is_political_conflict(user_id, c_id):
    '''
    Returns whether user user_id, and candidate c_id conflict with
    regards to user_id's preference for political party.

    Arguments:
        user_id (int): id (index) of user we are trying to get matches for
        c_id (int): id (index) of candidate user

    Returns:
        is_conflict (boolean): True if c_id is not a valid candidate
            for user_id, False otherwise
    '''
    if user_id == 80:
        return False
    party_idx = 10
    party_preference_idx = 11

    u_party = responses[user_id][party_idx]
    c_party = responses[c_id][party_idx]
    u_party_preference = responses[user_id][party_preference_idx]

    # if 'Any/all of the above' in u's preferences, then c is valid candidate (no conflict)
    if 'Any/all of the above' in u_party_preference:
        return False

    # if c's party is in u's preferences, then c is valid candidate (no conflict)
    if c_party in u_party_preference:
        return False

    # otherwise, there's a conflict
    return True

def filter(user_id):
    '''
    Gets list of candidate user ids: this is the subset of all users
    that are valid candidates after filtering for for preferences in
    3 categories: gender, religion, and political party

    Arguments:
        user_id (int): id (index) of user for which to get candidates

    Returns:
        candidate_user_ids (list): list of user id's of users that pass
                user_id's filtering criteria
    '''

    # initially make all users except the given user_id a candidate
    candidate_flags = [True] * N_users
    candidate_flags[user_id] = False

    # filter out candidates that have gender/religion/political party conflict
    for c_id in range(N_users):
        if (is_gender_conflict(user_id, c_id) 
            or is_religion_conflict (user_id, c_id) 
            or is_political_conflict(user_id, c_id)):
            candidate_flags[c_id] = False

    # use candidate_flags to get list of valid candidate ids
    candidate_user_ids = [i for i in range(N_users) if candidate_flags[i]]
    return candidate_user_ids

def score(user_id, c_id):
    '''
    Returns a score of c_id as a potential match for user_id.
    Computes score by taking weighted based on contribution of
    each 'weight' question. See google doc for details.

    Arguments:
        user_id (int): id (index) of user
        c_id (int): id (index) of candidate

    Returns:
        score (float): value indicating how good of a match candididate c_id 
        is for user user_id.
    '''
    score = get_socioeconomic_score(responses[user_id], responses[c_id])
    score += get_majors_score(responses[user_id], responses[c_id])
    score += get_intelligence_score(responses[user_id], responses[c_id])
    score += get_enjoy_talking_score(responses[user_id], responses[c_id])
    score += get_similarity_score(responses[user_id], responses[c_id])
    score += get_activity_score(responses[user_id], responses[c_id])
    return score

def get_normalized_map(scores_map):
    '''
    Normalizes the scores map so that all scores are between 0 and 1.

    Arguments:
        scores_map (int->float dict): map from user id to candidate score for each
                                      valid candidate for user with id user_id
    
    Returns:
        normalized_map (int->float dict): map from user id to candidate score between 0 and 1
    '''
    if len(scores_map) == 0:
        return scores_map
    min_score = min(scores_map.values())
    max_score = max(scores_map.values())
    normalized_map = {}
    for c_id, score in scores_map.items():
        normalized_map[c_id] = (score - min_score)/(max_score - min_score)
    return normalized_map

def get_scores_map(user_id):
    '''
    Gets scores map for user with id user_id. The scores map contains all
    users besides user_id after the filtering step and the corresponding
    "candidate score" of each candidate after the weighting step.

    Arguments:
        user_id (int): id of user to construct candidate scores map. 
                       user_id corresponds to the index of the user
                       in the responses matrix (from the parsed csv file)

    Returns:
        scores_map (int->float dict): map from user id to candidate score for each 
                                      valid candidate for user with id user_id

    '''
    # gets list of candidate user ids
    candidate_user_ids = filter(user_id)

    # initialize scores map: key is candidate id, value is candidate score (init to 0)
    scores_map = dict.fromkeys(candidate_user_ids, 0)

    # score each candidate
    for c_id in scores_map:
        candidate_score = score(user_id, c_id)
        scores_map[c_id] = candidate_score
    
    return get_normalized_map(scores_map)

def get_all_scores_maps():
    '''
    Gets scores map for all users.

    Arguments:
        None

    Returns:
        scores_map_list (list of int->float dicts): list of scores map for all users;
            scores_map_list[i] = scores map (map from candidate to candidate score) for user i
    '''
    scores_map_list = []
    for i in range(N_users):
        scores_map_for_i = get_scores_map(i)
        scores_map_list.append(scores_map_for_i)

    return scores_map_list

def get_all_pairings(scores_map_list):
    '''
    Gets matches for all users, based on the scores_map and score function S.
    In particular, for people A and B, compute match score S defined below

        S(A, B) = exp(A's score for B) + exp(B's score for A)

    We then sort the scores in decreasing order and greedily assign matches.
    It skips a potential match if both users already have at least MIN_MATCHES matches
    or at least one of them has at least MATCH_THRESHOLD matches.

    Arguments:
        scores_map_list (list of int->float dicts): list of scores map for all users;
            scores_map_list[i] = scores map (map from candidate to candidate score) for user i

    Returns:
         match_pairs (list): a list of all matches between users expressed as tuples of user ids
    '''
    edges = []
    for user1 in range(N_users):
        for user2 in range(user1 + 1, N_users):
            if user2 not in scores_map_list[user1] or user1 not in scores_map_list[user2]:
                continue
            match_score = math.exp(scores_map_list[user1][user2]) + math.exp(scores_map_list[user2][user1])
            edges.append((user1, user2, match_score))
    
    edges.sort(key=lambda x: -x[2])
    match_cnts = [0 for _ in range(N_users)]
    match_pairs = []
    for user1, user2, _ in edges:
        if match_cnts[user1] >= MIN_MATCHES and match_cnts[user2] >= MIN_MATCHES:
            continue
        elif match_cnts[user1] >= MATCH_THRESHOLD or match_cnts[user2] >= MATCH_THRESHOLD:
            continue
        match_cnts[user1] += 1
        match_cnts[user2] += 1
        match_pairs.append((user1, user2))

    print_match_stats(match_cnts)
    return match_pairs

def print_match_stats(match_cnts):
    '''
    Prints histogram and for each user the number of times the user appeared in the
    top 3 recommendations of some other user.

    Arguments:
        match_cnts (list): match_cnts[i] = number of pairings user is in

    Returns:
        None
    '''
    histogram = [0 for _ in range(max(match_cnts) + 1)]
    for cnt in match_cnts:
        histogram[cnt] += 1
    for i in range(len(histogram)):
        print('%d users have %d matches.' % (histogram[i], i))

    first_name_idx = 2
    last_name_idx = 3
    user_cnts = [(responses[user_id][first_name_idx], responses[user_id][last_name_idx], match_cnts[user_id]) \
                 for user_id in range(N_users)]
    user_cnts.sort(key=lambda x: -x[2])
    for entry in user_cnts:
        print('%s %s is in %d matches.' % (entry[0], entry[1], entry[2]))

    print ('\n==> There are %d matches' % (sum(match_cnts)/2))

def get_info(id, include_blurb=False):
    '''
    Gets name/email/blurb info for user with given id.

    Arguments:
        id (int): id (index) of a user
        include_blurb (boolean): whether to include user blurb in the result

    Returns:
        info (list): list containing: [name, email, (optional) blurb]
            note: name consists of concatenating first and last time
    '''
    email_idx = 1
    first_name_idx = 2
    last_name_idx = 3
    blurb_idx = 46

    row = responses[id]
    name = row[first_name_idx] + ' ' + row[last_name_idx]
    email = row[email_idx]

    info = [name, email]
    if include_blurb:
        blurb = row[blurb_idx]
        if len(blurb) < 1: blurb = 'None provided'
        info.append(blurb)

    return info

def format_and_save(match_pairs):
    '''
    Formats and saves match pairs into a file. Each row is a single match
    pair, with name/email/blurb for each person.

    Arguments: 
        match_pairs (list): list of tuples of ints, (id1, id2) of users where
            at least one person was a recommendation (appeared in the top-3 list)
            for the other person

    Returns:
        None
    '''
    with open(RESULTS_CSV, mode='w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # write header
        header = [
            'name1', 'email1', 'blurb1',
            'name2', 'email2', 'blurb2', 
        ]
        csv_writer.writerow(header)

        # write contents
        for tup in match_pairs:
            id1, id2 = tup
            row = get_info(id1, include_blurb=True) + get_info(id2, include_blurb=True)
            csv_writer.writerow(row)

def print_results():
    '''
    Open results csv and print contents nicely to console.

    Arguments:
        None

    Returns:
        None
    '''
    df = pd.read_csv(RESULTS_CSV)
    print (' ')
    for index, row in df.iterrows():
        print ('-- %s | %s | %s' % (row['name1'], row['email1'], row['blurb1']))
        print ('-- %s | %s | %s' % (row['name2'], row['email2'], row['blurb2']))
        print (' ')

def run_squad():
    # 1. for each person, get scores map containing candidate score for each valid candidate
    scores_map_list = get_all_scores_maps()

    # 2. get all matches as a list of tuples of user ids
    match_pairs = get_all_pairings(scores_map_list)

    # 3. extract and save the names/emails/blurbs to results csv file
    format_and_save(match_pairs)

    # 4. open results csv and print contents nicely to console
    print_results()

run_squad()
