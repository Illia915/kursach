import tkinter as tk
from models import CollectionModel
from controller import MainController
from views import MainView


def main():
    root = tk.Tk()
    model = CollectionModel()
    controller = MainController(model)
    view = MainView(root, controller)
    controller.set_view(view)
    controller.startup()
    root.mainloop()


if __name__ == "__main__":
    main()
