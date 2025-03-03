import streamlit as st
import pandas as pd
import plotly.express as px
import os
import json
from cryptography.fernet import Fernet

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")

# Function to get user-specific file names
def get_user_files(username):
    return f"{username}_key.key", f"{username}_expenses.json"

# Function to generate or load encryption key for a user
def load_key(username):
    key_file, _ = get_user_files(username)

    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, "wb") as file:
            file.write(key)
    else:
        with open(key_file, "rb") as file:
            key = file.read()

    return Fernet(key)

# Function to encrypt data
def encrypt_data(cipher, data):
    return cipher.encrypt(data.encode()).decode()

# Function to decrypt data
def decrypt_data(cipher, encrypted_data):
    return cipher.decrypt(encrypted_data.encode()).decode()

# Function to save expenses securely
def save_expenses(username, expenses):
    key_file, data_file = get_user_files(username)
    cipher = load_key(username)
    encrypted_data = encrypt_data(cipher, json.dumps(expenses))

    with open(data_file, "w") as file:
        json.dump({"data": encrypted_data}, file)

# Function to load expenses securely
def load_expenses(username):
    key_file, data_file = get_user_files(username)
    cipher = load_key(username)

    if not os.path.exists(data_file):
        return []

    with open(data_file, "r") as file:
        data = json.load(file)
        return json.loads(decrypt_data(cipher, data["data"]))

# Function to reset user expenses
def reset_data(username):
    key_file, data_file = get_user_files(username)
    if os.path.exists(data_file):
        os.remove(data_file)
    st.success("✅ Your expenses have been reset!")
    st.rerun()

# Main function
def main():
    st.title("💰 Smart Expense Manager By Rahima | Track, Save & Succeed")

    st.markdown("💸 **Take control of your finances with ease!**\n\n"
                "📊 **Manage your expenses like a pro** ║ track, analyze, and stay within budget effortlessly.\n\n"
                "🎯 **Smart budgeting made simple** ║ monitor your spending, gain financial clarity, and achieve your savings goals.")
    
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


    
    username = st.text_input("Enter Your Username", placeholder="E.g., Your Name")

    if not username:
        st.warning("Please enter your username to continue.")
        return

    df = pd.DataFrame(load_expenses(username))

    st.header("📝 Add Your Expense")
    expense_name = st.text_input("Expense Name", placeholder="Enter expense (e.g., Grocery, Rent)")
    amount = st.number_input("Amount (Rs.)", min_value=0.0, format="%.2f")
    category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Entertainment", "Other"])
    date = st.date_input("Date")

    if st.button("Add Expense"):
        if expense_name and amount > 0:
            new_expense = {"Name": expense_name, "Amount": amount, "Category": category, "Date": str(date)}
            expenses = load_expenses(username)
            expenses.append(new_expense)
            save_expenses(username, expenses)
            st.success(f"Expense '{expense_name}' of Rs. {amount} added successfully!")
            st.rerun()
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
        st.download_button("Download CSV", data=csv, file_name=f"{username}_expenses.csv", mime="text/csv")

        st.header("🛑 Reset Your Expenses")
        if st.button("Reset Expenses"):
            reset_data(username)

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
        <div class="footer">Developed with ❤️ by <span style='color: #E63946;'> Rahima Shaikh </span> using Streamlit</div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
