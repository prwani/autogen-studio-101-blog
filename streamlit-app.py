import streamlit as st
from autogenstudio.teammanager import TeamManager
import asyncio

st.title("Dev Team App")
user_input = st.text_input("Enter something:")

# Initialize the TeamManager
manager = TeamManager()

# Run a task with a specific team configuration
result = asyncio.run(manager.run(
task=user_input,
team_config="dev-team-config.json",
))
if user_input:
    st.write(result)
