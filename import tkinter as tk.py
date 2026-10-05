import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw, ImageFont
import sqlite3
import qrcode
import os


# ---------------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------------

conn = sqlite3.connect("employees.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    gender TEXT,
    age TEXT,
    dob TEXT,
    blood_group TEXT,
    department TEXT,
    designation TEXT,
    mobile TEXT,
    email TEXT,
    address TEXT,
    photo TEXT
)
""")

conn.commit()


# ---------------------------------------------------------
# MAIN WINDOW
# ---------------------------------------------------------

root = tk.Tk()
root.title("Employee ID Card Generator")
root.geometry("900x650")
root.configure(bg="#e8f0f8")


# ---------------------------------------------------------
# VARIABLES
# ---------------------------------------------------------

employee_id = tk.StringVar()
name = tk.StringVar()
gender = tk.StringVar()
age = tk.StringVar()
dob = tk.StringVar()
blood_group = tk.StringVar()
department = tk.StringVar()
designation = tk.StringVar()
mobile = tk.StringVar()
email = tk.StringVar()

photo_path = ""


# ---------------------------------------------------------
# TITLE
# ---------------------------------------------------------

title = tk.Label(
    root,
    text="EMPLOYEE ID CARD GENERATOR",
    font=("Arial", 24, "bold"),
    bg="#1f4e78",
    fg="white",
    pady=15
)

title.pack(fill="x")


# ---------------------------------------------------------
# FORM FRAME
# ---------------------------------------------------------

form_frame = tk.Frame(root, bg="#e8f0f8")
form_frame.pack(pady=20)


def create_label(text, row, column):
    label = tk.Label(
        form_frame,
        text=text,
        font=("Arial", 11, "bold"),
        bg="#e8f0f8"
    )
    label.grid(row=row, column=column, padx=10, pady=8, sticky="w")


def create_entry(variable, row, column):
    entry = tk.Entry(
        form_frame,
        textvariable=variable,
        width=25,
        font=("Arial", 11)
    )
    entry.grid(row=row, column=column, padx=10, pady=8)
    return entry


# ---------------------------------------------------------
# EMPLOYEE DETAILS
# ---------------------------------------------------------

create_label("Employee ID", 0, 0)
create_entry(employee_id, 0, 1)

create_label("Employee Name", 0, 2)
create_entry(name, 0, 3)

create_label("Gender", 1, 0)
create_entry(gender, 1, 1)

create_label("Age", 1, 2)
create_entry(age, 1, 3)

create_label("Date of Birth", 2, 0)
create_entry(dob, 2, 1)

create_label("Blood Group", 2, 2)
create_entry(blood_group, 2, 3)

create_label("Department", 3, 0)
create_entry(department, 3, 1)

create_label("Designation", 3, 2)
create_entry(designation, 3, 3)

create_label("Mobile Number", 4, 0)
create_entry(mobile, 4, 1)

create_label("Email", 4, 2)
create_entry(email, 4, 3)


# ---------------------------------------------------------
# ADDRESS
# ---------------------------------------------------------

create_label("Address", 5, 0)

address_entry = tk.Entry(
    form_frame,
    width=60,
    font=("Arial", 11)
)

address_entry.grid(
    row=5,
    column=1,
    columnspan=3,
    padx=10,
    pady=8
)


# ---------------------------------------------------------
# PHOTO SELECTION
# ---------------------------------------------------------

def select_photo():

    global photo_path

    photo_path = filedialog.askopenfilename(
        title="Select Employee Photo",
        filetypes=[
            ("Image Files", "*.jpg *.jpeg *.png")
        ]
    )

    if photo_path:
        photo_label.config(
            text="Photo Selected",
            fg="green"
        )


photo_button = tk.Button(
    form_frame,
    text="Select Employee Photo",
    command=select_photo,
    bg="#3498db",
    fg="white",
    font=("Arial", 10, "bold"),
    width=20
)

photo_button.grid(
    row=6,
    column=1,
    pady=10
)

photo_label = tk.Label(
    form_frame,
    text="No Photo Selected",
    bg="#e8f0f8",
    fg="red"
)

photo_label.grid(
    row=6,
    column=2
)


# ---------------------------------------------------------
# SAVE EMPLOYEE
# ---------------------------------------------------------

def save_employee():

    if employee_id.get() == "":
        messagebox.showerror(
            "Error",
            "Please enter Employee ID"
        )
        return

    if name.get() == "":
        messagebox.showerror(
            "Error",
            "Please enter Employee Name"
        )
        return

    if department.get() == "":
        messagebox.showerror(
            "Error",
            "Please enter Department"
        )
        return

    try:

        cursor.execute("""
        INSERT INTO employees
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            employee_id.get(),
            name.get(),
            gender.get(),
            age.get(),
            dob.get(),
            blood_group.get(),
            department.get(),
            designation.get(),
            mobile.get(),
            email.get(),
            address_entry.get(),
            photo_path
        ))

        conn.commit()

        messagebox.showinfo(
            "Success",
            "Employee details saved successfully!"
        )

    except sqlite3.IntegrityError:

        messagebox.showerror(
            "Error",
            "Employee ID already exists!"
        )


