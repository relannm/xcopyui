import tkinter as tk
from tkinter import filedialog
import os
import shutil

## CONFIG
WINDOW_WIDTH = 400
WINDOW_HEIGHT = 600

PROGRAM_DESC = "Configure then press the button to copy specific files\n" \
               "from one directory (Source) to another directory (Destination).\n" \
               "It copies from source directory and its sub-directories"
PROGRAM_TITLE = 'The Choosy Copier'
SRC_LABEL = "Source directory"
DST_LABEL = "Destination directory"
FLT_LABEL = "File type(s) to be copied (ex: .py; .xls; .c; .txt)"
FLN_LABEL = "File name(s) to be copied (starting letter or words of file name)"

MAIN_BG = "#2C394B"
SECOND_BG = "white"
BTN_COLOR = "#FF4C29"
BTN_HOVER = "#3E6D9C"
BTN_FONT = MAIN_FONT = WHITE = "#FFFFFF"
GREY = "#999999"
BLACK = "#000000"


# to search for directory
def search_dir(target):
    current_dir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=window, initialdir=current_dir, title=f'Please Select {target} Directory')
    return tempdir


def search_src_dir():
    src_dir = search_dir("Source")
    if len(src_dir) > 0:
        entry_src.delete(0, tk.END)
        entry_src.insert(0, src_dir)
        entry_src.configure(fg=BLACK)


def search_dst_dir():
    dst_dir = search_dir("Destination")
    if len(dst_dir) > 0:
        entry_dst.delete(0, tk.END)
        entry_dst.insert(0, dst_dir)
        entry_dst.configure(fg=BLACK)


# to move the window
def window_click(event):
    window_x, window_y = window.winfo_x(), window.winfo_y()
    mouse_x, mouse_y = window.winfo_pointerx(), window.winfo_pointery()

    window_click.offset_x = mouse_x - window_x
    window_click.offset_y = mouse_y - window_y


def move_window(event):
    mouse_x, mouse_y= window.winfo_pointerx(), window.winfo_pointery()

    x = mouse_x - window_click.offset_x
    y = mouse_y - window_click.offset_y
    window.geometry(f'+{x}+{y}')


# close button
def close_button_enter(event):
   close_button.config(fg=BTN_COLOR)


def close_button_leave(event):
   close_button.config(fg=GREY)


# copy files button
def button_enter(event):
   button.config(bg=BTN_HOVER)


def button_leave(event):
   button.config(bg=BTN_COLOR)


#directories button
def button_dir_enter(event):
   button.config(bg=BTN_HOVER)


def button_dir_leave(event):
   button.config(bg=BTN_COLOR)


# clear text box when click to prepare for character input
def clear_entry_src(x):
    if entry_src.get() == SRC_LABEL:
        entry_src.delete(0, tk.END)
        entry_src.configure(fg=BLACK)


def clear_entry_dst(x):
    if entry_dst.get() == DST_LABEL:
        entry_dst.delete(0, tk.END)
        entry_dst.configure(fg=BLACK)


def clear_entry_flt(x):
    if entry_flt.get() == FLT_LABEL:
        entry_flt.delete(0, tk.END)
        entry_flt.configure(fg=BLACK)


def clear_entry_fln(x):
    if entry_fln.get() == FLN_LABEL:
        entry_fln.delete(0, tk.END)
        entry_fln.configure(fg=BLACK)


# reset text box - when entry is blank
def reset_entry_src(x):
    if not entry_src.get():
        entry_src.insert(0, SRC_LABEL)
        entry_src.configure(fg=GREY)


def reset_entry_dst(x):
    if not entry_dst.get():
        entry_dst.insert(0, DST_LABEL)
        entry_dst.configure(fg=GREY)


def reset_entry_flt(x):
    if not entry_flt.get():
        entry_flt.insert(0, FLT_LABEL)
        entry_flt.configure(fg=GREY)


def reset_entry_fln(x):
    if not entry_fln.get():
        entry_fln.insert(0, FLN_LABEL)
        entry_fln.configure(fg=GREY)


