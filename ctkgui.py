import tkinter as tk
import customtkinter as ctk
import os
from helper.readjson import *
from tkinter import messagebox
from filepath import *

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


def reset_script():
    try:
        with open(multitest_ori, 'r', encoding='UTF8') as file:
            origin_script = file.read()
            print(origin_script)
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found")

    try:
        with open(multitest_modi, "w") as file:
            file.write(origin_script)
            messagebox.showinfo("Success", "Success Reset file")
            file.close()
    except Exception as e:
        messagebox.showerror("Error", f"Failed to reset text: {str(e)}")


# def modify_label_text(label_text) -> str:
#     # Replace spaces with underscores
#     modified_text = label_text.replace(";", "\t")

#     lines = modified_text.split("\n")
#     prefix = "\t"
#     modified_lines = [f"{prefix}{line}" for line in lines]
#     modified_text = "\n".join(modified_lines)
#     # Convert to lowercase
#     modified_text = modified_text.lower()

#     return modified_text


# def insert_text_to_file(filename, line_number, text_to_insert) -> None:
#     try:
#         with open(filename, 'r') as file:
#             lines = file.readlines()
#     except FileNotFoundError:
#         messagebox.showerror("Error", "File not found.")
#         return

#     if line_number > len(lines):
#         messagebox.showerror(
#             "Error", "Line number exceeds the number of lines in the file.")
#         return

#     lines.insert(line_number - 1, modify_label_text(text_to_insert) + '\n')

#     try:
#         with open(filename, 'w') as file:
#             file.writelines(lines)
#         messagebox.showinfo("Success", f"Text inserted at line {line_number}.")
#     except Exception as e:
#         messagebox.showerror("Error", f"Failed to insert text: {str(e)}")

def modify_label_text(label_text) -> str:
    # Replace spaces with underscores
    modified_text = label_text.replace(";", "\t")

    lines = modified_text.split("\n")
    prefix = "    "
    modified_lines = [f"{prefix}{line}" for line in lines]
    modified_text = "\n".join(modified_lines)

    return modified_text


def insert_text_to_file(filename, line_number, text_to_insert) -> None:
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("Error", "File not found.")
        return

    if line_number > len(lines):
        messagebox.showerror(
            "Error", "Line number exceeds the number of lines in the file.")
        return

    lines.insert(line_number - 1, modify_label_text(text_to_insert) + '\n')

    try:
        with open(filename, 'w') as file:
            file.writelines(lines)
        messagebox.showinfo("Success", f"Text inserted at line {line_number}.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to insert text: {str(e)}")


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Appium Tester for QA")
        self.geometry(f"{950}x{580}")
        self.resizable(False, False)

        self.textbox = ctk.CTkTextbox(self, width=250, height=200)
        self.textbox.place(x=10, y=10, relwidth=0.55)

        self.submit = ctk.CTkButton(
            self, text='SUBMIT', command=self.on_submit)
        self.submit.place(x=10, y=220)

        self.reset = ctk.CTkButton(self, text='RESET', command=self.on_reset)
        self.reset.place(x=160, y=220)

        self.entry_udid = ctk.CTkEntry(self, placeholder_text='input udid')
        self.entry_udid.place(x=570, y=10)

        self.entry_devicename = ctk.CTkEntry(
            self, placeholder_text='input devicename')
        self.entry_devicename.place(x=570, y=40)

        self.entry_systemport = ctk.CTkEntry(
            self, placeholder_text='input systemport')
        self.entry_systemport.place(x=570, y=70)

        self.entry_package = ctk.CTkEntry(
            self, placeholder_text='input package')
        self.entry_package.place(x=10, y=300)

        self.entry_activity = ctk.CTkEntry(
            self, placeholder_text='input activity')
        self.entry_activity.place(x=10, y=330)

        self.app_data_save_btn = ctk.CTkButton(
            self, text='SET', command=self.on_data_save)
        self.app_data_save_btn.place(x=160, y=300)

        self.save = ctk.CTkButton(
            self, text='SAVE', command=self.on_save_emulator)
        self.save.place(x=570, y=100)

        self.combo_list = ctk.CTkComboBox(self, values=get_emuid(
        ), command=self.combo_callback, variable=ctk.StringVar(value="select emulator"), state='readonly')
        self.combo_list.place(x=720, y=10)

        self.remove_cap = ctk.CTkButton(
            self, text='REMOVE', command=self.on_remove)
        self.remove_cap.place(x=720, y=50)

        self.run_test = ctk.CTkButton(
            self, text='RUN', command=self.on_test)
        self.run_test.place(x=720, y=550)

        self.label_udid = ctk.CTkLabel(self, text='null')
        self.label_udid.place(x=730, y=90)

        self.label_devicename = ctk.CTkLabel(self, text='null')
        self.label_devicename.place(x=730, y=110)

        self.label_systemport = ctk.CTkLabel(self, text='null')
        self.label_systemport.place(x=730, y=130)

    def on_submit(self) -> None:
        line_number = 67
        text_to_insert = self.textbox.get("1.0", tk.END).strip()
        insert_text_to_file(multitest_modi,
                            line_number, text_to_insert)

    def on_reset(self) -> None:
        reset_script()

    def on_save_emulator(self) -> None:
        udid = self.entry_udid.get()
        devicename = self.entry_devicename.get()
        systemport = self.entry_systemport.get()

        putcaps(udid, devicename, systemport)

        self.combo_reset()

    def combo_callback(self, choice) -> None:
        print("clicked combobox", choice)
        data_list = get_emudata(choice)

        self.data_update(choice)

        print(self.combo_list.get())

    def on_remove(self) -> None:
        choice = self.combo_list.get()
        print("selected!! ", choice)
        remove_key_value_pair('caps.json', choice)

        self.combo_reset()

    def combo_reset(self) -> None:
        first_val = ctk.StringVar()
        first_val.set(get_first_key())
        self.combo_list.configure(values=get_emuid(), variable=first_val)
        self.data_update(get_first_key())

    def data_update(self, choice) -> None:
        data_list = get_emudata(choice)
        self.label_udid.configure(text='udid : ' + data_list[0][1])
        self.label_devicename.configure(text='device : ' + data_list[1][1])
        self.label_systemport.configure(text='systemport : ' + data_list[2][1])

    def on_data_save(self) -> None:
        pacakge_ = self.entry_package.get()
        activity_ = self.entry_activity.get()
        setapps(pacakge_, activity_)

    def on_test(self) -> None:
        os.system("pytest -n auto")


if __name__ == "__main__":

    app = App()
    app.mainloop()
