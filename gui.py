import os
import PySimpleGUI as sg
from downloader import Downloader

layout = [
    [sg.Text("Welcome to the Video Downloader!", key="container")],
    [sg.Text("Paste the link down below")],
    sg.Input(key="input"),
    sg.Button("Ok", size=(12, 2), mouseover_colors=("blue",)),
]

WD = os.getcwd()


def create_layout(texts, options, inputs=None, size=(640, 480), file_browse=None):
    sg.theme("DarkBlue4")
    layout = [texts, inputs, options]
    if not inputs:
        layout = [texts, options]

    if file_browse:
        return sg.Window(
            file_browse,
            title="Video Downloader",
            layout=layout,
            finalize=True,
            font=("Bahnschrift SemiBold Condensed",),
            size=size,
        )
    return sg.Window(
        title="Video Downloader",
        layout=layout,
        finalize=True,
        font=("Bahnschrift SemiBold Condensed",),
        size=size,
    )


window = create_layout(
    texts=[layout[0], layout[1]], inputs=[layout[2]], options=[layout[3]]
)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    if event == "Ok" and not values["input"]:
        continue

    try:
        downloader = Downloader(values["input"])
    except Exception as ex:
        window.extend_layout(window, [[sg.Text("Invalid link", text_color="red")]])
        continue

    window.close()
    window = create_layout(
        texts=[[sg.Text("Separate audio and video?")]],
        options=[sg.Button("Y", size=(12, 2)), sg.Button("N", size=(12, 2))],
    )
    event, values = window.read()
    downloader.set_progressive(event)
    downloader.set_formats()
    formats = downloader.get_formats()
    window.close()

    options = None
    if downloader.get_progressive() == True:
        options = [
            [
                sg.Button(
                    f"type: {extension.type} extension: {extension.mime_type} resolution: {extension.resolution}",
                    border_width=5,
                )
            ]
            for extension in formats
        ]
    else:
        options = sg.Listbox(
            [
                f"type: {extension.type} extension: {extension.mime_type} resolution: {extension.resolution}"
                if extension.type == "video"
                else f"type: {extension.type} extension: {extension.mime_type}"
                for extension in formats
            ],
            size=(40, 15),
        )

    window = create_layout(
        texts=[sg.Text("Available formats")],
        inputs=[options],
        options=[sg.Button("Ok", size=(12, 2), mouseover_colors=("blue",))],
    )
    event, values = window.read()
    dados = values[0][0].split()
    downloader.set_type(dados[1])
    downloader.set_mime_type(dados[3].split("/")[1])
    if downloader.get_type() == "video":
        downloader.set_resolution(dados[5])

    window.close()
    window = create_layout(
        texts=[[sg.Text("Choose a folder: ")]],
        inputs=[sg.Input(key="IN2", enable_events=True)],
        options=[sg.FolderBrowse(initial_folder=WD), sg.Button("Submit")],
    )
    event, values = window.read()
    downloader.set_path(values["Browse"])
    path = downloader.download()
    window.extend_layout(window, [[sg.Text(f"path: {path}", text_color="cyan")]])
    print("hello")
    break

window.close()
