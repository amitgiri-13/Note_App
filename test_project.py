import pytest 
from project import NoteApp
import os

app = NoteApp()

def test_open_file():
    assert app.open_file("test_directory","test_file.txt") == "This is a test file."
    assert app.open_file("test_directory","test_file.docs") == "FileFormatNotSupported"
    assert app.open_file("test_directory","fake.txt") == "File not found"

def test_save_file():
    assert app.save_file("test_directory","test_file_2.txt","This is test file_2.") == "Saved successfully"
    assert app.save_file("test_directory_2","test_file_2.txt","This is test file_2.") == "Created a new directory test_directory_2" or "Saved successfully"

def test_delete_file():
    app.save_file("test_directory_2","test_file_3.txt","Deleting this...")
    assert app.delete_file("test_directory_2","test_file_3.txt") == "Deleted file successfully"
    assert app.delete_file("test_directory","fake_file.txt") == "File Not Found"
    assert app.delete_file("fake_directory","test_file.txt") == "Couldnot find that directory"

def test_find_meaning():
    assert isinstance(app.find_meaning("cat"),str)
    with pytest.raises(IndexError):
        app.find_meaning("qwerty")

def test_send_email():
    assert app.send_email("prabinpyakurel82@gmail.com","Test Case","This is a test email","test_directory/test_file.txt") == "Sent"
    assert app.send_email("","","","") == "Could not send email"