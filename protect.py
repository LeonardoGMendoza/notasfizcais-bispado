import glob

for file in glob.glob('pages/*.py'):
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    protection_code = 'import streamlit as st\nif "authentication_status" not in st.session_state or not st.session_state["authentication_status"]:\n    st.switch_page("app.py")\n'
    if 'st.switch_page' not in content:
        with open(file, 'w', encoding='utf-8') as f:
            f.write(protection_code + '\n' + content)
