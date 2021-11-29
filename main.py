# ============================================================= #
#  Python Individual Project, Year 1, Semester 1                #
#                                                               #
#  Course: 13006107 Introduction to Computers and Programming   #
#  Program: Software Engineering Program                        #
#  University: Faculty of Engineering, KMITL                    #
#                                                               #
#  Project: CalcLab                                             #
#  Repository: https://github.com/DulapahV/CalcLab              #
#  Written by: Dulapah Vibulsanti (64011388)                    #
# ============================================================= #

"""
CalcLab requires the following modules, however, the program will install them
automatically. Should the program fail to do so, please install them manually
through the terminal with the following commands.
1. pip install numpy
2. pip install forex-python
"""

import math
import os
import random
import requests
import subprocess
import sys
import turtle as t
from abc import ABC, abstractmethod
from datetime import datetime

"""Determine which tkinter version to use"""
try:
    import tkinter as tk  # python 3
    from tkinter import messagebox
except ImportError:
    import Tkinter as tk  # python 2
    from Tkinter import messagebox

"""Check for numpy module"""
try:
    import numpy
except ImportError:
    print("> numpy module is missing!\n" +
          "Trying to install required module: numpy")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "numpy"])
    print()
finally:
    import numpy

"""Check for forex-python module"""
try:
    from forex_python.converter import (CurrencyRates, RatesNotAvailableError,
                                        DecimalFloatMismatchError)
    from forex_python.bitcoin import BtcConverter
except ImportError:
    print("> forex-python module is missing!\nTrying to install required " +
          "module: forex-python")
    subprocess.check_call([sys.executable, "-m", "pip", "install",
                          "forex-python"])
finally:
    from forex_python.converter import CurrencyRates, RatesNotAvailableError
    from forex_python.bitcoin import BtcConverter

"""
This list stores all the pages in the program, respectively. To add
more pages, put their class name into this list.

The page name will be automatically space-separated when encountering
capital letters.

The first page in this list will be the first page to appear.
"""
pages = ["Calculator", "SelectionMenu", "DateComparator", "CurrencyConverter",
         "VolumeConverter", "LengthConverter", "WeightAndMassConverter",
         "TemperatureConverter", "EnergyConverter", "AreaConverter",
         "SpeedConverter", "TimeConverter", "PowerConverter", "DataConverter",
         "PressureConverter", "AngleConverter"]

"""
The following lists/dictionaries store all the conversion units as well as
their conversion factors (only dictionary), respectively.

To add more conversion units to a list, simply add them to the list.

To add more conversion units to a dictionary, it must follow
the format: {"[unit name]": [conversion factor]}

Some conversion types cannot be manually added as it requires
more complex calculations (i.e. temperature).
"""
currency = ['BTC', 'AED', 'AUD', 'BRL', 'CAD', 'CHF', 'CLP', 'CNY', 'COP',
            'CZK', 'DKK', 'EUR', 'GBP', 'HKD', 'HUF', 'IDR', 'ILS', 'INR',
            'JPY', 'KRW', 'MXN', 'MYR', 'NOK', 'NZD', 'PHP', 'PLN', 'RON',
            'RUB', 'SAR', 'SEK', 'SGD', 'THB', 'TRY', 'TWD', 'USD', 'ZAR']

volume = {"Milliliters": 0.001,
          "Cubic centimeters": 0.001,
          "Liters": 1,
          "Cubic meters": 1000,
          "Teaspoons (US)": 0.004929,
          "Tablespoons (US)": 0.014787,
          "Fluid ounces (US)": 0.029574,
          "Cups (US)": 0.236588,
          "Pints (US)": 0.473176,
          "Quarts (US)": 0.946353,
          "Gallons (US)": 3.785412,
          "Cubic inches": 0.016387,
          "Cubic feet": 28.31685,
          "Cubic yards": 764.5549,
          "Teaspoons (UK)": 0.005919,
          "Tablespoons (UK)": 0.017758,
          "Fluid ounces (UK)": 0.028413,
          "Pints (UK)": 0.568261,
          "Quarts (UK)": 1.136523,
          "Gallons (UK)": 4.54609}

length = {"Nanometers": 10 ** -9,
          "Microns": 10 ** -6,
          "Millimeters": 0.001,
          "Centimeters": 0.01,
          "Meters": 1,
          "Kilometers": 1000,
          "Inches": 0.0254,
          "Feet": 0.3048,
          "Yards": 0.9144,
          "Miles": 1609.344,
          "Nautical Miles": 1852}

weightMass = {"Carats": 2 * (10 ** -4),
              "Milligrams": 10 ** -6,
              "Centigrams": 10 ** -5,
              "Decigrams": 10 ** -4,
              "Grams": 0.001,
              "Dekagrams": 0.01,
              "Hectogram": 0.1,
              "Kilograms": 1,
              "Metric tonnes": 1000,
              "Ounces": 0.02835,
              "Pounds": 0.453592,
              "Stone": 6.350293,
              "Short tons (US)": 907.1847,
              "Long tons (US)": 1016.047}

energy = {"Electron volts": 1.602177 * (10 ** -19),
          "Joules": 1,
          "Kilojoules": 1000,
          "Thermal calories": 4.184,
          "Food calories": 4184,
          "Foot-pounds": 1.355818,
          "British thermal units": 1055.056}

area = {"Square millimeters": 10 ** -6,
        "Square centimeters": 10 ** -4,
        "Square meters": 1,
        "Hectares": 10 ** 5,
        "Square kilometers": 10 ** 6,
        "Square inches": 6.45 * (10 ** -4),
        "Square feet": 0.092903,
        "Square yards": 0.836127,
        "Acres": 4046.856,
        "Square miles": 2589988}

speed = {"Centimeters per second": 0.01,
         "Meters per second": 1,
         "Kilometers per hour": 0.277778,
         "Feet per second": 0.3048,
         "Miles per hour": 0.447,
         "Knots": 0.5144,
         "Mach": 340.3}

time = {"Microseconds": 10 ** -6,
        "Milliseconds": 0.001,
        "Seconds": 1,
        "Minutes": 60,
        "Hours": 3600,
        "Days": 86400,
        "Weeks": 604800,
        "Years": 31557600}

power = {"Watts": 1,
         "Kilowats": 1000,
         "Horsepower (US)": 745.6999,
         "Foot-pounds/minute": 0.022597,
         "BTUs/minute": 17.58427}

data = {"Bits": 1.25 * (10 ** -7),
        "Bytes": 10 ** -6,
        "Kilobits": 1.25 * (10 ** -4),
        "Kibibits": 1.28 * (10 ** -4),
        "Kilobytes": 0.001,
        "Kibibytes": 0.001024,
        "Megabits": 0.125,
        "Mebibits": 0.131072,
        "Megabytes": 1,
        "Mebibytes": 1.048576,
        "Gigabits": 125,
        "Gibibits": 134.2177,
        "Gigabytes": 1000,
        "Gibibytes": 1073.742,
        "Terabits": 125000,
        "Tebibits": 137439,
        "Terabytes": 10 ** 6,
        "Tebibytes": 1099512,
        "Petabits": 1.25 * (10 ** 8),
        "Pebibits": 140737488,
        "Petabytes": 10 ** 9,
        "Pebibytes": 1125899907,
        "Exabits": 1.25 * (10 ** 8),
        "Exbibits": 144115188076,
        "Exabytes": 10 ** 12,
        "Exibytes": 1152921504607,
        "Zetabits": 1.25 * (10 ** 14),
        "Zebibits": 147573952589676,
        "Zetabytes": 10 ** 15,
        "Zebibytes": 1.180592 * (10 ** 15),
        "Yottabit": 1.25 * (10 ** 17),
        "Yobibits": 1.511157 * (10 ** 17),
        "Yottabyte": 10 ** 18,
        "Yobibytes": 1.208926 * (10 ** 18)}

