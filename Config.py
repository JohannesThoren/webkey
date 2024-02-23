from tkinter import *
from tkinter import ttk
import json
import math


class App(Tk):
    def __init__(self):
        super().__init__()
        self.geometry("800x900")
        self.title("Webkey Configurator")

        self.__profilesData = json.load(open("static/profiles.json"))

        self.frm = ttk.Frame(self, padding=10)
        self.frm.pack()

        self.__optionProfile = StringVar()
        self.__profileList = self.GetProfilesList()

        self.__selectedProfile = self.__profileList[0]

        self.__buttons = []

    def GetButton(self, bntId):
        profiles = self.__profilesData.get("profiles")
        keyMap = None

        for profile in profiles:
            if profile.get("name") == self.__selectedProfile:
                keyMap = profile.get("keyMap")
                break

        if keyMap == None:
            print(
                "unable to find profile",
                self.__selectedProfile,
                " please check the profiles.json file",
            )
            return None

        for key in keyMap:
            if key.get("id") == bntId:
                return key

    def GetProfilesList(self):
        l = []
        for profile in self.__profilesData.get("profiles"):
            name = profile.get("name")
            print(name)
            l.append(name)

        return l

    def __ProfileChange(self, *args):
        self.__selectedProfile = args[0]
        print(self.__selectedProfile)
        for btnId, button in enumerate(self.__buttons):
            key = self.GetButton(btnId)
            if key != None:
                button.config(text=key.get("text"))
            else:
                button.config(text=str(btnId))

        self.__SelectedButtonChange(0)
        return

    def __SelectedButtonChange(self, btnId):
        print(btnId)

        return

    def CreateWidgets(self):

        profileControlls = ttk.LabelFrame(self.frm, text="Profile Controlls")
        profileControlls.grid()

        ttk.Label(profileControlls, text="Selected Profile").grid(column=0, row=0)
        ttk.OptionMenu(
            profileControlls,
            self.__optionProfile,
            self.__selectedProfile,
            *self.__profileList,
            command=self.__ProfileChange
        ).grid(column=1, row=0)
        # ttk.Label(profileControlls, text="New Profile").grid(row=1, column=0)

        buttonFrm = ttk.LabelFrame(self.frm, text="Buttons", padding=10)
        buttonFrm.grid()

        for row in range(0, 5):
            for col in range(0, 7):
                bntId = col + (row * 7)
                key = self.GetButton(bntId)
                btn = None

                if key != None:
                    btn = Button(
                        buttonFrm,
                        text=key.get("text"),
                        height=6,
                        width=12,
                        command=lambda i=bntId: self.__SelectedButtonChange(i),
                    )
                    btn.grid(column=col, row=row)
                else:
                    btn = Button(
                        buttonFrm,
                        text=str(bntId),
                        height=6,
                        width=12,
                        command=lambda i=bntId: self.__SelectedButtonChange(i),
                    )
                    btn.grid(column=col, row=row)

                self.__buttons.append(btn)


        btnConfFrame = ttk.LabelFrame(self.frm, text="Configure", padding=10)
        btnConfFrame.grid()

        ttk.Label(btnConfFrame, text="poof").grid(column=0, row=0)


        return


if __name__ == "__main__":
    app = App()
    app.CreateWidgets()
    app.GetButton(10)
    app.mainloop()
