import os
import uuid

import fitz
from libs.basic.file import files_in_folder, file_extension

from gui import Message, RunTimeData


def process(pdf_dir, out_dir):
    """合并pdf"""
    out_pdf = fitz.Document()
    files_path = files_in_folder(pdf_dir, filter_extend=['pdf'])
    for file_path in files_path:
        Message.info(f'开始提取:{file_path}')
        with fitz.Document(file_path) as now_pdf:
            out_pdf.insert_pdf(now_pdf)

    out_pdf_path = os.path.join(out_dir, f"PDF合并文件-{uuid.uuid1()}.pdf")
    out_pdf.save(out_pdf_path)
