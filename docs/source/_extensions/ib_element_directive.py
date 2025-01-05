
from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter
from docutils.parsers.rst import Directive

class inkBoardElement(ClassDocumenter):

    objtype = '-inkboardelement'


    def generate(self, more_content = None, real_modname = None, check_module = False, all_members = False):

        ##generate in the parent class simply does this too.
        ##But in here simply setup the stuff to be documented.
        r = super().generate(more_content, real_modname, check_module, all_members)
        
        return r


def setup(app: Sphinx):
    # app.add_directive("ib_element", inkBoardElement)
    app.add_autodocumenter(inkBoardElement)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
