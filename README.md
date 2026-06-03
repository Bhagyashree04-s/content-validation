# Content Validation QA Tool

A comprehensive Python-based tool for validating and comparing document content across multiple formats (PDF, Word, Images with OCR). The tool detects mismatched words, missing words, extra words, spacing differences, and structural variations.

## Features

- **Multi-Format Support**: Compare PDF vs PDF, PDF vs Word (.docx), PDF vs Images (with OCR)
- **Detailed Comparison**: Detect word mismatches, missing/extra words, spacing differences, and line-level variations
- **Flexible Matching**: Support both strict and normalized text comparison
- **Batch Processing**: Compare multiple files from folders
- **Page-Level Analysis**: Track mismatches by page number when available
- **Multiple Output Formats**: Generate reports in JSON and CSV
- **Comprehensive Reports**: Include file names, page numbers, mismatch types, expected/actual text, and positions

## Requirements

- Python 3.11 or higher
- pip (Python package manager)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Bhagyashree04-s/content-validation.git
cd content-validation
```

### 2. Create a Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Additional Setup (for OCR support)

For Tesseract OCR functionality, install Tesseract:

**Ubuntu/Debian:**
```bash
sudo apt-get install tesseract-ocr
```

**macOS:**
```bash
brew install tesseract
```

**Windows:**
Download and install from: https://github.com/UB-Mannheim/tesseract/wiki

## Project Structure

```
content-validation/
├── README.md
├── requirements.txt
├── config.yaml                 # Configuration file
├── main.py                     # CLI entry point
├── src/
│   ├── __init__.py
│   ├── extractors/             # Text extraction modules
│   │   ├── __init__.py
│   │   ├── base.py            # Base extractor class
│   │   ├── pdf_extractor.py   # PDF text extraction
│   │   ├── docx_extractor.py  # Word document extraction
│   │   └── image_extractor.py # Image OCR extraction
│   ├── normalizers/            # Text normalization
│   │   ├── __init__.py
│   │   └── text_normalizer.py # Text cleanup and normalization
│   ├── comparators/            # Comparison engines
│   │   ├── __init__.py
│   │   ├── base.py            # Base comparator class
│   │   ├── word_comparator.py # Word-level comparison
│   │   ├── spacing_comparator.py # Whitespace comparison
│   │   └── structural_comparator.py # Line and paragraph comparison
│   ├── reports/                # Report generation
│   │   ├── __init__.py
│   │   ├── base.py            # Base reporter class
│   │   ├── json_reporter.py   # JSON report generation
│   │   └── csv_reporter.py    # CSV report generation
│   └── utils/
│       ├── __init__.py
│       ├── logger.py          # Logging configuration
│       └── helpers.py         # Helper functions
├── tests/
│   ├── __init__.py
│   ├── test_extractors.py     # Tests for extractors
│   ├── test_normalizers.py    # Tests for normalizers
│   ├── test_comparators.py    # Tests for comparators
│   └── test_reports.py        # Tests for reporters
└── examples/
    ├── sample_config.py
    └── sample_usage.py
```

## Quick Start

### Basic Comparison (Command Line)

```bash
# Compare two PDF files
python main.py --source sample1.pdf --target sample2.pdf

# Compare PDF with Word document
python main.py --source sample.pdf --target sample.docx

# Compare PDF with Image (OCR)
python main.py --source sample.pdf --target sample_image.png

# Batch comparison from folders
python main.py --source-dir ./pdfs --target-dir ./docs --output-dir ./reports

# Strict comparison (case-sensitive, preserve spaces)
python main.py --source sample.pdf --target sample.docx --strict

# Ignore case and normalize spaces
python main.py --source sample.pdf --target sample.docx --ignore-case --normalize
```

### Programmatic Usage

```python
from src.extractors.pdf_extractor import PDFExtractor
from src.extractors.docx_extractor import DocxExtractor
from src.comparators.word_comparator import WordComparator
from src.reports.json_reporter import JsonReporter

# Extract text from PDF and Word files
pdf_extractor = PDFExtractor()
word_extractor = DocxExtractor()

pdf_content = pdf_extractor.extract('document.pdf')
word_content = word_extractor.extract('document.docx')

# Compare content
comparator = WordComparator()
mismatches = comparator.compare(pdf_content.content, word_content.content)

