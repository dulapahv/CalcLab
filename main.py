#===============================================================#
#  Python Individual Project, Year 1, Semester 1                #
#                                                               #
#  Course: 13006107 Introduction to Computers and Programming   #
#  Program: Software Engineering Program                        #
#  University: Faculty of Engineering, KMITL                    #
#                                                               #
#  Project: Calculatory                                         #
#  Repository: https://github.com/DulapahV/Calculatory          #
#  Written by: Dulapah Vibulsanti (64011388)                    #
#===============================================================#

# * Please install this package *
# pip install forex-python

try:
    import tkinter as tk  # python 3
except ImportError:
    import Tkinter as tk  # python 2
from abc import ABC, abstractmethod
from math import pi, e, sqrt, log, log10, factorial, radians, sin, cos, tan, sinh, cosh, tanh
from numpy import cbrt
from datetime import datetime
from forex_python.converter import CurrencyRates, RatesNotAvailableError
from forex_python.bitcoin import BtcConverter


class CalculatorApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for frame in (SelectionMenu, Calculator, DateCalculator, CurrencyConverter, VolumeConverter, LengthConverter,
                      WeightAndMassConverter, TemperatureConverter, EnergyConverter, AreaConverter, SpeedConverter,
                      TimeConverter, PowerConverter, DataConverter, PressureConverter, AngleConverter):
            page_name = frame.__name__
            frame = frame(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("Calculator")

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()


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
        pass


class AnswerField:
    def summon_answer_field(self, row, columnSpan):
        self.text = tk.Entry(self, width=21, justify="right", bd=0, bg="black", fg="white", font=("Arial", 32))
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

    def set_value(self, pastValue, value):
        if value % 1 == 0:
            value = int(value)
        if value == float(pastValue.replace(',', '')):
            self.text.config(fg="black")
            self.after(100, lambda: self.text.config(fg="white"))
        self.text.delete(0, tk.END)
        if len(str(int(value))) <= 18 and len(self.text.get()) <= 18:
            self.text.insert(0,
                             f"{round(value, 18 - len(str(int(value)))):,}")  # round(value, 18 - len(str(int(value))))
        else:
            self.text.insert(0, f"{round(value, 12):e}")

    def negative(self):
        if self.text.get().replace(',', '') == "0" or float(self.text.get().replace(',', '')) > 0:
            self.text.insert(0, "-")
        else:
            self.text.delete(0, 1)

    def clear(self):
        self.dotButton["state"] = "normal"
        self.memory = None
        self.text.delete(0, tk.END)
        self.text.insert(tk.END, 0)

    def delete(self):
        self.text.delete(len(self.text.get()) - 1, tk.END) if len(self.text.get()) != 1 else self.clear()
        if "." not in self.text.get():
            self.dotButton["state"] = "normal"

    def get_value(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__value = float(self.text.get().replace(',', ''))
        if self.__value % 1 == 0:
            self.__value = int(self.__value)
        return self.__value


class NumPad(AnswerField):
    def summon(self):
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                     command=self.clear).grid(row=3, column=2)
        self.negativeButton = tk.Button(self, width=5, height=2, text="+/-", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                        command=self.negative)
        self.negativeButton.grid(row=3, column=3)
        self.deleteButton = tk.Button(self, width=5, height=2, text="<", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                      command=self.delete).grid(row=3, column=4)

        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="white",
                                     bd=0, command=lambda: self.update(7)).grid(row=4, column=2)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="white",
                                     bd=0, command=lambda: self.update(8)).grid(row=4, column=3)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(9)).grid(row=4, column=4)

        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(4)).grid(row=5, column=2)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(5)).grid(row=5, column=3)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update(6)).grid(row=5, column=4)

        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update(1)).grid(row=6, column=2)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update(2)).grid(row=6, column=3)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="white",
                                     bd=0, command=lambda: self.update(3)).grid(row=6, column=4)

        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(0)).grid(row=7, column=3)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update("."))
        self.dotButton.grid(row=7, column=4)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="white",
                                     bd=0, command=self.equal).grid(row=7, column=2)

    def disable_negative(self):
        self.negativeButton.config(state="disabled")


