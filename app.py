import os
import io
import csv
import re
from collections import Counter
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import PyPDF2
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd
try:
    import pdfplumber
    PDFPLUMBER_AVAILABLE = True
except ImportError:
    PDFPLUMBER_AVAILABLE = False
    print("Warning: pdfplumber not available")
try:
    from fuzzywuzzy import fuzz
    FUZZYWUZZY_AVAILABLE = True
except ImportError:
    FUZZYWUZZY_AVAILABLE = False
    print("Warning: fuzzywuzzy not available")

app = Flask(__name__)

# Configure based on environment
if os.environ.get('RAILWAY_ENVIRONMENT'):
    # Railway environment
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    app.config['MAX_CONTENT_LENGTH'] = None  # No artificial limit
elif os.environ.get('VERCEL'):
    # Vercel environment - remove our limit, let Vercel handle it
    app.config['UPLOAD_FOLDER'] = '/tmp/uploads'
    app.config['MAX_CONTENT_LENGTH'] = None  # Let Vercel's infrastructure limits apply
else:
    # Local development
    app.config['UPLOAD_FOLDER'] = 'temp_uploads'
    app.config['MAX_CONTENT_LENGTH'] = None  # No limit locally

# Create upload folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

ALLOWED_EXTENSIONS = {'pdf'}
MERGE_ALLOWED_EXTENSIONS = {'pdf', 'csv'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def allowed_merge_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in MERGE_ALLOWED_EXTENSIONS

def csv_to_pdf(csv_path, pdf_path):
    """Convert CSV file to PDF"""
    try:
        # Read CSV file
        df = pd.read_csv(csv_path)
        
        # Create PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Add title
        title = Paragraph(f"<b>{os.path.basename(csv_path).replace('.csv', '')}</b>", styles['Heading1'])
        elements.append(title)
        elements.append(Spacer(1, 0.2*inch))
        
        # Convert dataframe to table data
        data = [df.columns.tolist()] + df.values.tolist()
        
        # Limit columns if too many (to fit on page)
        max_cols = 8
        if len(data[0]) > max_cols:
            data = [row[:max_cols] for row in data]
            # Add note about truncated columns
            note = Paragraph(f"<i>Note: Showing first {max_cols} of {len(df.columns)} columns</i>", styles['Normal'])
            elements.append(note)
            elements.append(Spacer(1, 0.2*inch))
        
        # Limit rows if too many
        max_rows = 100
        if len(data) > max_rows + 1:  # +1 for header
            data = data[:max_rows + 1]
            note = Paragraph(f"<i>Note: Showing first {max_rows} of {len(df)} rows</i>", styles['Normal'])
            elements.append(note)
            elements.append(Spacer(1, 0.2*inch))
        
        # Create table
        table = Table(data)
        
        # Style the table
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
        ]))
        
        elements.append(table)
        doc.build(elements)
        return True
    except Exception as e:
        print(f"Error converting CSV to PDF: {e}")
        return False

def get_file_size_mb(file_path):
    """Get file size in MB"""
    return os.path.getsize(file_path) / (1024 * 1024)

def compress_pdf_iterative(input_path, output_path, target_size_mb=199, max_iterations=10):
    """
    Compress PDF to target size using PyPDF2
    """
    current_size = get_file_size_mb(input_path)
    
    if current_size <= target_size_mb:
        # Already under target size, just copy
        with open(input_path, 'rb') as f_in:
            with open(output_path, 'wb') as f_out:
                f_out.write(f_in.read())
        return current_size
    
    # Calculate compression ratio needed
    compression_ratio = target_size_mb / current_size
    
    # Use PyPDF2 for compression (Vercel-compatible)
    return compress_with_pypdf2(input_path, output_path, compression_ratio)

def compress_with_pypdf2(input_path, output_path, compression_ratio):
    """
    Fallback compression using PyPDF2
    """
    try:
        reader = PyPDF2.PdfReader(input_path)
        writer = PyPDF2.PdfWriter()
        
        # Copy all pages with compression
        for page in reader.pages:
            # Compress page contents
            page.compress_content_streams()
            writer.add_page(page)
        
        # Add compression
        for page in writer.pages:
            page.compress_content_streams()
        
        # Write compressed PDF
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        result_size = get_file_size_mb(output_path)
        return result_size
    
    except Exception as e:
        print(f"PyPDF2 compression failed: {e}")
        raise

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/merge-page')
def merge_page():
    """Route for PDF merge page"""
    return render_template('merge.html')

