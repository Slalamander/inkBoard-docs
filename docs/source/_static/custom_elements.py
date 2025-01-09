


from PythonScreenStackManager.elements import Element, GridLayout, Layout, Button


class LabeledElements(GridLayout):

    def __init__(self, elements, **kwargs):
        
        labelelts = []
        for elt in elements:
            labelelts.append(self.create_element_label(elt))

        super().__init__(labelelts, **kwargs)

    def create_element_label(self, element: Element) -> Layout:
        elt_name = getattr(element,"label_text", element.__class__.__name__)

        label = Button(elt_name, fit_text=True, radius="h*0.15", background_color="white", tap_action=getattr(element, "label_tap_action", None))

        id = f"{element.id}_layout"
        labellayout = [["?", (element,"w")], ["h*0.2", (label, "w")]]
        return Layout(labellayout, id=id,
                    grid_row=getattr(element,"grid_row", None), grid_column=getattr(element,"grid_column", None))


from PIL import Image, ImageDraw

from PythonScreenStackManager.elements.baseelements import colorproperty, elementaction
from PythonScreenStackManager.pssm.styles import Style
from PythonScreenStackManager.pssm_types import ColorType
from PythonScreenStackManager.tools import DrawShapes

class DrawToggle(Element):
    """An example of how to make a custom element.
    """

    shorthand_actions = Element.action_shorthands | {"toggle": "toggle"}

    def __init__(self, handle_color: ColorType = "blue", on_color: ColorType = "yellow", off_color: ColorType = "red",  **kwargs):
        
        ##This passes all keyword arguments to the base Element init. 
        ##This has to always be called to set all required properties correctly.
        super().__init__( **kwargs) 
        
        self.handle_color = handle_color
        self.on_color = on_color
        self.off_color = off_color

        self.__toggleState = True

    @property
    def toggleState(self) -> bool:
        "The current state of the toggle"
        return self.__toggleState

    @colorproperty.NOT_NONE
    def handle_color(self) -> ColorType:
        "Color of the toggle circle"
        return self._handle_color
    
    @colorproperty
    def on_color(self) -> ColorType:
        "Color of the slide part when the toggle is on"
        return self._on_color
    
    @colorproperty
    def off_color(self) -> ColorType:
        "Color of the slide part when the toggle is off"
        return self._off_color
    

    def toggle(self):
        """Non async method for toggling.
        """
        self.__toggleState = not self.__toggleState
        self.update(updated=True) 
        return

    async def async_toggle(self):
        "Toggles the element, but uses async. Generally preferred."
        self.__toggleState = not self.__toggleState
        await self.async_update(updated=True)

    @elementaction
    def tap_action(self):
        "The function to call when tapping (short clicking) the toggle"
        self.toggle()
        return self._tap_action
    

    def generator(self, area = None, skipNonLayoutGen = False):

        if area != None:
            self._area = area

        [(x,y),(w,h)] = self.area

        background_color = Style.get_color(self.background_color, self.screen.imgMode)
        base_img = Image.new(self.screen.imgMode, (w,h), background_color)

        if self.toggleState:
            slide_color = self.on_color
        else:
            slide_color = self.off_color
        slide_color = Style.get_color(slide_color, base_img.mode)

        relative_height = "h*0.4"
        relative_width = "w*0.5"
        (slider_h, slider_w) = self._convert_dimension((relative_height, relative_width))        
        
        x_c, y_c = (int(w/2), int(h/2))
        xy = [(x_c - int(slider_w/2), y_c - int(slider_h/2)), (x_c + int(slider_w/2), y_c + int(slider_h/2))]

        DrawShapes.draw_rounded_rectangle(base_img, drawArgs={"fill": slide_color, "xy": xy})

        if self.toggleState:
            circle_x = xy[1][0]
        else:
            circle_x = xy[0][0]

        circle_r = int(slider_h*0.75)

        circle_xy = [(circle_x - circle_r, y_c - circle_r), (circle_x + circle_r, y_c + circle_r)]
        circle_col = Style.get_color(self.handle_color)
        DrawShapes.draw_circle(base_img, {"xy": circle_xy, "fill": circle_col})

        return base_img
    

