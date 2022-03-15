# Allows user to rank teams and get a results json file
#import pdb; pdb.set_trace()

import cv2
import imutils
import numpy as np

import json
import os
import random
import sys
import time

from google_images_download import google_images_download

# These are all modified by the user at runtime
NUM_IMAGES = 3
SEED_WEIGHT = None
RANDOMNESS = 0 

def get_timestamp():
    curr_time_struct = time.localtime()
    timestamp_str = str(time.time_ns())
    return timestamp_str

def make_results_file_name(file_name):
    timestamp = get_timestamp()
    results_file_name = file_name.split('.')[0] + '_results_' + timestamp \
            + '.json'
    return results_file_name

def download_images(google_search_term, num_images):
    response = google_images_download.googleimagesdownload()
    search_args = { \
            'limit': num_images, \
            'keywords': google_search_term, \
            'thumbnail': True, \
                # 2 second timeout when downloading images
            'socket_timeout': 2, \
                # does not print output
            'silent_mode': True, \
                # no extra image directory
            'no_directory': True, \
            }
    absolute_image_paths = response.download(search_args)
    return absolute_image_paths[0][google_search_term]


def delete_images(image_paths):
    for image in image_paths:
        if os.path.exists(image):
            os.remove(image)

def show_images(google_search_term, num_images):
    image_file_names = download_images(google_search_term, num_images)
    image_list = []
    for image_file_name in image_file_names:
        image = cv2.imread(image_file_name)
        if image is None:
            continue
        image = imutils.resize(image, height=400)
        #image.resize(image, (200, 200))
        image_list.append(image)

    collage = np.hstack(image_list)
    cv2.imshow(google_search_term, collage)
    # focus on this window
    cv2.setWindowProperty(google_search_term, cv2.WND_PROP_TOPMOST, 1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    delete_images(image_file_names)

def validate_int_from_user(user_input, min_max_tup):
    # min_max_tup is a tuple of (minimum, maximum) for the range that the user
    # input can be
    user_int = None
    try:
        user_int = int(user_input)
    except:
        print('\nThat\'s not an integer!\n')
    if not isinstance(user_int, int):
        return False
    if user_int < min_max_tup[0] or user_int > min_max_tup[1]:
        print(f'\nThat\'s outside of the bounds [{min_max_tup[0]}, ' \
                f'{min_max_tup[1]}]!\n')
        return False
    return True

def get_int_from_user(prompt, min_max_tup):
    # min_max_tup is a tuple of (minimum, maximum) for the range that the user
    # input can be
    got_int_from_user = False
    while not got_int_from_user:
        user_input = input(prompt)
        got_int_from_user = validate_int_from_user(user_input, min_max_tup)
    return int(user_input)


def get_valid_user_ranking(google_search_term):
    prompt = f'Rank {google_search_term} on a scale of -10 to 10.\nRanking: '
    return get_int_from_user(prompt, (-10, 10))

def get_seed_weight():
    prompt = f'How important do you think a team\'s seed is on a scale of 1 to ' \
            '10?\nRanking: '
    global SEED_WEIGHT
    SEED_WEIGHT = get_int_from_user(prompt, (1, 10))

def get_num_images_to_show():
    prompt = f'How many images do you want to see for each judging round?\n' \
            'The more pictures, the longer this will take.\n' \
            'Give a number between 1 and 5: '
    global NUM_IMAGES
    NUM_IMAGES = get_int_from_user(prompt, (1, 5))

def get_randomness_flag():
    prompt = f'Do you want any randomness added? 1 for yes, 0 for no.\n' \
            'Input: '
    global RANDOMNESS
    RANDOMNESS = get_int_from_user(prompt, (0, 1))

def get_logo_ranking(team_name):
    google_search_term = team_name + ' basketball logo'
    show_images(google_search_term, NUM_IMAGES)
    return get_valid_user_ranking(google_search_term)

def get_mascot_ranking(team_name):
    google_search_term = team_name + ' basketball mascot'
    show_images(google_search_term, NUM_IMAGES)
    return get_valid_user_ranking(google_search_term)

def get_funny_ranking(team_name):
    google_search_term = team_name + ' basketball funny meme'
    show_images(google_search_term, NUM_IMAGES)
    return get_valid_user_ranking(google_search_term)

def get_random_ranking(team_name):
    return random.randint(-10, 10)

def get_user_rankings(team_name):
    user_rankings = dict()
    user_rankings['logo_ranking'] = get_logo_ranking(team_name)
    user_rankings['mascot_ranking'] = get_mascot_ranking(team_name)
    user_rankings['funny_ranking'] = get_funny_ranking(team_name)
    if RANDOMNESS:
        user_rankings['random_ranking'] = get_random_ranking(team_name)
    return user_rankings

def get_final_ranking(user_ranking, seed):
    seed_ranking = (68 - seed) * SEED_WEIGHT / 10
    final_ranking = seed_ranking # base ranking
    final_ranking += sum(user_ranking.values())
    return final_ranking

def get_dict_from_json_file(json_file_name):
    json_file = open(json_file_name)
    json_dict = json.load(json_file)
    return json_dict

def get_results(teams_dict):
    results_dict = teams_dict
    for team_name in teams_dict.keys():
        team_user_rankings = get_user_rankings(team_name)
        results_dict[team_name].update(team_user_rankings)
        results_dict[team_name]['final_ranking'] = get_final_ranking( \
                team_user_rankings,
                results_dict[team_name]['seed']
                )
    return results_dict

def sort_results(results_dict):
    """ results in the format:
    <team_name>: 'final_ranking': <number>
    Sort the team_name by the final_ranking number
    """
    sorted_results = dict(sorted(results_dict.items(), key=lambda item: \
            item[1]['final_ranking'], reverse=True))
    return sorted_results

def make_results_file(teams_file_name):
    get_seed_weight()
    get_num_images_to_show()
    get_randomness_flag()
    results_file_name = make_results_file_name(teams_file_name)
    teams_dict = get_dict_from_json_file(teams_file_name)
    results_dict = get_results(teams_dict)
    results_dict = sort_results(results_dict)
    with open(results_file_name, 'w') as json_file:
        json.dump(results_dict, json_file, indent='\t') # indent with pretty
        # tabs
    print(f'Created rankings file {results_file_name}. Best teams are the ' \
            'top.\n')

def main():
    args = sys.argv[1:]
    if len(args) < 1:
        print('Usage: python rank_teams.py <teams_json>.json\n\n')
        return
    teams_file_name = args[0]
    make_results_file(teams_file_name)


if __name__ == '__main__':
    main()
