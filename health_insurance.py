import streamlit as st
import pandas as pd

# In-memory storage
if "policies" not in st.session_state:
    st.session_state.policies = {}

st.title("🏥 Health Insurance Management System")

menu = st.sidebar.selectbox("Menu", [
    "Add Policy",
    "View Policies",
    "Search Policy",
    "Update Policy",
    "Delete Policy",
    "Analytics"
])

# Add Policy
if menu == "Add Policy":
    st.subheader("Add New Policy")

    pid = st.text_input("Policy ID")
    name = st.text_input("Customer Name")
    age = st.number_input("Age", min_value=1)
    ptype = st.selectbox("Policy Type", ["Basic", "Premium", "Family"])
    premium = st.number_input("Premium Amount", min_value=0)
    claim = st.selectbox("Claim Status", ["Yes", "No"])

    if st.button("Add Policy"):
        if pid in st.session_state.policies:
            st.error("Policy ID already exists!")
        else:
            st.session_state.policies[pid] = {
                "Name": name,
                "Age": age,
                "Type": ptype,
                "Premium": premium,
                "Claim": claim
            }
            st.success("Policy added successfully!")

# View Policies
elif menu == "View Policies":
    st.subheader("All Policies")

    if st.session_state.policies:
        df = pd.DataFrame.from_dict(st.session_state.policies, orient='index')
        st.dataframe(df)
    else:
        st.warning("No policies found!")

# Search Policy
elif menu == "Search Policy":
    st.subheader("Search Policy")

    pid = st.text_input("Enter Policy ID")

    if st.button("Search"):
        if pid in st.session_state.policies:
            st.json(st.session_state.policies[pid])
        else:
            st.error("Policy not found!")

# Update Policy
elif menu == "Update Policy":
    st.subheader("Update Policy")

    pid = st.text_input("Enter Policy ID")

    if pid in st.session_state.policies:
        data = st.session_state.policies[pid]

        name = st.text_input("Name", data["Name"])
        age = st.number_input("Age", value=data["Age"])
        ptype = st.selectbox("Type", ["Basic", "Premium", "Family"])
        premium = st.number_input("Premium", value=data["Premium"])
        claim = st.selectbox("Claim", ["Yes", "No"])

        if st.button("Update"):
            st.session_state.policies[pid] = {
                "Name": name,
                "Age": age,
                "Type": ptype,
                "Premium": premium,
                "Claim": claim
            }
            st.success("Updated successfully!")

# Delete Policy
elif menu == "Delete Policy":
    st.subheader("Delete Policy")

    pid = st.text_input("Enter Policy ID")

    if st.button("Delete"):
        if pid in st.session_state.policies:
            del st.session_state.policies[pid]
            st.success("Deleted successfully!")
        else:
            st.error("Policy not found!")

# Analytics
elif menu == "Analytics":
    st.subheader("Analytics")

    if st.session_state.policies:
        df = pd.DataFrame.from_dict(st.session_state.policies, orient='index')

        st.write("Policy Count by Type:")
        st.write(df["Type"].value_counts())

        st.write("Average Premium:", df["Premium"].mean())
        st.write("Max Premium:", df["Premium"].max())

    else:
        st.warning("No data available!")
