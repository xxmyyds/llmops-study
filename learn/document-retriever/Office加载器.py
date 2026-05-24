# -*- coding: utf-8 -*-
# @Author  : xxmyyds
# @Time    : 2026/5/4 14:00
# @FileName: Office加载器.py
from langchain_community.document_loaders import UnstructuredExcelLoader, UnstructuredWordDocumentLoader, \
    UnstructuredPowerPointLoader

excel_loader = UnstructuredExcelLoader('../../study/Document组件的使用/员工考勤表.xlsx')

excel_documents = excel_loader.load()
print(excel_documents)
print(len(excel_documents))
print(excel_documents[0].metadata)

word_loader = UnstructuredWordDocumentLoader('../../study/Document组件的使用/喵喵.docx')

word_documents = word_loader.load()
print(word_documents)
print(len(word_documents))
print(word_documents[0].metadata)

ppt_loader = UnstructuredPowerPointLoader('../../study/Document组件的使用/章节介绍.pptx')
ppt_documents = ppt_loader.load()
print(ppt_documents)
print(len(ppt_documents))
print(ppt_documents[0].metadata)
