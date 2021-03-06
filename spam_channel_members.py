#! /usr/bin/env python
# Comes from: https://github.com/dangoldin/automating-management. Some changes made.
import config
from slack_helper import SlackHelper
import sys
from datetime import datetime

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Please specify channel and message'
        exit()

    channel_name = sys.argv[1].replace('#', '')
    message = sys.argv[2]


    sh = SlackHelper(config.SLACK_TOKEN, config.OTHER_TOKEN)
    channel_members = sh.get_channel_members('#' + channel_name)

    # Below is the code for sending messages to everyone
    for member_id in channel_members:
        username = sh.get_name_by_id(member_id)
        print 'Sending to {0}'.format(username)
        print sh.send_message(
            msg=message,
            as_user=True,
            channel=member_id,
            icon_url=None,
        )

    # for member_id in channel_members:
    #     print sh.set_reminder(
    #         reminder = message,
    #         date = date,
    #         user_id = member_id,
    #         )

