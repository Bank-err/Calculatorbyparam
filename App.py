import streamlit as st

# Function to calculate tax with marginal relief
def calculate_tax(income):
    standard_deduction = 75000
    threshold_income = 1275000  # ₹12.75L threshold for nil tax after standard deduction
    taxable_income = max(0, income - standard_deduction)

    # Tax slabs as per new regime
    tax_slabs = [
        (400000, 0.05),  # 5% on 4-8L
        (400000, 0.10),  # 10% on 8-12L
        (400000, 0.15),  # 15% on 12-16L
        (400000, 0.20),  # 20% on 16-20L
        (400000, 0.25),  # 25% on 20-24L
        (float('inf'), 0.30)  # 30% on above 24L
    ]

    # Compute tax slab-wise
    tax = 0
    remaining_income = taxable_income
    lower_limit = 400000  # First 4L is tax-free

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

    # Apply Marginal Relief
    if income > threshold_income:
        excess_income = income - threshold_income
        if total_tax > excess_income:
            total_tax = excess_income  # Marginal Relief applied

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
