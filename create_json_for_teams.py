# Script to convert text file into json file for further processing.
# See teams_2022.txt for text file format.

import sys
import json

def get_team_data(line):
    # Format of "<seed>. <team name> (<record>)"
    # Example: "16. Providence (25-5)"
    line_words = line.split(' ')
    seed = line_words[0].split('.')[0]
    team_name = ' '.join(line_words[1:-1])
    print(f'Read {team_name}.\n')
    return team_name, seed


def make_team_data_dict(team_lines):
    team_data = dict()
    for line in team_lines:
        team_name, seed = get_team_data(line)
        if team_name not in team_data:
            team_data[team_name] = dict()
            team_data[team_name]['seed'] = seed
        else:
            print(f'{team_name} shows up more than once in the text file!\n')
    return team_data

def convert_txt_to_dict(txt_file_name):
    txt_file = open(txt_file_name)
    txt_file_lines = txt_file.readlines()

    return make_team_data_dict(txt_file_lines)

def make_json_file_name(txt_file_name):

    json_file_name = txt_file_name.split('.')[0] + '.json'
    return json_file_name


def create_json_file(txt_file_name):
    json_dict = convert_txt_to_dict(txt_file_name)
    json_file_name = make_json_file_name(txt_file_name)
    print(f'json file name: {json_file_name}')
    with open(json_file_name, 'w') as json_file:
        json.dump(json_dict, json_file, indent='\t') # indent with pretty tabs


def main():
    args = sys.argv[1:]
    txt_file_name = args[0]
    create_json_file(txt_file_name)

if __name__ == '__main__':
    main()
