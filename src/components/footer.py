import streamlit as st

def footer_home():

    st.markdown("""
        <div style="margin-top:2rem; display:flex; justify-content:center; align-items:center;">
            <p style="font-size:20px; font-weight:bold; color:white;">
                Created with ❤️ by 
                <span style="
                    color:#00BFFF;
                    font-size:24px;
                    font-family:cursive;
                    text-shadow:2px 2px 5px #000;">
                    Chetan Jhod
                </span>
            </p>
        </div>
    """, unsafe_allow_html=True)


def footer_dashboard():
 st.markdown(
    "<h4 style='text-align:center; color:black;'>Created with ❤️ by <span style='color:#00BFFF;'>Chetan Jhod</span></h4>",
    unsafe_allow_html=True
)