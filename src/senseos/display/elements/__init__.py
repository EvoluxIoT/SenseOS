from displayio import Group, TileGrid, Bitmap, Palette, Shape
from displayio import OnDiskBitmap

from displayio_listselect import ListSelect

from adafruit_display_text.label import Label
from adafruit_display_text.bitmap_label import Label as BitmapLabel
from adafruit_display_text.scrolling_label import ScrollingLabel

from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
from adafruit_display_shapes.polygon import Polygon
from adafruit_display_shapes.line import Line
from adafruit_display_shapes.sparkline import MultiSparkline, Sparkline

from adafruit_display_notification import NotificationFree, PlainNotification

from adafruit_button import Button

from adafruit_progressbar.horizontalprogressbar import HorizontalProgressBar, HorizontalFillDirection
from adafruit_progressbar.verticalprogressbar import VerticalProgressBar, VerticalFillDirection


class SenseGuiElement:
    pass

class SenseGuiElementListSelect(SenseGuiElement, ListSelect):
    pass

class SenseGuiElementGroup(SenseGuiElement, Group):
    pass


class SenseGuiElementTileGrid(SenseGuiElement, TileGrid):
    pass


class SenseGuiElementBitmap(SenseGuiElement, Bitmap):
    pass


class SenseGuiElementPalette(SenseGuiElement, Palette):
    pass


class SenseGuiElementShape(SenseGuiElement, Shape):
    pass


class SenseGuiElementOnDiskBitmap(SenseGuiElement, OnDiskBitmap):
    pass


class SenseGuiElementLabel(SenseGuiElement, Label):

    pass


class SenseGuiElementBitmapLabel(SenseGuiElement, BitmapLabel):
    pass


class SenseGuiElementScrollingLabel(SenseGuiElement, ScrollingLabel):
    pass


class SenseGuiElementRect(SenseGuiElement, Rect):
    pass


class SenseGuiElementCircle(SenseGuiElement, Circle):
    pass


class SenseGuiElementRoundRect(SenseGuiElement, RoundRect):
    pass


class SenseGuiElementTriangle(SenseGuiElement, Triangle):
    pass


class SenseGuiElementPolygon(SenseGuiElement, Polygon):
    pass


class SenseGuiElementLine(SenseGuiElement, Line):
    pass


class SenseGuiElementSparkline(SenseGuiElement, Sparkline):
    pass


class SenseGuiElementMultiSparkline(SenseGuiElement, MultiSparkline):
    pass


class SenseGuiElementNotificationFree(SenseGuiElement, NotificationFree):
    pass


class SenseGuiElementPlainNotification(SenseGuiElement, PlainNotification):
    pass


class SenseGuiElementButton(SenseGuiElement, Button):
    pass


class SenseGuiElementHorizontalProgressBar(SenseGuiElement, HorizontalProgressBar):
    pass


class SenseGuiElementVerticalProgressBar(SenseGuiElement, VerticalProgressBar):
    pass


class SenseGuiElementHorizontalFillDirection(HorizontalFillDirection):
    pass


class SenseGuiElementVerticalFillDirection(VerticalFillDirection):
    pass


__all__ = [

    "SenseGuiElement",
    "SenseGuiElementGroup",
    "SenseGuiElementTileGrid",
    "SenseGuiElementBitmap",
    "SenseGuiElementPalette",
    "SenseGuiElementShape",
    "SenseGuiElementOnDiskBitmap",
    "SenseGuiElementLabel",
    "SenseGuiElementBitmapLabel",
    "SenseGuiElementScrollingLabel",
    "SenseGuiElementRect",
    "SenseGuiElementCircle",
    "SenseGuiElementRoundRect",
    "SenseGuiElementTriangle",
    "SenseGuiElementPolygon",
    "SenseGuiElementLine",
    "SenseGuiElementSparkline",
    "SenseGuiElementMultiSparkline",
    "SenseGuiElementNotificationFree",
    "SenseGuiElementPlainNotification",
    "SenseGuiElementButton",
    "SenseGuiElementHorizontalProgressBar",
    "SenseGuiElementHorizontalFillDirection",
    "SenseGuiElementVerticalProgressBar",
    "SenseGuiElementVerticalFillDirection",
    "SenseGuiElementListSelect"
]