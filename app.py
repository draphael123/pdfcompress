import os
import io
from flask import Flask, render_template, request, send_file, jsonify
from werkzeug.utils import secure_filename
import PyPDF2

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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

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

@app.route('/chunked')
def index_chunked():
    """Route for chunked upload version (handles large files)"""
    return render_template('index_chunked.html')

@app.route('/upload-chunk', methods=['POST'])
def upload_chunk():
    """Handle chunked file uploads for large PDFs"""
    try:
        chunk = request.files.get('chunk')
        chunk_index = int(request.form.get('chunkIndex'))
        total_chunks = int(request.form.get('totalChunks'))
        upload_id = request.form.get('uploadId')
        file_name = request.form.get('fileName')
        
        if not all([chunk, upload_id, file_name]):
            return jsonify({'error': 'Missing required fields'}), 400
        
        # Create directory for this upload
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], upload_id)
        os.makedirs(upload_dir, exist_ok=True)
        
        # Save chunk
        chunk_path = os.path.join(upload_dir, f'chunk_{chunk_index}')
        chunk.save(chunk_path)
        
        # Save metadata
        metadata_path = os.path.join(upload_dir, 'metadata.txt')
        with open(metadata_path, 'w') as f:
            f.write(f'{file_name}\n{total_chunks}\n')
        
        return jsonify({
            'success': True,
            'chunk_index': chunk_index,
            'total_chunks': total_chunks
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/compress-chunks', methods=['POST'])
def compress_chunks():
    """Reassemble chunks and compress the PDF"""
    try:
        data = request.get_json()
        upload_id = data.get('uploadId')
        target_size = float(data.get('target_size', 199))
        
        if not upload_id:
            return jsonify({'error': 'Upload ID required'}), 400
        
        upload_dir = os.path.join(app.config['UPLOAD_FOLDER'], upload_id)
        
        if not os.path.exists(upload_dir):
            return jsonify({'error': 'Upload not found'}), 404
        
        # Read metadata
        metadata_path = os.path.join(upload_dir, 'metadata.txt')
        with open(metadata_path, 'r') as f:
            lines = f.readlines()
            original_filename = lines[0].strip()
            total_chunks = int(lines[1].strip())
        
        # Reassemble file
        assembled_path = os.path.join(app.config['UPLOAD_FOLDER'], f'assembled_{upload_id}.pdf')
        
        with open(assembled_path, 'wb') as outfile:
            for i in range(total_chunks):
                chunk_path = os.path.join(upload_dir, f'chunk_{i}')
                if not os.path.exists(chunk_path):
                    return jsonify({'error': f'Missing chunk {i}'}), 500
                
                with open(chunk_path, 'rb') as infile:
                    outfile.write(infile.read())
        
        # Get original size
        original_size = get_file_size_mb(assembled_path)
        
        # Compress the assembled PDF
        output_filename = f"compressed_{original_filename}"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        compressed_size = compress_pdf_iterative(assembled_path, output_path, target_size)
        
        # Calculate compression percentage
        compression_percent = ((original_size - compressed_size) / original_size) * 100
        
        # Clean up chunks
        import shutil
        shutil.rmtree(upload_dir)
        os.remove(assembled_path)
        
        return jsonify({
            'success': True,
            'filename': output_filename,
            'original_size': f"{original_size:.2f}",
            'compressed_size': f"{compressed_size:.2f}",
            'compression_percent': f"{compression_percent:.1f}"
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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

