try:
    import tkinter as tk    # python 3
except ImportError:
    import Tkinter as tk    # python 2

from abc import ABC, abstractmethod
from math import sqrt, pi, sin, cos, tan, sinh, cosh, tanh
from datetime import date
from tkinter import StringVar
from forex_python.converter import CurrencyRates, CurrencyCodes

class CalculatorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (SelectionMenu, Calculator, DateCalculator, CurrencyConverter, VolumeConverter, LengthConverter,
                WeightAndMassConverter, TemperatureConverter, EnergyConverter, AreaConverter, SpeedConverter, TimeConverter,
                PowerConverter, DataConverter, PressureConverter, AngleConverter):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Calculator")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


class FrameConfig(ABC):
    @abstractmethod
    def set_bg_color(self, color):
        self.configure(bg=color)

    @abstractmethod
    def set_header_text(self, text):
        self.header = tk.Label(self, text=text, font=("Arial", 16), bg="black", fg="white").place(x=60, y=8)
    
    @abstractmethod
    def summon_answer_field(self, row, columnSpan):
        self.text = tk.Entry(self, width=21, justify="right", bd=0, bg="black", fg="white", font=("Arial", 32))
        self.text.grid(row=row, columnspan=columnSpan, pady = 8)
        self.text.insert(tk.END, 0)
    
    @abstractmethod
    def summon_num_pad(self):
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.clear).grid(row=3, column=3)
        self.deleteButton = tk.Button(self, width=5, height=2, text="<", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.delete).grid(row=3, column=4)

        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(7)).grid(row=4, column=2)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(8)).grid(row=4, column=3)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(9)).grid(row=4, column=4)

        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(4)).grid(row=5, column=2)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(5)).grid(row=5, column=3)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(6)).grid(row=5, column=4)

        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(1)).grid(row=6, column=2)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(2)).grid(row=6, column=3)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(3)).grid(row=6, column=4)

        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(0)).grid(row=7, column=3)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update("."))
        self.dotButton.grid(row=7, column=4)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="white", bd=0).grid(row=7, column=2)
    
    @abstractmethod
    def summon_option_menu(self, variable1, variable2, list):
        self.fromText = tk.Label(self, text="From", font=("Arial", 16), bg="black", fg="white").grid(row=3, column=1, padx=8, sticky="w")

        self.fromUnit = tk.OptionMenu(self, variable1, *list)
        self.fromUnit.config(width=19, bd=0, bg="#505050", fg="white", font=("Arial", 18))
        self.fromUnit.grid(row=4, column=1, padx=8)

        self.toText = tk.Label(self, text="To", font=("Arial", 16), bg="black", fg="white").grid(row=5, column=1, padx=8, sticky="w")

        self.toUnit = tk.OptionMenu(self, variable2, *list)
        self.toUnit.config(width=19, bd=0, bg="#505050", fg="white", font=("Arial", 18))
        self.toUnit.grid(row=6, column=1, padx=8)
        

class VerticalScrolledFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

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


