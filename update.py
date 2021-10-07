from os import path,remove
import win32api
import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
from requests import get
from tkinter import messagebox
import shutil

class Main(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Updater')
        
        self.f_path = path.dirname(__file__)
        self.iconbitmap(path.join(path.join(self.f_path,'icons'),'notebook.ico'))

        self.columnconfigure([0,1,2],minsize=40)
        self.rowconfigure([0,1,2],minsize=30)

        ttk.Label(self,text='Enter your version number:').grid(row=0,column=0,padx=10,pady=10)
        self.cv = ttk.Entry(self,width=10)
        self.cv.grid(row=0,column=1,padx=10,pady=10)
        self.btn = ttk.Button(text='Check for updates...',command= self.check_for_update)
        self.btn.grid(row=1,column=0)
        

    def check_for_update(self):
        self.current_version = float(self.cv.get())
        self.latest_version = self.find_latest_version()
        
        if self.current_version >= self.latest_version:
            self.show_check_result(False)
        elif self.current_version < self.latest_version:
            self.show_check_result(True)
    
    def find_latest_version(self):
        data = get('https://appz-website.herokuapp.com/apps')
        soup = BeautifulSoup(data.content,'html.parser')
        div = soup.find(class_='E-Note')
        dbtn = div.find('button')
        txt = dbtn.get_text()
        self.latest_version = ''.join([i for i in txt if not i.isalpha()]).strip()
        
        return float(self.latest_version)

    def show_check_result(self,updates):
        if updates:
            print(updates)
            message = messagebox.askyesno(parent=self,title='update option',message=f'Update is available\n {self.current_version} -> {self.latest_version}')
            if message==1:
                self.update()

    def update(self):
        file = get(f'https://appz-website.herokuapp.com/static/E-Note_setup.exe')
        open('E-Note_setup.exe','wb').write(file.content)

        win32api.ShellExecute(0,'open','E-Note_setup.exe',None,'.',0)
        

app = Main()
app.mainloop()

try:
    remove('E-Note_setup.exe')
except:
    pass