import streamlit as st

### Config ###
st.set_page_config(layout="wide")
api_key = ""

### end Config ###


### Sidebar ###
st.sidebar.title("API Key")
with st.sidebar.form(key="api_key_input", clear_on_submit=False):
    st.markdown(
        " Go to **the-odds-api.com** and get a free API key. Once you have it paste it in the form below. "
    )
    api_key = st.text_input("API Key", value="")
    st.form_submit_button()

    st.text(" One run of the application makes about 50 API calls. ")

### end Sidebar ###

### Main page ###
