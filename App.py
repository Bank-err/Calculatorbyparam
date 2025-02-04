import streamlit as st

# Function to calculate tax with marginal relief
def calculate_tax(income):
    standard_deduction = 75000
    threshold_income = 1275000  # ₹12.75L threshold for zero tax
    taxable_income = max(0, income - standard_deduction)

    # Define tax slabs (after ₹4L exemption)
    tax_slabs = [
        (400000, 0.05),  # 5% for ₹4L - ₹8L
        (400000, 0.10),  # 10% for ₹8L - ₹12L
        (400000, 0.15),  # 15% for ₹12L - ₹16L
        (400000, 0.20),  # 20% for ₹16L - ₹20L
        (400000, 0.25),  # 25% for ₹20L - ₹24L
        (float('inf'), 0.30)  # 30% above ₹24L
    ]
