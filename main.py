from tkinter import *

import pandas
from pandas import *
from random import *

BACKGROUND_COLOR = "#B1DDC6"
FRENCH = 'French'
ENGLISH = 'English'
current_card = {}


def getData():
  try:
    with open("data/words_to_learn.csv", 'r') as file:
      data = read_csv(file)
      word_list = data.to_dict(orient="records")
  except FileNotFoundError:
    with open("data/french_words.csv", 'r') as file:
      original_data = read_csv(file)
      #french_dict = {row.French:row.English for (index, row) in data.iterrows()}
      word_list = original_data.to_dict(orient="records")
  finally:
    return word_list


list = getData()

def flipCard():
    canvas.itemconfig(canvas_image, image=card_back)
    canvas.itemconfig(title, text="English", fill="white")
    canvas.itemconfig(word, text=current_card["English"], fill="white")


def next_card():
  global current_card, flip_timer
  window.after_cancel(flip_timer)
  current_card = choice(list)
  canvas.itemconfig(title, text="French", fill="black")
  canvas.itemconfig(word, text=current_card['French'], fill="black")
  canvas.itemconfig(canvas_image, image=card_front)
  flip_timer = window.after(3000, flipCard)
  

def is_known():
  list.remove(current_card)
  data = pandas.DataFrame(list)
  data.to_csv("data/words_to_learn.csv", index=False)
  print(len(list))
  next_card()


window = Tk()
window.title("Flashy")
window.config(background=BACKGROUND_COLOR)
window.config(pady=40, padx=40)

flip_timer = window.after(3000, flipCard)

card_back = PhotoImage(file="images/card_back.png")
card_front = PhotoImage(file="images/card_front.png")
right_image = PhotoImage(file="images/right.png")
wrong_image = PhotoImage(file="images/wrong.png")

canvas = Canvas(height=526, width=800, background=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 270, image=card_front)
canvas.grid(column=1, row=1, columnspan=2)
title = canvas.create_text(400, 150, text="Title", fill="black", font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 253, text='Word', fill="black", font=("Ariel", 60, "bold"))

wrong_mark = Button(image=wrong_image, highlightthickness=0, command=next_card)
wrong_mark.grid(column=1, row=2, )
right_mark = Button(image=right_image, highlightthickness=0, command=is_known)
right_mark.grid(column=2, row=2)

next_card()


window.mainloop()