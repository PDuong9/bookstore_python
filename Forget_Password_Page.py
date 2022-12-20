from tkinter import *
from PIL import ImageTk, Image
from tkinter import messagebox
import sqlite3

class Forgot:
     def __init__(self, window):
          self.window = Toplevel(window)
          self.window.title('Bookstore Online Project by Phong Duong')
          self.window.geometry('400x500')

          # ===== Forgot Image =====
          self.center_image = Image.open('images/forgoticon.jpg')
          self.size_image = self.center_image.resize((100,100), Image.Resampling.LANCZOS)
          image = ImageTk.PhotoImage(self.size_image)
          self.center_image_label = Label(self.window, image=image)
          self.center_image_label.image = image
          self.center_image_label.place(x=150, y=10)

          # ===== Username =====
          self.username_label = Label(self.window, text='Username', font=('Time',14, 'bold'))
          self.username_label.place(x=55, y=120)
          self.username_entry = Entry(self.window, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.username_entry.place(x=70, y=150, width=260)

          # ===== Old Password =====
          self.old_password = Label(self.window, text='Old Password', font=('Time', 14, 'bold'))
          self.old_password.place(x=55, y=190)
          self.old_password_entry = Entry(self.window, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.old_password_entry.place(x=70, y=220, width=260)

          # ===== New Password =====
          self.new_password = Label(self.window, text='New Password', font=('Time', 14, 'bold'))
          self.new_password.place(x=55, y=260)
          self.new_password_entry = Entry(self.window, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.new_password_entry.place(x=70, y=290, width=260)

          # ===== Re-enter New Password =====
          self.re_enter = Label(self.window, text='Re-Enter New Password', font=('Time', 14, 'bold'))
          self.re_enter.place(x=55, y=330)
          self.re_enter_entry = Entry(self.window, highlightthickness=0, relief=FLAT, font=('Time', 14, 'bold'))
          self.re_enter_entry.place(x=70, y=360, width=260)

          # ===== Confirm Button =====
          self.confirm_button = Button(self.window, text='Confirm', command=self.confirm)
          self.confirm_button.place(x=150, y=420)

     # Confirm Forgot Password Function
     def confirm(self):
          if self.username_entry.get() == "" or self.old_password_entry.get() == "" or self.new_password_entry.get() == "" or self.re_enter_entry.get() == "":
               messagebox.showinfo('Forgot a Password?', 'Please Complete All the Required Field!', icon="warning")
          elif self.re_enter_entry.get() != self.new_password_entry.get():
               messagebox.showinfo('Forgot a Password?','Your New Password is not matching!')
          else:
               try:
                    data = sqlite3.connect('users_data.db')
                    cursor = data.cursor()
                    cursor.execute('SELECT * from USERS where USERNAME ="'+str(self.username_entry.get())+'"')
                    row = cursor.fetchall()
                    if self.username_entry.get() == row[0][3]:
                         cursor.execute('UPDATE USERS set PASSWORD ="'+str(self.new_password_entry.get())+'"')
                         data.commit()
                         data.close()
                         messagebox.showinfo('Forgot a Password?','Your password has been changed successfully!✅')
     
                         self.username_entry.delete(0,END)
                         self.old_password_entry.delete(0,END)
                         self.new_password_entry.delete(0,END)
                         self.re_enter_entry.delete(0,END)
                         self.window.destroy()
               except Exception:
                    messagebox.showinfo('Forgot a Password?', 'Your username does not exist!', icon='warning')
