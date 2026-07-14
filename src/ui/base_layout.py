import streamlit as st


def style_background_home():

    st.markdown("""
        <style>
                
                .stApp{
                background : #5865F2 !important;
                }

                .stApp div[data-testid="stColumn"]{
                background-color : #E0E3FF !important;
                padding : 1.5rem !important;
                # padding-bottom : 2rem !important;
                border-radius : 4rem !important;
                }
        </style>

""", unsafe_allow_html=True)

def style_background_dashbord():

    st.markdown("""
        <style>
                
                .stApp{
                background : #E0E3FF !important;
                }
        </style>

# """, unsafe_allow_html=True)

def style_base_layout():






    st.markdown("""
        <style>
                 @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&display=swap');
                 @import url('https://fonts.googleapis.com/css2?family=Climate+Crisis:YEAR@1979&family=Outfit:wght@100..900&display=swap');
                







               
                #MainMenu, footer, header{
                visibility :hidden;
                }

                .block-container{
                padding-top:0rem !important;
                }

                h1{
                font-family: 'Climate Crisis' ,sans-serif !important;
                font-size:2rem !important;
                line-height : 2rem !important;
                margin-bottom : 0rem !important ;
                margin : 0rem !important ;
                text-align : center  !important ;
                padding: 0rem !important ;
                padding-bottom: 2rem !important ;
                }

                h2 {
                font-family:'Climate Crisis', sans-serif !important;
                font-size:1.5rem !important;
                line-height : 3rem !important;
                margin-bottom : 0rem !important ;   
                color : #3b3737 !important;   
        
                }
                 h3, h4, p{
                font-family:'Outfit',sans-serif !important;
                }

                button{
                border-radius : 1.5rem !important;
                background : #5865F2 !important;
                color : white !important;
                padding : 10px 20px !important;
                border : none !important;
                transition : transform 0.25s ease-in-out !important;

                }

                button[kind = "secondary"]{
                border-radius : 1.5rem !important;
                background : #EB459E !important;
                color : white !important;   
                padding : 10px 20px !important;
                border : none !important;
                transition : transform 0.25s ease-in-out !important;
                
                }

                button[kind = tertiary]{
                border-radius : 1.5rem !important;
                background : black !important;
                color : white !important;
                padding : 10px 20px !important;
                border : none !important;
                transition : transform 0.25s ease-in-out !important;
                
                }

                button:hover{
                transform : scale(1.05)
                }
        # chatgpt
                
       /* ===========================
   TEXT INPUT STYLING
=========================== */

/* Outer container */
div[data-testid="stTextInput"] > div {
    background: white !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 12px !important;
}

/* Inner container */
div[data-testid="stTextInput"] > div > div {
    background: white !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
    border-radius: 12px !important;
}

/* Actual input */
div[data-testid="stTextInput"] input {
    background: white !important;
    color: black !important;
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Focus state */
div[data-testid="stTextInput"] input:focus {
    border: none !important;
    outline: none !important;
    box-shadow: none !important;
}

/* Placeholder */
div[data-testid="stTextInput"] input::placeholder {
    color: #666 !important;
    opacity: 1 !important;
}

div[data-testid="stTextInput"] label {
    color: black !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
} 
                                        
                
        </style>
                

                

""", unsafe_allow_html=True)
    