def cleanupfilter(filter_string):
    filter_string = filter_string.replace(' ','')
    filter_string = filter_string.split(';')
    filter_string = list(filter(None, filter_string))
    return filter_string

def copyfiles(src_dir, dst_dir, fil_typ, fil_nam):
    output_text.config(state=tk.NORMAL)
    copy_counter = 0
    try:
        for path, subdirs, files in os.walk(src_dir):
            for file in files:
                for fname in fil_nam:
                    if file.startswith(fname):
                        for ftype in fil_typ:
                            if file.endswith(ftype):
                                src = os.path.join(path, file)
                                shutil.copy(src, dst_dir)
                                copy_counter += 1
                                output_text.insert(tk.END, f"Copied {file}\n")
                                output_text.yview(tk.END)
    except:
        if src_dir == dst_dir:
            output_text.insert(tk.END, "I'm going back to sleep... zzZZZ \nSource and destination are the same")
        else:
            output_text.insert(tk.END, "Oops! Something went wrong. Please check configuration and try again.\n")

    output_text.insert(tk.END, f"\n{copy_counter} files copied")
    output_text.yview(tk.END)
    output_text.config(state=tk.DISABLED)


def preparecopy():
    src_dir = entry_src.get()
    dst_dir = entry_dst.get()
    fil_typ = entry_flt.get()
    fil_nam = entry_fln.get()

    output_text.config(state=tk.NORMAL)
    output_text.delete(1.0, tk.END)

    output_text.insert(tk.END, "\n##### Checking directories... \n\n")
    error_flag = 0
    if not os.path.isdir(src_dir):
        output_text.insert(tk.END, "ERROR! Source directory invalid\n")
        error_flag = 1
    else:
        output_text.insert(tk.END, "Source directory: " + str(src_dir) + "\n")

    if not os.path.isdir(dst_dir):
        output_text.insert(tk.END, "ERROR! Destination directory is not a valid directory\n")
        error_flag = 1
    else:
        output_text.insert(tk.END, "Destination directory: " + str(dst_dir) + "\n")

    if fil_typ == FLT_LABEL or fil_typ == '' or fil_typ == ' ':
        fil_typ = ['']
    else:
        fil_typ = cleanupfilter(fil_typ)
    output_text.insert(tk.END, "File type(s): " + str(fil_typ) + "\n")

    if fil_nam == FLN_LABEL or fil_nam == '' or fil_nam == ' ':
        fil_nam = ['']
    else:
        fil_nam = cleanupfilter(fil_nam)
    output_text.insert(tk.END, "File name(s): " + str(fil_nam) + "\n\n")

    if error_flag == 0:
        output_text.insert(tk.END, "\n##### Copying files... \n\n")
        copyfiles(src_dir, dst_dir, fil_typ, fil_nam)
    else:
        output_text.insert(tk.END, "\nSomething is wrong, I can't go on\n")

    output_text.yview(tk.END)
    output_text.config(state=tk.DISABLED)

########## WINDOW ##########
# initialize window
window = tk.Tk()
window.title(PROGRAM_TITLE)
window.minsize(450, 600)
window.configure(bg=MAIN_BG)
window.overrideredirect(True)
window.attributes('-toolwindow', True)

# position of window after opening
##### get screen width and height
screen_width = window.winfo_screenwidth()     # width of the screen
screen_height = window.winfo_screenheight()   # height of the screen
##### calculate x and y coordinates for the Tk root window
win_pos_x = int((screen_width/2) - (WINDOW_WIDTH/2))
win_pos_y = int((screen_height/2) - (WINDOW_HEIGHT/2))
window.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{win_pos_x}+{win_pos_y}")

# create a title bar
title_bar = tk.Frame(window, bg=MAIN_BG, relief=tk.FLAT, bd=2)
# close button
close_button = tk.Button(title_bar, text="X", font=("Consolas", 18), bd=0, bg=MAIN_BG, fg=GREY, width=3, height=1,
                         relief=tk.FLAT, activebackground=MAIN_BG, activeforeground=BTN_COLOR,
                         highlightcolor=BTN_COLOR, command=window.destroy)
