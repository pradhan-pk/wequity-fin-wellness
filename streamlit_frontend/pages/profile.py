import streamlit as st
import requests

st.set_page_config(page_title="Profile", page_icon="👤")
st.title("👤 Welcome, " + st.session_state.get("username", "User"))

backend_url = "http://localhost:8000"

# Basic user details
st.subheader("My Details")

st.write(f"City: {st.session_state["city"]}")
# st.write(f"City Tier: {st.session_state["city_tier"]}")
st.write(f"Job Role: {st.session_state["job_type"]}")



# ---------- Section 1: Income Prediction ----------
st.header("📈 Income Prediction")
st.write("Based on your last 3 months' income and gig trends")


# past_income = st.text_input("Enter your past 3 months income (comma separated)")
# city = st.selectbox("Select City Tier", ["tier_1", "tier_2", "tier_3"])
# role = st.selectbox("Select Gig Role", ["ride_hailing", "food_delivery", "freelance"])

# if st.button("Predict Income"):
#     try:
#         history = list(map(float, past_income.split(",")))
#         payload = {
#             "income_history": history,
#             "city_tier": city,
#             "role": role
#         }
#         res = requests.post(f"{backend_url}/predict_income", json=payload)
#         if res.ok:
#             result = res.json()
#             st.success(f"Next Month Income: ₹{result['predicted_income']:.2f} ± ₹{result['volatility']:.2f}")
#         else:
#             st.error("Prediction failed.")
#     except:
#         st.error("Please enter valid comma-separated values.")

if st.button("Predict Next Month's Income"):
    response = requests.post(f"{backend_url}/predict_income", json={"username": st.session_state["username"]})
    if response.ok:
        result = response.json()
        st.success(f"Predicted Income: ₹{result['predicted_income']}")
        st.info(f"Estimated Volatility: ± ₹{round(result['volatility_estimate'] * result['predicted_income'], 2)}")
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
        "expenses": {
            "rent": rent,
            "groceries": groceries,
            "utilities": utilities,
            "transport": transport,
            "misc": misc
        }
    }
    res = requests.post(f"{backend_url}/save_expenses", json=expense_data)
    if res.ok:
        st.success("Expenses recorded!")
    else:
        st.error("Error saving expenses.")

# ---------- Section 3: Budget Advisor ----------
st.header("🧠 Budgeting Advisor")
if st.button("Get Budget Advice"):
    res = requests.get(f"{backend_url}/budget_advice", params={"username": st.session_state["username"]})
    if res.ok:
        advice = res.json()
        st.subheader("🔎 Recommendations:")
        st.markdown(f"**💰 Save More On:** {advice['save_on']}")
        st.markdown(f"**📈 Consider Investing In:** {advice['invest_in']}")
        st.markdown(f"**⚠️ Cut Back On:** {advice['cut_back_on']}")
    else:
        st.error("Couldn't fetch advice. Please try again later.")
