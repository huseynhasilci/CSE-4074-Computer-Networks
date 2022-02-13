import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.scrolledtext
from sqlite3 import *

import sqlite3
import socket
import threading

HOST = socket.gethostbyname(socket.gethostname())
PORT = 9090
FORMAT = "utf-8"

class Login:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.usernameLabel = tk.Label(self.frame, text="Username: ").grid(row=0, column=0)
        self.username = tk.StringVar()
        username = self.username.get()
        self.usernameEntry = tk.Entry(self.frame, textvariable=self.username).grid(row=0, column=1)

        self.password_label = tk.Label(self.frame,text="Password: ").grid(row = 1,column = 0)
        self.password = tk.StringVar()
        self.password_entry = tk.Entry(self.frame,textvariable= self.password,show = "*").grid(row = 1,column=1)

        self.login_button = tk.Button(self.frame,text ="Login",command = self.check_user,width = 17,height =1).grid(row= 2,column=1)

        self.register_button = tk.Button(self.frame,text = "Register",command=self.go_to_register,width = 17,height =1).grid(row = 3,column = 1)
        #self.HelloButton = tk.Button(self.frame, text = 'Hello', width = 25, command = self.new_window,)
        #self.HelloButton.pack()

        #self.input.pack()
        self.frame.pack()
    def close_windows(self):
        self.master.destroy()
        self.new_window

    def check_user(self):
        sqliteConnection = sqlite3.connect('new_file')
        cursor = sqliteConnection.cursor()
        query = "SELECT username,password FROM users WHERE username = ? AND password  = ?"

        count = cursor.execute(query,(self.username.get(),self.password.get(),))
        sqliteConnection.commit()

        self.rows1 = cursor.fetchall()
        #print(rows1[0][0])
        #cursor.close()
        if len(self.rows1)>0:
            print("Welcome to the server")
            update_query = "UPDATE users set status = ? WHERE username = ?"
            count = cursor.execute(update_query, ("Online",self.username.get(),))
            sqliteConnection.commit()
            get_all_values = "SELECT * FROM users"
            count = cursor.execute(get_all_values)
            rows = count.fetchall()
            #print(rows)
            cursor.close()
            self.go_to_messanger(rows)
        else:
            print("Wrong id and password")


    def go_to_register(self):
        self.master.destroy()  # close the current window
        self.master = tk.Tk()  # create another Tk instance
        self.app = Register(self.master)  # create Demo2 window
        self.master.mainloop()
    def go_to_messanger(self,rows):
        self.master.destroy()  # close the current window
        self.master = tk.Tk()  # create another Tk instance
        self.app = Messenger(self.master,rows,HOST,PORT,self.rows1[0][0])  # create Demo2 window,self.username.get()
        self.master.mainloop()

class Register:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.user_name_label = tk.Label(self.frame, text="Username: ").grid(row=0, column=0)
        self.username = tk.StringVar()
        self.username_Entry = tk.Entry(self.frame, textvariable=self.username).grid(row=0, column=1)

        self.password_label = tk.Label(self.frame, text="Password: ").grid(row=1, column=0)
        self.password = tk.StringVar()
        self.password_entry = tk.Entry(self.frame, textvariable=self.password, show="*").grid(row=1, column=1)

        self.register_button = tk.Button(self.frame, text="Register", command=self.register_user, width=17, height=1).grid(
            row=2, column=1)

        self.login_button = tk.Button(self.frame, text="Back To Login", command=self.go_to_login, width=17,
                                         height=1).grid(row=3, column=1)

        print(self.username.get(), self.password.get())

        self.frame.pack()
    def close_windows(self):
        self.master.destroy()



    def go_to_login(self):
        self.master.destroy()  # close the current window
        self.master = tk.Tk()  # create another Tk instance
        self.app = Login(self.master)  # create Demo2 window
        self.master.mainloop()
    def register_user(self):
        self.master.destroy()  # close the current window
        self.master = tk.Tk()  # create another Tk instance
        self.app = Login(self.master)  # create Demo2 window

        sqliteConnection = sqlite3.connect('new_file')
        cursor = sqliteConnection.cursor()
        print("Database created and Successfully Connected to SQLite")

        var_username = str(self.username.get())
        var_password = str(self.password.get())

        query = "INSERT INTO users (username,status,password) VALUES (?,'Offline',?)"

        # sqlite_select_Query = "select sqlite_version();"
        count = cursor.execute(query,(var_username,var_password,))
        sqliteConnection.commit()
        # print("SQLite Database Version is: ", record)
        cursor.close()

        self.master.mainloop()

