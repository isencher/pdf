# Import required library
from PyPDF2 import PdfReader, PdfWriter
import os
from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['OUTPUT_FOLDER'] = 'output'

# 确保上传和输出目录存在
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['OUTPUT_FOLDER'], exist_ok=True)

def split_pdf(pdf_path, pages, output_dir):
    """
    Split a PDF file into multiple files based on specified page numbers.

    Args:
        pdf_path (str): The path to the PDF file to split.
        pages (int): The number of pages in each sub-pdffile
        output_dir (str): The directory to save the split PDF files.

    Returns:
        None

    """

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Open the PDF file
    pdf = PdfReader(pdf_path)
    total_pages = len(pdf.pages)

    # Calculate number of output files needed
    num_files = (total_pages + pages - 1) // pages

    # Split the PDF into multiple files
    for i in range(num_files):
        writer = PdfWriter()
        
        # Calculate start and end pages for this split
        start_page = i * pages
        end_page = min((i + 1) * pages, total_pages)
        
        # Add pages to the writer
        for page_num in range(start_page, end_page):
            writer.add_page(pdf.pages[page_num])
            
        # Save the split PDF
        output_path = os.path.join(output_dir, f'split_{i+1}.pdf')
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)

def merge_pdfs(pdf_paths, output_path):
    """
    Merge multiple PDF files into a single PDF file.

    Args:
        pdf_paths (list): A list of paths to the PDF files to merge.
        output_path (str): The path to save the merged PDF file.

    Returns:
        None    

    """
    # Create a PDF writer object
    writer = PdfWriter()

    # Add pages from each PDF file to the writer
    for pdf_path in pdf_paths:
        pdf = PdfReader(pdf_path)
        for page in pdf.pages:
            writer.add_page(page)

    # Save the merged PDF
    with open(output_path, 'wb') as output_file:
        writer.write(output_file)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/split', methods=['POST'])
def split():
    if 'pdf_file' not in request.files:
        return 'No file uploaded', 400
    
    file = request.files['pdf_file']
    pages_per_split = int(request.form['pages'])
    
    if file.filename == '':
        return 'No file selected', 400
    
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    output_dir = os.path.join(app.config['OUTPUT_FOLDER'], 'split_' + filename.rsplit('.', 1)[0])
    split_pdf(filepath, pages_per_split, output_dir)
    
    # 清理上传的文件
    os.remove(filepath)
    return 'PDF split successfully', 200

@app.route('/merge', methods=['POST'])
def merge():
    if 'pdf_files' not in request.files:
        return 'No files uploaded', 400
    
    files = request.files.getlist('pdf_files')
    if not files or files[0].filename == '':
        return 'No files selected', 400
    
    # 保存上传的文件
    filepaths = []
    for file in files:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        filepaths.append(filepath)
    
    # 合并PDF
    output_path = os.path.join(app.config['OUTPUT_FOLDER'], 'merged.pdf')
    merge_pdfs(filepaths, output_path)
    
    # 清理上传的文件
    for filepath in filepaths:
        os.remove(filepath)
    
    return send_file(output_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
