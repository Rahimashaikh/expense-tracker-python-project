import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

def load_data():
    if os.path.exists("expenses.csv"):
        return pd.read_csv("expenses.csv")
    else:
        return pd.DataFrame(columns=["Name", "Amount", "Category", "Date"])

def save_data(df):
    df.to_csv("expenses.csv", index=False)

def reset_data():
    """Function to reset expenses (delete all records)."""
    if os.path.exists("expenses.csv"):
        os.remove("expenses.csv")  
    st.success("✅ Expenses have been reset! Start fresh for the new month.")
    st.rerun()  # 🔄 Refresh Streamlit App

def main():
 
 
    st.title("💰  Smart Expense Manager – Track , Save & Succeed")

    st.markdown("💸 **Take control of your finances with ease!**\n\n"
            "📊 **Manage your expenses like a pro** ║ track, analyze, and stay within budget effortlessly.\n\n"
            "🎯 **Smart budgeting made simple** ║ monitor your spending, gain financial clarity, and achieve your savings goals without the hassle.")


    st.markdown("""
    <style>
        body {
            background: linear-gradient(to right, #f8f9fa,rgba(125, 174, 222, 0.83));
        }
        .stApp {
            background: linear-gradient(to right, #f8f9fa,rgba(46, 88, 129, 0.25));
        }
    </style>
    """, unsafe_allow_html=True)









    df = load_data()

    st.header("📝 Add Your Expense")
    expense_name = st.text_input("Expense Name", placeholder="Enter expense (e.g., Grocery, Rent)")
    amount = st.number_input("Amount (Rs.)", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
    date = st.date_input("Date")

    if st.button("Add Expense"):
        if expense_name and amount > 0:
            new_expense = pd.DataFrame([[expense_name, amount, category, date]], 
                                       columns=["Name", "Amount", "Category", "Date"])
            df = pd.concat([df, new_expense], ignore_index=True)
            save_data(df)
            st.success(f"Expense '{expense_name}' of Rs. {amount} added successfully!")
        else:
            st.warning("Please enter valid expense details.")

    st.header("📊 Your Expenses")

    if not df.empty:
        st.dataframe(df)

        st.header("📈 Expense Breakdown")
        fig = px.pie(df, names='Category', values='Amount', title='Expenses by Category')
        st.plotly_chart(fig)

        st.header("⚠️ Set Budget Alert")
        budget_limit = st.number_input("Set Your Budget Limit (Rs.)", min_value=0.0, format="%.2f")

        total_expense = df["Amount"].sum()
        st.write(f"💸 **Total Expenses:** Rs. {total_expense}")
        if budget_limit > 0 and total_expense > budget_limit:
            st.error("🚨 Budget Exceeded! Try to control your expenses.")
        else:
            st.success("✅ You are within your budget.")

        st.header("📂 Download Expenses Report")
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("Download CSV", data=csv, file_name="expenses.csv", mime="text/csv")

        # 🔴 Reset Expenses Button
        st.header("🛑 Reset Expenses for New Month")
        if st.button("Reset Expenses"):
            reset_data()

    st.markdown("""
        <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 50%;
                transform: translateX(-50%);
                width: 100%;
                text-align: center;
                padding: 10px;
                font-weight: bold;
                font-size: 16px;
                background-color: #f1f1f1;
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
        <div class="footer">Developed with ❤️  by  <span style='color: #E63946;'> Rahima Shaikh </span>       using Streamlit</div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
