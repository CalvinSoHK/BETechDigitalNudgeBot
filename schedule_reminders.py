#! /usr/bin/env python
# Comes from: https://github.com/dangoldin/automating-management. Some changes made.
import config
from slack_helper import SlackHelper
import sys
from datetime import datetime
import util

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Please specify channel and message'
        exit()

    channel_name = 'general'
    post_at = sys.argv[1]
    message = sys.argv[2]

    sh = SlackHelper(config.SLACK_TOKEN, config.OTHER_TOKEN)
    channel_members = sh.get_channel_members('#' + channel_name)
    time = sh.convert_date_to_unix(post_at)

    # Below is the code for sending messages to everyone
    for member_id in channel_members:
        username = sh.get_name_by_id(member_id)
        print ('Sending to {0}'.format(username))
        print (sh.schedule_reminders(
            msg=message,
            user=member_id,
            time=time,
        ))