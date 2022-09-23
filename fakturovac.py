import tkinter as tk
from tkinter import ttk
from jinja2 import Template


def load_template():
    with open("./assets/faktura.html", "r") as file:
        template = Template(file.read())
        return template


def main():
    root = tk.Tk()
    root.title("Fakturovac")

    root.mainloop()


if __name__ == "__main__":
    main()
