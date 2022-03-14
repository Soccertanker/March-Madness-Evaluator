# March-Madness-Evaluator
Helps evaluate March Madness Men's basketball teams based on your weird criteria.

# Installation
In root directory of this repo, run the following:
```
  git clone https://github.com/Joeclinton1/google-images-download.git
  cd google-images-download && python setup.py install
```

Install requirements by running:
```
  pip install -r requirements.txt
```

# Usage
The rank_teams.py script takes as input a json file with the March Madness teams
and seeds. It then shows the user memes from each team and lets the user rank
the memes on a scale of 1 to 10. Then the script creates an output results json
file with final rankings for each team. High ranking = good

Run the following command:
```
  python3 rank_teams.py teams_2022.json
```

Find the results json file.
