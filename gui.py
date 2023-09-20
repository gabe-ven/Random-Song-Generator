import customtkinter as ctk
from customtkinter import CTkImage
import tkinter as tk
from tkinter import ttk
import tkinter.font as font
import webbrowser
from PIL import Image, ImageTk
from main import *
from settings import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BLUE)

        self.title("")
        self.iconbitmap("images/spotifyicon.ico")
        self.geometry("500x300")
        self.resizable(False, False)

        font = ctk.CTkFont(family=FONT, size=TITLE_SIZE, weight="bold")
        self.title_label = ctk.CTkLabel(
            self, text="Random Song Generator", font=font, text_color=DARK_BLUE
        )
        self.title_label.pack(pady=5)

        self.entry_frame = Entry(self)
        self.entry_frame.pack(pady=5)

    def create_song(self, genre):
        if hasattr(self, "song_frame") and self.song_frame:
            self.song_frame.destroy()

        self.song_frame = Song(self, genre)
        self.song_frame.pack(pady=20)

    def create_button(self):
        if hasattr(self, "button_frame") and self.button_frame:
            self.button_frame.destroy()

        self.button_frame = Buttons(self)
        self.button_frame.pack(expand=True, fill="both")


class Entry(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color=BLUE,
        )
        self.pack(pady=10)

        self.label = ctk.CTkLabel(
            self,
            text="Enter a genre (i.e. pop, rock, hip hop)",
            text_color=WHITE,
            font=(FONT, LABEL_SIZE),
        )
        self.label.pack()

        self.string_var = tk.StringVar()
        self.entry = ctk.CTkEntry(
            self,
            textvariable=self.string_var,
            height=30,
            width=200,
            border_width=0,
            font=(FONT, ENTRY_SIZE),
        )
        self.entry.pack(pady=10)
        self.entry.bind("<Return>", self.get_genre)

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.style.configure(
            "bar.Horizontal.TProgressbar",
            troughcolor=BLUE,
            bordercolor=BLUE,
            background=RED_ORANGE,
            lightcolor=RED_ORANGE,
            darkcolor=RED_ORANGE,
        )
        self.progress = ttk.Progressbar(
            self,
            orient="horizontal",
            length=200,
            mode="determinate",
            style="bar.Horizontal.TProgressbar",
        )

    def get_genre(self, event):
        self.genre = self.string_var.get()
        self.update_progress()

    def update_progress(self):
        current_value = self.progress["value"]
        if current_value < 100:
            new_value = current_value + 5
            self.progress["value"] = new_value
            self.progress.pack(pady=10)
            self.after(50, self.update_progress)
        else:
            self.progress.pack_forget()
            self.master.create_song(self.genre)
            self.master.create_button()
            self.master.entry_frame.pack_forget()

    def clear_entry(self):
        self.string_var.set("")


class Song(ctk.CTkFrame):
    def __init__(self, parent, genre):
        super().__init__(parent, fg_color=BLUE)
        self.pack()
        self.genre = genre
        self.song_name = ""
        self.artist_name = ""
        self.preview = ""
        self.display_info()

    def get_info(self):
        token = get_token()
        random_track = get_random_tracks_from_genre(token, self.genre)

        self.song_name = random_track["name"]
        self.artist_name = random_track["artists"][0]["name"]
        self.preview = random_track["preview"]

    def display_info(self):
        self.get_info()

        if hasattr(self, "label1"):
            self.label1.destroy()
        if hasattr(self, "label2"):
            self.label2.destroy()

        self.label1 = ctk.CTkLabel(
            self,
            text_color=GREEN,
            text=f"{self.song_name}",
            font=(FONT, INFO_SIZE, "bold"),
            wraplength=500,
        )
        self.label1.pack()
        self.label2 = ctk.CTkLabel(
            self,
            text=f"{self.artist_name}",
            font=(FONT, ARTIST_SIZE, "bold"),
            wraplength=500,
        )
        self.label2.pack()


class Buttons(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent, fg_color=BLUE)
        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1), weight=1, uniform="a")
        self.create_buttons()

    def create_buttons(self):
        if hasattr(self, "button1"):
            self.button1.destroy()
            self.button2.destroy()
            self.button3.destroy()
            self.button4.destroy()

        self.button1 = ctk.CTkButton(
            self,
            text="New Song",
            fg_color=ORANGE,
            text_color=DARK_BLUE,
            hover_color=DARK_ORANGE,
            font=(FONT, NEW_SIZE, "bold"),
            corner_radius=CORNER_RADIUS,
            command=self.update_song,
        )
        self.button1.grid(row=0, column=0, sticky="ns", padx=10, pady=15)
        self.button2 = ctk.CTkButton(
            self,
            text="▶",
            fg_color=PINK,
            text_color=DARK_BLUE,
            hover_color=DARK_PINK,
            font=(FONT, PLAY_SIZE, "bold"),
            corner_radius=CORNER_RADIUS,
            command=self.play_preview,
        )
        self.button2.grid(row=0, column=1, sticky="ns", padx=20, pady=15)
        self.button3 = ctk.CTkButton(
            self,
            text="New Genre",
            fg_color=ORANGE,
            text_color=DARK_BLUE,
            hover_color=DARK_ORANGE,
            font=(FONT, NEW_SIZE, "bold"),
            corner_radius=CORNER_RADIUS,
            command=self.update_genre,
        )
        self.button3.grid(row=0, column=2, sticky="ns", padx=10, pady=15)

        button_image = ctk.CTkImage(Image.open("images/spotify.png"), size=(30, 30))
        self.button4 = ctk.CTkButton(
            self,
            text="",
            fg_color=BLUE,
            hover_color=BLUE,
            image=button_image,
            command=self.open_spotify_link,
        )

        self.button4.grid(row=1, column=1, padx=10)

    def update_song(self):
        self.master.song_frame.display_info()

    def update_genre(self):
        self.master.song_frame.pack_forget()
        self.master.button_frame.pack_forget()
        self.master.entry_frame.clear_entry()

        # Create new Entry
        self.master.entry_frame = Entry(self.master)
        self.master.entry_frame.pack(pady=10)

    def play_preview(self):
        if self.master.song_frame.preview:
            webbrowser.open(self.master.song_frame.preview)

    def open_spotify_link(self):
        if self.master.song_frame.preview:
            parts = self.master.song_frame.preview.split("?cid=")
            track_id = parts[0].split("/")[-1]
            spotify_url = f"https://open.spotify.com/track/{track_id}"
            webbrowser.open(spotify_url)


if __name__ == "__main__":
    app = App()
    app.mainloop()
