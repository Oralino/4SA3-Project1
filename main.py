import os
import tkinter as tk
from dotenv import load_dotenv
from models.database_model import ObjectPool
from controllers.app_controller import AppController
from views.main_window import EngineOptimizerView

# loads the hidden environment variables into the script
load_dotenv()

# retrieves the keys from the environment variables
MONGO_URI = os.getenv("MONGO_URI")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def main():
    # Creates the database connection pool
    db_pool = ObjectPool(MONGO_URI)

    # Initializes the controller with the connection pool and API key
    controller = AppController(db_pool, GOOGLE_API_KEY)

    # Starts the Tkinter window and links it to the controller
    root = tk.Tk()
    app = EngineOptimizerView(root, controller)
    root.mainloop()


if __name__ == "__main__":
    main()