class SelectionMenu(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        FrameConfig.set_bg_color(self, "black")

        scrollFrame = VerticalScrolledFrame(self)
        scrollFrame.pack()

        pageList = ["Calculator", "DateCalculator", "CurrencyConverter", "VolumeConverter", "LengthConverter",
                "WeightAndMassConverter", "TemperatureConverter", "EnergyConverter", "AreaConverter", "SpeedConverter", "TimeConverter",
                "PowerConverter", "DataConverter", "PressureConverter", "AngleConverter"]
        for index, page in enumerate(pageList):
            spacedText = ""
            for i, letter in enumerate(page):
                if i and letter.isupper():
                    spacedText += " "
                spacedText += letter
            self.button = tk.Button(scrollFrame.interior, width=36, font=("Arial", 18), text=f"  {spacedText}", anchor="w", bg="#1C1C1C", fg="white", bd=1, 
                                    command=lambda index=index: open_page(pageList[index])).pack()

        def open_page(page):
            controller.show_frame(page)
            

class Calculator(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Calculator")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.memory = None
        self.lockSecInput = False
        self.operator = ""

        FrameConfig.summon_answer_field(self, 2, 8)

        self.factorialButton = tk.Button(self, width=5, height=2, text="x!", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=3, column=1)
        self.sqrtButton = tk.Button(self, width=5, height=2, text="√x", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=3, column=2)
        self.squareButton = tk.Button(self, width=5, height=2, text="x²", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=3, column=3)
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.clear).grid(row=3, column=4)
        self.percentButton = tk.Button(self, width=5, height=2, text="%", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.percent).grid(row=3, column=5)
        self.deleteButton = tk.Button(self, width=5, height=2, text="<", font=("Arial", 18), bg="#D4D4D2", bd=0, command=self.delete).grid(row=3, column=6)
        self.plusButton = tk.Button(self, width=5, height=2, text="+", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.add).grid(row=3, column=7)

        self.lnButton = tk.Button(self, width=5, height=2, text="ln", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=4, column=1)
        self.cbrtButton = tk.Button(self, width=5, height=2, text="∛x", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=4, column=2)
        self.cubeButton = tk.Button(self, width=5, height=2, text="x³", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=4, column=3)
        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(7)).grid(row=4, column=4)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(8)).grid(row=4, column=5)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(9)).grid(row=4, column=6)
        self.minusButton = tk.Button(self, width=5, height=2, text="-", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.minus).grid(row=4, column=7)

        self.commonLog = tk.Button(self, width=5, height=2, text="log", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=5, column=1)
        self.sinhButton = tk.Button(self, width=5, height=2, text="sinh", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=5, column=2)
        self.sinButton = tk.Button(self, width=5, height=2, text="sin", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=5, column=3)
        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(4)).grid(row=5, column=4)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(5)).grid(row=5, column=5)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(6)).grid(row=5, column=6)
        self.multiplyButton = tk.Button(self, width=5, height=2, text="x", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.multiply).grid(row=5, column=7)

        self.eButton = tk.Button(self, width=5, height=2, text="e", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=6, column=1)
        self.coshButton = tk.Button(self, width=5, height=2, text="cosh", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=6, column=2)
        self.cosButton = tk.Button(self, width=5, height=2, text="cos", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=6, column=3)
        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(1)).grid(row=6, column=4)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(2)).grid(row=6, column=5)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(3)).grid(row=6, column=6)
        self.divideButton = tk.Button(self, width=5, height=2, text="÷", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.divide).grid(row=6, column=7)

        self.piButton = tk.Button(self, width=5, height=2, text="π", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=7, column=1)
        self.tanhButton = tk.Button(self, width=5, height=2, text="tanh", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=7, column=2)
        self.tanButton = tk.Button(self, width=5, height=2, text="tan", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0).grid(row=7, column=3)
        self.negativeButton = tk.Button(self, width=5, height=2, text="+/-", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=self.negative).grid(row=7, column=4)
        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update(0)).grid(row=7, column=5)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="white", bd=0, command=lambda: self.update("."))
        self.dotButton.grid(row=7, column=6)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="white", bd=0, command=self.equal).grid(row=7, column=7)

    def update(self, char):
        self.text.config(fg="white")
        if self.lockSecInput == True:
            self.dotButton["state"] = "normal"
            self.text.delete(0, tk.END)
            self.text.insert(tk.END, 0)
            self.lockSecInput = False
        if len(self.text.get()) < 15: # limit to 15 characters
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
            
    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"

    def negative(self):
        self.text.config(fg="white")
        self.text.insert(0, "-") if float(self.text.get()) >= 0 else self.text.delete(0, 1)
        
    def add(self):
        self.memory = self.text.get()
        self.lockSecInput = True
        self.operator = "+"
    
    def minus(self):
        self.memory = self.text.get()
        self.lockSecInput = True
        self.operator = "-"

    def multiply(self):
        self.memory = self.text.get()
        self.lockSecInput = True
        self.operator = "*"
    
    def divide(self):
        self.memory = self.text.get()
        self.lockSecInput = True
        self.operator = "/"

    def percent(self):
        val = float(self.text.get())
        self.text.delete(0, tk.END)
        self.text.insert(0, val / 100)
    
    def equal(self):
        try:
            float(self.memory)
            float(self.text.get())
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        if self.memory != None:
            if self.operator == "+":
                result = float(self.memory) + float(self.text.get())
            elif self.operator == "-":
                result = float(self.memory) - float(self.text.get())
            elif self.operator == "*":
                result = float(self.memory) * float(self.text.get())
            elif self.operator == "/":
                try:
                    float(self.memory) / float(self.text.get())
                except ZeroDivisionError:
                    self.text.delete(0, tk.END)
                    self.text.insert(0, "Error")
                result = float(self.memory) / float(self.text.get())
            if result % 1 == 0:
                result = int(result)
            self.lockSecInput = True
            if result == float(self.text.get()):
                self.text.config(fg="black")
                self.after(100, lambda: self.text.config(fg="white"))
            self.text.delete(0, tk.END)
            self.text.insert(0, round(result, 12))


