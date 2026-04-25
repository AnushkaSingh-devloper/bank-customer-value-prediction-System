import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import pandas as pd
import joblib

# Load trained model
try:
    model = joblib.load("../model/final_bank_model.pkl")
    encoder = joblib.load("../model/label_encoder.pkl")
except Exception as e:
    print("Model Load Error:", e)

# Prediction function
def predict():
    try:
        print("Button clicked")

        # Check empty fields
        if not all([
            age_entry.get(),
            credit_entry.get(),
            spending_entry.get(),
            income_entry.get(),
            freq_entry.get(),
            avg_entry.get()
        ]):
            messagebox.showerror("Error", "Please fill all fields")
            return

        # Get values
        age = int(age_entry.get())
        credit = int(credit_entry.get())
        spending = int(spending_entry.get())
        income = int(income_entry.get())
        freq = int(freq_entry.get())
        avg = int(avg_entry.get())

        loan_mapping = {"Bad": 0, "Average": 1, "Good": 2}
        loan_value = loan_mapping[loan_var.get()]

        print("Input:", age, credit, spending, income, loan_value, freq, avg)

        # Create DataFrame (IMPORTANT FIX)
        data = pd.DataFrame([{
            'Age': age,
            'CreditScore': credit,
            'SpendingScore': spending,
            'Income': income,
            'LoanHistory': loan_value,
            'Transaction_Frequency': freq,
            'Avg_Transaction': avg
        }])

        # Prediction
        result = model.predict(data)
        print("Prediction:", result)

        # Output result
        if result[0] == 1:
            result_label.config(text="✅ High Value Customer", fg="#2ecc71")
        else:
            result_label.config(text="⚠️ Low Value Customer", fg="#e74c3c")

    except Exception as e:
        print("Error:", e)
        messagebox.showerror("Error", str(e))


# ---------------- UI ---------------- #

root = tk.Tk()
root.title("Bank Customer Intelligence System")
root.geometry("450x600")
root.configure(bg="#f4f6f7")

# Title
title = tk.Label(
    root,
    text="🏦 Bank Customer Predictor",
    font=("Helvetica", 18, "bold"),
    bg="#2c3e50",
    fg="white",
    pady=10
)
title.pack(fill="x")
# Frame
frame = tk.Frame(root, bg="#f4f6f7")
frame.pack(pady=20)

# Function to create entry fields
def create_entry(label_text):
    tk.Label(frame, text=label_text, bg="#f4f6f7", font=("Arial", 11)).pack()
    entry = tk.Entry(frame, font=("Arial", 11))
    entry.pack(pady=5)
    return entry

# Inputs
age_entry = create_entry("Age")
credit_entry = create_entry("Credit Score")
spending_entry = create_entry("Spending Score")
income_entry = create_entry("Income")

# Loan dropdown
tk.Label(frame, text="Loan History", bg="#f4f6f7", font=("Arial", 11)).pack()

loan_var = tk.StringVar()
loan_dropdown = ttk.Combobox(
    frame,
    textvariable=loan_var,
    values=["Bad", "Average", "Good"],
    state="readonly"
)
loan_dropdown.pack(pady=5)
loan_dropdown.current(0)

# Remaining inputs
freq_entry = create_entry("Transaction Frequency")
avg_entry = create_entry("Avg Transaction Value")

# Predict Button
predict_btn = tk.Button(
    root,
    text="Predict Customer Value",
    command=predict,
    bg="#3498db",
    fg="white",
    font=("Arial", 12, "bold"),
    padx=10,
    pady=5
)
predict_btn.pack(pady=15)

# Result Label
result_label = tk.Label(
    root,
    text="",
    font=("Arial", 14, "bold"),
    bg="#f4f6f7"
)
result_label.pack(pady=10)

# Footer
footer = tk.Label(
    root,
    text="Built using Machine Learning",
    bg="#2c3e50",
    fg="white",
    font=("Arial", 9)
)
footer.pack(side="bottom", fill="x")

# Run App
root.mainloop()