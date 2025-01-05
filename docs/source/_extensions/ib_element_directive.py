
import sys
import inspect
from types import MappingProxyType

import copy

from docutils.parsers.rst import Directive

from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter, PropertyDocumenter
from sphinx.util import inspect as sphinx_inspect, docstrings
from PythonScreenStackManager import elements
from PythonScreenStackManager.elements.baseelements import Element

def get_parent_elements(element_class: type[Element]):
    parent_classes = list(element_class.__bases__)
    parent_classes = []
    for cls in inspect.getclasstree(inspect.getmro(element_class)):
        if issubclass(cls,Element):
            # parent_classes.insert(0,cls)
            if cls != Element:
                parent_classes.extend()


def create_default_dict(element_class: type[Element]):

    base_args = inspect.signature(element_class.__init__)
    mro_classes = list(inspect.getmro(elements.Tile))   #0 is class itself, than highest is older parent
    ##This can be nested relatively ok by recursively calling the function.
    ##make dict: start at class itself, create dict. Then continue and call setdefault
    f = mro_classes[0].__elt_init__ ##use this as the original __init__ is overwritten by __init_subclass__
    base_args = inspect.signature(f)
    required_args = []
    optional_args = {}
    for param in base_args.parameters.values():
        if param.default == param.empty:
            if param.name != "self": required_args.append(param.name)
        else:
            optional_args[param.name] = param.default
    for parent_cls in mro_classes[1:]:
        if not issubclass(parent_cls,Element):
            continue
        
        if parent_cls == Element:
            init_func = parent_cls.__init__
        else:
            init_func = parent_cls.__elt_init__
        init_args = inspect.signature(init_func)
        for param in init_args.parameters.values():
            if param.default != param.empty:
                optional_args.setdefault(param.name, param.default)

    return tuple(required_args), MappingProxyType(optional_args)


class inkBoardElement(ClassDocumenter):

    objtype = '-inkboardelement'

    def get_object_members(self, want_all):
        members = super().get_object_members(True)
        ##Seem to not get the properties from parents. Gotta fix that.
        elt_cls = getattr(self.module,self.object_name)
        self.element_class = elt_cls
        required_args, optional_args = create_default_dict(elt_cls)
        elt_cls.element_required_args = required_args
        elt_cls.element_optional_args = optional_args
        property_members = []
        docced_props = set()
        for mem in members[1]:
            # if mem.docstring:
                ##For properties: the docstring is not yet present.
                # print(mem.docstring)
            if sphinx_inspect.isproperty(mem.object):
                
                prop_name = mem.object.fget.__name__
                docstr = mem.object.__doc__

                if prop_name in docced_props:
                    continue

                if not docstr: 
                    docstr = ""
                else:
                    docstr = docstr.strip()
                    if "\n" in docstr:
                        docstrs = docstr.splitlines()
                        docstrs = [string.strip() for string in docstrs]
                        docstr = " ".join(docstrs)
                    if not docstr.endswith((".","?","!", ",",";")):
                        docstr = docstr + "."

                ##docstring is changed for each property has they get doubled oops.
                ##So changing the docstrings in place is not ideal perhaps
                ##Maybe do so in the sorter? as it has the documenter. Or just set the objects docstring?
                if prop_name in optional_args:
                    if mem.object.fset == None:
                        continue
                    default_val = optional_args[prop_name]
                    if isinstance(default_val, str):
                        docstr = f"""| {docstr}
                        | **Optional**, defaults to ``"{default_val}"``
                        """
                    else:
                        ##For dicts, see if they can be converted to yaml?
                        docstr = f"""| {docstr}
                        | **Optional**, defaults to ``{default_val}``
                        """
                    # mem.object.__doc__ = docstr
                elif prop_name in required_args:
                    docstr = f"""**Required**. {docstr}"""
                    # mem.object.__doc__ = docstr
                else:
                    continue

                ##Nope doesn't work sadly.
                ##So implement the parser fixer or something. But where the f do they get parsed.
                # new_prop = copy.deepcopy(mem.object)
                # new_prop.__doc__ = docstr
                # mem.object = new_prop
                property_members.append(mem)
                # print(mem.object)

        ##Don't forget to sort them too. But also, check if that possible happens again after this function returns.
        return False, property_members

    def sort_members(self, documenters, order):
        for documenter, _ in documenters:
            documenter.options.noindex = True
            ##To edit the docstrings: need an elementproperty documenter.
            ##Simply based on propertydocumenter, just overwrite the get_doc function.
            ##Or maybe just append something to the end of it before returning it.
        return super().sort_members(documenters, order)

    def generate(self, more_content = None, real_modname = None, check_module = False, all_members = False):

        ##generate in the parent class simply does this too.
        ##But in here simply setup the stuff to be documented.
        old_name = self.name
        new_name = f"PythonScreenStackManager.elements.baseelements.{self.name}"
        self.name = new_name
        self.objtype = 'class'
        self.options.setdefault("inherited-members", {'object'})

        # self.options.setdefault("no-index", True)
        # self.options.no_index = True

        ##docstr edit: simply find the paramaters line and split from there?
        ##Should be roughly safe.

        ##include: at least mention id at the __init__?
        ##action_shorthands, color_properties
        ##See if the emulator icons can be included somehow? but maybe for a later point
        ##Same with automatically generating images probably.
        ##no-index
        ##all properties that are settable
        ##How to deal with defaults though?

        r = super().generate(more_content, real_modname, check_module, all_members)
        # self.element_class = getattr(self.module, old_name)
        ##Contents from parsing: put into attribute directive.result.data. Is in strings.
        ##Use that to parse the defaults into the properties (use the function inspector function I wrote for devices to get the defaults.)
        ##See self.document_members: If *all_members* is True, document all members, else those given by
        # *self.options.members*.
        ##Maybe overwrite get_object_members?
        ##And check if the docstring can be gathered from there

        ##For testing this:
        ##Add the stuff for the ClassDocumenter and see how it is parsed.
        ##From there: figure out what properties to put in.
        return r

