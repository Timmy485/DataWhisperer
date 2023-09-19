import streamlit as st


st. set_page_config(layout="wide")
st.markdown(
    """
    <style>
    .appview-container .main .block-container {
        padding-top: 2rem;
        margin: 0;
    }
    .css-usj992 {
    background-color: transparent;
    }
    </style>
    """,
    unsafe_allow_html=True
)


st.markdown(
    "<h1 style='text-align: center; padding: 10px;'>DATA WHISPERER</h1>",
    unsafe_allow_html=True
)
st.markdown(
    "<h3 style='text-align: center; padding: 2px;'>Unveil Insights From Docs.</h3>",
    unsafe_allow_html=True
)

# Sidebar Navigation with header background color
st.sidebar.markdown(
    "<h3 style= padding: 10px;'>Navigation</h3>",
    unsafe_allow_html=True
)

# Use a dropdown menu for feature selection
selected_feature = st.sidebar.selectbox("Select a Feature", (
    "Upload & Analyze Custom Document",
    "Query Existing Documents"
))

# Main Content with light background color
st.markdown(
    "<div style='background-color: #f9f9f9; padding: 0px;'>",
    unsafe_allow_html=True
)