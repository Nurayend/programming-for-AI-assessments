"""
FILE: app/dashboard.py
DESCRIPTION:
    The main entry point for the treSamlit web application. 
    It creates the user interface (UI) and visualises the data.

TEAM TASKS:
    1. Create a Sidebar Menu to switch between:
       - 'Student Entry' (Forms for input).
       - 'Wellbeing Dashboard' (For the Officer).
       - 'Course Director Analytics' (For the Director).
    2. Use st.form() to collect input and call 'database_manager' to save it.
    3. Use st.line_chart() or st.scatter_chart() to display data from 'analytics.py'.
    
    *Requirement: Provide simple analytics and visualise changes over time[cite: 72, 86].*
"""
#import streamlit as st