"""
SmartPLG Accelerator Web Application - Flask Backend
Handles PDF upload, processing, and file generation
Fixed: Using edi_extractor instead of smartcsv_ui to avoid tkinter dependency
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import tempfile
from pathlib import Path
from edi_extractor import EDIFieldExtractor
from csv_to_gentran_ddf import generate_ddf
import traceback

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = tempfile.gettempdir()
ALLOWED_EXTENSIONS = {'pdf', 'csv'}
MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'SmartCSV API is running'})


@app.route('/api/process', methods=['POST'])
def process_pdf():
    """
    Process uploaded PDF and return field mappings
    Returns JSON with field data and download links
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only PDF files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Process PDF
        extractor = EDIFieldExtractor(filepath)
        extractor.extract_text()
        field_mappings = extractor.parse_field_mappings()
        
        # Detect document type
        doc_type = 'Unknown'
        if '810' in filename.lower():
            doc_type = 'EDI 810 (Invoice)'
        elif '850' in filename.lower():
            doc_type = 'EDI 850 (Purchase Order)'
        elif '856' in filename.lower():
            doc_type = 'EDI 856 (Ship Notice/Manifest)'
        
        # Get N1 codes if available
        n1_codes = extractor.code_lists.get('N101', [])
        n1_info = [{'code': code, 'description': desc} for code, desc in n1_codes]
        
        # Generate output files
        output_base = filepath.rsplit('.', 1)[0] + '_output'
        excel_file = output_base + '.xlsx'
        csv_file = output_base + '.csv'
        
        extractor.generate_excel_file(field_mappings)
        
        # Prepare field data for frontend
        fields = [
            {
                'id': i,
                'description': desc,
                'code': code
            }
            for i, (desc, code) in enumerate(field_mappings, 1)
        ]
        
        # Prepare response
        response = {
            'success': True,
            'documentType': doc_type,
            'filename': filename,
            'totalFields': len(field_mappings),
            'n1Codes': n1_info,
            'fields': fields,
            'downloads': {
                'excel': f'/api/download/{os.path.basename(excel_file)}',
                'csv': f'/api/download/{os.path.basename(csv_file)}'
            }
        }
        
        return jsonify(response)
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error processing PDF: {error_trace}")
        return jsonify({
            'error': f'Error processing PDF: {str(e)}',
            'details': error_trace
        }), 500


@app.route('/api/download/<filename>', methods=['GET'])
def download_file(filename):
    """Download generated Excel or CSV file"""
    try:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        
        if not os.path.exists(filepath):
            return jsonify({'error': 'File not found'}), 404
        
        return send_file(
            filepath,
            as_attachment=True,
            download_name=filename
        )
    
    except Exception as e:
        return jsonify({'error': f'Error downloading file: {str(e)}'}), 500


@app.route('/api/supported-formats', methods=['GET'])
def supported_formats():
    """Return information about supported EDI formats"""
    formats = [
        {
            'code': '850',
            'name': 'Purchase Order',
            'description': 'EDI 850 Purchase Order transaction set',
            'n1Codes': ['BT (Bill-to-Party)', 'ST (Ship To)', 'SU (Supplier/Manufacturer)', 'VN (Vendor)']
        },
        {
            'code': '810',
            'name': 'Invoice',
            'description': 'EDI 810 Invoice transaction set',
            'n1Codes': ['BT (Bill-to-Party)', 'II (Issuer of Invoice)', 'RE (Remittance Party)', 'ST (Ship To)', 'VN (Vendor)']
        },
        {
            'code': '856',
            'name': 'Ship Notice/Manifest',
            'description': 'EDI 856 Advance Ship Notice transaction set',
            'n1Codes': ['ST (Ship To)', 'VN (Vendor)', 'SF (Ship From)']
        }
    ]
    
    return jsonify({'formats': formats})


@app.route('/api/upload-csv', methods=['POST'])
def upload_csv():
    """
    Upload CSV file for DDF generation
    Returns the filename for subsequent DDF generation
    """
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Validate file type
        if not file.filename.endswith('.csv'):
            return jsonify({'error': 'Invalid file type. Only CSV files are allowed'}), 400
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Read field count from CSV
        import csv
        with open(filepath, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            field_names = next(reader)
            field_count = len(field_names)
        
        response = {
            'success': True,
            'filename': filename,
            'fieldCount': field_count,
            'message': 'CSV file uploaded successfully'
        }
        
        return jsonify(response)
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error uploading CSV: {error_trace}")
        return jsonify({
            'error': f'Error uploading CSV: {str(e)}',
            'details': error_trace
        }), 500


@app.route('/api/generate-ddf', methods=['POST'])
def generate_ddf_file():
    """
    Generate DDF file from CSV
    Expects JSON with csvFilename and transactionName
    """
    try:
        data = request.get_json()
        
        if not data or 'csvFilename' not in data:
            return jsonify({'error': 'CSV filename is required'}), 400
        
        csv_filename = data['csvFilename']
        transaction_name = data.get('transactionName', 'CSVDATA')
        
        # Construct full path
        csv_path = os.path.join(app.config['UPLOAD_FOLDER'], csv_filename)
        
        if not os.path.exists(csv_path):
            return jsonify({'error': 'CSV file not found'}), 404
        
        # Generate DDF file
        ddf_path = generate_ddf(csv_path, transaction_name=transaction_name)
        ddf_filename = os.path.basename(ddf_path)
        
        # Read field count from CSV
        import csv
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            field_names = next(reader)
            field_count = len(field_names)
        
        response = {
            'success': True,
            'message': 'DDF file generated successfully',
            'ddfFilename': ddf_filename,
            'transactionName': transaction_name,
            'fieldCount': field_count,
            'download': f'/api/download/{ddf_filename}'
        }
        
        return jsonify(response)
    
    except Exception as e:
        error_trace = traceback.format_exc()
        print(f"Error generating DDF: {error_trace}")
        return jsonify({
            'error': f'Error generating DDF: {str(e)}',
            'details': error_trace
        }), 500


if __name__ == '__main__':
    # Get port from environment variable (Railway/Render) or default to 5001
    port = int(os.environ.get('PORT', 5001))
    
    print("=" * 60)
    print("SmartPLG Accelerator - Backend Server")
    print("=" * 60)
    print(f"Server starting on port {port}")
    print("API endpoints:")
    print("  - GET  /api/health              - Health check")
    print("  - POST /api/process             - Process PDF file")
    print("  - POST /api/upload-csv          - Upload CSV file")
    print("  - POST /api/generate-ddf        - Generate DDF from CSV")
    print("  - GET  /api/download/<filename> - Download generated file")
    print("  - GET  /api/supported-formats   - Get supported EDI formats")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=port)

# Made with Bob
