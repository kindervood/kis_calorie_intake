import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime
import matplotlib.pyplot as plt

class AddDishWindow:
    def __init__(self, root, db_manager):
        self.db_manager = db_manager
        self.add_window = tk.Toplevel(root)
        self.add_window.title("Add Dish")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.add_window, text="Dish Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(self.add_window)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)
        self.name_entry.bind('<FocusOut>', self.check_existing_dish)

        tk.Label(self.add_window, text="Portion Size (g):").grid(row=1, column=0, padx=10, pady=5)
        self.portion_size_entry = tk.Entry(self.add_window)
        self.portion_size_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Date Consumed (YYYY-MM-DD):").grid(row=2, column=0, padx=10, pady=5)
        self.date_entry = tk.Entry(self.add_window)
        self.date_entry.grid(row=2, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Kcal per 100g:").grid(row=3, column=0, padx=10, pady=5)
        self.kcal_entry = tk.Entry(self.add_window)
        self.kcal_entry.grid(row=3, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Protein per 100g:").grid(row=4, column=0, padx=10, pady=5)
        self.protein_entry = tk.Entry(self.add_window)
        self.protein_entry.grid(row=4, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Fat per 100g:").grid(row=5, column=0, padx=10, pady=5)
        self.fat_entry = tk.Entry(self.add_window)
        self.fat_entry.grid(row=5, column=1, padx=10, pady=5)

        tk.Label(self.add_window, text="Carbs per 100g:").grid(row=6, column=0, padx=10, pady=5)
        self.carbs_entry = tk.Entry(self.add_window)
        self.carbs_entry.grid(row=6, column=1, padx=10, pady=5)

        submit_button = tk.Button(self.add_window, text="Submit", command=self.submit_dish)
        submit_button.grid(row=7, column=0, columnspan=2, pady=10)

    def check_existing_dish(self, event):
        name = self.name_entry.get()
        if name:
            dish = self.db_manager.execute_query('SELECT kcal, protein, fat, carbs FROM dishes WHERE name = ?', (name,))
            if dish:
                self.kcal_entry.delete(0, tk.END)
                self.protein_entry.delete(0, tk.END)
                self.fat_entry.delete(0, tk.END)
                self.carbs_entry.delete(0, tk.END)
                
                self.kcal_entry.insert(0, dish[0][0])
                self.protein_entry.insert(0, dish[0][1])
                self.fat_entry.insert(0, dish[0][2])
                self.carbs_entry.insert(0, dish[0][3])

    def submit_dish(self):
        name = self.name_entry.get()
        date = self.date_entry.get()
        kcal = self.kcal_entry.get()
        protein = self.protein_entry.get()
        fat = self.fat_entry.get()
        carbs = self.carbs_entry.get()
        portion_size = self.portion_size_entry.get()
        
        if name and kcal and protein and fat and carbs:
            try:
                kcal = float(kcal)
                protein = float(protein)
                fat = float(fat)
                carbs = float(carbs)
                
                # Check if dish already exists
                dish = self.db_manager.execute_query('SELECT id FROM dishes WHERE name = ?', (name,))
                
                if not dish:
                    # Insert into dishes table if not exists
                    self.db_manager.execute_update('''
                        INSERT INTO dishes (name, kcal, protein, fat, carbs)
                        VALUES (?, ?, ?, ?, ?)
                    ''', (name, kcal, protein, fat, carbs))
                    dish_id = self.db_manager.execute_query('SELECT last_insert_rowid()')[0][0]
                else:
                    dish_id = dish[0][0]
                
                # Only insert into consumption table if date and portion size are provided
                if date and portion_size:
                    portion_size = float(portion_size)
                    # Validate date format
                    datetime.strptime(date, '%Y-%m-%d')
                    
                    self.db_manager.execute_update('''
                        INSERT INTO consumption (dish_id, date, portion_size)
                        VALUES (?, ?, ?)
                    ''', (dish_id, date, portion_size)) 
                
                messagebox.showinfo("Success", "Dish added successfully!")
                self.add_window.destroy()
            except ValueError:
                messagebox.showwarning("Input Error", "Please enter valid numbers for kcal, protein, fat, carbs, and a valid date in YYYY-MM-DD format if provided.")
        else:
            messagebox.showwarning("Input Error", "Please provide all required details for the dish.")

class SearchDishWindow:
    def __init__(self, root, db_manager):
        self.db_manager = db_manager
        self.search_window = tk.Toplevel(root)
        self.search_window.title("Dish List")
        self.search_window.geometry("1000x500")
        self.create_widgets()

    def create_widgets(self):
        # Create a frame to center the search components
        search_frame = tk.Frame(self.search_window)
        search_frame.pack(pady=20)

        tk.Label(search_frame, text="Dish Name:").grid(row=0, column=0, padx=10, pady=5)
        self.name_entry = tk.Entry(search_frame, width=30)
        self.name_entry.grid(row=0, column=1, padx=10, pady=5)

        search_button = tk.Button(search_frame, text="Search", command=self.submit_search)
        search_button.grid(row=1, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.search_window, text="")
        self.result_label.pack(pady=10)

        # Create a frame for the Treeview
        tree_frame = tk.Frame(self.search_window)
        tree_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=10)

        self.tree = ttk.Treeview(tree_frame, columns=("Name", "Kcal", "Protein", "Fat", "Carbs"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Kcal", text="Kcal")
        self.tree.heading("Protein", text="Protein")
        self.tree.heading("Fat", text="Fat")
        self.tree.heading("Carbs", text="Carbs")
        self.tree.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        self.tree.bind("<Double-1>", self.on_double_click)

        self.populate_treeview()

    def submit_search(self):
        name = self.name_entry.get()
        if name:
            dish = self.db_manager.execute_query('SELECT * FROM dishes WHERE name = ?', (name,))
            if dish:
                self.result_label.config(text=f"Found: {dish[0][1]}, Kcal: {dish[0][2]}, Protein: {dish[0][3]}, Fat: {dish[0][4]}, Carbs: {dish[0][5]}")
            else:
                self.result_label.config(text="Dish not found.")
        else:
            messagebox.showwarning("Input Error", "Please enter a dish name to search.")

    def populate_treeview(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        
        dishes = self.db_manager.execute_query('SELECT id, name, kcal, protein, fat, carbs FROM dishes')

        for dish in dishes:
            self.tree.insert("", "end", iid=dish[0], values=dish[1:])

    def on_double_click(self, event):
        item_id = self.tree.selection()[0]
        column = self.tree.identify_column(event.x)
        column_index = int(column.replace('#', '')) - 1

        # Get the bounding box of the selected cell
        x, y, width, height = self.tree.bbox(item_id, column)
        # Adjust the position to align the Entry widget correctly
        x += self.tree.winfo_rootx() - self.search_window.winfo_rootx()
        y += self.tree.winfo_rooty() - self.search_window.winfo_rooty()

        entry = tk.Entry(self.search_window)
        entry.place(x=x, y=y, width=width, height=height)
        entry.insert(0, self.tree.item(item_id, 'values')[column_index])

        def save_edit(event):
            new_value = entry.get()
            entry.destroy()
            values = list(self.tree.item(item_id, 'values'))
            values[column_index] = new_value
            self.tree.item(item_id, values=values)

            # Update the database
            column_names = ["name", "kcal", "protein", "fat", "carbs"]
            self.db_manager.execute_update(f"UPDATE dishes SET {column_names[column_index]} = ? WHERE id = ?", (new_value, item_id))

        entry.bind('<FocusOut>', save_edit)
        entry.bind('<Return>', save_edit)
        entry.focus_set()

class PlotCalorieIntakeWindow:
    def __init__(self, root, db_manager):
        self.db_manager = db_manager
        self.plot_window = tk.Toplevel(root)
        self.plot_window.title("Plot Calorie Intake")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.plot_window, text="Start Date (YYYY-MM-DD):").grid(row=0, column=0, padx=10, pady=5)
        self.start_date_entry = tk.Entry(self.plot_window)
        self.start_date_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(self.plot_window, text="End Date (YYYY-MM-DD):").grid(row=1, column=0, padx=10, pady=5)
        self.end_date_entry = tk.Entry(self.plot_window)
        self.end_date_entry.grid(row=1, column=1, padx=10, pady=5)

        submit_button = tk.Button(self.plot_window, text="Submit", command=self.submit_plot)
        submit_button.grid(row=2, column=0, columnspan=2, pady=10)

    def submit_plot(self):
        start_date = self.start_date_entry.get()
        end_date = self.end_date_entry.get()
        
        if start_date and end_date:
            data = self.db_manager.execute_query('''
                SELECT c.date, SUM(d.kcal * c.portion_size / 100.0)  as total_kcal
                FROM consumption c
                JOIN dishes d ON c.dish_id = d.id
                WHERE c.date BETWEEN ? AND ?
                GROUP BY c.date
            ''', (start_date, end_date))

            if data:
                dates = [datetime.strptime(row[0], '%Y-%m-%d') for row in data]
                total_kcals = [row[1] for row in data]

                plt.bar(dates, total_kcals, color='skyblue')
                plt.xlabel('Date')
                plt.ylabel('Total Calories')
                plt.title('Total Calorie Intake Per Day')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
                self.plot_window.destroy()
            else:
                messagebox.showinfo("No Data", "No consumption data found for the given period.")
        else:
            messagebox.showwarning("Input Error", "Please provide both start and end dates.")
