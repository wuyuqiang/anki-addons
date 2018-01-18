from anki.hooks import addHook
from aqt.utils import shortcut
from aqt.qt import *
import Log


LOG = Log.getLogger(__name__)


# b("text_bold", self.toggleBold, _("Ctrl+B"), _("Bold text (Ctrl+B)"), check=True)
#
# b("text_italic", self.toggleItalic, _("Ctrl+I"), _("Italic text (Ctrl+I)"), check=True)
#
# b("text_under", self.toggleUnderline, _("Ctrl+U"), _("Underline text (Ctrl+U)"), check=True)
#
# b("text_super", self.toggleSuper, _("Ctrl+Shift+="), _("Superscript (Ctrl+Shift+=)"), check=True)
#
# b("text_sub", self.toggleSub, _("Ctrl+="), _("Subscript (Ctrl+=)"), check=True)
#
# b("text_clear", self.removeFormat, _("Ctrl+R"), _("Remove formatting (Ctrl+R)"))
#
# but = b("foreground", self.onForeground, _("F7"), _("Set foreground colour (F7)"), text=" ")
#
# but = b("change_colour", self.onChangeCol, _("F8"), _("Change colour (F8)"), text=downArrow())
#
# but = b("cloze", self.onCloze, _("Ctrl+Shift+C"), _("Cloze deletion (Ctrl+Shift+C)"), text="[...]")
#
# but.setFixedWidth(24)
# s = self.clozeShortcut2 = QShortcut(
#     QKeySequence(_("Ctrl+Alt+Shift+C")), self.parentWindow)
# s.connect(s, SIGNAL("activated()"), self.onCloze)
#
# b("mail-attachment", self.onAddMedia, _("F3"), _("Attach pictures/audio/video (F3)"))
#

def change_editor_hotkey(editor):

    button_name = "text_bold"
    button_hotkey = "Ctrl+B"
    button_tip = "Bold text (Ctrl+B)"

    b = editor._buttons[button_name]
    b.setShortcut(QKeySequence(button_hotkey))
    b.setToolTip(shortcut(button_tip))


addHook("setupEditorButtons", change_editor_hotkey)

