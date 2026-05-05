# SmartCSV - EDI Field Extractor

A modern web application for extracting EDI field descriptions from PDF specification documents and generating Excel/CSV output files.

## 🌟 Features

- **Lightning Fast** - Process EDI specification PDFs in seconds
- **Smart Extraction** - Automatically detects EDI format (850, 810, 856) and expands N1 segments
- **Dual Output** - Generates both Excel (.xlsx) and CSV (.csv) files with dynamic column widths
- **Modern Web UI** - Beautiful, responsive React-based interface with drag & drop
- **Field Analysis** - Visual dashboard showing extracted field statistics and types

## 📋 Supported EDI Formats

| Format | Name | N1 Codes |
|--------|------|----------|
| **850** | Purchase Order | BT, ST, SU, VN (4 codes) |
| **810** | Invoice | BT, II, RE, ST, VN (5 codes) |
| **856** | Ship Notice/Manifest | ST, VN, SF (3 codes) |

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Modern web browser (Chrome, Firefox, Safari, Edge)

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Start the backend server:**
```bash
python app.py
```
Server will start on `http://localhost:5001`

3. **Open the web interface:**
- Simply open `index.html` in your browser
- Or use: `file:///Users/rangampetasairam/Downloads/SmartCSV UI/index.html`

### Alternative Startup

**macOS/Linux:**
```bash
./start_web.sh
```

**Windows:**
```batch
start_web.bat
```

## 💻 Usage

1. **Upload PDF** - Drag and drop your EDI specification PDF or click "Browse Files"
2. **Process** - Click "Process PDF" and wait a few seconds
3. **View Results** - See extracted fields, N1 codes, and field analysis
4. **Download** - Click "Download Excel" or "Download CSV"

## 📊 Output Format

### Excel Output (.xlsx)
- **Row 1**: Field descriptions (centered headers with gray background)
- **Row 2**: Field codes (e.g., [BIG01], [N101_BT], [N102_BT])
- **Dynamic column widths**: Auto-adjusted to content
- **N1 Expansion**: Separate columns for each entity code

### CSV Output (.csv)
- Same structure as Excel
- Compatible with all spreadsheet applications
- Easy to import into databases

## 🎨 UI Features

- **Purple gradient header** with clean typography
- **Feature cards** showcasing project capabilities
- **Drag & drop** file upload with visual feedback
- **Real-time processing** with loading indicators
- **Field analysis dashboard** with statistics
- **Responsive design** works on all devices
- **Cool footer** with gradient text and stats

## 📁 Project Structure

```
SmartCSV UI/
├── app.py              # Flask backend server
├── smartcsv_ui.py      # Core PDF processing logic
├── index.html          # React web interface
├── requirements.txt    # Python dependencies
├── start_web.sh        # Linux/Mac startup script
├── start_web.bat       # Windows startup script
├── WEB_README.md       # Detailed web app documentation
└── README.md           # This file
```

## 🔧 API Endpoints

**Base URL:** `http://localhost:5001/api`

- `GET /health` - Health check
- `POST /process` - Process PDF file (multipart/form-data)
- `GET /download/<filename>` - Download generated file
- `GET /supported-formats` - Get supported EDI formats info

## 🐛 Troubleshooting

### Backend Issues

**Port 5001 already in use:**
```bash
# On macOS, disable AirPlay Receiver:
# System Preferences → General → AirDrop & Handoff → Disable AirPlay Receiver
```

**Module not found:**
```bash
pip install -r requirements.txt
```

### Frontend Issues

**Network error:**
- Ensure backend is running: `python app.py`
- Check browser console for errors
- Verify API_BASE_URL in index.html matches backend port

## 🎯 Key Features Explained

### N1 Segment Expansion
Automatically creates separate columns for each N1 entity identifier code:
- **850**: BT (Bill-to-Party), ST (Ship To), SU (Supplier), VN (Vendor)
- **810**: BT, II (Issuer of Invoice), RE (Remittance Party), ST, VN
- **856**: ST (Ship To), VN (Vendor), SF (Ship From)

### Automatic Field Filtering
- Removes unwanted segments (ST, SE, CTT)
- Filters out qualifier fields
- Removes N302 (second address line)
- Keeps only relevant data fields

### Field Analysis Dashboard
After processing, displays:
- Total fields extracted
- Number of N1 codes
- Output formats available
- Extracted field types (segment names)

## 📝 Example Workflow

1. Start backend: `python app.py`
2. Open `index.html` in browser
3. Upload EDI 810 Invoice PDF
4. View results:
   - Document Type: EDI 810 (Invoice)
   - Total Fields: ~55 fields
   - N1 Codes: BT, II, RE, ST, VN
5. Download Excel and CSV files

## 🔒 Security Notes

For production deployment:
- Configure CORS properly in `app.py`
- Add file validation and size limits
- Use HTTPS with SSL certificates
- Implement authentication if needed
- Deploy behind reverse proxy (nginx/Apache)

## 📞 Support

For issues or questions:
- Check this README for solutions
- Review `WEB_README.md` for detailed documentation
- Check browser console for frontend errors
- Check terminal for backend errors

## 📄 License

Same as the original SmartCSV project.

---

**Made with ❤️ for efficient EDI field extraction**

**Version:** 2.0 (Web Application)
**Last Updated:** May 2026