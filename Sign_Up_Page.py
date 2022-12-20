from tkinter import *
from PIL import Image, ImageTk
import sqlite3
from tkinter import messagebox


class Sign_Up:
     def __init__(self, window):
          self.window =Toplevel(window)
          self.window.title('Bookstore Online Project by Phong Duong')
          self.window.geometry('700x500+430+200')

          # ===== Sign Up Frame =====
          self.signup = Frame(self.window, width='700', height='500')
          self.signup.place(relx=0.5, rely=0.5, anchor=CENTER)

          # ===== Left Side Image =====
          self.left_side = Image.open('images/Leftside.jpg')
          self.size_image = self.left_side.resize((300,300), Image.Resampling.LANCZOS)
          image = ImageTk.PhotoImage(self.size_image)
          self.left_side_label = Label(self.signup, image=image)
          self.left_side_label.image = image
          self.left_side_label.place(x=25, y=100)

          # ===== Heading =====
          self.txt = 'Sign Up'
          self.heading = Label(self.signup, text=self.txt, font=('Time', 25, 'bold'))
          self.heading.place(x=480, y=50, width=100, height=30)

                    # ===== User Information =====
          # ===== Fist Name =====
          self.firstname = Label(self.signup, text='First Name', font=('Time', 14, 'bold'))
          self.firstname.place(x=350, y=100)
          self.firstname_entry = Entry(self.signup, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.firstname_entry.place(x=410, y=130, width=260)

          # ===== Last Name =====
          self.lastname = Label(self.signup, text='Last Name', font=('Time', 14, 'bold'))
          self.lastname.place(x=350, y=160)
          self.lastname_entry = Entry(self.signup, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.lastname_entry.place(x=410, y=190, width=260)

          # ===== Username =====
          self.username = Label(self.signup, text='Username', font=('Time', 14, 'bold'))
          self.username.place(x=350, y=220)
          self.username_entry = Entry(self.signup, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.username_entry.place(x=410, y=250, width=260)

          # ===== Password =====
          self.password = Label(self.signup, text='Password', font=('Time', 14, 'bold'))
          self.password.place(x=350, y=280)
          self.password_entry = Entry(self.signup, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.password_entry.place(x=410, y=310, width=260)

          # ===== Sign Up Button =====
          self.signup_button = Button(self.signup, text='Sign Up', command=self.sign_up)
          self.signup_button.place(x=500, y=350)

          # ===== If you have an account already =====
          self.account = Label(self.signup, pady=7, text='If you have an account already?', font=('Time', 11, 'underline'))
          self.account.place(x=400, y=400)
          self.account = Button(self.signup, text='Sign In', border=0, command=self.go_back)
          self.account.place(x=580, y=400)

          # ===== Database =====
          # Create a database or connect to the exist one
          self.user_data = sqlite3.connect('users_data.db')

          # Create cursor
          self.cursor = self.user_data.cursor()

          # Create table
          self.cursor.execute("""CREATE TABLE IF NOT EXISTS USERS (
               ID INTEGER PRIMARY KEY,
               first_name TEXT NOT NULL,
               last_name TEXT NOT NULL,
               username TEXT UNIQUE,
               password TEXT NOT NULL
          )""")

          self.window.mainloop()

     # Sign Up Function
     def sign_up(self):
          first_name = self.firstname_entry.get()
          last_name = self.lastname_entry.get()
          username = self.username_entry.get()
          password = self.password_entry.get()

          if len(first_name) == 0 or len(last_name) == 0 or len(username) == 0 or len(password) == 0:
               messagebox.showinfo('Sign Up',"Sorry, can't sign up make sure all fields are complete!", icon="warning")
          elif username == "admin":
               messagebox.showinfo('Sign Up', "Invalid!", icon="warning")
          else:
               try:
                    # Create a database or connect to the exist one
                    self.user_data = sqlite3.connect('users_data.db')
                    # Create cursor
                    self.cursor = self.user_data.cursor()
                    # Insert into Table
                    self.cursor.execute("INSERT INTO USERS (first_name, last_name, username, password) VALUES (?, ?, ?, ?)", (
                         str(first_name),
                         str(last_name),
                         str(username),
                         str(password)
                    ))

                    # Display database
                    self.cursor.execute("SELECT * from USERS")
                    print()
                    print("ID\tFIRST NAME\tLAST NAME\tUSERNAME\tPASSWORD")
                    for row in self.cursor:
                         print ("{}\t{}\t\t{}\t\t{}\t\t{}".format(row[0],row[1],row[2],row[3],row[4]))                                   
                    
                    # Commit change
                    self.user_data.commit()

                    # Close connection
                    self.user_data.close()

                    # Clear the Text Boxes
                    self.firstname_entry.delete(0,END)
                    self.lastname_entry.delete(0,END)
                    self.username_entry.delete(0,END)
                    self.password_entry.delete(0,END)

                    messagebox.showinfo('Sign Up','Sign Up Successful')
                    self.window.destroy()
               
               except Exception:
                    messagebox.showinfo('Sign In', 'This Username has already been taken! ☹️', icon="warning")

     # Go Back to Sign In Page
     def go_back(self):
          self.window.destroy()
          print('back')
          