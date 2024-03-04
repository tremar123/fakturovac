import tkinter as tk
import json
import datetime
import tempfile
import pay_by_square
import qrcode
import pdfkit
import os
from tkinter import END, MULTIPLE, Menu, Toplevel, ttk, messagebox
from tkinter.filedialog import asksaveasfilename
from jinja2 import Template

root = tk.Tk()

current_date = datetime.datetime.now()
current_year = current_date.date().strftime("%Y")


def load_template():
    with open(os.path.join(os.path.dirname(__file__), "faktura.html"), "r") as file:
        template = Template(file.read())
        return template


def user_data_edit_window():
    win = Toplevel(root)
    win.title("Nastavenia")
    win.attributes("-type", "topmost")

    user_name_label = ttk.Label(win, text="Meno a priezvisko")
    user_name_label.grid(row=0, column=0)
    user_name_entry = ttk.Entry(win)
    user_name_entry.grid(row=0, column=1)

    user_address_label = ttk.Label(win, text="Adresa")
    user_address_label.grid(row=1, column=0)
    user_address_entry = ttk.Entry(win)
    user_address_entry.grid(row=1, column=1)

    user_city_label = ttk.Label(win, text="PSČ, mesto")
    user_city_label.grid(row=2, column=0)
    user_city_entry = ttk.Entry(win)
    user_city_entry.grid(row=2, column=1)

    user_country_label = ttk.Label(win, text="Krajina")
    user_country_label.grid(row=3, column=0)
    user_country_entry = ttk.Entry(win)
    user_country_entry.grid(row=3, column=1)

    user_ico_label = ttk.Label(win, text="IČO")
    user_ico_label.grid(row=4, column=0)
    user_ico_entry = ttk.Entry(win)
    user_ico_entry.grid(row=4, column=1)

    user_dic_label = ttk.Label(win, text="DIČ")
    user_dic_label.grid(row=5, column=0)
    user_dic_entry = ttk.Entry(win)
    user_dic_entry.grid(row=5, column=1)

    user_email_label = ttk.Label(win, text="Email")
    user_email_label.grid(row=6, column=0)
    user_email_entry = ttk.Entry(win)
    user_email_entry.grid(row=6, column=1)

    user_IBAN_label = ttk.Label(win, text="IBAN")
    user_IBAN_label.grid(row=7, column=0)
    user_IBAN_entry = ttk.Entry(win)
    user_IBAN_entry.grid(row=7, column=1)

    user_SWIFT_label = ttk.Label(win, text="SWIFT")
    user_SWIFT_label.grid(row=8, column=0)
    user_SWIFT_entry = ttk.Entry(win)
    user_SWIFT_entry.grid(row=8, column=1)

    user_btn_cancel = ttk.Button(win, text="Zrušiť", command=win.destroy)
    user_btn_cancel.grid(row=9, column=0)

    try:
        with open(os.path.join(os.path.dirname(__file__), "data.json"), "r") as file:
            data = json.load(file)
            user_name_entry.insert(0, data["name"])
            user_address_entry.insert(0, data["address"])
            user_city_entry.insert(0, data["city"])
            user_country_entry.insert(0, data["country"])
            user_ico_entry.insert(0, data["ico"])
            user_dic_entry.insert(0, data["dic"])
            user_email_entry.insert(0, data["email"])
            user_IBAN_entry.insert(0, data["iban"])
            user_SWIFT_entry.insert(0, data["swift"])
    except FileNotFoundError or json.decoder.JSONDecodeError:
        pass

    def save_user_data():
        with open(os.path.join(os.path.dirname(__file__), "data.json"), "w") as file:
            newData = {
                "name": user_name_entry.get(),
                "address": user_address_entry.get(),
                "city": user_city_entry.get(),
                "country": user_country_entry.get(),
                "ico": user_ico_entry.get(),
                "dic": user_dic_entry.get(),
                "email": user_email_entry.get(),
                "iban": user_IBAN_entry.get(),
                "swift": user_SWIFT_entry.get(),
            }
            json.dump(newData, file)
        win.destroy()

    user_btn_save = ttk.Button(win, text="Uložiť", command=save_user_data)
    user_btn_save.grid(row=9, column=1)


def load_user_data():
    try:
        with open(os.path.join(os.path.dirname(__file__), "data.json"), "r") as file:
            return json.load(file)
    except FileNotFoundError:
        # NOTE: after this i need to read the file, can this be done with async?
        # user_data_edit_window()
        messagebox.showinfo("Vyplňte údaje", "Edit > Nastavenia")


def add_product():
    if product_name_entry.get() == "" or product_count_entry.get() == "" or product_price_entry.get() == "":
        messagebox.showerror("Vyžadované políčka", "Vyplňte všetky políčka")
        return
    products_list.insert(
        END, f"{product_name_entry.get()} - {product_count_entry.get()}ks - {product_price_entry.get()}€/ks")
    product_name_entry.delete(0, END)
    product_price_entry.delete(0, END)
    product_count_entry.delete(0, END)


def remove_product():
    # BUG: this is not deleting everything that is selected
    for product in products_list.curselection():
        products_list.delete(product)


def clear_products():
    products_list.delete(0, END)


template = load_template()

root.title("Fakturovac")

menu = tk.Menu(root)
editMenu = Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=editMenu)
editMenu.add_command(label="Nastavenia", command=user_data_edit_window)

root.config(menu=menu)

# client data
name_label = ttk.Label(root, text="Meno a priezvisko")
name_label.grid(row=0, column=0)
name_entry = ttk.Entry(root)
name_entry.grid(row=0, column=1)