pressure = {"Atmospheres": 101325,
            "Bars": 10 ** 5,
            "Kilopascals": 1000,
            "Millimeters of mercury": 133.3,
            "Pascals": 1,
            "Pounds per square inch": 6894.757}

angle = {"Degrees": 1,
         "Radians": 57.29578,
         "Gradians": 0.9}


class CalcLab(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        """
        This container is where all the frames (or pages) will be stacked
        on top of each other, then each one that we want visible will be
        raised above the others.
        """
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        classList = []
        self.frames = {}
        for element in pages:
            classList.append(self.str_to_class(element))
        for frame in classList:
            page_name = frame.__name__
            frame = frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        """
        Show the first page based on the first element in the pages list.
        """
        self.show_frame(pages[0])

        """Clear all history in history.txt"""
        try:
            open("history.txt", "w").close()
        except PermissionError:
            tk.messagebox.showerror("Error", "Error occurred: Cannot access" +
                                    " history.txt\n\nIt may be set to " +
                                    "read-only or you might not have\n" +
                                    "enough disk space.")
            sys.exit(1)

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        # reset answer field and various text to default after changing page
        try:
            frame.text.delete(0, tk.END)
            frame.text.insert(tk.END, 0)
            frame.ratesDetail.config(text="")
        except AttributeError:
            pass

    def str_to_class(self, className):
        return getattr(sys.modules[__name__], className)


class UpdateNumber(ABC):
    @abstractmethod
    def update(self, char):
        pass

    @abstractmethod
    def negative(self):
        pass

    @abstractmethod
    def clear(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def equal(self):
        pass

    @abstractmethod
    def set_text(self, value):
        AnswerField.set_value(self, value)

    @abstractmethod
    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class AnswerField:
    """Manipulating and getting value from the answer field."""

    def summon(self, row=2, columnSpan=5):
        self.text = tk.Entry(self, width=21, justify="right", bd=0,
                             bg="#000000", fg="#FFFFFF",
                             insertbackground="#FFFFFF",
                             selectbackground="#505050", font=("Arial", 32))
        self.text.grid(row=row, columnspan=columnSpan, pady=8)
        self.text.insert(tk.END, 0)

    def update(self, char):
        if len(self.text.get()) < 15:  # limit to 15 characters
            if char == ".":
                self.text.insert(tk.END, char)
                self.dotButton["state"] = "disabled"
                return None
            elif char == 0 and self.text.get() != "0":
                self.text.insert(tk.END, char)
            elif char != 0 and self.text.get() == "0":
                self.text.delete(len(self.text.get()) - 1, tk.END)
                self.text.insert(tk.END, char)
            elif self.text.get() == "-0":
                self.text.delete(1, tk.END)
                self.text.insert(tk.END, char)
            elif char != 0:
                self.text.insert(tk.END, char)

    def set_value(self, value):
        try:
            int(value)
            float(value)
        except (NameError, SyntaxError, ValueError, OverflowError):
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
            return 1
        if value % 1 == 0:
            value = int(value)
        if value == AnswerField.get_value(self):
            self.text.config(fg="#000000")
            self.after(100, lambda: self.text.config(fg="#FFFFFF"))
        if "." in str(value):
            self.dotButton["state"] = "disabled"
        else:
            self.dotButton["state"] = "normal"
        self.text.delete(0, tk.END)
        if len(str(int(value))) <= 18 and len(self.text.get()) <= 18:
            self.text.insert(0,
                             f"{round(value, 18 - len(str(int(value)))):,}")
        else:
            self.text.insert(0, f"{round(value, 12):e}")

    def negative(self):
        if (self.text.get().replace(',', '') == "0" or
                float(self.text.get().replace(',', '')) > 0):
            self.text.insert(0, "-")
        else:
            self.text.delete(0, 1)

    def clear(self):
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        if len(self.text.get()) != 1:
            self.text.delete(len(self.text.get()) - 1, tk.END)
        else:
            self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"

    def get_value(self):
        try:
            self.__value = eval(self.text.get().replace(',', ''))
        except (NameError, SyntaxError, ValueError, OverflowError):
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
            return None
        return self.__value


class NumPad(AnswerField):
    """NumPad for converter tools."""

    def summon(self):
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                     command=self.clear).grid(row=3, column=2)
        self.negativeButton = tk.Button(self, width=5, height=2, text="+/-", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                        command=self.negative)
        self.negativeButton.grid(row=3, column=3)
        self.deleteButton = tk.Button(self, width=5, height=2, text="⌫", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                      command=self.delete).grid(row=3, column=4)

        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                     activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0)
        self.sevenButton.grid(row=4, column=2)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                     activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                     self.update(8)).grid(row=4, column=3)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(9)).grid(row=4, column=4)

        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(4)).grid(row=5, column=2)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(5)).grid(row=5, column=3)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update(6)).grid(row=5, column=4)

        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update(1)).grid(row=6, column=2)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update(2)).grid(row=6, column=3)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                     activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                     self.update(3)).grid(row=6, column=4)

        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(0)).grid(row=7, column=3)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update("."))
        self.dotButton.grid(row=7, column=4)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="#FFFFFF",
                                     activebackground="#FFBD69", activeforeground="#FFFFFF", bd=0,
                                     command=self.equal).grid(row=7, column=2)

    def disable_negative(self):
        self.negativeButton["state"] = "disabled"


class Frame:
    """Customization for header text and background color."""

    def set_bg_color(self, color):
        self.configure(bg=color)

    def set_header_text(self, text):
        self.header = tk.Label(self, text=text, font=("Arial", 16),
                               bg="#000000", fg="#FFFFFF").place(x=60, y=8)


class SelectionButton:
    """Selection button for user to enter tools selection menu."""

    def summon(self, controller):
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="#FFFFFF", bd=0, font=("Arial", 18), width=3,
                                      activebackground="#767676", activeforeground="#FFFFFF", command=lambda:
                                      controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")


