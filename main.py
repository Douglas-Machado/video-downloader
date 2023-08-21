import os
from pytube import YouTube
from dotenv import load_dotenv

load_dotenv()


class Downloader():
    def __init__(self, url, oauth=False, allow_oauth_cache=True):
        self.yt = YouTube(url=url, use_oauth=oauth, allow_oauth_cache=allow_oauth_cache)
        self.__mime_type = None
        self.__type = None
        self.__formats = []
        self.is_progressive = True


    def main(self):
        self.set_progressive()
        self.set_formats()
        self.list_formats()
        self.set_type()
        self.set_mime_type()
        video = self.yt.streams.filter(
            progressive=self.is_progressive,
            type=self.get_type(),
            file_extension=self.get_mime_type()
        ).order_by(
            'resolution'
        ).desc().first()

        path = video.download(os.getenv('DOWNLOAD_PATH'))
        print(f"Video downloaded in: {path}")


    def get_type(self):
        return self.__type


    def set_type(self):
        user_input = input("Audio or Video? (A/V)")
        if user_input in ('A', 'a'):
            self.__type = 'audio'
        elif user_input in ('V', 'v'):
            self.__type = 'video'
        else:
            self.set_type()


    def set_mime_type(self):
        m_types = []
        for format in self.get_formats():
            if format['type'] == self.get_type():
                m_types.append(format['mime_type'])
        
        for m_type in m_types:
            print(f"Extension: {m_type}")
        user_input = input("Select the extension: ")

        if user_input not in m_types:
            self.set_mime_type()

        self.__mime_type = user_input


    def get_mime_type(self):
        return self.__mime_type


    def get_formats(self):
        return self.__formats


    def set_formats(self):
        unique_formats_list = []
        for extension in [{"type": info.type, "mime_type": info.mime_type.split('/')[1]} for info in self.yt.streams]:
            if (extension) not in unique_formats_list:
                unique_formats_list.append(extension)
        self.__formats = unique_formats_list


    def list_formats(self):
        print("Available types: ")
        for extension in self.get_formats():
            print(f"type: {extension['type']} | extension: {extension['mime_type']}")


    def set_progressive(self):
        user_input = input("Separate audio and video? (Y/N)")
        if user_input in ('Y', 'y'):
            self.is_progressive = True
        elif user_input in ('N', 'n'):
            self.is_progressive = False
        else:
            self.set_progressive()


url_input = input("Video url: ")
downloader = Downloader(url_input)
downloader.main()
