import os

import fitz
from libs.basic.file import pure_file_name

from gui import Message


def split_pdf(split_rules, pdf_file_path, out_dir):
    raw_file_name = pure_file_name(pdf_file_path)

    raw_pdf = fitz.Document(pdf_file_path)

    # 开始解析规则数据
    parsing_rules = []  # ((页码起,页码终), 页码名)
    if split_rules == "":
        for i, _ in enumerate(raw_pdf):
            parsing_rules.append((i + 1, i + 1))
    else:
        if "," in split_rules:
            split_rule_list = split_rules.split(',')
            for split_rule in split_rule_list:
                if "-" in split_rule:
                    page_range = split_rule.split("-")
                    parsing_rules.append(page_range)
                else:
                    parsing_rules.append((split_rule, split_rule))
        else:
            if "-" in split_rules:
                page_range = split_rules.split("-")
                parsing_rules.append(page_range)
            else:
                parsing_rules.append((split_rules, split_rules))

    # 根据规则写入文件
    Message.info(f"规则解析:{str(parsing_rules)}")
    Message.info(f"需生成:{len(parsing_rules)}个文件")

    for pages_range in parsing_rules:
        out_pdf = fitz.Document()
        pages_start = int(pages_range[0]) - 1
        pages_end = int(pages_range[1]) - 1
        out_pdf.insert_pdf(raw_pdf, from_page=pages_start, to_page=pages_end)
        file_name = f'{raw_file_name}-{pages_start + 1}-{pages_end + 1}.pdf'
        out_pdf_path = os.path.join(out_dir, file_name)
        out_pdf.save(out_pdf_path)
        Message.info(f'文件保存:{out_pdf_path}')
