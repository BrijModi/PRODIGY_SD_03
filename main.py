from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector


# Connect to MySQL
def connect_to_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="2714",
        database="contact_db"
    )


# Window
Window = Tk()
Window.title('Contacts')
Window.resizable(False, False)
Window.geometry('600x500')


# Images
def make_image_transparent(img_path):
    image = Image.open(img_path).convert("RGBA")
    data = image.getdata()
    new_data = [(255, 255, 255, 0) if item[0] > 200 and item[1] > 200 and item[2] > 200 else item for item in data]
    image.putdata(new_data)
    return image

canvas = Canvas(Window, width=600, height=650)
canvas.pack()

bg_image = ImageTk.PhotoImage(Image.open("fade1.png"))
canvas.create_image(0, 0, anchor=NW, image=bg_image)

top_image = ImageTk.PhotoImage(make_image_transparent("Contacts.png"))
canvas.create_image(230, 75, anchor=NW, image=top_image)


# Add a Contact Button
def Add_Contact():
    
    # Save Contact to database
    def save_contact():
        name = Name_entry.get()
        phone = int(Number_entry.get())
        email = Email_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        
        query = "INSERT INTO contacts (name, phone, email) VALUES (%s, %s, %s)"
        try:
            cursor.execute(query, (name, phone, email))
            conn.commit()
            messagebox.showinfo("Success", "Contact added successfully")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error: {err}")
        
        cursor.close()
        conn.close()
        
        Add.destroy()

    # Window
    Add = Toplevel(Window, bg='#60C9F3')
    Add.geometry('550x450')
    Add.resizable(False, False)
    Add.title('Add Contact')

    # Labels
    Label(Add, text='Enter User Name :', font=('Comic Sans', 14), bg='#60C9F3').place(x=44, y=80)
    Label(Add, text='Enter Phone Number :', font=('Comic Sans', 14), bg='#60C9F3').place(x=44, y=150)
    Label(Add, text='Enter Email Address :', font=('Comic Sans', 14), bg='#60C9F3').place(x=44, y=220)

    # Entry
    Name_entry = Entry(Add, font=('Comic Sans', 14), width=18, border=3)
    Name_entry.place(x=210, y=78)
    Number_entry = Entry(Add, font=('Comic Sans', 14), width=18, border=3)
    Number_entry.place(x=241, y=148)
    Email_entry = Entry(Add, font=('Comic Sans', 14), width=24, border=3)
    Email_entry.place(x=238, y=218)

    # Add Button
    Button(Add, text='Add', font=('Comic Sans', 14), width=10, border=5, command=save_contact).place(x=220, y=310)

Add_Button = Button(Window,
                    text='Add Contact',
                    font=('Comic Sans', 14),
                    width=20,
                    border=5,
                    relief=RAISED,
                    command=Add_Contact
                    )
Add_Button.place(x=180, y=280)


# View a Contact Button
def View_Contact():
    
    # Function to fetch and display contacts
    def fetch_contacts(view_window):
        conn = connect_to_db()
        cursor = conn.cursor()

        query = "SELECT * FROM contacts"
        cursor.execute(query)
        contacts = cursor.fetchall()

        if not contacts:
            Label(view_window, text="No contacts found", bg='#60C9F3', font=('Comic Sans', 22, 'bold')).place(x=320, y=300)
        else:
            # Define headers
            headers = ["Name", "Phone", "Email", "Edit", "Delete"]
            for col, header in enumerate(headers):
                Label(view_window,
                        text=header,
                        bg='#60C9F3',
                        font=('Comic Sans', 14, 'bold')).grid(row=0, column=col, padx=40, pady=10)

            # Display contacts
            for row, contact in enumerate(contacts, start=1):
                for col, detail in enumerate(contact):
                    Label(view_window,
                            text=detail,
                            bg='#60C9F3',
                            font=('Comic Sans', 14)).grid(row=row, column=col, padx=40, pady=10)

                # Edit button
                Button(view_window,
                        text="Edit",
                        border=3,
                        font=('Comic Sans', 13),
                        command=lambda c=contact: edit_contact(c, view_window)).grid(row=row,column=len(contact), padx=20, pady=10)

                # Delete button
                Button(view_window,
                        text="Delete",
                        border=3,
                        font=('Comic Sans', 13),
                        command=lambda p=contact[1]: delete_contact(p, view_window)).grid(row=row, column=len(contact) + 1, padx=20, pady=10)

        cursor.close()
        conn.close()

    # Function to delete contact from database
    def delete_contact(phone, view_window):
        conn = connect_to_db()
        cursor = conn.cursor()
        
        query = "DELETE FROM contacts WHERE phone = %s"
        cursor.execute(query, (phone,))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        messagebox.showinfo("Success", "Contact deleted successfully")
        view_window.destroy()  # Close the view window

    # Window
    View = Toplevel(Window, bg='#60C9F3')
    View.geometry('900x650')
    View.resizable(False, False)
    View.title('View Contacts')

    fetch_contacts(View)

# Function to edit a contact
def edit_contact(contact, view_window):
    def save_edits():
        new_name = name_entry.get()
        new_phone = int(phone_entry.get())
        new_email = email_entry.get()

        conn = connect_to_db()
        cursor = conn.cursor()
        
        query = "UPDATE contacts SET name = %s, phone = %s, email = %s WHERE phone = %s"
        cursor.execute(query, (new_name, new_phone, new_email, contact[1]))
        conn.commit()
        
        cursor.close()
        conn.close()
        
        messagebox.showinfo("Success", "Contact updated successfully")
        edit_win.destroy()  # Close the edit window
        view_window.destroy()  # Optionally close the view window as well

    edit_win = Toplevel(Window, bg='#60C9F3')
    edit_win.geometry('550x350')
    edit_win.resizable(False, False)
    edit_win.title('Edit Contact')

    Label(edit_win, text='Edit User Name:', font=('Comic Sans', 14), bg='#60C9F3').place(x=44, y=50)
    Label(edit_win, text='Edit Phone Number:', font=('Comic Sans', 14), bg='#60C9F3').place(x=44, y=120)
    Label(edit_win, text='Edit Email Address:', font=('Comic Sans', 14), bg='#60C9F3').place(x=44, y=190)

    name_entry = Entry(edit_win, font=('Comic Sans', 14), width=24, border=3)
    name_entry.place(x=230, y=48)
    name_entry.insert(0, contact[0])

    phone_entry = Entry(edit_win, font=('Comic Sans', 14), width=24, border=3)
    phone_entry.place(x=230, y=118)
    phone_entry.insert(0, contact[1])

    email_entry = Entry(edit_win, font=('Comic Sans', 14), width=24, border=3)
    email_entry.place(x=230, y=188)
    email_entry.insert(0, contact[2])

    Button(edit_win, 
            text='Save',
            font=('Comic Sans', 14),
            width=10,
            border=5,
            command=save_edits).place(x=220, y=250)

View_Button = Button(Window,
                    text='View Contacts',
                    font=('Comic Sans', 14),
                    width=20,
                    border=5,
                    relief=RAISED,
                    command=View_Contact
                    )
View_Button.place(x=180, y=350)


# Running in loop
Window.mainloop()

