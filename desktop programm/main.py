import customtkinter as ctk
import tkinter as tk
from tkinter import simpledialog, filedialog, messagebox
import serial
import serial.tools.list_ports
import time
ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("blue")

class textIde(ctk.CTk):
    def __init__(self, master=None):
        super().__init__()

        self.title("DroneIDE")
        self.geometry("800x600")
        self.root = ctk.CTk()
        self.toolbar = ctk.CTkFrame(self.master, width=50, height=768)
        self.toolbar.pack(side="left", fill="y")

        self.label = ctk.CTkLabel(self.toolbar, text="FGSDr", font=("Arial", 15))
        self.label.pack(pady=10)

        self.paint_button = ctk.CTkButton(self.toolbar, text="Open", command=self.save)
        self.paint_button.pack(fill="x", pady=10)

        self.ide_button = ctk.CTkButton(self.toolbar, text="Save", command=self.open)
        self.ide_button.pack(fill="x", pady=10)

        self.run_button = ctk.CTkButton(self.toolbar, text="Quit", command=self.quit)
        self.run_button.pack(fill="x", pady=10)

        # Arduino IDE components
        self.port_label = ctk.CTkLabel(self.toolbar, text="com port:")
        self.port_label.pack(pady=5)

        self.port_combo = ctk.CTkComboBox(self.toolbar, values=[])
        self.port_combo.pack(pady=5)

        # Set the first port as the default selection if there are any ports available
        ports = self.get_serial_ports()
        if ports:
            self.port_combo.set(ports[0])  # Выбор первого порта по умолчанию

        self.send_button = ctk.CTkButton(self.toolbar, text="Upload", command=self.send_code)
        self.send_button.pack(pady=5)

        self.send_line_button = ctk.CTkButton(self.toolbar, text="Send Line", command=self.send_line)
        self.send_line_button.pack(pady=5)

        self.text_area = tk.Text(self, font=("Consolas", 12))
        self.text_area.pack(fill="both", side=ctk.RIGHT, expand=True)
        self.text_area.tag_config('keyword', foreground='#f250e7')  # purple
        self.text_area.tag_config('builtin', foreground='#9950f2')  # blue-violet
        self.text_area.tag_config('string', foreground='#6a8759')  # green
        self.text_area.tag_config('comment', foreground='#8d9ba6')  # dark green
        self.text_area.tag_config('unknown', foreground='#84adf0')  # blue-violet
        self.text_area.tag_config('class', foreground='#48b083')  # green-blue
        self.text_area.tag_config('clas', foreground='#50adfa')  # green-blue
        self.text_area.tag_config('def_func', foreground='#dee86d')  # light green

        self.keywords = ['if', 'else', 'for', 'while', 'import', 'class', 'function', 'func', 'return', '++', '+', '>', '<', '=', '@obj', 'case', 'forward()', 'back()', 'start()', 'landing()']
        self.builtins = ['self', 'print', 'len', 'range', 'list', 'dict', 'set', 'int', 'float', 'str', 'bool', 'var', 'let']
        self.strings = ['"', "'", '"""', "'''"]
        self.comments = ['// ']
        self.clas = ['class', 'function', '++', '+', '>', '<', '=', '@obj', 'case']

        self.text_area.bind("<KeyRelease>", self.highlight_syntax_realtime)  
        self.line_number_area = tk.Text(self, width=5, height=400, font=("Consolas", 12))
        self.line_number_area.pack(side=ctk.LEFT, fill="y")
        self.update_line_numbers()

        self.serial_port = None
        self.current_line = 1
        self.text_area.tag_config('current_line', background='yellow')

        self.port_combo.bind("<FocusIn>", self.update_ports)

    def get_serial_ports(self):
        """Получить список доступных последовательных портов"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports

    def update_ports(self, event=None):
        """Update the list of available serial ports in the combobox."""
        start_time = time.time()
        timeout = 1  # seconds
        while time.time() - start_time < timeout:
            ports = self.get_serial_ports()
            if ports and self.port_combo.get() not in ports:
                self.port_combo.configure(values=ports)
                self.port_combo.set(ports[0])
                return
            elif ports and not self.port_combo.cget("values"):
                 self.port_combo.configure(values=ports)
                 self.port_combo.set(ports[0])
                 return
            time.sleep(0.2)  # Check every 200ms
        # If no new ports are found after the timeout, update with whatever is available
        ports = self.get_serial_ports()
        self.port_combo.configure(values=ports)
        if ports and self.port_combo.get() not in ports:
            self.port_combo.set(ports[0])

    def send_code(self):
        """Отправить код на выбранный последовательный порт"""
        if self.serial_port is None or not self.serial_port.is_open:
            try:
                selected_port = self.port_combo.get()
                self.serial_port = serial.Serial(selected_port, 9600, timeout=1)
                time.sleep(2)  # Ждем, чтобы Arduino инициализировался
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть порт: {e}")
                return

        code = self.text_area.get("1.0", tk.END)
        self.serial_port.write(code.encode('utf-8'))  # Отправка кода на Arduino
        time.sleep(2)  # Ждем, чтобы Arduino обработал код
        print("Код отправлен на Arduino!")

    def auto_brace(self, event):
        if event.char in "{}[]()<>":
            self.text_area.insert("insert", event.char)
            self.text_area.insert("insert", self.get_closing_brace(event.char))
            self.text_area.mark_set("insert", "insert -1c")

    def get_closing_brace(self, char):
        braces = {"{": "}", "[": "]", "(": ")", "<":">"}
        return braces[char]

    def update_line_numbers(self):
        self.line_number_area.delete("1.0", "end")
        for i, line in enumerate(self.text_area.get("1.0", "end").split("\n"), start=1):
            self.line_number_area.insert("end", f"{i}\n")
        self.after(100, self.update_line_numbers)

    def highlight_syntax_realtime(self, event):
        self.text_area.tag_remove('keyword', '1.0', 'end')
        self.text_area.tag_remove('builtin', '1.0', 'end')
        self.text_area.tag_remove('string', '1.0', 'end')
        self.text_area.tag_remove('comment', '1.0', 'end')
        self.text_area.tag_remove('unknown', '1.0', 'end')
        self.text_area.tag_remove('class', '1.0', 'end')
        self.text_area.tag_remove('clas', '1.0', 'end')
        self.text_area.tag_remove('def_func', '1.0', 'end')

        text = self.text_area.get('1.0', 'end-1c')
        lines = text.split('\n')

        for i, line in enumerate(lines, 1):
            words = line.split()
            for j, word in enumerate(words):
                if word in self.keywords:
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('keyword', start, end)

                elif word in self.builtins:
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('builtin', start, end)

                elif word == 'class':
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('clas', start, end)

                    if j + 1 < len(words):
                        next_word = words[j + 1]
                        start = f'{i}.{line.index(next_word)}'
                        end = f'{i}.{line.index(next_word) + len(next_word)}'
                        self.text_area.tag_add('class', start, end)

                elif word == 'def':
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('clas', start, end)

                    if j + 1 < len(words):
                        next_word = words[j + 1]
                        start = f'{i}.{line.index(next_word)}'
                        end = f'{i}.{line.index(next_word) + len(next_word)}'
                        self.text_area.tag_add('def_func', start, end)

                elif word.endswith('__') or word.endswith('.__'):  # Check for class names
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('class', start, end)

                elif word not in self.keywords and word not in self.builtins and not word.isdigit():
                    start = f'{i}.{line.index(word)}'
                    end = f'{i}.{line.index(word) + len(word)}'
                    self.text_area.tag_add('unknown', start, end)

            for string in self.strings:
                if string in line:
                    start = f'{i}.{line.index(string)}'
                    end = f'{i}.{line.index(string) + len(string)}'
                    self.text_area.tag_add('string', start, end)

            for comment in self.comments:
                if comment in line:
                    start = f'{i}.{line.index(comment)}'
                    end = f'{i}.end'
                    self.text_area.tag_add('comment', start, end)

    def run(self):
        self.mainloop()

    def open(self):
        self.text_area.delete("1.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".fde", filetypes=[('FDE', '*.fde')])
        if file_path:
            with open(file_path, 'w') as file:
                code = self.text_area.get("1.0", tk.END)
                file.write(code)

    def save(self):
        file_path = filedialog.askopenfilename(filetypes=[('FDE', '*.fde')])
        if file_path:
            with open(file_path, 'r') as file:
                code = file.read()
                self.text_area.delete('1.0', tk.END)
                self.text_area.insert(tk.END, code)

    def quit(self):
        if self.serial_port and self.serial_port.is_open:
            self.serial_port.close()
        self.destroy()
        self.quit()

    def highlight_line(self, line_number):
        """Highlights the given line number in the text area."""
        self.text_area.tag_remove('current_line', '1.0', tk.END)  # Remove previous highlights
        start = f'{line_number}.0'
        end = f'{line_number}.end'
        self.text_area.tag_add('current_line', start, end)
        self.text_area.see(start)  # Scroll to the current line

    def send_line(self):
        """Отправить код построчно на выбранный последовательный порт"""
        if self.serial_port is None or not self.serial_port.is_open:
            try:
                selected_port = self.port_combo.get()
                self.serial_port = serial.Serial(selected_port, 9600, timeout=1)
                time.sleep(2)  # Ждем, чтобы Arduino инициализировался
            except Exception as e:
                messagebox.showerror("Ошибка", f"Не удалось открыть порт: {e}")
                return

        code = self.text_area.get("1.0", tk.END)
        lines = code.split('\n')
        if self.current_line <= len(lines):
            line = lines[self.current_line - 1] + '\n'  # Add newline character
            self.serial_port.write(line.encode('utf-8'))
            time.sleep(0.1)  # Give some time to process
            print(f"Отправлена строка {self.current_line}: {line.strip()}")
            self.highlight_line(self.current_line)
            self.current_line += 1
        else:
            messagebox.showinfo("Информация", "Весь код отправлен!")
            self.text_area.tag_remove('current_line', '1.0', tk.END)  # Remove highlight
            self.current_line = 1  # Reset line number for next run

if __name__ == "__main__":
    app = textIde()
    app.run()