import streamlit as st
from multiapp import MultiApp
from apps import home, data, model,volume # import your app modules here

app = MultiApp()

st.markdown("""
# AAKASH KHANAL'S FINANCIAL TOOLS

""")

# Add all your application here
app.add_app("Home (Stock Info Retriever)", home.app)
app.add_app("Data", data.app)
app.add_app("TA For Stocks/ETFs", model.app)
app.add_app("Unusual Volume Indicator", volume.app)
# The main app
app.run()
