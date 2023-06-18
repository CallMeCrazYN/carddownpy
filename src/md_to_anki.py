import random
import genanki
from tags import *
from learningcards import *
from file_loader import *
from md_to_html import card_content_to_html

# Generates anki-stacks from md-files
def md_to_anki(
    input : str, 
    deck_name : str,
    ):
    """
    Creates an anki-deck from the given md-file.
    :input: single file or path
    :deck_name: name of the tag that is given after the start_tag in the file - also the name of the Anki-Deck
    
    returns: message that anki-deck was created
    """
    # directory-converter
    if (os.path.isdir(input) == True):
        cardlist = load_multiple_files(input, deck_name)
        print (cardlist)
        md_cards = []
        print (cardlist)
        for card in cardlist:
            md_cards.append(parse_md_cards(card))
            print (md_cards)
            
        anki_deck = genanki.Deck(id_generator(),deck_name)
        
        for card in md_cards:
            note_list = anki_note_from_list(card)
            for note in note_list:
                anki_deck.add_note(note)
        
        card_package = genanki.Package(anki_deck)
        card_package.write_to_file(deck_name + '.apkg')
        print("Writing file was succesful!")
        return
        
    # file-converter
    md_cards = load_one_file(input, deck_name)
    # empty file has no need to be converted
    if (md_cards == ""):
        return
    flashcards = parse_md_cards(md_cards)
    # generating the anki file
    anki_deck = genanki.Deck(id_generator(),deck_name)
    for card in flashcards:
        note = anki_note(card)
        anki_deck.add_note(note)
    card_package = genanki.Package(anki_deck)
    card_package.write_to_file(deck_name + '.apkg')
    print("Writing file was succesful!")

def anki_note(card : LearningCard):
    """
    Generates anki-notes from the given Learningcard.
    
    returns: single anki-flashcard
    """
    model = genanki.BASIC_MODEL
    front = card_content_to_html(card.get_front_content())
    back = card_content_to_html(card.get_back_content())
    fields = [front, back]

    note = genanki.Note(model,fields)
    
    return note

def anki_note_from_list(card_list : list):
    """
    Generates anki-notes from the given Learningcard.
    
    returns: single anki-flashcard
    """
    note_list = []
    for x in card_list:
        print (x.get_front_content())
        model = genanki.BASIC_MODEL
        front = card_content_to_html(x.get_front_content())
        back = card_content_to_html(x.get_back_content())
        fields = [front, back]
        note_list.append(genanki.Note(model,fields))
    
    return note_list

def id_generator():
    """
    Creates a random id for the model- and deck-identification.
    
    returns: random number that can be used as an id
    """
    return random.randrange(1 << 30, 1 << 31)

# test
md_to_anki("/Users/joinas/Documents/Uni/Software-Engineering/Markdown-Anki/Markdown-LearningCards", "#test")