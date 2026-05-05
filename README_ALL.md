# SmartPLG Accelerator

A professional tool for converting EDI PDF specifications to Excel templates and GENTRAN DDF files for IBM Sterling Integrator.

## 🚀 Features

### Core Capabilities
✨ **User-Friendly Interface**
- Clean, modern GUI with intuitive controls
- Browse and select PDF files easily
- Real-time progress tracking with detailed logging
- Professional appearance with modern styling

🎯 **Smart EDI Extraction**
- Automatically extracts EDI field descriptions and codes from PDF specifications
- Intelligent segment expansion (N1, N2, N3, N4 segments)
- Filters out qualifier fields automatically
- Supports multiple EDI formats (850, 810, and more)
- Handles conditional elements (M, O, C, X)

📊 **Excel Output**
- Two-row format: descriptions and codes
- Dynamic column widths that auto-adjust to content
- Professional formatting with bold headers and gray background
- Center-aligned codes for better readability
- Ready for data mapping and integration

🔧 **GENTRAN DDF Generation** (NEW!)
- Converts Excel templates to GENTRAN XML-based DDF files
- Compatible with IBM Sterling Integrator
- VARDELIMFILE format for CSV processing
- Configurable field delimiters and quote characters
- Automatic field name sanitization
- Handles duplicate field names intelligently

### Process Types
- **Inbound**: Generates Excel template only
- **Outbound**: Generates Excel template + CSV file + optional DDF file

## 📋 Quick Start

### Prerequisites

- Python 3.8 or higher
- PyPDF2 library
- openpyxl library

### Installation

