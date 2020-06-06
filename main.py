from lxml import html
from os import listdir
from os.path import isfile, join

def main():
    # List only mod files in the current folder
    temp_files = [f for f in listdir(".") if isfile(join(".", f))]
    files = [f for f in temp_files if f[-5:] == ".html"]    
    
    # Parsing through all mods files
    list_containing_all_lists = []
    largest_list_index = 0
    for index, f in enumerate(files):
        with open(f, "r") as f:
            page = f.read()
        tree = html.fromstring(page)
        list_of_mods = tree.xpath('//tr/td//text()')[::7]
        list_containing_all_lists.append(list_of_mods)
        if len(list_of_mods) > len(list_containing_all_lists[largest_list_index]):
            largest_list_index = index

    # Set operations to find unused mods
    list_of_all_mods = list_containing_all_lists[largest_list_index]
    list_containing_all_lists.pop(largest_list_index)

    for each in list_containing_all_lists:
        list_of_all_mods = set(list_of_all_mods) - set(each)

    with open('out.txt', 'w') as f:
        for index, each in enumerate(list_of_all_mods):
            f.write(f"{index+1} {each}\n")
    print("Output saved")

if __name__ == "__main__":
    main()