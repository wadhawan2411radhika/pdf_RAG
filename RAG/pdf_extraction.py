from langchain_community.document_loaders import PyMuPDFLoader

def pdf_reader(path):
    loader = PyMuPDFLoader(path)
    docs = loader.load()
    return docs

def reformat_text(input_path, output_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()
    
    reformatted_text = ""
    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        if not stripped_line:
            continue  # Skip empty lines
        
        if i > 0 and len(reformatted_text) > 0 and not reformatted_text.endswith(('.','!','?')):  
            # Check if the previous line ended with a sentence-ending punctuation
            reformatted_text += " "  # Add a space instead of a newline
        else:
            reformatted_text += "\n"  # Add a newline for a new paragraph
        
        reformatted_text += stripped_line

    with open(output_path, 'w') as file:
        file.write(reformatted_text)

def save_pdf2text(docs, output_path):
    with open(output_path, 'w') as f:
        for doc in docs:
            f.write(doc.page_content)
            f.write('\n')  # Add a newline between pages for readability

def process_pdf(year):
    pdf_path = f'data/raw/{year}-annual-report_print.pdf'
    output_path = f'data/processed/{year}-annual-report.txt'

    input_path_txt = f'data/processed/{year}-annual-report.txt'
    output_path_txt = f'data/processed/{year}-annual-report-reformatted.txt'

    docs = pdf_reader(pdf_path)
    save_pdf2text(docs, output_path)
    reformat_text(input_path_txt, output_path_txt)

def main():
    process_pdf(2022)
    process_pdf(2023)

if __name__ == '__main__':
    main()

