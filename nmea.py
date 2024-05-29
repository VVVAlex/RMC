import time
import functools
import operator
import customtkinter as ctk
from edit import Editor
from port import Port
from data_gps import GPS

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

trace = print if True else lambda *x: None  # False | True


class App(ctk.CTk):
    """Основной класс"""

    WIDTH = 642
    HEIGHT = 354

    def __init__(self):
        super().__init__(fg_color='grey55')
        self.title("GPS Simulator RMC")
        self.after(300, lambda: self.iconbitmap("gps.ico"))
        self.geometry(f"{App.WIDTH}x{App.HEIGHT}")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.resizable(False, True)
        self.minsize(self.WIDTH, 300)
        self.maxsize(self.WIDTH, 700)
        self.old_secs = 0
        self.show = False
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.top = Port(self)
        self.top.grid(row=0, column=0, padx=1, pady=(1, 0), sticky="we")
        self.top.grid_columnconfigure(2, weight=1)
        self.top.grid_rowconfigure(0, weight=1)

        self.cnt = GPS(self)
        self.cnt.grid(row=1, column=0, padx=1, sticky="nsew")
        self.cnt.grid_columnconfigure((0, 1), weight=1)

        self.frame_cb = ctk.CTkFrame(self, corner_radius=0, fg_color="grey20")
        self.frame_cb.grid(row=2, column=0, sticky="we", padx=1)
        self.check_var = ctk.StringVar(value="off")
        self.checkbox = ctk.CTkCheckBox(self.frame_cb, text="Show msg", font=("Roboto Medium", -14),
                                        command=self.checkbox_event, border_width=2, border_color="#565B5E",
                                        variable=self.check_var, onvalue="on", offvalue="off")
        self.checkbox.grid(row=0, column=0, sticky="w", padx=5, pady=2)

        self.ed = Editor(self)
        self.ed.grid(row=4, column=0, padx=1, pady=1, sticky="nsew")

        self.lab_lat = self.cnt.d_send.lab_lat
        self.lab_lon = self.cnt.d_send.lab_lon
        self.speed = self.cnt.d_set.speed
        self.kurs = self.cnt.d_set.kurs

        self.top.scan_prt([])
        self.tick()

    def tick(self) -> None:
        """Цикл посылки данных"""
        secs = time.time()
        if secs - self.old_secs >= 1:   # задержка 1.0
            self.old_secs = secs
            self.cnt.d_send.set_local_time()       # показать локальное время
            self.send_data()
        self.update()
        self.after(20, self.tick)

    def send_data(self) -> None:
        """Посылка данных в порт"""
        t_uts = time.strftime('%H%M%S')
        t_data = time.strftime('%d%m%y')
        lat_text = self.lab_lat.cget('text')
        n_s = lat_text[-1]
        lat = lat_text[:2] + lat_text[3:9]
        lon_text = self.lab_lon.cget('text')
        w_e = lon_text[-1]
        lon = lon_text[:3] + lon_text[4:10]
        try:
            speed = f"{float(self.speed.get()):05.1f}"
            kurs = f"{self.kurs.get():05.1f}"
        except TypeError:
            return
        data_str = f"GPRMC{t_uts}A{lat}{n_s}{lon}{w_e}{speed}{kurs}{t_data}031.1W"
        ks = functools.reduce(operator.xor, (ord(i) for i in data_str), 0)
        ks_hex = hex(ks)[-2:]
        msg = f'$GPRMC,{t_uts},A,{lat},{n_s},{lon},{w_e},{speed},{kurs},{t_data},031.1,W,*{ks_hex}'
        msg_bytes = msg.encode('latin-1') + b'\n'
        if self.show:
            self.ed.set_text_to_edit(msg_bytes.decode('latin-1'))
        self.top.send_(msg_bytes)

    def checkbox_event(self) -> None:
        """Обработчик флажка"""
        self.show = False
        if self.check_var.get() == 'on':
            self.show = True

    def on_closing(self):
        """Выход"""
        self.top.stop()
        self.destroy()
        self.after(300)
        raise SystemExit()


if __name__ == "__main__":
    app = App()
    app.mainloop()
