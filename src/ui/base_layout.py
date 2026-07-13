import streamlit as st

def style_background_home():

    st.markdown("""
        <style>
                
             .stApp{
                background: #5865F2 !important;
            }
            .stApp div[data-testid="stColumn"]{ 
                background-color:#E0E3FF !important;
                padding:1.5rem !important;
                border-radius:5rem !important;
                }
    </style>
                
                
                
                """
            ,unsafe_allow_html=True)
    




    
def style_background_dashboard():

    st.markdown("""
        <style>
                
             .stApp{
                background: #E0E3FF !important;
            }

       </style>
                
                
                """
            ,unsafe_allow_html=True)
    




    
def style_base_layout():
#asdasd
    
    st.markdown("""
       <style>
       @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis&display=swap');
       @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@100..900&display=swap');
                /*hide Top Bar of streamlit */

       /* Hide Top Bar of streamlit */

           #MainMenu, footer, header {
             visibility: hidden;
            }

             .block-container {
                 padding-top:1.5rem !important;
            }

                
            h1 {
                
                font-family: 'climate crisis' , sans-serif !important;
                font-size: 1.8rem !important;
                font-weight: 700 !important;
                line-height: 1.1 !important;
                margin-bottom:0rem !important;
            }

            h2 {
                
                font-family: 'climate crisis' , sans-serif !important;
                font-size: 1.5rem !important;
                line-height:0.9 !important;
                margin-bottom:0rem !important;
                }

            h1, h2, h3 {
                color: #111111 !important;
                opacity: 1 !important;
                text-shadow: none !important;
            }

            h3, h4, p {
                font-family: 'outfit', sans-serif;
            }
                
            button{
                border-radius: 1.5rem !important;
                background-color: #5865F2 !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }
                

            button[kind="secondary"]{
                border-radius: 1.5rem !important;
                background-color: #EB459E !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }
                
            button[kind="tertiary"]{
                border-radius: 1.5rem !important;
                background-color: black !important;
                color: white !important;
                padding: 10px 20px !important;
                border: none !important;
                transition: transform 0.25s ease-in-out !important;
                }

            .stButton > button:hover {
                transform: scale(1.05);
            }
            div[data-testid="stTextInput"] input {
               background: #FFFFFF !important;
               color: #111111 !important;
              -webkit-text-fill-color: #111111 !important;
               border: 2px solid #D9D9D9 !important;
               border-radius: 14px !important;
            }

            div[data-testid="stTextInput"] input:focus {
                border: 2px solid #5865F2 !important;
                box-shadow: 0 0 0 2px rgba(88,101,242,0.15) !important;
            }

            div[data-testid="stTextInput"] input::placeholder {
                color: #9CA3AF !important;
                opacity: 1 !important;
            }

            div[data-testid="stWidgetLabel"] p {
                color: #111111 !important;
                font-weight: 600 !important;
            }
            label {
                    color: #111111 !important;
                }

                [data-testid="stWidgetLabel"] {
                color: #111111 !important;
            }
        </style>
                
                
                """
            ,unsafe_allow_html=True)