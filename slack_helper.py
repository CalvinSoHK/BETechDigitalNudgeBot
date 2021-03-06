#! /usr/bin/env python
# Comes from: https://github.com/dangoldin/automating-management. Some changes made.
from slackclient import SlackClient
import time
import datetime
import config


class SlackHelper:
    def __init__(self, bot_token, user_token):
        self.sc_bot = SlackClient(bot_token)
        self.sc_user = SlackClient(user_token)
        self.user_map = self.get_users_as_map()

    def get_users_as_map(self):
        users = self.sc_bot.api_call('users.list')
        users = users['members']
        user_map = {}
        for user in users:
            if not user['deleted']:
                user_map[user['profile']['real_name'].lower()] = user
        return user_map

    def get_username_for_fullname(self, fullname):
        return self.user_map[fullname.lower()]['name'].lower()

    def get_name_by_id(self, my_id):
        return [user['name'] for user in self.user_map.values() if user['id'] == my_id][0]

    def convert_date_to_unix(self, date):
        return time.mktime(datetime.datetime.strptime(date, "%m/%d/%Y %H:%M:%S").timetuple())

    def send_message(self, msg, channel, icon_url, as_user = False):
        return self.sc_bot.api_call(
            'chat.postMessage',
            as_user=as_user,
            channel=channel,
            icon_url=icon_url,
            text=msg,
            link_names=1,
            parse='full',
            )

    def schedule_reminders(self, msg, user, time):
        return self.sc_user.api_call(
            'reminders.add',
            text = msg,
            user = user,
            time = time,
            )

    def schedule_message(self, msg, channel, post_time):
        return self.sc_bot.api_call(
            'chat.scheduleMessage',
            channel = channel,
            text = msg,
            as_user = False,
            post_at = post_time,
            )

    def execute_command(self, msg, username, channel, icon_url, as_user = False):
        return self.sc_bot.api_call(
            'chat.command',
            username=username,
            as_user=as_user,
            channel=channel,
            icon_url=icon_url,
            command=msg,
            link_names=1,
            parse='full',
            )

    def get_channel_members(self, channel_filter):
        all_channels = self.sc_bot.api_call('channels.list')['channels']

        my_channel = [channel for channel in all_channels \
            if channel['name'] == channel_filter.replace('#', '')]

        if not my_channel:
            return None

        user_ids = [user['id'] for user in self.user_map.values()]

        return [user for user in my_channel[0]['members'] if user in user_ids]

    def get_emoji(self):
        return self.sc_bot.api_call(
            'emoji.list',
            )
