
import sys
import inspect
from types import MappingProxyType

import copy

from docutils.parsers.rst import Directive

from sphinx.application import Sphinx
from sphinx.ext.autodoc import ClassDocumenter, PropertyDocumenter, Documenter, ALL
from sphinx.util import inspect as sphinx_inspect, docstrings, logging
from PythonScreenStackManager import elements
from PythonScreenStackManager.elements.baseelements import Element, TileElement,\
                                colorproperty, elementaction, classproperty as ib_classproperty

def get_parent_elements(element_class: type[Element]):
    parent_classes = list(element_class.__bases__)
    parent_classes = []
    for cls in inspect.getclasstree(inspect.getmro(element_class)):
        if issubclass(cls,Element):
            # parent_classes.insert(0,cls)
            if cls != Element:
                parent_classes.extend()

_LOGGER = logging.getLogger(__name__)
ELEMENT_TAB_GROUP = "element-property-tabs-sync"

ELEMENT_TAB_FULL = "element-properties-full"
ELEMENT_TAB_FULL_LABEL = "Full"

ELEMENT_TAB_SHORT = "element-properties-compact"
ELEMENT_TAB_SHORT_LABEL = "Compact"

ELEMENT_TAB_LIST = "element-properties-list"
ELEMENT_TAB_LIST_LABEL = "List"

def create_default_dict(element_class: type[Element]):

    #0 is class itself, than highest is older parent
    ##This can be nested relatively ok by recursively calling the function.
    ##make dict: start at class itself, create dict. Then continue and call setdefault
    
    # f = mro_classes[0].__elt_init__ ##use this as the original __init__ is overwritten by __init_subclass__
    
    if element_class == Element:
        init_func = Element.__init__
    else:
        init_func = element_class.__elt_init__
    
    base_args = inspect.signature(init_func)
    required_args = []
    optional_args = {}

    mro_classes = inspect.getmro(element_class)
    for param in base_args.parameters.values():
        if param.default == param.empty:
            if param.name == "self" or param.kind == param.VAR_KEYWORD or param.kind == param.VAR_POSITIONAL:
                continue 
            required_args.append(param.name)
        else:
            optional_args[param.name] = param.default
    for parent_cls in mro_classes[1:]:
        if parent_cls == Element:
            init_func = parent_cls.__init__
        elif hasattr(parent_cls, "__elt_init__"):
            init_func = parent_cls.__elt_init__
        else:
            continue

        init_args = inspect.signature(init_func)
        for param in init_args.parameters.values():
            if param.default != param.empty:
                optional_args.setdefault(param.name, param.default)

    return tuple(required_args), MappingProxyType(optional_args)


