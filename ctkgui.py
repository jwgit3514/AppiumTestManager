import tkinter as tk
from tkinter import ttk
import customtkinter as ctk
import os
from helper.readjson import *
from tkinter import messagebox
from filepath import *
from TkinterDnD2 import DND_ALL, TkinterDnD
from CTkListbox import *
from PIL import Image
import pickle
import atexit

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

class FrameForFile(ctk.CTkFrame, TkinterDnD.DnDWrapper):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

        self.TkdndVersion = TkinterDnD._require(self)

        self.Label = ctk.CTkLabel(self, text="None")
        self.Label.pack(expand=True, padx=100)  


        # self.file_listbox = CTkListbox(self, command=self.show_value, text_color='black')
        # self.file_listbox.pack(expand=True)    

        self.file_listbox = tk.Listbox(self, selectmode='browse', width=50) 
        self.file_listbox.bind('<<ListboxSelect>>', self.show_value)
        self.file_listbox.pack(expand=True) 
        self.file_listbox.drop_target_register(DND_ALL)
        self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)

        self.rm_btn = ctk.CTkButton(self, text='REMOVE', command=self.on_remove)
        self.rm_btn.pack(pady=10)

    def update_image(self, image_path):
        img = Image.open(image_path)
        width, height = img.size
        img = ctk.CTkImage(light_image=Image.open(os.path.join(image_path)), size=(width/4, height/4))
        self.Label.configure(text = '', image=img)
    
    def on_drop(self, event):
        file_path = event.data
        self.insert_listbox(file_path)
        self.save_pickle_data(file_path)
        self.print_Frame(file_path)        

    def print_Frame(self, file_path) -> None:
        file_path_ = file_path
        print(file_path_)
        self.update_image(file_path_)
    
    def insert_listbox(self, file_path) -> None:        
        self.file_listbox.insert(self.file_listbox.size(), file_path)

    def show_value(self, event):
        #print('key : ', self.file_listbox.curselection())
        selected_index = self.file_listbox.curselection()[0]
        selected_option = self.file_listbox.get(selected_index)
        self.print_Frame(selected_option)

    def test_setting(self):
        pass

    def save_pickle_data(self, data):
        try:
            with open('data_.pickle', 'rb') as f:
                data_list = pickle.load(f)
        except Exception as e:
            print("Error!!!! : ", e)
            data_list = []
        # print("data_list : " ,data_list)
        data_list.append(data)
        # print("appended_list : ", data_list)
        with open('data_.pickle', 'wb') as f:
            pickle.dump(data_list, f)

    def delete_from_list(self):
        selection = self.file_listbox.curselection()
        if(len(selection) == 0):
            return
        self.file_listbox.delete(selection[0])

    def delete_from_pickle(self):
        try:
            with open('data_.pickle', 'rb') as f:
                data_list = pickle.load(f)
        except Exception as e:
            print("Error!!!! : ", e)
            return
        
        selected_index = self.file_listbox.curselection()[0]
        selected_option = self.file_listbox.get(selected_index)

        print('selected_option : ', selected_option) 
        print('pre list : ' , data_list)
        data_list.remove(selected_option)
        print('past list : ' , data_list)
        with open('data_.pickle', "wb") as f:
            pickle.dump(data_list, f)

    def on_remove(self):
        self.delete_from_pickle()
        self.delete_from_list()

class TestFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        
        super().__init__(master, **kwargs)
        
        self.entry_udid = ctk.CTkEntry(self, placeholder_text='input udid')
        self.entry_udid.place(x=20, y=20)

        self.entry_devicename = ctk.CTkEntry(
            self, placeholder_text='input devicename')
        self.entry_devicename.place(x=20, y=50)

        self.entry_systemport = ctk.CTkEntry(
            self, placeholder_text='input systemport')
        self.entry_systemport.place(x=20, y=80)
        
        self.save = ctk.CTkButton(
        self, text='SAVE EMU', command=self.on_save_emulator)
        self.save.place(x=20, y=110)

        self.combo_list = ctk.CTkComboBox(self, values=get_emuid(
        ), command=self.combo_callback, variable=ctk.StringVar(value="select emulator"), state='readonly')
        self.combo_list.place(x=20, y=160)

        self.label_udid = ctk.CTkLabel(self, text='null')
        self.label_udid.place(x=20, y=190)
        self.label_devicename = ctk.CTkLabel(self, text='null')
        self.label_devicename.place(x=20, y=220)
        self.label_systemport = ctk.CTkLabel(self, text='null')
        self.label_systemport.place(x=20, y=250)

        self.remove_cap = ctk.CTkButton(
        self, text='REMOVE', command=self.on_remove)
        self.remove_cap.place(x=20, y=280)

        self.entry_package = ctk.CTkEntry(
            self, placeholder_text='input package')
        self.entry_package.place(x=200, y=20)

        self.entry_activity = ctk.CTkEntry(
            self, placeholder_text='input activity')
        self.entry_activity.place(x=200, y=50)
        
        self.app_data_save_btn = ctk.CTkButton(
        self, text='SET PACKAGE DATA', command=self.on_data_save)
        self.app_data_save_btn.place(x=200, y=80) 

        self.reset = ctk.CTkButton(self, text='RESET', command=self.on_reset)
        self.reset.place(x=200, y=110)        

        self.run_test = ctk.CTkButton(
            self, text='RUN', command=self.on_test)
        self.run_test.place(x=400, y=400)

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

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.TkdndVersion = TkinterDnD._require(self)

        self.title("Appium Tester for QA")
        self.geometry(f"{950}x{580}")
        self.resizable(False, False)

        self.my_frame = FrameForFile(master=self, border_width=1, border_color='black')
        self.my_frame.pack(side="left", fill='both')

        self.testframe = TestFrame(master=self)
        self.testframe.pack(expand=True, fill='both')


def cleatup_func():
    try:
        os.remove('./data_.pickle')        
    except OSError as e:
        print(f"file not found!: {e}")

if __name__ == "__main__":
    atexit.register(cleatup_func)

    app = App()    
    app.mainloop()


