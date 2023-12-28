from tkinter import *
from tkinter import ttk,filedialog
import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import email_configure
import nltk
from tkinter import font,colorchooser



class NoteApp:
    def __init__(self):
        self.subjects = []
        self.set_subject()

    def open_file(self,directory,filename):
        path = f"./{directory}/{filename}"
        extension = filename.split('.')[-1]
        if extension == 'txt':
            try:
               with open(path,mode="r",encoding="utf-8") as file:
                    text = file.read()
                    return text

            except FileNotFoundError:
                return 'File not found'
        
        else:
            return "File Format Not Supported"

    def save_file(self,directory,filename,text_content):
        try:
            path=f'./{directory}/{filename}'
            with open(path,mode='a',encoding='utf-8') as file:
                file.write(text_content)
                return 'Saved successfully'

        except:
            os.makedirs(f'./{directory}')
            self.save_file(directory,filename,text_content)
            return f'Created a new directory {directory}'
    
    def delete_file(self,directory,filename):
        try:
            file_path=f'./{directory}/{filename}'
            if os.path.exists(f'./{directory}'):
                    if os.path.exists(file_path):
                        os.remove(file_path)
                        return 'Deleted file successfully'
                    else:
                        return 'File Not Found'
            else:
                return "Couldnot find that directory"
        except:
            return 'Deletion Unsuccessful'
    
    def set_subject(self): 
        subjects=self.open_file('subject','subject.txt')
        self.subjects = []
        for subject in subjects.split("\n"):
            if subject not in self.subjects:
               self.subjects.append(subject)
        self.subjects.pop()

    def find_meaning(self,word):
        meanings = nltk.corpus.wordnet.synsets(word)
        #for meaning in meanings:
           #print(f"Meaning: {meaning.definition()}")
        return (meanings[0].definition())
        
    def send_email(self,receiver,subject,body,filepath):
        try:
            message = MIMEMultipart()
            message['From'] = email_configure.email_id
            message['To'] = receiver
            message['Subject'] = subject
            message.attach(MIMEText(body,'plain'))

            with open(filepath,mode='rb') as attachment:
                part= MIMEApplication(attachment.read(), Name=filepath.split('/')[-1])
                
            message.attach(part)


            with smtplib.SMTP('smtp.gmail.com',587) as server:
                server.starttls()
                server.login(email_configure.email_id,email_configure.password)
                server.send_message(message)
                return 'Sent'
        except:
            return "Couldnot send an email"