class inkBoardElement(ClassDocumenter):
    """_summary_

    Available options:
    :warn-required: bool, defaults to True. Displays a warning if an element is missing a required argument that is not linked to a property
    :summary-docstr: bool, only displays the first line of the element's docstring.
    """    

    objtype = '-inkboardelement'
    option_spec = ClassDocumenter.option_spec | {"summary-docstr": lambda *arg: True}
    option_spec["ignore-required"] = lambda arg: True
    directivetype = "class"

    def generate(self, more_content = None, real_modname = None, check_module = False, all_members = False):

        ##generate in the parent class simply does this too.
        ##But in here simply setup the stuff to be documented.
        old_name = self.name
        if self.name == "Element" or self.name.startswith("_"):
            ##Figure out how to functionally index these lol.
            modname = "PythonScreenStackManager.elements.baseelements"
        elif real_modname:
            modname = real_modname
        else:
            modname = self.env.ref_context.get('py:module')

        new_name = f"{modname}.{self.name}"
        # self.name = new_name
        # self.objtype = 'class'
        self.options.setdefault("inherited-members", {'object'})

        ##docstr edit: simply find the paramaters line and split from there?
        ##Should be roughly safe.

        ##include: at least mention id at the __init__?
        ##action_shorthands, color_properties
        ##See if the emulator icons can be included somehow? but maybe for a later point
        ##Same with automatically generating images probably.
        ##all properties that are settable

        r = super().generate(more_content, modname, check_module, all_members)

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
        elif not original_docstr:
            short_doc = []
        else:
            short_doc = []
            for docstr in original_docstr[0]:
                if docstr.strip() == "Parameters":
                    break
                short_doc.append(docstr)

        if issubclass(self.element_class, TileElement): #and isinstance(self.element_class.tiles,ib_classproperty):
            if self.element_class.tiles and isinstance(self.element_class.tiles,tuple):
                short_doc.append(" ")
                short_doc.append("| Available element tiles are:")
                line = "| "
                for tile in self.element_class.tiles:
                    line = line + f"``{tile}``, "
                line = line.rstrip(", ")
                short_doc.append(line)
                    # short_doc.append(f" - ``{tile}``")
            
            if self.element_class.defaultLayouts:
                short_doc.append("   ")
                short_doc.append("Shorthand ``tile_layout`` values are:")

                for shorthand, tile_layout in self.element_class.defaultLayouts.items():
                    short_doc.append(f""" - ``{shorthand}``: ``"{tile_layout}"``""")

        short_doc.append(" ")
        short_doc.append("Available shorthand actions are:")
        for action, function_name in self.element_class.action_shorthands.items():
            try:
                func = getattr(self.element_class, function_name)
                docs = inspect.getdoc(func)
                if docs:
                    d = docstrings.prepare_docstring(docs)
                    func_summary = d[0]
                    short_doc.append(f' - ``{action}``: {func_summary}')
                else:
                    short_doc.append(f' - ``{action}``')
            except Exception as e:
                _LOGGER.error(f"{elt_cls}: {e}")
                continue

        return [short_doc]

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
        if not self.options.get("ignore-required", False):
            for prop in required_args:
                if prop not in found_required and prop != "kwargs":
                    _LOGGER.warning(f"{self.element_class}: Missing required argument {prop} in documentation")
        return False, property_members

    def sort_members(self, documenters, order):
        # sorted_docs = super().sort_members(documenters, order)
        required_props = []
        color_props = []
        action_props = []
        other_props = []
        
        for documenter_tuple in documenters:
            documenter = documenter_tuple[0]
            documenter.options.noindex = True
            documenter.directive.state.document.settings.tab_width += 4
            prop_name = documenter.name.split(".")[-1]
            prop = getattr(self.element_class,prop_name)
            if prop_name in self.element_class.element_required_args:
                required_props.append(documenter_tuple)
            elif isinstance(prop,colorproperty):
                color_props.append(documenter_tuple)
            elif isinstance(prop,elementaction):
                action_props.append(documenter_tuple)
            else:
                other_props.append(documenter_tuple)
            ##To edit the docstrings: need an elementproperty documenter.
            ##Simply based on propertydocumenter, just overwrite the get_doc function.
            ##Or maybe just append something to the end of it before returning it.
        
        ##On top: the results of action_shorthands etc? or put those into the element docstrings maybe
        required_props.sort(key=lambda e: e[0].name)
        color_props.sort(key=lambda e: e[0].name)
        action_props.sort(key=lambda e: e[0].name)
        other_props.sort(key=lambda e: e[0].name)

        sorted_docs = [*required_props, *color_props, *action_props, *other_props]
        return sorted_docs

    def document_members(self, all_members = False):
        
        source_name = self.get_sourcename()
        
        self.add_line("**Element Properties**", source_name)
        self.add_line("  ", source_name)
        self.add_line(".. tab-set::", source_name)
        self.indent += self.content_indent

        self.add_line(f":sync-group: {ELEMENT_TAB_GROUP}", source_name)
        self.add_line("  ", source_name)
        tab_item_indent = self.indent

        self.add_line(f".. tab-item:: {ELEMENT_TAB_FULL_LABEL}", source_name)
        self.indent += self.content_indent
        self.add_line(f":sync: {ELEMENT_TAB_FULL}", source_name)
        self.add_line("  ", source_name)        
        
        self.env.temp_data['autodoc:module'] = self.modname
        if self.objpath:
            self.env.temp_data['autodoc:class'] = self.objpath[0]

        want_all = (all_members or
                    self.options.inherited_members or
                    self.options.members is ALL)
        # find out which members are documentable
        members_check_module, members = self.get_object_members(want_all)

        # document non-skipped members
        memberdocumenters: list[tuple[Documenter, bool]] = []
        for (mname, member, isattr) in self.filter_members(members, want_all):
            classes = [cls for cls in self.documenters.values()
                    if cls.can_document_member(member, mname, isattr, self)]
            if not classes:
                # don't know how to document this member
                continue
            # prefer the documenter with the highest priority
            classes.sort(key=lambda cls: cls.priority)
            # give explicitly separated module name, so that members
            # of inner classes can be documented
            full_mname = f'{self.modname}::' + '.'.join((*self.objpath, mname))
            documenter = classes[-1](self.directive, full_mname, self.indent)
            memberdocumenters.append((documenter, isattr))

        member_order = self.options.member_order or self.config.autodoc_member_order
        memberdocumenters = self.sort_members(memberdocumenters, member_order)

        for documenter, isattr in memberdocumenters:
            documenter.generate(
                all_members=True, real_modname=self.real_modname,
                check_module=members_check_module and not isattr)

        self.indent = tab_item_indent
        self.add_line(f".. tab-item:: {ELEMENT_TAB_SHORT_LABEL}", source_name)
        self.indent += self.content_indent

        self.add_line(f":sync: {ELEMENT_TAB_SHORT}", source_name)
        self.add_line("  ", source_name)

        for documenter, isattr in memberdocumenters:
            documenter.is_compact = True
            documenter.indent = self.indent
            documenter.generate(
                all_members=True, real_modname=self.real_modname,
                check_module=members_check_module and not isattr)

        self.indent = tab_item_indent
        self.add_line(f".. tab-item:: {ELEMENT_TAB_LIST_LABEL}", source_name)
        self.indent += self.content_indent

        self.add_line(f":sync: {ELEMENT_TAB_LIST}", source_name)
        self.add_line("  ", source_name)

        for documenter, isattr in memberdocumenters:
            documenter.is_compact = True
            # documenter.indent = self.indent
            docstr = documenter.get_doc()[0][0]
            new_line = f"- ``{documenter.object_name}``, {docstr}. {documenter.summary_docstr}"
            self.add_line(new_line, source_name)
            # self.add_line(f"{documenter.summary_docstr}", source_name)
        ##Add a list view too?

        # reset current objects
        self.env.temp_data['autodoc:module'] = None
        self.env.temp_data['autodoc:class'] = None

    def _document_members(self, all_members = False):
        source_name = self.get_sourcename()
        self.add_line(".. tab-set::", source_name)
        self.indent += self.content_indent
        
        self.add_line(f":sync-group: {ELEMENT_TAB_GROUP}", source_name)
        self.add_line("  ", source_name)
        tab_item_indent = self.indent
        
        self.add_line(f".. tab-item:: {ELEMENT_TAB_FULL_LABEL}", source_name)
        self.indent += self.content_indent

        self.add_line(f":sync: {ELEMENT_TAB_FULL}", source_name)
        self.add_line("  ", source_name)
        self.indent = tab_item_indent
        self.add_line(f".. tab-item:: {ELEMENT_TAB_SHORT_LABEL}", source_name)
        self.indent += self.content_indent

        self.add_line(f":sync: {ELEMENT_TAB_SHORT}", source_name)
        self.add_line("  ", source_name)
        self.add_line("I'm tab 2", source_name)
        res = self.directive.result.data
        return
    
