import os
import openai
import time
import subprocess
import pygame.mixer

import tkinter as tk
from tkinter import ttk, filedialog
import re
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText

openai.api_key = "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"  # supply your API key however you choose

# Error messages vector
error_messages = [
    "Permission denied",
    "No such file or directory",
    "Command not found",
    "Segmentation fault",
    "Unable to allocate memory",
    "Filesystem full",
    "Connection refused",
    "Invalid argument",
    "Read-only file system",
    "Device not found",
    "Bus error",
    "Kernel panic",
    "ERROR",
    "ERR",
    "WARNING",
    "WARN",
    "Failed",
    "Could not",
    "No",
    "not",
    "no",
    "Dependency Issues",
    "Grub Bootloader Errors",
    "Graphics Driver Issues",
    "Network Connection Problems",
    "Application Crashes",
    "Disk Space Exhaustion",
    "USB Device Recognition",
    "Audio Issues",
    "System Freezing or Unresponsiveness",
    "System Update Problems",
    "Yum/DNF Repository Errors",
    "Firewall Configuration Problems",
    "SELinux Issues",
    "Networking and DNS Errors",
    "Kernel-related Issues",
    "Disk and Filesystem Errors",
    "Service Startup Failures",
    "Hardware Compatibility Issues",
    "System Update Problems",
]

def open_frequency_distribution_window():
    subprocess.Popen(['python', 'Frequency_Distribution_Window.py'])
def analyze_syslog(syslog_content):
    if syslog_content:
        found_errors = []
        lines = syslog_content.split("\n")  # Split syslog content into lines
        for error in error_messages:
            pattern = r"\w{3}\s+\d{1,2}\s\d{2}:\d{2}:\d{2}.*?(" + re.escape(error) + ")"
            for line_num, line in enumerate(lines, start=1):
                match = re.search(pattern, line)
                if match:
                    message = line  # Use the original syslog message instead of the error message vector
                    found_errors.append(f"Line {line_num}: {message}")

        if found_errors:
            display_errors(found_errors)
        else:
            messagebox.showinfo("No Errors", "No error messages were found in the syslog.")
    else:
        messagebox.showerror("Error", "Failed to load syslog content.")


def upload_action():
    file_path = filedialog.askopenfilename(title="Select syslog file")
    if file_path:
        try:
            with open(file_path, 'r') as file:
                syslog_content = file.read()
            if syslog_content:
                analyze_syslog(syslog_content)  # Pass the syslog content to analyze_syslog function
                messagebox.showinfo("Success", "Syslog file loaded successfully.")
            else:
                messagebox.showwarning("Empty File", "The selected file is empty.")
        except Exception as e:
            messagebox.showerror("Error", str(e))


