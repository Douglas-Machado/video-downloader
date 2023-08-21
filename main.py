from pytube import YouTube

user_input = input("Video url: ")
yt = YouTube(user_input, use_oauth=False, allow_oauth_cache=True)

try:
    video = yt.streams.filter(
    progressive=True,
    file_extension='mp4'
    ).order_by(
        'resolution'
    ).desc().first()

    path = video.download('D:/downloads')
    print(f"Video downloades in: {path}")
except Exception as ex:
    print(ex.args[0])