class ElementPropertyDocumenter(PropertyDocumenter):
    ##Set the thingy for priority one higher
    priority = PropertyDocumenter.priority + 1
    objtype = 'elementproperty'
    directivetype = "property"

    def __init__(self, directive, name, indent = '', is_compact: bool = False):
        self.is_compact = is_compact
        super().__init__(directive, name, indent)

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
        # self.objtype = 'property'
        source_name = self.get_sourcename()
        indents = 3
        new_indent = [self.content_indent for i in range(0,indents)]
        # self.indent = self.indent + "".join(new_indent)
        # self.indent = '           '

        super().generate(more_content, real_modname, check_module, all_members)
        res = self.directive.result.data
        return

    def get_doc(self):

        if not self.is_compact:
            return self.get_full_doc()
        else:
            return self.get_compact_doc()

    def get_full_doc(self):
        docstr = sphinx_inspect.getdoc(self.object, self.get_attr, self.config.autodoc_inherit_docstrings,
                        self.parent, self.object_name)
        
        if docstr:
            d = docstrings.prepare_docstring(docstr)
            self.summary_docstr = d[0]
        else:
            self.summary_docstr = ""
        # docstring = docstring + "This is an appended docstring"
        if not docstr: 
            docstr = ""
        else:
            if "----------" in docstr:
                docstr = docstr.split("----------")[0]

            docstr = docstr.strip()
            if "\n" in docstr:
                docstrs = docstr.splitlines()
                docstrs = [string.strip() for string in docstrs]
                docstr = " ".join(docstrs)
            if not docstr.endswith((".","?","!", ",",";")):
                docstr = docstr + "."
            
            self.value_docstr = self.get_default_val_string()
            if self.arg_type == "optional":
                docstr = f"""| {docstr}
                    | {self.value_docstr}
                    """
            else:
                docstr = f"{self.value_docstr}. {docstr}"
        
        if docstr:
            tab_width = self.directive.state.document.settings.tab_width
            d = docstrings.prepare_docstring(docstr, tab_width)
            return [d]
        return []
    
    def get_compact_doc(self):

        return [[self.value_docstr]]
    
    def get_default_val_string(self):

        if self.object_name in self.parent.element_optional_args:
            default_val = self.parent.element_optional_args[self.object_name]
            self.arg_type = "optional"
            if isinstance(default_val, str):
                docstr = f'**Optional**, defaults to ``"{default_val}"``'
            else:
                ##For dicts, see if they can be converted to yaml?
                docstr = f"**Optional**, defaults to ``{default_val}``"
            # mem.object.__doc__ = docstr
        elif self.object_name in self.parent.element_required_args:
            docstr = f"**Required**"
            self.arg_type = "required"
        else:
            self.arg_type = None
            return None
        return docstr
    
class CustomClassDocumenter(ClassDocumenter):
    
    option_spec = ClassDocumenter.option_spec
    option_spec["index-members"] = lambda arg: True
    option_spec["summary-docstr"] = lambda *arg: True
    priority = ClassDocumenter.priority + 1

    objtype = "class-custom"
    directivetype = "class"

    def sort_members(self, documenters, order):
        if not self.options.get("index-members", False):
            for documenter, _ in documenters:
                documenter.options.noindex = True
        return super().sort_members(documenters, order)
    
    def get_doc(self):
        original_docstr = super().get_doc()
        if self.options.get("summary-docstr", False) and original_docstr:
            # new_str = 
            return [[original_docstr[0][0]]]
        return original_docstr

def setup(app: Sphinx):
    # app.add_directive("ib_element", inkBoardElement)
    app.add_autodocumenter(ElementPropertyDocumenter)
    app.add_autodocumenter(inkBoardElement)
    app.add_autodocumenter(CustomClassDocumenter)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
