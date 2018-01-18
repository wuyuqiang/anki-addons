# -*- coding: utf-8 -*-
# Author:  Albert Lyubarsky
# Email: albert.lyubarsky@gmail.com
# License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
#
#   Answer Confirmation plugin for Anki 2.0
__version__ = "1.0.0"


from aqt.reviewer import Reviewer
from aqt.utils import tooltip
from anki.hooks import wrap

import Log


HARD_TAG = "Hard"
EASY_TAG = "Easy"

LOG = Log.getLogger(__name__)


def answerCard_before(self, ease) :
    l = self._answerButtonList()
    a = [item for item in l if item[0] == ease]
    if len(a) > 0 :
        easeText = a[0][1]
        node = self.card.note()
        if HARD_TAG == easeText :
            node.delTag(EASY_TAG)
            node.addTag(HARD_TAG)
        elif EASY_TAG == easeText:
            node.delTag(HARD_TAG)
            node.addTag(EASY_TAG)
        tooltip(easeText)


Reviewer._answerCard  = wrap(Reviewer._answerCard, answerCard_before, "before")
