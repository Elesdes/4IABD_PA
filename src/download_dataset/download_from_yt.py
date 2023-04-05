import asyncio

import pandas as pd
import yt_dlp as yt
from dotenv import load_dotenv

load_dotenv()

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


class YTDLSource():
    def __init__(self, source, *, data):
        super().__init__(source)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

    @classmethod
    async def from_playlist(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        filename = []
        data_file = []
        if 'entries' in data:
            for yt_file in data['entries']:
                data_file.append(yt_file)
            for yt_file in data_file:
                filename.append(yt_file['title'] if stream else ytdl.prepare_filename(yt_file))
        return filename


async def start(loop):
    df = pd.read_csv('data/done.csv', sep=",")
    for index, row in df.iterrows():
        try:
            await YTDLSource.from_url(f"{row['TITRE']}_{row['ARTISTE']}", loop=loop)
        except:
            # TODO: Que faire des erreurs de downloads?
            # Propositions: mettre les musiques problématiques dans un autre fichier
            pass


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(start(loop))
