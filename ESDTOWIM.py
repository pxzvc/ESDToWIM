import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
import threading

def select_esd_file():
    esd_file_path = filedialog.askopenfilename(filetypes=[("ESD files", "*.esd")])
    if esd_file_path:
        esd_entry.delete(0, tk.END)
        esd_entry.insert(0, esd_file_path)

def select_wim_directory():
    wim_directory_path = filedialog.askdirectory()
    if wim_directory_path:
        wim_entry.delete(0, tk.END)
        wim_entry.insert(0, wim_directory_path)

def get_esd_indexes():
    esd_file = esd_entry.get()
    if esd_file:
        command = f'dism /Get-WimInfo /WimFile:"{esd_file}"'
        try:
            output = os.popen(command).read()
            messagebox.showinfo("ESD Indexes", output)
        except Exception as e:
            print("An error occurred:", e)
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please select an ESD file.")

def convert_esd_to_wim():
    esd_file = esd_entry.get()
    wim_directory = wim_entry.get()
    index_number = index_entry.get()
    compression_option = compression_var.get()  # Get the selected compression option
    if esd_file and wim_directory and index_number and compression_option:
        wim_file = os.path.join(wim_directory, "install.wim")
        # Format the command with the user-selected compression option
        command = f'dism /export-image /SourceImageFile:"{esd_file}" /SourceIndex:{index_number} /DestinationImageFile:"{wim_file}" /CheckIntegrity /Compress:{compression_option}'
        try:
            convert_button.config(state=tk.DISABLED)
            threading.Thread(target=run_conversion, args=(command,)).start()
        except Exception as e:
            print("An error occurred:", e)
            messagebox.showerror("Error", f"An error occurred: {e}")
    else:
        messagebox.showerror("Error", "Please select ESD file, WIM directory, provide index number, and select compression option.")

def run_conversion(command):
    try:
        os.system(command)
        print("Conversion successful.")
        messagebox.showinfo("Success", "ESD file converted to WIM successfully.")
    except Exception as e:
        print("An error occurred:", e)
        messagebox.showerror("Error", f"An error occurred: {e}")
    finally:
        convert_button.config(state=tk.NORMAL)

# Create the main window
root = tk.Tk()
root.title("ESD To WIM v.3.1 - By pxzvc")
root.configure(bg='#2e2e2e')  # Set background color to match Photoshop's dark theme
root.resizable(False, False)  # Prevent window resizing

# Create style for buttons
style = ttk.Style()
style.configure('TButton', foreground='#2e2e2e', background='#2e2e2e', bordercolor='#2e2e2e')  # Set button colors

# Change background color of dropdown menu
style.map('TCombobox', fieldbackground=[('readonly', '#1f1f1f')])

# Compression options
compression_options = ["max", "fast", "none"]

# Create and place widgets
esd_label = tk.Label(root, text="ESD File:", bg='#2e2e2e', fg='#ffffff')
esd_label.grid(row=0, column=0, padx=5, pady=5, sticky="e")

esd_entry = tk.Entry(root, width=50)
esd_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

esd_button = ttk.Button(root, text="Select", command=select_esd_file)
esd_button.grid(row=0, column=3, padx=5, pady=5)

wim_label = tk.Label(root, text="WIM Directory:", bg='#2e2e2e', fg='#ffffff')
wim_label.grid(row=1, column=0, padx=5, pady=5, sticky="e")

wim_entry = tk.Entry(root, width=50)
wim_entry.grid(row=1, column=1, columnspan=2, padx=5, pady=5)

wim_button = ttk.Button(root, text="Select", command=select_wim_directory)
wim_button.grid(row=1, column=3, padx=5, pady=5)

index_label = tk.Label(root, text="Index Number:", bg='#2e2e2e', fg='#ffffff')
index_label.grid(row=2, column=0, padx=5, pady=5, sticky="e")

index_entry = tk.Entry(root, width=10)
index_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

get_index_button = ttk.Button(root, text="Get ESD Indexes", command=get_esd_indexes)
get_index_button.grid(row=2, column=2, padx=5, pady=5, sticky="w")

compression_label = tk.Label(root, text="Compression:", bg='#2e2e2e', fg='#ffffff')
compression_label.grid(row=3, column=0, padx=5, pady=5, sticky="e")

compression_var = tk.StringVar(root)
compression_var.set(compression_options[0])  # Set default compression option
compression_dropdown = ttk.Combobox(root, textvariable=compression_var, values=compression_options, state='readonly', width=15)
compression_dropdown.grid(row=3, column=1, columnspan=2, padx=5, pady=5, sticky="w")

# Convert button at bottom center
convert_button = ttk.Button(root, text="Convert", command=convert_esd_to_wim, width=30)
convert_button.grid(row=5, column=0, columnspan=4, padx=5, pady=10)

# Run the main event loop
root.mainloop()
