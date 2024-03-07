import json
from tkinter import *
from tkinter import ttk
from tkinter import simpledialog
from tkinter import Tk, Button, OptionMenu
from tkinter import StringVar

from time import sleep
from subprocess import *
from tkinter import messagebox

from ProfileManager import ProfileManager


class App:

    def __init__(self) -> None:

        self.root = Tk()
        self.root.resizable(False, False)
        self.__pm: ProfileManager = ProfileManager()
        self.__profile_list = self.__pm.GetListOfProfiles()
        self.__selected_button_id = 0

        self.__server_process = None
        self.__config_file = json.load(open("config.json"))

        self.__root_frame = ttk.Frame(self.root, padding=10)

        self.__server_controll_frame = ttk.LabelFrame(
            self.__root_frame, text="Server Controlls", padding=10
        )
        self.__server_controll_frame.pack(side=TOP, anchor=W, fill=X, expand=YES)

        self.__start_server_button = ttk.Button(
            self.__server_controll_frame, text="Start Server"
        )
        self.__start_server_button.pack(side=LEFT, anchor=W)

        self.__stop_server_button = ttk.Button(
            self.__server_controll_frame, text="Stop Server"
        )
        self.__stop_server_button.pack(side=LEFT, anchor=W)

        self.__server_status_lable = ttk.Label(
            self.__server_controll_frame, text="Server Status: Offline"
        )
        self.__server_status_lable.pack(side=LEFT, anchor=W)

        self.__profile_config_frame = ttk.LabelFrame(
            self.__root_frame, text="Profile Configuration", padding=10
        )
        self.__profile_config_frame.pack(side=TOP, anchor=W, fill=X)

        self.__profile_config_controlls = ttk.Frame(self.__profile_config_frame)
        self.__profile_config_controlls.pack(side=TOP, anchor=W, fill=X)

        self.__opt_menu_val = StringVar(self.__profile_config_controlls)

        if len(self.__profile_list) != 0:
            self.__selected_profile: str = self.__profile_list[0]
        else:
            self.__selected_profile: str = ""

        self.__profile_select = ttk.OptionMenu(
            self.__profile_config_controlls,
            self.__opt_menu_val,
            self.__selected_profile,
            *self.__profile_list,
            command=self.__handle_option_change
        )
        self.__profile_select.pack(side=LEFT, anchor=W)

        self.__new_profile_button = ttk.Button(
            self.__profile_config_controlls, text="New Profile"
        )
        self.__new_profile_button.pack(side=LEFT, anchor=W)

        self.__delete_profile_button = ttk.Button(
            self.__profile_config_controlls, text="Delete Profile"
        )
        self.__delete_profile_button.pack(side=LEFT, anchor=W)

        self.__mapping_frame = ttk.Frame(self.__profile_config_frame, padding=10)
        self.__mapping_frame.pack(side=TOP, anchor=W, fill=X)
        self.__mapping_buttons: list = []

        self.__setup_mapping_controlls()

        self.__action_label = ttk.Label(self.__profile_config_frame, text="Action")
        self.__action_label.pack(side=LEFT, anchor=W)

        self.__btn_action = StringVar(self.root)
        self.__btn_text = StringVar(self.root)

        self.__action_input = ttk.Entry(
            self.__profile_config_frame, textvariable=self.__btn_action
        )
        self.__action_input.pack(side=LEFT, anchor=W)

        self.__text_label = ttk.Label(self.__profile_config_frame, text="Text")
        self.__text_label.pack(side=LEFT, anchor=W)

        self.__text_input = ttk.Entry(
            self.__profile_config_frame, textvariable=self.__btn_text
        )
        self.__text_input.pack(side=LEFT, anchor=W)

        self.__save_mapping_btn = ttk.Button(self.__profile_config_frame, text="Save")
        self.__save_mapping_btn.pack(side=LEFT, anchor=W)

        self.__root_frame.pack(side="top", anchor="nw", fill="both", expand=YES)

        self.root.protocol("WM_DELETE_WINDOW", self.__handle_closing)

    def __handle_option_change(self, *args):
        self.__selected_profile = args[0]
        self.__action_input.delete(0, END)
        self.__text_input.delete(0, END)
        self.__update_btn_text()

    def __update_btn_text(self):

        for i in range(0, len(self.__mapping_buttons)):
            mapping = self.__pm.GetMapping(self.__selected_profile, str(i))

            if mapping != None:
                self.__mapping_buttons[i].config(text=mapping.get("text"))
            else:
                self.__mapping_buttons[i].config(text=str(i))

    def __handle_click(self, btnId):
        self.__selected_button_id = btnId
        mapping = self.__pm.GetMapping(self.__selected_profile, str(btnId))

        self.__action_input.delete(0, END)
        self.__text_input.delete(0, END)

        if mapping != None:
            self.__action_input.insert(0, mapping.get("action"))
            self.__text_input.insert(0, mapping.get("text"))
        else:
            print(mapping)

    def __handle_save(self):
        self.__pm.UpdateMapping(
            self.__selected_profile,
            str(self.__selected_button_id),
            self.__text_input.get(),
            self.__action_input.get(),
        )

        self.__update_btn_text()

    def __setup_mapping_controlls(self):
        for i in range(0, 4):
            for j in range(0, 7):
                btnId = j + i * 7
                mapping = self.__pm.GetMapping(self.__selected_profile, str(btnId))
                btnText: str = str(btnId)

                if mapping != None:
                    btnText = mapping.get("text")

                btn = ttk.Button(
                    self.__mapping_frame,
                    text=btnText,
                    width=20,
                    command=lambda bi=btnId: self.__handle_click(bi),
                )
                btn.grid(row=i, column=j)
                self.__mapping_buttons.append(btn)
        return

    def __update_server_status_lable(self, status: int | None):
        statusString = ""
        if status != None:
            statusString = "Server Status: Offline"
        else:
            statusString = "Server Status: Online"

        self.__server_status_lable.config(text=statusString)

    def __start_server_command(self):
        self.__server_process = Popen(self.__config_file["webserver_executeable"])
        self.__update_server_status_lable(self.__server_process.poll())

    def __stop_server_command(self):
        try:
            self.__server_process.kill()

            sleep(0.1)
            self.__update_server_status_lable(self.__server_process.poll())
        except:
            return

    def __handle_new_profile(self):
        profile_name = simpledialog.askstring("New Profile", "Profile Name")
        self.__pm.NewProfile(profile_name)
        print(profile_name)
        if profile_name == "":
            if messagebox.askretrycancel(
                title="retry", message="Invalid text entered. Try again? "
            ):
                self.__handle_new_profile()
            return

        if messagebox.askyesno(
            "Restart?",
            "To add a new profile you need to restart the program, Would you like to close it now?",
        ):
            self.__handle_closing()
        else:
            return

    def __handle_closing(self):
        self.__stop_server_command()
        exit()

    def __delete_profile(self):
        self.__pm.RemoveProfile(self.__selected_profile)
        if messagebox.askyesno(
            "Restart?",
            "some changes have been made to the profiles. For these changes to take affect you need to restart the application. Restart now?",
        ):
            self.__handle_closing()

        return

    def SetCommands(self):
        self.__start_server_button.config(command=self.__start_server_command)
        self.__stop_server_button.config(command=self.__stop_server_command)
        self.__new_profile_button.config(command=self.__handle_new_profile)
        self.__delete_profile_button.config(command=self.__delete_profile)
        self.__save_mapping_btn.config(command=self.__handle_save)
        return

    def MainLoop(self):
        self.root.mainloop()
