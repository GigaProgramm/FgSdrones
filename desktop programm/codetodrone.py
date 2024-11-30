import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time

class SimpleArduinoIDE:
    def __init__(self, master):
        self.master = master
        master.title("Простой аналог Arduino IDE без Arduino IDE")

        self.port_label = tk.Label(master, text="Выберите последовательный порт:")
        self.port_label.pack(pady=5)

        self.port_combo = ttk.Combobox(master, values=self.get_serial_ports())
        self.port_combo.pack(pady=5)
        self.port_combo.current(0)  # Выбор первого порта по умолчанию

        self.code_area = tk.Text(master, height=20, width=50)
        self.code_area.pack(padx=10, pady=10)

        self.send_button = tk.Button(master, text="Отправить на Arduino", command=self.send_code)
        self.send_button.pack(pady=5)

        self.serial_port = None

    def get_serial_ports(self):
        """Получить список доступных последовательных портов"""
        ports = [port.device for port in serial.tools.list_ports.comports()]
        return ports

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

        code = self.code_area.get("1.0", tk.END)
        self.serial_port.write(code.encode('utf-8'))  # Отправка кода на Arduino
        time.sleep(2)  # Ждем, чтобы Arduino обработал код
        print("Код отправлен на Arduino!")

if __name__ == "__main__":
    root = tk.Tk()
    app = SimpleArduinoIDE(root)
    root.mainloop()