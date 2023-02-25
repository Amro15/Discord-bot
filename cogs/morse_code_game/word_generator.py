from essential_generators import DocumentGenerator
import random
RANDOM_DOC = DocumentGenerator()

# store recent strings so we don't send too many duplicate guesses
global recent_strings
recent_strings = []
def store_recent(s):
    # limit array to 5 strings we don t want to waste memory
    if len(recent_strings) > 4:
        recent_strings.pop(0)
    recent_strings.append(s)
    return recent_strings

def generate_letter():
    random_letters = list(str(RANDOM_DOC.word()).upper())
    random_letter = random.choice(random_letters)
    if random_letter not in recent_strings:
        store_recent(random_letter)
        return random_letter
    else:
        return generate_letter()

def generate_word():
    random_word = RANDOM_DOC.word()
    if random_word not in recent_strings:
        store_recent(random_word)
        return random_word
    else:
        return generate_word()

# take only 4 words out of the setnece 
def generate_sentence():
    sentence = str(RANDOM_DOC.sentence()).replace(".", " ")
    random_sentence = sentence.split(" ") 
    if len(random_sentence) > 4:
        return " ".join(random_sentence[:4])
    return sentence