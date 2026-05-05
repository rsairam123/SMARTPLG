#!/usr/bin/env python3
"""
CSV to GENTRAN DDF Converter
Generates GENTRAN XML-based DDF files from CSV files for IBM Sterling Integrator
"""

import csv
import xml.etree.ElementTree as ET
from xml.dom import minidom
import argparse
from pathlib import Path
import re
import sys


def sanitize_field_name(name: str, seen_names: set) -> str:
    """
    Sanitize field name to be a valid identifier
    
    Args:
        name: Original field name from CSV
        seen_names: Set of already used names to avoid duplicates
    
    Returns:
        Sanitized field name
    """
    # Convert to uppercase and replace spaces with underscores
    sanitized = re.sub(r'[^A-Z0-9_]', '_', name.upper())
    
    # Remove consecutive underscores
    sanitized = re.sub(r'_+', '_', sanitized)
    
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    
    # Prefix with FIELD_ if name starts with digit or is empty
    if not sanitized or sanitized[0].isdigit():
        sanitized = 'FIELD_' + sanitized
    
    # Handle duplicates by appending _2, _3, etc.
    original = sanitized
    counter = 2
    while sanitized in seen_names:
        sanitized = f"{original}_{counter}"
        counter += 1
    
    seen_names.add(sanitized)
    return sanitized


def generate_ddf(csv_path: str, output_path: str = None, transaction_name: str = "CSVDATA") -> str:
    """
    Generate GENTRAN DDF file from CSV
    
    Args:
        csv_path: Path to input CSV file
        output_path: Path for output DDF file (default: same name with .ddf extension)
        transaction_name: Name for the transaction (default: "CSVDATA")
    
    Returns:
        Path to generated DDF file
    
    Raises:
        FileNotFoundError: If CSV file doesn't exist
        ValueError: If CSV file is empty or has no columns
    """
    csv_file = Path(csv_path)
    
    if not csv_file.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")
    
    # Read first row to get field names
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            field_names = next(reader)
        except StopIteration:
            raise ValueError("CSV file is empty")
    
    if not field_names:
        raise ValueError("CSV file has no columns")
    
    # Determine output path
    if output_path is None:
        output_path = csv_file.with_suffix('.ddf')
    
    # Create XML structure
    root = ET.Element('GENTRANDDF', VERSION="1.0")
    
    # Add EXTENDEDRULELIBRARIES (empty element)
    ET.SubElement(root, 'EXTENDEDRULELIBRARIES')
    
    # Add VARDELIMFILE
    vardelimfile = ET.SubElement(root, 'VARDELIMFILE',
                                 NAME=transaction_name,
                                 DESCRIPTION=f"{transaction_name} CSV File",
                                 NOTE="Auto-generated from CSV first row",
                                 ACTIVE="yes",
                                 FIELDDELIM="0x2c",  # comma
                                 QUOTECHAR="0x22")   # double quote
    
    # Add VARDELIMREC
    vardelimrec = ET.SubElement(vardelimfile, 'VARDELIMREC',
                                NAME="DATA",
                                DESCRIPTION="Data Record",
                                NOTE="",
                                ACTIVE="yes",
                                MINLOOP="1",
                                MAXLOOP="999999",
                                LOOPCONTROL="normal",
                                ORDERINGTAG="",
                                TAG="",
                                TAGFIELDNUM="65535",
                                FLOATING="no")
    
    # Add fields
    seen_names = set()
    for field_name in field_names:
        sanitized_name = sanitize_field_name(field_name, seen_names)
        
        ET.SubElement(vardelimrec, 'VARDELIMFIELD',
                     NAME=sanitized_name,
                     DESCRIPTION=field_name,
                     NOTE="",
                     ACTIVE="yes",
                     MANDATORY="no",
                     NOTUSED="no",
                     MINDATALEN="0",
                     MAXDATALEN="256",
                     TYPE="string",
                     FORMAT="")
    
    # Convert to pretty-printed XML
    xml_str = ET.tostring(root, encoding='unicode')
    
    # Parse and pretty print
    dom = minidom.parseString(xml_str)
    pretty_xml = dom.toprettyxml(indent="  ", encoding='UTF-8')
    
    # Add DOCTYPE after XML declaration
    doctype = b'<!DOCTYPE GENTRANDDF>\n'
    xml_lines = pretty_xml.split(b'\n')
    final_xml = xml_lines[0:1] + [doctype] + xml_lines[1:]
    
    # Write to file
    with open(output_path, 'wb') as f:
        f.write(b'\n'.join(final_xml))
    
    return str(output_path)


def main():
    """Main entry point for command-line usage"""
    parser = argparse.ArgumentParser(
        description='Generate GENTRAN XML-based DDF file from CSV',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.csv
  %(prog)s input.csv -n "EDI850"
  %(prog)s input.csv -o output.ddf -n "TRANSACTION"

The DDF file uses VARDELIMFILE format with:
  - FIELDDELIM: 0x2c (comma)
  - QUOTECHAR: 0x22 (double quote)
  - All fields as string type with 256 max length
        """
    )
    
    parser.add_argument('csv_file',
                       help='Path to input CSV file')
    
    parser.add_argument('-o', '--output',
                       help='Output DDF file path (default: same name with .ddf extension)')
    
    parser.add_argument('-n', '--name',
                       default='CSVDATA',
                       help='Transaction name (default: CSVDATA)')
    
    args = parser.parse_args()
    
    try:
        print(f"Reading CSV file: {args.csv_file}")
        
        # Read field count
        with open(args.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            field_names = next(reader)
            field_count = len(field_names)
        
        print(f"Found {field_count} fields")
        print(f"Transaction name: {args.name}")
        
        # Generate DDF
        output_file = generate_ddf(args.csv_file, args.output, args.name)
        
        print(f"\n✓ DDF file generated successfully!")
        print(f"Output: {output_file}")
        print(f"\nDDF Configuration:")
        print(f"  - Format: VARDELIMFILE (CSV)")
        print(f"  - Field delimiter: 0x2c (comma)")
        print(f"  - Quote character: 0x22 (double quote)")
        print(f"  - Fields: {field_count}")
        print(f"  - Record type: DATA")
        
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

# Made with Bob
