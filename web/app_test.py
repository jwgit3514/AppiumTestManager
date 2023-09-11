import pandas as pd
import streamlit as st

df = pd.DataFrame({"A": [1, 2, 3], "B": [2, 3, 4]})

df["C"] = df["B"]

if "data" not in st.session_state:
    st.session_state.data = df

editor_value = st.data_editor(
    st.session_state["data"],
    column_config={
        "B": st.column_config.SelectboxColumn(label="test_type", options=[0, 1], width="None", required=True,),
        "C": st.column_config.Column(disabled=True)},
    hide_index=True,
)

if not editor_value.equals(st.session_state["data"]):
    editor_value["C"] = editor_value["B"]
    st.session_state["data"] = editor_value
    st.experimental_rerun()


if st.button('test'):
    for i in range(len(st.session_state.data['B'])):
        print(st.session_state.data['B'][i])
