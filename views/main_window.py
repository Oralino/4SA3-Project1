import tkinter as tk

class EngineOptimizerView:
    def __init__(self, root, controller):
        # Sets up the main application window size and title
        self.root = root
        self.controller = controller
        self.root.title("Engine Optimizer")
        self.root.geometry("600x500")

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
        self.ini_text = tk.Text(root, height=5)
        self.ini_text.pack()

        # Creates the action buttons for the interface
        self.save_button = tk.Button(root, text="Save Profile")
        self.save_button.pack()

        self.load_button = tk.Button(root, text="Load Profiles")
        self.load_button.pack()

        self.delete_button = tk.Button(root, text="Delete Profile")
        self.delete_button.pack()

        self.shop_button = tk.Button(root, text="Find PC Shops")
        self.shop_button.pack()

        # Creates the list area to display database records and map results
        self.listbox = tk.Listbox(root, width=70)
        self.listbox.pack()