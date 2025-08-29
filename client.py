import socket, json, threading
from tkinter import *

HOST = "192.168.1.226"   
PORT = 5000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

root = Tk()
root.geometry('450x400')
root.resizable(0,0)
root.title('Multiplayer Kéo-Búa-Bao')
root.config(bg='seashell3')

Label(root, text='Kéo - Búa - Bao', font='arial 22 bold', 
      bg='seashell2', fg="black").pack(pady=10)

Result = StringVar()

result_label = Label(root, textvariable=Result, font='arial 13 bold', 
                     bg='seashell2', width=50, height=4, wraplength=400, fg="blue")
result_label.pack(pady=20)


def listen_server():
    while True:
        try:
            data = client.recv(1024).decode()
            if data:
                res = json.loads(data)
                if res["type"]=="wait":
                    Result.set("Đã chọn, chờ người chơi khác...")
                elif res["type"]=="result":
                    txt = f"Bạn: {res['you']} | Đối thủ: {res['opponent']}\n"
                    if res["winner"]=="draw":
                        txt += "Kết quả: Hòa!"
                    elif res["winner"]=="you":
                        txt += "Kết quả: Bạn thắng!"
                    else:
                        txt += "Kết quả: Bạn thua!"
                    Result.set(txt)
        except:
            break

def play(choice):
    msg = {"type":"play","choice":choice}
    client.send(json.dumps(msg).encode())
    Result.set(f"Bạn đã chọn: {choice}. Đang chờ...")

def Reset():
    Result.set("")

def Exit():
    client.close()
    root.destroy()


btn_frame = Frame(root, bg="seashell3")
btn_frame.pack(pady=15)

Button(btn_frame, text='Bao', font='arial 15 bold', bg='lightblue',
       width=8, command=lambda: play("Bao")).grid(row=0, column=0, padx=10)

Button(btn_frame, text='Búa', font='arial 15 bold', bg='lightgreen',
       width=8, command=lambda: play("Bua")).grid(row=0, column=1, padx=10)

Button(btn_frame, text='Kéo', font='arial 15 bold', bg='lightpink',
       width=8, command=lambda: play("Keo")).grid(row=0, column=2, padx=10)

control_frame = Frame(root, bg="seashell3")
control_frame.pack(pady=15)

Button(control_frame, font='arial 13 bold', text='RESET', 
       padx=10, bg='khaki', command=Reset).grid(row=0, column=0, padx=20)

Button(control_frame, font='arial 13 bold', text='EXIT', 
       padx=10, bg='tomato', command=Exit).grid(row=0, column=1, padx=20)


threading.Thread(target=listen_server, daemon=True).start()

root.mainloop()

