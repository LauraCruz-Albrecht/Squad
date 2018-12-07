# Squad

## Mission
Great friendships shouldn't just be happy accidents. All too often, our social lives at Stanford are determined by our freshman-year dorm mates, our classmates, and people who we meet by chance. But it doesn't have to be that way.

Introducing Squad, a friendship matching algorithm that leverages social psychology research to match you with others on the Farm who share your values and interests. Our goal: to help you find a new way to reach out of your social circle and meet the Stanford besties you never knew you had.

This repo contains the code for the Squad friendship-matching algorithm.

## Team
Laura Cruz-Albrecht, Tara Iyer, Eric Xu, Glenn Yu

Special shoutout to Glenn for the inspiration behind this project :)

## Repo details
- **squad.py**: the Squad friendship-matching algorithm. Takes questionnaire responses csv as input, and outputs csv of friend pair recommendations (3-6 recommendations per user).
- **score.py**: custom scoring utility functions leveraged by the squad algorithm.
- **indices.txt**: text file containing indices alongside each question in the google form, helpful for indexing into csv data inside squad.py.
- **create_auto_email_sheet.py**: script that takes csv of matchings produced by the squad algorithm, and generates the html and other metadata needed for sending the custom squad match emails.
- **create_auto_email_sheet_test.py**: same as create_auto_email_sheet.py, except reads from and writes to a test file.
- **Results_test.csv**: sample csv output produced by running the squad algorithm.
- **Auto_email_sheet_test.csv**: sample csv output produced by running the create_auto_email_sheet_test.py script.

## General stats
For privacy, the questionnaire form responses and matches produced by the Squad algorithm are ommitted from this repository. In total, we ran the Squad matching algorithm on 343 participants, and for each participant provided 3-6 matches, for a total of 709 matching recommendations.
