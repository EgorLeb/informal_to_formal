import streamlit as st

text = st.text_area("Введите текст в неформальной форме", max_chars=300, height=150)

if st.button("Перевести"):
    st.text_area("Ответ", max_chars=300, height=150, value=", блять, ".join(text.upper().split()))
else:
    st.text_area("Ответ", max_chars=300, height=150)