# Generate report
reporter = JsonReporter()
reporter.generate_report(mismatches, 'report.json')

print("Comparison complete. Report saved to report.json")
```

## Configuration

Edit `config.yaml` to customize comparison settings:

```yaml
comparison:
  ignore_case: false
  normalize_whitespace: false
  ignore_punctuation: false
  detect_page_changes: true

extraction:
  pdf_engine: "pdfplumber"  # or "pymupdf"
  ocr_language: "eng"
  ocr_timeout: 300

reporting:
  include_position: true
  include_context: true
  context_lines: 2

batch:
  file_extensions:
    - ".pdf"
    - ".docx"
    - ".png"
    - ".jpg"
    - ".tiff"
  max_workers: 4
```

## Output Report

Reports include detailed information:

```json
{
  "summary": {
    "source_file": "sample.pdf",
    "target_file": "sample.docx",
    "total_mismatches": 5,
    "word_mismatches": 3,
    "spacing_mismatches": 1,
    "structural_mismatches": 1,
    "missing_words": 2,
    "extra_words": 1,
    "similarity_score": 0.95,
    "comparison_time": 2.34
  },
  "mismatches": [
    {
      "type": "word_mismatch",
      "page": 1,
      "line": 5,
      "position": 15,
      "expected": "validation",
      "actual": "validation!",
      "context_expected": "Document validation is important",
      "context_actual": "Document validation! is important",
      "severity": "medium"
    }
  ]
}
```

## Command Line Options

```
usage: main.py [-h] [--source SOURCE] [--target TARGET] 
               [--source-dir SOURCE_DIR] [--target-dir TARGET_DIR]
               [--output OUTPUT] [--output-dir OUTPUT_DIR]
               [--config CONFIG] [--strict] [--ignore-case]
               [--normalize] [--ignore-punctuation] [--page-wise]
               [--format {json,csv,both}] [--verbose]

Content Validation QA Tool

optional arguments:
  -h, --help                    show this help message and exit
  --source SOURCE              Path to source file
  --target TARGET              Path to target file
  --source-dir SOURCE_DIR      Directory containing source files
  --target-dir TARGET_DIR      Directory containing target files
  --output OUTPUT              Output report file path
  --output-dir OUTPUT_DIR      Directory for batch output reports
  --config CONFIG              Configuration file path
  --strict                     Enable strict comparison (case-sensitive)
  --ignore-case                Ignore case differences
  --normalize                  Normalize whitespace
  --ignore-punctuation         Ignore punctuation
  --page-wise                  Perform page-by-page comparison
  --format {json,csv,both}    Output format (default: json)
  --verbose                    Enable verbose logging
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_extractors.py -v

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

## Examples

### Example 1: Compare Two PDFs

```bash
python main.py --source docs/report_v1.pdf --target docs/report_v2.pdf --format json --output results/comparison.json
```

### Example 2: Compare PDF and Word Document

```bash
python main.py --source docs/template.pdf --target docs/template.docx --ignore-case --format both
```

### Example 3: Batch Comparison

```bash
python main.py --source-dir ./source_pdfs --target-dir ./target_docs --output-dir ./reports --format csv
```

### Example 4: Strict Comparison with OCR

```bash
python main.py --source document.pdf --target scanned_page.png --strict --format json
```

## Troubleshooting

### OCR Not Working
- Ensure Tesseract is installed and in system PATH
- Check `pytesseract.pytesseract.pytesseract_path` if on Windows

### PDF Extraction Issues
- Try switching PDF engine: edit `config.yaml` or use `--config`
- Check if PDF is corrupted or password-protected

### Memory Issues with Large Files
- Process files in smaller batches
- Reduce `max_workers` in batch configuration

### Encoding Issues
- Ensure files are in UTF-8 encoding
- Check file integrity

## Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

MIT License - feel free to use and modify

## Support

For issues and questions:
- Open an issue on GitHub
- Check existing issues for solutions
- Review the documentation

## Changelog

### v1.0.0 (Initial Release)
- PDF extraction (PyMuPDF and pdfplumber support)
- Word document extraction
- Image OCR extraction
- Word-level comparison
- Spacing comparison
- Structural comparison
- JSON and CSV reporting
- CLI interface
- Batch processing
- Comprehensive test suite
