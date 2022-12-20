from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import json
import os

from Cart_Page import Cart

class User_Page:
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
          self.user_name = Label(self.frame, text='Hi! Users ❤️', font=('Time', 20))
          self.user_name.place(x=20, y=10)
          self.logout_button = Button(self.frame, text='Log Out', command=self.logout)
          self.logout_button.place(x=850, y=10)

          # ===== Display Books (Tree View) =====
          self.column = ('#', 'Name', 'Author', 'Publisher', 'Year','Genre', 'Price')
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

          # ===== Buy books button =====
          self.buy_button = Button(self.window_frame, text='Buy', command=self.buy, width=8)
          self.buy_button.place(x=1050, y=700)

          # ===== Add to Cart Button =====
          self.add_cart_button = Button(self.window_frame, text='Add to Cart',command=self.add_cart)
          self.add_cart_button.place(x=900, y=700)

          # ===== Cart Icon Button =====
          self.cart_icon = Button(self.window_frame, text='🛒', command=self.cart)
          self.cart_icon.place(x=90, y=700)

          # ===== Reload books button =====
          self.reload_button = Button(self.window_frame, border=0,text='🔄', command=self.reload,width=1)
          self.reload_button.place(x=1145, y=160)

          # ===== Database =====
          self.data = sqlite3.connect('books.db')
          self.c = self.data.cursor()
          self.c.execute("""CREATE TABLE IF NOT EXISTS books (
               name text,
               author text,
               publisher text,
               year integer,
               genre text,
               stocks integer,
               price float)
               """)
          
          self.c.execute("SELECT rowid, name,author,publisher,year,genre,price FROM books ORDER BY name ASC")
          self.records = self.c.fetchall()
          global count
          count = 0 

          for x in self.records:
               self.my_tree.insert(parent="", index="end", iid=count, text="Parent", values=(x))
               
               count += 1


          self.window.mainloop()

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
                    self.c.execute("SELECT rowid,name,author,publisher,year,genre,price FROM books WHERE name = ? OR author = ? OR publisher = ? OR year = ? OR genre = ?", (lookup_data, lookup_data, lookup_data, lookup_data, lookup_data))
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

          self.c.execute("SELECT rowid, name,author,publisher,year,genre,price FROM books ORDER BY name ASC")
          self.records = self.c.fetchall()

          global count
          
          for x in self.records:
               self.my_tree.insert(parent="", index="end", iid=count, values=(x))
               
               count += 1


     # Buy Function
     def buy(self):
          if not self.my_tree.selection():
               messagebox.showinfo('User Page', 'Please Select Something to Buy', icon="warning")
          else:
               while True:
                    with open('report.txt','a') as test:
                         item = self.my_tree.focus()
                         content = self.my_tree.item(item)
                         # selected_title = content.get('values')[1]
                         selected_price = content.get('values')[6]
                         # title = json.dumps(selected_title)
                         price = float(selected_price)
                         test.write(f'{price}')
                         test.close()

                    with open('report.txt', 'r') as file:
                         tax_rate = 0.087
                         # Create a variable to store the sum of the float values
                         total = 0
                         # Read each line from the file
                         for line in file:
                              # Split the line into individual values
                              values = line.split()
                              # Create an empty list to store the float values
                              numbers = []
                              # Iterate over each value in the line
                              for value in values:
                                   # Check if the value is a float
                                   try:
                                        # If it is a float, convert it and append it to the numbers list
                                        numbers.append(float(value))
                                   except ValueError:
                                        # If it is not a float, ignore it
                                        pass
                              # Sum the float values in the numbers list
                              result = sum(numbers)
                              # Add the tax to the result
                              result *= (1 + tax_rate)
                              # Add the result to the total
                              total += result 
                              total = round(total,2)

                    messagebox.showerror('Buy', 'Your Total is ${}\nThank you 😊'.format(total))
                    os.remove('report.txt')
                    break

     # Add Cart Function
     def add_cart(self):
          if not self.my_tree.selection():
               messagebox.showinfo('User Page','Please Select Something to Add to Your Cart')
          else:
               with open('report.txt','a') as test:
                    item = self.my_tree.focus()
                    content = self.my_tree.item(item)
                    selected_title = content.get('values')[1]
                    selected_price = content.get('values')[6]
                    title = json.dumps(selected_title)
                    price = float(selected_price)
                    test.write(f'{title} {price}\n')
                    test.close()
               
     # Cart Icon Function
     def cart(self):
          try:
               if not open('report.txt'):
                    print('No')
               else:
                    Cart(self.window)
          except Exception:
               messagebox.showinfo('Cart','Your Cart is Empty')


     # Log Out Function
     def logout(self):
          self.window.destroy()
          print('See You Again!')
          