class DateCalculator(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Date Calculator")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, sticky="w")

        # FrameConfig.summon_answer_field(self, 2, 2)
        self.text = tk.Entry(self, width=21, justify="right", bd=0, bg="black", fg="white", font=("Arial", 32))
        self.text.grid(row=2, padx=8, pady = 8, sticky="w")
        self.text.insert(tk.END, "Same dates")

        self.fromText = tk.Label(self, text="From (format: 02/12/2021)", font=("Arial", 16), bg="black", fg="white").grid(row=4, padx=8, sticky="w")

        self.fromDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="white", font=("Arial", 22))
        self.fromDate.grid(row=5, padx=8, pady = 8, sticky="w")
        self.fromDate.insert(tk.END, date.today().strftime("%d/%m/%Y"))

        self.fromText = tk.Label(self, text="To (format: 02/12/2021)", font=("Arial", 16), bg="black", fg="white").grid(row=6, padx=8, sticky="w")

        self.toDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="white", font=("Arial", 22))
        self.toDate.grid(row=7, padx=8, pady = 8, sticky="w")
        self.toDate.insert(tk.END, date.today().strftime("%d/%m/%Y"))

        self.calcButton = tk.Button(self, height=2, text="Calculate", font=("Arial", 18), bg="#FF9500", fg="white", bd=0).grid(row=9, padx=8, sticky="w")


class CurrencyConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Currency Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromCurrencyVal = StringVar(value="Select a currency")
        self.toCurrencyVal = StringVar(value="Select a currency")
        currencyList = ["USD", "JPY", "EUR", "THB", "IDR", "BGN", "ILS", "GBP", "AUD", "CHF", "HKD"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromCurrencyVal, self.toCurrencyVal, currencyList)
        FrameConfig.summon_num_pad(self)


    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class VolumeConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Volume Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        volumeList = ["Milliliters", "Liters", "Cubic meters", "Teaspoons (US)", "Tablespoons (US)", "Fluid ounces (US)", "Cups (US)", "Pints (US)",
                        "Quarts (US)", "Gallons (US)", "Cubic inches", "Cubic feet", "Cubic yards", "Teaspoons (UK)", "Tablespoons (UK)", 
                        "Fluid ounces (UK)", "Cups (UK)", "Pints (UK)", "Quarts (UK)", "Gallons (UK)"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, volumeList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class LengthConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Length Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        lengthList = ["Nanometers", "Microns", "Millimeters", "Centimeters", "Meters", "Kilometers", "Inches", "Feet", "Yards", "Miles", "Nautical Miles"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, lengthList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class WeightAndMassConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Weight and Mass Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        weightMassList = ["Carats", "Milligrams", "Centigrams", "Decigrams", "Grams", "Dekagrams", "Hectogram", "Kilograms", "Metric tonnes", "Ounces",
                        "Pounds", "Stone", "Short tons (US)", "Long tons (US)"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, weightMassList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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
    
    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class TemperatureConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Temperature Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        temperatureList = ["Celsius", "Fahrenheit", "Kelvin"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, temperatureList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class EnergyConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Energy Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        energyList = ["Electron volts", "Joules", "Kilojoules", "Thermal calories", "Food calories", "Foot-pounds", "British thermal units"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, energyList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class AreaConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Area Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        areaList = ["Square millimeters", "Square centimeters", "Square meters", "Hectares", "Square kilometers", "Square inches", "Square feet",
                    "Square yards", "Acres", "Square miles"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, areaList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class SpeedConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Speed Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        speedList = ["Centimeters per second", "Meters per second", "Kilometers per hour", "Feet per second", "Miles per hour", "Knots", "Mach"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, speedList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class TimeConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Time Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        volumeList = ["Milliliters", "Liters", "Cubic meters", "Teaspoons (US)", "Tablespoons (US)", "Fluid ounces (US)", "Cups (US)", "Pints (US)",
                        "Quarts (US)", "Gallons (US)", "Cubic inches", "Cubic feet", "Cubic yards", "Teaspoons (UK)", "Tablespoons (UK)", 
                        "Fluid ounces (UK)", "Cups (UK)", "Pints (UK)", "Quarts (UK)", "Gallons (UK)"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, volumeList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class PowerConverter(tk.Frame, ABC):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Power Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        volumeList = ["Milliliters", "Liters", "Cubic meters", "Teaspoons (US)", "Tablespoons (US)", "Fluid ounces (US)", "Cups (US)", "Pints (US)",
                        "Quarts (US)", "Gallons (US)", "Cubic inches", "Cubic feet", "Cubic yards", "Teaspoons (UK)", "Tablespoons (UK)", 
                        "Fluid ounces (UK)", "Cups (UK)", "Pints (UK)", "Quarts (UK)", "Gallons (UK)"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, volumeList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class DataConverter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Data Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        volumeList = ["Milliliters", "Liters", "Cubic meters", "Teaspoons (US)", "Tablespoons (US)", "Fluid ounces (US)", "Cups (US)", "Pints (US)",
                        "Quarts (US)", "Gallons (US)", "Cubic inches", "Cubic feet", "Cubic yards", "Teaspoons (UK)", "Tablespoons (UK)", 
                        "Fluid ounces (UK)", "Cups (UK)", "Pints (UK)", "Quarts (UK)", "Gallons (UK)"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, volumeList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class PressureConverter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Pressure Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        volumeList = ["Milliliters", "Liters", "Cubic meters", "Teaspoons (US)", "Tablespoons (US)", "Fluid ounces (US)", "Cups (US)", "Pints (US)",
                        "Quarts (US)", "Gallons (US)", "Cubic inches", "Cubic feet", "Cubic yards", "Teaspoons (UK)", "Tablespoons (UK)", 
                        "Fluid ounces (UK)", "Cups (UK)", "Pints (UK)", "Quarts (UK)", "Gallons (UK)"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, volumeList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


class AngleConverter(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        
        FrameConfig.set_bg_color(self, "black")
        FrameConfig.set_header_text(self, "Angle Converter")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3, 
                                    command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1, sticky="w")

        self.total = 0
        self.fromUnitVal = StringVar(value="Select a unit")
        self.toUnitVal = StringVar(value="Select a unit")
        volumeList = ["Milliliters", "Liters", "Cubic meters", "Teaspoons (US)", "Tablespoons (US)", "Fluid ounces (US)", "Cups (US)", "Pints (US)",
                        "Quarts (US)", "Gallons (US)", "Cubic inches", "Cubic feet", "Cubic yards", "Teaspoons (UK)", "Tablespoons (UK)", 
                        "Fluid ounces (UK)", "Cups (UK)", "Pints (UK)", "Quarts (UK)", "Gallons (UK)"]

        FrameConfig.summon_answer_field(self, 2, 5)
        FrameConfig.summon_option_menu(self, self.fromUnitVal, self.toUnitVal, volumeList)
        FrameConfig.summon_num_pad(self)
    
    def update(self, char):
        self.text.config(fg="white")
        if len(self.text.get()) < 15: # limit to 15 characters
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

    def clear(self):
        self.text.config(fg="white")
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.config(fg="white")
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"


if __name__ == "__main__":
    app = CalculatorApp()
    app.title("CalculatorX")
    app.resizable(width=False, height=False)
    app.mainloop()