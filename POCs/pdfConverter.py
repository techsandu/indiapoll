import PyPDF2
import csv

def pdfConverter():
    print("pdf")
    with open("/Users/sandeep/Neta/POCs/2011.pdf",'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        text_data = []
        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text_data.append(page.extract_text())
    csv_file_name = 'output.csv'
    with open(csv_file_name,'w',newline='',encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        for line in text_data:
            csv_writer.writerow([line])
    print(f'PDF data has been successfully converted to {csv_file_name}')
if __name__ == '__main__':
    pdfConverter()