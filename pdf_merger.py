from PyPDF2 import PdfReader, PdfWriter, PdfMerger
import os
import re

def is_blank_or_intentional(page):
    """
    Checks if a page is blank or contains 'intentionally blank' text.
    Returns True if the page should be removed.
    """
    try:
        text = page.extract_text().strip().lower()
        
        # Check if page is essentially empty (very little text)
        if len(text) < 50:  # Adjust threshold as needed
            return True
        
        # Check for "intentionally blank" variations
        intentional_patterns = [
            r'intentionally\s*blank',
            r'this\s*page\s*is\s*intentionally\s*blank',
            r'intentionally\s*left\s*blank',
            r'page\s*intentionally\s*blank'
        ]
        
        for pattern in intentional_patterns:
            if re.search(pattern, text):
                return True
                
        return False
    except:
        # If text extraction fails, keep the page to be safe
        return False


def remove_first_page(input_pdf, temp_output):
    """
    Removes the first page from a PDF, filters out blank/intentional pages,
    and saves it as a temporary file.
    Only processes PDFs with 2+ pages.
    """
    reader = PdfReader(input_pdf)
    
    # Skip PDFs with only 1 page (they would become empty)
    if len(reader.pages) <= 1:
        print(f"Skipping '{os.path.basename(input_pdf)}' - only 1 page")
        return False

    writer = PdfWriter()
    pages_added = 0
    blank_pages_removed = 0

    # Skip the first page (index 0) and filter remaining pages
    for page_num in range(1, len(reader.pages)):
        page = reader.pages[page_num]
        
        if is_blank_or_intentional(page):
            blank_pages_removed += 1
            print(f"  - Removing blank/intentional page {page_num + 1}")
        else:
            writer.add_page(page)
            pages_added += 1

    # Don't save if no pages remain after filtering
    if pages_added == 0:
        print(f"  - No content pages remaining after filtering")
        return False

    # Save the trimmed PDF
    with open(temp_output, "wb") as f:
        writer.write(f)
    
    if blank_pages_removed > 0:
        print(f"  - Removed {blank_pages_removed} blank/intentional page(s)")
    
    return True


def remove_first_page_and_merge(folder_path, final_output="merged_no_first_pages.pdf"):
    """
    Removes the first page from every PDF in the given folder,
    filters out blank and 'intentionally blank' pages,
    then merges all the trimmed PDFs into a single PDF.
    Only includes PDFs that actually have content after removal.
    """
    merger = PdfMerger()
    pdf_files = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")])

    if not pdf_files:
        print("No PDF files found in the folder.")
        return

    print(f"Processing {len(pdf_files)} PDFs...")

    temp_files = []
    for pdf in pdf_files:
        input_path = os.path.join(folder_path, pdf)
        temp_path = os.path.join(folder_path, f"_temp_{pdf}")
        
        print(f"Processing: {pdf}")
        success = remove_first_page(input_path, temp_path)
        
        # Only add to merge list if successful (PDF had content after filtering)
        if success:
            temp_files.append(temp_path)
        else:
            print(f"  - Excluded from merge")

    if not temp_files:
        print("No valid PDFs to merge after processing.")
        return

    print(f"\nMerging {len(temp_files)} modified PDFs...")
    for temp_pdf in temp_files:
        merger.append(temp_pdf)

    merger.write(final_output)
    merger.close()

    print(f"Done! Merged file saved as: {final_output}")

    # Clean up temporary files
    for temp_pdf in temp_files:
        if os.path.exists(temp_pdf):
            os.remove(temp_pdf)
    print("Temporary files deleted.")


if __name__ == "__main__":
    folder = r"C:\Users\DELL\Documents\ZIO"
    output = "merged_zio_trimmed.pdf"
    remove_first_page_and_merge(folder, output)