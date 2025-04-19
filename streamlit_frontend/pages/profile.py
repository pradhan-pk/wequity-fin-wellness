import streamlit as st
import requests
import matplotlib.pyplot as plt

st.set_page_config(page_title="Profile", page_icon="👤")
st.title("👤 Welcome, " + st.session_state.get("username", "User"))

backend_url = "http://localhost:8000"

# Basic user details
st.subheader("My Details")

st.write(f"**City**: {st.session_state["city"]}")
# st.write(f"City Tier: {st.session_state["city_tier"]}")
st.write(f"**Job Role**: {st.session_state["job_type"]}")
st.write("")
past_income = st.session_state["past_income"]


fig, ax = plt.subplots(figsize=(8,5))
ax.bar(["Month 1", "Month 2", "Month 3"], past_income, color="skyblue")
ax.set_xlabel("Income (₹)")
ax.set_title("Past 3 Months Income")
# ax.invert_yaxis()  # Invert the y-axis for an inverted horizontal bar chart
col1, col2, col3 = st.columns([1, 3, 1])
with col2: 
    st.pyplot(fig)
    # Center-align the "City" line
    st.markdown(f"<div style='text-align: center;'>Past 3 Months Income: ₹{past_income[0]}, ₹{past_income[1]}, ₹{past_income[2]}</div>", unsafe_allow_html=True)


# ---------- Section 1: Income Prediction ----------
st.header("📈 Income Prediction")
st.write("Based on your last 3 months' income and gig trends")

if st.button("Predict Next Month's Income"):
    response = requests.post(f"{backend_url}/predict_income", json={"username": st.session_state["username"]})
    if response.ok:
        result = response.json()
        st.write(f"**Predicted Income: ₹{result['predicted_income']}**")
        st.write(f"**Estimated Volatility: ± ₹{round(result['volatility_estimate'] * result['predicted_income'], 2)}**")
        st.session_state["next_month_income"] = result['predicted_income']
        st.session_state["volatility"] = result['volatility_estimate']
    else:
        st.error(f"Failed: {response.json()['detail']}")



# ---------- Section 2: Expense Tracker ----------
st.header("💸 Expense Tracker")

st.write("Manually enter your monthly expenses:")

with st.form("expense_form"):
    rent = st.number_input("🏠 Rent", min_value=0)
    groceries = st.number_input("🛒 Groceries", min_value=0)
    utilities = st.number_input("🔌 Utilities", min_value=0)
    transport = st.number_input("🚗 Transportation", min_value=0)
    misc = st.number_input("📦 Miscellaneous", min_value=0)
    submit_expense = st.form_submit_button("Submit")

if submit_expense:
    expense_data = {
        "username": st.session_state["username"],
        "city": st.session_state["city"],
        "city_tier": st.session_state["city_tier"],
        "past_income": st.session_state["past_income"],
        "next_month_income": st.session_state["next_month_income"],
        "volatility": st.session_state["volatility"],
        "expenses": {
            "rent": rent,
            "groceries": groceries,
            "utilities": utilities,
            "transport": transport,
            "misc": misc
        }
    }
    res = requests.post(f"{backend_url}/save_expenses_suggest", json=expense_data)
    if res.ok:
        st.success("Expenses recorded!")
    else:
        st.error("Error saving expenses.")

    # ---------- Section 3: Budget Advisor ----------
    st.header("🧠 Budgeting Advisor")
    # if st.button("Get Budget Advice"):
    #     res = requests.get(f"{backend_url}/budget_advice", params={"username": st.session_state["username"]})
    #     if res.ok:
    #         advice = res.json()
    #         st.subheader("🔎 Recommendations:")
    #         st.markdown(f"**💰 Save More On:** {advice['save_on']}")
    #         st.markdown(f"**📈 Consider Investing In:** {advice['invest_in']}")
    #         st.markdown(f"**⚠️ Cut Back On:** {advice['cut_back_on']}")
    #     else:
    #         st.error("Couldn't fetch advice. Please try again later.")

    response = res.json()
    st.markdown(response["advice"], unsafe_allow_html=True)