# ---------------------------------------------------------
# GENERATE QR CODE
# ---------------------------------------------------------

def generate_qr():

    if employee_id.get() == "":
        messagebox.showerror(
            "Error",
            "Enter Employee ID first"
        )
        return

    qr_data = f"""
Employee ID: {employee_id.get()}
Name: {name.get()}
Department: {department.get()}
Designation: {designation.get()}
Mobile: {mobile.get()}
"""

    qr = qrcode.make(qr_data)

    filename = employee_id.get() + "_QR.png"

    qr.save(filename)

    return filename


# ---------------------------------------------------------
# GENERATE ID CARD
# ---------------------------------------------------------

def generate_id_card():

    if employee_id.get() == "":
        messagebox.showerror(
            "Error",
            "Please enter Employee ID"
        )
        return

    if name.get() == "":
        messagebox.showerror(
            "Error",
            "Please enter Employee Name"
        )
        return

    qr_file = generate_qr()

    # ID CARD SIZE
    width = 600
    height = 850

    card = Image.new(
        "RGB",
        (width, height),
        "white"
    )

    draw = ImageDraw.Draw(card)

    # -----------------------------------------------------
    # HEADER
    # -----------------------------------------------------

    draw.rectangle(
        (0, 0, width, 120),
        fill="#1f4e78"
    )

    try:
        title_font = ImageFont.truetype(
            "arial.ttf",
            32
        )

        sub_font = ImageFont.truetype(
            "arial.ttf",
            20
        )

        normal_font = ImageFont.truetype(
            "arial.ttf",
            22
        )

    except:

        title_font = ImageFont.load_default()
        sub_font = ImageFont.load_default()
        normal_font = ImageFont.load_default()


    draw.text(
        (width // 2, 35),
        "ABC COMPANY",
        fill="white",
        font=title_font,
        anchor="mm"
    )

    draw.text(
        (width // 2, 85),
        "EMPLOYEE ID CARD",
        fill="white",
        font=sub_font,
        anchor="mm"
    )


    # -----------------------------------------------------
    # EMPLOYEE PHOTO
    # -----------------------------------------------------

    if photo_path and os.path.exists(photo_path):

        try:

            photo = Image.open(photo_path)
            photo = photo.resize((180, 180))

            card.paste(
                photo,
                (210, 145)
            )

        except:

            draw.rectangle(
                (210, 145, 390, 325),
                outline="black"
            )

    else:

        draw.rectangle(
            (210, 145, 390, 325),
            outline="black"
        )

        draw.text(
            (300, 235),
            "PHOTO",
            fill="black",
            font=normal_font,
            anchor="mm"
        )


    # -----------------------------------------------------
    # EMPLOYEE NAME
    # -----------------------------------------------------

    draw.text(
        (width // 2, 365),
        name.get(),
        fill="black",
        font=title_font,
        anchor="mm"
    )

    draw.text(
        (width // 2, 405),
        designation.get(),
        fill="gray",
        font=sub_font,
        anchor="mm"
    )


    # -----------------------------------------------------
    # EMPLOYEE DETAILS
    # -----------------------------------------------------

    details = [
        ("Employee ID", employee_id.get()),
        ("Gender", gender.get()),
        ("Age", age.get()),
        ("DOB", dob.get()),
        ("Blood Group", blood_group.get()),
        ("Department", department.get()),
        ("Mobile", mobile.get()),
        ("Email", email.get())
    ]

    y = 455

    for label, value in details:

        draw.text(
            (80, y),
            label + ":",
            fill="black",
            font=normal_font
        )

        draw.text(
            (280, y),
            value,
            fill="black",
            font=normal_font
        )

        y += 38


    # -----------------------------------------------------
    # QR CODE
    # -----------------------------------------------------

    if qr_file and os.path.exists(qr_file):

        qr_image = Image.open(qr_file)

        qr_image = qr_image.resize(
            (120, 120)
        )

        card.paste(
            qr_image,
            (420, 680)
        )


    # -----------------------------------------------------
    # FOOTER
    # -----------------------------------------------------

    draw.rectangle(
        (0, 800, width, 850),
        fill="#1f4e78"
    )

    draw.text(
        (width // 2, 825),
        "VALID EMPLOYEE",
        fill="white",
        font=sub_font,
        anchor="mm"
    )


    # -----------------------------------------------------
    # SAVE CARD
    # -----------------------------------------------------

    filename = (
        employee_id.get()
        + "_Employee_ID_Card.png"
    )

    card.save(filename)

    messagebox.showinfo(
        "Success",
        "Employee ID Card generated successfully!\n\n"
        + filename
    )


# ---------------------------------------------------------
# SEARCH EMPLOYEE
# ---------------------------------------------------------

def search_employee():

    emp_id = employee_id.get()

    if emp_id == "":
        messagebox.showerror(
            "Error",
            "Enter Employee ID"
        )
        return

    cursor.execute(
        "SELECT * FROM employees WHERE employee_id=?",
        (emp_id,)
    )

    data = cursor.fetchone()

    if data:

        employee_id.set(data[0])
        name.set(data[1])
        gender.set(data[2])
        age.set(data[3])
        dob.set(data[4])
        blood_group.set(data[5])
        department.set(data[6])
        designation.set(data[7])
        mobile.set(data[8])
        email.set(data[9])

        address_entry.delete(
            0,
            tk.END
        )

        address_entry.insert(
            0,
            data[10]
        )

        messagebox.showinfo(
            "Employee Found",
            "Employee details loaded successfully!"
        )

    else:

        messagebox.showerror(
            "Not Found",
            "Employee not found!"
        )


# ---------------------------------------------------------
# CLEAR FORM
# ---------------------------------------------------------

def clear_form():

    employee_id.set("")
    name.set("")
    gender.set("")
    age.set("")
    dob.set("")
    blood_group.set("")
    department.set("")
    designation.set("")
    mobile.set("")
    email.set("")

    address_entry.delete(
        0,
        tk.END
    )

    global photo_path
    photo_path = ""

    photo_label.config(
        text="No Photo Selected",
        fg="red"
    )


# ---------------------------------------------------------
# BUTTON FRAME
# ---------------------------------------------------------

button_frame = tk.Frame(
    root,
    bg="#e8f0f8"
)

button_frame.pack(pady=15)


save_button = tk.Button(
    button_frame,
    text="SAVE EMPLOYEE",
    command=save_employee,
    bg="#27ae60",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
)

save_button.grid(
    row=0,
    column=0,
    padx=8
)


generate_button = tk.Button(
    button_frame,
    text="GENERATE ID CARD",
    command=generate_id_card,
    bg="#2980b9",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
)

generate_button.grid(
    row=0,
    column=1,
    padx=8
)


search_button = tk.Button(
    button_frame,
    text="SEARCH EMPLOYEE",
    command=search_employee,
    bg="#8e44ad",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
)

search_button.grid(
    row=0,
    column=2,
    padx=8
)


clear_button = tk.Button(
    button_frame,
    text="CLEAR",
    command=clear_form,
    bg="#e67e22",
    fg="white",
    font=("Arial", 11, "bold"),
    width=18
)

clear_button.grid(
    row=0,
    column=3,
    padx=8
)


# ---------------------------------------------------------
# EXIT BUTTON
# ---------------------------------------------------------

exit_button = tk.Button(
    root,
    text="EXIT",
    command=root.destroy,
    bg="#c0392b",
    fg="white",
    font=("Arial", 11, "bold"),
    width=15
)

exit_button.pack(pady=10)


# ---------------------------------------------------------
# START APPLICATION
# ---------------------------------------------------------

root.mainloop()


# ---------------------------------------------------------
# CLOSE DATABASE
# ---------------------------------------------------------

conn.close()