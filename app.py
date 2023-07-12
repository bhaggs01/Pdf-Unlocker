import pikepdf
import streamlit as st
from PyPDF2 import PdfMerger

st.markdown(""" 

""")
st.title("Play with PDF")


def main():
    option = st.selectbox(
        "working with PDFs",
        ('Unlock PDF', 'Merge PDF'),

    )
    if option == "Unlock PDF":
        uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()

            # st.write("filename: ", uploaded_file.name)
            pdf_pass = st.text_input("PDF Password")
        unlock = st.button("Unlock PDF")
        if unlock:
            pdf = pikepdf.open(uploaded_file, password=pdf_pass)
            pdf.save(uploaded_file.name)
            st.write("File Successfully Unlocked")
            with open(uploaded_file.name, 'rb') as f:
                PDFByte = f.read()
                st.download_button(label="Download",
                                   data=PDFByte,
                                   file_name=uploaded_file.name,
                                   mime='application/octet-stream')

    elif option == "Merge PDF":
        uploaded_files = st.file_uploader("Choose a PDF file", accept_multiple_files=True)
        for uploaded_file in uploaded_files:
            bytes_data = uploaded_file.read()
            st.write("filename: ", uploaded_file.name)
        merge = st.button("Merge")
        if merge:
            merger = PdfMerger()
            for pdf in uploaded_files:
                merger.append(pdf)
                merger.write("result.pdf")
            with open("result.pdf", 'rb') as f:
                PDFbyte = f.read()

            st.download_button(label="Download PDF",
                               data=PDFbyte,
                               file_name="result.pdf",
                               mime="application/octet-stream")


if __name__ == '__main__':
    main()