class PeerToPeer:
    def __init__(self,master):
        self.master = master
        self.frame = tk.Frame(self.master)

        self.pw = ttk.Panedwindow(self.frame, orient=tk.HORIZONTAL)
        self.pw.pack(fill=tk.BOTH, expand=True)

        self.w2 = ttk.Panedwindow(self.pw, orient=tk.VERTICAL)


        self.frame2 = ttk.Frame(self.pw, width=720, height=400, relief=tk.SUNKEN)
        self.frame3 = ttk.Frame(self.pw, width=720, height=240, relief=tk.SUNKEN)

        self.w2.add(self.frame2)
        self.w2.add(self.frame3)

        self.pw.add(self.w2)
        #self.pw.add(self.frame1)

        self.input_area = tk.Text(self.frame3, height=10)
        self.input_area.grid(row=0, column=0, padx=25, pady=25)
        self.input_scroll = tk.Scrollbar(self.frame3, orient=tk.VERTICAL)
        self.input_scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10)
        self.input_area.config(yscrollcommand=self.input_scroll.set)

        self.send_button = tk.Button(self.frame3, text="Send")
        self.send_button.config(font=("Arial", 12))
        self.send_button.grid(row=1, column=0)

        self.chat_label = tk.Label(self.frame2, text="Chat:")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.grid(row=0, column=0, padx=20, pady=5)

        self.text_area = tk.scrolledtext.ScrolledText(self.frame2)
        self.text_area.grid(row=1, column=0, padx=20, pady=5)
        self.text_area.config(stat="disabled")

        self.frame.pack()



