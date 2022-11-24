import tkinter as tk
import os
import shutil

## CONFIG
PROGRAM_DESC = "Configure then press the button to copy specific files\n" \
               "from one directory (Source) to another directory (Destination).\n" \
               "It copies from source directory and its sub-directories"
PROGRAM_TITLE = 'The Choosy Copier'
SRC_LABEL = "Source directory"
DST_LABEL = "Destination directory"
FLT_LABEL = "File type(s) to be copied (ex: .py; .xls; .c; .txt)"
FLN_LABEL = "File name(s) to be copied (starting letter or words of file name)"

MAIN_BG = '#2C394B'
SECOND_BG = "white"
BTN_COLOR = '#FF4C29'
BTN_FONT = "#FFFFFF"
MAIN_FONT = "#FFFFFF"
GREY = "#999999"
BLACK = "#000000"


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

    output_text.insert(tk.END, "File type(s): " + str(fil_typ) + "\n")
    output_text.insert(tk.END, "Start of file name(s): " + str(fil_nam) + "\n")

    output_text.insert(tk.END, "\nChecking directories...\n\n")
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
        copyfiles(src_dir, dst_dir, fil_typ, fil_nam)
    else:
        output_text.insert(tk.END, "\nSomething is wrong, I can't go on\n")

    output_text.yview(tk.END)
    output_text.config(state=tk.DISABLED)

########## WINDOW ##########
# initialize window
window = tk.Tk()
window.title("x2x:copy")
window.geometry("450x600")
window.minsize(450, 600)
window.configure(bg=MAIN_BG)

# description
label_program = tk.Label(window, text=PROGRAM_TITLE, bg=MAIN_BG, fg=MAIN_FONT, font=("Arial", 18, "bold"))
label_program.pack(padx=5, pady=20)
label_program = tk.Label(window, text=PROGRAM_DESC, bg=MAIN_BG, fg=MAIN_FONT, font=("Arial", 11))
label_program.pack(padx=5, pady=5)

# source
entry_src = tk.Entry(window, width=70, bd=5, fg=GREY, relief=tk.FLAT, font=("Arial", 9))
entry_src.insert(0, SRC_LABEL)
entry_src.pack(padx=20, pady=10)
entry_src.bind("<FocusIn>", clear_entry_src)
entry_src.bind("<FocusOut>", reset_entry_src)

# destination
entry_dst = tk.Entry(window, width=70, bd=5, fg=GREY, relief=tk.FLAT, font=("Arial", 9))
entry_dst.insert(0, DST_LABEL)
entry_dst.pack(padx=20, pady=10)
entry_dst.bind("<FocusIn>", clear_entry_dst)
entry_dst.bind("<FocusOut>", reset_entry_dst)

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
                   font=("Arial", 12), activebackground=GREY, activeforeground=BLACK, command=preparecopy)
button.pack(padx=10, pady=20)

# output
output_text = tk.Text(window, bg="#334756", fg=BTN_FONT, width=100, height=150, relief=tk.FLAT, font=('Arial', 8))
output_text.pack(padx=20, pady=20)
output_text.config(state=tk.DISABLED)

# show window
window.mainloop()
