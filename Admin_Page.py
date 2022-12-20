from tkinter import *
from tkinter import ttk
import sqlite3
from tkinter import messagebox

from Add_Book import *

class Admin_Page:
     def __init__(self, window):
          self.window = Toplevel(window)
          self.window.title('Bookstore Online Project by Phong Duong')
          self.window.geometry('1250x750+140+120')
          self.my_tree = ttk.Treeview(window)

          # ===== Frame =====
          self.window_frame = Frame(self.window, width='1250', height='750')
          self.window_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

          # ===== Heading =====
          self.heading = Label(self.window_frame, text='Welcome to My Bookstore', font=('Time', 50))
          self.heading.place(x=630, y=20, anchor=CENTER)

          # ===== Display of user name and logout button =====
          self.frame = Frame(self.window_frame, width=950, height=50)
          self.frame.place(x=150, y=85)
          self.user_name = Label(self.frame, text='Hi! Admin 🤖', font=('Time', 20))
          self.user_name.place(x=20, y=10)
          self.logout_button = Button(self.frame, text='Log Out', command=self.bye)
          self.logout_button.place(x=850, y=10)

          # ===== Display Books (Tree View) =====
          self.column = ('#', 'Name', 'Author', 'Publisher', 'Year','Genre', 'Stocks', 'Price')
          self.my_tree = ttk.Treeview(self.window_frame, columns=self.column, show='headings')
          self.my_tree.place(relx=0.04, rely=0.25, width=1150, height=500)

          self.my_tree.heading("#", text="#")
          self.my_tree.column("#", width=10, anchor=CENTER)
          self.my_tree.heading("Name", text="Title")
          self.my_tree.column("Name", width=150, anchor=CENTER)
          self.my_tree.heading("Author", text="Author")
          self.my_tree.column("Author", width=150, anchor=CENTER)
          self.my_tree.heading("Publisher", text="Publisher")
          self.my_tree.column("Publisher", width=150, anchor=CENTER)
          self.my_tree.heading("Year", text="Released")
          self.my_tree.column("Year",width=50, anchor=CENTER)
          self.my_tree.heading("Genre", text="Genre")
          self.my_tree.column("Genre", width=150, anchor=CENTER)
          self.my_tree.heading("Stocks", text="Stocks")
          self.my_tree.column("Stocks", width=30, anchor=CENTER)
          self.my_tree.heading("Price", text="Price")
          self.my_tree.column("Price", width=50, anchor=CENTER)
          
          # ===== Search bar =====
          self.search_bar_label = Label(self.window_frame, text='Search', font=('Time', 14, 'bold'))
          self.search_bar_label.place(x=50, y=160)
          self.search_bar = Entry(self.window_frame, highlightthickness=0, border=0,relief=FLAT, font=('Time', 14, 'bold'))
          self.search_bar.place(x=105, y=162, width=980, height=25)

          # ===== Search Button =====
          self.search_button = Button(self.window_frame, border=0 ,text='🔎', command=self.search)
          self.search_button.place(x=1090, y=160)

          # ===== Add books button =====
          self.add_button = Button(self.window_frame, text='Add Books', command=self.add)
          self.add_button.place(x=1050, y=700)

          # ===== Delete books button =====
          self.delete_button = Button(self.window_frame, text='Delete', command=self.delete)
          self.delete_button.place(x=950, y=700)

          # ===== Reload books button =====
          self.reload_button = Button(self.window_frame, border=0,text='🔄', command=self.reload,width=1)
          self.reload_button.place(x=1145, y=160)

          # ===== Database =====
          self.data = sqlite3.connect('books.db')
          self.c = self.data.cursor()
          self.c.execute("""CREATE TABLE IF NOT EXISTS books (
               name text unique,
               author text,
               publisher text,
               year integer,
               genre text,
               stocks integer,
               price float)
               """)

          self.c.execute("SELECT rowid, * FROM books ORDER BY name ASC")
          self.records = self.c.fetchall()
          global count
          count = 0 
          
          for x in self.records:
               self.my_tree.insert(parent="", index="end", iid=count, text="Parent", values=(x))
               count += 1

          self.data.commit()
          self.data.close()

          self.window.mainloop()

     # Delete Function
     def delete(self):
          if not self.my_tree.selection():
               messagebox.showinfo('Admin Page', 'Please Select Something First!', icon="warning")
          else:
               result = messagebox.askquestion('Admin Page', 'Are you sure you want to delete this record?')
               if result == 'yes':
                    item = self.my_tree.focus()
                    contents = (self.my_tree.item(item))
                    selected_item = contents['values']
                    self.my_tree.delete(item)
                    data = sqlite3.connect('books.db')
                    cursor = data.cursor()
                    cursor.execute("DELETE from books WHERE oid = %d" % selected_item[0])
                    print('Deleted Item Success!')
                    data.commit()
                    cursor.close()
                    data.close()

     # Search Function
     def search(self, counter = 0):
          # Check if the counter has reached the maximum number of allowed recursion calls
          if counter == 1:
               return

          lookup_data = self.search_bar.get()

          if lookup_data == "":
               messagebox.showinfo('Search', "It's Empty Field! 🧐", icon="warning")
          else:
               try:
                    self.data = sqlite3.connect('books.db')
                    self.c = self.data.cursor()
                    self.c.execute("SELECT rowid, * FROM books WHERE name = ? OR author = ? OR publisher = ? OR year = ? OR genre = ?", (lookup_data, lookup_data, lookup_data, lookup_data, lookup_data))
                    self.records = self.c.fetchall()
                    if lookup_data == self.records[0][1] or lookup_data == self.records[0][2] or lookup_data == self.records[0][3] or lookup_data == self.records[0][4] or lookup_data == self.records[0][5]:
                         for record in self.my_tree.get_children():
                              self.my_tree.delete(record)

                         count = 0

                         for x in self.records:
                              self.my_tree.insert(parent="", index="end", iid=count, text="Parent", values=(x))
                              count += 1

                    # Call the function again, incrementing the counter by 1
                    self.search(counter + 1)
               except Exception:
                    messagebox.showinfo('Search', 'No Information Found! 😔', icon="warning")

     # Reload Function
     def reload(self):
          for record in self.my_tree.get_children():
               self.my_tree.delete(record)

          self.data = sqlite3.connect('books.db')
          self.c = self.data.cursor()

          self.c.execute("SELECT rowid, * FROM books ORDER BY name ASC")
          self.records = self.c.fetchall()

          global count
          
          for x in self.records:
               self.my_tree.insert(parent="", index="end", iid=count, values=(x))
               
               count += 1

     # Log Out Function
     def bye(self):
          self.window.destroy()
          print('See U Again!')

     # Add Function
     def add(self):
          global Add_Book
          Add_Book(self.window)