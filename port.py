import customtkinter as ctk
import tkinter as tk
import serial
import sys
import glob
from edit import family, font_size

port_exc = serial.SerialException


class Port(ctk.CTkFrame):
    """Верхний фрейм"""

    def __init__(self, master=None, timeout=0.15):
        self.master = master
        super().__init__(master, corner_radius=0, border_width=0, border_color="grey75")
        font = ctk.CTkFont(family=f"{family}", size=font_size+2)
        self.br = 4800
        self.tty = serial.Serial(timeout=timeout, baudrate=self.br)
        self.tty.write_timeout = 0  # !!
        self.started = False
        self.info = tk.StringVar()

        self.combobox = ctk.CTkComboBox(
            self, values=["Выбор порта"], command=self._combobox_callback,
            dropdown_font=font, font=font,
            button_color="#1f538d", button_hover_color="#14375e"
        )
        self.combobox.grid(row=0, column=0, padx=2, sticky="w")

        self.combobox_br = ctk.CTkComboBox(
            self, font=font, values=['4800', '9600', '19200', '38400', '57600', '115200'],
            dropdown_font=font, command=self._combobox_callback_br,
            button_color="#1f538d", button_hover_color="#14375e"
        )
        self.combobox_br.grid(row=0, column=1, padx=2, sticky="w")

        self.lab_info = ctk.CTkLabel(
            self, textvariable=self.info, width=315, anchor="w", font=font,
        )
        self.lab_info.grid(row=0, column=2, padx=(10, 2), pady=2, sticky="we")

    def _combobox_callback_br(self, arg=None) -> None:
        """Выбор скорости передачи порта"""
        self.br = self.combobox_br.get()
        self.tty.baudrate = int(self.br)
        msg = f"Порт {self.tty.port} открыт,  скорость {self.tty.baudrate}"
        if self.tty.is_open:
            self.set_port_info(msg)

    def _combobox_callback(self, arg=None) -> None:
        """Выбор порта"""
        self.change_port(self.combobox.get())

    def open_port(self, port_: str) -> None:
        """Открывает выбранный порт"""
        self.tty.port = port_
        self.tty.open()
        self.tty.reset_input_buffer()

    # def clear_port(self) -> None:
    #     """Очистка порта"""
    #     self.tty.reset_input_buffer()

    def is_open(self) -> bool:
        """Tue если порт открыт и False если нет"""
        return self.tty.is_open

    def set_port_info(self, msg) -> None:
        """Информация о порте"""
        self.info.set(f"{msg}")

    def scan(self) -> list[str] | list:
        """Сканируем порты и возвращаем доступные в виде ['COM1', ...]"""
        if sys.platform.startswith("win"):
            ports = (f"COM{i + 1}" for i in range(20))
        elif sys.platform.startswith("linux") or sys.platform.startswith("cygwin"):
            # это исключает ваш текущий терминал "/dev/tty"
            ports = glob.glob("/dev/tty[A-Za-z]*")
        elif sys.platform.startswith("darwin"):
            ports = glob.glob("/dev/tty.*")
        else:
            raise EnvironmentError("Неподдерживаемая платформа")
        available = []
        port_list = self.scan_port()
        for prt in ports:
            if port_list:
                if prt in port_list:
                    available.append(prt)
                    continue
            try:
                s = serial.Serial(prt)
                s.close()
                available.append(prt)
            except (OSError, serial.SerialException):
                pass
        return available

    @staticmethod
    def scan_port() -> list[str]:
        """Сканируем порты и возвращаем доступные в виде ['COM1', ...]
        Не видит виртуальных портов!
        """
        from serial.tools import list_ports
        available = []
        for _port in list_ports.comports():
            available.append(_port[0])
        if available:
            return available

    def start(self) -> None:
        """start"""
        if self.tty.is_open:
            self.started = True

    def stop(self) -> None:
        """stop"""
        if self.started:
            self.started = False
            self.tty.close()

    def send_(self, data: bytes) -> None:
        """Посылка данных"""
        if self.started:
            # arr = bytearray(data)
            self.tty.write(data)

    def change_port(self, port_) -> None:
        """Смена номера порта"""
        msg = f"Не открыть порт {port_}"
        if not self.is_open():
            try:
                self.open_port(port_)
                self.start()
                msg = f"Порт {port_} открыт,  скорость {self.tty.baudrate}"
            except port_exc:
                pass
        else:
            self.stop()
            self.tty = serial.Serial(timeout=0.15, baudrate=self.br)  # объект Serial
            try:
                self.open_port(port_)
                self.start()
                msg = f"Порт {port_} открыт, таймаут {self.tty.timeout}, скорость {self.tty.baudrate}"
            except port_exc:
                pass
        self.set_port_info(msg)

    def scan_prt(self, tty: list[str | None]) -> None:
        """Сканируем порты и открываем сохраненный"""
        val = tty if tty else self.scan()
        self.combobox.configure(values=val)
