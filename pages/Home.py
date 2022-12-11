import streamlit as st
from hydralit import HydraHeadApp
import streamlit_nested_layout
class HomePage(HydraHeadApp):

    def run(self):
        group1 = st.empty()
        with group1.container():
            col1,col2,col3 = st.columns([1,2,1])
            with col1:
                st.write(' ')
            with col2:
                group2 = st.empty()
                with group2.container():
                    st.title("Đồ án môn học Machine Learning")
                    st.header("Thành viên nhóm:")
                    col2_1,col2_2 = st.columns([1,1])
                    with col2_1:
                        st.subheader("Họ và tên")
                        st.write("Lê Anh Hùng")
                        st.write("Nguyễn Thanh Danh")
                        st.write("Nguyễn Khắc Dương")
                    with col2_2:
                        st.subheader("Mã số sinh viên")
                        st.write("20110617")
                        st.write("20110145")
                        st.write("20110627")
            with col3:
                st.write(' ')
