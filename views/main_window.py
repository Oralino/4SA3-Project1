import tkinter as tk
from tkinter import filedialog
import webbrowser
import urllib.parse

class EngineOptimizerView:
    def __init__(self, root, controller):
        # Sets up the main application window size and title
        self.root = root
        self.controller = controller
        self.root.title("Engine Optimizer")
        self.root.geometry("600x680")

        # Tracks what type of data is currently in the listbox
        self.list_mode = "profiles"

        # Creates a blank list to temporarily store database records in memory
        self.cached_profiles = []

        # Creates the text entry field for the game name
        self.game_label = tk.Label(root, text="Game Name:")
        self.game_label.pack()
        self.game_entry = tk.Entry(root)
        self.game_entry.pack()

        # Creates the text entry field for the graphics card
        self.gpu_label = tk.Label(root, text="GPU:")
        self.gpu_label.pack()
        self.gpu_entry = tk.Entry(root)
        self.gpu_entry.pack()

        # Creates a larger text area for the configuration details
        self.ini_label = tk.Label(root, text="Engine.ini Tweaks:")
        self.ini_label.pack()

        # Creates a container frame to hold the text box and scrollbar together
        self.text_frame = tk.Frame(root)
        self.text_frame.pack(pady=5)

        # Creates the vertical scrollbar and anchors it to the right side of the frame
        self.scrollbar = tk.Scrollbar(self.text_frame)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Creates a taller text widget and links its vertical movement to the scrollbar
        self.ini_text = tk.Text(self.text_frame, height=10, width=50, yscrollcommand=self.scrollbar.set)
        self.ini_text.pack(side=tk.LEFT)

        # Commands the scrollbar to control the text widget
        self.scrollbar.config(command=self.ini_text.yview)

        # Creates a frame to hold the file management buttons side by side
        self.file_frame = tk.Frame(root)
        self.file_frame.pack(pady=5)

        # Creates the import export and expand buttons
        self.import_button = tk.Button(self.file_frame, text="Import INI", command=self.import_ini)
        self.import_button.pack(side=tk.LEFT, padx=5)

        self.export_button = tk.Button(self.file_frame, text="Export INI", command=self.export_ini)
        self.export_button.pack(side=tk.LEFT, padx=5)

        self.expand_button = tk.Button(self.file_frame, text="Expand Editor", command=self.open_expanded_editor)
        self.expand_button.pack(side=tk.LEFT, padx=5)

        # Creates the action buttons and links them to the class methods below
        self.save_button = tk.Button(root, text="Save Profile", command=self.save_profile)
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Profiles", command=self.load_profiles)
        self.load_button.pack()

        self.delete_button = tk.Button(root, text="Delete Profile", command=self.delete_profile)
        self.delete_button.pack()

        self.shop_button = tk.Button(root, text="Find PC Shops", command=self.find_shops)
        self.shop_button.pack()

        # Creates the list area and binds a double left click event to it
        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack(pady=10)
        self.listbox.bind("<Double-1>", self.handle_double_click)

    def import_ini(self):
        # Opens a file dialog to select a text file and loads its contents into the text box
        filepath = filedialog.askopenfilename(
            title="Select Engine.ini File",
            filetypes=[("INI Files", "*.ini"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            with open(filepath, "r") as file:
                content = file.read()
            self.ini_text.delete("1.0", tk.END)
            self.ini_text.insert("1.0", content)
            print(f"SUCCESS: Loaded file from {filepath}")

    def export_ini(self):
        # Opens a file dialog to save the current text box contents to a file on the computer
        filepath = filedialog.asksaveasfilename(
            defaultextension=".ini",
            title="Save Engine.ini File",
            filetypes=[("INI Files", "*.ini"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            content = self.ini_text.get("1.0", tk.END).strip()
            with open(filepath, "w") as file:
                file.write(content)
            print(f"SUCCESS: Saved tweaks to {filepath}")

    def open_expanded_editor(self):
        # Creates a new pop out window on top of the main application
        editor_window = tk.Toplevel(self.root)
        editor_window.title("Expanded Engine.ini Editor")
        editor_window.geometry("800x600")

        # Creates a container frame for the expanded text area and scrollbar
        expand_frame = tk.Frame(editor_window)
        expand_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Creates the vertical scrollbar for the expanded window
        expand_scroll = tk.Scrollbar(expand_frame)
        expand_scroll.pack(side=tk.RIGHT, fill=tk.Y)

        # Creates a massive text widget and links it to the scrollbar
        expanded_text = tk.Text(expand_frame, yscrollcommand=expand_scroll.set)
        expanded_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        expand_scroll.config(command=expanded_text.yview)

        # Copies the current text from the main window into the expanded window
        current_content = self.ini_text.get("1.0", tk.END)
        expanded_text.insert("1.0", current_content)

        def apply_changes():
            # Replaces the text in the main window with the newly edited text and closes the pop out
            new_content = expanded_text.get("1.0", tk.END).strip()
            self.ini_text.delete("1.0", tk.END)
            self.ini_text.insert("1.0", new_content)
            editor_window.destroy()

        # Creates a button to save the changes and close the expanded window
        apply_button = tk.Button(editor_window, text="Apply Changes & Close", command=apply_changes)
        apply_button.pack(pady=10)

    def save_profile(self):
        # Gathers input data from the text boxes and sends it to the controller
        game = self.game_entry.get()
        gpu = self.gpu_entry.get()
        ini_data = self.ini_text.get("1.0", tk.END).strip()
        print("DEBUG: Button clicked. Sending payload to controller.")
        self.controller.save_profile(game, gpu, ini_data)

    def load_profiles(self):
        # Updates the list mode requests profiles stores them in memory and displays them in the list
        self.list_mode = "profiles"
        self.listbox.delete(0, tk.END)
        self.cached_profiles = self.controller.load_profiles()
        
        for p in self.cached_profiles:
            display_text = f"{p['game']} | {p['gpu']}"
            self.listbox.insert(tk.END, display_text)

    def find_shops(self):
        # Updates the list mode requests local shop data from the controller and displays it in the list
        self.list_mode = "shops"
        self.listbox.delete(0, tk.END)
        shops = self.controller.fetch_shops("PC repair shop near me")
        for shop in shops:
            self.listbox.insert(tk.END, shop)

    def handle_double_click(self, event):
        # Determines which action to take based on the current list mode
        if self.list_mode == "profiles":
            self.populate_fields()
        elif self.list_mode == "shops":
            self.open_shop_search()

    def populate_fields(self):
        # Identifies which item was clicked
        selected_indices = self.listbox.curselection()
        if not selected_indices:
            return
        
        # Matches the clicked item to the full data stored in memory
        index = selected_indices[0]
        profile = self.cached_profiles[index]

        # Clears all current text in the input boxes
        self.game_entry.delete(0, tk.END)
        self.gpu_entry.delete(0, tk.END)
        self.ini_text.delete("1.0", tk.END)

        # Inserts the selected database record into the input boxes
        self.game_entry.insert(0, profile.get("game", ""))
        self.gpu_entry.insert(0, profile.get("gpu", ""))
        self.ini_text.insert("1.0", profile.get("ini_data", ""))

    def open_shop_search(self):
        # Opens a Google Search for the selected shop name and address
        selected = self.listbox.get(tk.ACTIVE)
        if selected:
            # Encodes the shop string for a safe URL
            query = urllib.parse.quote(selected)
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
            print(f"SUCCESS: Opening search for {selected}")

    def delete_profile(self):
        # Sends the selected game name from the list to the controller for deletion
        selected = self.listbox.get(tk.ACTIVE)
        if selected and self.list_mode == "profiles":
            game_name = selected.split(" | ")[0]
            self.controller.delete_profile(game_name)
            self.load_profiles()