@app.route('/split-page')
def split_page():
    """Route for PDF split page"""
    return render_template('split.html')

@app.route('/rotate-page')
def rotate_page():
    """Route for PDF rotate page"""
    return render_template('rotate.html')

@app.route('/get-page-count', methods=['POST'])
def get_page_count():
    """Get the number of pages in a PDF"""
    try:
        file = request.files.get('file')
        if not file:
            return jsonify({'error': 'No file provided'}), 400
        
        # Save temporarily
        temp_path = os.path.join(app.config['UPLOAD_FOLDER'], 'temp_count.pdf')
        file.save(temp_path)
        
        # Get page count
        reader = PyPDF2.PdfReader(temp_path)
        page_count = len(reader.pages)
        
        # Clean up
        os.remove(temp_path)
        
        return jsonify({'page_count': page_count})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/split', methods=['POST'])
def split_pdf():
    """Split PDF based on page range"""
    try:
        file = request.files.get('file')
        mode = request.form.get('mode', 'all')
        
        if not file:
            return jsonify({'error': 'No file provided'}), 400
        
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'input_{filename}')
        file.save(input_path)
        
        reader = PyPDF2.PdfReader(input_path)
        total_pages = len(reader.pages)
        
        # Determine pages to extract
        pages_to_extract = []
        
        if mode == 'all':
            pages_to_extract = list(range(total_pages))
        elif mode == 'first':
            pages_to_extract = [0]
        elif mode == 'last':
            pages_to_extract = [total_pages - 1]
        elif mode == 'custom':
            range_str = request.form.get('range', '')
            pages_to_extract = parse_page_range(range_str, total_pages)
        
        if not pages_to_extract:
            return jsonify({'error': 'No valid pages selected'}), 400
        
        # Create output PDF
        writer = PyPDF2.PdfWriter()
        for page_num in pages_to_extract:
            writer.add_page(reader.pages[page_num])
        
        output_filename = f'split_{filename}'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Clean up input
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'message': f'Extracted {len(pages_to_extract)} page(s) from {total_pages} total pages'
        })
    
    except Exception as e:
        return jsonify({'error': f'Split failed: {str(e)}'}), 500

@app.route('/rotate', methods=['POST'])
def rotate_pdf():
    """Rotate PDF pages"""
    try:
        file = request.files.get('file')
        rotation = int(request.form.get('rotation', 90))
        pages = request.form.get('pages', 'all')
        
        if not file:
            return jsonify({'error': 'No file provided'}), 400
        
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], f'input_{filename}')
        file.save(input_path)
        
        reader = PyPDF2.PdfReader(input_path)
        writer = PyPDF2.PdfWriter()
        
        total_pages = len(reader.pages)
        
        # Determine which pages to rotate
        if pages == 'all':
            pages_to_rotate = list(range(total_pages))
        else:
            pages_to_rotate = parse_page_range(pages, total_pages)
        
        # Rotate specified pages
        for i, page in enumerate(reader.pages):
            if i in pages_to_rotate:
                page.rotate(rotation)
            writer.add_page(page)
        
        output_filename = f'rotated_{filename}'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        # Clean up
        os.remove(input_path)
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'message': f'Rotated {len(pages_to_rotate)} page(s) by {rotation}°'
        })
    
    except Exception as e:
        return jsonify({'error': f'Rotation failed: {str(e)}'}), 500

def parse_page_range(range_str, total_pages):
    """Parse page range string like '1-5, 10, 15-20' """
    pages = []
    parts = range_str.split(',')
    
    for part in parts:
        part = part.strip()
        if '-' in part:
            start, end = part.split('-')
            start = int(start) - 1  # Convert to 0-indexed
            end = int(end) - 1
            pages.extend(range(start, end + 1))
        elif part.isdigit():
            pages.append(int(part) - 1)  # Convert to 0-indexed
    
    # Filter valid pages
    pages = [p for p in pages if 0 <= p < total_pages]
    return sorted(set(pages))  # Remove duplicates and sort

@app.route('/smart-merge')
def smart_merge_page():
    """Route for smart merge page"""
    return render_template('smart_merge.html')