class OptionMenu:
    """Option menu for selecting conversion units in converter tools."""

    def summon(self, variable1, variable2, list):
        self.fromText = tk.Label(self, text="From", font=("Arial", 16), bg="#000000", fg="#FFFFFF"
                                 ).grid(row=3, column=1, padx=8, sticky="w")

        self.fromUnit = tk.OptionMenu(self, variable1, *list)
        self.fromUnit.config(width=19, bd=0, bg="#505050", fg="#FFFFFF", activebackground="#A5A5A5",
                             activeforeground="#FFFFFF",
                             font=("Arial", 18), anchor="w")
        self.fromUnit.grid(row=4, column=1, padx=8)

        self.toText = tk.Label(self, text="To", font=("Arial", 16), bg="#000000", fg="#FFFFFF"
                               ).grid(row=5, column=1, padx=8, sticky="w")

        self.toUnit = tk.OptionMenu(self, variable2, *list)
        self.toUnit.config(width=19, bd=0, bg="#505050", fg="#FFFFFF", activebackground="#A5A5A5",
                           activeforeground="#FFFFFF", font=("Arial", 18), anchor="w")
        self.toUnit.grid(row=6, column=1, padx=8)


class VerticalScrolledFrame(tk.Frame):
    """Initializing vertical scrolled frame for the tools selection menu."""

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        v = tk.Scrollbar(self, orient=tk.VERTICAL)
        v.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=v.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        v.config(command=canvas.yview)

        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        def _configure_interior(event):
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


class SelectionMenu(tk.Frame):
    """
    Initializing tools selection menu and putting buttons into the
    vertical scrolled frame.
    """

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")

        scrollFrame = VerticalScrolledFrame(self)
        scrollFrame.pack(fill="both", expand=True)

        # Remove selection menu button from the
        # list since user is already in that page
        pages.remove("SelectionMenu")
        pageList = pages
        for index, page in enumerate(pageList):
            spacedText = ""
            for i, letter in enumerate(page):
                if i and letter.isupper():
                    spacedText += " "
                spacedText += letter
            self.button = tk.Button(scrollFrame.interior, width=36, font=("Arial", 18), text=f"  {spacedText}",
                                    anchor="w", bg="#1C1C1C", fg="#FFFFFF", activebackground="#767676",
                                    activeforeground="#FFFFFF", bd=1,
                                    command=lambda index=index: open_page(pageList[index])).pack()

        def open_page(page):
            controller.show_frame(page)


