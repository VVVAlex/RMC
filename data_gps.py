import collections

import customtkinter as ctk
from intspinbox import IntSpinbox as Spinbox
import time
from collections import namedtuple
from edit import family, font_size


class Left(ctk.CTkFrame):
    """Левый фрейм"""

    def __init__(self, master=None):
        # self.master = master
        super().__init__(master, corner_radius=0)
        font = ctk.CTkFont(family=f"{family}", size=font_size)
        ctk.CTkLabel(
            self, text="W84", width=100, anchor="w", font=font,
        ).grid(row=0, column=0, padx=(10, 2), pady=2, sticky="w")
        self.lab_time = ctk.CTkLabel(
            self, text="", width=100, anchor="e", font=font,
        )
        self.lab_time.grid(row=0, column=1, padx=(10, 2), pady=(2, 2), sticky="e")

        ctk.CTkLabel(
            self, text="LAT", width=100, anchor="w", font=font,
        ).grid(row=1, column=0, padx=(10, 2), pady=2, sticky="w")
        self.lab_lat = ctk.CTkLabel(
            self, text=f"58{0xB0:c}10.750{0xB4:c}N", width=100, anchor="e", font=font,
        )
        self.lab_lat.grid(row=1, column=1, padx=(10, 2), pady=2, sticky="e")
        ctk.CTkLabel(
            self, text="LON", width=100, anchor="w", font=font,
        ).grid(row=2, column=0, padx=(10, 2), pady=(2, 2), sticky="w")
        self.lab_lon = ctk.CTkLabel(
            self, text=f"030{0xB0:c}13.867{0xB4:c}W", width=100, anchor="e", font=font,
        )
        self.lab_lon.grid(row=2, column=1, padx=(10, 2), pady=2, sticky="e")

    def set_local_time(self) -> None:
        """Установка машинного времени"""
        t = time.strftime('%d.%m.%y %H:%M:%S')
        self.lab_time.configure(text=t)

    def set_lat_lon(self, data: collections.namedtuple) -> None:
        """Обновить данные широты и долготы"""
        # print(data)
        dt_lat = int(data.lat_min) + int(data.lat_sec)/60
        d_lat = f"{dt_lat:.3f}"
        dt_lon = int(data.lon_min) + int(data.lon_sec) / 60
        d_lon = f"{dt_lon:.3f}"
        # self.lab_lat.configure(text=f"{data.lat_gr.zfill(2)}{0xB0:c}{dt_lat:.3f}{0xB4:c}{data.lat_we}")
        self.lab_lat.configure(text=f"{data.lat_gr.zfill(2)}{0xB0:c}{d_lat.zfill(6)}{0xB4:c}{data.lat_we}")
        # self.lab_lon.configure(text=f"{data.lon_gr.zfill(3)}{0xB0:c}{dt_lon:.3f}{0xB4:c}{data.lon_ns}")
        self.lab_lon.configure(text=f"{data.lon_gr.zfill(3)}{0xB0:c}{d_lon.zfill(6)}{0xB4:c}{data.lon_ns}")


