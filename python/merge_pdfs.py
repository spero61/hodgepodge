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

pdf_writer = PyPDF2.PdfFileWriter()

for filename in sorted_filenames:
    pdf_file_obj = open(filename, "rb")
    pdf_reader = PyPDF2.PdfFileReader(pdf_file_obj)

    # add all the pages to pdf_writer to merge pdf files in order
    for page_num in range(0, pdf_reader.numPages):
        page_obj = pdf_reader.getPage(page_num)
        pdf_writer.addPage(page_obj)

pdf_output = open(output_filename, "wb")
pdf_writer.write(pdf_output)
pdf_output.close()
