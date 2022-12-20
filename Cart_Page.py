from tkinter import *
from tkinter import ttk
import PIL.Image
from PIL import ImageTk
from tkinter import messagebox
import os

from User_Page import *

class Cart:
     def __init__(self, window):
          self.window = Toplevel(window)
          self.window.geometry('500x500')
          self.my_tree = ttk.Treeview(window)

          # ===== Frame =====
          self.cart_frame = Frame(self.window, height=500, width=500)
          self.cart_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

          # ===== Logo =====
          self.cart_logo = PIL.Image.open('images/icon3.png')
          self.logo_size = self.cart_logo.resize((120,120))
          image = ImageTk.PhotoImage(self.logo_size)
          self.left_side_label = Label(self.cart_frame, image=image)
          self.left_side_label.image = image
          self.left_side_label.place(x=257, y=55, anchor=CENTER)

          # ===== Cart List =====
          self.column = ('Items', 'Price')
          self.my_tree = ttk.Treeview(self.cart_frame, columns = self.column, show='headings')
          self.my_tree.place(relx=0.05, rely=0.20, width=450, height=300)

          self.my_tree.heading("Items", text="Items")
          self.my_tree.column("Items", width=150, anchor=CENTER)
          self.my_tree.heading("Price", text="Price")
          self.my_tree.column("Price", width=50, anchor=CENTER)

          # ===== Buy Button =====
          self.cart_buy = Button(self.cart_frame, text='Buy', height=1, width=10, command=self.buy)
          self.cart_buy.place(x=300, y=450)

          # ===== Total Button =====
          self.cart_total = Button(self.cart_frame, text='Total', height=1, width=10, command=self.total)
          self.cart_total.place(x=80, y=450)
          
          # ===== Get Data from Text File =====
          self.file = open('report.txt')
          global count
          count = 0 
          for x in self.file:
               self.my_tree.insert("", "end", iid=count, values=(x))
               count += 1

     # Buy Function
     def buy(self):
          messagebox.showinfo('Cart', 'Thank You!''\n''❤️')
          os.remove('report.txt')
          self.window.destroy()
     
     # Total Function
     def total(self):
          # Open the file for reading
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

          # Total Label
          self.cart_total = Label(self.cart_frame, text=' Total: ${}'.format(total), font=('Time',20,'bold'))
          self.cart_total.place(x=240, y=405)
