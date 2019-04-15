#! /usr/bin/env python
# Comes from: https://github.com/dangoldin/automating-management. Some changes made.
import config
from slack_helper import SlackHelper
import sys
from datetime import datetime
import util
import time

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print ('Please specify channel and message')
        exit()

    channel_name = sys.argv[1]
    post_at = sys.argv[2]
    message = sys.argv[3]

    sh = SlackHelper(config.BOT_USER_TOKEN, config.OAUTH_USER_TOKEN)
    channel_members = sh.get_channel_members('#' + channel_name)

    count = 0

    # Below is the code for sending messages to everyone
    for member_id in channel_members:
        count += 1
        if (count == 20):
            time.sleep(65)
            count = 0
        username = sh.get_name_by_id(member_id)
        print ('Sending to {0}'.format(username))
        print (sh.schedule_reminders(
            msg=message,
            user=member_id,
            time=post_at,
        ))
