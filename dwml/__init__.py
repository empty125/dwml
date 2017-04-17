"""
http://www.ecma-international.org/publications/standards/Ecma-376.htm
"""
try:
	import lxml.etree as ET # It's faster than 'xml.etree.ElementTree' in CPython
except ImportError:
	import xml.etree.ElementTree as ET

__version__ = '0.2'

class NotSupport(Exception):
	"""
	not support exception
	"""
	pass

__all__ = ['docx', 'latex_dict', 'omml','utils']

for module in __all__:
    __import__(module, globals(), locals(), [])
