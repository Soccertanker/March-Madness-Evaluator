# Allows user to rank teams and get a results json file
#import pdb; pdb.set_trace()

import cv2
import imutils
import numpy as np

import json
import os
import sys
import time

from google_images_download import google_images_download

NUM_IMAGES = 1

def get_timestamp():
    curr_time_struct = time.localtime()
    timestamp_str = time.strftime('%X', curr_time_struct)
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

def get_user_ranking(google_search_term):
    # TODO 
    return 10

def get_logo_ranking(team_name):
    google_search_term = team_name + ' basketball logo'
    print(f'\n\nEvaluate the {google_search_term} images and rank them between '
            '1 and 10.\n')
    show_images(google_search_term, 5)
    return get_user_ranking(google_search_term)


def get_mascot_ranking(team_name):
    google_search_term = team_name + ' basketball mascot'
    print(f'\n\nEvaluate the {google_search_term} images and rank them between '
            '1 and 10.\n')
    show_images(google_search_term, 5)
    return get_user_ranking(google_search_term)

def get_funny_ranking(team_name):
    google_search_term = team_name + ' basketball funny meme'
    print(f'\n\nEvaluate the {google_search_term} images and rank them between '
            '1 and 10.\n')
    show_images(google_search_term, NUM_IMAGES)
    return get_user_ranking(google_search_term)

def get_random_ranking(team_name):
    return 111

def get_user_rankings(team_name):
    user_rankings = dict()
    #user_rankings['logo_ranking'] = get_logo_ranking(team_name)
    #user_rankings['mascot_ranking'] = get_mascot_ranking(team_name)
    user_rankings['funny_ranking'] = get_funny_ranking(team_name)
    user_rankings['random_ranking'] = get_random_ranking(team_name)
    return user_rankings

def get_final_ranking(user_ranking, seed):
    # TODO
    return 50

def get_dict_from_json_file(json_file_name):
    json_file = open(json_file_name)
    json_dict = json.load(json_file)
    return json_dict

def get_results(teams_dict):
    results_dict = teams_dict
    for team_name in teams_dict.keys():
        team_user_rankings = get_user_rankings(team_name)
        results_dict[team_name].update(team_user_rankings)
        results_dict[team_name]['final ranking'] = get_final_ranking( \
                team_user_rankings,
                results_dict[team_name]['seed']
                )
    return results_dict

def make_results_file(teams_file_name):
    results_file_name = make_results_file_name(teams_file_name)
    teams_dict = get_dict_from_json_file(teams_file_name)
    results_dict = get_results(teams_dict)
    with open(results_file_name, 'w') as json_file:
        json.dump(results_dict, json_file, indent='\t') # indent with pretty
        # tabs
    print(f'Created rankings file {results_file_name}. HIGHEST \'final '
            'ranking\' is the best.')

def main():
    args = sys.argv[1:]
    teams_file_name = args[0]
    make_results_file(teams_file_name)


if __name__ == '__main__':
    main()
