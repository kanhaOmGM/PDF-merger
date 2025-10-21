# PDF First Page Remover & Merger

A Python utility that removes the first page from multiple PDFs, filters out blank or "intentionally blank" pages, and merges them into a single document.

## Features

- **First Page Removal**: Automatically removes the first page from each PDF
- **Blank Page Detection**: Identifies and removes pages with minimal content (< 50 characters)
- **Intentional Blank Detection**: Removes pages marked as "intentionally blank" or similar variations
- **Batch Processing**: Processes all PDFs in a specified folder
- **Smart Merging**: Only includes PDFs that have content remaining after filtering
- **Safety Checks**: Skips single-page PDFs to prevent creating empty documents

## Requirements

```bash
pip install PyPDF2
```

## Usage

### Basic Usage

1. Update the folder path in the script:
```python
folder = r"C:\Users\YourName\Documents\YourFolder"
output = "merged_output.pdf"
remove_first_page_and_merge(folder, output)
```

2. Run the script:
```bash
python pdf_merger.py
```

### As a Module

```python
from pdf_merger import remove_first_page_and_merge

# Process all PDFs in a folder
remove_first_page_and_merge(
    folder_path="path/to/pdfs",
    final_output="merged_result.pdf"
)
```

## How It Works

1. **Scans** the specified folder for PDF files
2. **Processes** each PDF by:
   - Removing the first page
   - Filtering out blank pages (less than 50 characters)
   - Removing "intentionally blank" pages
3. **Merges** all processed PDFs into a single output file
4. **Cleans up** temporary files automatically

## Detection Patterns

The script identifies "intentionally blank" pages using these patterns:
- "intentionally blank"
- "this page is intentionally blank"
- "intentionally left blank"
- "page intentionally blank"

## Configuration

### Adjust Blank Page Threshold

Modify the character threshold in `is_blank_or_intentional()`:
```python
if len(text) < 50:  # Change this value
    return True
```

### Add Custom Patterns

Add patterns to detect specific page types:
```python
intentional_patterns = [
    r'your\s*custom\s*pattern',
    # existing patterns...
]
```

## Output

The script provides detailed console output:
```
Processing 10 PDFs...
Processing: document1.pdf
  - Removing blank/intentional page 3
  - Removed 1 blank/intentional page(s)
Processing: document2.pdf
  - Excluded from merge
...
Merging 8 modified PDFs...
Done! Merged file saved as: merged_output.pdf
Temporary files deleted.
```

## Error Handling

- **Single-page PDFs**: Skipped automatically (would become empty)
- **Empty results**: PDFs with no content after filtering are excluded from merge
- **Text extraction failures**: Pages are kept by default to prevent data loss

## Notes

- Original PDFs are never modified
- Temporary files are automatically deleted after merging
- PDFs are processed in alphabetical order
- The script is safe to run multiple times (overwrites output file)

## License

Free to use and modify.

## Contributing

Feel free to submit issues or pull requests for improvements.