class Calculator(tk.Frame, UpdateNumber):
    """Calculator (scientific)."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Calculator")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__memory = 0
        self.__reVal = 0
        self.__lockSecInput = False
        self.__lockOperatorInput = False
        self.__operator = None

        AnswerField.summon(self, 2, 8)

        self.graphButton = tk.Button(self, text="⧟", bg="#1C1C1C", fg="#FFFFFF", bd=0, font=("Cambria", 18), width=3,
                                     activebackground="#767676", activeforeground="#FFFFFF", command=self.plot_graph
                                     ).place(x=442, y=0)

        self.historyButton = tk.Button(self, text="↺", bg="#1C1C1C", fg="#FFFFFF", bd=0, font=("Cambria", 18), width=3,
                                       activebackground="#767676", activeforeground="#FFFFFF", command=self.show_history
                                       ).grid(row=1, column=7, sticky="E")

        self.factButton = tk.Button(self, width=5, height=2, text="x!", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                    activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                    command=self.factorial).grid(row=3, column=1)
        self.sqrtButton = tk.Button(self, width=5, height=2, text="√x", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                    activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                    command=self.sqrt).grid(row=3, column=2)
        self.squareButton = tk.Button(self, width=5, height=2, text="x²", font=("Arial", 18), bg="#1C1C1C",
                                      fg="#FFFFFF", activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                      command=self.square).grid(row=3, column=3)
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                     command=self.clear).grid(row=3, column=4)
        self.percentButton = tk.Button(self, width=5, height=2, text="%", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                       command=self.percent).grid(row=3, column=5)
        self.deleteButton = tk.Button(self, width=5, height=2, text="⌫", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                      command=self.delete).grid(row=3, column=6)
        self.divideButton = tk.Button(self, width=5, height=2, text="÷", font=("Arial", 18), bg="#FF9500", fg="#FFFFFF",
                                      activebackground="#FF9500", activeforeground="#FFFFFF", bd=0, command=self.divide)
        self.divideButton.grid(row=3, column=7)

        self.lnButton = tk.Button(self, width=5, height=2, text="ln", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                  activebackground="#767676", activeforeground="#FFFFFF", bd=0, command=self.ln).grid(
                                  row=4, column=1)
        self.cbrtButton = tk.Button(self, width=5, height=2, text="∛x", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                    activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                    command=self.cbrt).grid(row=4, column=2)
        self.cubeButton = tk.Button(self, width=5, height=2, text="x³", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                    activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                    command=self.cube).grid(row=4, column=3)
        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                     activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                     self.update(7)).grid(row=4, column=4)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                     activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                     self.update(8)).grid(row=4, column=5)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(9)).grid(row=4, column=6)
        self.multiplyButton = tk.Button(self, width=5, height=2, text="x", font=("Arial", 18), bg="#FF9500",
                                        fg="#FFFFFF", activebackground="#FF9500", activeforeground="#FFFFFF", bd=0,
                                        command=self.multiply)
        self.multiplyButton.grid(row=4, column=7)

        self.commonLog = tk.Button(self, width=5, height=2, text="log", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                   activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                   command=self.log10).grid(row=5, column=1)
        self.sinhButton = tk.Button(self, width=5, height=2, text="sinh", font=("Arial", 18), bg="#1C1C1C",
                                    fg="#FFFFFF", activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                    command=self.sinh).grid(row=5, column=2)
        self.sinButton = tk.Button(self, width=5, height=2, text="sin", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                   activebackground="#767676", activeforeground="#FFFFFF", bd=0, command=self.sin).grid(
                                   row=5, column=3)
        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(4)).grid(row=5, column=4)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(5)).grid(row=5, column=5)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update(6)).grid(row=5, column=6)
        self.minusButton = tk.Button(self, width=5, height=2, text="-", font=("Arial", 18), bg="#FF9500", fg="#FFFFFF",
                                     activebackground="#FF9500", activeforeground="#FFFFFF", bd=0, command=self.minus)
        self.minusButton.grid(row=5, column=7)

        self.eButton = tk.Button(self, width=5, height=2, text="e", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                 bd=0, activebackground="#767676", activeforeground="#FFFFFF", command=self.eVal).grid(
                                 row=6, column=1)
        self.coshButton = tk.Button(self, width=5, height=2, text="cosh", font=("Arial", 18), bg="#1C1C1C",
                                    fg="#FFFFFF", activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                    command=self.cosh).grid(row=6, column=2)
        self.cosButton = tk.Button(self, width=5, height=2, text="cos", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                   activebackground="#767676", activeforeground="#FFFFFF", bd=0, command=self.cos).grid(
                                   row=6, column=3)
        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update(1)).grid(row=6, column=4)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update(2)).grid(row=6, column=5)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                     activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                     self.update(3)).grid(row=6, column=6)
        self.plusButton = tk.Button(self, width=5, height=2, text="+", font=("Arial", 18), bg="#FF9500", fg="#FFFFFF",
                                    activebackground="#FF9500", activeforeground="#FFFFFF", bd=0, command=self.add)
        self.plusButton.grid(row=6, column=7)

        self.piButton = tk.Button(self, width=5, height=2, text="π", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                  bd=0, activebackground="#767676", activeforeground="#FFFFFF", command=self.piVal).grid(
                                  row=7, column=1)
        self.tanhButton = tk.Button(self, width=5, height=2, text="tanh", font=("Arial", 18), bg="#1C1C1C",
                                    fg="#FFFFFF", activebackground="#767676", activeforeground="#FFFFFF", bd=0,
                                    command=self.tanh).grid(row=7, column=2)
        self.tanButton = tk.Button(self, width=5, height=2, text="tan", font=("Arial", 18), bg="#1C1C1C", fg="#FFFFFF",
                                   activebackground="#767676", activeforeground="#FFFFFF", bd=0, command=self.tan).grid(
                                   row=7, column=3)
        self.negativeButton = tk.Button(self, width=5, height=2, text="+/-", font=("Arial", 18), bg="#505050",
                                        activebackground="#A5A5A5", activeforeground="#FFFFFF", fg="#FFFFFF", bd=0,
                                        command=self.negative).grid(row=7, column=4)
        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                    activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                    self.update(0)).grid(row=7, column=5)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="#FFFFFF",
                                   activebackground="#A5A5A5", activeforeground="#FFFFFF", bd=0, command=lambda:
                                   self.update("."))
        self.dotButton.grid(row=7, column=6)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="#FFFFFF",
                                     activebackground="#FFBD69", activeforeground="#FFFFFF", bd=0,
                                     command=self.equal)
        self.equalButton.grid(row=7, column=7)

    def update(self, char):
        self.__lockOperatorInput = False
        if self.__lockSecInput:
            self.dotButton["state"] = "normal"
            self.text.delete(0, tk.END)
            self.text.insert(tk.END, 0)
            self.__lockSecInput = False
        self.plusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.minusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.multiplyButton.config(bg="#FF9500", fg="#FFFFFF")
        self.divideButton.config(bg="#FF9500", fg="#FFFFFF")
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        self.plusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.minusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.multiplyButton.config(bg="#FF9500", fg="#FFFFFF")
        self.divideButton.config(bg="#FF9500", fg="#FFFFFF")
        self.__memory = 0
        self.__reVal = 0
        self.__lockOperatorInput = True
        self.__operator = None
        AnswerField.clear(self)

    def delete(self):
        if not self.__lockOperatorInput:
            AnswerField.delete(self)

    def equal(self):
        self.__lockOperatorInput = True
        self.plusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.minusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.multiplyButton.config(bg="#FF9500", fg="#FFFFFF")
        self.divideButton.config(bg="#FF9500", fg="#FFFFFF")
        self.__displayedText = self.text.get().replace(',', '')
        history = open("history.txt", "a")
        try:
            float(self.__memory)
            float(self.__displayedText)
        except ValueError:
            try:
                float(self.__memory)
                history.write(f"{self.text.get()} = {eval(self.text.get())}\n")
                self.set_text(eval(self.text.get()))
            except:
                self.display_error()
                return 1
        if self.__operator is not None:
            if self.__operator == "+":
                if self.__reVal == 0:
                    self.__value = eval(str(self.__memory)) + eval(str(self.__displayedText))
                    self.__reVal = eval(str(self.__displayedText))
                else:
                    self.__value += self.__reVal
            elif self.__operator == "-":
                if self.__reVal == 0:
                    self.__value = float(self.__memory) - float(self.__displayedText)
                    self.__reVal = float(self.__displayedText)
                else:
                    self.__value -= self.__reVal
            elif self.__operator == "*":
                if self.__reVal == 0:
                    self.__value = float(self.__memory) * float(self.__displayedText)
                    self.__reVal = float(self.__displayedText)
                else:
                    self.__value *= self.__reVal
            elif self.__operator == "/":
                try:
                    float(self.__memory) / float(self.__displayedText)
                except ZeroDivisionError:
                    self.display_error()
                    return 1
                if self.__reVal == 0:
                    self.__value = float(self.__memory) / float(self.__displayedText)
                    self.__reVal = float(self.__displayedText)
                else:
                    self.__value /= self.__reVal
            self.__lockSecInput = True
            self.set_text(self.__value)
            if self.__operator is not None:
                history.write(f"{self.__memory} {self.__operator} {eval(self.__displayedText)} = {self.text.get()}\n")
            history.close()

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")

    def add(self):
        if not self.__lockOperatorInput:
            self.equal()
        self.plusButton.config(bg="#FFFFFF", fg="#FF9500", activebackground="#FFFFFF", activeforeground="#FF9500")
        self.minusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.multiplyButton.config(bg="#FF9500", fg="#FFFFFF")
        self.divideButton.config(bg="#FF9500", fg="#FFFFFF")
        try:
            self.__memory = eval(self.text.get().replace(',', ''))
        except (NameError, SyntaxError, ValueError, OverflowError):
            self.display_error()
            return 1
        self.__reVal = 0
        self.__lockOperatorInput = True
        self.__lockSecInput = True
        self.__operator = "+"
        self.dotButton["state"] = "normal"

    def minus(self):
        if not self.__lockOperatorInput:
            self.equal()
        self.plusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.minusButton.config(bg="#FFFFFF", fg="#FF9500", activebackground="#FFFFFF", activeforeground="#FF9500")
        self.multiplyButton.config(bg="#FF9500", fg="#FFFFFF")
        self.divideButton.config(bg="#FF9500", fg="#FFFFFF")
        try:
            self.__memory = self.text.get().replace(',', '')
        except (NameError, SyntaxError, ValueError, OverflowError):
            self.display_error()
            return 1
        self.__reVal = 0
        self.__lockOperatorInput = True
        self.__lockSecInput = True
        self.__operator = "-"
        self.dotButton["state"] = "normal"

    def multiply(self):
        if not self.__lockOperatorInput:
            self.equal()
        self.plusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.minusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.multiplyButton.config(bg="#FFFFFF", fg="#FF9500", activebackground="#FFFFFF", activeforeground="#FF9500")
        self.divideButton.config(bg="#FF9500", fg="#FFFFFF")
        try:
            self.__memory = self.text.get().replace(',', '')
        except (NameError, SyntaxError, ValueError, OverflowError):
            self.display_error()
            return 1
        self.__reVal = 0
        self.__lockOperatorInput = True
        self.__lockSecInput = True
        self.__operator = "*"
        self.dotButton["state"] = "normal"

    def divide(self):
        if not self.__lockOperatorInput:
            self.equal()
        self.plusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.minusButton.config(bg="#FF9500", fg="#FFFFFF")
        self.multiplyButton.config(bg="#FF9500", fg="#FFFFFF")
        self.divideButton.config(bg="#FFFFFF", fg="#FF9500", activebackground="#FFFFFF", activeforeground="#FF9500")
        try:
            self.__memory = self.text.get().replace(',', '')
        except:
            self.display_error()
            return 1
        self.__reVal = 0
        self.__lockOperatorInput = True
        self.__lockSecInput = True
        self.__operator = "/"
        self.dotButton["state"] = "normal"

    def percent(self):
        try:
            self.set_text(eval(self.text.get().replace(',', '')) / 100)
        except:
            self.display_error()
            return 1

    def square(self):
        try:
            eval(self.text.get().replace(',', ''))**2
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(value**2)
        history = open("history.txt", "a")
        history.write(f"({value})^2 = {self.text.get()}\n")
        history.close()

    def cube(self):
        try:
            eval(self.text.get().replace(',', ''))**3
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(value**3)
        history = open("history.txt", "a")
        history.write(f"({value})^3 = {self.text.get()}\n")
        history.close()

    def sqrt(self):
        try:
            math.sqrt(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.sqrt(value))
        history = open("history.txt", "a")
        history.write(f"sqrt({value}) = {self.text.get()}\n")
        history.close()

    def cbrt(self):
        try:
            numpy.cbrt(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(numpy.cbrt(value))
        history = open("history.txt", "a")
        history.write(f"cbrt({value}) = {self.text.get()}\n")
        history.close()

    def sin(self):
        try:
            math.sin(math.radians(eval(self.text.get().replace(',', ''))))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.sin(math.radians(value)))
        history = open("history.txt", "a")
        history.write(f"sin({value}) = {self.text.get()}\n")
        history.close()

    def cos(self):
        try:
            math.cos(math.radians(eval(self.text.get().replace(',', ''))))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.cos(math.radians(value)))
        history = open("history.txt", "a")
        history.write(f"cos({value}) = {self.text.get()}\n")
        history.close()

    def tan(self):
        try:
            math.tan(math.radians(eval(self.text.get().replace(',', ''))))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.tan(math.radians(value)))
        history = open("history.txt", "a")
        history.write(f"tan({value}) = {self.text.get()}\n")
        history.close()

    def sinh(self):
        try:
            math.sinh(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.sinh(value))
        history = open("history.txt", "a")
        history.write(f"sinh({value}) = {self.text.get()}\n")
        history.close()

    def cosh(self):
        try:
            math.cosh(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.cosh(value))
        history = open("history.txt", "a")
        history.write(f"cosh({value}) = {self.text.get()}\n")
        history.close()

    def tanh(self):
        try:
            math.tanh(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.tanh(value))
        history = open("history.txt", "a")
        history.write(f"tanh({value}) = {self.text.get()}\n")
        history.close()

    def ln(self):
        try:
            math.log(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.log(value))
        history = open("history.txt", "a")
        history.write(f"ln({value}) = {self.text.get()}\n")
        history.close()

    def log10(self):
        try:
            math.log10(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.log10(value))
        history = open("history.txt", "a")
        history.write(f"log10({value}) = {self.text.get()}\n")
        history.close()

    def factorial(self):
        try:
            math.factorial(eval(self.text.get().replace(',', '')))
        except:
            self.display_error()
            return 1
        value = eval(self.text.get().replace(',', ''))
        self.set_text(math.factorial(value))
        history = open("history.txt", "a")
        history.write(f"({value})! = {self.text.get()}\n")
        history.close()

    def eVal(self):
        self.set_text(math.e)

    def piVal(self):
        self.set_text(math.pi)

    def show_history(self):
        popup = tk.Tk()
        popup.title("History")
        popup.geometry("420x720")
        popup.minsize(420, 720)
        popup.maxsize(1024, 720)
        popup.configure(bg="#000000")
        popup.focus_force()
        v = tk.Scrollbar(popup)
        h = tk.Scrollbar(popup, orient="horizontal")
        v.pack(side="right", fill="y")
        h.pack(side="bottom", fill="x")
        history = open("history.txt", "r")
        historySize = os.path.getsize("history.txt")
        text = ("There is no history yet.\n\nTip:\nYou can copy numbers " +
                "from here\nand paste them into the app's\nanswer field.")
        clearButton = tk.Button(popup, text="🗑", height=1, font=("Arial", 18), bg="#FF9500", fg="#FFFFFF",
                                activebackground="#FF9500", activeforeground="#FFFFFF", bd=0,
                                command=lambda: [open("history.txt", "w").close(), textBox.delete("1.0", tk.END),
                                textBox.insert(tk.END, "There is no history yet.\n\nTip:\nYou can copy numbers " +
                                               "from here\nand paste them into the app's\nanswer field."),
                                                 clearButton.destroy()])
        if historySize != 0:
            text = history.read()[:-1]
            clearButton.pack(side="bottom", anchor="e", padx=10, pady=5)
        history.close()
        textBox = tk.Text(popup, height=21, bg="#000000", fg="#FFFFFF", insertbackground="#FFFFFF",
                          selectbackground="#505050", bd=0, font=("Arial", 18), wrap="none", spacing3=3,
                          yscrollcommand=v.set)
        textBox.pack(anchor="w", padx=10, pady=10)
        textBox.insert(tk.END, text)

        h.config(command=textBox.xview)
        v.config(command=textBox.yview)
        textBox.yview(tk.END)
        popup.mainloop()

    def plot_graph(self):
        errTitle = "Graph Plotter Error"
        syntaxErrMsg = ("Error occurred: Invalid syntax\n\n" +
                        "Expression must be in the format:\ny=mx+c, y=mx^n+c, y=n, " +
                        "x=n\n\nFor example:\ny=20\nx=(22/7)+5\ny=2x\ny=-2x+10\n" +
                        "y = (1/2)x - (100/3)\ny=0.03x^3+20")
        slopeLowErrMsg = "Error occurred: Slope (m) value is too low"
        exponentErrMsg = "Error occurred: Unexpected slope (m) value"
        exponentHighErrMsg = "Error occurred: Exponent value must be between 0 and 6, inclusive"
        exponentInterceptErrMsg = ("Error occurred: Unexpected y-intercept (c) value and/or "+ 
                                   "unexpected exponent value")
        font = ("Arial", 18)
        isXonly = False
        # remove spaces and convert expression to lower case
        expression = self.text.get().replace(" ", "").lower()

        # check if the expression is "y=" or "x=" or "f(x)=", if not then raise error
        if expression[:2] != "y=" and expression[:2] != "x=" and expression[:5] != "f(x)=":
            tk.messagebox.showinfo(errTitle, syntaxErrMsg)
            return 1

        # check if expression is "x=" or not
        if expression[:2] == "x=":
            isXonly = True

        # store "y=","x=", "f(x)=" prefix to a variable to be used when writing equation later on,
        # then remove "y=","x=", "f(x)=" prefix
        if expression[:2] == "y=" or expression[:2] == "x=":
            prefix = expression[:2]
            expression = expression.removeprefix("y=")
            expression = expression.removeprefix("x=")
        else:
            prefix = expression[:5]
            expression = expression.removeprefix("f(x)=")  

        expo = 1 # default value of exponent
        c = 0 # default value of y-intercept

        # check if expression is "y=x", "y=-x", "x=y", or "x=-y"
        if expression.split("x") == ['', '']:
            m = 1; c = 0
        elif expression.split("x") == ['-', '']:
            m = -1; c = 0
        elif expression.split("y") == ['', '']:
            m = 1; c = 0
            isXonly = False
        elif expression.split("y") == ['-', '']:
            m = -1; c = 0
            isXonly = False
            
        else:
            # split expression between "x"
            # if the front split contains no number, then m = 1 or -1. Else, eval m
            valBeforeX = expression.split("x")[0]
            if valBeforeX == "":
                m = 1
            elif valBeforeX == "-":
                m = -1
            else:
                try:
                    m = round(eval(valBeforeX), 2)
                except (SyntaxError, NameError, TypeError):
                    tk.messagebox.showinfo(errTitle, exponentErrMsg)
                    return 1
            
            # check if there is other term left
            if not expression.replace(str(m), ""):
                expo = 0
            else:
                # if the back split contains no number, then c = 0. Else, eval c
                valAfterX = expression.split("x")[1]
                # print(valAfterX)
                if valAfterX == "":
                    c = 0
                else:
                    try:
                        c = round(eval(valAfterX), 2)
                    except (SyntaxError, NameError, TypeError):
                        # if the expression contains exponent (back split contains "^"), split again based on "+" and "-",
                        # then eval expo
                        valBeforeOp = valAfterX.split("+")[0][1:]
                        if "-" in valBeforeOp:
                            valBeforeOp = valAfterX.split("-")[0][1:]
                        if valBeforeOp == "":
                            tk.messagebox.showinfo(errTitle, exponentInterceptErrMsg)
                            return 1
                        try:
                            valBeforeOp = round(eval(valBeforeOp), 2)
                        except (SyntaxError, NameError, TypeError):
                            tk.messagebox.showinfo(errTitle, exponentErrMsg)
                            return 1
                        expo = valBeforeOp
                        
                        # get c value
                        # check whether there is c value or not, if so, split based on "+" and "-", then eval c
                        if len(valAfterX.split("+")) == 1 and len(valAfterX.split("-")) == 1:
                            c = 0
                        else:
                            try:
                                try:
                                    valAfterOp = eval(valAfterX.split("+")[1])
                                except (SyntaxError, NameError, TypeError):
                                    tk.messagebox.showinfo(errTitle, exponentInterceptErrMsg)
                                    return 1
                            except IndexError:
                                try:
                                    valAfterOp = eval(valAfterX.split("-")[1]) * -1
                                except (SyntaxError, NameError, TypeError):
                                    tk.messagebox.showinfo(errTitle, exponentInterceptErrMsg)
                                    return 1
                            c = valAfterOp
        # prevent user from entering too high exponent value
        if expo > 6:
            tk.messagebox.showinfo(errTitle, exponentHighErrMsg)
            return 1
        
        try:
            if expo == 0:
                xInt = (0 - c) / m
            elif expo % 2 != 0:
                xInt = round((((c) / m) ** (1/float(expo)) * -1), 2)
                if xInt == -0:
                    xInt = 0
            elif expo % 2 == 0 and c == 0:
                xInt = 0
            else:
                xInt = "n/a"
        except ZeroDivisionError:
            tk.messagebox.showinfo(errTitle, slopeLowErrMsg)
            return 1
        try:
            if xInt % 1 == 0:
                xInt = int(xInt)
        except TypeError:
            pass
        yInt = c

        try:
            t.setworldcoordinates(-100, -100, 100, 100)
        except:
            pass
        t.title("Graph Plotter")
        t.setworldcoordinates(-100, -100, 100, 100)
        t.ht()
        t.tracer(0, 0)
        t.pen(pencolor="black", pensize=0)
        for axis in range(4):
            interval = 0
            sign = 1
            if axis == 1 or axis == 2:
                sign = -1
            for i in range(25):
                t.dot()
                t.write(interval * sign)
                t.fd(10)
                interval += 10
            t.bk(250)
            t.rt(90)

        color = "#%06x" % random.randint(0, 0xFFFFFF)
        t.pu()
        t.pen(pencolor=color, pensize=4)

        if m == 1 or m == -1:
            slope = ""
        else:
            slope = m
        
        if prefix == "y=" and expo == 0:
            var = ""
            xInt = "n/a"; yInt = slope
        elif prefix == "y=":
            var = "x"
        else:
            var = "y"

        if isXonly:
            t.setpos(m, -250)
            t.pd()
            t.setpos(m, random.randint(-10, 10))
            tempX, tempY = t.pos()
            t.pu()
            t.setx(tempX + random.randint(0, 10))
            t.write(f"{prefix}{slope}, xInt = {slope}, yInt = 'n/a'", font=font)
            t.setpos(tempX, tempY)
            t.pd()
            t.setpos(m, 250)
        else:
            for x in range(-250, 250):
                y = m * (x**expo) + c
                if x != -250:
                    t.pd()
                if x == 0:
                    t.pu()
                    tempX, tempY = t.pos()
                    t.setpos(random.randint(int(tempX) - 10, int(tempX) + 10),
                            random.randint(int(tempY) - 10, int(tempY) + 10))
                    if expo == 0 or expo == 1:
                        if c == 0:
                            if m == 0 or m == 1:
                                t.write(f"      {prefix}{var}, {xInt = }, {yInt = }", font=font)
                            elif m == -1:
                                t.write(f"      {prefix}-{slope}{var}, {xInt = }, {yInt = }", font=font)
                            else:
                                t.write(f"      {prefix}{slope}{var}, {xInt = }, {yInt = }", font=font)
                        elif c >= 0:
                            if m == 0 or m == 1:
                                t.write(f"      {prefix}{var}+{c}, {xInt = }, {yInt = }", font=font)
                            elif m == -1:
                                t.write(f"      {prefix}-{slope}{var}+{c}, {xInt = }, {yInt = }", font=font)
                            else:
                                t.write(f"      {prefix}{slope}{var}+{c}, {xInt = }, {yInt = }", font=font)
                        else:
                            if m == 0 or m == 1:
                                t.write(f"      {prefix}{var}{c}, {xInt = }, {yInt = }", font=font)
                            elif m == -1:
                                t.write(f"      {prefix}-{slope}{var}{c}, {xInt = }, {yInt = }", font=font)
                            else:
                                t.write(f"      {prefix}{slope}{var}{c}, {xInt = }, {yInt = }", font=font)
                    else:
                        if c == 0:
                            if m == 0 or m == 1:
                                t.write(f"      {prefix}{var}^{expo}, {xInt = }, {yInt = }", font=font)
                            elif m == -1:
                                t.write(f"      {prefix}-{slope}{var}^{expo}, {xInt = }, {yInt = }", font=font)
                            else:
                                t.write(f"      {prefix}{slope}{var}^{expo}, {xInt = }, {yInt = }", font=font)
                        elif c >= 0:
                            if m == 0 or m == 1:
                                t.write(f"      {prefix}{var}^{expo}+{c}, {xInt = }, {yInt = }", font=font)
                            elif m == -1:
                                t.write(f"      {prefix}-{slope}{var}^{expo}+{c}, {xInt = }, {yInt = }", font=font)
                            else:
                                t.write(f"      {prefix}{slope}{var}^{expo}+{c}, {xInt = }, {yInt = }", font=font)
                        else:
                            if m == 0 or m == 1:
                                t.write(f"      {prefix}{var}^{expo}{c}, {xInt = }, {yInt = }", font=font)
                            elif m == -1:
                                t.write(f"      {prefix}-{slope}{var}^{expo}{c}, {xInt = }, {yInt = }", font=font)
                            else:
                                t.write(f"      {prefix}{slope}{var}^{expo}{c}, {xInt = }, {yInt = }", font=font)
                    t.setpos(tempX, tempY)
                    t.pd()
                t.setpos(x, y)
        t.pu()
        t.setpos(0, 0)
        t.update()


class DateComparator(tk.Frame):
    """Date comparator."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.__day = 0
        self.__week = 0
        self.__month = 0
        self.__year = 0
        self.__sumDay = 0
        self.__text = ""

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Date Comparator")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="#FFFFFF", bd=0, font=("Arial", 18), width=3,
                                      command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, sticky="w")

        self.text = tk.Entry(self, width=32, justify="right", bd=0, disabledbackground="#000000",
                             disabledforeground="#FFFFFF", font=("Arial", 22))
        self.text.grid(row=2, padx=8, pady=8, sticky="w")
        self.text.insert(tk.END, "Same dates")
        self.text["state"] = "disabled"

        self.textDay = tk.Entry(self, width=32, justify="right", bd=0, disabledbackground="#000000",
                                disabledforeground="#FFFFFF", font=("Arial", 22))
        self.textDay.grid(row=3, padx=8, pady=8, sticky="w")
        self.textDay.insert(tk.END, "0 day")
        self.textDay["state"] = "disabled"

        self.noticeText = tk.Label(self, text="From (format: 02/12/2021)", font=("Arial", 16), bg="#000000",
                                   fg="#FFFFFF").grid(row=5, padx=8, sticky="w")

        self.fromDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="#FFFFFF", font=("Arial", 20),
                                 insertbackground="#FFFFFF", selectbackground="#A5A5A5", highlightthickness=2)
        self.fromDate.grid(row=6, padx=8, pady=8, sticky="w")
        self.fromDate.insert(tk.END, datetime.today().strftime("%d/%m/%Y"))

        self.noticeText = tk.Label(self, text="To (format: 02/12/2021)", font=("Arial", 16), bg="#000000",
                                   fg="#FFFFFF").grid(row=7, padx=8, sticky="w")

        self.toDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="#FFFFFF", font=("Arial", 20),
                               insertbackground="#FFFFFF", selectbackground="#A5A5A5", highlightthickness=2)
        self.toDate.grid(row=8, padx=8, pady=8, sticky="w")
        self.toDate.insert(tk.END, datetime.today().strftime("%d/%m/%Y"))

        self.calcButton = tk.Button(self, height=2, text="Calculate", font=("Arial", 18), bg="#FF9500", fg="#FFFFFF",
                                    activebackground="#FFBD69", activeforeground="#FFFFFF", bd=0,
                                    command=self.equal).grid(row=10, padx=8, sticky="w")

    def equal(self):
        try:
            self.__fromDay, self.__fromMonth, self.__fromYear = self.fromDate.get().split("/")
            self.__toDay, self.__toMonth, self.__toYear = self.toDate.get().split("/")
        except ValueError:
            self.display_error()
            return 1
        self.__fromDay, self.__fromMonth, self.__fromYear = self.fromDate.get().split("/")
        self.__toDay, self.__toMonth, self.__toYear = self.toDate.get().split("/")
        try:
            self.__fromDay = int(self.__fromDay)
            self.__fromMonth = int(self.__fromMonth)
            self.__fromYear = int(self.__fromYear)
            self.__toDay = int(self.__toDay)
            self.__toMonth = int(self.__toMonth)
            self.__toYear = int(self.__toYear)
        except ValueError:
            self.display_error()
            return 1
        if (1 <= self.__fromDay <= 31 and 1 <= self.__toDay <= 31 and 1 <= self.__fromMonth <= 12 and
                1 <= self.__toMonth <= 12 and self.__fromYear >= 0 and self.__toYear >= 0):
            self.__sumDay = abs(self.__fromDay - self.__toDay) + (abs(self.__fromMonth - self.__toMonth) * 30) + (abs(
                self.__fromYear - self.__toYear) * 365)
            self.__year = self.__sumDay // 365
            self.__month = (self.__sumDay - self.__year * 365) // 30
            self.__week = (self.__sumDay - self.__year * 365 - self.__month * 30) // 7
            self.__day = (self.__sumDay - self.__year * 365 - self.__month * 30 - self.__week * 7)
            if self.__year == 0 and self.__month == 0 and self.__week == 0 and self.__day == 0:
                self.__text = "Same dates"
            else:
                self.__text = f"{self.__year:,} years, {self.__month} months, {self.__week} weeks, {self.__day} days"
                if self.__year == 1 and len(str(self.__year)) == 1:
                    self.__text = self.__text.replace("1 years", "1 year")
                if self.__month == 1 and len(str(self.__month)) == 1:
                    self.__text = self.__text.replace("1 months", "1 month")
                if self.__week == 1 and len(str(self.__week)) == 1:
                    self.__text = self.__text.replace("1 weeks", "1 week")
                if self.__day == 1 and len(str(self.__day)) == 1:
                    self.__text = self.__text.replace("1 days", "1 day")
                if self.__year == 0 and len(str(self.__year)) == 1:
                    self.__text = self.__text.replace("0 years, ", "")
                if self.__month == 0 and len(str(self.__month)) == 1:
                    self.__text = self.__text.replace("0 months, ", "")
                if self.__week == 0 and len(str(self.__week)) == 1:
                    self.__text = self.__text.replace("0 weeks, ", "")
                if self.__day == 0 and len(str(self.__day)) == 1:
                    self.__text = self.__text.replace("0 days", "")
                self.__text = self.__text.removesuffix(", ")
            self.update(self.__text)
            self.textDay.delete(0, tk.END)
            if self.__sumDay == 0 or self.__sumDay == 1:
                self.textDay.insert(0, f"{self.__sumDay} day")
            else:
                self.textDay.insert(0, f"{self.__sumDay:,} days")
        else:
            self.display_error()
        self.text["state"] = "disabled"
        self.textDay["state"] = "disabled"

    def update(self, char):
        self.text["state"] = "normal"
        self.textDay["state"] = "normal"
        if char == self.text.get():
            self.text.config(fg="#000000")
            self.after(100, lambda: self.text.config(fg="#FFFFFF"))
        self.text.delete(0, tk.END)
        AnswerField.update(self, char)

    def display_error(self):
        self.text["state"] = "normal"
        self.textDay["state"] = "normal"
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")
        self.textDay.delete(0, tk.END)
        self.textDay.insert(0, "")
        self.text["state"] = "disabled"
        self.textDay["state"] = "disabled"


