import streamlit as st

st.set_page_config(
    page_title="TranslateMate",
    page_icon="translate.png"
) 

st.header(":mailbox: Contact Us")

contact_form = """ 
<form action="https://formsubmit.co/vsai1510@gmail.com" method="POST">
     <input type="text" name="name" placeholder="Name" required>
     <input type="email" name="email" placeholder="E-mail" required>
     <textarea name="message" placeholder="Message"></textarea>
     <button type="submit">Send</button>
</form>
"""

st.markdown(contact_form, unsafe_allow_html=True)

def css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style",unsafe_allow_html=True)
css("style/style.css")
