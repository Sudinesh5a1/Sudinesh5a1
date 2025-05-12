# gui_brute_force_simulator.py
import itertools
import string
import time
import tkinter as tk
from tkinter import messagebox
def brute_force_gui(target_password, output_label):
    characters = string.ascii_lowercase + string.digits
    attempts = 0
    start_time = time.time()
    for password_length in range(1, 5):  # Max 4 characters
        for guess in itertools.product(characters, repeat=password_length):
            guess_password = ''.join(guess)
            attempts += 1
            output_label.config(text=f"Trying: {guess_password}")
            root.update()
            if guess_password == target_password:
                end_time = time.time()
                messagebox.showinfo(
                    "Password Cracked",
                    f"Password: {guess_password}\nAttempts: {attempts}\nTime: {end_time - start_time:.2f}s"
                )
                return
    messagebox.showwarning("Failed", "Could not crack the password.")
def start_brute_force():
    password = password_entry.get()
    if not password:
        messagebox.showerror("Input Error", "Please enter a password to crack.")
        return
    if len(password) > 4:
        messagebox.showerror("Input Error", "Max 4 characters allowed (a-z, 0-9)")
        return
    brute_force_gui(password, output_label)
# GUI Setup
root = tk.Tk()
root.title("Brute Force Simulator")
root.geometry("400x250")
root.resizable(False, False)
tk.Label(root, text="Enter Password (Max 4 chars, a-z, 0-9):", font=("Arial", 12)).pack(pady=10)
password_entry = tk.Entry(root, font=("Arial", 14), justify="center")
password_entry.pack(pady=5)
tk.Button(root, text="Start Brute Force", command=start_brute_force, font=("Arial", 12), bg="red", fg="white").pack(pady=15)
output_label = tk.Label(root, text="", font=("Arial", 12))
output_label.pack(pady=10)
tk.Label(root, text="For demo use only – Educational Purpose", font=("Arial", 8)).pack(side="bottom", pady=5)
root.mainloop()
