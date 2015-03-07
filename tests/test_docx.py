# -*- coding: utf-8 -*-
import re
import shutil
import unittest
import zipfile

from base import PROJECT_ROOT
from dwml import ET
from dwml import omml
from dwml.utils import PY2

try:
	from io import StringIO
except:
	from StringIO import StringIO

DOCXML_ROOT = ''.join(('<w:document xmlns:wpc="http://schemas.microsoft.com/office/word/2010/wordprocessingCanvas"'
			,'xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006" '
			,'xmlns:o="urn:schemas-microsoft-com:office:office" '
			,'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
			,'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
			,'xmlns:v="urn:schemas-microsoft-com:vml" '
			,'xmlns:wp14="http://schemas.microsoft.com/office/word/2010/wordprocessingDrawing" '
			,'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing" '
			,'xmlns:w10="urn:schemas-microsoft-com:office:word" '
			,'xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
			,'xmlns:w14="http://schemas.microsoft.com/office/word/2010/wordml" '
			,'xmlns:wpg="http://schemas.microsoft.com/office/word/2010/wordprocessingGroup" '
			,'xmlns:wpi="http://schemas.microsoft.com/office/word/2010/wordprocessingInk" '
			,'xmlns:wne="http://schemas.microsoft.com/office/word/2006/wordml" '
			,'xmlns:wps="http://schemas.microsoft.com/office/word/2010/wordprocessingShape" mc:Ignorable="w14 wp14">'
			,'{0}</w:document>'
		))

TEXT = '<w:r><w:t> {0} </w:t></w:r>'

class TestDocx(unittest.TestCase):

	omath_re = re.compile(r"<m:omath>.*?</m:omath>",re.IGNORECASE)

	def test_write(self):
		src = PROJECT_ROOT+'/tests/simple.docx'
		dst = PROJECT_ROOT+'/tests/simple-test.docx'
		shutil.copyfile(src=src, dst=dst)
		zf = zipfile.ZipFile(dst,mode='a')
		doc_stream = zf.open('word/document.xml')
		all_xml = doc_stream.read()

		def to_latex(mathobj):
			if PY2:
				s = mathobj.group(0)
				dr = unicode(DOCXML_ROOT,'utf-8')
				xml_str = dr.format(s)
			else:
				xml_str = DOCXML_ROOT.format(mathobj.group(0))
			fileobj = StringIO(xml_str)
			for omath in omml.load(fileobj):
				u = TEXT.replace('{0}',omath.latex)
				return u if not PY2 else unicode(u,'utf-8')
		t = self.omath_re.sub(to_latex,all_xml.decode('utf-8'))
		zf.writestr('word/document.xml',t.encode('utf-8'))
		zf.close()


if __name__ == '__main__':
	unittest.main()