class ElementPropertyDocumenter(PropertyDocumenter):
    ##Set the thingy for priority one higher
    priority = PropertyDocumenter.priority + 1
    objtype = 'elementproperty'

    @classmethod
    def can_document_member(cls, member, membername, isattr, parent):
        if not isinstance(parent, inkBoardElement):
            return False

        elt_cls = getattr(parent.module, parent.object_name, None)
        if not inspect.isclass(elt_cls):
            return False
        if not issubclass(elt_cls,Element):
            return False
        
        return sphinx_inspect.isproperty(getattr(elt_cls,membername,None))
    
    def generate(self, more_content = None, real_modname = None, check_module = False, all_members = False):
        self.objtype = 'property'
        return super().generate(more_content, real_modname, check_module, all_members)

    def get_doc(self):
        self.parent
        docstr = sphinx_inspect.getdoc(self.object, self.get_attr, self.config.autodoc_inherit_docstrings,
                        self.parent, self.object_name)
        # docstring = docstring + "This is an appended docstring"
        if not docstr: 
            docstr = ""
        else:
            docstr = docstr.strip()
            if "\n" in docstr:
                docstrs = docstr.splitlines()
                docstrs = [string.strip() for string in docstrs]
                docstr = " ".join(docstrs)
            if not docstr.endswith((".","?","!", ",",";")):
                docstr = docstr + "."
            
            if self.object_name in self.parent.element_optional_args:
                default_val = self.parent.element_optional_args[self.object_name]
                if isinstance(default_val, str):
                    docstr = f"""| {docstr}
                    | **Optional**, defaults to ``"{default_val}"``
                    """
                else:
                    ##For dicts, see if they can be converted to yaml?
                    docstr = f"""| {docstr}
                    | **Optional**, defaults to ``{default_val}``
                    """
                # mem.object.__doc__ = docstr
            elif self.object_name in self.parent.element_required_args:
                docstr = f"""**Required**. {docstr}"""
        
        if docstr:
            tab_width = self.directive.state.document.settings.tab_width
            return [docstrings.prepare_docstring(docstr, tab_width)]
        return []

def setup(app: Sphinx):
    # app.add_directive("ib_element", inkBoardElement)
    app.add_autodocumenter(ElementPropertyDocumenter)
    app.add_autodocumenter(inkBoardElement)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
