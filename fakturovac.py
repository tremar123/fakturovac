import tkinter as tk
from tkinter import ttk


def main():
    root = tk.Tk()
    root.title("Fakturovac")

    ttk.Label(root, text="input").pack()
    ttk.Entry(root).pack()

    root.mainloop()


if __name__ == "__main__":
    main()
