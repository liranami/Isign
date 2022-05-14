from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import main
import cv2
import showVideoOnGui
import tkinter
import PIL
import threading
import time
from threading import Thread, Lock
stop = False


def startvideo():
    global stop
    stop = False


def stopvideo():
    global stop
    stop = True
    for i in range(10):
        print("dsgdgfsdhshsfh")



def clearCapture(capture):
    capture.release()
    cv2.destroyAllWindows()

def camerasConnected():
    n = 0
    for i in range(3):
        try:
            cap = cv2.VideoCapture(i)
            ret, frame = cap.read()
            cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            clearCapture(cap)
            n += 1
        except:
            clearCapture(cap)
            break
    return n

def update(userGui):
    global stop
    capture = cv2.VideoCapture(0)
    ret, frame = capture.read()  # Read frame from webcam
    canvas = tkinter.Canvas(userGui, width=640, height=480)
    canvas.place(x=10, y=80)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
    canvas.create_image(0, 0, image=photo, anchor=tkinter.NW)
    if not stop:
        userGui.after(1,update(userGui))
    else:
        return




def changeToUserWin(oldWin):
    oldWin.destroy()
    userGui = Tk()
    userGui.geometry("1024x600")
    userGui.title("Isign - user")
    userGui.configure(bg="#FFFFFF")
    canvas = Canvas(userGui, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    canvas.create_rectangle(578.0, 9.0, 578.0, 590.0, fill="#3D7892", outline="")
    canvas.create_rectangle(26.0, 105.0, 551.0, 560.0, fill="#FFFFFF", outline="#000000")
    canvas.create_text(620.0, 242.0, anchor="nw", text="translated words :", fill="#000000", font=("Roboto", 18 * -1))
    canvas.create_text(702.0, 40.0, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))
    #### textarea   later : textarea.insert(tk.END, *variable*)
    textarea = Text(userGui, height=18, width=40)
    textarea.place(x=615, y=270)

    # Drop down
    clicked = StringVar()
    options = []
    numOfCams = camerasConnected()
    if numOfCams == 0:
        messagebox.showerror("Error", "Please connect camera!")
        clicked.set("no camera")
    else:
        for i in range(numOfCams):
            options.append(i + 1)
        #clicked.set(options[0])
    chooseCamera = ttk.OptionMenu(userGui, clicked, options[0], *options)
    chooseCamera.place(x=680, y=150, width=100, height=30)
    # create start/stop Btn - and texts
    startBtn_image = PhotoImage(file='assets/start_btn.png')
    stopBtn_image = PhotoImage(file='assets/stop_btn.png')
    goBack_image = PhotoImage(file='assets/goBack.png')
    startBtn = Button(image=startBtn_image, borderwidth=0, highlightthickness=0,
                      command= lambda: [threading.Thread(target=update, args=(userGui,)).start(),startvideo()], relief="flat")
    stopBtn = Button(image=stopBtn_image, borderwidth=0, highlightthickness=0, command = lambda: stopvideo(),
                     relief="flat")
    goBackBtn = Button(image=goBack_image, borderwidth=0, highlightthickness=0, command=lambda: main.main(userGui),
                       relief="flat")
    startBtn.place(x=814, y=150, width=77, height=30)
    stopBtn.place(x=902, y=150, width=77, height=30)
    goBackBtn.place(x=26, y=32, width=25, height=25)

    #x = threading.Thread(target=update, args=(userGui,))
    #update(userGui)
    #x.start()
    userGui.resizable(False, False)
    userGui.mainloop()
