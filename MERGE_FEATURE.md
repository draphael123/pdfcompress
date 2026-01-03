# 📑 PDF Merge Feature

Your PDF Compressor now includes a powerful **PDF Merge** feature that lets you combine up to 20 PDFs into a single document!

## ✨ Features

### **Upload Multiple PDFs**
- 📁 Select up to 20 PDF files at once
- 📂 Drag and drop multiple files
- ✅ Automatic PDF validation

### **Reorder Files**
- 🔄 Drag and drop to rearrange
- ⬆️ Move up button
- ⬇️ Move down button
- 🎯 Perfect order control

### **Manage Your Files**
- 👁️ Preview all selected files
- 🗑️ Remove unwanted files
- 📊 See file count (X / 20)
- 📏 View individual file sizes

### **Merge & Download**
- 🔗 One-click merge
- 📊 Progress tracking
- ⬇️ Download merged PDF
- 📈 See total merged size

---

## 🌐 Access the Merge Feature

### **Main Page:**
```
http://localhost:5000/merge-page
```

### **Deployed:**
```
Vercel: https://your-app.vercel.app/merge-page
Railway: https://your-app.railway.app/merge-page
```

### **From Other Pages:**
- Link on main compressor page
- Link on chunked upload page
- Direct navigation

---

## 🎯 How to Use

### **Step 1: Upload PDFs**
1. Click the upload area or drag & drop
2. Select multiple PDFs (hold Ctrl/Cmd)
3. Up to 20 files maximum
4. All files must be PDFs

### **Step 2: Arrange Order**
1. Files are numbered 1, 2, 3...
2. Drag and drop to reorder
3. Or use ⬆️⬇️ buttons
4. Order determines merge sequence

### **Step 3: Review**
- ✅ Check file names
- ✅ Verify order
- ✅ Remove any unwanted files
- ✅ See total file count

### **Step 4: Merge**
1. Click "🔗 Merge PDFs" button
2. Wait for processing
3. Progress bar shows status
4. Automatic completion

### **Step 5: Download**
1. See merge statistics
2. Click "⬇️ Download Merged PDF"
3. File downloads automatically
4. Original files are deleted (secure)

---

## 🎨 Visual Features

### **Colorful Interface**
- 🌈 Animated gradient background
- 🎨 Colorful buttons and elements
- ✨ Hover effects and animations
- 📱 Mobile responsive

### **File List**
- 🔢 Numbered badges (1, 2, 3...)
- 📄 File names displayed
- 📊 File sizes shown
- 🎯 Clear visual hierarchy

### **Progress Tracking**
- 📊 Animated progress bar
- 💙 Glowing cyan gradient
- ⚡ Real-time percentage
- ✅ Completion notification

---

## 🔧 Technical Details

### **Backend (Python/Flask)**
```python
@app.route('/merge', methods=['POST'])
def merge_pdfs():
    # Uses PyPDF2.PdfMerger
    # Combines multiple PDFs in order
    # Returns merged file
```

### **Merge Process**
1. Receives up to 20 PDF files
2. Validates each file is a PDF
3. Saves files temporarily
4. Uses PyPDF2.PdfMerger to combine
5. Writes merged PDF
6. Cleans up temporary files
7. Returns merged file info

### **File Handling**
- ✅ Secure filename handling
- ✅ Temporary file cleanup
- ✅ Auto-delete after download
- ✅ Error handling

---

## 📊 Limits & Specifications

| Feature | Limit |
|---------|-------|
| **Max Files** | 20 PDFs |
| **Min Files** | 2 PDFs |
| **File Types** | PDF only |
| **Max Size per File** | Platform dependent* |
| **Total Size** | Platform dependent* |

*Platform limits:
- **Vercel Free**: 4.5 MB per file
- **Vercel Pro**: 100 MB per file
- **Railway**: 200 MB per file
- **Local**: No limit

---

## 💡 Use Cases

### **Business**
- 📋 Combine multiple invoices
- 📊 Merge reports
- 📝 Compile contracts
- 📄 Consolidate documents

### **Academic**
- 📚 Combine research papers
- 📖 Merge study materials
- 📝 Compile assignments
- 🎓 Create course materials

### **Personal**
- 📸 Combine scanned documents
- 🎨 Merge portfolios
- 📄 Consolidate receipts
- 📋 Create compilations

---

## 🚀 Examples

### **Example 1: Monthly Reports**
```
Files:
1. January_Report.pdf
2. February_Report.pdf
3. March_Report.pdf

Result: merged_3_pdfs.pdf (Q1_Reports)
```

