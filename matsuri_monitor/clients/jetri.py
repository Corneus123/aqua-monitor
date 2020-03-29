import multiprocessing as mp

import pandas as pd
import requests

from matsuri_monitor import chat

CHANNEL_ENDPOINT = 'https://storage.googleapis.com/vthell-data/channels.json'
LIVE_ENDPOINT = 'https://storage.googleapis.com/vthell-data/live.json'


class Jetri:

    def __init__(self):
        channels = requests.get(CHANNEL_ENDPOINT).json()['channels']
        self._lock = mp.Lock()
        self.channels = pd.DataFrame.from_records(channels, index='id')
        self.lives = pd.DataFrame(index=pd.Series(name='id'), columns=['title', 'type', 'startTime', 'channel'])

    def update(self):
        """Re-accesses jetri endpoints and updates active lives"""
        lives = requests.get(LIVE_ENDPOINT).json()

        with self._lock:
            to_concat = []
            for chid, records in lives.items():
                channel_lives = pd.DataFrame.from_records(
                    records, index='id', columns=['id', 'title', 'type', 'startTime']
                )
                channel_lives['channel'] = chid
                to_concat.append(channel_lives)

            self.lives = pd.concat(to_concat)

    @property
    def currently_live(self):
        """Returns IDs of currently live streams"""
        return self.lives[self.lives['type'] == 'live'].index.tolist()
    
    def get_channel_info(self, channel_id: str):
        """Returns a ChannelInfo object for the given channel ID"""
        return chat.ChannelInfo(
            id=channel_id,
            name=self.channels.loc[channel_id]['name'],
            thumbnail_url=self.channels.loc[channel_id]['thumbnail'],
        )

    def get_live_info(self, video_id: str):
        """Returns a VideoInfo object for the given video ID"""
        return chat.VideoInfo(
            id=video_id,
            title=self.lives.loc[video_id]['title'],
            channel=self.get_channel_info(self.lives.loc[video_id]['channel']),
        )