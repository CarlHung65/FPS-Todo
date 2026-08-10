import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="Employees Management System", layout="wide")

st.title("Employees")

API_URL = "http://127.0.0.1:8000/employees"

def fetch_data():
    try:
        response = requests.get(API_URL)
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"status code : {response.status_code}")
            return []
    except Exception as e:
        st.error("Failed to link backend. Please check the backend was running.")
        return []
    
data = fetch_data()

if data:
    df = pd.DataFrame(data)
    
    col1, col2 = st.columns(2)

    with col1:
        search_keyword = st.text_input("Search employee's name : ")

    with col2:
        departments = ["All"] + sorted([d for d in df["department"].unique() if d])
        selected_dept = st.selectbox("Department:", departments)

    filtered_df = df.copy()
    if search_keyword:
        filtered_df = filtered_df[filtered_df["name"].astype(str).str.contains(search_keyword, case=False, na=False)]
    if selected_dept != "All":
        filtered_df = filtered_df[filtered_df["department"] == selected_dept]

    st.dataframe(filtered_df, use_container_width=True)

    if st.button("Reload data"):
        st.rerun()

else:
    st.info("No data. Please check backend service is running.")