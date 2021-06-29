from gui import Menu, OneFileSelect, FolderSelect, OutFolderSelect, Input

from features.pdf.merge_pdf import process as merge_pdf
from features.pdf.split_pdf import split_pdf as split_pdf

pdf_menu = Menu.add_cascade("PDF")

pdf_menu.add_command(
    name="合成PDF",
    description="合成指定文件夹中的所有PDF文件",
    components=[
        FolderSelect(button_text="PDF文件夹"),
        OutFolderSelect()
    ],
    run_func=merge_pdf
)

pdf_menu.add_command(
    name="拆分PDF",
    description="根据指定规则拆分PDF文件\n如:1,2-4,5 将文件拆分为3个文件\n默认一个页面拆分为单一文件",
    components=[
        Input(button_text="拆分规则", default_value=""),
        OneFileSelect(button_text="PDF文件", file_types="pdf"),
        OutFolderSelect(),
    ],
    run_func=split_pdf
)
