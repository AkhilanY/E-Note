# game console Icon made by "https://www.freepik.com" (title="Freepik") from "https://www.flaticon.com/" (title="Flaticon"-www.flaticon.com)
__author__ = 'AkhilanY'
__version__ = '1.0'

import tkinter as tk
from tkinter import ttk
from tkinter import filedialog,messagebox,scrolledtext,font,colorchooser
import datetime as dt
import time
from os import path
import os
import markdown
import webbrowser

class TextEditor(tk.Tk):

    def __init__(self):

        super().__init__()      

        # window
        self.title(' E-NOTE')
        self.geometry('800x500')
        self.iconbitmap(self.path_ico('notebook.ico'))

        self.columnconfigure(0,minsize=1000,weight=1)
        self.rowconfigure([0,1,2],minsize=1000,weight=1)

        # style object
        self.style = ttk.Style(self)

        # adding exit function to exit window
        self.protocol('WM_DELETE_WINDOW',self.exitfile)

        # clearing clipboard before running to 
        self.clipboard_clear()

        # variables
        self.f=''
        self.selected=''
        self.default_font = ('Calibri',11,'normal')
        self.wrapped=0
        self.colorno=0
        self.zoomvalue = 100
        self.trans_value = 1.0
        self.theme='vista'
        self.ed_bg = (255,255,255)

        # calling functions for widgets
        self.widgets()
        self.filemenu()
        self.editmenu()
        self.formatmenu()
        self.viewmenu()
        self.statusbar()
        self.shortcut_bind()

    def path_ico(e,file):
        f_path = path.dirname(__file__)
        ico_path = path.join(path.join(f_path,'icons'),file)
        return ico_path

    def widgets(self):

        # editor

        self.texteditor=scrolledtext.ScrolledText(self,undo=True,wrap=tk.NONE,font=self.default_font,yscrollcommand=tk.NONE,width=700,height=10)
        self.texteditor.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
        self.texteditor.focus_set()

        # scrollbars

        #self.verti_scrol = tk.Scrollbar(self,command=self.texteditor.yview)
        self.hori_scroll = tk.Scrollbar(self,orient='horizontal',command=self.texteditor.xview)
        self.hori_scroll.pack(fill=tk.X)

        self.texteditor['xscrollcommand']=self.hori_scroll.set

        # mainmenu

        self.mainmenu=tk.Menu(master=self)
        self.config(menu=self.mainmenu)

    def filemenu(self):

        # file menu

        self.filemenu=tk.Menu(master=self.mainmenu,tearoff=0)
        self.filemenu.add_command(label='New',command=self.newfile,accelerator='Ctrl+N')
        self.filemenu.add_command(label='Open',command=self.openfile,accelerator='Ctrl+O')
        self.filemenu.add_command(label='Save',command=self.save,accelerator='Ctrl+S')
        self.filemenu.add_command(label='Save As',command=self.save_as,accelerator='Ctrl+Shift+S')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Exit',command=self.exitfile,accelerator='Esc')

        self.mainmenu.add_cascade(label=' File',menu=self.filemenu)

    def editmenu(self):

         # edit menu

        self.editmenu=tk.Menu(master=self.mainmenu,tearoff=0)
        self.editmenu.add_command(label='Undo',command=self.texteditor.edit_undo,accelerator='Ctrl+Z')
        self.editmenu.add_command(label='Redo',command=self.texteditor.edit_redo,accelerator='Ctrl+Y')
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Cut',command=lambda:self.cut_text(False),accelerator='Ctrl+X')
        self.editmenu.add_command(label='Copy',command=lambda:self.copy_text(False),accelerator='Ctrl+C')
        self.editmenu.add_command(label='Paste',command=lambda:self.paste_text(False),accelerator='Ctrl+V')
        self.editmenu.add_separator()
        self.editmenu.add_command(label='Find & Replace',command=self.findNreplace_win,accelerator='Ctrl+F')

        self.editmenu.add_command(label='Delete All',command=self.delete_all,accelerator='Ctrl+Del')
        self.editmenu.add_command(label='Select All',command=self.select_all,accelerator='Ctrl+A')
        self.editmenu.add_command(label='Time/Date',command=self.date_time,accelerator='Ctrl+D')

        self.mainmenu.add_cascade(label='Edit',menu=self.editmenu)

    def formatmenu(self):

        # format menu

        self.formatmenu = tk.Menu(master=self.mainmenu,tearoff=0)
        self.formatmenu.add_checkbutton(label='WORD WRAP',command=self.wrap)

        # font sub menu

        self.fontmenu = tk.Menu(master=self.formatmenu,tearoff=0)
        self.fontmenu.add_command(label='Change Font...',command=self.font_win)
        self.fontmenu.add_command(label='Font Color...',command=self.change_font_color)
        self.fontmenu.add_command(label='Bold',command=self.boldtext,accelerator='Ctrl+B')
        self.fontmenu.add_command(label='Italics',command=self.italicstext,accelerator='Alt+I')
        
        self.formatmenu.add_cascade(label='Font',menu=self.fontmenu)        

        self.mainmenu.add_cascade(label='Format',menu=self.formatmenu)

    def viewmenu(self):

        # view menu

        self.viewmenu = tk.Menu(master=self.mainmenu,tearoff=0)
        self.viewmenu.add_command(label='convert to html',command=self.md2html)
        # zoom submenu

        self.zoommenu = tk.Menu(master=self.viewmenu,tearoff=0)
        self.zoommenu.add_command(label='Zoom In',command=self.zoom_in,accelerator='Ctrl +')
        self.zoommenu.add_command(label='Zoom Out     ',command=self.zoom_out,accelerator='Ctrl -')

        self.viewmenu.add_cascade(label='Zoom',menu=self.zoommenu)

        # editor config
        self.viewmenu.add_cascade(label='Editor',command=self.editor_config_win)

        self.mainmenu.add_cascade(label='View',menu=self.viewmenu)

    def shortcut_bind(self):

        # binding keyboard shortcuts

        self.texteditor.bind('<Control-Key-n>',self.newfile)
        self.texteditor.bind('<Control-Key-o>',self.openfile)
        self.texteditor.bind('<Control-Key-s>',self.save)
        self.texteditor.bind('<Control-Shift-S>',self.save_as)
        self.texteditor.bind('<Escape>',self.exitfile)
        self.texteditor.bind('<Control-Key-c>',self.copy_text)
        self.texteditor.bind('<Control-Key-x>',self.cut_text)
        self.texteditor.bind('Control-Key-v',self.paste_text)
        self.texteditor.bind('<Control-Key-f>',self.findNreplace_win)
        self.texteditor.bind('<Control-Key-Delete>',self.delete_all)
        self.texteditor.bind('<Control-Key-a>',self.select_all)
        self.texteditor.bind('<Control-Key-d>',self.date_time)
        self.texteditor.bind('<Control-Key-b>',self.boldtext)
        self.texteditor.bind('<Alt-i>',self.italicstext)
        self.texteditor.bind('<Control-Key-=>',self.zoom_in)
        self.texteditor.bind('<Control-Key-minus>',self.zoom_out)

    def statusbar(self):

        self.statusbar = ttk.Frame(self,width=800)
        self.statusbar.pack(side=tk.BOTTOM,fill=tk.X)

        self.statusbar.columnconfigure([i for i in range(10)],minsize=80,weight=2)
        self.statusbar.rowconfigure(0,minsize=10,weight=2)

        ttk.Label(self.statusbar,text=' UTF-8',borderwidth=1,relief=tk.SOLID).grid(row=0,column=9,sticky=tk.NSEW)
        
        self.zoom_pct = ttk.Label(self.statusbar,text=f'{self.zoomvalue}%',borderwidth=1,relief=tk.SOLID)
        self.zoom_pct.grid(row=0,column=8,sticky=tk.NSEW)

        self.status_lbl = ttk.Label(self.statusbar,text='',relief=tk.SOLID)
        self.status_lbl.grid(row=0,column=0,columnspan=8,sticky=tk.NSEW)

        # sizegrip
        self.sizegrip = ttk.Sizegrip(self.statusbar)
        self.sizegrip.grid(row=0,column=9,sticky=tk.SE)
   
    ######################################################################################

    def save(self,*keyshort):

        try:

            # opening the existing file if there are any
            self.file = open(self.f, "w")

            text = self.texteditor.get("1.0", tk.END)
            self.file.write(text)

            self.file.close()

        # catching error

        except FileNotFoundError:return self.save_as()

    def save_as(self,*keyshort):

        # path of file

        filetobesaved=tk.filedialog.asksaveasfilename(title='Save As',initialdir='/',defaultextension=".txt",filetypes=(('Text Files',".txt"),('All Files',".")))        

        # returing nothing to escape exception

        if not filetobesaved:
            return

        # resetting current file

        self.f=filetobesaved

        # opening file in editor

        self.file=open(self.f,"w")

        text=self.texteditor.get('1.0',tk.END)
        self.file.write(text)

        self.file.close()

        # changing title
        self.fname = f'{self.f[self.f.rfind("/")+1:]}'
        self.title(f'{self.fname} - E-NOTE')        

    def openfile(self,*keyshort):

        # path for opening file

        filetobeopened=tk.filedialog.askopenfilename(title='Open',initialdir='/',filetypes=(('Text File',"*.txt"),('All Files',"*.*")))
        
        # returning nothing if no path,to escape exception 

        if not filetobeopened:
            return

        # resetting current file
        
        self.f=filetobeopened

        # opening file in editor

        self.file=open(self.f,"r+")
        text=self.file.read()

        self.texteditor.delete("1.0",tk.END)
        self.texteditor.insert('1.0',text)

        self.file.close()

        # changing title
        self.fname = f'{self.f[self.f.rfind("/")+1:]}'
        self.title(f'{self.fname} - E-NOTE')

    def newfile(self,*keyshort):

        # asking to save changes

        message=messagebox.askyesnocancel(title='Save option',message='Do you want to save the existing file')            

        # checking if user want to save changes

        if message==1:
                self.save()
                self.texteditor.delete('1.0',tk.END)
                self.title(' E-NOTE')

        if message==0:
            self.texteditor.delete('1.0',tk.END)
            self.title(' E-NOTE')

        # resetting current file

        self.f=''

    def exitfile(self,*keyshort):

        # asking to save

        message=messagebox.askyesnocancel(title='Save option',message='Do you want to save changes to the file')

        # checking if user want to save or not
  
        if message==1:
            self.save()
            self.destroy()

        elif message==0:
            self.destroy()

    def cut_text(self,keyshort):

        try:

            # checking if keyboard shortcut is used

            if keyshort:
                self.selected = self.clipboard_get()

            if self.texteditor.selection_get():
                self.selected=self.texteditor.selection_get()
                self.texteditor.delete(tk.SEL_FIRST,tk.SEL_LAST)

                self.clipboard_clear()
                self.clipboard_append(self.selected)

        except:pass

    def copy_text(self,keyshort):

        try:
            # checking if keyboard shortcut is used

            if keyshort:
                self.selected = self.clipboard_get()

            if self.texteditor.selection_get():
                self.selected=self.texteditor.selection_get()

                self.clipboard_clear()
                self.clipboard_append(self.selected)

        except:pass

    def paste_text(self,keyshort):

        try:
            
            # checking if keyboard shortcut is used

            if keyshort:
                self.selected = self.clipboard_get()
            
            if self.selected:
                cursor_pos = self.texteditor.index(tk.INSERT)
                self.texteditor.insert(cursor_pos, self.selected)

        except:pass

    def findNreplace_win(self,*keyshort):
        
        # window

        self.frwin = tk.Toplevel(self)
        self.frwin.title('find')
        self.frwin.iconbitmap(self.path_ico('notebook.ico'))
        self.frwin.protocol('WM_DELETE_WINDOW',self.close_frwin)

        self.frwin.columnconfigure([0,1,2,3],minsize=20)
        self.frwin.rowconfigure([0,1,2],minsize=30)

        # variables

        self.last_fr = ''
        self.undid_fr=False

        # labels

        ttk.Label(self.frwin,text='  Find:',width=10,justify=tk.CENTER).grid(row=0,column=0)

        ttk.Label(self.frwin,text='  Replace:',width=10,justify=tk.CENTER).grid(row=1,column=0)

        # entry

        self.s_entry = ttk.Entry(self.frwin,width=50)
        self.s_entry.grid(row=0,column=1,columnspan=3,padx=10)
        self.s_entry.focus_set()

        self.r_entry = ttk.Entry(self.frwin,width=50)
        self.r_entry.grid(row=1,column=1,columnspan=3,sticky=tk.N,padx=10)
        self.r_entry.focus_set()

        # buttons

        search_btn = ttk.Button(self.frwin,text='Find',command=self.find)
        search_btn.grid(row=2,column=1,padx=10,pady=10)

        replace_btn = ttk.Button(self.frwin,text='Replace',command=lambda:self.replace(self.s_entry.get(),self.r_entry.get()))
        replace_btn.grid(row=2,column=2,pady=10)

        self.undo_fr_btn = ttk.Button(self.frwin,text='Undo',command=self.undo_findNreplace)
        self.undo_fr_btn.grid(row=2,column=3,pady=10)

    def close_frwin(self):

        self.texteditor.tag_remove('found', '1.0',tk.END)
        self.frwin.destroy()

    def find(self):

        # removing the before added find tags

        text=self.s_entry.get()
        self.texteditor.tag_remove('found', '1.0',tk.END)

        # finding

        if text:

            index = '1.0'

            while True:

                index = self.texteditor.search(text,index,stopindex=tk.END)
                
                # break if not found

                if not index:break

                # getting the last index of the word

                last_idx = f'{index}+ {len(text)}c'

                self.texteditor.tag_add('found', index,last_idx)

                # setting the index to find after already found

                index = last_idx

            # highlighting

            self.texteditor.tag_config('found',background='yellow')

        self.s_entry.focus_set()

        # resetting variables

        self.last_fr = 'find'
        self.undid_fr=False

    def replace(self,ftext,rtext):

        # variables

        self.replaced = ftext
        self.t2replace = rtext

        # check if both test is present to continue

        if (ftext and rtext):

            index = '1.0'

            while True:

                index = self.texteditor.search(ftext,index,stopindex=tk.END)

                # break if not found

                if not index:break

                # finding the last index of the found word

                last_idx = f'{index}+{len(ftext)}c'

                # replacing

                self.texteditor.delete(index,last_idx)
                self.texteditor.insert(index, rtext)

                self.texteditor.tag_add('found',index, last_idx)
                
                # changing the index to search from next index

                index = last_idx

        self.s_entry.focus_set()

        # resetting variables

        self.last_fr = 'replace'
        self.undid_fr=False

    def undo_findNreplace(self):

        if self.undid_fr==False:

            if self.last_fr=='find':

                self.texteditor.tag_config('found',background='white')

            elif self.last_fr=='replace':

                self.replace(self.t2replace,self.replaced)
                self.texteditor.tag_config('found',background='white')

            self.undid_fr=True
            
    def delete_all(self,*keyshort):

        self.texteditor.delete('1.0',tk.END)

    def select_all(self,*keyshort):

        self.texteditor.tag_add('sel','1.0',tk.END)    

    def date_time(self,*keyshort):

        now = dt.datetime.now()

        timedate = now.strftime('%H:%M %d-%m-%Y')

        cur_pos = self.texteditor.index(tk.INSERT)
        self.texteditor.insert(cur_pos,timedate)

    def boldtext(self,*keyshort):

        try:

            bold_font = font.Font(self.texteditor,self.texteditor.cget('font'))
            bold_font.configure(weight='bold')

            self.texteditor.tag_configure('bold',font=bold_font)

            if 'bold' in self.texteditor.tag_names('sel.first'):
                self.texteditor.tag_remove('bold', 'sel.first','sel.last')

            else:
                self.texteditor.tag_add('bold', 'sel.first','sel.last')

        except:pass

    def italicstext(self,*keyshort):

        try:

            italics_font = font.Font(self.texteditor,self.texteditor.cget('font'))
            italics_font.configure(slant='italic')

            self.texteditor.tag_configure('italics',font=italics_font)

            if 'italics' in self.texteditor.tag_names('sel.first'):
                self.texteditor.tag_remove('italics', 'sel.first','sel.last')

            else:
                self.texteditor.tag_add('italics', 'sel.first','sel.last')

        except:pass

    def font_win(self,*keyshort):
        
        # window

        fowin = tk.Toplevel(self)
        fowin.title('Font')
        fowin.resizable(0,0)
        fowin.iconbitmap(self.path_ico('notebook.ico'))

        fowin.columnconfigure([0,1],minsize=40)
        fowin.rowconfigure([0,1],minsize=20)

        # available fonts

        font_avail=font.families()

        # font style frame

        fstyle_fr = ttk.LabelFrame(fowin,text='Font Style')
        fstyle_fr.grid(row=0,column=1,sticky=tk.NSEW,pady=10,padx=30)

        fstyle_fr.columnconfigure(0,minsize=10)
        fstyle_fr.rowconfigure([0,1],minsize=5)

        # font and font size options frame

        font_op_fr = ttk.LabelFrame(fowin,text='Font')
        font_op_fr.grid(row=0,column=0,sticky=tk.NE,pady=10,padx=10)

        font_op_fr.columnconfigure([0,1],minsize=70)
        font_op_fr.rowconfigure([0,1],minsize=20)

        # sample test frame

        sam_test_fr = tk.Frame(fowin)
        sam_test_fr.grid(row=1,column=0)

        sam_test_fr.columnconfigure([0,1],minsize=70)
        sam_test_fr.rowconfigure(0,minsize=20)

        # apply and cancel frame

        ap_can_fr = tk.Frame(fowin)
        ap_can_fr.grid(row=1,column=1,sticky=tk.SW,padx=20,pady=20)

        ap_can_fr.columnconfigure([0,1],minsize=70)
        ap_can_fr.rowconfigure([0,1],minsize=10)

        # variables

        self.font_selected = tk.StringVar()
        self.font_size_sel = tk.IntVar()
        self.italics_sel = tk.StringVar(value='roman')
        self.bold_sel= tk.StringVar(value='normal')

        # font style option

        ttk.Label(font_op_fr,text='Font:').grid(row=0,column=0,padx=10,pady=10)

        self.font_op = ttk.Combobox(font_op_fr,textvariable=self.font_selected,values=font_avail)
        self.font_op.grid(row=0,column=1,padx=10,pady=10)
        self.font_op.current(32)
        self.font_op.focus()

        # font size option

        ttk.Label(font_op_fr,text='Font size:').grid(row=1,column=0,padx=10,pady=10)

        self.font_size_op = ttk.Combobox(font_op_fr,textvariable=self.font_size_sel,values=[11,12,14,16,18,20,22,24,26,28,32,36,42,48,64,72])
        self.font_size_op.grid(row=1,column=1,padx=10,pady=10)
        self.font_size_op.current(0)

        # italics and bold option

        self.italics_cb = ttk.Checkbutton(fstyle_fr,text='Italics',variable=self.italics_sel,onvalue='italic',offvalue='roman')
        self.italics_cb.grid(row=0,column=0,sticky=tk.NW,pady=10,padx=30)

        self.bold_cb = ttk.Checkbutton(fstyle_fr,text='Bold',variable=self.bold_sel,onvalue='bold',offvalue='normal')
        self.bold_cb.grid(row=1,column=0,sticky=tk.NW,pady=0,padx=30)

        # sample text and test button

        self.sample_text = tk.Label(sam_test_fr,text='Sample',font=self.font_selected.get(),borderwidth=2,relief=tk.SOLID,background='white',width=10,height=3)
        self.sample_text.grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)
        
        self.font_test = ttk.Button(sam_test_fr,text='Test',command=lambda:self.change_font(self.sample_text))
        self.font_test.grid(row=0,column=1,padx=5,pady=5,sticky=tk.E)

        # apply and cancel button

        self.change_font_btn = ttk.Button(ap_can_fr,text='Apply',command=lambda:self.change_font(self.texteditor))
        self.change_font_btn.grid(row=1,column=0,padx=5,pady=5)
        
        self.font_cancel_btn = ttk.Button(ap_can_fr,text='Cancel',command=fowin.destroy)
        self.font_cancel_btn.grid(row=1,column=1,padx=5,pady=5)

    def change_font_color(self,*keyshort):

        color = colorchooser.askcolor(title='Font Color')

        try:

            if self.texteditor.selection_get():
                pos1 = self.texteditor.index('sel.first')
                pos2 = self.texteditor.index('sel.last')

                self.texteditor.tag_add(f'color{self.colorno}', pos1,pos2)
                self.texteditor.tag_configure(f'color{self.colorno}',foreground=color[1])
                
                self.colorno+=1
        except:pass

    def change_font(self,widg):
        
        # font object

        _font = font.Font(family=self.font_selected.get(),size=self.font_size_sel.get(),weight=self.bold_sel.get(),slant=self.italics_sel.get())
        
        # configuring font

        widg.configure(font=_font)

        self.default_font=_font

    def wrap(self):

        # checking if already wrapped

        if self.wrapped:
            self.texteditor['wrap']=tk.NONE

        else:
            self.texteditor['wrap']=tk.WORD

            # resetting wrapped
            self.wrapped = 1
        
    def zoom_in(self,*keyshort):

        if self.zoomvalue>=150:
            return

        font,size,others=self.texteditor.cget('font').split()
        size=int(size)+2

        self.texteditor.config(font=(font,size,others))

        self.zoomvalue+=10
        self.zoom_pct['text']=f'{self.zoomvalue}%'

    def zoom_out(self,*keyshort):
        
        if self.zoomvalue<=100:
            return

        font,size,others=self.texteditor.cget('font').split()
        size=int(size)-2

        self.texteditor.config(font=(font,size,others))

        self.zoomvalue-=10
        self.zoom_pct['text']=f'{self.zoomvalue}%'

    def change_theme(self,e):
        
        self.style.theme_use(self.theme_sel.get())
        self.theme=self.theme_sel.get()

    def editor_config_win(self):

        # window

        self.eg_win=tk.Toplevel(self)
        self.eg_win.title('Editor Configuration')
        self.eg_win.iconbitmap(self.path_ico('notebook.ico'))
        self.eg_win.focus()

        self.eg_win.columnconfigure([0,1],minsize=200)
        self.eg_win.rowconfigure([0,1],minsize=100)

        # frames

        self.trans_fr = ttk.LabelFrame(self.eg_win,text='Transparency')
        self.trans_fr.grid(row=0,column=0,padx=10,pady=10,sticky=tk.NSEW)

        self.bg_fr = ttk.LabelFrame(self.eg_win,text='Background')
        self.bg_fr.grid(row=1,column=0,padx=10,pady=10,sticky=tk.NSEW)

        self.theme_fr = ttk.LabelFrame(self.eg_win,text='Theme')
        self.theme_fr.grid(row=0,column=1,padx=10,pady=10,sticky=tk.NSEW)

        # widgets

        self.theme_sel = tk.StringVar(value=self.theme)

        self.trans_slider = ttk.Scale(self.trans_fr,from_=0,to=1,command=self.transparent)
        self.trans_slider.set(self.trans_value)
        self.trans_slider.pack()

        self.theme_cb = ttk.Combobox(self.theme_fr,textvariable=self.theme_sel,values=[theme for theme in self.style.theme_names()])
        self.theme_cb.grid(row=0,column=1,padx=10,pady=10)
        self.theme_cb.bind('<<ComboboxSelected>>',self.change_theme)

        self.bg_btn = ttk.Button(self.bg_fr,text='Change Editor Color',command=self.change_bg)
        self.bg_btn.pack(pady=10)     

    def transparent(self,e):

        v=self.trans_slider.get()

        if v!=self.trans_value:
            if v<self.trans_value:self.trans_value-=v
            else:self.trans_value+=v

            self.attributes('-alpha',v)
            self.eg_win.focus_set()

    def change_bg(self):

        bg = colorchooser.askcolor(title='Editor Background Color')
        self.texteditor.config(bg=bg[1])
        self.ed_bg=bg[1]

    def md2html(self):

        if not '.md' in self.f:
            messagebox.showerror(title='Markdown view error',message='The file is not a markdown file')
        
        else:
            self.save()
            with open(self.f,'r+') as file:
                txt = file.read()
                html = markdown.markdown(txt)
                self.save_html(html)
                
                

    def save_html(self,html):
        file = filedialog.asksaveasfilename(title='Save As',initialdir='/',defaultextension=".html",filetypes=(('html files',"*.html"),('html files',"*.htm")))
        if not file:
            return
        
        with open(file,'w') as file:
            file.write(html)
            file.close()

app=TextEditor()
app.mainloop()

