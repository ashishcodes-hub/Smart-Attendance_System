import streamlit as st

def header_home():
    logo = "https://i.ibb.co/YTYGn5qV/logo.png"

    st.markdown(f"""
        <div style="
                display:flex; 
                flex-direction:column;
                align-items : center, 
                justify-content:center ,
                margin-bottom:10px,
                margin-top : 50px" >
            <img src ='{logo}' style = 'height:70px;' />
            <h1 style='text-align:center; color : #E0E3FF'>SNAP <br> CLASS </h1>
        </div>        
""", unsafe_allow_html=True)