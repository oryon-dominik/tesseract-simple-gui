#!/usr/bin/env python3
# coding: utf-8

"""
Tesseract-GUI, a very simple graphical User Interface for the OCR-Software Tesseract
A seperate tesseract installation is required.
See: https://github.com/tesseract-ocr/tesseract

This script is licensed under the revised BSD License (see LICENSE)
Copyright (c) 2019-present Dominik Geldmacher <oryon@cyberise.de>
All rights reserved.

"""

__version__ = "0.1.3"
__author__ = "oryon/dominik"
__date__ = "March 12, 2019"
__updated__ = "August 8, 2020"


"""
# Windows-Users (outside of their virtualenvironment):
# If you've installed pyinstaller, you can use it to create your own executable
pyinstaller.exe --onefile --icon=tss_simple.ico --clean tss_simple.py
"""

import os
import subprocess
from pathlib import Path
import json
import shutil

import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext


class TesseractGUI(tk.Frame):

    status = None
    tesseract = None

    def __init__(self, master=None):
        super().__init__(master)
        self.parent = master
        self.filename = None
        self.text = "Optical character recognition from image to text via 'Tesseract'\nOutput-File will be created as .txt in the same folder as origin"
        self.language, self.encoding = self.get_language_encoding()
        self.status = self.set_status()
        self.selected = tk.StringVar()
        self.init_ui()

    def init_ui(self):
        # Set-up basics
        self.parent.title("Tesseract Simple GUI")
        self.parent.geometry(f"{380}x{550}")
        try:
            self.parent.wm_iconbitmap("tss_simple.ico")
        except tk.TclError:
            # just skip the icon
            pass
        # Set-up Grid-Geometry
        self.configure_grid()
        # Populate the Grid
        self.create_widgets()
        self.widget_geometry()

    def configure_grid(self):
        # Create underlying frames
        self.instructions = tk.Frame(
            master=self.parent, bg="snow", bd=2, relief=tk.GROOVE
        )
        self.buttons = tk.Frame(master=self.parent, bg="snow", bd=2, relief=tk.RIDGE)
        self.textbox = tk.Frame(master=self.parent, bg="snow", bd=2, relief=tk.GROOVE)
        self.statusbar = tk.Frame(
            master=self.parent, bg="snow", bd=2, relief=tk.GROOVE, height=12
        )
        # Configure 'em
        self.instructions.pack(fill=tk.X, padx=2, pady=2)
        self.buttons.pack(padx=2, pady=0, anchor=tk.CENTER)
        self.textbox.pack(fill=tk.BOTH, padx=2, pady=2, expand=True)
        self.statusbar.pack(fill=tk.X, padx=2, pady=2)

    def create_widgets(self):
        self.instruction_label = tk.Label(master=self.instructions, text=self.text)
        self.button_choice = tk.Button(
            master=self.buttons, text="Choose File", command=self.choose_file, width=12
        )
        self.file_name_label = tk.Entry(
            master=self.buttons,
            state="disabled",
            exportselection=0,
            width=24,
            textvariable=self.selected,
        )
        self.button_convert = tk.Button(
            master=self.buttons, text="OCR", command=self.convert, width=12
        )
        self.output = scrolledtext.ScrolledText(master=self.textbox)
        self.output.insert(tk.END, "Converted text will display here")
        self.status_label = tk.Label(
            master=self.statusbar, text=self.status, anchor="w"
        )

    def widget_geometry(self):
        self.instruction_label.pack(fill=tk.BOTH, padx=2, pady=2, expand=True)
        self.button_choice.pack(
            side="left", padx=2, pady=2, ipadx=2, ipady=2, anchor=tk.CENTER
        )
        self.file_name_label.pack(
            side="left",
            padx=10,
            pady=2,
            ipadx=2,
            ipady=2,
            expand=True,
            anchor=tk.CENTER,
        )
        self.button_convert.pack(
            side="left", padx=2, pady=2, ipadx=2, ipady=2, anchor=tk.CENTER
        )
        self.output.pack(fill=tk.BOTH, padx=2, pady=2, expand=True)
        self.status_label.pack(fill=tk.BOTH, padx=2, pady=2, expand=True)

    def get_status(self, fallback_status=None):
        if self.status is None:
            # Initializing..
            # TODO: check for issues & errors and display here
            if shutil.which("tesseract") is None:
                self.status = "Status: Did not find a valid Tesseract Installation"
                self.tesseract = False
                return self.status
            elif shutil.which("tesseract") is not None:
                self.tesseract = True
            self.status = "Status: Waiting for file"
            return self.status
        else:
            # if lang.json is not found, this get's called before init
            try:
                self.status = self.status_label["text"]
            except AttributeError:  
                self.status = fallback_status
            return self.status

    def set_status(self, status=None):
        """ displays self.status in statusbar """
        if status is None:
            return self.get_status()
        else:
            try:
                self.status_label.config(text=str(status))
            except AttributeError:
                self.get_status(fallback_status=status)
            return self.get_status()

    def choose_file(self):
        """ tkinter file-dialog """
        self.filename = None
        self.filename = filedialog.askopenfilename(
            initialdir=".",
            title="Select file",
            filetypes=(
                ("Image Files", "*.png *.jpg *.jpeg *.tiff"),
                ("All Files", "*.*"),
            ),
        )
        if self.filename:
            self.set_status("File selected")  # TODO: check for file validity
            short_fhandle = str(self.filename).split(os.path.sep)[-1]
            self.selected.set(short_fhandle)
        else:
            self.set_status("Please select a file")

    def get_language_encoding(self, _file="lang.json"):
        """ reads language file from disk """

        folder = os.getcwd()
        seperator = os.path.sep

        file_path = Path(f"{folder}{seperator}{_file}")

        if not file_path.exists() or not file_path.is_file():
            self.set_status("Language-File not found - using english")
            return "eng", "utf-8"

        else:
            with open(file_path, "r") as f:
                try:
                    settings = json.load(f)
                    return settings["language"], settings["encoding"]

                except Exception as e:
                    self.set_status(f"Language-File Importing-Error {e} - using english & utf-8")
                    return "eng", "utf-8"

    def convert(self):
        """ executes tesseract OCR """
        if self.filename and self.tesseract:
            error = False
            self.set_status("OCR executing, please wait..")

            try:
                # $ tesseract inputfilename outputfile -l language
                outputname = self.filename[:-4] + "_ocr"
                process = []
                process.append("tesseract")
                process.append(self.filename)
                process.append(outputname)
                process.append("-l")
                process.append(self.language)

                subprocess.run(
                    process, stdout=subprocess.DEVNULL
                )  # TODO: catch output and exceptions

                scanned_text = self.read_text(f"{outputname}.txt")

                self.output.delete("1.0", tk.END)
                self.output.insert(tk.END, scanned_text)

                if not error:
                    self.set_status("Image converted succesfully")

                elif error:
                    self.set_status("Error with text recognition")

            except Exception as e:
                error = True
                self.set_status(f"Error: {e}")
        else:
            if not self.tesseract:
                self.set_status("No Tesseract Installation found - can't convert image")
            if not self.filename:
                self.set_status("Choose a File to convert")

    def read_text(self, file_name):
        with open(file_name, "r", encoding=self.encoding) as _file:
            try:
                text = _file.read()
                return str(text).lstrip()
            except Exception as e:
                return f"Text-File Importing-Error: {e}"


def main():
    root = tk.Tk()
    app = TesseractGUI(root)
    app.mainloop()


if __name__ == "__main__":
    main()
