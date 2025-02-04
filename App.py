import streamlit as st

# Function to calculate tax under the new tax regime
def calculate_new_tax(income):
    standard_deduction = 75000
    threshold = 1275000  # 12.75L (including standard deduction)

    slabs = [(0, 0), (300000, 0.05), (600000, 0.1), (900000, 0.15), (1200000, 0.2), (1500000, 0.3)]
    
    if income <= threshold:
        return 0, 0, []

    taxable_income = income - standard_deduction
    tax = 0
    breakdown = []

    for i in range(1, len(slabs)):
        if taxable_income > slabs[i][0]:
            slab_tax = (min(taxable_income, slabs[i][0]) - slabs[i - 1][0]) * slabs[i][1]
            tax += slab_tax
            breakdown.append(f"₹{slabs[i - 1][0] + 1} - ₹{slabs[i][0]}: ₹{round(slab_tax, 2)}")

    marginal_relief = max(0, (income - threshold) - tax)
    final_tax = min(tax, income - threshold) + marginal_relief
    cess = final_tax * 0.04

    return round(final_tax, 2), round(cess, 2), breakdown

# Function to calculate tax under the old tax regime
def calculate_old_tax(income, deductions):
    old_threshold = 250000
    slabs = [(0, 0), (250000, 0.05), (500000, 0.2), (1000000, 0.3)]

    taxable_income = max(0, income - deductions)
    tax = 0
    breakdown = []

    for i in range(1, len(slabs)):
        if taxable_income > slabs[i][0]:
            slab_tax = (min(taxable_income, slabs[i][0]) - slabs[i - 1][0]) * slabs[i][1]
            tax += slab_tax
            breakdown.append(f"₹{slabs[i - 1][0] + 1} - ₹{slabs[i][0]}: ₹{round(slab_tax, 2)}")

    cess = tax * 0.04
    return round(tax, 2), round(cess, 2), breakdown

# Streamlit UI
st.title("💰 Bank-err's Income Tax Calculator for FY 2025-26")
st.markdown("### **As per new tax regime**")
st.markdown("### **Marginal income relief applied**")

# Income input
income = st.number_input("Enter your total annual income (₹)", min_value=0, step=1000, value=1275000)

# Tax Regime Selection
tab1, tab2 = st.tabs(["New Tax Regime", "Old Tax Regime"])

# New Tax Regime
with tab1:
    new_tax, new_cess, new_breakdown = calculate_new_tax(income)
    show_breakup = st.checkbox("Show tax & cess breakup")

    st.subheader(f"Tax Payable: ₹{new_tax + new_cess}")
    if show_breakup:
        st.markdown(f"**Tax: ₹{new_tax}**  \n**Cess (4%): ₹{new_cess}**")
        st.markdown("**Tax Breakdown:**")
        for item in new_breakdown:
            st.markdown(f"- {item}")

# Old Tax Regime
with tab2:
    st.markdown("### **Enter Deductions**")
    sec_80c = st.number_input("80C (LIC, PPF, ELSS, EPF, Tuition Fees, etc.)", min_value=0, step=1000)
    sec_80d = st.number_input("80D (Health Insurance Premium)", min_value=0, step=1000)
    home_loan = st.number_input("Section 24 (Home Loan Interest)", min_value=0, step=1000)
    hra = st.number_input("HRA Exemption", min_value=0, step=1000)

    total_deductions = sec_80c + sec_80d + home_loan + hra
    old_tax, old_cess, old_breakdown = calculate_old_tax(income, total_deductions)

    st.subheader(f"Tax Payable: ₹{old_tax + old_cess}")
    if show_breakup:
        st.markdown(f"**Tax: ₹{old_tax}**  \n**Cess (4%): ₹{old_cess}**")
        st.markdown("**Tax Breakdown:**")
        for item in old_breakdown:
            st.markdown(f"- {item}")

# Footer
st.markdown("<h4 style='color:cyan; text-align:center;'>Created by - Paramjeet Singh Gusain</h4>", unsafe_allow_html=True)
