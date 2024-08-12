import streamlit as st
import re

def sanitize_input(raw_data):
    sanitized_data = re.sub(r'<.*?>', '', raw_data)
    sanitized_data = re.sub(r'[^\w\s\.,:;\-]', '', sanitized_data)
    return sanitized_data

def style_nmap_output_html(sanitized_data):
    lines = sanitized_data.splitlines()
    styled_html = """
    <style>
        .nmap-output {
            font-family: 'Courier New', Courier, monospace;
            background-color: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            border-radius: 8px;
            border: 1px solid #34495e;
            max-width: 600px;
            margin: 0 auto;
        }
        .nmap-output .header {
            color: #ecf0f1;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .nmap-output .port-info {
            color: #3498db;
            font-weight: bold;
        }
        .nmap-output .port-open {
            color: #2ecc71;
        }
        .nmap-output .port-closed {
            color: #e74c3c;
        }
    </style>
    <div class="nmap-output">
    """

    for line in lines:
        if "Nmap scan report" in line:
            styled_html += f'<div class="header">{line}</div>'
        elif "open" in line:
            styled_html += f'<div class="port-info port-open">{line}</div>'
        elif "closed" in line:
            styled_html += f'<div class="port-info port-closed">{line}</div>'
        else:
            styled_html += f'<div>{line}</div>'

    styled_html += "</div>"
    return styled_html

st.title("Nmap Beautifier")

raw_data = st.text_area("Paste your Nmap scan results here:")

uploaded_file = st.file_uploader("Or upload your Nmap scan results", type=["txt"])

if raw_data or uploaded_file:
    if uploaded_file:
        raw_data = uploaded_file.read().decode('utf-8')

    sanitized_data = sanitize_input(raw_data)

    beautified_html_output = style_nmap_output_html(sanitized_data)

    st.markdown(beautified_html_output, unsafe_allow_html=True)

    st.download_button(
        label="Download as HTML",
        data=beautified_html_output,
        file_name="nmap_output.html",
        mime="text/html",
    )
