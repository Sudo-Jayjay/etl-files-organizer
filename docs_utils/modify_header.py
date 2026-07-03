from docx import Document

def replace_right_header(filepath, new_text, output_path):
    doc = Document(filepath)

    for section in doc.sections:
        header = section.header

        for para in header.paragraphs:
            runs = para.runs

            if len(runs) < 2:
                continue  # No right-side content, skip

            # Keep Run 0 (\t), clear all runs after it
            for run in runs[1:]:
                run.text = ""

            # Place new text in Run 1
            runs[1].text = new_text

    doc.save(output_path)