### **Example 2: Invoice Compilation**
```
Files:
1. Invoice_001.pdf
2. Invoice_002.pdf
3. Invoice_003.pdf
... (up to 20)

Result: merged_20_pdfs.pdf (All_Invoices)
```

### **Example 3: Research Papers**
```
Files:
1. Introduction.pdf
2. Literature_Review.pdf
3. Methodology.pdf
4. Results.pdf
5. Conclusion.pdf

Result: merged_5_pdfs.pdf (Complete_Research)
```

---

## 🎯 Tips & Best Practices

### **Ordering**
- 📝 Upload files in desired order
- 🔄 Or reorder after upload
- ✅ Verify order before merging
- 🎯 First file = first in output

### **File Names**
- 📄 Use descriptive names
- 🔢 Number files if needed (01_, 02_...)
- ✅ Keep names short for display
- 📝 Check spelling

### **Performance**
- ⚡ Smaller files merge faster
- 📊 20 files takes ~10-30 seconds
- 💾 Large files need more time
- 🚀 Railway handles large files better

### **Quality**
- ✅ Merge preserves original quality
- 📄 No compression during merge
- 🎨 All formatting maintained
- 📊 Exact copy of originals

---

## 🔗 Integration with Other Features

### **Compress then Merge**
1. Compress individual PDFs first
2. Then merge compressed files
3. Results in smaller merged file

### **Merge then Compress**
1. Merge all PDFs first
2. Then compress the merged file
3. Single large file to target size

### **Workflow Example**
```
Step 1: Merge 10 PDFs → merged.pdf (200 MB)
Step 2: Compress merged.pdf → compressed_merged.pdf (199 MB)
Result: All files in one, under size limit!
```

---

## 📱 Mobile Support

### **Fully Responsive**
- ✅ Works on phones
- ✅ Works on tablets
- ✅ Touch-friendly
- ✅ Swipe to reorder (on mobile)

### **Mobile Features**
- 📱 Tap to upload
- 👆 Touch to reorder
- 🗑️ Tap to remove
- ⬇️ Tap to download

---

## 🔐 Security & Privacy

### **File Handling**
- 🔒 Files stored temporarily
- 🗑️ Auto-deleted after download
- 🔐 Secure filename handling
- ✅ No permanent storage

### **Privacy**
- ❌ Files not logged
- ❌ No file content scanning
- ❌ No data collection
- ✅ Complete privacy

---

## 🆚 Comparison with Other Tools

| Feature | This Tool | Adobe Acrobat | Online Tools |
|---------|-----------|---------------|--------------|
| **Free** | ✅ Yes | ❌ $15/mo | ⚠️ Limited |
| **File Limit** | 20 files | Unlimited | 2-5 files |
| **Reordering** | ✅ Easy | ✅ Yes | ⚠️ Basic |
| **Privacy** | ✅ Local | ⚠️ Cloud | ❌ Stored |
| **Quality** | ✅ Perfect | ✅ Perfect | ⚠️ Varies |
| **Speed** | ⚡ Fast | ⚡ Fast | 🐌 Slow |

---

## 🎓 API Endpoint (for developers)

### **Merge PDFs**
```
POST /merge
Content-Type: multipart/form-data

Body:
files: [PDF file 1, PDF file 2, ...]

Response:
{
  "success": true,
  "filename": "merged_X_pdfs.pdf",
  "num_files": X,
  "total_size": "XX.XX MB"
}
```

---

## 🚧 Troubleshooting

### **"Maximum 20 files allowed"**
- Remove some files
- Merge in batches
- Combine outputs after

### **"File is not a PDF"**
- Verify file extension
- Convert to PDF first
- Remove non-PDF files

### **Merge takes too long**
- Large files need more time
- Wait for completion
- Try Railway for large files

### **Out of memory**
- Too many large files
- Try fewer files
- Use Railway (more memory)

---

## ✅ Summary

✨ **Merge up to 20 PDFs**  
🔄 **Drag & drop reordering**  
🗑️ **Easy file management**  
📊 **Progress tracking**  
⬇️ **One-click download**  
🎨 **Beautiful interface**  
📱 **Mobile friendly**  
🔒 **Secure & private**

---

## 🔗 Quick Links

**Access Merge Tool:**
- Local: http://localhost:5000/merge-page
- Deployed: https://your-app.vercel.app/merge-page

**Other Features:**
- Compressor: `/`
- Large Files: `/chunked`
- Merge: `/merge-page`

---

**Your PDF toolkit is now complete with merging functionality!** 🎉

Compress, merge, and manage your PDFs all in one place! 🚀

