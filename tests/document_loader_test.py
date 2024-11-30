import os
import shutil
import unittest

from langchain_core.documents import Document

from document_loaders.pdf_loader import PdfLoader


class TestPdfLoader(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_load_documents_invalid_directory(self):
        loader = PdfLoader("/path/to/nonexistent/directory")
        with self.assertRaises(ValueError) as context:
            loader.load_documents()
        self.assertEqual(str(context.exception), "Invalid directory path")

    def test_load_documents_empty_directory(self):
        empty_dir = "empty_directory"
        os.makedirs(empty_dir, exist_ok=True)
        loader = PdfLoader(empty_dir)
        self.assertEqual(loader.load_documents(), [])
        shutil.rmtree(empty_dir)

    def test_load_documents_success(self):
        test_dir = "test_pdfs"
        os.makedirs(test_dir, exist_ok=True)

        # Create a simple PDF file
        pdf_path = os.path.join(test_dir, "test.pdf")
        with open(pdf_path, 'wb') as f:
            f.write(
                b'%PDF-1.0\n1 0 obj<</Type/Catalog/Pages 2 0 R>>endobj 2 0 obj<</Type/Pages/Kids[3 0 R]/Count '
                b'1>>endobj 3 0 obj<</Type/Page/MediaBox[0 0 3 3]>>endobj\nxref\n0 4\n0000000000 65535 f\n0000000010 '
                b'00000 n\n0000000053 00000 n\n0000000102 00000 n\ntrailer<</Size 4/Root 1 0 R>>\nstartxref\n149\n%EOF')

        pdf_loader = PdfLoader(test_dir)
        documents = pdf_loader.load_documents()

        self.assertIsInstance(documents, list)
        self.assertGreater(len(documents), 0)
        self.assertIsInstance(documents[0], Document)

        shutil.rmtree(test_dir)


if __name__ == '__main__':
    unittest.main()
