from lxml import html
from os import listdir
from os.path import isfile, join
from tkinter import ttk, BooleanVar, filedialog
from ttkthemes import ThemedTk, ThemedStyle

class UserInterface:
    def __init__(self, window):
        # variable declare
        self.all_mods_list= []

        # root window init
        self.window = window
        self.window.geometry("435x283")
        self.window.title("ArmA Mod Sorter")
        self.window.configure(background="#F6F4F2")
        self.window.resizable(0,0)

        # add tree view
        self.listbox = ttk.Treeview(self.window)
        self.listbox["columns"] = ("Details")
        self.listbox.heading("#0", text="#")
        self.listbox.heading("#1", text="Name")
        self.listbox.column("#0",minwidth=0,width=50) 
        self.listbox.column("#1",minwidth=0,width=350)
        ttk.Style().configure("Treeview", fieldbackground="#FEFEFE", background="#FEFEFE")
        self.listbox.grid(row=2, column=0, sticky="nse", padx=15, pady=10)

        # add buttons
        ttk.Button(self.window, text="Quit", command=self.window.destroy).grid(row=3, column=0, sticky="e", padx=15)
        ttk.Button(self.window, text="Add Modlist", command=self.add_modlist).grid(row=3, column=0, sticky="w", padx=15)
        ttk.Button(self.window, text="Process", command=self.process_list).grid(row=3, column=0, sticky="w", padx=95)
        ttk.Button(self.window, text="Save", command=self.save_output).grid(row=3, column=0, sticky="w", padx=175)


    def add_modlist(self):
        # import modlists
        self.filenames = filedialog.askopenfilenames(title = "Select mods",filetypes = (("html files","*.html"),("all files","*.*")))

        # add the mods to treeview
        # Parsing through all mods files
        list_containing_all_lists = []
        largest_list_index = 0
        for index, f in enumerate(self.filenames):
            with open(f, "r") as f:
                page = f.read()
            tree = html.fromstring(page)
            list_of_mods = tree.xpath('//tr/td//text()')[::7]
            list_containing_all_lists.append(list_of_mods)
            if len(list_of_mods) > len(list_containing_all_lists[largest_list_index]):
                largest_list_index = index
        self.list_containing_all_lists = list_containing_all_lists
        self.largest_list_index = largest_list_index

        # adding all mods to one list
        for each_list in list_containing_all_lists:
            for each_item in each_list:
                self.all_mods_list.append(each_item)
        # remove duplicates and sort
        self.all_mods_list = list(set(self.all_mods_list))
        self.all_mods_list.sort()

        self.refresh_list(self.all_mods_list)

    def refresh_list(self, update_list):
        if not update_list:
            self.listbox.delete(*self.listbox.get_children())
            self.listbox.insert("", "end", text="--", values=("--", ))
        else:
            count = 1
            self.listbox.delete(*self.listbox.get_children())
            for each_item in update_list:
                self.listbox.insert("", "end", text=count, values=(each_item, ))
                count += 1

    def process_list(self):
        # Set operations to find unused mods
        list_containing_all_lists = self.list_containing_all_lists
        list_of_all_mods = list_containing_all_lists[self.largest_list_index]
        list_containing_all_lists.pop(self.largest_list_index)

        # use set difference to get unwanted mods and sort them
        for each in list_containing_all_lists:
            list_of_all_mods = list(set(list_of_all_mods) - set(each))
        list_of_all_mods.sort()

        self.unwanted_mods = list_of_all_mods
        self.refresh_list(list_of_all_mods)

    def save_output(self):
        # save to html
        savefile = filedialog.asksaveasfile(title = "Save modlist", filetypes = (("html files","*.html"),("all files","*.*")))
        with open(savefile.name, 'w') as f:
            for index, each in enumerate(self.unwanted_mods):
                f.write(f"{index+1} {each}\n")
        print("Output saved")

# legacy code
# def main():
#     print("Working...")

#     try:
#         # List only mod files in the current folder
#         # temp_files = [f for f in listdir(".") if isfile(join(".", f))]
#         # files = [f for f in temp_files if f[-5:] == ".html"]    
        
#         # Parsing through all mods files
#         list_containing_all_lists = []
#         largest_list_index = 0
#         for index, f in enumerate(files):
#             with open(f, "r") as f:
#                 page = f.read()
#             tree = html.fromstring(page)
#             list_of_mods = tree.xpath('//tr/td//text()')[::7]
#             list_containing_all_lists.append(list_of_mods)
#             if len(list_of_mods) > len(list_containing_all_lists[largest_list_index]):
#                 largest_list_index = index

#         # Set operations to find unused mods
#         list_of_all_mods = list_containing_all_lists[largest_list_index]
#         list_containing_all_lists.pop(largest_list_index)

#         for each in list_containing_all_lists:
#             list_of_all_mods = list(set(list_of_all_mods) - set(each))

#         with open('out.txt', 'w') as f:
#             list_of_all_mods.sort()
#             for index, each in enumerate(list_of_all_mods):
#                 f.write(f"{index+1} {each}\n")
#         print("Output saved")
#     except:
#         with open('out.txt', 'w') as f:
#             f.write("An error occured")

if __name__ == "__main__":
    window = ThemedTk(theme="ra")
    obj = UserInterface(window)
    window.mainloop()