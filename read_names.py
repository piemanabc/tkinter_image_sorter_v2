import tkinter as tk

import os
from PIL import Image, ImageTk
from functools import partial
import math


pos = 0
page = 0
count = 0
cols = 5
rows = 5
items_pp = cols*rows
img_dir = 'D:/Python/tkinter_image_sorter_v2/Pics_here/'


def load_imgs(imgs):
    names = os.listdir(imgs)
    names.sort()
    return names


def frame_draw(nrow, ncol):
    ids = []
    ids_r = []
    for row in range(0, nrow):
        for col in range(0, ncol):
            button = tk.Button(root, borderwidth=1)
            button.grid(in_=rightframe, padx=5, pady=5, column=col, row=row,)
            ids_r.append(button)
        ids.append(ids_r)
        ids_r = []
    return ids


def array_maker(names, nrow, ncol):
    count = 0
    rows = []
    page = []
    pages = []
    for group in range(0, int(math.ceil((len(names)/(nrow*ncol))))):
        for collection in range(0, nrow):
            for item in range(ncol):
                try:
                    rows.append(names[count])
                except IndexError:
                    rows.append(None)
                count = count + 1
            page.append(rows)
            rows = []
        pages.append(page)
        page = []
    ticker = 1
    for page in pages:
        print("page {}".format(ticker))
        for row in page:
            print(row)
        print()
        ticker = ticker + 1
    return pages


def row_col_draw(nrow, ncol, direcroty, book, ids, for_bac):
    global pos
    if for_bac == '-':
        pos = pos - 1
    elif for_bac == '+':
        pos = pos + 1
    elif for_bac == '':
        pos = pos + 0
    else:
        pos = for_bac

    try:
        page = book[pos]
    except IndexError:
        pos = 0
        page = book[pos]

    for row_n in range(0, nrow):
        c_row = page[row_n]
        row_ids = ids[row_n]
        for col in range(0, ncol):
            button = row_ids[col]
            try:
                img = Image.open("{}{}".format(direcroty, c_row[col]))
                img = img.resize((50, 50), Image.ANTIALIAS)
                phot = ImageTk.PhotoImage(img)
                button.config(image=phot, command=partial(open_full, "{}{}".format(direcroty, c_row[col])))
                button.image = phot
            except FileNotFoundError:
                button.config(text='', command=None)
                button.image = None
            button.grid()


def test(row_ids, col):

    button = row_ids[col]
    button.image = None

    button.config(text="", command=None)
    button.grid()


def open_full(full_dir):

    image = Image.open(full_dir)
    w = image.width
    h = image.height

    popout = tk.Toplevel()
    topframe = tk.Frame(popout)
    topframe.grid()
    popout.geometry("{}x{}".format(w + 20, h + 70))
    popout.title("Full Resolution image")

    photo = ImageTk.PhotoImage(image)
    label = tk.Label(topframe, image=photo)
    label.image = photo
    label.grid(padx=10)

    msg = tk.Message(popout)
    msg.grid()

    button = tk.Button(popout, text="Dismiss", command=popout.destroy)
    button.grid()


# 02/02/21 - As of now this is a mess, what needs to happen is:
# -- disp_img() needs to be integrated with the row_col_draw \
# -- this also needs to be made to work with a function that runs on start up which will make the image frames which /
# -- can be edited by the row_col_draw function
# -- start up can be cleaned up and so can the variable names.

root = tk.Tk()

menubar = tk.Menu(root)

filemenu = tk.Menu(root, tearoff=0)
filemenu.add_command(label="Do something")
filemenu.add_separator()

filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

leftframe = tk.Frame(root, background="bisque", width=10, height=100)
rightframe = tk.Frame(root, background="pink", width=10, height=100)

leftframe.grid(row=0, column=0, columnspan=3, sticky="nsew")
rightframe.grid(row=0, column=1, columnspan=9, sticky="nsew")

root.config(menu=menubar)


root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=3)


img_names = load_imgs(img_dir)
frame_ids = frame_draw(rows, cols)
pages = array_maker(img_names,rows,cols)

row_col_draw(rows, cols, img_dir, pages, frame_ids, '')

bottom_button_container =tk.Frame(root)
page_id_frame = tk.Frame(bottom_button_container)

page_id_frame.grid(row=1, column=1, sticky=tk.NSEW)
bottom_button_container.grid(row=1, column=1, sticky=tk.NSEW)

button = tk.Button(root, text='text', command=None, borderwidth=0)
button.grid(sticky=tk.EW, row=1, column=0,)

button = tk.Button(bottom_button_container, text='back', command=partial(row_col_draw, rows, cols, img_dir, pages, frame_ids, '-'))
button.grid(sticky=tk.W, row=1, column=0,)

button = tk.Button(bottom_button_container, text='forward', command=partial(row_col_draw, rows, cols, img_dir, pages, frame_ids, '+'))
button.grid(sticky=tk.E, row=1, column=len(pages)+1)

for item in range(0, len(pages)):
    button = tk.Button(page_id_frame, text=item + 1, command=partial(row_col_draw, rows, cols, img_dir, pages, frame_ids, item))
    button.grid(sticky=tk.EW, row=0, column=item+1)

root.mainloop()