class NoteAppGUI(NoteApp):
    def __init__(self,root):

        self.root = root
        super().__init__()
        self.root.title('Keep Notes')
        self.root.geometry('960x980')
        self.root.resizable(False, False)
        self.color = ['white','lightgray','skyblue','blue','teal']
        self.subject_dir = None
        self.create_gui()
    
        self.mycolor = None

    def create_gui(self):
        #creating menu bar
        self.my_menu = Menu(self.root)
        self.root.config(menu=self.my_menu)

        #file menu bar
        self.file_menu = Menu(self.my_menu)
        self.my_menu.add_cascade(label="File", menu=self.file_menu)
       
        edit_menu = Menu(self.my_menu)
        self.my_menu.add_cascade(label="Edit",menu=edit_menu)
        edit_menu.add_command(label="Add Subject",command=self.add_subject)
        edit_menu.add_separator()
        edit_menu.add_command(label="Delete Subject",command=self.delete_subject)
        #toolbar
        self.side_frame = Frame(self.root, width=100, bg=self.color[1])
        self.side_frame.pack(side='left')
        
        #fontbar
        self.top_frame=Frame(self.root, height=20, bg=self.color[1])
        self.top_frame.pack(side='top', fill='x')

        #edit frame

        self.start_frame = Frame(self.root, width=20, bg=self.color[1])
        self.start_frame.pack(side='left', fill='both',expand=1)
       
        self.start_label = Label(self.start_frame,text='Organize Your Notes!',font=("Arial",20),bg=self.color[1],fg=self.color[4])
        self.start_label.place(relx=0.34,rely=0.45)

        self.subject = ttk.Combobox(self.start_frame,values=self.subjects, width=40)
        self.subject.place(relx=0.35,rely=0.5)
        self.subject.set('Select Your Subject')

        self.start_button = Button(self.start_frame,text='Start',bg=self.color[2],command=lambda: self.start_note(self.subject.get()))
        self.start_button.place(relx=0.46,rely=0.55)
        
    def create_tools(self):
        undo_button = Button(self.side_frame,text='Undo',bg=self.color[2],borderwidth=3,command=self.text_box.edit_undo)
        undo_button.pack(padx=3,pady=3,ipadx=10)

        redo_button = Button(self.side_frame,text='Redo',bg=self.color[2],borderwidth=3,command=self.text_box.edit_redo)
        redo_button.pack(padx=3,pady=3,ipadx=10)

        clear_button = Button(self.side_frame,text='Clear',bg=self.color[2],borderwidth=3,command=lambda:self.text_box.delete('1.0',END))
        clear_button.pack(padx=3,pady=3,ipadx=8)
        
        #for top frame
        font_options = ['Arial','Times New Roman','Helvetica','Calibri']
        self.font_type = ttk.Combobox(self.top_frame,width=15,values=font_options)
        self.font_type.pack(side='left',padx=3,pady=3)
        self.font_type.current(0)

        font_sizes = [ _ for _ in range(10,25)]
        self.font_size = ttk.Combobox(self.top_frame,width=5,values=font_sizes)
        self.font_size.pack(side='left',padx=3,pady=3)
        self.font_size.current(2)
        
        self.text_color = Button(self.top_frame,text="Color", bg=self.color[2],command=self.get_color)
        self.text_color.pack(side='left',padx=3,pady=3) 
        
        set_button = Button(self.top_frame,text="Set",bg=self.color[2],command=self.set_command)
        set_button.pack(side='left',padx=3,pady=3)

        search_button = Button(self.top_frame,text="Search", bg=self.color[2],command=self.search_command)
        search_button.pack(side='left',padx=3,pady=3)

        
        share_button = Button(self.top_frame,text="Share", bg=self.color[2],command=self.share_command)
        share_button.pack(side='right',padx=10,pady=3)

        back_button = Button(self.top_frame,text='Back',bg=self.color[2],command=self.back_command)
        back_button.pack(padx=3,pady=3,ipadx=10,side="right")

    def start_note(self, current_subject):
        if current_subject == 'Select Your Subject':
           return 
        self.start_frame.destroy()
        self.file_menu.add_command(label='New',command=self.new_command)
        self.file_menu.add_command(label="Open",command=self.open_command)
        self.file_menu.add_command(label="Save",command= self.save_command)
        self.file_menu.add_command(label='Delete',command= self.delete_command)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit",command=self.root.quit)
        
        self.subject_dir = current_subject
        self.editing_frame = Frame(self.root, width=20, bg=self.color[0])
        self.editing_frame.pack(side='left', fill='both',expand=1)
        #self.create_tools()
        a4_width = 595
        a4_height = 842
        scrollbar = Scrollbar(self.editing_frame)
        scrollbar.pack(side='right', fill='y')
        self.text_box=Text(self.editing_frame,wrap='word',borderwidth=10,yscrollcommand=scrollbar.set,width=int(a4_width/8),height=int(a4_height/12),undo=True,font=('Arial',12))
        self.text_box.pack(fill='both',expand=1)
        scrollbar.config(command=self.text_box.yview)
        self.root.title(f'Keep Notes :- {self.subject_dir}')
        self.create_tools()

    def open_command(self):
        self.text_box.delete('1.0',END)
        path = filedialog.askopenfilename(filetypes=[('Text Files','*.txt'),('All files','*.*')],initialdir=f'./{self.subject_dir}')
        if not path:
            return
        path_list = path.split('/')
        text = self.open_file(path_list[-2],path_list[-1])
        self.text_box.insert(END,text)
        

        self.root.title(f'Keep Notes :- {self.subject_dir}/{path_list[-1]}')

    def save_command(self):
        path = filedialog.asksaveasfilename(filetypes=[('Text Files','*.txt'),('All files','*.*')],defaultextension='.txt',initialdir=f'./{self.subject_dir}')
        if not path:
            return
        path_list = path.split('/')
        text_content = self.text_box.get('1.0', END)
        self.save_file(self.subject_dir,path_list[-1],text_content)
        self.root.title(f'Keep Notes :- {self.subject_dir}/{path_list[-1]}')

    def search_command(self):
        try:
            text = self.text_box.selection_get().strip()
            meaning = self.find_meaning(text)
            end_index = self.text_box.index("sel.last")
            self.text_box.insert(end_index,f'({meaning}) ')
            self.text_box.tag_configure("meaning_font", font=("Arial", 10, "italic"),foreground='green')
            self.text_box.tag_add("meaning_font", end_index, f"{end_index}+{len(meaning)+3}c")
        except:
            return
        
    def share_command(self):
        self.email_window = Tk()
        self.email_window.title("Share File")
        self.email_window.geometry("800x500")
        self.path = None

        def send_command():
            receiver = to_entry.get()
            subject = subject_entry.get()
            body = body_text.get("1.0",END)
            if receiver:
                self.send_email(receiver,subject,body,self.path)
                self.email_window.destroy()

        def select_command():
            self.path = filedialog.askopenfilename()
            if self.path:
                selected_label.config(text=f"{self.path}")
                  

        to_label = Label(self.email_window,text="To:")
        to_label.pack()

        to_entry = Entry(self.email_window,width=50,borderwidth=5)
        to_entry.pack(padx=3,pady=3)

        subject_label = Label(self.email_window,text="subject:")
        subject_label.pack()

        subject_entry = Entry(self.email_window,width=50,borderwidth=5)
        subject_entry.pack(padx=3,pady=3)

        body_label = Label(self.email_window,text="body:")
        body_label.pack()

        body_text = Text(self.email_window,height=5,width=50,borderwidth=5)
        body_text.pack(fill="x",padx=3,pady=3)

        attachment_frame = Frame(self.email_window)
        attachment_frame.pack()

        attachment_label = Label(attachment_frame,text="Attachment:")
        attachment_label.pack()

        selected_label = Label(attachment_frame,text="select file to share")
        selected_label.pack(padx=10,pady=10)

        select_button = Button(attachment_frame,text="Select File",command=select_command)
        select_button.pack()
        
        send_button = Button(self.email_window,text="Send",bg="teal",command=send_command)
        send_button.pack(padx=10,pady=10)
        
    def set_command(self):
        font_type = self.font_type.get()
        font_size = self.font_size.get()
        color = self.mycolor
        if not color:
            color = "black"
        try:
            self.text_box.configure(font=("font_type",font_size),fg=color)
        except:
            return
        
    def get_color(self):
        self.mycolor = colorchooser.askcolor()[1]
        self.text_color.config(bg=self.mycolor)

    def back_command(self):
        for children in self.root.winfo_children():
            children.destroy()
        self.create_gui()
        self.root.title("Keep Notes")
    
    def add_subject(self):
        add_window = Tk()
        add_window.geometry("400x100")
        add_window.title("Add Your Subjects")
        entry = Entry(add_window)
        entry.pack(padx=10,pady=10)

        def add_command():
            if entry.get() not in self.subjects:
                subject = f"{entry.get()}\n"
                self.save_file("subject","subject.txt",subject)
                
                self.set_subject()
                self.back_command()
                entry.delete(0,END)
            else:
                return 
        add = Button(add_window,text="ADD",bg="teal",command=add_command)
        add.pack(padx=10,pady=10)

    def delete_subject(self):
        delete_window = Tk()
        delete_window.geometry("400x100")
        delete_window.title("Delete Your Subjects")
        entry = Entry(delete_window)
        entry.pack(padx=10,pady=10)

        def delete_command():
            subject = entry.get()
            with open("./subject/subject.txt",mode="r") as file:
                lines = file.readlines()
            with open("./subject/subject.txt",mode="w") as file:
                for line in lines:
                    if line.strip() != subject:
                        file.write(line)
                        file.truncate()
            self.set_subject()
            delete_window.destroy()
            self.back_command()

        delete = Button(delete_window,text="DELETE",bg="teal",command=delete_command)
        delete.pack(padx=10,pady=10)

    def new_command(self):
        self.text_box.delete('1.0',END)
        self.root.title(f"Keep Notes :- {self.subject_dir}/New File")
        
    def delete_command(self):
        path = filedialog.askopenfilename(filetypes=[('Text Files','*.txt'),('All files','*.*')],initialdir=f'./{self.subject_dir}')
        if not path:
            return 
        path_list = path.split('/')
        self.delete_file(path_list[-2],path_list[-1])


def main():
    root=Tk()
    app=NoteAppGUI(root)
    root.mainloop()
    

if __name__ == '__main__':
    main()