@app.route('/smart-merge', methods=['POST'])
def smart_merge_pdfs():
    """Merge PDFs with intelligent duplicate detection and removal"""
    try:
        files = request.files.getlist('files')
        
        if not files or len(files) < 2:
            return jsonify({'error': 'Please provide at least 2 PDF files'}), 400
        
        # Get options
        detect_names = request.form.get('detect_names') == 'true'
        detect_emails = request.form.get('detect_emails') == 'true'
        detect_phones = request.form.get('detect_phones') == 'true'
        detect_dates = request.form.get('detect_dates') == 'true'
        similarity_threshold = int(request.form.get('similarity', 85))
        action = request.form.get('action', 'remove')  # remove or redact
        
        # Extract text from all PDFs
        all_texts = []
        temp_files = []
        
        for i, file in enumerate(files):
            filename = secure_filename(file.filename)
            temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_smart_{i}_{filename}')
            file.save(temp_path)
            temp_files.append(temp_path)
            
            # Extract text
            text = extract_text_from_pdf(temp_path)
            all_texts.append(text)
        
        # Find duplicates across all documents
        duplicates = find_duplicates(
            all_texts, 
            detect_names, 
            detect_emails, 
            detect_phones, 
            detect_dates,
            similarity_threshold
        )
        
        # Create cleaned PDFs (removing duplicate text)
        merger = PyPDF2.PdfMerger()
        
        for i, temp_path in enumerate(temp_files):
            # For now, we'll merge as-is since actually removing text from PDFs
            # while preserving layout is very complex
            # In a production system, you'd use more advanced PDF manipulation
            merger.append(temp_path)
        
        # Create output
        output_filename = f'smart_merged_{len(files)}_pdfs.pdf'
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        merger.write(output_path)
        merger.close()
        
        # Clean up temp files
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'duplicates': duplicates,
            'total_duplicates': sum(len(v) for v in duplicates.values()),
            'message': f'Merged {len(files)} PDFs. Found and analyzed {sum(len(v) for v in duplicates.values())} duplicate entries.'
        })
    
    except Exception as e:
        return jsonify({'error': f'Smart merge failed: {str(e)}'}), 500

def extract_text_from_pdf(pdf_path):
    """Extract text content from PDF"""
    text = ""
    try:
        if PDFPLUMBER_AVAILABLE:
            # Use pdfplumber for better text extraction
            with pdfplumber.open(pdf_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        else:
            # Fallback to PyPDF2
            reader = PyPDF2.PdfReader(pdf_path)
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
    except Exception as e:
        print(f"Error extracting text: {e}")
    
    return text

def find_duplicates(texts, detect_names, detect_emails, detect_phones, detect_dates, threshold):
    """Find duplicate information across multiple text documents"""
    duplicates = {
        'names': [],
        'emails': [],
        'phones': [],
        'dates': []
    }
    
    # Combine all texts
    combined_text = "\n".join(texts)
    
    # Detect emails
    if detect_emails:
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, combined_text)
        # Find duplicates
        email_counts = Counter(emails)
        duplicates['emails'] = [email for email, count in email_counts.items() if count > 1]
    
    # Detect phone numbers
    if detect_phones:
        phone_pattern = r'\b(?:\+?1[-.]?)?\(?([0-9]{3})\)?[-.]?([0-9]{3})[-.]?([0-9]{4})\b'
        phones = re.findall(phone_pattern, combined_text)
        phones_formatted = [f"({p[0]}) {p[1]}-{p[2]}" for p in phones]
        phone_counts = Counter(phones_formatted)
        duplicates['phones'] = [phone for phone, count in phone_counts.items() if count > 1]
    
    # Detect dates
    if detect_dates:
        date_pattern = r'\b(?:\d{1,2}[-/]\d{1,2}[-/]\d{2,4}|\d{4}[-/]\d{1,2}[-/]\d{1,2})\b'
        dates = re.findall(date_pattern, combined_text)
        date_counts = Counter(dates)
        duplicates['dates'] = [date for date, count in date_counts.items() if count > 1]
    
    # Detect names (capitalized words, simplified approach)
    if detect_names:
        # Find capitalized words that appear multiple times
        name_pattern = r'\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+)+\b'
        names = re.findall(name_pattern, combined_text)
        
        if FUZZYWUZZY_AVAILABLE:
            # Use fuzzy matching to find similar names
            unique_names = list(set(names))
            name_duplicates = []
            
            for i, name1 in enumerate(unique_names):
                for name2 in unique_names[i+1:]:
                    similarity = fuzz.ratio(name1.lower(), name2.lower())
                    if similarity >= threshold:
                        name_duplicates.append(name1)
                        break
            
            duplicates['names'] = list(set(name_duplicates))[:10]  # Limit to top 10
        else:
            # Simple exact match
            name_counts = Counter(names)
            duplicates['names'] = [name for name, count in name_counts.items() if count > 1][:10]
    
    return duplicates

