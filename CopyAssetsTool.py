# MIT License
# 
# Copyright (c) 2023 GewoonIraj
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import os
import json
import shutil
from colorama import init, Fore, Style

init(autoreset=True)

def setup_config():
    if not os.path.exists("config.json"):
        print("Config file not found. Setting up...")
        
        source_base = input("Provide a path for the Input location: ")
        destination_base = input("Provide a path for the Output location: ")
        
        config_data = {
            "source_base": source_base,
            "destination_base": destination_base
        }
        
        with open("config.json", "w") as file:
            json.dump(config_data, file, indent=4)
            
        print("Config file created!")
    else:
        print("Config file already exists.")

setup_config()

with open("config.json", "r") as config_file:
    config = json.load(config_file)

source_base = config.get("source_base", "")

def main_menu():
    display_ascii_art()
    while True:
        print("\nChoose an action:")
        print(Fore.CYAN + "1. Start copying assets")
        print(Fore.CYAN + "2. Open cleaning menu")
        print(Fore.RED + "3. Exit")
        
        choice = input(Fore.WHITE + "Your choice (1-3): ").strip()
        if choice == "1":
            # Process copying goes here...
            process_copying(choose_destination(), handle_override_option(), ask_copy_pictos())
        elif choice == "2":
            cleaning_menu()
        elif choice == "3":
            exit()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def choose_destination():
    display_ascii_art()
    menu_items = [
        (Fore.CYAN + "Use local output folder from the script's root directory"),
        (Fore.CYAN + "Use output folder from config.json"),
        (Fore.RED + "Return to Main Menu")
    ]
    
    while True:
        print("\nChoose a destination folder:")
        for i, item in enumerate(menu_items, 1):
            print(f"{i}. {item}")
        
        choice = input(Fore.WHITE + "Your choice (1-3): ").strip()
        
        if choice == "1":
            return os.path.join(os.path.dirname(__file__), "output")
        elif choice == "2":
            destination_base = config.get("destination_base", "")
            if not destination_base:
                print(Fore.RED + "Error: Missing destination_base in config.json.")
                exit(1)
            return destination_base
        elif choice == "3":
            main_menu()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def handle_override_option():
    display_ascii_art()
    menu_items = [
        (Fore.CYAN + "Override all existing folders (& files)"),
        (Fore.CYAN + "Only non-existing folders"),
        (Fore.RED + "Return to Main Menu")
    ]
    
    while True:
        print("\nChoose an option:")
        for i, item in enumerate(menu_items, 1):
            print(f"{i}. {item}")

        choice = input(Fore.WHITE + "Your choice (1-3): ").strip()
        
        if choice == "1":
            return "Override"
        elif choice == "2":
            return "Non-existing"
        elif choice == "3":
            return choose_destination()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def ask_copy_pictos():
    display_ascii_art()
    while True:
        choice = input(Fore.CYAN + "Copy 'pictos' folder as well? (Y/N or 'R' to Return to the Main Menu): ").strip().lower()
        if choice in ("y", "n"):
            return choice == "y"
        elif choice == "r":
            return handle_override_option()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")

def process_copying(destination_base, copy_mode, copy_pictos):
    for codenamed_map in os.listdir(source_base):
        source_folder = os.path.join(source_base, codenamed_map)
        if not os.path.exists(source_folder):
            print(Fore.RED + f"Skipping '{codenamed_map}' because the input folder doesn't exist.")
            continue

        print(Fore.YELLOW + f"\nUpdating '{codenamed_map}':")
        destination_folder = os.path.join(destination_base, codenamed_map)

        if copy_mode == "Non-existing" and os.path.exists(destination_folder):
            print(Fore.GREEN + "Output folder already exists. Skipping...")
            continue

        for subfolder_name in ["textures", "phone_textures", "pictos"]:
            source_subfolder = os.path.join(source_folder, subfolder_name)
            if not os.path.exists(source_subfolder):
                continue

            if subfolder_name == "pictos" and not copy_pictos:
                continue
            
            for root, _, files in os.walk(source_subfolder):
                for file in files:
                    if file.endswith(".png"):
                        source_file = os.path.join(root, file)
                        destination_file = os.path.join(destination_folder, subfolder_name, file)

                        os.makedirs(os.path.dirname(destination_file), exist_ok=True)
                        shutil.copy2(source_file, destination_file)
            
            print(Fore.GREEN + f"{subfolder_name.capitalize()} files copied.")

    print(Fore.CYAN + "\nAll updates completed.")

