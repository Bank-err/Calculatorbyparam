import streamlit as st

# Function to calculate tax correctly with marginal relief
def calculate_tax(income):
    standard_deduction = 75000
    threshold_income = 1275000  # ₹12.75L threshold for nil tax after deduction
    taxable_income = max(0, income - standard_deduction)

    # Tax slabs as per new regime (After ₹4L exemption)
    tax_slabs = [
        (400000, 0.05),  # 5% for ₹4L - ₹8L
        (400000, 0.10),  # 10% for ₹8L - ₹12L
        (400000, 0.15),  # 15% for ₹12L - ₹16L
        (400000, 0.20),  # 20% for ₹16L - ₹20L
        (400000, 0.25),  # 25% for ₹20L - ₹24L
        (float('inf'), 0.30)  # 30% above ₹24L
    ]

    # Compute tax based on slabs
    tax = 0
    remaining_income = taxable_income
    lower_limit = 400000  # No tax for first ₹4L

    for slab, rate in tax_slabs:
        if remaining_income > 0:
            taxable_amount = min(remaining_income, slab)
            tax += taxable_amount * rate
            remaining_income -= taxable_amount
        else:
            break

    # Cess Calculation (4%)
    cess = tax * 0.04
    total_tax = tax + cess

    # Apply Marginal Relief → Tax should be ₹0 if income is ₹12.75L or less
    if income <= threshold_income:
        total_tax = 0  

    return round(tax, 2), round(cess, 2), round(total_tax, 2)

# Streamlit UI
st.title("Bank-err's Income Tax Calculator for FY 2025-26")
st.write("As per new tax regime (including marginal tax relief)")

income = st.number_input("Enter your Annual Income (₹)", min_value=0, step=1000, value=1275000)
tax, cess, total_tax = calculate_tax(income)

# Display tax breakdown
st.subheader("💰 Tax Calculation Breakdown")
st.write(f"**Standard Deduction:** ₹75,000")
st.write(f"**Tax (Before Cess & Relief):** ₹{tax}")
st.write(f"**Cess (4%):** ₹{cess}")
st.write(f"**Total Tax Payable:** ₹{total_tax}")

# Developer Credit
st.markdown("<h4 style='color:cyan'>Developed by Paramjeet Gusain</h4>", unsafe_allow_html=True)
