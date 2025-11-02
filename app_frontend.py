import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/items/"

st.title("🕸 FastAPI + SQLite3 CRUD App ! ")

st.set_page_config(page_title="FastAPI CRUD App", page_icon="🕸", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #f9fafc;
        padding: 2rem;
        border-radius: 10px;
    }
    h1, h2, h3 {
        color: #2b5876;
        text-align: center;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
    .stButton>button:hover {
        background-color: #45a049;
    }
    </style>
""", unsafe_allow_html=True)




menu = st.sidebar.selectbox("Menu", ["Create", "Read", "Update", "Delete"])

# --- CREATE ---
if menu == "Create":
    st.subheader("Add a new item")
    name = st.text_input("Name")
    price = st.number_input("Price", min_value=0.0)
    description = st.text_area("Description")

    if st.button("Create"):
        data = {"name": name, "price": price, "description": description}
        res = requests.post(API_URL, json=data)
        st.success(res.json()["message"])

# --- READ ---
elif menu == "Read":
    st.subheader("All items")
    res = requests.get(API_URL)
    if res.status_code == 200:
        items = res.json()
        st.table(items)
    else:
        st.error("Error loading items")

# --- UPDATE ---
elif menu == "Update":
    st.subheader("Update item")
    item_id = st.number_input("Item ID", min_value=1, step=1)
    name = st.text_input("New Name")
    price = st.number_input("New Price", min_value=0.0)
    description = st.text_area("New Description")

    if st.button("Update"):
        data = {"name": name, "price": price, "description": description}
        res = requests.put(f"{API_URL}{item_id}", json=data)
        if res.status_code == 200:
            st.success("Updated successfully")
        else:
            st.error(res.json()["detail"])

# --- DELETE ---
elif menu == "Delete":
    st.subheader("Delete item")
    item_id = st.number_input("Item ID to delete", min_value=1, step=1)

    if st.button("Delete"):
        res = requests.delete(f"{API_URL}{item_id}")
        if res.status_code == 200:
            st.success("Deleted successfully")
        else:
            st.error(res.json()["detail"])
