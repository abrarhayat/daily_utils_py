import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def calculate_savings(after_tax_salary, num_pay_periods, tax_rate, product_price, setup_fee):
    # Convert after-tax to gross (approximation)
    gross_salary = after_tax_salary / (1 - tax_rate)

    # Remove GST from product price (salary sacrifice uses GST-exclusive cost)
    product_price_ex_gst = product_price / 1.1

    # Salary sacrifice amount per pay period (pre-tax)
    sacrifice_per_period = product_price_ex_gst / num_pay_periods

    # Gross pay after sacrifice
    reduced_gross_salary = gross_salary - sacrifice_per_period

    # After-tax pay with sacrifice
    take_home_with_sacrifice = reduced_gross_salary * (1 - tax_rate)

    # Create lists to track cumulative balances
    balance_with_sacrifice = []
    balance_without_sacrifice = []
    running_with_sacrifice = 0
    running_without_sacrifice = 0

    # Compute cumulative take-home per fortnight
    num_fortnights = 26  # Total fortnights in a year is 26
    for fortnight in range(1, num_fortnights + 1):
        if fortnight <= num_pay_periods:
            running_with_sacrifice += take_home_with_sacrifice
        else:
            running_with_sacrifice += after_tax_salary

        # Without sacrifice: same after-tax pay, but purchase cost once
        running_without_sacrifice += after_tax_salary

        balance_with_sacrifice.append(running_with_sacrifice)
        balance_without_sacrifice.append(running_without_sacrifice)

    # Deduct setup fee and product cost appropriately
    balance_with_sacrifice[-1] -= setup_fee  # small one-time fee
    balance_without_sacrifice[-1] -= product_price

    # Year-end totals
    total_take_home_year_sacrifice = balance_with_sacrifice[-1]
    total_take_home_year_normal = balance_without_sacrifice[-1]
    savings = total_take_home_year_sacrifice - total_take_home_year_normal

    # Breakdown metrics
    tax_savings = product_price_ex_gst * tax_rate
    net_cost_sacrifice = product_price_ex_gst - tax_savings + setup_fee

    df = pd.DataFrame({
        "Fortnight": list(range(1, num_fortnights + 1)),
        "With Salary Sacrifice": balance_with_sacrifice,
        "Without Salary Sacrifice": balance_without_sacrifice,
    })

    return {
        "savings": savings,
        "net_cost_sacrifice": net_cost_sacrifice,
        "tax_savings": tax_savings,
        "gst_excluded_price": product_price_ex_gst,
        "df": df,
        "total_with_sacrifice": total_take_home_year_sacrifice,
        "total_without_sacrifice": total_take_home_year_normal
    }


def main():
    st.title("💰 Salary Sacrifice Savings Calculator (Australia)")
    st.caption("Estimate how much you could save by salary packaging your work device.")
    st.write("This calculator uses a simplified flat tax rate for illustration only. Actual results depend on your full taxable income and employer policy.")

    # User inputs
    after_tax_salary = st.number_input("Fortnightly Take-Home Salary (after tax):", min_value=0.0, value=2000.0, step=100.0)
    num_pay_periods = st.number_input("Number of Fortnights to Spread Cost Over:", min_value=1, max_value=26, value=6, step=1)
    tax_rate = st.number_input("Flat Tax Rate (e.g., 0.30 = 30%):", min_value=0.0, max_value=1.0, value=0.30, step=0.01)
    product_price = st.number_input("Product Price (incl. GST):", min_value=0.0, value=2600.0, step=100.0)
    setup_fee = st.number_input("Packaging Setup Fee ($):", min_value=0.0, value=10.0, step=1.0)

    if st.button("Calculate Savings"):
        results = calculate_savings(after_tax_salary, num_pay_periods, tax_rate, product_price, setup_fee)

        st.subheader("📊 Results Summary")
        col1, col2, col3 = st.columns(3)
        col1.metric("Estimated Savings", f"${results['savings']:,.2f}")
        col2.metric("Net Cost (with Salary Sacrifice)", f"${results['net_cost_sacrifice']:,.2f}")
        col3.metric("Tax Saved", f"${results['tax_savings']:,.2f}")

        st.write("---")
        st.subheader("💼 Annual Comparison")
        st.write(f"**Without Salary Sacrifice:** ${results['total_without_sacrifice']:,.2f}")
        st.write(f"**With Salary Sacrifice:** ${results['total_with_sacrifice']:,.2f}")

        diff = results['savings']
        if diff > 0:
            st.success(f"✅ You end up **${diff:,.2f} ahead** with salary sacrifice!")
        else:
            st.warning(f"⚠️ You end up **${abs(diff):,.2f} behind** with salary sacrifice.")

        # 📈 Plot cumulative balance over time
        df = results['df']
        st.subheader("📈 Bank Balance Over Time (Fortnightly)")
        fig, ax = plt.subplots()
        ax.plot(df["Fortnight"], df["With Salary Sacrifice"], label="With Salary Sacrifice", linewidth=2)
        ax.plot(df["Fortnight"], df["Without Salary Sacrifice"], label="Without Salary Sacrifice", linestyle="--", linewidth=2)
        ax.set_xlabel("Fortnight")
        ax.set_ylabel("Cumulative Take-Home Pay ($)")
        ax.set_title("Comparison of Bank Balance Over the Year")
        ax.legend()
        st.pyplot(fig)

        with st.expander("📖 Detailed Breakdown"):
            st.write(f"- Product price (incl. GST): ${product_price:,.2f}")
            st.write(f"- Product price (excl. GST): ${results['gst_excluded_price']:,.2f}")
            st.write(f"- Tax savings on pre-tax value: ${results['tax_savings']:,.2f}")
            st.write(f"- Setup fee: ${setup_fee:,.2f}")
            st.write(f"- Net cost of item: ${results['net_cost_sacrifice']:,.2f}")

        st.caption("Note: GST savings typically apply only if your employer can claim input tax credits. "
                   "This is a simplified model for educational purposes.")

if __name__ == "__main__":
    main()
