import streamlit as st
import requests
import pandas as pd
from datetime import date, datetime

st.set_page_config(page_title="Employees Management System", layout="wide")

st.title("Employees")

API_URL = "http://127.0.0.1:8000/employees"

tab1, tab2, tab3 = st.tabs(["List and Create", "Update", "Delete"])

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

# ==========================================
# Tab 1: 新增和查看員工資料
# ==========================================
with tab1:
    with st.sidebar:
        st.header("➕ 新增員工")
        
        with st.form("add_employee_form", clear_on_submit=True):
            emp_id = st.text_input("員工編號 (必填)*", placeholder="例如：E005")
            name = st.text_input("姓名 (必填)*", placeholder="例如：張小明")
            gender = st.selectbox("性別", ["Male", "Female", "Other"])
            email = st.text_input("Email", placeholder="test@example.com")
            phone = st.text_input("電話", placeholder="0912345678")
            department = st.text_input("部門", placeholder="研發部")
            salary = st.number_input("薪水", min_value=0.0, step=1000.0, value=45000.0)
            hire_date = st.date_input("到職日期", value=date.today())
            
            submitted = st.form_submit_button("送出新增")
            
            if submitted:
                if not emp_id or not name:
                    st.warning("⚠️ 請填寫必填欄位 (員工編號與姓名)")
                else:
                    # 打包要傳給 FastAPI 的 JSON 資料
                    payload = {
                        "emp_id": emp_id,
                        "name": name,
                        "gender": gender,
                        "email": email if email else None,
                        "phone": phone if phone else None,
                        "department": department if department else None,
                        "salary": salary,
                        "hire_date": str(hire_date)  # 日期轉為字串 ISO 格式 (YYYY-MM-DD)
                    }
                    
                    # 發送 POST 請求給 FastAPI
                    res = requests.post(API_URL, json=payload)
                    
                    if res.status_code == 201:
                        st.success(f"🎉 成功新增員工：{name}！")
                        st.rerun()  # 重新整理頁面以抓取最新資料
                    else:
                        error_msg = res.json().get("detail", "新增失敗")
                        st.error(f"❌ 新增失敗：{error_msg}")
                        
# ==========================================
# Tab 2: 編輯員工資料
# ==========================================
with tab2:
    st.subheader("✏️ 修改員工資訊")
    if data:
        # 下拉選單選取要編輯的員工
        emp_options = {f"ID: {e['id']} | {e['name']} ({e['emp_id']})": e for e in data}
        selected_option = st.selectbox("選擇要編輯的員工：", list(emp_options.keys()))
        selected_emp = emp_options[selected_option]

        # 預填原有資料的表單
        with st.form("edit_form"):
            new_name = st.text_input("姓名", value=selected_emp.get("name") or "")
            new_gender = st.selectbox("性別", ["Male", "Female", "Other"], 
                                      index=["Male", "Female", "Other"].index(selected_emp.get("gender")) if selected_emp.get("gender") in ["Male", "Female", "Other"] else 0)
            new_email = st.text_input("Email", value=selected_emp.get("email") or "")
            new_phone = st.text_input("電話", value=selected_emp.get("phone") or "")
            new_dept = st.text_input("部門", value=selected_emp.get("department") or "")
            new_salary = st.number_input("薪水", value=float(selected_emp.get("salary") or 0))
            
            # 日期轉檔防錯處理
            raw_date = selected_emp.get("hire_date")
            default_date = datetime.strptime(raw_date, "%Y-%m-%d").date() if raw_date else date.today()
            new_date = st.date_input("到職日期", value=default_date)

            if st.form_submit_button("💾 儲存修改"):
                payload = {
                    "name": new_name, "gender": new_gender,
                    "email": new_email or None, "phone": new_phone or None,
                    "department": new_dept or None, "salary": new_salary,
                    "hire_date": str(new_date)
                }
                res = requests.put(f"{API_URL}/{selected_emp['id']}", json=payload)
                if res.status_code == 200:
                    st.success("修改成功！")
                    st.rerun()
                else:
                    st.error("修改失敗！")

# ==========================================
# Tab 3: 刪除員工資料
# ==========================================
with tab3:
    st.subheader("🗑️ 刪除員工紀錄")
    if data:
        emp_options_del = {f"ID: {e['id']} | {e['name']} ({e['emp_id']}) - {e['department']}": e['id'] for e in data}
        target_label = st.selectbox("選擇要刪除的員工：", list(emp_options_del.keys()))
        target_id = emp_options_del[target_label]

        st.warning("⚠️ 警告：刪除動作無法復原！")
        if st.button("❌ 確認刪除此員工", type="primary"):
            res = requests.delete(f"{API_URL}/{target_id}")
            if res.status_code == 204:
                st.success("員工已成功刪除！")
                st.rerun()
            else:
                st.error("刪除失敗！")