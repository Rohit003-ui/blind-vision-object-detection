import tkinter as tk
import subprocess
import time

def run_python_script():
        # Running the Python script
        subprocess.run(['python', 'main_code.py'])

def submit_form():
    name = name_entry.get()
    email = email_entry.get()
    message = message_entry.get("1.0", tk.END)

    if name and email and message.strip():
        print(f"Name: {name}")
        print(f"Email: {email}")
        print(f"Message: {message}")
        tk.messagebox.showinfo("Thank You!", "Message submitted successfully!")
    else:
        tk.messagebox.showwarning("Incomplete Form", "Please fill all fields.")

def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb

def gradient_effect(start_color, end_color, steps, frame):
    for i in range(steps + 1):
        red = int(start_color[0] + (end_color[0] - start_color[0]) * i / steps)
        green = int(start_color[1] + (end_color[1] - start_color[1]) * i / steps)
        blue = int(start_color[2] + (end_color[2] - start_color[2]) * i / steps)
        color = rgb_to_hex((red, green, blue))
        
        frame.config(bg=color)
        root.update()
        time.sleep(0.01)

# Initialize tkinter window
root = tk.Tk()
root.title("Blind Vision")
root.geometry("800x600")
root.config(bg="#f8f9fa")

# font styles
header_font = ("Poppins", 24, "bold")
subheader_font = ("Poppins", 18)
text_font = ("Poppins", 14)

# Navigation (Header Section) 
header_frame = tk.Frame(root, bg="#333")
header_frame.pack(fill="x")

header_label = tk.Label(header_frame, text="Blind Vision", font=header_font, fg="white", bg="#333")
header_label.pack(side="left", padx=20)

nav_buttons = ["Home", "About", "Projects", "Contact"]
for nav in nav_buttons:
    tk.Button(header_frame, text=nav, font=text_font, bg="#555", fg="white").pack(side="right", padx=10)

# Home Section Gradient
home_frame = tk.Frame(root, pady=20)
home_frame.pack(fill="both", expand=True)

home_title = tk.Label(home_frame, text="Welcome to Blind Vision", font=header_font)
home_title.pack(pady=10)

home_description = tk.Label(home_frame, text="Explore cutting-edge computer vision project. Discover tutorials, resources, and innovative solutions for your next AI-based vision project!", font=text_font, wraplength=600)
home_description.pack(pady=10)

try_button = tk.Button(home_frame, text="Try This", font=subheader_font, command=run_python_script)
try_button.pack(pady=20)

# Add a gradient effect between two colors (light blue to light purple)
root.after(0, gradient_effect, (173, 216, 230), (230, 173, 216), 100, home_frame)

#  About Section 
about_frame = tk.Frame(root, pady=20)
about_frame.pack(fill="both", expand=True)

about_title = tk.Label(about_frame, text="About Blind Vision", font=header_font)
about_title.pack(pady=10)

about_description = tk.Label(about_frame, text="Our project is dedicated to showcasing the power and potential of computer vision technology.", font=text_font, wraplength=600)
about_description.pack(pady=10)

vision_label = tk.Label(about_frame, text="Our Vision", font=subheader_font)
vision_label.pack(pady=5)

vision_description = tk.Label(about_frame, text="We envision a world where computer vision can be integrated into everyday life.", font=text_font, wraplength=600)
vision_description.pack(pady=5)

#  Projects Section 
projects_frame = tk.Frame(root, pady=20)
projects_frame.pack(fill="both", expand=True)

projects_title = tk.Label(projects_frame, text="Blind Vision for the Visually Impaired", font=header_font)
projects_title.pack(pady=10)

projects_description = tk.Label(projects_frame, text="This project serves as a real-time solution for the blind, helping people in their daily lives.", font=text_font, wraplength=600)
projects_description.pack(pady=10)

#  Contact Section 
contact_frame = tk.Frame(root, pady=20)
contact_frame.pack(fill="both", expand=True)

contact_title = tk.Label(contact_frame, text="Contact Us", font=header_font)
contact_title.pack(pady=10)

form_frame = tk.Frame(contact_frame)
form_frame.pack(pady=10)

# Form elements (Name, Email, Message)
tk.Label(form_frame, text="Name:", font=text_font).grid(row=0, column=0, sticky="w", padx=10, pady=5)
name_entry = tk.Entry(form_frame, font=text_font, width=40)
name_entry.grid(row=0, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Email:", font=text_font).grid(row=1, column=0, sticky="w", padx=10, pady=5)
email_entry = tk.Entry(form_frame, font=text_font, width=40)
email_entry.grid(row=1, column=1, padx=10, pady=5)

tk.Label(form_frame, text="Message:", font=text_font).grid(row=2, column=0, sticky="nw", padx=10, pady=5)
message_entry = tk.Text(form_frame, font=text_font, width=40, height=5)
message_entry.grid(row=2, column=1, padx=10, pady=5)

submit_button = tk.Button(contact_frame, text="Send Message", font=subheader_font, command=submit_form)
submit_button.pack(pady=10)

# Starting tkinter main loop
root.mainloop()
