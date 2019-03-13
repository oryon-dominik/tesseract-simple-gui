# Tesseract simple GUI

A very simple graphical User Interface for the OCR-Software [Tesseract](https://github.com/tesseract-ocr/tesseract) written in Python
The pure purpose is to convert images to .txt files via GUI - no special cases are adressed. Feel free to request features though.

## Installation

Windows Users can download the [executable](https://github.com/oryon-dominik/tesseract_simple_gui/blob/master/tss_simple.exe) and run the program as a standalone.
Other OSs have to compile for themselves or just use the script.

A valid installation of tesseract in your path-environment is required.
You may follow the installation-instructions in the tesseract repository.

Windows Users may use a [Windows-Installer](https://github.com/UB-Mannheim/tesseract/wiki).
On 64-bit Windows and Tesseract-Version 4.0.0 the installation directory is `<Your Users Home>\AppData\Local\Tesseract-OCR`,
click [here](https://www.architectryan.com/2018/03/17/add-to-the-path-on-windows-10/) for a tutorial on how-to modify your windows-10 PATH accordingly or modify the powershell-commands below for your needs:

```powershell
$user_env = [Environment]::GetEnvironmentVariable("PATH", "User")
$tesseract_path = "C:\Users\<username>\AppData\Local\Tesseract-OCR"
[Environment]::SetEnvironmentVariable("PATH", "$user_env;$tesseract_path", "User")
```

## Usage

Should be pretty self-explanatory:

- Import a file with "Choose File"
- Click "OCR"
- A text file has been created in your images directory, you can also copy the text directly from the GUI

## Languages

Modify or create the file `lang.json` in the executables directory with the language abbreviation and the encoding (see example) you want to use.
Obviously the language has to be already installed with tesseract. (Check for `.traineddata`-files in `...\Tesseract-OCR\tessdata`)

Example `lang.json`:

```lang.json
{
    "language": "eng",
    "encoding": "utf-8"
}
```