class CurrencyConverter(tk.Frame, UpdateNumber):
    """Currency converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Currency Converter")
        SelectionButton.summon(self, controller)

        self.__c = CurrencyRates()
        self.__b = BtcConverter()
        self.__value = 0
        self.__fromCurrency = tk.StringVar(value="BTC")
        self.__toCurrency = tk.StringVar(value="USD")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromCurrency, self.__toCurrency, currency)
        NumPad.summon(self)
        NumPad.disable_negative(self)

        self.ratesDetail = tk.Label(self, padx=8, justify="left", font=("Arial", 12), bg="#000000", fg="#FFFFFF")
        self.ratesDetail.grid(row=7, column=1, sticky="w")

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        self.ratesDetail.config(text="")
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        # Check for internet connection
        url = "https://api.coindesk.com/"
        timeout = 5
        try:
            request = requests.get(url, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout):
            answer = tk.messagebox.askretrycancel("Error", "Error occurred: No internet connection\n\n" +
                                                  "Check your connection and try again.")
            self.equal() if answer else self.display_error()
            return 1
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            if self.__fromCurrency.get() == "BTC" or self.__toCurrency.get() == "BTC":
                try:
                    float(self.__value)
                except (DecimalFloatMismatchError, TypeError):
                    self.display_error()
                try:
                    self.__b.convert_btc_to_cur(self.__value, self.__toCurrency.get())
                except RatesNotAvailableError:
                    self.text.delete(0, tk.END)
                    self.text.insert(0, "Rates Not Available")
                    return 1
                if self.__fromCurrency.get() == "BTC":
                    self.ratesDetail.config(text=f"1 BTC = {(self.__b.get_latest_price(self.__toCurrency.get())):,.9f} " +
                                            f"{self.__toCurrency.get()}" +
                                            f"\nUpdated {datetime.today().strftime('%d/%m/%Y %I:%M %p')}")
                    self.__value = self.__b.convert_btc_to_cur(self.__value, self.__toCurrency.get())

                else:
                    self.ratesDetail.config(text=f"1 {self.__fromCurrency.get()} = " +
                                            f"{(self.__b.convert_to_btc(self.__value, self.__fromCurrency.get())):,.12f} BTC" +
                                            f"\nUpdated {datetime.today().strftime('%d/%m/%Y %I:%M %p')}")
                    self.__value = self.__b.convert_to_btc(self.__value, self.__fromCurrency.get())
            else:
                try:
                    self.__c.convert(self.__fromCurrency.get(), self.__toCurrency.get(), self.__value)
                except RatesNotAvailableError:
                    self.text.delete(0, tk.END)
                    self.text.insert(0, "Rates Not Available")
                    return 1
                self.__value = self.__c.convert(self.__fromCurrency.get(), self.__toCurrency.get(), self.__value)
                self.ratesDetail.config(text=f"1 {self.__fromCurrency.get()} = " +
                                        f"{(self.__c.get_rate(self.__fromCurrency.get(), self.__toCurrency.get())):,.7f} " +
                                        f"{self.__toCurrency.get()}\nUpdated {datetime.today().strftime('%d/%m/%Y %I:%M %p')}")
            self.set_text(round(self.__value, 7))

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class VolumeConverter(tk.Frame, UpdateNumber):
    """Volume converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Volume Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Milliliters")
        self.__toUnitVal = tk.StringVar(value="Teaspoons (US)")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(volume.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * volume[self.__fromUnitVal.get()] / volume[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class LengthConverter(tk.Frame, UpdateNumber):
    """Length converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Length Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Centimeters")
        self.__toUnitVal = tk.StringVar(value="Inches")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(length.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * length[self.__fromUnitVal.get()] / length[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class WeightAndMassConverter(tk.Frame, UpdateNumber):
    """Weight and mass converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Weight and Mass Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilograms")
        self.__toUnitVal = tk.StringVar(value="Pounds")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(weightMass.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * weightMass[self.__fromUnitVal.get()] / weightMass[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class TemperatureConverter(tk.Frame, UpdateNumber):
    """Temperature converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Temperature Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Celsius")
        self.__toUnitVal = tk.StringVar(value="Fahrenheit")
        self.__temperatureList = ["Celsius", "Fahrenheit", "Kelvin"]

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, self.__temperatureList)
        NumPad.summon(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            if self.__fromUnitVal.get() != self.__toUnitVal.get():
                if self.__fromUnitVal.get() == "Celsius":
                    if self.__toUnitVal.get() == "Fahrenheit":
                        self.set_text((self.__value * 9 / 5) + 32)
                    else:
                        self.set_text(self.__value + 273.15)
                elif self.__fromUnitVal.get() == "Fahrenheit":
                    if self.__toUnitVal.get() == "Celsius":
                        self.set_text((self.__value - 32) * 5 / 9)
                    else:
                        self.set_text(((self.__value - 32) * 5 / 9) + 273.15)
                elif self.__fromUnitVal.get() == "Kelvin":
                    if self.__toUnitVal.get() == "Celsius":
                        self.set_text(self.__value - 273.15)
                    else:
                        self.set_text((self.__value - 273.15) * (9 / 5) + 32)
            else:
                self.set_text(self.__value)

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class EnergyConverter(tk.Frame, UpdateNumber):
    """Energy converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Energy Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Joules")
        self.__toUnitVal = tk.StringVar(value="Food calories")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(energy.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * energy[self.__fromUnitVal.get()] / energy[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class AreaConverter(tk.Frame, UpdateNumber):
    """Area converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Area Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Square meters")
        self.__toUnitVal = tk.StringVar(value="Square feet")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(area.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * area[self.__fromUnitVal.get()] / area[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class SpeedConverter(tk.Frame, UpdateNumber):
    """Speed converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Speed Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilometers per hour")
        self.__toUnitVal = tk.StringVar(value="Miles per hour")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(speed.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * speed[self.__fromUnitVal.get()] / speed[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class TimeConverter(tk.Frame, UpdateNumber):
    """Time converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Time Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Hours")
        self.__toUnitVal = tk.StringVar(value="Minutes")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(time.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * time[self.__fromUnitVal.get()] / time[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class PowerConverter(tk.Frame, UpdateNumber):
    """Power converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Power Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilowats")
        self.__toUnitVal = tk.StringVar(value="Horsepower (US)")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(power.keys()))
        NumPad.summon(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None:
            self.display_error()
        else:
            self.set_text(self.__value * power[self.__fromUnitVal.get()] / power[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class DataConverter(tk.Frame, UpdateNumber):
    """Data converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Data Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Gigabytes")
        self.__toUnitVal = tk.StringVar(value="Megabytes")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(data.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * data[self.__fromUnitVal.get()] / data[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class PressureConverter(tk.Frame, UpdateNumber):
    """Pressure converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Pressure Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Atmospheres")
        self.__toUnitVal = tk.StringVar(value="Bars")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(pressure.keys()))
        NumPad.summon(self)
        NumPad.disable_negative(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None or self.__value < 0:
            self.display_error()
        else:
            self.set_text(self.__value * pressure[self.__fromUnitVal.get()] / pressure[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


class AngleConverter(tk.Frame, UpdateNumber):
    """Angle converter."""

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "#000000")
        Frame.set_header_text(self, "Angle Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Degrees")
        self.__toUnitVal = tk.StringVar(value="Radians")

        AnswerField.summon(self)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(angle.keys()))
        NumPad.summon(self)

    def update(self, char):
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__value = AnswerField.get_value(self)
        if self.__value is None:
            self.display_error()
        else:
            self.set_text(self.__value * angle[self.__fromUnitVal.get()] / angle[self.__toUnitVal.get()])

    def set_text(self, value):
        AnswerField.set_value(self, value)

    def display_error(self):
        self.text.delete(0, tk.END)
        self.text.insert(0, "Error")


if __name__ == "__main__":
    CalcLab = CalcLab()
    CalcLab.title("CalcLab")
    CalcLab.resizable(width=False, height=False)
    CalcLab.mainloop()