class Right(ctk.CTkFrame):
    """Правый фрейм"""

    def __init__(self, master):
        super().__init__(master, corner_radius=0, border_width=0, border_color="grey65")
        self.master = master
        font = ctk.CTkFont(family=f"{family}", size=font_size)
        font2 = ctk.CTkFont(family=f"{family}", size=-14)
        self.data_gps = namedtuple('data_gps', ['lat_gr', 'lat_min', 'lat_sec', 'lat_we',
                                                'lon_gr', 'lon_min', 'lon_sec', 'lon_ns', 'speed', 'kurs'])
        validate_cmd_kurs = (self.register(self.is_okay_kurs), '%P')
        validate_cmd_speed = (self.register(self.is_okay_speed), '%P')
        ctk.CTkLabel(
            self, text=f"Курс {0xB0:c}", width=120, anchor="center", font=font2,
        ).grid(row=0, column=0, padx=(10, 2), pady=2, sticky="w")
        ctk.CTkLabel(
            self, text=f"Скорость kn", width=120, anchor="center", font=font2,
        ).grid(row=0, column=1, padx=(10, 2), pady=2, sticky="e")
        self.kurs = Spinbox(self, width=120, step_size=1,
                            from_=0, to=360,
                            validatecommand=validate_cmd_kurs
                            )
        self.kurs.grid(row=1, column=0, sticky='w', padx=8, pady=4)
        self.speed = Spinbox(self, width=120, step_size=1,
                             from_=0, to=100,
                             validatecommand=validate_cmd_speed
                             )
        self.speed.grid(row=1, column=1, sticky='e', padx=8, pady=4)
        self.kurs.set(20)
        self.speed.set(10)
        width = 70
        self.grid_columnconfigure((0, 1), weight=1)
        # self.grid_rowconfigure(2, weight=10)
        self.frame_in = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.frame_in.grid(row=2, column=0, columnspan=2, sticky="nsew")
        self.frame_in.grid_columnconfigure((0, 1, 2, 3, 4), weight=1)
        ctk.CTkLabel(self.frame_in, text="").grid(row=0, column=0)
        ctk.CTkLabel(self.frame_in, text="Град.", font=font2).grid(row=0, column=1)
        ctk.CTkLabel(self.frame_in, text="Мин.", font=font2).grid(row=0, column=2, pady=2)
        ctk.CTkLabel(self.frame_in, text="Сек.", font=font2).grid(row=0, column=3)
        ctk.CTkLabel(self.frame_in, text="NSEW", font=font2).grid(row=0, column=4)
        ctk.CTkLabel(self.frame_in, text="Широта", width=width-30, font=font2).grid(row=1, column=0)
        ctk.CTkLabel(self.frame_in, text="Долгота", width=width-30, font=font2).grid(row=2, column=0, pady=2)

        validate_lat_gr = (self.register(self.is_okay_lat_gr), '%P')
        self.e_lat_gr = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lat_gr,
                                     validate='key', justify='center', font=font)
        self.e_lat_gr.grid(row=1, column=1)
        validate_lat_min = (self.register(self.is_okay_lat_min), '%P')
        self.e_lat_min = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lat_min,
                                      validate='key', justify='center',  font=font)
        self.e_lat_min.grid(row=1, column=2)
        validate_lat_sec = (self.register(self.is_okay_lat_sec), '%P')
        self.e_lat_sec = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lat_sec,
                                      validate='key', justify='center', font=font)
        self.e_lat_sec.grid(row=1, column=3)
        validate_lat_ns = (self.register(self.is_okay_lat_ns), '%P')
        self.e_lat_ns = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lat_ns,
                                     validate='key', justify='center', font=font)
        self.e_lat_ns.grid(row=1, column=4, padx=(0, 6))

        validate_lon_gr = (self.register(self.is_okay_lon_gr), '%P')
        self.e_lon_gr = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lon_gr,
                                     validate='key', justify='center', font=font)
        self.e_lon_gr.grid(row=2, column=1)
        validate_lon_min = (self.register(self.is_okay_lon_min), '%P')
        self.e_lon_min = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lon_min,
                                      validate='key',justify='center', font=font)
        self.e_lon_min.grid(row=2, column=2)
        validate_lon_sec = (self.register(self.is_okay_lon_sec), '%P')
        self.e_lon_sec = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lon_sec,
                                      validate='key', justify='center', font=font)
        self.e_lon_sec.grid(row=2, column=3)
        validate_lon_we = (self.register(self.is_okay_lon_we), '%P')
        self.e_lon_we = ctk.CTkEntry(self.frame_in, width=width, validatecommand=validate_lon_we,
                                     validate='key', justify='center', font=font)
        self.e_lon_we.grid(row=2, column=4, padx=(0, 6))

        self.btn = ctk.CTkButton(self.frame_in, text="Apply", font=font2,
                                 width=width, command=self.apply)
        self.btn.grid(row=3, column=2, pady=2)

        self.begin()

    def apply(self, arg=None) -> None:
        """Обработчик кнопки Apply"""
        dat = self.data_gps(self.e_lat_gr.get(), self.e_lat_min.get(), self.e_lat_sec.get(), self.e_lat_ns.get(),
                            self.e_lon_gr.get(), self.e_lon_min.get(), self.e_lon_sec.get(), self.e_lon_we.get(),
                            self.speed.get(), self.kurs.get())
        self.master.update_lat_lon(dat)

    def begin(self) -> None:
        """Начальные данные"""
        self.e_lon_we.insert(0, 'W')
        self.e_lat_ns.insert(0, 'N')
        self.e_lat_gr.insert(0, '58')
        self.e_lon_gr.insert(0, '030')
        self.e_lat_min.insert(0, '10')
        self.e_lon_min.insert(0, '13')
        self.e_lat_sec.insert(0, '45')
        self.e_lon_sec.insert(0, '52')

    def check_lat_lon(self, par: str, arg: str) -> None:
        """Проверка широты на 60 и долготы на 180"""
        if arg == '60' and par == '60':
            self.e_lat_min.delete(0, 'end')
            self.e_lat_min.insert(0, '00')
            self.e_lat_min.configure(state='disabled')
            self.e_lat_sec.delete(0, 'end')
            self.e_lat_sec.insert(0, '00')
            self.e_lat_sec.configure(state='disabled')
        elif arg == '60' and par != '60':
            self.e_lat_min.configure(state='normal')
            self.e_lat_sec.configure(state='normal')
        if arg == '180' and par == '180':
            self.e_lon_min.delete(0, 'end')
            self.e_lon_min.insert(0, '00')
            self.e_lon_min.configure(state='disabled')
            self.e_lon_sec.delete(0, 'end')
            self.e_lon_sec.insert(0, '00')
            self.e_lon_sec.configure(state='disabled')
        elif arg == '180' and par != '180':
            self.e_lon_min.configure(state='normal')
            self.e_lon_sec.configure(state='normal')

    def is_ok(self, par: str, limit: int, arg) -> bool:
        """Валидация. Если возвращает False, то значение временной зоны не изменить"""
        if par == '':
            return True
        try:
            value = int(par)
        except ValueError:
            return False
        if value > limit or value < 0 or len(par) > len(arg):
            return False
        self.check_lat_lon(par, arg)
        return True

    def is_okay_lat_gr(self, par: str) -> bool:
        """Валидация градусов широты"""
        return self.is_ok(par, 60, '60')

    def is_okay_lon_gr(self, par: str) -> bool:
        """Валидация градусов долготы"""
        return self.is_ok(par, 180, '180')

    def is_okay_lat_min(self, par: str) -> bool:
        """Валидация минут широты"""
        return self.is_ok(par, 59, '59')

    def is_okay_lon_min(self, par: str) -> bool:
        """Валидация минут долготы"""
        return self.is_ok(par, 59, '59')

    def is_okay_lat_sec(self, par: str) -> bool:
        """Валидация секунд широты"""
        return self.is_ok(par, 59, '59')

    def is_okay_lon_sec(self, par: str) -> bool:
        """Валидация секунд долготы"""
        return self.is_ok(par, 59, '59')

    @staticmethod
    def is_okay_lon_we(par: str) -> bool:
        """Валидация долготы"""
        if par == '':
            return True
        if len(par) > 1:
            return False
        if par not in ('W', 'E'):
            return False
        return True

    @staticmethod
    def is_okay_lat_ns(par: str) -> bool:
        """Валидация широты"""
        if par == '':
            return True
        if len(par) > 1:
            return False
        if par not in ('N', 'S'):
            return False
        return True

    def is_okay_kurs(self, par: str) -> bool:
        """Валидация курса"""
        return self.is_ok(par, 360, '360')

    def is_okay_speed(self, par: str) -> bool:
        """Валидация скорости"""
        return self.is_ok(par, 100, '100')


class GPS(ctk.CTkFrame):
    """Центральный фрейм"""

    def __init__(self, master):
        super().__init__(master, corner_radius=0, border_width=0, border_color="green")
        self.master = master

        self.d_send = Left(self)
        self.d_send.grid(row=0, column=0, padx=(1, 0), sticky="nsew")

        self.d_set = Right(self)
        self.d_set.grid(row=0, column=1, padx=(0, 1), sticky="nsew")

    def update_lat_lon(self, data: collections.namedtuple) -> None:
        """Обновить данные широты и долготы"""
        self.d_send.set_lat_lon(data)
