from pytube import YouTube
from customtkinter import *
from tkinter import messagebox
from time import sleep
import sys
import os
from requests import get, status_codes


class YoutubeDowloader:
    def __init__(self):
        self.videos_streams = []
        self.audio_streams = []
        self.window = CTk()
        self.window.geometry("685x800")
        self.window.resizable(False, False)
        self.window.title("Z_OxO YTB DOWNLOADER")
        try:
            if getattr(sys, "frozen", False):
                # Check if pyinstaller froze .exe
                executable_dir = sys._MEIPASS
            else:
                executable_dir = os.path.dirname(os.path.abspath(__file__))

            self.audio_path = os.path.join(executable_dir, "Audio")
            self.videos_path = os.path.join(executable_dir, "Videos")
            self.icon_path = os.path.join(executable_dir, "icon\YTBDownloader.ico")
        except Exception as e:
            messagebox.showerror(title="Error", message=e)
        self.window.iconbitmap(self.icon_path)

    def main_window(self):
        self.url = CTkEntry(
            self.window,
            height=100,
            width=635,
            placeholder_text="ENTER YOUTUBE VIDEO URL",
            font=("", 15),
        )
        self.url.grid(row=0, column=1, sticky="s", pady=10, padx=25)
        CTkButton(
            self.window,
            width=635,
            height=20,
            text="Submit",
            command=self.create_download_button,
        ).grid(
            row=1,
            column=1,
            sticky="s",
            pady=10,
            padx=25,
        )
        CTkLabel(
            self.window,
            width=635,
            height=100,
            text="Downloads :",
            font=("", 35),
        ).grid(
            row=2,
            column=1,
            sticky="s",
            pady=5,
            padx=5,
        )
        self.mp3Frame = CTkFrame(self.window, width=300, height=300)
        self.mp4Frame = CTkFrame(self.window, width=300, height=300)
        self.mp3Frame.grid(row=3, column=1, sticky="ne", padx=10, pady=5)
        self.mp4Frame.grid(row=3, column=1, sticky="nw", padx=10, pady=5)
        CTkButton(
            self.window,
            text="Open Videos output folder",
            width=100,
            height=20,
            command=lambda: os.startfile(self.videos_path),
        ).grid(column=1, row=4, sticky="nw", padx=70, pady=10)
        CTkButton(
            self.window,
            text="Open output Audio folder",
            width=100,
            height=20,
            command=lambda: os.startfile(self.audio_path),
        ).grid(column=1, row=4, sticky="ne", padx=85, pady=10)
        self.window.mainloop()

    def filter_stream(self):

        self.videos_streams_sure = self.streams.filter(progressive=True)
        for stream in self.streams:
            if stream.type == "video" and stream not in self.videos_streams_sure:
                self.videos_streams.append(stream)
            elif stream.mime_type == "audio/webm":
                self.audio_streams.append(stream)
        self.videos_streams = sorted(
            self.videos_streams, key=lambda x: int(x.resolution[:-1]), reverse=True
        )

    def reset_all(self):
        for widget in self.window.winfo_children():
            widget.destroy()
        self.main_window()

    def reset_frame_download(self):
        for widget in self.mp3Frame.winfo_children():
            widget.destroy()
        for widget in self.mp4Frame.winfo_children():
            widget.destroy()
        self.videos_streams, self.audio_streams, self.videos_streams_sure = [], [], []
        self.window.update()

    def create_download_button(self):
        self.reset_frame_download()
        try:
            print(get(self.url.get()).status_code)
            if get(self.url.get()).status_code != 200:
                messagebox.showerror(
                    title="Z_OxO YTB DOWNLOADER",
                    message="Invalid URL , please check if the url is valid",
                )
                self.reset_all()
                return
        except Exception as e:
            messagebox.showerror(
                title="Z_OxO YTB DOWNLOADER",
                message=f"Invalid URL : {e}]",
            )
            self.reset_all()
            return
        self.yt = YouTube(self.url.get())
        self.streams = self.yt.streams
        self.filter_stream()

        def download(stream, button):
            button.configure(text="Download in progress ...", fg_color="gray")
            self.window.update()
            sleep(0.5)
            try:
                if "audio" in stream.type:

                    stream.download(
                        output_path=self.audio_path,
                        filename=(
                            f"{stream.title} {stream.abr}.mp3"
                            if not os.path.exists(rf"{self.audio_path}\{stream.title}")
                            else f"{stream.title} {stream.abr} (1).mp3"
                        ),
                    )
                else:
                    stream.download(
                        output_path=self.videos_path,
                        filename=(
                            f"{stream.title} {stream.resolution} {stream.type}.mp4"
                            if not os.path.exists(rf"{self.videos_path}\{stream.title}")
                            else f"{stream.title} {stream.resolution} {stream.type} (1).mp4"
                        ),
                    )
                button.configure(
                    text="Succesfully download ",
                    fg_color="green",
                    hover_color="green",
                )
                if stream.resolution == "1080p":
                    messagebox.showwarning(
                        title="MP4 DOWNLOAD",
                        message="1080p video might be broke , blame Youtube API",
                    )
            except Exception as e:
                button.configure(text=f"Error :{e} ")
                sleep(2)
                button.configure(
                    text=f"{stream.mime_type} - {stream.abr} - {stream.type} - {stream.filesize_mb}",
                )

        try:
            for stream in self.videos_streams_sure:
                button = CTkButton(
                    self.mp4Frame,
                    width=260,
                    height=25,
                    text=f"{stream.mime_type} - {stream.resolution} - {stream.type} - {stream.filesize_mb} MB (SURE DOWNLOAD)",
                )
                button.configure(
                    command=lambda stream=stream, button=button: download(
                        stream, button
                    ),
                )
                button.pack(padx=10, pady=2)

            for stream in self.videos_streams:
                button = CTkButton(
                    self.mp4Frame,
                    width=260,
                    height=25,
                    text=f"{stream.mime_type} - {stream.resolution} - {stream.type} - {stream.filesize_mb} MB",
                )
                button.configure(
                    command=lambda stream=stream, button=button: download(
                        stream, button
                    ),
                )
                button.pack(padx=10, pady=2)
            for audio_stream in self.audio_streams:
                button = CTkButton(
                    self.mp3Frame,
                    width=260,
                    height=25,
                    text=f"{audio_stream.mime_type} - {audio_stream.abr} - {audio_stream.type} - {audio_stream.filesize_mb} MB",
                )
                button.configure(
                    command=lambda stream=audio_stream, button=button: download(
                        stream, button
                    ),
                )
                button.pack(pady=1, padx=5)

        except Exception as e:
            print("An error occurred:", str(e))
        self.window.update()


ytbd = YoutubeDowloader()
ytbd.main_window()
