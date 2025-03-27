import streamlit as st
import PyPDF2

def extract_text(uploaded_file):
    reader = PyPDF2.PdfReader(uploaded_file)
    merged_pdf = PyPDF2.PdfWriter()

    zone_1_prefix = ["ART", "NEEB", "STAUF", "COOR"]
    zone_3_prefix = ["EDB", "ED", "EDC", "MUSIC"]
    zone_4_prefix = ["CDN", "BYAC", "HLMK", "ISTBX", "COWDN", "SHESC"]

    special_cases = ["COOR L1-18", "COOR L1-72", "COOR L1-80", "EDB 120", "EDB L1-26", "HLMK 101",
                     "BYAC 110", "BYAC 150", "BYAC 190", "BYAC 140", "BYAC 260"]

    zone_1_list, zone_3_list, zone_4_list = [], [], []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            lines = text.split("\n")
            if len(lines) > 1:
                line = lines[1][6:]  # Extract room ID
                line_prefix = line.split(" ")[0]

                loop_num = 2 if line not in special_cases else 1
                for _ in range(loop_num):
                    if line_prefix in zone_1_prefix:
                        zone_1_list.append(page)
                    if line_prefix in zone_3_prefix:
                        zone_3_list.append(page)
                    if line_prefix in zone_4_prefix:
                        zone_4_list.append(page)

    for page in zone_1_list + zone_3_list + zone_4_list:
        merged_pdf.add_page(page)

    return merged_pdf

st.title("PDF Processor")
uploaded_file = st.file_uploader("Upload a PDF", type="pdf")

if uploaded_file:
    processed_pdf = extract_text(uploaded_file)
    output_filename = "Processed_PDF.pdf"

    with open(output_filename, "wb") as output_file:
        processed_pdf.write(output_file)

    with open(output_filename, "rb") as output_file:
        st.download_button("Download Processed PDF", output_file, file_name=output_filename, mime="application/pdf")