def delete_contents(folder_path):
    """Delete the content of a folder."""
    try:
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        return True
    except Exception as e:
        return str(e)

def cleaning_menu():
    display_ascii_art()
    """Prompt the user for deletion option."""
    options = {
        "1": ("output", "output"),
        "2": ("destination", config.get("destination_base", "")),
        "3": ("both folders", None),
        "4": ("Return to Main Menu", None)
    }
    
    while True:
        print("\nChoose a deletion option:")
        print(Fore.CYAN + "1. Only delete local output folder from the script's root directory")
        print(Fore.CYAN + "2. Only delete output folder from config.json")
        print(Fore.CYAN + "3. Delete both folders")
        print(Fore.RED + "4. Return to Main Menu")
        
        choice = input(Fore.WHITE + "Your choice (1-4): ").strip()
        if choice in options:
            folder_name, folder_path = options[choice]
            if folder_name == "Return to Main Menu":
                return
            confirmation = input(Fore.CYAN + f"Are you sure you want to delete the contents of {folder_name} folder? (Y/N): ").strip().lower()
            if confirmation == "y":
                if folder_name == "both folders":
                    folder_paths = ["output", config.get("destination_base", "")]
                    errors = [delete_contents(path) for path in folder_paths if delete_contents(path) != True]
                    if not errors:
                        print(Fore.GREEN + f"Contents of {folder_name} folder deleted successfully.")
                    else:
                        print(Fore.RED + "\n".join(errors))
                else:
                    result = delete_contents(folder_path)
                    if result is True:
                        print(Fore.GREEN + f"Contents of {folder_name} folder deleted successfully.")
                    else:
                        print(Fore.RED + f"Error deleting contents of {folder_name} folder: {result}")
            else:
                print(Fore.RED + f"Cancelled deletion of contents in {folder_name} folder.")
        else:
            print(Fore.RED + "Invalid choice. Please enter '1', '2', '3', or '4'.")

def display_ascii_art():
    print(Fore.GREEN + Style.BRIGHT + """
   _____                                                             _               _______                   _ 
  / ____|                                 /\                        | |             |__   __|                 | |
 | |        ___    _ __    _   _         /  \     ___   ___    ___  | |_   ___         | |      ___     ___   | |
 | |       / _ \  | '_ \  | | | |       / /\ \   / __| / __|  / _ \ | __| / __|        | |     / _ \   / _ \  | |
 | |____  | (_) | | |_) | | |_| |      / ____ \  \__ \ \__ \ |  __/ | |_  \__ \        | |    | (_) | | (_) | | |
  \_____|  \___/  | .__/   \__, |     /_/    \_\ |___/ |___/  \___|  \__| |___/        |_|     \___/   \___/  |_|
                  | |       __/ |                                                                                
                  |_|      |___/                                                                                 
  __  __               _              _                                                                          
 |  \/  |             | |            | |              _                                                          
 | \  / |   __ _    __| |   ___      | |__    _   _  (_)                                                         
 | |\/| |  / _` |  / _` |  / _ \     | '_ \  | | | |                                                             
 | |  | | | (_| | | (_| | |  __/     | |_) | | |_| |  _                                                          
 |_|  |_|  \__,_|  \__,_|  \___|     |_.__/   \__, | (_)                                                         
                                               __/ |                                                             
                                              |___/                                                              
                                                              _                    _                             
    ____                                                     (_)                  (_)                            
   / __ \    __ _    ___  __      __   ___     ___    _ __    _   _ __    __ _     _                             
  / / _` |  / _` |  / _ \ \ \ /\ / /  / _ \   / _ \  | '_ \  | | | '__|  / _` |   | |                            
 | | (_| | | (_| | |  __/  \ V  V /  | (_) | | (_) | | | | | | | | |    | (_| |   | |                            
  \ \__,_|  \__, |  \___|   \_/\_/    \___/   \___/  |_| |_| |_| |_|     \__,_|   | |                            
   \____/    __/ |                                                               _/ |                            
            |___/                                                               |__/                             
""")

if __name__ == "__main__":
    main_menu()
