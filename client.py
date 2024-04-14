import socket
import threading
from tkinter import *
from tkinter import scrolledtext, PhotoImage
from ttkthemes import ThemedTk

class Client:
  def __init__(self, host='127.0.0.1', port=55555):
    self.nickname = input("Enter your nickname: ")

    self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.client.connect((host, port))

    self.root = ThemedTk(theme="yaru")
    self.root.title("Chatroom")

    self.chatBox = scrolledtext.ScrolledText(self.root, bg='white', fg='black', padx=10, pady=10, wrap=WORD)
    self.chatBox.pack(padx=5, pady=5, fill=BOTH, expand=True)
    self.chatBox.configure(state='disabled')

    self.messageFrame = Frame(self.root)
    self.messageFrame.pack(padx=5, pady=5, fill=X)

    self.messageEntry = Text(self.messageFrame, bg='white', fg='black', height=1)
    self.messageEntry.pack(side=LEFT, fill=X, expand=True)
    def on_char_change(self, event):
        print("Text changed")
        message = self.messageEntry.get('1.0', 'end').strip()
        self.sendButton.config(state=NORMAL if message else DISABLED)

    # Bind function to be called on every character change
    self.messageEntry.bind('<<TextChange>>', on_char_change)
    self.messageEntry.bind("<Return>", self.write)

    self.sendIcon = PhotoImage(file='send_icon.png')  # make sure 'send_icon.png' is in the same directory
    self.sendButton = Button(self.messageFrame, image=self.sendIcon, command=self.write, width=20, height=20, compound="center")
    self.sendButton.pack(side=RIGHT)

    receive_thread = threading.Thread(target=self.receive)
    receive_thread.start()

    self.root.mainloop()

  def write(self, event=None):
    message = self.messageEntry.get('1.0', 'end').strip()
    self.messageEntry.delete('0.0', 'end')
    if message != "":
      data = f"{self.nickname}:\n{message}"
      self.client.send(data.encode('ascii'))

  def receive(self):
    while True:
      try:
        message = self.client.recv(1024).decode('ascii')
        if message == 'NICK':
          self.client.send(self.nickname.encode('ascii'))
        else:
          self.chatBox.configure(state='normal')
          self.chatBox.insert('end', message + "\n")
          self.chatBox.configure(state='disabled')
      except:
        print("An error occured!")
        self.client.close()
        break


if __name__ == "__main__":
  client = Client()
