import tkinter as tk
from tkinter import messagebox
import sqlite3
import random

# Database setup
conn = sqlite3.connect("meal_planner.db")
cursor = conn.cursor()

# Check if 'diet_type' column exists; if not, add it
cursor.execute("PRAGMA table_info(meal_plans)")
columns = [col[1] for col in cursor.fetchall()]
if "diet_type" not in columns:
    cursor.execute("ALTER TABLE meal_plans ADD COLUMN diet_type TEXT")
    conn.commit()

# Expanded meal database with ingredients
MEAL_DATABASE = {
    "Vegan": {
        "Breakfast": ["Chia Pudding with Almonds", "Oatmeal with Blueberries", "Cashew Yogurt with Flaxseeds"],
        "Lunch": ["Quinoa Salad with Chickpeas", "Avocado & Spinach Wrap", "Sweet Potato Buddha Bowl"],
        "Dinner": ["Lentil Soup with Brown Rice", "Tempeh Stir-Fry with Coconut Sauce", "Grilled Zucchini & Bell Peppers"]
    },
    "Plant-Based": {
        "Breakfast": ["Smoothie with Bananas & Hemp Seeds", "Tofu Scramble with Peppers", "Whole Grain Toast with Avocado"],
        "Lunch": ["Kale & Quinoa Bowl", "Black Bean Chili with Corn", "Stuffed Bell Peppers with Mushrooms"],
        "Dinner": ["Vegetable Curry with Brown Rice", "Baked Sweet Potatoes with Almond Sauce", "Cauliflower Stir-Fry"]
    },
    "Raw": {
        "Breakfast": ["Raw Almond Butter with Dates", "Goji Berry & Coconut Bowl", "Chia Seeds with Raw Cacao"],
        "Lunch": ["Zucchini Noodles with Cherry Tomatoes", "Raw Mushroom Salad with Lemon Dressing", "Sprouts & Kimchi Bowl"],
        "Dinner": ["Fermented Vegetables with Cashews", "Mixed Greens with Cashew Dressing", "Raw Veggie Wraps"]
    },
    "Whole-Food": {
        "Breakfast": ["Steel-Cut Oats with Walnuts", "Fruit Bowl with Flaxseeds", "Whole-Grain Toast with Almond Butter"],
        "Lunch": ["Black Beans & Brown Rice", "Roasted Carrots & Kale Bowl", "Whole-Grain Pasta with Tomato Sauce"],
        "Dinner": ["Wild Rice with Roasted Eggplant", "Steamed Broccoli & Lentils", "Miso Glazed Vegetables"]
    }
}

# Main Application Window
class MealPlannerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome to Healthy Bitez Meal Planner")
        self.root.geometry("700x450")

        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(main_frame, text="Welcome to Healthy Bitez Meal Planner!", font=("Arial", 14)).pack(pady=10)

        tk.Button(main_frame, text="Create Meal Plan", command=self.open_meal_planner).pack(pady=5)
        tk.Button(main_frame, text="View Saved Plans", command=self.view_saved_plans).pack(pady=5)
        tk.Button(main_frame, text="Exit", command=root.quit).pack(pady=5)

    def open_meal_planner(self):
        planner_window = tk.Toplevel(self.root)
        planner_window.title("Meal Planner")
        planner_window.geometry("700x450")

        planner_frame = tk.Frame(planner_window)
        planner_frame.pack(expand=True, fill="both", padx=20, pady=20)

        tk.Label(planner_frame, text="Select Dietary Preference:", font=("Arial", 12)).pack()
        diet_type_var = tk.StringVar()
        diet_type_var.set("Vegan")
        tk.OptionMenu(planner_frame, diet_type_var, *MEAL_DATABASE.keys()).pack()

        tk.Label(planner_frame, text="Select Meal Type:", font=("Arial", 12)).pack()
        meal_type_var = tk.StringVar()
        meal_type_var.set("Breakfast")
        tk.OptionMenu(planner_frame, meal_type_var, "Breakfast", "Lunch", "Dinner").pack()

        def generate_plan():
            diet_type = diet_type_var.get()
            meal_type = meal_type_var.get()

            if not diet_type or not meal_type:
                messagebox.showerror("Error", "Please select both a diet and meal type.")
                return

            meal_options = MEAL_DATABASE[diet_type][meal_type]
            meal_plan = random.choice(meal_options)
            grocery_list = meal_plan.split()  # Extract words as basic ingredient list

            cursor.execute("INSERT INTO meal_plans (diet_type, meals, grocery_list) VALUES (?, ?, ?)", 
                           (diet_type, meal_plan, ", ".join(grocery_list)))
            conn.commit()

            self.show_ingredients_window(meal_plan, grocery_list)

        tk.Button(planner_frame, text="Generate Plan", command=generate_plan).pack(pady=10)

    def show_ingredients_window(self, meal_plan, ingredients):
        ingredients_window = tk.Toplevel(self.root)
        ingredients_window.title("Meal Ingredients")
        ingredients_window.geometry("600x400")

        tk.Label(ingredients_window, text=f"Meal: {meal_plan}", font=("Arial", 12)).pack(pady=10)
        tk.Label(ingredients_window, text="Ingredients:", font=("Arial", 12, "bold")).pack()

        for ingredient in ingredients:
            tk.Label(ingredients_window, text=f"- {ingredient}", font=("Arial", 10)).pack()

    def view_saved_plans(self):
        saved_window = tk.Toplevel(self.root)
        saved_window.title("Saved Meal Plans")
        saved_window.geometry("700x450")

        saved_frame = tk.Frame(saved_window)
        saved_frame.pack(expand=True, fill="both", padx=20, pady=20)

        cursor.execute("SELECT * FROM meal_plans")
        plans = cursor.fetchall()

        for plan in plans:
            tk.Label(saved_frame, text=f"Diet: {plan[1]} | Meal: {plan[2]}", font=("Arial", 10)).pack()
            tk.Label(saved_frame, text=f"Grocery List: {plan[3]}", font=("Arial", 10)).pack()

if __name__ == "__main__":
    root = tk.Tk()
    app = MealPlannerApp(root)
    root.mainloop()
