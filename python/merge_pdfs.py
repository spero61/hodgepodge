# PyPDF2 docs: https://pypdf2.readthedocs.io/en/latest/
import PyPDF2, os, sys

# Usage: python merge_pdfs.py [filename]
if len(sys.argv) == 2:
    output_filename = sys.argv[1]
    if not output_filename.endswith(".pdf"):
        output_filename += ".pdf"
else:
    output_filename = "merged.pdf"

# key: filename, value: modification timestamp in Unix epoch time (in float)
pdf_files = {}
for filename in os.listdir("."):
    if filename.endswith(".pdf"):
        pdf_files[filename] = os.path.getmtime(filename)

# sort pdf_files by value (the time of last modification)
sorted_pdf_files = sorted(pdf_files.items(), key=lambda item: item[1])

# sorted_filenames: a list of pdf filenames (sorted by modification time ascending order)
sorted_filenames = []
for pdf_tuple in sorted_pdf_files:
    sorted_filenames.append(pdf_tuple[0])

# more merging options: https://pypdf2.readthedocs.io/en/latest/user/merging-pdfs.html
pdf_merger = PyPDF2.PdfMerger()

for pdf in sorted_filenames:
    pdf_merger.append(pdf)

pdf_merger.write(output_filename)
pdf_merger.close()
