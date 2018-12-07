import os
import re
import csv
import math
import pandas as pd
import numpy as np

'''
create_auto_email_sheet.py
--------------------------
this file reads in the Responses_final.csv and outputs a sheet
properly formatted for auto-email sending with google sheets.

Each row contains two columns:
- recipients: the two recipient emails, comma-separated
- names: 'firstname1 and firstname2'
- message: the html formatted message, with the custom names and blurbs


    recipients, names, message
    p1@, p2@  , Bob and Sally, <html msg>
    ...

Resource to auto-send from sheets:
https://developers.google.com/apps-script/articles/sending_emails
'''

# Source file with matching results
RESULTS_CSV = 'Results_final.csv'

# Destination file to write the auto email sheet
DEST_CSV = 'Auto_email_sheet.csv'

FORM_URL = 'https://docs.google.com/forms/d/e/1FAIpQLSfTbME3RNBvIS72547_0wYmlJalA5cmyhjUaER94MnM90RaEg/viewform'

HTML_MESSAGE_BASE = "<div dir='ltr'> Hey %s and %s,&nbsp;<div>&nbsp;</div>" + \
                    "<div>Hope you're both having a fantastic week! We want to thank you so much again for filling out the Squad form and we are so excited to announce that you two are a......</div>" + \
                    "<div>&nbsp;</div><div><div><img class='CToWUd a6T' style='display: block; margin-left: auto; margin-right: auto;' tabindex='0'src='https://ci5.googleusercontent.com/proxy/-t_uTssMDAzIi2p9e-f780d-Yb07BPCjPZmIq2b-H9YWZ4tlJ_XLy1xLEBXyORi5B2XjGrbQq5KHR_l7BWa435FaxWHDP1CNIuQgEXa7u2mUrBvshFqYHMv-MpliphGc7zRBMWA-Mjglri1z=s0-d-e1-ft#https://media1.tenor.com/images/0d2e4ada3b4bb2d3367a7fb052f6f862/tenor.gif?itemid=5620712' alt='Fire Match GIF - Fire Match Cartoon GIFs' width='218' height='158' /></div></div><div>&nbsp;</div>" + \
                    "<div style='text-align: center;''><span style='color: #ff0000; font-size: xx-large;'><strong>MATCH!!!!!</strong></span></div><div>&nbsp;</div>" + \
                    "<div>So go ahead and start scheduling a time to get to know each other -- over a meal, walk, or maybe even...p-set. We know it's Week 9 (yeah we're sad too), but it'd be great <span style='color: #000000;'>if the both of you could try to meet up sometime this week or as soon as&nbsp;you can. " + \
                    "We'd love to hear how it goes; as a reminder, we'll be giving out either a Starbucks or a Coupa gift card to the first 20 (and possibly more!) people who meet up&nbsp;by next Tuesday, Dec. 4th&nbsp;:)&nbsp;</span></div><div>&nbsp;</div>" + \
                    "<div>Here are your blurbs before you start stalking each other:</div><div>&nbsp;</div>" + \
                    "<div>%s: %s</div>" + \
                    "<div>%s: %s</div>" + \
                    "<div>&nbsp;</div><div><span style='color: #000000;'>All you have to do to be eligible for a gift card is send us a picture of the two of you from your meet-up " + \
                    "and fill out this short&nbsp;<a href='" + FORM_URL + "'><strong>feedback form</strong></a>&nbsp;(where you will upload your picture!) about this specific match. " + \
                    "Of course, you can meet up for pure, good, un-capitalistic reasons as well (though we'd still appreciate you filling out the short feedback form).</span></div><div>&nbsp;</div><div>" + \
                    "<span style='color: #000000;'>We know that friendships take time to develop,&nbsp;but we're thrilled that we could help you two connect.&nbsp;We hope this will be the start of an incredible new friendship!</span></div><div>&nbsp;</div><div>" + \
                    "<div>Also, please check your Spam folder - it's possible some of your other matches may have gone there, and you won't want to miss them!</div><div>&nbsp;</div>" + \
                    "<span style='color: #000000;'>- The Squad team</span></div></div>"

def create_auto_email_sheet():
    '''
    Reads in the Responses_final.csv and writes a csv properly formatted 
    for auto-email sending with google sheets.

    Each row contains two columns:
    - recipients: the two recipient emails, comma-separated
    - message: the html formatted message, with the custom names and blurbs


        recipients, names, message
        p1@, p2@ , Bob and Sally, <html msg>
        ...

    Arguments:
        None

    Returns:
        None
    '''

    with open(DEST_CSV, mode='w') as f:
        csv_writer = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        # write header
        header = ['recipients', 'names', 'message']
        csv_writer.writerow(header)

        # open results file to read from
        df = pd.read_csv(RESULTS_CSV)

        for index, row in df.iterrows():
            name1, email1, blurb1 = row['name1'], row['email1'], row['blurb1']
            name2, email2, blurb2 = row['name2'], row['email2'], row['blurb2']

            fullname1 = ' '.join([n.capitalize() for n in name1.split()])
            fullname2 = ' '.join([n.capitalize() for n in name2.split()])

            firstname1 = fullname1.split()[0]
            firstname2 = fullname2.split()[0]

            recipients = '%s,%s' % (email1, email2)  # emails, comma-separated
            names = '%s and %s' % (firstname1, firstname2)
            message = HTML_MESSAGE_BASE % (firstname1, firstname2, fullname1, blurb1, fullname2, blurb2)

            csv_writer.writerow([recipients, names, message])

create_auto_email_sheet()