def open_response_window(errors):
    def delete_special_characters():
        # Get the content from the listbox_response
        response_text = listbox_response.get(1.0, tk.END)

        # Remove special characters using regular expression
        cleaned_text = re.sub(r'[^\w\s]', '', response_text)

        # Update the listbox_response with the cleaned text
        listbox_response.configure(state="normal")
        listbox_response.delete(1.0, tk.END)
        listbox_response.insert(tk.END, cleaned_text)
        listbox_response.configure(state="disabled")


    def show_selected_message():
        start_time = time.time()  # Record start time

        selected_index = listbox.curselection()
        if selected_index:
            selected_error = errors[selected_index[0]]
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user",
                           "content": "I have the following problem in Linux: " + selected_error + " My question is: How to fix the problem?"}]
            )
            answer = response.choices[0].message.content

            elapsed_time = time.time() - start_time  # Calculate elapsed time

            listbox_response.configure(state="normal")  # Enable editing state
            listbox_response.insert(tk.END, answer)
            listbox_response.configure(state="disabled")  # Disable editing state

            response_time_label.configure(text="Elapsed Time: {:.2f} seconds".format(elapsed_time))

    def clear_listbox():
        listbox_response.configure(state="normal")  # Enable editing state
        listbox_response.delete(1.0, tk.END)
        listbox_response.configure(state="disabled")  # Disable editing state

        response_time_label.configure(text="Elapsed Time: ")  # Clear the response_time_label

    def run_voice_script():
        selected_text = listbox_response.get(1.0, tk.END)  # Get the text from listbox_response
        selected_text = selected_text.strip()  # Remove leading/trailing whitespace

        # Create a temporary file to store the selected text
        temp_file_path = "selected_text.txt"
        with open(temp_file_path, "w") as file:
            file.write(selected_text)

        # Run the Voice.py script using the selected text
        subprocess.Popen(['python', 'Voice.py', temp_file_path])

    def stop_voice_script():
        pygame.mixer.init()
        pygame.mixer.music.stop()
        pygame.mixer.quit()

    response_window = tk.Toplevel()
    response_window.title("Chatbot Response")

    # Create the first LabelFrame for "ChatGPT"
    chatgpt_frame = ttk.LabelFrame(response_window, text="ChatGPT")
    chatgpt_frame.pack(padx=10, pady=5, expand=True, fill=tk.BOTH)

    listbox_response = ScrolledText(chatgpt_frame, width=120, height=10, wrap=tk.WORD)
    listbox_response.pack(padx=10, pady=10, expand=True, fill=tk.BOTH)

    # ... (buttons for "ChatGPT" frame)
    button_delete_special_chars = tk.Button(chatgpt_frame, text="Delete special characters",
                                            command=delete_special_characters)
    button_delete_special_chars.pack(side=tk.LEFT, padx=5, pady=5)

    button_clear = tk.Button(chatgpt_frame, text="Clear", command=clear_listbox)
    button_clear.pack(side=tk.LEFT, padx=5, pady=5)

    button_voice = tk.Button(chatgpt_frame, text="Voice", command=run_voice_script)
    button_voice.pack(side=tk.LEFT, padx=5, pady=5)

    button_stop_voice = tk.Button(chatgpt_frame, text="Stop Voice", command=stop_voice_script)
    button_stop_voice.pack(side=tk.LEFT, padx=5, pady=5)


    scrollbar_response = ttk.Scrollbar(response_window, orient=tk.VERTICAL, command=listbox_response.yview)
    scrollbar_response.pack(side=tk.RIGHT, fill=tk.Y)

    scrollbar_response_x = ttk.Scrollbar(response_window, orient=tk.HORIZONTAL, command=listbox_response.xview)
    scrollbar_response_x.pack(side=tk.BOTTOM, fill=tk.X)

    listbox_response.configure(yscrollcommand=scrollbar_response.set, xscrollcommand=scrollbar_response_x.set)
    listbox_response.configure(state="disabled")  # Set initial state as disabled

    listbox = tk.Listbox(response_window, width=50, height=10)
    listbox.pack(fill=tk.BOTH, expand=True)

    scrollbar = ttk.Scrollbar(response_window, orient=tk.VERTICAL, command=listbox.yview)
#    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    listbox.config(yscrollcommand=scrollbar.set)


    button_show_answer = tk.Button(response_window, text="Show answer of the ChatGPT", command=show_selected_message)
    button_show_answer.pack()
    response_time_label = tk.Label(response_window, text="Elapsed Time: ")
    response_time_label.pack()

    num_records_label = tk.Label(response_window, text="Number of Records: {}".format(len(errors)))
    num_records_label.pack()






    for error in errors:
        listbox.insert(tk.END, error)  # Usamos listbox_errors en lugar de listbox para agregar los errores


def display_errors(errors):
    open_response_window(errors)


def create_menu():
    root = tk.Tk()
    root.title("Syslog Analyzer")

    menubar = tk.Menu(root)
    root.config(menu=menubar)

    analyze_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Analyze", menu=analyze_menu)
    analyze_menu.add_command(label="Analyze syslog", command=upload_action)
    analyze_menu.add_command(label="Frequency Distribution", command=open_frequency_distribution_window)  # Nueva opción

    root.mainloop()
# Run the application
create_menu()
