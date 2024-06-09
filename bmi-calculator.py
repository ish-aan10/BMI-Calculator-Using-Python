import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import csv

custom_font = ("Bahnschrift", 12)

class BMICalculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")
        self.root.config(bg="#a1d1ff")
        self.canvas = tk.Canvas(self.root,width=400,height=400,border=0,bg="white")
        self.canvas.grid(row=0,column=0,padx=10,pady=10)
        
        self.label = tk.Label(root,text="BMI CALCULATOR",font=("Bahnschrift", 22, "bold"),bg="white")
        self.canvas.create_window(200,30, window=self.label)
        
        self.measure = tk.StringVar(value="metric")
        
        self.metric = tk.Radiobutton(root,text="METRIC",bg="white",activebackground="white",value="metric",variable=self.measure,font=custom_font,command=lambda: self.update_measure())
        self.canvas.create_window(140,71, window=self.metric)
        self.imperial = tk.Radiobutton(root,text="IMPERIAL",bg="white",activebackground="white",value="imperial",variable=self.measure,font=custom_font,command=lambda: self.update_measure())
        self.canvas.create_window(250,71, window=self.imperial)

        self.weight_label = tk.Label(root,text="WEIGHT:",font=custom_font,bg="white")
        self.canvas.create_window(100,114, window=self.weight_label)
        self.weight_entry = tk.Entry(root,justify="center",font=("Bahnschrift", 15),width=10,bg="#d4eefc")
        self.canvas.create_window(200,115, window=self.weight_entry)
        self.w_label = tk.Label(root,text="in kg",bg="white",font=custom_font)
        self.canvas.create_window(305,115, window=self.w_label)

        self.height_label = tk.Label(root,text="HEIGHT:",font=custom_font,bg="white")
        self.canvas.create_window(100,154, window=self.height_label)
        self.height_entry = tk.Entry(root,justify="center",font=("Bahnschrift", 15),width=10,bg="#d4eefc")
        self.canvas.create_window(200,155, window=self.height_entry)
        self.h_label = tk.Label(root,text="in cm",bg="white",font=custom_font)
        self.canvas.create_window(305,155, window=self.h_label)
    
        self.error_label = tk.Label(root,text="",bg="white",fg="red",font=("Bahnschrift", 14, "bold"))
        self.canvas.create_window(200,190, window=self.error_label)
        
        self.result_label = tk.Label(root, text="", font=("Bahnschrift", 18, "bold"),bg="#a1d1ff", width=25,height=3)
        self.canvas.create_window(200,260, window=self.result_label)

        self.calculate_button = tk.Button(root,bg="#5451fc",activebackground="#5451fc",text="CALCULATE BMI",font=custom_font,command=self.calculate_bmi,width=20, height=2)
        self.canvas.create_window(101,370, window=self.calculate_button)

        self.graph_button = tk.Button(root, bg="#ff4040",activebackground="#ff4040",text="VIEW DATA", font=custom_font, width=20, height=2, command=self.view_historical_data)
        self.canvas.create_window(300,370, window=self.graph_button)

        self.user_data = {}
        self.root.protocol("WM_WINDOW_DESTROY", self.save_data)
   
    def update_measure(self):
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        if self.measure.get() == "metric":
            self.w_label.config(text="in kg")
            self.h_label.config(text="in cm")
        elif self.measure.get() == "imperial":
            self.w_label.config(text="in pounds")
            self.h_label.config(text="in feets")
        self.root.update()
    
    def calculate_bmi(self):
        if self.weight_entry.get() == "" or self.height_entry.get() == "":
            self.error_label.config(text="Input Cannot Be Empty")
            root.after(3000, self.clear_error_message)
            return
        if self.weight_entry.get().isalpha() or self.height_entry.get().isalpha():
            self.error_label.config(text="Input Cannot Be a Character or String")
            root.after(3000, self.clear_error_message)
            return
        if float(self.weight_entry.get()) < 0 or float(self.height_entry.get()) < 0:
            self.error_label.config(text="Invalid Input")
            root.after(3000, self.clear_error_message)
            return
        
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())

            if self.measure.get() == "imperial":
                weight = weight * 0.453592
                height = height * 0.0254 * 12
            else:
                height = height/100

            bmi = weight / (height ** 2)
            category = self.get_category(bmi)

            self.result_label.config(text=f"BMI: {bmi:.2f} ({category})")

            username = "default"
            if username not in self.user_data:
                self.user_data[username] = []
            self.user_data[username].append((weight, height, bmi))

        except ValueError as e:
            self.error_label_label.config(text=f"{e}")
            root.after(3000, self.clear_error_message)
            return

    def clear_error_message(self):
        self.error_label.config(text="")
    
    def get_category(self, bmi):
        if bmi < 16:
            return "Severe Thinness"
        elif bmi < 17:
            return "Moderate Thinness"
        elif bmi < 18.5:
            return "Mild Thinness"
        elif bmi < 25:
            return "Normal"
        elif bmi < 30:
            return "Overweight"
        elif bmi < 35:
            return "Obese Class I"
        elif bmi < 40:
            return "Obese Class II"
        else:
            return "Obese Class III"

    def view_historical_data(self):
        username = "default"
        if username not in self.user_data:
            messagebox.showinfo("No data", "No historical data available")
            return

        weights, heights, bmis = zip(*self.user_data[username])
        plt.plot(bmis,color="#0000cc",linewidth=5,marker="o",markersize=12,markerfacecolor="#d60012")
        plt.xlabel("MEASUREMENT")
        plt.ylabel("BMI")
        plt.title("BMI Trend Analysis")
        plt.show()

    def save_data(self):
        with open("user_data.csv", "w", newline="") as csvfile:
            writer = csv.writer(csvfile)
            for username, data in self.user_data.items():
                for weight, height, bmi in data:
                    writer.writerow([username, weight, height, bmi])

    def load_data(self):
        try:
            with open("user_data.csv", "r", newline="") as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    username, weight, height, bmi = row
                    if username not in self.user_data:
                        self.user_data[username] = []
                    self.user_data[username].append((float(weight), float(height), float(bmi)))
        except FileNotFoundError:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = BMICalculator(root)
    app.load_data()
    root.mainloop()
    app.save_data()