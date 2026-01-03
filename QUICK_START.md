# Quick Start Guide

## Your PDF Compressor is Ready! 🎉

The Flask server is currently running and ready to use.

### Access Your Application

Open your web browser and go to:

**http://localhost:5000**

or

**http://127.0.0.1:5000**

### How to Use

1. **Upload a PDF**
   - Click the upload area or drag and drop your PDF file
   - The file can be of any size

2. **Set Target Size** (Optional)
   - Default is 199MB
   - You can adjust this to any size you need

3. **Compress**
   - Click the "Compress PDF" button
   - Wait for the compression to complete
   - You'll see a progress bar during compression

4. **Download**
   - Once complete, you'll see compression statistics
   - Click "Download Compressed PDF" to save your file
   - The compressed file will be automatically downloaded

### Features Available

✅ **Drag & Drop Upload** - Simply drag your PDF onto the upload area
✅ **Real-time Progress** - See compression progress in real-time
✅ **Compression Stats** - View original size, compressed size, and space saved
✅ **Quality Preservation** - Advanced algorithms maintain PDF quality
✅ **Auto Cleanup** - Files are automatically deleted after download for privacy
✅ **Large File Support** - Handles PDFs up to 2GB

### Server Information

- **Status**: Running ✅
- **URL**: http://127.0.0.1:5000
- **Port**: 5000
- **Debug Mode**: Enabled (for development)

### To Stop the Server

Press `CTRL+C` in the terminal where the server is running.

### Troubleshooting

**Can't access the website?**
- Make sure the server is running (you should see "Running on http://127.0.0.1:5000")
- Check that no other application is using port 5000
- Try accessing http://127.0.0.1:5000 instead of localhost

**Upload fails?**
- Ensure the file is a valid PDF
- Check that the file size is under 2GB
- Verify you have enough disk space

**Compression takes too long?**
- Large PDFs (>500MB) may take several minutes
- The progress bar will show you the status
- Don't close the browser tab while compressing

### Next Steps

For production deployment, consider:
- Using a production WSGI server (like Gunicorn or uWSGI)
- Setting up HTTPS
- Configuring a reverse proxy (like Nginx)
- Increasing server resources for large files

Enjoy compressing your PDFs! 📄✨