address_label = ttk.Label(root, text="Adresa")
address_label.grid(row=1, column=0)
address_entry = ttk.Entry(root)
address_entry.grid(row=1, column=1)

city_label = ttk.Label(root, text="PSČ, mesto")
city_label.grid(row=2, column=0)
city_entry = ttk.Entry(root)
city_entry.grid(row=2, column=1)

country_label = ttk.Label(root, text="Krajina")
country_label.grid(row=3, column=0)
country_entry = ttk.Entry(root)
country_entry.grid(row=3, column=1)

ico_label = ttk.Label(root, text="IČO")
ico_label.grid(row=4, column=0)
ico_entry = ttk.Entry(root)
ico_entry.grid(row=4, column=1)

icdph_label = ttk.Label(root, text="IČ DPH")
icdph_label.grid(row=5, column=0)
icdph_entry = ttk.Entry(root)
icdph_entry.grid(row=5, column=1)

dic_label = ttk.Label(root, text="DIČ")
dic_label.grid(row=6, column=0)
dic_entry = ttk.Entry(root)
dic_entry.grid(row=6, column=1)

# list of products

product_name_label = ttk.Label(root, text="Názov")
product_name_label.grid(row=0, column=2)
product_name_entry = ttk.Entry(root)
product_name_entry.grid(row=0, column=3)

product_count_label = ttk.Label(root, text="Počet")
product_count_label.grid(row=1, column=2)
product_count_entry = ttk.Entry(root)
product_count_entry.grid(row=1, column=3)

product_price_label = ttk.Label(root, text="Cena za kus")
product_price_label.grid(row=2, column=2)
product_price_entry = ttk.Entry(root)
product_price_entry.grid(row=2, column=3)

const_label = ttk.Label(root, text="Konštantý symbol")
const_label.grid(row=7, column=0)
const_entry = ttk.Entry(root)
const_entry.grid(row=7, column=1, pady=20)

id_label = ttk.Label(root, text="ID")
id_label.grid(row=7, column=2)
id_entry = ttk.Entry(root)
id_entry.grid(row=7, column=3, pady=20)

products_list_label = ttk.Label(root, text="Produkty")
products_list_label.grid(row=8, column=0)

products_list_scrollbar = ttk.Scrollbar(root)
products_list_scrollbar.grid(row=9, column=4, sticky="nesw", pady=(0, 20))

products_list = tk.Listbox(root, selectmode=MULTIPLE)
products_list.configure(yscrollcommand=products_list_scrollbar.set)
products_list_scrollbar.configure(command=products_list.yview)
products_list.grid(row=9, column=0, columnspan=4, sticky="ew", pady=(0, 20))

product_add_btn = ttk.Button(root, text="Pridať", command=add_product)
product_add_btn.grid(row=3, column=3, rowspan=2)

product_remove_btn = ttk.Button(root, text="Odstrániť", command=remove_product)
product_remove_btn.grid(row=13, column=1)

product_clear_btn = ttk.Button(
    root, text="Zmazať všetko", command=clear_products)
product_clear_btn.grid(row=13, column=2)


def render_template():
    products = []

    overall_sum = 0

    for product in products_list.get(0, END):
        p = product.split(" - ")
        price_sum = float(p[1][:-2]) * float(p[2][:-4])
        overall_sum += price_sum

        products.append({
            "name": p[0],
            "count": p[1],
            "price": p[2],
            "price_sum": "{:.2f}".format(price_sum),
        })

    user_data = load_user_data()

    # this sucks
    if user_data == None:
        raise ValueError("Object can't be None!")

    id = f"{str(current_year)}{int(id_entry.get()):04d}"

    pay_code = pay_by_square.generate(
        amount=overall_sum,
        iban=user_data["iban"],
        swift=user_data["swift"],
        currency="EUR",
        variable_symbol=id,
        constant_symbol=const_entry.get(),
    )

    qr_code_img = qrcode.make(pay_code)

    with tempfile.TemporaryDirectory() as tmp_dir:
        qr_code_img.save(os.path.join(tmp_dir, "qr.png"))

        with open(os.path.join(tmp_dir, "render.html"), "w") as tmp_render:
            tmp_render.write(template.render(
                id=id,
                user_data=user_data,
                date_of_issue=current_date.date().strftime("%d. %m. %Y"),
                due_date=datetime.datetime.strftime(
                    current_date + datetime.timedelta(days=14), "%d. %m. %Y"),
                client={
                    "name": name_entry.get(),
                    "address": address_entry.get(),
                    "city": city_entry.get(),
                    "country": country_entry.get(),
                    "ico": ico_entry.get(),
                    "icdph": icdph_entry.get(),
                    "dic": dic_entry.get(),
                },
                products=products,
                sum="{:.2f}".format(overall_sum),
                const_sym=const_entry.get()
            ))

        save_as = asksaveasfilename(initialdir=os.path.expanduser("~"), initialfile=f"faktura_{id}.pdf", defaultextension=".pdf", filetypes=[
                                    ("Všetky súbory", "*.*"), ("Portable File Document", "*.pdf")])

        pdfkit.from_file(os.path.join(tmp_dir, "render.html"), save_as, options={
                         "enable-local-file-access": ""})


render_btn = ttk.Button(root, text="Vytvoriť faktúru", command=render_template)
render_btn.grid(row=14, column=0, columnspan=4, pady=20)

if __name__ == "__main__":
    root.mainloop()
