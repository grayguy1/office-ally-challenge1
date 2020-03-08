# Team Name
Members:
- Anoop Babu
- Ahsan Wahab
- Jamshidbek Mirzakhalov
- Sherzod Kariev

## Patient Matching

## Set up instructions
1. pip install -r requirements.txt
2. python app.py
3. Go to http://127.0.0.1:5000/pie

## Proof of Concept Steps
## Inspiration
We wanted to try out this challenge by using some fancy ML algorithms in NLP, but the structure of the problem was quite tricky and caught our attention.

## What it does
Showcases a dashboard where a user bring in data, pick one of the provided algorithms and a threshold to calculate the results. We make use of Levenshtein distance to compare the data as well as weighting some inputs accordingly. 

## How we built it
We use the distance calculated through Levenshtein algorithm in addition to applying different weights to certain entries (i.e. gender). We believe this weight optimization can be more efficiently performed using more complicated ML algorithms. 

## Contact info
anoopbabu@mail.usf.edu