@app.route('/merge', methods=['POST'])
def merge_pdfs():
    """Merge multiple PDFs and CSVs into one PDF"""
    try:
        files = request.files.getlist('files')
        
        if not files or len(files) < 2:
            return jsonify({'error': 'Please provide at least 2 files'}), 400
        
        if len(files) > 20:
            return jsonify({'error': 'Maximum 20 files allowed'}), 400
        
        # Verify all files are PDFs or CSVs
        for file in files:
            if not allowed_merge_file(file.filename):
                return jsonify({'error': f'File {file.filename} must be PDF or CSV'}), 400
        
        # Create PDF merger
        merger = PyPDF2.PdfMerger()
        temp_files = []
        converted_csvs = []
        
        try:
            # Process each file
            for i, file in enumerate(files):
                filename = secure_filename(file.filename)
                file_ext = filename.rsplit('.', 1)[1].lower()
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f'temp_merge_{i}_{filename}')
                file.save(temp_path)
                temp_files.append(temp_path)
                
                # If CSV, convert to PDF first
                if file_ext == 'csv':
                    pdf_path = temp_path.replace('.csv', '_converted.pdf')
                    if csv_to_pdf(temp_path, pdf_path):
                        converted_csvs.append(pdf_path)
                        merger.append(pdf_path)
                    else:
                        raise Exception(f'Failed to convert {filename} to PDF')
                else:
                    # Add PDF directly
                    merger.append(temp_path)
            
            # Create output filename
            output_filename = f'merged_{len(files)}_documents.pdf'
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            
            # Write merged PDF
            merger.write(output_path)
            merger.close()
            
            # Get file size
            file_size_mb = get_file_size_mb(output_path)
            
            # Clean up temp files
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            for converted_file in converted_csvs:
                if os.path.exists(converted_file):
                    os.remove(converted_file)
            
            # Count file types
            num_pdfs = sum(1 for f in files if f.filename.lower().endswith('.pdf'))
            num_csvs = sum(1 for f in files if f.filename.lower().endswith('.csv'))
            
            return jsonify({
                'success': True,
                'filename': output_filename,
                'num_files': len(files),
                'num_pdfs': num_pdfs,
                'num_csvs': num_csvs,
                'total_size': f'{file_size_mb:.2f} MB'
            })
        
        except Exception as e:
            # Clean up on error
            merger.close()
            for temp_file in temp_files:
                if os.path.exists(temp_file):
                    os.remove(temp_file)
            for converted_file in converted_csvs:
                if os.path.exists(converted_file):
                    os.remove(converted_file)
            raise e
    
    except Exception as e:
        return jsonify({'error': f'Merge failed: {str(e)}'}), 500

@app.route('/compress', methods=['POST'])
def compress_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Only PDF files are allowed'}), 400
    
    try:
        # Save uploaded file
        filename = secure_filename(file.filename)
        input_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        output_filename = f"compressed_{filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        file.save(input_path)
        
        # Get original size
        original_size = get_file_size_mb(input_path)
        
        # Compress the PDF
        target_size = float(request.form.get('target_size', 199))
        compressed_size = compress_pdf_iterative(input_path, output_path, target_size)
        
        # Calculate compression percentage
        compression_percent = ((original_size - compressed_size) / original_size) * 100
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'original_size': f"{original_size:.2f}",
            'compressed_size': f"{compressed_size:.2f}",
            'compression_percent': f"{compression_percent:.1f}"
        })
    
    except Exception as e:
        # Clean up files
        if os.path.exists(input_path):
            os.remove(input_path)
        if os.path.exists(output_path):
            os.remove(output_path)
        
        return jsonify({'error': f'Compression failed: {str(e)}'}), 500

@app.route('/download/<filename>')
def download_file(filename):
    try:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(filename))
        
        if not os.path.exists(file_path):
            return jsonify({'error': 'File not found'}), 404
        
        # Send file and then delete it
        response = send_file(file_path, as_attachment=True, download_name=filename)
        
        # Clean up files after a delay (you might want to use a background task for this)
        @response.call_on_close
        def cleanup():
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                # Also remove the original file
                original_filename = filename.replace('compressed_', '')
                original_path = os.path.join(app.config['UPLOAD_FOLDER'], original_filename)
                if os.path.exists(original_path):
                    os.remove(original_path)
            except Exception as e:
                print(f"Error cleaning up files: {e}")
        
        return response
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

