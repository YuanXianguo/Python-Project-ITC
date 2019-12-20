import tkinter as tk
from tkinter import messagebox

window = tk.Tk()
window.title('my window')
window.geometry('300x200')

def hello_callback():
    messagebox.showinfo('Hello Python', 'Hello Runoob')

b = tk.Button(window, text='点我', command=hello_callback)
b.pack() # 将小部件放置到主窗口中

window.mainloop() # 进入消息循环


