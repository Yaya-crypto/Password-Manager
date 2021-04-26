import json
from tkinter import *
from tkinter import messagebox
from random import choice, randint, shuffle

import pyperclip

letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
           'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
           'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']


def generate_random_password():
    password_letters = [choice(letters) for letter in range(randint(8, 10))]
    password_symbols = [choice(symbols) for symbol in range(randint(2, 4))]
    password_numbers = [choice(numbers) for number in range(randint(2, 4))]

    password_list = password_numbers + password_symbols + password_letters
    shuffle(password_list)

    password = "".join(password_list)
    password_input.delete(0, END)
    password_input.insert(0, password)
    pyperclip.copy(password)


def add_pass():
    website = input_website.get()
    email = email_user_input.get()
    password = password_input.get()

    new_entry = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(password) == 0:
        messagebox.showinfo(title="Error", message=f"Fields cannot be empty")
    else:
        try:
            with open("password_file.json", mode="r") as file:
                # Read existing data
                data = json.load(file)
        except (FileNotFoundError, json.decoder.JSONDecodeError):
            with open("password_file.json", mode="w") as file:
                json.dump(new_entry, file, indent=4)
        else:
            # Updating data
            data.update(new_entry)

            with open("password_file.json", "w") as file:
                # Saving data
                json.dump(data, file, indent=4)
        finally:
            input_website.delete(0, END)
            # email_user_input.delete(0, END)
            password_input.delete(0, END)


def search_pass():
    website_to_search = input_website.get()
    try:
        with open("password_file.json") as file:
            json_data = json.load(file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error!", message="Data does not exist yet.")
    else:
        if website_to_search in json_data:
            # This is a nested dictionary
            email = json_data[website_to_search]["email"]
            password = json_data[website_to_search]["password"]
            messagebox.showinfo(title=website_to_search, message=f"Email: {email}\nPassword: {password}.")
        else:
            messagebox.showinfo(title="Error!", message=f"Website {website_to_search} is not saved.")


# User Interface
window = Tk()
window.title("Password Manager")
window.config(padx=30, pady=50)

canvas = Canvas(width=300, height=196, highlightthickness=0)

password_image = PhotoImage(file="passwordapp.png")
canvas.create_image(160, 98, image=password_image)
canvas.grid(column=1, row=0, columnspan=2)

website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

input_website = Entry(width=35)
input_website.focus()
input_website.grid(column=2, row=1, rowspan=2)

email_user_label = Label(text="Email/Username:")
email_user_label.grid(column=0, row=4)

email_user_input = Entry(width=35)
email_user_input.insert(0, "example@emailname.com")
email_user_input.grid(column=2, row=2, rowspan=4)

password_label = Label(text="Password:")
password_label.grid(column=0, row=7)

password_input = Entry(width=35)
password_input.grid(column=2, row=7)

generate_password_button = Button(text="Generate", width=10, command=generate_random_password)
generate_password_button.grid(column=3, row=7)

add_password_button = Button(text="Add", width=35, command=add_pass)
add_password_button.grid(column=2, row=8)

search_button = Button(text="Search", width=10, command=search_pass)
search_button.grid(column=3, row=1)

window.mainloop()