1. **Install Python** from [python.org](https://www.python.org/downloads/)

2. **Install required libraries**:
```bash
pip install -r requirements.txt
```

Or install individually:
```bash
pip install PyPDF2 openpyxl
```

### Running the Application

**Windows:**
```bash
RUN_ACCELERATOR.bat
```

**Or run manually:**
```bash
python smartplg_accelerator.py
```

## 📖 How to Use

### Main Application

1. **Launch the Application**
   - Double-click `RUN_ACCELERATOR.bat` or run `python smartplg_accelerator.py`

2. **Select PDF File**
   - Click "Browse PDF..." button
   - Navigate to your EDI specification PDF
   - Select the file (e.g., `EDI850_4010_Spec.pdf`)

3. **Choose Output Location**
   - The application auto-suggests an output filename
   - Click "Choose Location..." to customize if needed

4. **Select Process Type**
   - **Inbound**: Excel template only
   - **Outbound**: Excel template + CSV file

5. **Enable DDF Generation** (Optional)
   - Check "Generate GENTRAN DDF file from Excel template"
   - Only available for Outbound process type

6. **Generate Files**
   - Click "Generate Files" button
   - Watch the progress in the log window
   - Success message will show all generated files

### Standalone DDF Converter

You can also convert existing CSV files to DDF format using the standalone script:

```bash
# Basic usage
python csv_to_gentran_ddf.py input.csv

# With custom transaction name
python csv_to_gentran_ddf.py input.csv -n "EDI850"

# With custom output path
python csv_to_gentran_ddf.py input.csv -o output.ddf -n "TRANSACTION"
```

**Command-line options:**
- `csv_file`: Path to input CSV file (required)
- `-o, --output`: Output DDF file path (optional, default: same name with .ddf extension)
- `-n, --name`: Transaction name (optional, default: "CSVDATA")

## 📁 Output Files

### Excel File (.xlsx)
**Row 1 (Descriptions):**
- Bold font (size 11)
- Gray background (#D3D3D3)
- Center-aligned
- Example: `Transaction Set Purpose Code | Purchase Order Type Code | Purchase Order Number`

**Row 2 (Codes):**
- Regular font (size 10)
- Center-aligned
- Example: `[BEG01] | [BEG02] | [BEG03]`

**Column Widths:**
- Automatically adjusted based on content length
- Minimum width of 12 characters
- Extra padding of 2 characters for readability

### CSV File (Outbound only)
- Same structure as Excel file
- Two rows: descriptions and codes
- Comma-delimited format
- UTF-8 encoding

### DDF File (Optional, Outbound only)
- GENTRAN XML-based format
- VARDELIMFILE configuration for CSV processing
- Field delimiter: 0x2c (comma)
- Quote character: 0x22 (double quote)
- All fields configured as string type with 256 max length
- Compatible with IBM Sterling Integrator

## 🔧 DDF File Structure

The generated DDF file follows this structure:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE GENTRANDDF>
<GENTRANDDF VERSION="1.0">
  <EXTENDEDRULELIBRARIES/>
  <VARDELIMFILE NAME="TRANSACTION_NAME" DESCRIPTION="..." ACTIVE="yes" 
                FIELDDELIM="0x2c" QUOTECHAR="0x22">
    <VARDELIMREC NAME="DATA" DESCRIPTION="Data Record" ACTIVE="yes" 
                 MINLOOP="1" MAXLOOP="999999">
      <VARDELIMFIELD NAME="FIELD_NAME" DESCRIPTION="Field Description" 
                     TYPE="string" MAXDATALEN="256" MANDATORY="no" ACTIVE="yes"/>
      <!-- More fields... -->
    </VARDELIMREC>
  </VARDELIMFILE>
</GENTRANDDF>
```

### DDF Configuration Details

| Attribute | Value | Description |
|-----------|-------|-------------|
| FIELDDELIM | 0x2c | Comma delimiter for CSV fields |
| QUOTECHAR | 0x22 | Double quote for fields with special characters |
| TYPE | string | All fields are string type |
| MAXDATALEN | 256 | Maximum field length |
| MANDATORY | no | All fields are optional |
| MINLOOP | 1 | Minimum record occurrences |
| MAXLOOP | 999999 | Maximum record occurrences |

### Field Name Sanitization

The DDF generator automatically sanitizes field names:
- Converts to uppercase
- Replaces spaces with underscores
- Removes special characters (keeps only A-Z, 0-9, _)
- Prefixes with "FIELD_" if name starts with digit
- Handles duplicates by appending _2, _3, etc.

**Examples:**
- "Transaction Set Code" → "TRANSACTION_SET_CODE"
- "Purchase Order #" → "PURCHASE_ORDER"
- "123 Field" → "FIELD_123"
- "Name" (duplicate) → "NAME_2"

## 🎯 Supported EDI Elements

The tool extracts elements from various EDI segments:

- **BEG** - Beginning Segment for Purchase Order
- **BIG** - Beginning Segment for Invoice
- **CUR** - Currency
- **ITD** - Terms of Sale/Deferred Terms
- **DTM** - Date/Time Reference
- **N9** - Reference Identification
- **MSG** - Message Text
- **N1** - Name (with intelligent expansion)
- **N2** - Additional Name Information
- **N3** - Address Information
- **N4** - Geographic Location
- **PER** - Administrative Communications Contact
- **PO1** - Baseline Item Data
- **LIN** - Item Identification
- **PID** - Product/Item Description
- **SCH** - Line Item Schedule
- **CTT** - Transaction Totals

## 🔍 Technical Details

### Extraction Logic

1. **PDF Text Extraction**: Uses PyPDF2 to extract text from PDF pages
2. **Content Detection**: Identifies "Element Summary" or "Data Element Summary" sections
3. **Code List Extraction**: Finds and extracts code lists for segment expansion
4. **Pattern Matching**: Uses regex patterns to match EDI element lines
5. **Segment Expansion**: Intelligently expands N1-N4 segments based on code lists
6. **Filtering**: Removes qualifier fields and duplicates
7. **Excel Generation**: Creates formatted Excel with dynamic column widths
8. **CSV Generation**: Optionally creates CSV file for outbound processing
9. **DDF Generation**: Optionally converts CSV to GENTRAN DDF format

### Element Code Formats

Supports various EDI element code formats:
- Standard: `BEG01` (3 letters + 2 digits)
- N-segment: `N101` (1 letter + 1 digit + 2 digits)
- Extended: `PO107` (2 letters + 1 digit + 2 digits)

### Requirement Indicators

- **M** - Mandatory
- **O** - Optional
- **C** - Conditional
- **X** - Conditional (situational)

## 🆚 Comparison with SmartCSV UI

| Feature | SmartPLG Accelerator | SmartCSV UI |
|---------|---------------------|-------------|
| Excel Output | ✅ | ✅ |
| CSV Output | ✅ | ✅ |
| DDF Generation | ✅ NEW! | ❌ |
| Segment Expansion | ✅ Enhanced | ✅ |
| Process Types | ✅ Inbound/Outbound | ✅ Inbound/Outbound |
| Standalone DDF Tool | ✅ | ❌ |
| UI Design | ✅ Modern | ✅ Modern |

## 🛠️ Troubleshooting

### Application Won't Start

**Problem**: Error message about Python not found
**Solution**: Install Python 3.8+ and ensure it's in your system PATH

### Missing Dependencies

**Problem**: Error about PyPDF2 or openpyxl module
**Solution**: Run `pip install -r requirements.txt`

### No Fields Extracted

**Problem**: Excel file is empty or has no fields
**Solution**:
- Verify the PDF is an EDI specification document
- Check that the PDF contains "Element Summary" or "Data Element Summary" sections
- Ensure the PDF is not password-protected or corrupted
- Supported formats: EDI 850 (Purchase Order) and EDI 810 (Invoice)

### DDF Generation Failed

**Problem**: DDF file not generated or contains errors
**Solution**:
- Ensure CSV file was generated successfully first
- Check that CSV file has valid field names in first row
- Verify CSV file is not empty
- Check log window for specific error messages

### Invalid Field Names in DDF

**Problem**: Field names in DDF are not as expected
**Solution**: Field names are automatically sanitized for compatibility. Original names are preserved in the DESCRIPTION attribute.

## 💡 Tips

### Tip 1: Output Location
The application suggests an output filename based on your PDF name. You can change it by clicking "Choose Location..."

### Tip 2: Log Window
The log window shows detailed information about extraction, including:
- Code lists found and expanded
- Number of fields extracted
- Files generated
- Any warnings or errors

### Tip 3: DDF Generation
DDF generation is only available for Outbound process type since it requires a CSV file as input.

### Tip 4: Batch Processing
To process multiple PDFs:
1. Process each file individually through the GUI
2. Or use the standalone `csv_to_gentran_ddf.py` script for batch DDF conversion

### Tip 5: Verify Output
After generation:
- Open Excel file to verify field extraction
- Check CSV file format if generated
- Validate DDF file structure if generated
- Review log window for any warnings

## 📚 Use Cases

### Use Case 1: EDI Integration Setup
1. Extract fields from EDI specification PDF
2. Generate Excel template for data mapping
3. Generate DDF file for Sterling Integrator configuration
4. Import DDF into Sterling Integrator
5. Use Excel template for mapping documentation

### Use Case 2: Data Migration
1. Extract fields from legacy EDI specification
2. Generate CSV template
3. Populate CSV with migration data
4. Generate DDF for new system
5. Import into target EDI platform

### Use Case 3: Documentation
1. Extract fields from EDI specification
2. Generate Excel template
3. Use as reference documentation
4. Share with business analysts and developers

## 🔐 System Requirements

- **OS**: Windows 10/11, macOS, Linux
- **Python**: 3.8 or higher
- **RAM**: 512 MB minimum
- **Disk**: 100 MB for application + space for output files
- **Dependencies**: PyPDF2, openpyxl

## 📄 License

This tool is provided as-is for EDI specification processing and GENTRAN DDF generation.

## 🆘 Support

For issues or questions:
1. Check the log window for detailed error messages
2. Verify your PDF file format
3. Ensure all dependencies are installed
4. Review this README for troubleshooting tips

## 📝 Version History

### v3.0.0 (Current) - SmartPLG Accelerator
- **NEW: GENTRAN DDF file generation** - Convert Excel/CSV to DDF format
- **NEW: Standalone DDF converter** - Command-line tool for batch processing
- **Enhanced UI** - Added DDF generation option
- **Improved logging** - More detailed progress information
- **Better error handling** - Clear error messages and recovery
- Support for both EDI 850 and 810 specifications
- Intelligent N1-N4 segment expansion
- Professional Excel formatting with dynamic column widths

### v2.0.0 - SmartCSV UI
- Excel output with dynamic column widths
- Professional formatting
- Support for EDI 850 and 810
- N1 segment expansion

### v1.0.0 - Initial Release
- Basic PDF to CSV conversion
- Simple field extraction

---

**Made with ❤️ for EDI professionals and integration specialists**