class Frame:
    def set_bg_color(self, color):
        self.configure(bg=color)

    def set_header_text(self, text):
        self.header = tk.Label(self, text=text, font=("Arial", 16), bg="black", fg="white").place(x=60, y=8)


class SelectionButton:
    def summon(self, controller):
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3,
                                      command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1,
                                                                                                   sticky="w")


class OptionMenu:
    def summon(self, variable1, variable2, list):
        self.fromText = tk.Label(self, text="From", font=("Arial", 16), bg="black", fg="white").grid(row=3, column=1,
                                 padx=8, sticky="w")

        self.fromUnit = tk.OptionMenu(self, variable1, *list)
        self.fromUnit.config(width=19, bd=0, bg="#505050", fg="white", font=("Arial", 18), anchor="w")
        self.fromUnit.grid(row=4, column=1, padx=8)

        self.toText = tk.Label(self, text="To", font=("Arial", 16), bg="black", fg="white").grid(row=5, column=1,
                               padx=8, sticky="w")

        self.toUnit = tk.OptionMenu(self, variable2, *list)
        self.toUnit.config(width=19, bd=0, bg="#505050", fg="white", font=("Arial", 18), anchor="w")
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


class SelectionMenu(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")

        scrollFrame = VerticalScrolledFrame(self)
        scrollFrame.pack()

        pageList = ["Calculator", "DateCalculator", "CurrencyConverter", "VolumeConverter", "LengthConverter",
                    "WeightAndMassConverter", "TemperatureConverter", "EnergyConverter", "AreaConverter",
                    "SpeedConverter", "TimeConverter", "PowerConverter", "DataConverter", "PressureConverter", 
                    "AngleConverter"]
        for index, page in enumerate(pageList):
            spacedText = ""
            for i, letter in enumerate(page):
                if i and letter.isupper():
                    spacedText += " "
                spacedText += letter
            self.button = tk.Button(scrollFrame.interior, width=36, font=("Arial", 18), text=f"  {spacedText}",
                                    anchor="w", bg="#1C1C1C", fg="white", bd=1,
                                    command=lambda index=index: open_page(pageList[index])).pack()

        def open_page(page):
            controller.show_frame(page)  

class Calculator(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Calculator")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3,
                                      command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, column=1,
                                                                                                   sticky="w")

        self.__value = 0
        self.__memory = 0
        self.__reVal = 0
        self.__lockSecInput = False
        self.__operator = None

        AnswerField.summon_answer_field(self, 2, 8)

        self.factorialButton = tk.Button(self, width=5, height=2, text="x!", font=("Arial", 18), bg="#1C1C1C",
                                         fg="white", bd=0, command=self.factorial).grid(row=3, column=1)
        self.sqrtButton = tk.Button(self, width=5, height=2, text="√x", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                    bd=0, command=self.sqrt).grid(row=3, column=2)
        self.squareButton = tk.Button(self, width=5, height=2, text="x²", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                      bd=0, command=self.square).grid(row=3, column=3)
        self.clearButton = tk.Button(self, width=5, height=2, text="AC", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                     command=self.clear).grid(row=3, column=4)
        self.percentButton = tk.Button(self, width=5, height=2, text="%", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                       command=self.percent).grid(row=3, column=5)
        self.deleteButton = tk.Button(self, width=5, height=2, text="<", font=("Arial", 18), bg="#D4D4D2", bd=0,
                                      command=self.delete).grid(row=3, column=6)
        self.plusButton = tk.Button(self, width=5, height=2, text="+", font=("Arial", 18), bg="#FF9500", fg="white",
                                    bd=0, command=self.add).grid(row=3, column=7)

        self.lnButton = tk.Button(self, width=5, height=2, text="ln", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                  bd=0, command=self.ln).grid(row=4, column=1)
        self.cbrtButton = tk.Button(self, width=5, height=2, text="∛x", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                    bd=0, command=self.cbrt).grid(row=4, column=2)
        self.cubeButton = tk.Button(self, width=5, height=2, text="x³", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                    bd=0, command=self.cube).grid(row=4, column=3)
        self.sevenButton = tk.Button(self, width=5, height=2, text="7", font=("Arial", 18), bg="#505050", fg="white",
                                     bd=0, command=lambda: self.update(7)).grid(row=4, column=4)
        self.eightButton = tk.Button(self, width=5, height=2, text="8", font=("Arial", 18), bg="#505050", fg="white",
                                     bd=0, command=lambda: self.update(8)).grid(row=4, column=5)
        self.nineButton = tk.Button(self, width=5, height=2, text="9", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(9)).grid(row=4, column=6)
        self.minusButton = tk.Button(self, width=5, height=2, text="-", font=("Arial", 18), bg="#FF9500", fg="white",
                                     bd=0, command=self.minus).grid(row=4, column=7)

        self.commonLog = tk.Button(self, width=5, height=2, text="log", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                   bd=0, command=self.log10).grid(row=5, column=1)
        self.sinhButton = tk.Button(self, width=5, height=2, text="sinh", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                    bd=0, command=self.sinh).grid(row=5, column=2)
        self.sinButton = tk.Button(self, width=5, height=2, text="sin", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                   bd=0, command=self.sin).grid(row=5, column=3)
        self.fourButton = tk.Button(self, width=5, height=2, text="4", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(4)).grid(row=5, column=4)
        self.fiveButton = tk.Button(self, width=5, height=2, text="5", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(5)).grid(row=5, column=5)
        self.sixButton = tk.Button(self, width=5, height=2, text="6", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update(6)).grid(row=5, column=6)
        self.multiplyButton = tk.Button(self, width=5, height=2, text="x", font=("Arial", 18), bg="#FF9500", fg="white",
                                        bd=0, command=self.multiply).grid(row=5, column=7)

        self.eButton = tk.Button(self, width=5, height=2, text="e", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0,
                                 command=self.eVal).grid(row=6, column=1)
        self.coshButton = tk.Button(self, width=5, height=2, text="cosh", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                    bd=0, command=self.cosh).grid(row=6, column=2)
        self.cosButton = tk.Button(self, width=5, height=2, text="cos", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                   bd=0, command=self.cos).grid(row=6, column=3)
        self.oneButton = tk.Button(self, width=5, height=2, text="1", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update(1)).grid(row=6, column=4)
        self.twoButton = tk.Button(self, width=5, height=2, text="2", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update(2)).grid(row=6, column=5)
        self.threeButton = tk.Button(self, width=5, height=2, text="3", font=("Arial", 18), bg="#505050", fg="white",
                                     bd=0, command=lambda: self.update(3)).grid(row=6, column=6)
        self.divideButton = tk.Button(self, width=5, height=2, text="÷", font=("Arial", 18), bg="#FF9500", fg="white",
                                      bd=0, command=self.divide).grid(row=6, column=7)

        self.piButton = tk.Button(self, width=5, height=2, text="π", font=("Arial", 18), bg="#1C1C1C", fg="white", bd=0,
                                  command=self.piVal).grid(row=7, column=1)
        self.tanhButton = tk.Button(self, width=5, height=2, text="tanh", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                    bd=0, command=self.tanh).grid(row=7, column=2)
        self.tanButton = tk.Button(self, width=5, height=2, text="tan", font=("Arial", 18), bg="#1C1C1C", fg="white",
                                   bd=0, command=self.tan).grid(row=7, column=3)
        self.negativeButton = tk.Button(self, width=5, height=2, text="+/-", font=("Arial", 18), bg="#505050",
                                        fg="white", bd=0, command=self.negative).grid(row=7, column=4)
        self.zeroButton = tk.Button(self, width=5, height=2, text="0", font=("Arial", 18), bg="#505050", fg="white",
                                    bd=0, command=lambda: self.update(0)).grid(row=7, column=5)
        self.dotButton = tk.Button(self, width=5, height=2, text=".", font=("Arial", 18), bg="#505050", fg="white",
                                   bd=0, command=lambda: self.update("."))
        self.dotButton.grid(row=7, column=6)
        self.equalButton = tk.Button(self, width=5, height=2, text="=", font=("Arial", 18), bg="#FF9500", fg="white",
                                     bd=0, command=self.equal).grid(row=7, column=7)

    def update(self, char):
        if self.__lockSecInput == True:
            self.dotButton["state"] = "normal"
            self.text.delete(0, tk.END)
            self.text.insert(tk.END, 0)
            self.__lockSecInput = False
        AnswerField.update(self, char)

    def negative(self):
        AnswerField.negative(self)

    def clear(self):
        self.__reVal = None
        self.__operator = None
        AnswerField.clear(self)

    def delete(self):
        AnswerField.delete(self)

    def equal(self):
        self.__displayedText = self.text.get().replace(',', '')
        try:
            float(self.__memory)
            float(self.__displayedText)
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        if self.__operator != None:
            if self.__operator == "+":
                if self.__reVal == 0:
                    self.__value = float(self.__memory) + float(self.__displayedText)
                    self.__reVal = float(self.__displayedText)
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
                    self.text.delete(0, tk.END)
                    self.text.insert(0, "Error")
                if self.__reVal == 0:
                    self.__value = float(self.__memory) / float(self.__displayedText)
                    self.__reVal = float(self.__displayedText)
                else:
                    self.__value /= self.__reVal
            self.__lockSecInput = True
            self.set_text(self.__displayedText, self.__value)

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)

    def add(self):
        self.__memory = self.text.get().replace(',', '')
        self.__reVal = 0
        self.__lockSecInput = True
        self.__operator = "+"

    def minus(self):
        self.__memory = self.text.get().replace(',', '')
        self.__reVal = 0
        self.__lockSecInput = True
        self.__operator = "-"

    def multiply(self):
        self.__memory = self.text.get().replace(',', '')
        self.__reVal = 0
        self.__lockSecInput = True
        self.__operator = "*"

    def divide(self):
        self.__memory = self.text.get().replace(',', '')
        self.__reVal = 0
        self.__lockSecInput = True
        self.__operator = "/"

    def percent(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.set_text(0, float(self.text.get().replace(',', '')) / 100)

    def square(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, float(self.text.get().replace(',', '')) ** 2)

    def cube(self):
        try:
            float(self.text.get().replace(',', ''))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, float(self.text.get().replace(',', '')) ** 3)

    def sqrt(self):
        try:
            sqrt(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, sqrt(float(self.text.get().replace(',', ''))))

    def cbrt(self):
        try:
            cbrt(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, cbrt(float(self.text.get().replace(',', ''))))

    def sin(self):
        try:
            sin(radians(float(self.text.get().replace(',', ''))))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, sin(radians(float(self.text.get().replace(',', '')))))

    def cos(self):
        try:
            cos(radians(float(self.text.get().replace(',', ''))))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, cos(radians(float(self.text.get().replace(',', '')))))

    def tan(self):
        try:
            tan(radians(float(self.text.get().replace(',', ''))))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, tan(radians(float(self.text.get().replace(',', '')))))

    def sinh(self):
        try:
            sinh(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, sinh(float(self.text.get().replace(',', ''))))

    def cosh(self):
        try:
            cosh(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, cosh(float(self.text.get().replace(',', ''))))

    def tanh(self):
        try:
            tanh(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, tanh(float(self.text.get().replace(',', ''))))

    def ln(self):
        try:
            log(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, log(float(self.text.get().replace(',', ''))))

    def log10(self):
        try:
            log10(float(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, log10(float(self.text.get().replace(',', ''))))

    def factorial(self):
        try:
            factorial(int(self.text.get().replace(',', '')))
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        self.__memory = self.text.get().replace(',', '')
        self.set_text(self.__memory, factorial(int(self.text.get().replace(',', ''))))

    def eVal(self):
        self.set_text(self.__memory, e)

    def piVal(self):
        self.set_text(self.__memory, pi)


class DateCalculator(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        self.__day = 0
        self.__week = 0
        self.__month = 0
        self.__year = 0
        self.__text = ""
        
        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Date Calculator")
        self.switchButton = tk.Button(self, text="≡", bg="#1C1C1C", fg="white", bd=0, font=("Arial", 18), width=3,
                                      command=lambda: controller.show_frame("SelectionMenu")).grid(row=1, sticky="w")

        self.text = tk.Entry(self, width=28, justify="right", bd=0, bg="black", fg="white", font=("Arial", 24))
        self.text.grid(row=2, padx=8, pady=8, sticky="w")
        self.text.insert(tk.END, "Same dates")

        self.grid_rowconfigure(4, minsize=10)
        self.fromText = tk.Label(self, text="From (format: 02/12/2021)", font=("Arial", 16), bg="black",
                                 fg="white").grid(row=5, padx=8, sticky="w")

        self.fromDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="white", font=("Arial", 22))
        self.fromDate.grid(row=6, padx=8, pady=8, sticky="w")
        self.fromDate.insert(tk.END, datetime.today().strftime("%d/%m/%Y"))

        self.fromText = tk.Label(self, text="To (format: 02/12/2021)", font=("Arial", 16), bg="black", fg="white").grid(
            row=7, padx=8, sticky="w")

        self.toDate = tk.Entry(self, width=21, justify="left", bd=0, bg="#505050", fg="white", font=("Arial", 22))
        self.toDate.grid(row=8, padx=8, pady=8, sticky="w")
        self.toDate.insert(tk.END, datetime.today().strftime("%d/%m/%Y"))

        self.grid_rowconfigure(9, minsize=20)
        self.calcButton = tk.Button(self, height=2, text="Calculate", font=("Arial", 18), bg="#FF9500", fg="white",
                                    bd=0, command=self.equal).grid(row=10, padx=8, sticky="w")

    def equal(self):
        try:
            self.__fromDay, self.__fromMonth, self.__fromYear = self.fromDate.get().split("/")
            self.__toDay, self.__toMonth, self.__toYear = self.toDate.get().split("/")
        except ValueError:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
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
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")
        if (1 <= self.__fromDay <= 31 and 1 <= self.__toDay <= 31 and 1 <= self.__fromMonth <= 12 and 
        1 <= self.__toMonth <= 12 and self.__fromYear >= 1 and self.__toYear >= 1):
            self.__day = abs(self.__fromDay - self.__toDay) + (abs(self.__fromMonth - self.__toMonth) * 30) + (abs(
                            self.__fromYear - self.__toYear) * 365)
            self.__year = self.__day // 365
            self.__month = (self.__day - self.__year*365) // 30
            self.__week = (self.__day - self.__year*365 - self.__month*30) // 7
            self.__day = (self.__day - self.__year*365 - self.__month*30 - self.__week*7)
            if self.__year == 0 and self.__month == 0 and self.__week == 0 and self.__day == 0:
                self.__text = "Same dates"
            else:
                self.__text = f"{self.__year} years, {self.__month} months, {self.__week} weeks, {self.__day} days"
                if self.__year != 11:
                    self.__text = self.__text.replace("1 years", "1 year")
                if self.__month != 11:
                    self.__text = self.__text.replace("1 months", "1 month")
                if self.__week != 11:
                    self.__text = self.__text.replace("1 weeks", "1 week")
                if self.__day != 11:
                    self.__text = self.__text.replace("1 days", "1 day")
                self.__text = self.__text.replace("0 years, ", "")
                self.__text = self.__text.replace("0 months, ", "")
                self.__text = self.__text.replace("0 weeks, ", "")
                self.__text = self.__text.replace("0 days", "")
                self.__text = self.__text.removesuffix(", ")
            self.update(self.__text)
        else:
            self.text.delete(0, tk.END)
            self.text.insert(0, "Error")

    def update(self, char):
        if char == self.text.get():
            self.text.config(fg="black")
            self.after(100, lambda: self.text.config(fg="white"))
        self.text.delete(0, tk.END)
        AnswerField.update(self, char)

class CurrencyConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Currency Converter")
        SelectionButton.summon(self, controller)

        self.__c = CurrencyRates()
        self.__b = BtcConverter()
        self.__value = 0
        self.__fromCurrency = tk.StringVar(value="BTC")
        self.__toCurrency = tk.StringVar(value="USD")
        self.__currencyList = ["BTC", "USD", "JPY", "EUR", "THB", "IDR", "BGN", "ILS", "GBP", "AUD", "CHF", "HKD"]

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromCurrency, self.__toCurrency, self.__currencyList)
        NumPad.summon(self)
        NumPad.disable_negative(self)

        self.ratesDetail = tk.Label(self, padx=8, justify="left", font=("Arial", 12), bg="black", fg="white")
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
        self.__value = AnswerField.get_value(self)
        if self.__fromCurrency.get() == "BTC" or self.__toCurrency.get() == "BTC":
            try:
                self.__value = self.__b.convert_btc_to_cur(self.__value, self.__toCurrency.get())
            except RatesNotAvailableError:
                self.text.delete(0, tk.END)
                self.text.insert(0, "Rates Not Available")
                return 1
            if self.__fromCurrency.get() == "BTC":
                self.ratesDetail.config(text=f"1 BTC = {(self.__b.get_latest_price(self.__toCurrency.get())):.9f}" + 
                                        f" {self.__toCurrency.get()}" + 
                                        f"\nUpdated {datetime.today().strftime('%d/%m/%Y %I:%M %p')}")
                self.__value = self.__b.convert_btc_to_cur(self.__value, self.__toCurrency.get())
                
            else:
                self.ratesDetail.config(text=f"1 {self.__toCurrency.get()} = " + 
                                        f"{(self.__b.convert_to_btc(self.__value, self.__fromCurrency.get())):.12f} BTC" + 
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
                                    f"{(self.__c.get_rate(self.__fromCurrency.get(), self.__toCurrency.get())):.7f}" + 
                                    f" {self.__toCurrency.get()}\nUpdated {datetime.today().strftime('%d/%m/%Y %I:%M %p')}")
        self.set_text(self.text.get(), round(self.__value, 2))

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class VolumeConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Volume Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Milliliters")
        self.__toUnitVal = tk.StringVar(value="Teaspoons (US)")
        self.__volume = {"Milliliters": 0.001, "Cubic centimeters": 0.001, "Liters": 1, "Cubic meters": 1000,
                         "Teaspoons (US)": 0.004929, "Tablespoons (US)": 0.014787, "Fluid ounces (US)": 0.029574, 
                         "Cups (US)": 0.236588, "Pints (US)": 0.473176, "Quarts (US)": 0.946353, "Gallons (US)": 3.785412, 
                         "Cubic inches": 0.016387, "Cubic feet": 28.31685, "Cubic yards": 764.5549, 
                         "Teaspoons (UK)": 0.005919, "Tablespoons (UK)": 0.017758, "Fluid ounces (UK)": 0.028413, 
                         "Pints (UK)": 0.568261, "Quarts (UK)": 1.136523, "Gallons (UK)": 4.54609}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__volume.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__volume[self.__fromUnitVal.get()] / self.__volume[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class LengthConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Length Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Centimeters")
        self.__toUnitVal = tk.StringVar(value="Inches")
        self.__length = {"Nanometers": 0.000000001, "Microns": 0.000001, "Millimeters": 0.001, "Centimeters": 0.01,
                         "Meters": 1, "Kilometers": 1000, "Inches": 0.0254, "Feet": 0.3048, "Yards": 0.9144, 
                         "Miles": 1609.344, "Nautical Miles": 1852}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__length.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__length[self.__fromUnitVal.get()] / self.__length[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class WeightAndMassConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Weight and Mass Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilograms")
        self.__toUnitVal = tk.StringVar(value="Pounds")
        self.__weightMass = {"Carats": 0.0002, "Milligrams": 0.000001, "Centigrams": 0.00001, "Decigrams": 0.0001,
                             "Grams": 0.001, "Dekagrams": 0.01, "Hectogram": 0.1, "Kilograms": 1, "Metric tonnes": 1000,
                             "Ounces": 0.02835, "Pounds": 0.453592, "Stone": 6.350293, "Short tons (US)": 907.1847, 
                             "Long tons (US)": 1016.047}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__weightMass.keys()))
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
        self.set_text(self.__value, self.__value * self.__weightMass[self.__fromUnitVal.get()] / self.__weightMass[
            self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class TemperatureConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Temperature Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Celsius")
        self.__toUnitVal = tk.StringVar(value="Fahrenheit")
        self.__temperatureList = ["Celsius", "Fahrenheit", "Kelvin"]

        AnswerField.summon_answer_field(self, 2, 5)
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
        if self.__fromUnitVal.get() != self.__toUnitVal.get():
            if self.__fromUnitVal.get() == "Celsius":
                if self.__toUnitVal.get() == "Fahrenheit":
                    AnswerField.set_value(self, self.__value, (self.__value * 9 / 5) + 32)
                else:
                    AnswerField.set_value(self, self.__value, self.__value + 273.15)
            elif self.__fromUnitVal.get() == "Fahrenheit":
                if self.__toUnitVal.get() == "Celsius":
                    AnswerField.set_value(self, self.__value, (self.__value - 32) * 5 / 9)
                else:
                    AnswerField.set_value(self, self.__value, ((self.__value - 32) * 5 / 9) + 273.15)
            elif self.__fromUnitVal.get() == "Kelvin":
                if self.__toUnitVal.get() == "Celsius":
                    AnswerField.set_value(self, self.__value, self.__value - 273.15)
                else:
                    AnswerField.set_value(self, self.__value, ((self.__value - 273.15) * (9 / 5) + 32))
        else:
            self.set_text(self.__value, self.__value)

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class EnergyConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Energy Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Joules")
        self.__toUnitVal = tk.StringVar(value="Food calories")
        self.__energy = {"Electron volts": 1.602177 * (10 ** -19), "Joules": 1, "Kilojoules": 1000,
                         "Thermal calories": 4.184, "Food calories": 4184, "Foot-pounds": 1.355818, 
                         "British thermal units": 1055.056}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__energy.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__energy[self.__fromUnitVal.get()] / self.__energy[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class AreaConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Area Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Square meters")
        self.__toUnitVal = tk.StringVar(value="Square feet")
        self.__area = {"Square millimeters": 0.000001, "Square centimeters": 0.0001, "Square meters": 1,
                       "Hectares": 100000, "Square kilometers": 1000000, "Square inches": 0.000645, 
                       "Square feet": 0.092903, "Square yards": 0.836127, "Acres": 4046.856, "Square miles": 2589988}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__area.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__area[self.__fromUnitVal.get()] / self.__area[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class SpeedConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Speed Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilometers per hour")
        self.__toUnitVal = tk.StringVar(value="Miles per hour")
        self.__speed = {"Centimeters per second": 0.01, "Meters per second": 1, "Kilometers per hour": 0.277778,
                        "Feet per second": 0.3048, "Miles per hour": 0.447, "Knots": 0.5144, "Mach": 340.3}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__speed.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__speed[self.__fromUnitVal.get()] / self.__speed[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class TimeConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Time Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Hours")
        self.__toUnitVal = tk.StringVar(value="Minutes")
        self.__time = {"Microseconds": 0.000001, "Milliseconds": 0.001, "Seconds": 1, "Minutes": 60, "Hours": 3600,
                       "Days": 86400, "Weeks": 604800, "Years": 31557600}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__time.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__time[self.__fromUnitVal.get()] / self.__time[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class PowerConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Power Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Kilowats")
        self.__toUnitVal = tk.StringVar(value="Horsepower (US)")
        self.__power = {"Watts": 1, "Kilowats": 1000, "Horsepower (US)": 745.6999, "Foot-pounds/minute": 0.022597,
                        "BTUs/minute": 17.58427}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__power.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__power[self.__fromUnitVal.get()] / self.__power[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class DataConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Data Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Gigabytes")
        self.__toUnitVal = tk.StringVar(value="Megabytes")
        self.__data = {"Bits": 0.000000125, "Bytes": 0.000001, "Kilobits": 0.000125, "Kibibits": 0.000128,
                       "Kilobytes": 0.001, "Kibibytes": 0.001024, "Megabits": 0.125, "Mebibits": 0.131072, 
                       "Megabytes": 1, "Mebibytes": 1.048576, "Gigabits": 125, "Gibibits": 134.2177, 
                       "Gigabytes": 1000, "Gibibytes": 1073.742, "Terabits": 125000, "Tebibits": 137439, 
                       "Terabytes": 1000000, "Tebibytes": 1099512, "Petabits": 125000000, "Pebibits": 140737488,
                       "Petabytes": 10 ** 9, "Pebibytes": 1125899907, "Exabits": 1.25 * (10 ** 8),
                       "Exbibits": 144115188076, "Exabytes": 10 ** 12, "Exibytes": 1152921504607, 
                       "Zetabits": 1.25 * (10 ** 14), "Zebibits": 147573952589676, "Zetabytes": 10 ** 15, 
                       "Zebibytes": 1.180592 * (10 ** 15), "Yottabit": 1.25 * (10 ** 17), 
                       "Yobibits": 1.511157 * (10 ** 17), "Yottabyte": 10 ** 18, "Yobibytes": 1.208926 * (10 ** 18)}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__data.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__data[self.__fromUnitVal.get()] / self.__data[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class PressureConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Pressure Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Atmospheres")
        self.__toUnitVal = tk.StringVar(value="Bars")
        self.__pressure = {"Atmospheres": 101325, "Bars": 100000, "Kilopascals": 1000, "Millimeters of mercury": 133.3,
                           "Pascals": 1, "Pounds per square inch": 6894.757}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__pressure.keys()))
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
        self.set_text(self.__value, self.__value * self.__pressure[self.__fromUnitVal.get()] / self.__pressure[
            self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


class AngleConverter(tk.Frame, UpdateNumber):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        Frame.set_bg_color(self, "black")
        Frame.set_header_text(self, "Angle Converter")
        SelectionButton.summon(self, controller)

        self.__value = 0
        self.__fromUnitVal = tk.StringVar(value="Degrees")
        self.__toUnitVal = tk.StringVar(value="Radians")
        self.__angle = {"Degrees": 1, "Radians": 57.29578, "Gradians": 0.9}

        AnswerField.summon_answer_field(self, 2, 5)
        OptionMenu.summon(self, self.__fromUnitVal, self.__toUnitVal, list(self.__angle.keys()))
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
        self.set_text(self.__value,
                      self.__value * self.__angle[self.__fromUnitVal.get()] / self.__angle[self.__toUnitVal.get()])

    def set_text(self, pastValue, value):
        AnswerField.set_value(self, pastValue, value)


if __name__ == "__main__":
    app = CalculatorApp()
    app.title("Calculatory")
    app.resizable(width=False, height=False)
    app.mainloop()
