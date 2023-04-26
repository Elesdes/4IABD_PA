import asyncio

import pandas as pd
import yt_dlp as yt

yt.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'outtmpl': "music_raw/%(title)s.%(ext)s",
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
        'preferredquality': '192',
    }],
    'noplaylist': False,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'restrictfilenames': False,
    'default_search': 'auto',
    'source_address': '0.0.0.0'  # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}
ytdl = yt.YoutubeDL(ytdl_format_options)


class YTDLSource:
    def __init__(self, data):
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, music_name, loop=None):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None,
                                          lambda: ytdl.extract_info(music_name))
        if 'entries' in data:
            data = data['entries'][0]
        filename = ytdl.prepare_filename(data)
        return filename


async def start(loop):
    df = pd.read_csv('data/scraped/complete_kaggle_dataset.csv')
    for row in df.values:
        try:
            await YTDLSource.from_url(music_name=f"{row['track_name']}_{row['artist_name']}",
                                      loop=loop)
        except Exception as e:
            # TODO: Que faire des erreurs de downloads?
            # Propositions: mettre les musiques problématiques dans un autre fichier
            pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop))
