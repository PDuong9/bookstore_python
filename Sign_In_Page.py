from tkinter import *
from tkinter import messagebox
import PIL.Image
import sqlite3

from Sign_Up_Page import *
from Forget_Password_Page import *
from User_Page import *
from Admin_Page import *


class Sign_In:
     def __init__(self, window):
          self.window = window
          self.window.title('Bookstore Online Project by Phong Duong')
          self.window.geometry('700x500+430+200')

          # ===== Login Frame =====
          self.login_frame = Frame(self.window, width='700', height='500')
          self.login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)
          
          # ===== Heading =====
          self.txt = 'Sign In'
          self.heading = Label(self.login_frame, text=self.txt, font=('Time', 25, 'bold'))
          self.heading.place(x=480, y=90, width=100, height=30)

          # ===== Left Side Image =====
          self.left_side = PIL.Image.open('images/leftside.jpg')
          self.size_image = self.left_side.resize((300,300))
          image = ImageTk.PhotoImage(self.size_image)
          self.left_side_label = Label(self.login_frame, image=image)
          self.left_side_label.image = image
          self.left_side_label.place(x=50, y=100)

          # ===== Username =====
          self.user_var = StringVar()
          self.username = Label(self.login_frame, text='Username', font=('Time', 14, 'bold'))
          self.username.place(x=400, y=150)
          self.username_entry = Entry(self.login_frame, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'), textvariable=self.user_var)
          self.username_entry.place(x=410, y=180, width=260)

          # ===== Password =====
          self.pass_var = StringVar()
          self.password = Label(self.login_frame, text='Password', font=('Time', 14, 'bold'))
          self.password.place(x=400, y=210)
          self.password_entry = Entry(self.login_frame, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'), show='•', textvariable=self.pass_var)
          self.password_entry.place(x=410, y=240, width=260)

          # ===== Forgot Password =====
          self.forgot = Button(self.login_frame, text='Forgot password?', font=('Time', 11, 'underline'), borderwidth=0, command=self.forgot)
          self.forgot.place(x=550, y=270)

          # ===== Login Button =====
          self.button = Button(self.login_frame, text='Login',border=0, command=self.login)
          self.button.place(x=500, y=300)
     
          # ===== Sign up Button =====
          self.label = Label(self.login_frame, width=30, pady=7, text="Don't have an account?", font=('Time',11))
          self.label.place(x=380, y=350)
          self.sign_up_button = Button(self.login_frame, text='Sign up', border=0, command=self.sign_up)
          self.sign_up_button.place(x=560, y=350)
          

     # Login Function
     def login(self):
          username = self.user_var.get()
          password = self.pass_var.get()     
          if username == "" or password == "":
               messagebox.showinfo('Sign In','Username or Password cannot be empty!', icon="warning")
          else:
               while True:
                    try:
                         data = sqlite3.connect('users_data.db')
                         c = data.cursor()
                         c.execute('SELECT * from USERS where USERNAME ="'+str(username)+'"')
                         row = c.fetchall()
                         if username == 'admin' and password == 'admin':
                              self.username_entry.delete(0,END)
                              self.password_entry.delete(0,END)
                              print('Admin Login!')
                              Admin_Page(self.window)
                         elif row[0][3] == username and row[0][4] == password:
                              self.username_entry.delete(0,END)
                              self.password_entry.delete(0,END)
                              print('Users Login!')
                              User_Page(self.window)
                         else:
                              messagebox.showinfo('Sign In', 'Username or Password Incorrect!', icon="warning")
                         break
                    except Exception:
                         messagebox.showinfo('Sign In', "Your account doesn't exist!", icon="warning")
                         break

     # Forgot Password Function
     def forgot(self):
          Forgot(self.window)

     # Sign Up Function
     def sign_up(self):
          Sign_Up(self.window)
          

def main():
     window = Tk()
     Sign_In(window)
     window.mainloop()

if __name__ == '__main__':
     main()
 