# Note_App
#### Video Demo: https://youtu.be/_eRYiy14twg
This is a simple and minimal note app designed  using Python Tkinter library for GUI.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)


## Overview
This application is so designed to organize notes of different topics under respective subject. A user can create, save, open, edit, delete and even share note through in-built emailing system.

![image](https://github.com/user-attachments/assets/0545cde6-6a5c-4f6d-a7f3-455ef50f6265)  ![image](https://github.com/user-attachments/assets/e5389c85-2e8a-4a44-812c-abcc4cb54b21)



## Features
- Interactive GUI interface built with tkinter.
- Add and Delete subjects 
- Create, Save, Open, Edit and Delete files
- Search functionality for meanings
- Share files 
- Organize notes of each subject in their respective directory


## Requirements
- Python 3.x
- Tkinter (usually included in Python installations)
- SMTPLIB 
- nltk

## Installation
1. Create a directory:
   ```bash
   mkdir <directory_name>
   ```

2. Create a virtual environment:
   ```bash
   cd <directory_name>
   python -m venv env
   ```

3. Clone the repository:
   ```bash
   git clone <repository_url>
   ```

## Usage
1. Open a terminal or command prompt.
2. Navigate to the directory where the app files are located.
3. Activate the virtual environment: `source env/bin/activate`.
4. Install dependencies: `pip install -r requirements.txt`.
5. Run the command `cd NOTE_APP`.
6. Configure your email:
   - create .env file and add the following:
   - "EMAIL_ID" = "your host email id"
   - "PASSWORD" = "password of the email"
   
8. Run the command: `python project.py`.
9. The gui window will appear. Take your notes.
10. Stay organized.

## Contributing
Contributions are welcome! Feel free to open issues or pull requests for any improvements or bug fixes.

## License
This project is licensed under the [MIT License](LICENSE).