title_bar.pack(expand=1, fill=tk.X)
close_button.pack(padx=0, pady=0, side=tk.RIGHT)
close_button.bind('<Enter>', close_button_enter)
close_button.bind('<Leave>', close_button_leave)

# description
label_program = tk.Label(window, text=PROGRAM_TITLE, bg=MAIN_BG, fg=MAIN_FONT, font=("Arial", 18, "bold"))
label_program.pack(padx=5, pady=5)
label_program = tk.Label(window, text=PROGRAM_DESC, bg=MAIN_BG, fg=MAIN_FONT, font=("Arial", 11))
label_program.pack(padx=5, pady=5)

## DIRECTORIES
dirframe = tk.Frame(window, bg=MAIN_BG, bd=0)
dirframe.columnconfigure(0, weight=1)

# source
entry_src = tk.Entry(dirframe, width=70, bd=5, fg=GREY, relief=tk.FLAT, font=("Arial", 9))
entry_src.insert(0, SRC_LABEL)
entry_src.grid(row=0, column=0, sticky=tk.W+tk.E, pady=10)

button_src = tk.Button(dirframe, text="...", bg=WHITE, width=2, bd=3, relief=tk.FLAT, font=("Arial", 8),
                       activebackground=WHITE, activeforeground=WHITE, command=search_src_dir)
button_src.grid(row=0, column=1, sticky=tk.W+tk.E, pady=5)

entry_src.bind("<FocusIn>", clear_entry_src)
entry_src.bind("<FocusOut>", reset_entry_src)

# destination
entry_dst = tk.Entry(dirframe, width=70, bd=5, fg=GREY, relief=tk.FLAT, font=("Arial", 9))
entry_dst.insert(0, DST_LABEL)
entry_dst.grid(row=1, column=0, sticky=tk.W+tk.E, pady=10)
entry_dst.bind("<FocusIn>", clear_entry_dst)
entry_dst.bind("<FocusOut>", reset_entry_dst)

button_dst = tk.Button(dirframe, text="...", bg="#FFFFFF", width=2, bd=3, relief=tk.FLAT, font=("Arial", 8),
                       activebackground=WHITE, activeforeground=WHITE, command=search_dst_dir)
button_dst.grid(row=1, column=1, sticky=tk.W+tk.E, pady=5)

dirframe.pack(padx=20, pady=0, fill="both", expand=True)

# file type
entry_flt = tk.Entry(window, width=70, bd=5, fg=GREY, relief=tk.FLAT, font=("Arial", 9))
entry_flt.insert(0, FLT_LABEL)
entry_flt.pack(padx=20, pady=10)
entry_flt.bind("<FocusIn>", clear_entry_flt)
entry_flt.bind("<FocusOut>", reset_entry_flt)

# file name
entry_fln = tk.Entry(window, width=70, bd=5, fg=GREY, relief=tk.FLAT, font=("Arial", 9))
entry_fln.insert(0, FLN_LABEL)
entry_fln.pack(padx=20, pady=10)
entry_fln.bind("<FocusIn>", clear_entry_fln)
entry_fln.bind("<FocusOut>", reset_entry_fln)

# execute button
button = tk.Button(window, text="COPY FILES", bd=0, bg=BTN_COLOR, fg=BTN_FONT, width=15, height=2, relief=tk.FLAT,
                   font=("Arial", 12), activebackground=GREY, activeforeground="#555", command=preparecopy)
button.pack(padx=10, pady=20)
button.bind('<Enter>', button_enter)
button.bind('<Leave>', button_leave)

# output
output_text = tk.Text(window, bg="#334756", fg=BTN_FONT, width=100, height=150, relief=tk.FLAT, font=('Arial', 8))
output_text.pack(padx=20, pady=20)
output_text.config(state=tk.DISABLED)

# to move the window
title_bar.bind('<B1-Motion>', move_window)
title_bar.bind('<Button-1>', window_click)

#window.lift()                       #to start window it top level
window.attributes('-topmost', 1)    #to keep window in top level

# show window
window.mainloop()
