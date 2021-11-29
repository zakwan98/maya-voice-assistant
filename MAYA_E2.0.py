from tkinter import *
from PIL import ImageTk,Image
from tkinter import PhotoImage
import login
import main

root = Tk()

root.title('Maya')
root.geometry('600x570')
root.configure(background="white")

img = ImageTk.PhotoImage(Image.open('Maya.png'))
panel1 = Label(root, image=img, background="white")
panel1.pack(side='right', fill='both', expand='no')


userText = StringVar()

userText.set('Your Virtual Assistant MAYA')
userFrame = LabelFrame(root, text='Maya',background="white", font=('Railways', 24, 'bold'))
userFrame.pack(fill='both', expand='yes')

top = Message(userFrame, textvariable=userText, bg='forestgreen', fg='white')
top.config(font=("Century Gothic", 15, 'bold'))
top.pack(side='top', fill='both', expand='yes')


#btn = Button(root, text='Speak', font=('railways', 10, 'bold'), bg='red', fg='white', command=self.clicked).pack(fill='x', expand='no')
#btn2 = Button(root, text='Close', font=('railways', 10, 'bold'), bg='yellow', fg='black', command=root.destroy).pack(fill='x', expand='no')

def button():
    main.themain()


#btn = Button(root, text="Speak",font=('railways', 10, 'bold'),bg='black', fg='white', width=10, height=1, command=(button)).pack()
#btn2 = Button(root, text="Close",font=('railways', 10, 'bold'),bg='yellow', fg='black', width=10, height=1, command=root.destroy).pack()

def admin():
    root.destroy()
    login.main_screen()

imagetest = PhotoImage(file="mic.png")
imageexit = PhotoImage(file="exit.png")

btn2 = Button(root, image=imageexit, command=lambda:root.destroy).pack(side=TOP,anchor=E)
btn = Button(root, image=imagetest, command=lambda:button()).pack(side=TOP)


btn3= Button(root, text="Admin",font=('railways', 10, 'bold'),bg='yellow', fg='black', width=10, height=1, command=lambda:admin()).pack(expand='no')


panel2 = Label(root, text="Created for Ivan Design Studio", height=1, bg="forestgreen",fg='white', font=('calibre',7,"bold")).pack(side=BOTTOM,fill = 'x', expand='false')
panel3 = Label(background="white").pack()

root.mainloop()
