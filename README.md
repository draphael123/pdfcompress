# PDF Compressor Website

A beautiful and functional web application that compresses PDF files of any size down to a target size (default: 199MB) without major quality decline.

## Features

- 🚀 **Handle Any Size PDF**: Upload and compress PDFs of any size
- 🎯 **Customizable Target Size**: Set your desired output size (default: 199MB)
- 🎨 **Beautiful Modern UI**: Drag-and-drop interface with real-time progress
- 💾 **Quality Preservation**: Uses advanced compression algorithms to maintain quality
- 🔒 **Privacy First**: Files are automatically deleted after download
- 📊 **Compression Stats**: See original size, compressed size, and space saved

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Setup

1. Install the required Python packages:

```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask server:

```bash
python app.py
```

2. Open your web browser and navigate to:

```
http://localhost:5000
```

3. Use the application:
   - Click the upload area or drag and drop a PDF file
   - Optionally adjust the target size (default is 199MB)
   - Click "Compress PDF"
   - Wait for the compression to complete
   - Download your compressed PDF

## How It Works

The application uses two powerful PDF processing libraries:

1. **pikepdf**: Primary compression engine that preserves quality while reducing file size
2. **PyPDF2**: Fallback compression for additional file size reduction

The compression algorithm:
- Analyzes the original file size
- Calculates the required compression ratio
- Applies object stream compression
- Compresses content streams
- Adjusts quality settings based on target size
- Iteratively compresses until target is reached

## Technical Details

### Backend (Python/Flask)

- **Framework**: Flask 3.0.0
- **PDF Libraries**: PyPDF2, pikepdf
- **Max Upload Size**: 2GB (configurable)
- **File Storage**: Temporary uploads folder (auto-cleanup)

### Frontend

- **Pure HTML/CSS/JavaScript**: No frameworks required
- **Drag & Drop**: Modern file upload interface
- **Real-time Progress**: Visual feedback during compression
- **Responsive Design**: Works on desktop and mobile

## File Structure

```
PDF Compression/
├── app.py                  # Flask backend server
├── requirements.txt        # Python dependencies
├── templates/
│   └── index.html         # Frontend HTML/CSS/JS
├── temp_uploads/          # Temporary file storage (auto-created)
└── README.md              # This file
```

## Configuration

You can customize the application by modifying these settings in `app.py`:

- `MAX_CONTENT_LENGTH`: Maximum upload file size (default: 2GB)
- `UPLOAD_FOLDER`: Directory for temporary file storage
- Default target size in the frontend (199MB)

## Security Notes

- Files are stored temporarily and deleted after download
- Secure filename handling prevents directory traversal
- File type validation ensures only PDFs are processed
- Maximum upload size prevents resource exhaustion

## Troubleshooting

### "Compression failed" error

- Ensure the PDF is not corrupted
- Try a smaller target size
- Check that you have enough disk space

### Server won't start

- Verify Python 3.8+ is installed
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 5000 is available

### Upload fails

- Check file is a valid PDF
- Ensure file size is under 2GB
- Verify you have write permissions in the project directory

## Future Enhancements

- Batch processing multiple PDFs
- Cloud storage integration
- Advanced compression options
- Password-protected PDF support
- Page range selection

## License

This project is open source and available for personal and commercial use.

## Support

For issues, questions, or suggestions, please create an issue in the project repository.


