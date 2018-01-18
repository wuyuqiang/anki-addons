# -*- coding: utf-8 -*-

"""
Copyright: Kealan Hobelmann
License: GNU GPL, version 3 or later; http://www.gnu.org/copyleft/gpl.html
Select any number of cards in the card browser and create exact copies of each card in a separate deck.

To use:

1) Open the card browser
2) Select the desired cards
3) Go to Edit > Copy Cards
4) In the pop-up window, enter the Deck your copied cards should be placed into

A couple notes:

- The copied cards should look exactly like the originals
- Tags are preserved in the copied cards
- If the new deck does not exist yet, it will be created
- Review history is NOT copied to the new cards (they appear as new cards)
- The cards will be marked as duplicates (because they are!)
"""

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from anki.hooks import addHook
from aqt import mw
from aqt.utils import getOnlyText
from anki.utils import timestampID

def copyCards(nids):
    mw.checkpoint("Copy Cards")
    mw.progress.start()
    
    # Get desired deck name from input box
    deckName = getOnlyText(_("New deck name:"), default="Copied Cards")
    if not deckName:
        return
    deckName = deckName.replace('"', "")
    
    # Create new deck with name from input box
    deck = mw.col.decks.get(mw.col.decks.id(deckName))
    
    # Copy notes
    for nid in nids:
        #print "Found note: %s" % (nid)
        note = mw.col.getNote(nid)
        model = note.model()
        
        # Assign model to deck
        mw.col.decks.select(deck['id'])
        mw.col.decks.get(deck)['mid'] = model['id']
        mw.col.decks.save(deck)

        # Assign deck to model
        mw.col.models.setCurrent(model)
        mw.col.models.current()['did'] = deck['id']
        mw.col.models.save(model)
        
        # Create new note
        note_copy = mw.col.newNote()
        # Copy tags and fields (all model fields) from original note
        note_copy.tags = note.tags
        note_copy.fields = note.fields

        # Refresh note and add to database
        note_copy.flush()
        mw.col.addNote(note_copy)
        
    # Reset collection and main window
    mw.col.reset()
    mw.reset()
    
    
def setupMenu(browser):
    a = QAction("Copy Cards", browser)
    browser.connect(a, SIGNAL("triggered()"), lambda e=browser: onCopyCards(e))
    browser.form.menuEdit.addSeparator()
    browser.form.menuEdit.addAction(a)

def onCopyCards(browser):
    copyCards(browser.selectedNotes())

addHook("browser.setupMenus", setupMenu)
