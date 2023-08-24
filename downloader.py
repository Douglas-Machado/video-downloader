from pytube import YouTube


class Downloader:
    def __init__(self, url, oauth=False, allow_oauth_cache=True):
        self.yt = YouTube(url=url, use_oauth=oauth, allow_oauth_cache=allow_oauth_cache)
        self.__mime_type = None
        self.__type = None
        self.__formats = []
        self.__is_progressive = True
        self.__resolution = None
        self.__path = './'

    def download(self):
        video = (
            self.yt.streams.filter(
                progressive=self.get_progressive(),
                type=self.get_type(),
                file_extension=self.get_mime_type(),
                res=self.get_resolution()
            )
            .order_by("resolution")
            .desc()
            .first()
        )

        path = video.download(self.get_path())
        print(f"Video downloaded in: {path}")

    def get_path(self):
        return self.__path

    def set_path(self, path):
        self.__path = path

    def get_resolution(self):
        return self.__resolution

    def set_resolution(self, resolution):
        self.__resolution = resolution

    def get_type(self):
        return self.__type

    def set_type(self, type):
        self.__type = type

    def set_mime_type(self, mime_type):
        self.__mime_type = mime_type

    def get_mime_type(self):
        return self.__mime_type

    def get_formats(self):
        return self.__formats

    def set_formats(self):
        self.__formats = self.yt.streams.filter(progressive=self.get_progressive())

    def get_progressive(self):
        return self.__is_progressive

    def set_progressive(self, input: bool):
        if input == "Y":
            self.__is_progressive = False
        else:
            self.__is_progressive = True
