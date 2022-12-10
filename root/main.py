import streamlit as st
from pages import pages
from hydralit import HydraApp

over_theme = {'txc_inactive': '#FFFFFF'}
if __name__ == '__main__':

    app = HydraApp(title='Đồ án Machine learning',favicon="🐙",
        use_navbar=True, 
        hide_streamlit_markers=False,
        banner_spacing=[5,30,60,30,5],
        navbar_sticky=False,
        navbar_theme=over_theme,
        sidebar_state="collapsed",
        use_loader=False,
    )
    app.st = st

    ##Chỉnh css của web
    #Tắt sidebar
    no_sidebar_style = """
        <style>
            div[data-testid="stSidebarNav"] {display: none;}
            div[data-testid="collapsedControl"] {display: none;}
            section[data-testid="stSidebar"] {display:none;}
        </style>
    """
    st.markdown(no_sidebar_style, unsafe_allow_html=True)

    #Tắt footer
    hide_st_style = f"""
        <style>
            footer {{visibility: hidden;}}
        </style>
    """
    st.markdown(hide_st_style, unsafe_allow_html=True)
    #background
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
    background: radial-gradient(farthest-side ellipse at 10% 0, hsl(300, 100%, 95%), hsl(190, 50%, 70%) 80%, hsl(226, 40%, 60%) 120%);
    background-size: 180%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: local;
    }}
    [data-testid="stSidebar"] > div:first-child {{
    background: linear-gradient(#50a3a2 0%, #53e3a6 100%);
    background-position: center; 
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
    [data-testid="stHeader"] {{
    background: rgba(0,0,0,0);
    }}
    [data-testid="stToolbar"] {{
    right: 2rem;
    }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)


    for app_name,app_function  in pages.items():
        if(app_name == "Home"):
            app.add_app(app_name,app=app_function(),is_home=True)
        else:
            app.add_app(app_name,app=app_function())

    app.run()


