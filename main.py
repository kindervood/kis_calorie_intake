import tkinter as tk
from database import DatabaseManager
from windows import AddDishWindow, SearchDishWindow, PlotCalorieIntakeWindow

class CalorieApp:
    def __init__(self, root):
        self.root = root
        self.db_manager = DatabaseManager()
        self.setup_ui()

    def setup_ui(self):
        self.root.title("Calorie Counting App")
        self.root.geometry("400x300")
        self.root.configure(bg="#f0f0f0")

        title_label = tk.Label(self.root, text="Calorie Counting App", font=("Helvetica", 16, "bold"), bg="#f0f0f0")
        title_label.pack(pady=20)

        button_font = ("Helvetica", 12)
        button_bg = "#44944a"
        button_fg = "#ffffff"

        add_dish_button = tk.Button(self.root, text="Add Dish", command=self.open_add_dish_window, font=button_font, bg=button_bg, fg=button_fg)
        add_dish_button.pack(pady=10, ipadx=10, ipady=5)

        search_dish_button = tk.Button(self.root, text="Dish List", command=self.open_search_dish_window, font=button_font, bg=button_bg, fg=button_fg)
        search_dish_button.pack(pady=10, ipadx=10, ipady=5)

        plot_calorie_intake_button = tk.Button(self.root, text="Plot Calorie Intake", command=self.open_plot_calorie_intake_window, font=button_font, bg=button_bg, fg=button_fg)
        plot_calorie_intake_button.pack(pady=10, ipadx=10, ipady=5)

        footer_label = tk.Label(self.root, text="Track your daily calorie intake easily!", font=("Helvetica", 10), bg="#f0f0f0")
        footer_label.pack(side="bottom", pady=10)

    def open_add_dish_window(self):
        AddDishWindow(self.root, self.db_manager)

    def open_search_dish_window(self):
        SearchDishWindow(self.root, self.db_manager)

    def open_plot_calorie_intake_window(self):
        PlotCalorieIntakeWindow(self.root, self.db_manager)

if __name__ == "__main__":
    root = tk.Tk()
    app = CalorieApp(root)
    root.mainloop()