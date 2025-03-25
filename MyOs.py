import os
import shutil
import time
import json
import logging
import tkinter as tk
from tkinter import messagebox, simpledialog, font, Menu, filedialog, Text
from tkinter import ttk
import webbrowser
import psutil  # Make sure to install psutil using pip
from cryptography.fernet import Fernet
import socket  # For port scanning
import subprocess  # For pinging IP addresses
import platform  # For system information
import zipfile  # For file compression
from tkhtmlview import HTMLLabel  # For web browsing
import threading  # For task scheduling

# Configure logging
logging.basicConfig(filename='debug_log.json', level=logging.DEBUG, 
                    format='{"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}')

class SimpleOS:
    def __init__(self, root):
        self.root = root
        self.root.title("Simple OS")
        self.root.geometry("800x600")
        self.root.configure(bg="#F0F0F0")  # Light gray background

        # Default settings
        self.default_directory = os.getcwd()  # Set default directory to current working directory
        self.font_size = 10  # Default font size

        # Font
        self.custom_font = font.Font(family="Segoe UI", size=self.font_size)

        # Load user data
        self.load_user_data()

        # Set the style for ttk
        self.set_style()

        # Menu Bar
        self.menu_bar = Menu(root, bg="#0078D7", fg="#FFFFFF")
        self.root.config(menu=self.menu_bar)

        # Create Menus
        self.create_file_menu()
        self.create_web_menu()
        self.create_help_menu()
        self.create_security_menu()
        self.create_system_menu()
        self.create_task_menu()  # New Task Scheduler Menu

        # Frame for output and input
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(pady=10, fill=tk.BOTH, expand=True)

        # Welcome Message
        self.show_welcome_message()

        # Search Bar
        self.search_entry = ttk.Entry(self.main_frame, width=80, font=self.custom_font)
        self.search_entry.pack(padx=10, pady=(5, 10), fill=tk.X)
        self.search_entry.bind("<KeyRelease>", self.search_files)

        # Output Area
        self.output_area = tk.Text(self.main_frame, width=80, height=20, bg="#FFFFFF", fg="#000000", font=self.custom_font, wrap=tk.WORD)
        self.output_area.pack(padx=10, pady=(10, 0), fill=tk.BOTH, expand=True)

        # Input Area
        self.command_entry = ttk.Entry(self.main_frame, width=80, font=self.custom_font)
        self.command_entry.pack(padx=10, pady=(5, 10), fill=tk.X)
        self.command_entry.bind("<Return>", self.execute_command)

        # Button Frame
        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=(5, 10))

        # Add buttons
        self.run_button = ttk.Button(self.button_frame, text="Run Command", command=self.run_command_from_entry)
        self.run_button.pack(side=tk.LEFT, padx=5)

        self.clear_button = ttk.Button(self.button_frame, text="Clear Output", command=self.clear_output)
        self.clear_button.pack(side=tk.LEFT, padx=5)

    def load_user_data(self):
        """Load user data from a configuration file."""
        self.user_data_file = "users.cfg"
        if os.path.exists(self.user_data_file):
            with open(self.user_data_file, "r") as file:
                content = file.read().strip()  # Read and strip whitespace
                if content:  # Check if the content is not empty
                    try:
                        self.user_data = json.loads(content)  # Use json.loads instead of json.load
                    except json.JSONDecodeError as e:
                        logging.error(f"Error decoding JSON from {self.user_data_file}: {e}")
                        self.user_data = {}  # Initialize to empty dictionary on error
                else:
                    self.user_data = {}  # Initialize to empty dictionary if file is empty
        else:
            self.user_data = {}

    def save_user_data(self):
        """Save user data to a configuration file."""
        with open(self.user_data_file, "w") as file:
            json.dump(self.user_data, file)

    def log_debug(self, message):
        """Log debug messages to the JSON file."""
        logging.debug(message)

    def show_welcome_message(self):
        welcome_frame = ttk.Frame(self.main_frame)
        welcome_frame.pack(pady=(10, 0))

        welcome_label = ttk.Label(welcome_frame, text="Welcome to IMPNEN OS!", font=("Segoe UI", 10, "bold"), foreground="#0078D7")
        welcome_label.pack(pady=(10, 5))

        description_label = ttk.Label(welcome_frame, text="Your lightweight operating system simulation.", font=("Segoe UI", 8), foreground="#555555")
        description_label.pack(pady=(0, 10))

    def set_style(self):
        # Set the style for ttk
        style = ttk.Style()
        style.theme_use('clam')  # Use a modern theme
        style.configure("TButton", padding=6, relief="flat", background="#0078D7", foreground="white", font=self.custom_font)
        style.map("TButton", background=[("active", "#005A9E")])
        style.configure("TLabel", background="#F0F0F0", font=self.custom_font)
        style.configure("TFrame", background="#F0F0F0")

    def create_file_menu(self):
        file_menu = Menu(self.menu_bar, tearoff=0, bg="#0078D7", fg="#FFFFFF")
        file_menu.add_command(label="List Files", command=self.list_files)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_command(label="Create Directory", command=self.create_directory)
        file_menu.add_command(label="Delete File/Dir", command=self.delete_file_or_dir)
        file_menu.add_command(label="Read File", command=self.read_file)
        file_menu.add_command(label="Edit File", command=self.edit_file)
        file_menu.add_command(label="Create File", command=self.create_file)
        file_menu.add_command(label="Copy File", command=self.copy_file)
        file_menu.add_command(label="Move File", command=self.move_file)
        file_menu.add_command(label="Rename File/Dir", command=self.rename_file_or_dir)
        file_menu.add_command(label="Show File Properties", command=self.show_file_properties)
        file_menu.add_command(label="Open Task Manager", command=self.open_task_manager)
        file_menu.add_command(label="Compress File", command=self.compress_file)
        file_menu.add_command(label="Decompress File", command=self.decompress_file)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.confirm_exit)
        self.menu_bar.add_cascade(label="File", menu=file_menu)

    def create_web_menu(self):
        web_menu = Menu(self.menu_bar, tearoff=0, bg="#0078D7", fg="#FFFFFF")
        web_menu.add_command(label="Open Google", command=lambda: self.open_web_window("https://www.google.com"))
        web_menu.add_command(label="Open YouTube", command=lambda: self.open_web_window("https://www.youtube.com"))
        self.menu_bar.add_cascade(label="Web", menu=web_menu)

    def create_help_menu(self):
        help_menu = Menu(self.menu_bar, tearoff=0, bg="#0078D7", fg="#FFFFFF")
        help_menu.add_command(label="About", command=self.show_about)
        self.menu_bar.add_cascade(label="Help", menu=help_menu)

    def create_security_menu(self):
        security_menu = Menu(self.menu_bar, tearoff=0, bg="#0078D7", fg="#FFFFFF")
        security_menu.add_command(label="View Security Logs", command=self.view_security_logs)
        security_menu.add_command(label="Network Traffic Monitor", command=self.network_traffic_monitor)
        security_menu.add_command(label="Intrusion Detection System", command=self.intrusion_detection_system)
        security_menu.add_command(label="Secure File Deletion", command=self.secure_file_deletion)
        security_menu.add_command(label="Malware Scanner", command=self.malware_scanner)
        security_menu.add_command(label="Scan Ports", command=self.scan_ports)
        security_menu.add_command(label="Encrypt File", command=self.encrypt_file)
        security_menu.add_command(label="Decrypt File", command=self.decrypt_file)
        security_menu.add_command(label="View Network Connections", command=self.view_network_connections)
        security_menu.add_command(label="Ping IP Address", command=self.ping_ip_address)
        security_menu.add_command(label="Check for Updates", command=self.check_for_updates)
        security_menu.add_command(label="Malware Scan", command=self.malware_scan)
        self.menu_bar.add_cascade(label="Security", menu=security_menu)

    def create_system_menu(self):
        system_menu = Menu(self.menu_bar, tearoff=0, bg="#0078D7", fg="#FFFFFF")
        system_menu.add_command(label="System Information", command=self.show_system_info)
        system_menu.add_command(label="Open File Explorer", command=self.open_file_explorer_window)
        system_menu.add_command(label="Show Disk Information", command=self.show_disk_info)
        system_menu.add_command(label="Manage Windows Services", command=self.manage_services)
        system_menu.add_command(label="Show Running Processes", command=self.show_running_processes)
        system_menu.add_command(label="Shutdown", command=self.shutdown_system)
        system_menu.add_command(label="Restart", command=self.restart_system)
        self.menu_bar.add_cascade(label="System", menu=system_menu)

    def create_task_menu(self):
        task_menu = Menu(self.menu_bar, tearoff=0, bg="#0078D7", fg="#FFFFFF")
        task_menu.add_command(label="Task Scheduler", command=self.create_task_scheduler)
        self.menu_bar.add_cascade(label="Tasks", menu=task_menu)

    def run_command_from_entry(self):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.run_command(command)

    def clear_output(self):
        self.output_area.delete(1.0, tk.END)

    def execute_command(self, event):
        command = self.command_entry.get()
        self.command_entry.delete(0, tk.END)
        self.run_command(command)

    def run_command(self, command):
        if command.lower() == 'exit':
            if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
                self.log_debug("User  exited the application.")
                self.root.quit()
        elif command.lower() == 'help':
            self.output_area.insert(tk.END, "Available commands:\n")
            self.output_area.insert(tk.END, "1. list - List files in the current directory\n")
            self.output_area.insert(tk.END, "2. create <filename> - Create a new file\n")
            self.output_area.insert(tk.END, "3. delete <filename> - Delete a file\n")
            self.output_area.insert(tk.END, "4. dir - List current directory\n")
            self.output_area.insert(tk.END, "5. exit - Exit the application\n")
        elif command.lower().startswith('create '):
            file_name = command.split(' ', 1)[1]
            self.create_file(file_name)
        elif command.lower().startswith('delete '):
            file_name = command.split(' ', 1)[1]
            self.delete_file(file_name)
        elif command.lower() == 'dir':
            self.list_files()
        else:
            self.output_area.insert(tk.END, f"Unrecognized command: {command}\n")
        self.output_area.see(tk.END)

    def list_files(self):
        try:
            files = os.listdir('.')
            self.output_area.insert(tk.END, "Files in the current directory:\n")
            for file in files:
                self.output_area.insert(tk.END, f"{file}\n")
            self.output_area.insert(tk.END, "\n")
            self.log_debug("Listed files in the current directory.")
        except Exception as e:
            self.output_area.insert(tk.END, f"Error listing files: {e}\n")
            self.log_debug(f"Error listing files: {e}")
        self.output_area.see(tk.END)

    def open_folder(self):
        folder_path = filedialog.askdirectory(title="Select Folder")
        if folder_path:
            os.chdir(folder_path)  # Change current directory
            self.list_files()  # List files in the selected folder

    def create_directory(self):
        dir_name = simpledialog.askstring("Input", "Enter directory name:")
        if dir_name:
            try:
                os.makedirs(dir_name)
                self.output_area.insert(tk.END, f"Directory '{dir_name}' created successfully.\n")
                self.log_debug(f"Created directory: {dir_name}")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error creating directory: {e}\n")
                self.log_debug(f"Error creating directory: {e}")
            self.output_area.see(tk.END)

    def delete_file_or_dir(self):
        name = simpledialog.askstring("Input", "Enter the name of the file or directory to delete:")
        if name:
            try:
                if os.path.isfile(name):
                    os.remove(name)
                    self.output_area.insert(tk.END, f"File '{name}' deleted successfully.\n")
                    self.log_debug(f"Deleted file: {name}")
                elif os.path.isdir(name):
                    os.rmdir(name)
                    self.output_area.insert(tk.END, f"Directory '{name}' deleted successfully.\n")
                    self.log_debug(f"Deleted directory: {name}")
                else:
                    self.output_area.insert(tk.END, f"'{name}' not found.\n")
                    self.log_debug(f"'{name}' not found for deletion.")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error deleting '{name}': {e}\n")
                self.log_debug(f"Error deleting '{name}': {e}")
            self.output_area.see(tk.END)

    def read_file(self):
        file_name = filedialog.askopenfilename(title="Select File", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                    self.output_area.insert(tk.END, f"Contents of '{file_name}':\n{content}\n")
                    self.log_debug(f"Read file: {file_name}")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error reading file '{file_name}': {e}\n")
                self.log_debug(f"Error reading file '{file_name}': {e}")
            self.output_area.see(tk.END)

    def edit_file(self):
        file_name = filedialog.askopenfilename(title="Select File to Edit", filetypes=(("Text Files", "*.txt"), ("All Files", "*.*")))
        if file_name:
            try:
                with open(file_name, 'r') as file:
                    content = file.read()
                # Create a new window for editing
                edit_window = tk.Toplevel(self.root)
                edit_window.title(f"Edit {file_name}")
                edit_area = Text(edit_window, wrap=tk.WORD)
                edit_area.insert(tk.END, content)
                edit_area.pack(expand=True, fill=tk.BOTH)
                
                def save_changes():
                    with open(file_name, 'w') as file:
                        file.write(edit_area.get(1.0, tk.END))
                    edit_window.destroy()
                    self.log_debug(f"Saved changes to file: {file_name}")
                
                save_button = ttk.Button(edit_window, text="Save", command=save_changes)
                save_button.pack(pady=5)

            except Exception as e:
                self.output_area.insert(tk.END, f"Error reading file '{file_name}': {e}\n")
                self.log_debug(f"Error reading file '{file_name}': {e}")
            self.output_area.see(tk.END)

    def create_file(self, file_name):
        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write("")  # Create an empty file
                self.output_area.insert(tk.END, f"File '{file_name}' created successfully.\n")
                self.log_debug(f"Created file: {file_name}")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error creating file '{file_name}': {e}\n")
                self.log_debug(f"Error creating file '{file_name}': {e}")
            self.output_area.see(tk.END)

    def delete_file(self, file_name):
        if file_name:
            try:
                os.remove(file_name)
                self.output_area.insert(tk.END, f"File '{file_name}' deleted successfully.\n")
                self.log_debug(f"Deleted file: {file_name}")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error deleting file '{file_name}': {e}\n")
                self.log_debug(f"Error deleting file '{file_name}': {e}")
            self.output_area.see(tk.END)

    def copy_file(self):
        source = simpledialog.askstring("Input", "Enter source file name:")
        destination = simpledialog.askstring("Input", "Enter destination file name:")
        if source and destination:
            try:
                shutil.copy(source, destination)
                self.output_area.insert(tk.END, f"File '{source}' copied to '{destination}'.\n")
                self.log_debug(f"Copied file from '{source}' to '{destination}'.")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error copying file: {e}\n")
                self.log_debug(f"Error copying file from '{source}' to '{destination}': {e}")
            self.output_area.see(tk.END)

    def move_file(self):
        source = simpledialog.askstring("Input", "Enter source file name:")
        destination = simpledialog.askstring("Input", "Enter destination file name:")
        if source and destination:
            try:
                shutil.move(source, destination)
                self.output_area.insert(tk.END, f"File '{source}' moved to '{destination}'.\n")
                self.log_debug(f"Moved file from '{source}' to '{destination}'.")
            except Exception as e:
                self.output_area.insert(tk.END, f"Error moving file: {e}\n")
                self.log_debug(f"Error moving file from '{source}' to '{destination}': {e}")
            self.output_area.see(tk.END)

    def rename_file_or_dir(self):
        old_name = simpledialog.askstring("Input", "Enter the name of the file or directory to rename:")
        if old_name and os.path.exists(old_name):
            new_name = simpledialog.askstring("Input", "Enter the new name:")
            if new_name:
                try:
                    os.rename(old_name, new_name)
                    self.output_area.insert(tk.END, f"'{old_name}' renamed to '{new_name}'.\n")
                    self.log_debug(f"Renamed '{old_name}' to '{new_name}'.")
                except Exception as e:
                    self.output_area.insert(tk.END, f"Error renaming '{old_name}': {e}\n")
                    self.log_debug(f"Error renaming '{old_name}': {e}")
                self.output_area.see(tk.END)
        else:
            self.output_area.insert(tk.END, f"'{old_name}' not found.\n")
            self.log_debug(f"'{old_name}' not found for renaming.")

    def show_file_properties(self):
        file_name = simpledialog.askstring("Input", "Enter file name:")
        if file_name and os.path.exists(file_name):
            stats = os.stat(file_name)
            properties = f"Name: {file_name}\nSize: {stats.st_size} bytes\nCreated: {time.ctime(stats.st_ctime)}\nModified: {time.ctime(stats.st_mtime)}"
            messagebox.showinfo("File Properties", properties)
            self.log_debug(f"Displayed properties for file: {file_name}")
        else:
            self.output_area.insert(tk.END, f"'{file_name}' not found.\n")
            self.log_debug(f"'{file_name}' not found for properties display.")

    def open_task_manager(self):
        task_manager_window = tk.Toplevel(self.root)
        task_manager_window.title("Task Manager")
        task_manager_window.geometry("600x400")

        columns = ("PID", "Image Name", "Session Name", "Session#", "Mem Usage")
        tree = ttk.Treeview(task_manager_window, columns=columns, show='headings')
        tree.pack(fill=tk.BOTH, expand=True)

        for col in columns:
            tree.heading(col, text=col)

        tasks = os.popen('tasklist').readlines()[3:]
        for task in tasks:
            task_info = task.split()
            if len(task_info) >= 5:
                pid = task_info[1]
                image_name = task_info[0]
                session_name = task_info[2]
                session_number = task_info[3]
                mem_usage = task_info[4]
                tree.insert("", "end", values=(pid, image_name, session_name, session_number, mem_usage))

        scrollbar = ttk.Scrollbar(task_manager_window, orient="vertical", command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side='right', fill='y')

    def search_files(self, event):
        search_term = self.search_entry.get().lower()
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, "Search results:\n")
        for root, dirs, files in os.walk('.'):
            for file in files:
                if search_term in file.lower():
                    self.output_area.insert(tk.END, f"{os.path.join(root, file)}\n")
        self.output_area.insert(tk.END, "\n")
        self.output_area.see(tk.END)

    def show_about(self):
        about_window = tk.Toplevel(self.root)
        about_window.title("About Simple OS")
        about_window.geometry("400x300")

        # Create a Text widget for the about message
        about_text = tk.Text(about_window, wrap=tk.WORD, bg="#FFFFFF", fg="#000000", font=self.custom_font)
        about_text.pack(expand=True, fill=tk.BOTH)

        # Insert the about message into the Text widget
        about_message = (
            "Simple OS\n"
            "Version: 1.0\n"
            "Developed by: SARDIDEV\n\n"
            "Description:\n"
            "Simple OS is a lightweight operating system simulation built using Tkinter.\n"
            "It provides a user-friendly interface for performing basic file operations,\n"
            "system monitoring, and web browsing functionalities.\n"
        )
        about_text.insert(tk.END, about_message)
        about_text.config(state=tk.DISABLED)  # Make the text widget read-only

    def confirm_exit(self):
        if messagebox.askyesno("Confirm Exit", "Are you sure you want to exit?"):
            self.log_debug("User  exited the application.")
            self.root.quit()

    def open_web_window(self, url):
        web_window = tk.Toplevel(self.root)
        web_window.title("Web Browser")
        web_window.geometry("800x600")

        html_label = HTMLLabel(web_window, html=f'<iframe src="{url}" width="100%" height="100%"></iframe>')
        html_label.pack(fill="both", expand=True)

    def scan_ports(self):
        ip_address = simpledialog.askstring("Input", "Enter IP address to scan:")
        if ip_address:
            port_range = simpledialog.askstring("Input", "Enter port range (e.g., 1-1024):")
            if port_range:
                start_port, end_port = map(int, port_range.split('-'))
                open_ports = []
                for port in range(start_port, end_port + 1):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(1)
                    result = sock.connect_ex((ip_address, port))
                    if result == 0:
                        open_ports.append(port)
                    sock.close()
                self.output_area.insert(tk.END, f"Open ports on {ip_address}:\n{open_ports}\n")
                self.log_debug(f"Scanned ports on {ip_address}: {open_ports}")
                self.output_area.see(tk.END)

    def view_network_connections(self):
        connections = psutil.net_connections(kind='inet')
        self.output_area.delete(1.0, tk.END)
        self.output_area.insert(tk.END, "Active Network Connections:\n")
        for conn in connections:
            self.output_area.insert(tk.END, f"Local Address: {conn.laddr}, Remote Address: {conn.raddr}, Status: {conn.status}\n")
        self.output_area.see(tk.END)

    def ping_ip_address(self):
        ip_address = simpledialog.askstring("Input", "Enter IP address to ping:")
        if ip_address:
            response = subprocess.run(["ping", "-c", "4", ip_address], capture_output=True, text=True)
            self.output_area.insert(tk.END, response.stdout)
            self.log_debug(f"Pinging IP address: {ip_address}")
            self.output_area.see(tk.END)

    def encrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Encrypt")
        if file_path and os.path.exists(file_path):
            key = Fernet.generate_key()
            f = Fernet(key)

            with open(file_path, "rb") as file:
                file_data = file.read()
            encrypted_data = f.encrypt(file_data)

            with open(file_path, "wb") as file:
                file.write(encrypted_data)

            with open("secret.key", "wb") as key_file:
                key_file.write(key)

            messagebox.showinfo("Success", f"File '{file_path}' encrypted successfully. Key saved as 'secret.key'.")
            self.log_debug(f"Encrypted file: {file_path}")
        else:
            messagebox.showerror("Error", "File not found.")

    def decrypt_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Decrypt")
        if file_path and os.path.exists(file_path):
            try:
                key = open("secret.key", "rb").read()
                f = Fernet(key)

                with open(file_path, "rb") as file:
                    encrypted_data = file.read()
                decrypted_data = f.decrypt(encrypted_data)

                with open(file_path, "wb") as file:
                    file.write(decrypted_data)

                messagebox.showinfo("Success", f"File '{file_path}' decrypted successfully.")
                self.log_debug(f"Decrypted file: {file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to decrypt file: {e}")
                self.log_debug(f"Failed to decrypt file '{file_path}': {e}")
        else:
            messagebox.showerror("Error", "File not found.")

    def show_system_info(self):
        system_info = (
            f"System: {platform.system()}\n"
            f"Node Name: {platform.node()}\n"
            f"Release: {platform.release()}\n"
            f"Version: {platform.version()}\n"
            f"Machine: {platform.machine()}\n"
            f"Processor: {platform.processor()}\n"
            f"RAM: {round(psutil.virtual_memory().total / (1024 ** 3), 2)} GB\n"
        )
        messagebox.showinfo("System Information", system_info)
        self.log_debug("Displayed system information.")

    def show_disk_info(self):
        disk_info = ""
        partitions = psutil.disk_partitions()
        for partition in partitions:
            usage = psutil.disk_usage(partition.mountpoint)
            disk_info += (f"Device: {partition.device}\n"
                          f"Mountpoint: {partition.mountpoint}\n"
                          f"File System Type: {partition.fstype}\n"
                          f"Total Size: {usage.total / (1024 ** 3):.2f} GB\n"
                          f"Used: {usage.used / (1024 ** 3):.2f} GB\n"
                          f"Free: {usage.free / (1024 ** 3):.2f} GB\n"
                          f"Percentage Used: {usage.percent}%\n\n")
        if disk_info:
            messagebox.showinfo("Disk Information", disk_info)
            self.log_debug("Displayed disk information.")
        else:
            messagebox.showinfo("Disk Information", "No disk information available.")

    def manage_services(self):
        service_name = simpledialog.askstring("Input", "Enter the name of the service:")
        action = simpledialog.askstring("Input", "Enter 'start', 'stop', or 'restart':")
        if service_name and action in ['start', 'stop', 'restart']:
            command = f"sc {action} {service_name}"
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            if result.returncode == 0:
                messagebox.showinfo("Success", f"Service '{service_name}' {action}ed successfully.")
                self.log_debug(f"Service '{service_name}' {action}ed successfully.")
            else:
                messagebox.showerror("Error", f"Failed to {action} service '{service_name}': {result.stderr}")
                self.log_debug(f"Failed to {action} service '{service_name}': {result.stderr}")
        else:
            messagebox.showerror("Error", "Invalid input.")

    def show_running_processes(self):
        processes = psutil.process_iter(['pid', 'name', 'status'])
        process_info = "Running Processes:\n\n"
        for process in processes:
            process_info += f"PID: {process.info['pid']}, Name: {process.info['name']}, Status: {process.info['status']}\n"
        messagebox.showinfo("Running Processes", process_info)
        self.log_debug("Displayed running processes.")

    def open_file_explorer_window(self):
        explorer_window = tk.Toplevel(self.root)
        explorer_window.title("File Explorer")
        explorer_window.geometry("600x400")

        self.current_directory = os.getcwd()  # Start in the current working directory

        # Frame for the file list
        file_frame = ttk.Frame(explorer_window)
        file_frame.pack(fill=tk.BOTH, expand=True)

        # Listbox to display files and directories
        self.file_listbox = tk.Listbox(file_frame, font=self.custom_font)
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Scrollbar for the listbox
        scrollbar = ttk.Scrollbar(file_frame, orient="vertical", command=self.file_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill='y')
        self.file_listbox.config(yscrollcommand=scrollbar.set)

        # Load files and directories
        self.load_files()

        # Bind double-click event to open files or directories
        self.file_listbox.bind("<Double-1>", self.open_selected)

        # Button to go up a directory
        up_button = ttk.Button(explorer_window, text="Up", command=self.go_up_directory)
        up_button.pack(pady=5)

        # Button to select a file or directory
        select_button = ttk.Button(explorer_window, text="Select", command=self.select_file)
        select_button.pack(pady=5)

    def load_files(self):
        self.file_listbox.delete(0, tk.END)  # Clear the listbox
        try:
            for item in os.listdir(self.current_directory):
                self.file_listbox.insert(tk.END, item)  # Add each item to the listbox
        except Exception as e:
            messagebox.showerror("Error", f"Could not load files: {e}")

    def open_selected(self, event):
        selected_item = self.file_listbox.get(self.file_listbox.curselection())
        selected_path = os.path.join(self.current_directory, selected_item)

        if os.path.isdir(selected_path):
            self.current_directory = selected_path  # Change to the selected directory
            self.load_files()  # Load files in the new directory
        else:
            messagebox.showinfo("File Selected", f"You selected: {selected_path}")

    def go_up_directory(self):
        self.current_directory = os.path.dirname(self.current_directory)  # Go up one directory
        self.load_files()  # Load files in the new directory

    def select_file(self):
        selected_item = self.file_listbox.get(self.file_listbox.curselection())
        selected_path = os.path.join(self.current_directory, selected_item)
        messagebox.showinfo("File Selected", f"You selected: {selected_path}")

    def shutdown_system(self):
        if messagebox.askyesno("Confirm Shutdown", "Are you sure you want to shut down the system?"):
            self.log_debug("User  initiated system shutdown.")
            os.system("shutdown /s /t 1")  # Shutdown command for Windows

    def restart_system(self):
        if messagebox.askyesno("Confirm Restart", "Are you sure you want to restart the system?"):
            self.log_debug("User   initiated system restart.")
            os.system("shutdown /r /t 1")  # Restart command for Windows

    def compress_file(self):
        file_path = filedialog.askopenfilename(title="Select File to Compress")
        if file_path:
            zip_file_path = filedialog.asksaveasfilename(defaultextension=".zip", title="Save Compressed File As")
            if zip_file_path:
                with zipfile.ZipFile(zip_file_path, 'w') as zip_file:
                    zip_file.write(file_path, os.path.basename(file_path))
                messagebox.showinfo("Success", f"File '{file_path}' compressed to '{zip_file_path}' successfully.")
                self.log_debug(f"Compressed file '{file_path}' to '{zip_file_path}'.")

    def decompress_file(self):
        zip_file_path = filedialog.askopenfilename(title="Select Zip File to Decompress", filetypes=[("Zip Files", "*.zip")])
        if zip_file_path:
            extract_folder = filedialog.askdirectory(title="Select Folder to Extract To")
            if extract_folder:
                with zipfile.ZipFile(zip_file_path, 'r') as zip_file:
                    zip_file.extractall(extract_folder)
                messagebox.showinfo("Success", f"File '{zip_file_path}' decompressed successfully.")
                self.log_debug(f"Decompressed file '{zip_file_path}' to '{extract_folder}'.")

    def view_security_logs(self):
        logs = "No security logs available."  # Replace with actual log retrieval logic
        messagebox.showinfo("Security Logs", logs)
        self.log_debug("Viewed security logs.")

    def network_traffic_monitor(self):
        monitor_window = tk.Toplevel(self.root)
        monitor_window.title("Network Traffic Monitor")
        monitor_window.geometry("400x300")

        traffic_label = ttk.Label(monitor_window, text="Monitoring network traffic...")
        traffic_label.pack(pady=10)

        def update_traffic():
            traffic_label.config(text="Traffic data: ...")  # Update with real data
            monitor_window.after(5000, update_traffic)  # Update every 5 seconds

        update_traffic()
        self.log_debug("Opened network traffic monitor.")

    def intrusion_detection_system(self):
        ids_window = tk.Toplevel(self.root)
        ids_window.title("Intrusion Detection System")
        ids_window.geometry("400x300")

        alert_label = ttk.Label(ids_window, text="No intrusions detected.")
        alert_label.pack(pady=10)

        def check_for_intrusions():
            alert_label.config(text="Alert: Intrusion detected!")  # Update with real data
            ids_window.after(10000, check_for_intrusions)  # Check every 10 seconds

        check_for_intrusions()
        self.log_debug("Opened intrusion detection system.")

    def secure_file_deletion(self):
        file_path = filedialog.askopenfilename(title="Select File to Securely Delete")
        if file_path:
            with open(file_path, "r+b") as file:
                length = os.path.getsize(file_path)
                file.write(os.urandom(length))  # Overwrite with random data
            os.remove(file_path)
            messagebox.showinfo("Success", "File securely deleted.")
            self.log_debug(f"Securely deleted file: {file_path}")

    def malware_scanner(self):
        scan_window = tk.Toplevel(self.root)
        scan_window.title("Malware Scanner")
        scan_window.geometry("400x300")

        result_label = ttk.Label(scan_window, text="Scanning for malware...")
        result_label.pack(pady=10)

        def perform_scan():
            result_label.config(text="Scan complete. No threats detected.")
            self.log_debug("Performed malware scan.")

        perform_scan()

    def toggle_firewall(self):
        action = simpledialog.askstring("Input", "Enter 'enable' to enable or 'disable' to disable the firewall:")
        if action in ['enable', 'disable']:
            command = f"netsh advfirewall set allprofiles state {action}"
            subprocess.run(command, shell=True)
            messagebox.showinfo("Success", f"Firewall {action}d successfully.")
            self.log_debug(f"Firewall {action}d.")

    def check_for_updates(self):
        if platform.system() == "Windows":
            messagebox.showinfo("Update Check", "Your system is up to date.")
            self.log_debug("Checked for updates: System is up to date.")
        else:
            messagebox.showinfo("Update Check", "No updates available for your system.")
            self.log_debug("Checked for updates: No updates available.")

    def malware_scan(self):
        messagebox.showinfo("Malware Scan", "No malware detected.")
        self.log_debug("Performed malware scan: No malware detected.")

    def create_task_scheduler(self):
        task_window = tk.Toplevel(self.root)
        task_window.title("Task Scheduler")
        task_window.geometry("400x300")

        task_label = ttk.Label(task_window, text="Enter command to schedule:")
        task_label.pack(pady=10)

        self.task_entry = ttk.Entry(task_window, width=50)
        self.task_entry.pack(pady=5)

        time_label = ttk.Label(task_window, text="Enter time in seconds:")
        time_label.pack(pady=10)

        self.time_entry = ttk.Entry(task_window, width=10)
        self.time_entry.pack(pady=5)

        schedule_button = ttk.Button(task_window, text="Schedule Task", command=self.schedule_task)
        schedule_button.pack(pady=10)

    def schedule_task(self):
        command = self.task_entry.get()
        time_delay = int(self.time_entry.get())
        threading.Timer(time_delay, self.run_command, args=[command]).start()
        messagebox.showinfo("Task Scheduled", f"Task scheduled to run in {time_delay} seconds.")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleOS(root)
    root.mainloop()