class Messenger:
    def __init__(self, master, users, host, port,mesanger_username): #
        self.master = master
        self.users = users
        self.nickname = mesanger_username
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        self.gui_done = False
        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def close_windows(self):
        self.master.destroy()

    def gui_loop(self):
        self.frame = tk.Frame(self.master)

        self.pw = ttk.Panedwindow(self.frame, orient=tk.HORIZONTAL)
        self.pw.pack(fill=tk.BOTH, expand=True)

        self.w2 = ttk.Panedwindow(self.pw, orient=tk.VERTICAL)

        self.frame1 = ttk.Frame(self.pw, width=720, height=640, relief=tk.SUNKEN)
        self.frame2 = ttk.Frame(self.pw, width=720, height=400, relief=tk.SUNKEN)
        self.frame3 = ttk.Frame(self.pw, width=720, height=500, relief=tk.SUNKEN)

        self.w2.add(self.frame2)
        self.w2.add(self.frame3)

        self.pw.add(self.w2)
        self.pw.add(self.frame1)

        scrollbarx = tk.Scrollbar(self.frame1, orient=tk.HORIZONTAL)
        scrollbary = tk.Scrollbar(self.frame1, orient=tk.VERTICAL)

        self.treeview = ttk.Treeview(self.frame1, columns=("status", "name"), show='headings', height=25)
        self.treeview.grid(row=0, column=0)
        self.treeview.heading('status', text="Status", anchor=tk.CENTER)
        self.treeview.column("status", stretch=tk.NO, width=100)
        self.treeview.heading('name', text="Name", anchor=tk.CENTER)
        self.treeview.column("name", stretch=tk.NO)
        for i in self.users:
            # print(i[0])
            self.treeview.insert("", "end", text="Status", value=(i[1], i[0]))

        scrollbary.config(command=self.treeview.yview)
        scrollbary.grid(row=0, column=1)
        scrollbarx.config(command=self.treeview.xview)
        scrollbarx.grid(row=1, column=0)

        ws_lbl = tk.Label(self.frame1, text="Name: ", font=('calibri', 12, 'normal'))
        ws_lbl.grid(row=2, column=0)
        ws_ent = tk.Entry(self.frame1, width=20, font=('Arial', 15, 'bold'))
        ws_ent.grid(row=3, column=0)
        ws_btn1 = tk.Button(self.frame1, text='Search', width=8, font=('calibri', 12, 'normal'))
        ws_btn1.grid(row=4, column=0)
        ws_btn2 = tk.Button(self.frame1, text='Reset', width=8, font=('calibri', 12, 'normal'),command = self.reset_user_infos)
        ws_btn2.grid(row=5, column=0)

        self.ws_btn3 = tk.Button(self.frame1, text='CHAT', width=8, font=('calibri', 12, 'normal'),command = self.peer_2_peer)
        self.ws_btn3.grid(row=6, column=0)


        self.input_area = tk.Text(self.frame3, height=10)
        self.input_area.grid(row=0, column=0, padx=25, pady=25)
        self.input_scroll = tk.Scrollbar(self.frame3, orient=tk.VERTICAL, command=self.input_area.yview)
        self.input_scroll.grid(row=0, column=1, sticky=tk.N + tk.S, pady=10)
        self.input_area.config(yscrollcommand=self.input_scroll.set)

        self.send_button = tk.Button(self.frame3, text="Send",command = self.write)
        self.send_button.config(font=("Arial", 12))
        self.send_button.grid(row=1, column=0)

        self.chat_label = tk.Label(self.frame2, text="Chat:")
        self.chat_label.config(font=("Arial", 12))
        self.chat_label.grid(row=0, column=0, padx=20, pady=5)

        self.text_area = tk.scrolledtext.ScrolledText(self.frame2)
        self.text_area.grid(row=1, column=0, padx=20, pady=5)
        self.text_area.config(stat="disabled")
        self.gui_done = True
        self.frame.pack()



    def write(self):
        message = f"{self.nickname}: {self.input_area.get('1.0','end')}"
        self.sock.send(message.encode(FORMAT))
        self.input_area.delete('1.0','end')


    def stop(self):
        self.running = False
        self.win.destroy()
        self.sock.close()
        exit(0)


    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode(FORMAT)
                if message == 'NICK':
                    self.sock.send(self.nickname.encode(FORMAT))
                    #self.sock.send(self.password)
                else:
                    if self.gui_done:
                        self.text_area.config(state="normal")
                        self.text_area.insert('end',message)
                        self.text_area.yview('end')
                        self.text_area.config(state="disabled")

            except ConnectionAbortedError:
                break

            except:
                print("Error")
                self.sock.close()
                break

    def reset_user_infos(self):

        self.treeview.selection()
        fetchdata = self.treeview.get_children()
        for f in fetchdata:
            self.treeview.delete(f)

        sqliteConnection = sqlite3.connect('new_file')
        cursor = sqliteConnection.cursor()

        get_all_values = "SELECT * FROM users"
        count = cursor.execute(get_all_values)
        sqliteConnection.commit()
        rows = count.fetchall()
        for i in rows:
            # print(i[0])
            self.treeview.insert("", "end", text="Status", value=(i[1], i[0]))

        cursor.close()
    def peer_2_peer(self):
        self.master = tk.Tk()
        self.app = PeerToPeer(self.master)
        self.master.mainloop()

def main():
    root = tk.Tk()
    app = Login(root)

    root.mainloop()
    sqliteConnection = sqlite3.connect('new_file')
    cursor = sqliteConnection.cursor()
    update_query = "UPDATE users set status = ? WHERE username = ?"
    count = cursor.execute(update_query, ("Offline", app.rows1[0][0],))
    sqliteConnection.commit()
    cursor.close()
    #print()

if __name__ == '__main__':
    main()