from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

from Admin_Page import *

class Add_Book:
     def __init__(self, window):
          self.window = Toplevel(window)
          self.window.title('Bookstore Online Project by Phong Duong')
          self.window.geometry('500x450')
          self.my_tree = ttk.Treeview(window)

          # ===== Heading =====
          self.heading = Label(self.window, text='Insert a Book', font=('Time', 30))
          self.heading.pack(pady=30)
          
          # ===== Insert Frame =====
          self.frame = Frame(self.window, width=500, height=100)
          self.frame.pack(pady=10)

          # ===== Insert books sections =====
          self.name_label = Label(self.frame, text='Title', font=('Time', 20))
          self.name_label.grid(row=0, column=0, pady=5)
          self.name = Entry(self.frame, width=30)
          self.name.grid(row=0, column=1, padx=20)

          self.author_label = Label(self.frame, text='Author', font=('Time', 20))
          self.author_label.grid(row=1, column=0, pady=5)
          self.author = Entry(self.frame, width=30)
          self.author.grid(row=1, column=1, padx=20)

          self.publisher_label = Label(self.frame, text='Publisher', font=('Time', 20))
          self.publisher_label.grid(row=2, column=0, pady=5)
          self.publisher = Entry(self.frame, width=30)
          self.publisher.grid(row=2, column=1, padx=20)

          self.year_label = Label(self.frame, text='Released', font=('Time', 20))
          self.year_label.grid(row=3, column=0, pady=5)
          self.year = Entry(self.frame, width=30)
          self.year.grid(row=3, column=1, padx=20)

          self.genre_label = Label(self.frame, text='Genre', font=('Time', 20))
          self.genre_label.grid(row=4, column=0, pady=5)
          self.genre = Entry(self.frame, width=30)
          self.genre.grid(row=4, column=1, padx=20)

          self.stocks_label = Label(self.frame, text='Stocks', font=('Time', 20))
          self.stocks_label.grid(row=5, column=0, pady=5)
          self.stocks = Entry(self.frame, width=30)
          self.stocks.grid(row=5, column=1, padx=20)

          self.price_label = Label(self.frame, text='Price', font=('Time', 20))
          self.price_label.grid(row=6, column=0, pady=5)
          self.price = Entry(self.frame, width=30)
          self.price.grid(row=6, column=1, padx=20)

          # ==== Submit Button =====
          self.submit_button = Button(self.window, text='Submit', command=self.submit)
          self.submit_button.pack()


     # Add Book Function
     def submit(self):
          if self.name.get() == "" or self.author.get() == "" or self.publisher.get() == "" or self.year.get() == "" or self.genre.get() == "" or self.stocks.get() == "" or self.price.get() == "":
               messagebox.showinfo('Add Book', 'Please Complete the Required Field', icon="warning")
          else:
               try:
                    self.data = sqlite3.connect('books.db')
                    self.cursor = self.data.cursor()
                    self.cursor.execute("INSERT INTO books (name, author, publisher, year, genre, stocks, price) VALUES (?, ?, ?, ?, ?, ?, ?)", (
                         str(self.name.get()),
                         str(self.author.get()),
                         str(self.publisher.get()),
                         str(self.year.get()),
                         str(self.genre.get()),
                         str(self.stocks.get()),
                         str(self.price.get())
                    ))
                    self.data.commit()
                    self.cursor.execute("SELECT * FROM books")
                    self.fetch = self.cursor.fetchall()
                    for data in self.fetch:
                         self.my_tree.insert(parent="", index="end", text="Parent", values=(data))
                    self.cursor.close()
                    self.data.close()

                    self.name.delete(0,END)
                    self.author.delete(0,END)
                    self.publisher.delete(0,END)
                    self.year.delete(0,END)
                    self.genre.delete(0,END)
                    self.stocks.delete(0,END)
                    self.price.delete(0,END)

               except Exception:
                    messagebox.showinfo('Add Books', 'This Books Already Exists!')
