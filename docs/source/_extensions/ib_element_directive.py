
import sys
import inspect
from types import MappingProxyType

import copy

from docutils.parsers.rst import Directive

from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter, PropertyDocumenter
from sphinx.util import inspect as sphinx_inspect, docstrings, logging
from PythonScreenStackManager import elements
from PythonScreenStackManager.elements.baseelements import Element, colorproperty, elementaction

def get_parent_elements(element_class: type[Element]):
    parent_classes = list(element_class.__bases__)
    parent_classes = []
    for cls in inspect.getclasstree(inspect.getmro(element_class)):
        if issubclass(cls,Element):
            # parent_classes.insert(0,cls)
            if cls != Element:
                parent_classes.extend()

_LOGGER = logging.getLogger(__name__)

def create_default_dict(element_class: type[Element]):

    #0 is class itself, than highest is older parent
    ##This can be nested relatively ok by recursively calling the function.
    ##make dict: start at class itself, create dict. Then continue and call setdefault
    
    # f = mro_classes[0].__elt_init__ ##use this as the original __init__ is overwritten by __init_subclass__
    
    if element_class == Element:
        init_func = Element.__init__
    else:
        init_func = element_class.__init__
    
    base_args = inspect.signature(init_func)
    required_args = []
    optional_args = {}

    mro_classes = list(inspect.getmro(element_class)) 
    for param in base_args.parameters.values():
        if param.default == param.empty:
            if param.name == "self" or param.kind == param.VAR_KEYWORD or param.kind == param.VAR_POSITIONAL:
                continue 
            required_args.append(param.name)
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
    option_spec = ClassDocumenter.option_spec | {"summary-docstr": lambda *arg: True}

    def get_object_members(self, want_all):
        members = super().get_object_members(True)
        ##Seem to not get the properties from parents. Gotta fix that.

        required_args, optional_args = create_default_dict(self.element_class)
        self.element_class.element_required_args = required_args
        self.element_class.element_optional_args = optional_args
        property_members = []
        found_required = set()
        for mem in members[1]:
            # if mem.docstring:
                ##For properties: the docstring is not yet present.
                # print(mem.docstring)
            if sphinx_inspect.isproperty(mem.object):
                
                prop_name = mem.object.fget.__name__
                if prop_name in optional_args:
                    if mem.object.fset == None:
                        continue
                    pass
                elif prop_name in required_args:
                    found_required.add(prop_name)
                    pass
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
        for prop in required_args:
            if prop not in found_required and prop != "kwargs":
                _LOGGER.warning(f"{elt_cls}: Missing required argument {prop} in documentation")
        return False, property_members

    def sort_members(self, documenters, order):
        # sorted_docs = super().sort_members(documenters, order)
        color_props = []
        action_props = []
        other_props = []
        
        for documenter_tuple in documenters:
            documenter = documenter_tuple[0]
            documenter.options.noindex = True
            prop_name = documenter.name.split(".")[-1]
            prop = getattr(self.element_class,prop_name)
            if isinstance(prop,colorproperty):
                color_props.append(documenter_tuple)
            elif isinstance(prop,elementaction):
                action_props.append(documenter_tuple)
            else:
                other_props.append(documenter_tuple)
            ##To edit the docstrings: need an elementproperty documenter.
            ##Simply based on propertydocumenter, just overwrite the get_doc function.
            ##Or maybe just append something to the end of it before returning it.
        
        ##On top: the results of action_shorthands etc? or put those into the element docstrings maybe
        color_props.sort(key=lambda e: e[0].name)
        action_props.sort(key=lambda e: e[0].name)
        other_props.sort(key=lambda e: e[0].name)

        sorted_docs = [*color_props, *action_props, *other_props]
        return sorted_docs

    def generate(self, more_content = None, real_modname = None, check_module = False, all_members = False):

        ##generate in the parent class simply does this too.
        ##But in here simply setup the stuff to be documented.
        old_name = self.name
        if self.name == "Element":
            modname = "PythonScreenStackManager.elements.baseelements"
        else:
            modname = "PythonScreenStackManager.elements"

        new_name = f"{modname}.{self.name}"
        self.name = new_name
        self.objtype = 'class'
        self.options.setdefault("inherited-members", {'object'})

        ##docstr edit: simply find the paramaters line and split from there?
        ##Should be roughly safe.

        ##include: at least mention id at the __init__?
        ##action_shorthands, color_properties
        ##See if the emulator icons can be included somehow? but maybe for a later point
        ##Same with automatically generating images probably.
        ##all properties that are settable

        r = super().generate(more_content, real_modname, check_module, all_members)

        ##For testing this:
        ##Add the stuff for the ClassDocumenter and see how it is parsed.
        ##From there: figure out what properties to put in.
        return r


    def get_doc(self):
        original_docstr = super().get_doc()
        elt_cls = getattr(self.module,self.object_name)
        self.element_class: Element = elt_cls

        if self.options.get("summary-docstr", False):
            new_str = original_docstr[0][0]
            short_doc = [new_str]
        else:
            short_doc = []
            for docstr in original_docstr[0]:
                if docstr.strip() == "Parameters":
                    break
                short_doc.append(docstr)

        short_doc.append(" ")
        short_doc.append("Available shorthand actions are:")
        self.fullname
        for action, function in self.element_class.action_shorthands.items():
            d = docstrings.prepare_docstring(inspect.getdoc(getattr(self.element_class, function)))
            func_summary = d[0]
            short_doc.append(f' - ``{action}``: {func_summary}')

        short_doc.append(" ")
        return [short_doc]

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
