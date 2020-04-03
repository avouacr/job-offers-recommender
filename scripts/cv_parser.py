
import os
import io

import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.pdfpage import PDFPage

cv_path = 'cv_fr_1p.pdf'


def cv_to_text(cv_path):
    """

    Sources :
    https://dzone.com/articles/exporting-data-from-pdfs-with-python
    https://gist.github.com/terencezl/61fe3f28c44a763dd1e9f060b8ff6f2e
    https://www.blog.pythonlibrary.org/2018/05/03/exporting-data-from-pdfs-with-python/

    :param cv_path:
    :return:
    """
    assert os.path.splitext(cv_path)[-1] == '.pdf', 'CV should be a pdf file.'

    # Perform layout analysis for all text
    laparams = pdfminer.layout.LAParams()
    setattr(laparams, 'all_texts', True)

    resource_manager = PDFResourceManager()
    retstr = io.StringIO()
    txt_converter = TextConverter(resource_manager, retstr, laparams=laparams)
    page_interpreter = PDFPageInterpreter(resource_manager, txt_converter)

    with open(cv_path, "rb") as fp:
        for page in PDFPage.get_pages(fp, check_extractable=True, caching=True):
            # Extract text from each page of the CV
            page_interpreter.process_page(page)
            text = retstr.getvalue()
            # Close open handles
            txt_converter.close()
            retstr.close()

    if text:
        return text