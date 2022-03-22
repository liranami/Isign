from tkinter import *
from PIL import Image, ImageTk
import main


def goToGui():
    pass  # TODO : create dev gui
    print("enter")


def validUsers(user, password):
    if user.get().lower() == 'liran' and password.get() == 'pass':
        goToGui()
    else:
        print("bye!")


def logIn(oldWin):
    oldWin.destroy()
    logInGui = Tk()
    logInGui.geometry("1024x600")
    logInGui.title("Isign - Developer LogIn")
    logInGui.configure(bg="#FFFFFF")
    canvas = Canvas(logInGui, bg="#FFFFFF", height=600, width=1024, bd=0, highlightthickness=0, relief="ridge")
    canvas.place(x=0, y=0)
    # create blue rectangle and on top of it our Isign LOGO
    canvas.create_rectangle(0.0, 0.0, 500.0, 600.0, fill="#78BFDD", outline="")
    logo_img = Image.open('assets/Logo.png')
    logo_resize = logo_img.resize((450, 450), Image.ANTIALIAS)
    logo_img = ImageTk.PhotoImage(logo_resize)
    logo = canvas.create_image(240.0, 300.0, image=logo_img)
    canvas.create_text(702.0, 40.0, anchor="nw", text="Isign", fill="#000000", font=("Roboto", 64 * -1))
    canvas.create_text(840, 80.0, anchor="nw", text="dev", fill="#000000", font=("Roboto", 18 * -1))
    # username text entry
    canvas.create_text(680.0, 170.0, anchor="nw", text="UserName", fill="#000000", font=("Roboto", 20 * -1))
    username = StringVar()
    usernameEntry = Entry(logInGui, textvariable=username)
    usernameEntry.place(x=680, y=200, width=200, height=40)

    # password text entry
    canvas.create_text(680.0, 300.0, anchor="nw", text="Password", fill="#000000", font=("Roboto", 20 * -1))
    password = StringVar()
    passwordEntry = Entry(logInGui, textvariable=password, show='*')
    passwordEntry.place(x=680, y=330, width=200, height=40)

    goBack_image = PhotoImage(file='assets/goBack_blue.png')
    logInBtn_image = PhotoImage(file='assets/Button.png')
    goBackBtn = Button(image=goBack_image, borderwidth=0, highlightthickness=0, command=lambda: main.main(logInGui),
                       relief="flat")
    logInBtn = Button(image=logInBtn_image, borderwidth=0, highlightthickness=0,
                      command=lambda: validUsers(username, password), relief="flat")
    goBackBtn.place(x=26, y=32, width=22, height=20)
    logInBtn.place(x=705, y=426, width=158, height=52)
    logInGui.resizable(False, False)
    logInGui.mainloop()
