import subprocess
import re
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import queue
import time

class CyberWiFiViewer(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Cyber Wi-Fi Password Viewer")
        self.geometry("600x400")
        self.configure(bg="#0f0f1f")
        self.resizable(False, False)
        self.style = ttk.Style(self)
        self.style.theme_use('clam')

        # Configure style for Treeview
        self.style.configure("Treeview",
                             background="#1b1b2f",
                             foreground="cyan",
                             fieldbackground="#1b1b2f",
                             font=('Consolas', 11))
        self.style.map('Treeview', background=[('selected', '#0a0a1a')])

        # Treeview with striped rows
        self.tree = ttk.Treeview(self, columns=("SSID", "Password"), show='headings', selectmode='browse')
        self.tree.heading("SSID", text="Wi-Fi SSID")
        self.tree.heading("Password", text="Password")
        self.tree.column("SSID", width=250, anchor='w')
        self.tree.column("Password", width=320, anchor='w')

        self.tree.tag_configure('odd', background="#14142f")
        self.tree.tag_configure('even', background="#1e1e3b")

        self.tree.pack(pady=15, padx=15, fill='both', expand=True)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient='horizontal', length=580, mode='determinate')
        self.progress.pack(pady=(0,5))

        # Status label
        self.status_label = tk.Label(self, text="Status: Idle", fg="cyan", bg="#0f0f1f", font=('Consolas', 11))
        self.status_label.pack()

        # Control frame for buttons and search
        control_frame = tk.Frame(self, bg="#0f0f1f")
        control_frame.pack(pady=10)

        self.scan_btn = ttk.Button(control_frame, text="Start Scan", command=self.start_scan)
        self.scan_btn.grid(row=0, column=0, padx=10)

        self.copy_all_btn = ttk.Button(control_frame, text="Copy All Passwords", command=self.copy_all)
        self.copy_all_btn.grid(row=0, column=1, padx=10)
        self.copy_all_btn.config(state='disabled')

        tk.Label(control_frame, text="Search SSID:", fg="cyan", bg="#0f0f1f", font=('Consolas', 11)).grid(row=0, column=2, padx=(20,5))
        self.search_var = tk.StringVar()
        self.search_var.trace('w', self.filter_ssid)
        self.search_entry = ttk.Entry(control_frame, textvariable=self.search_var, width=25)
        self.search_entry.grid(row=0, column=3, padx=5)

        # Bind click on treeview to copy password
        self.tree.bind('<ButtonRelease-1>', self.copy_selected_password)

        self.passwords = []
        self.is_scanning = False
        self.queue = queue.Queue()

        # Poll queue for UI updates
        self.after(100, self.process_queue)

    def start_scan(self):
        if self.is_scanning:
            return
        self.is_scanning = True
        self.passwords.clear()
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.progress['value'] = 0
        self.status_label.config(text="Status: Starting scan...")
        self.scan_btn.config(state='disabled')
        self.copy_all_btn.config(state='disabled')
        threading.Thread(target=self._scan_passwords_thread, daemon=True).start()

    def _scan_passwords_thread(self):
        try:
            result = subprocess.run(['netsh', 'wlan', 'show', 'profiles'], capture_output=True, text=True, check=True)
            profiles = re.findall(r"All User Profile\s*:\s(.*)", result.stdout)
        except Exception as e:
            self.queue.put({'type':'status', 'text': f"Error scanning profiles: {e}"})
            self.is_scanning = False
            self.scan_btn.config(state='normal')
            return

        total = len(profiles)
        for idx, profile in enumerate(profiles):
            if not self.is_scanning:
                break
            profile = profile.strip()
            self.queue.put({'type':'status', 'text': f"Scanning {idx+1}/{total}: {profile}"})
            try:
                proc = subprocess.Popen(['netsh', 'wlan', 'show', 'profile', profile, 'key=clear'],
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        text=True)
                stdout, _ = proc.communicate(timeout=5)
                pwd_match = re.search(r"Key Content\s*:\s(.*)", stdout)
                password = pwd_match.group(1) if pwd_match else "<No Password>"
            except Exception:
                password = "<Error>"

            wifi_data = {"SSID": profile, "Password": password}
            self.passwords.append(wifi_data)
            self.queue.put({'type':'insert', 'wifi_data': wifi_data, 'index': idx})
            self.queue.put({'type':'progress', 'value': (idx+1)/total * 100})
            time.sleep(0.3)  # smooth animation delay

        self.queue.put({'type':'status', 'text': "Scan complete!"})
        self.queue.put({'type':'scan_done'})

    def process_queue(self):
        try:
            while True:
                task = self.queue.get_nowait()
                if task['type'] == 'progress':
                    self.progress['value'] = task['value']
                elif task['type'] == 'status':
                    self.status_label.config(text=f"Status: {task['text']}")
                elif task['type'] == 'insert':
                    idx = task['index']
                    wifi_data = task['wifi_data']
                    tag = 'even' if idx % 2 == 0 else 'odd'
                    self.tree.insert("", "end", values=(wifi_data["SSID"], wifi_data["Password"]), tags=(tag,))
                elif task['type'] == 'scan_done':
                    self.is_scanning = False
                    self.scan_btn.config(state='normal')
                    self.copy_all_btn.config(state='normal')
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def filter_ssid(self, *_):
        search_text = self.search_var.get().lower()
        for item in self.tree.get_children():
            ssid = self.tree.item(item)['values'][0].lower()
            if search_text in ssid:
                self.tree.item(item, tags=self.tree.item(item, 'tags'))
                self.tree.reattach(item, '', 'end')
            else:
                self.tree.detach(item)

    def copy_selected_password(self, event):
        selected = self.tree.focus()
        if selected:
            pwd = self.tree.item(selected)['values'][1]
            self.clipboard_clear()
            self.clipboard_append(pwd)
            messagebox.showinfo("Copied", f"Password copied to clipboard:\n{pwd}")

    def copy_all(self):
        all_pwds = "\n".join(f"{d['SSID']}: {d['Password']}" for d in self.passwords)
        self.clipboard_clear()
        self.clipboard_append(all_pwds)
        messagebox.showinfo("Copied", "All passwords copied to clipboard!")

if __name__ == "__main__":
    app = CyberWiFiViewer()
    app.mainloop()
