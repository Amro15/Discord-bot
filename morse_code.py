MORSE_CODE_DICT = { 
    "A":".-",
    "N":"-.",
	"B":"-...",
    "O":"---",	 
 	"C":"-.-.",
    "P":".--.",	 
 	"D":"-..",
    "Q":"--.-",	 
 	"E":".",
    "R":".-.",	 
 	"F":"..-.",
    "S":"...",	 
 	"G":"--.",
    "T":"-",	 
 	"H":"....",
    "U":"..-",	 
 	"I":"..",
    "V":"...-",	 
 	"J":".---",
    "W":".--",	 
 	"K":"-.-",
    "X":"-..-",	 
 	"L":".-..",
    "Y":"-.--",	 
 	"M":"--",
    "Z":"--..",
    "1":".----",
    "6":"-....",	 
 	"2":"..---",
    "7":"--...",	 
 	"3":"...--",
    "8":"---..",	 
 	"4":"....-",
    "9":"----.",	 
 	"5":".....",
    "0":"-----",
    " ":"/",
    "?":"..--..",
    ";":"-.-.-.",	 
 	":":"---...",
    "/":"-..-.",	 
 	"-":"-....-",
    "\'":".----.",	 
 	"\"":".-..-.",
    "(":"-.--.",
    ")":"-.--.-",	 
 	"=":"-...-",
    "+":".-.-.",	 
 	"*":"-..-",
    "@":".--.-.",
    "Á":".--.-",
    "Ä":".-.-", 
 	"É":"..-..",
    "Ñ":"--.--", 
 	"Ö":"---.",
    "Ü":"..--" }	


fully_translated = True
"""Determines if the string has been fully translated"""
def decode_char(char: str) -> str:
   """Decodes a morse code character"""
   try:
      decoded_char = list(MORSE_CODE_DICT.keys())[list(MORSE_CODE_DICT.values()).index(char)]
   except ValueError:
      fully_translated = False
      return f"**{char}**"
   else:
      global fully_translated
      fully_translated = True
      return decoded_char

def decode(s: list) -> tuple[str, bool]:
    """Decodes a string of morse code returns a tuple of the decoded string and if the string was fully decoded or not"""
    decoded_sentence = ""
    for char in s:
        # / is the seperator between words
        if "/" in char :
            # if there is only / in the sentence just add a space
            if char == "/":
                decoded_sentence = decoded_sentence + " "
                continue
            else:
                    # if char ends with / add the space after decoding and resume the loop
                    if str(char).endswith("/"):
                        char = str(char).replace("/","")
                        decoded_sentence = decoded_sentence + decode_char(char) + " "
                    # if it starts with / add the space before decoding and finish the loop
                    elif str(char).startswith("/"):
                        char = str(char).replace("/","")
                        decoded_sentence = decoded_sentence + " " + decode_char(char)
                    # otherwise it means that the word starts and ends with a / thus we need to add a space before and after the word and resume the loop
                    elif str(char).startswith("/") and str(char).endswith("/"):
                        char = str(char).replace("/", "")
                        decoded_sentence = " " + decoded_sentence + decode_char(char) + " "
                    # that means there is a / in between two words but in 1 list element which we will need to sperate and decode with a space
                    else:
                        char1, char2 = str(char).split("/")
                        decoded_sentence = decoded_sentence + decode_char(char1) + " " + decode_char(char2)
        else:
         # normal chars with no /
         decoded_sentence = decoded_sentence + decode_char(char)

    return decoded_sentence.strip(), fully_translated
        
fully_encrypted = True
"""Determins if the string has been fully encrypted"""
def encrypt_char(char:str) -> str:
   """Encrypts a character to morse code"""
   try:
      encrypted_char = MORSE_CODE_DICT[char.upper()]
   except KeyError:
      global fully_encrypted
      fully_encrypted = False
      return f"**{char}**"
   else:
      return encrypted_char


def encrypt(s: list) -> tuple[str, bool]:
   """Encrypts a string of morse code returns a tuple of the decoded string and if the string was fully encrypted or not"""
   encrypted_sentence = ""
   for index, word in enumerate(s):
      # only add / between words after encrypting the first word
      if index != 0:
         encrypted_sentence = encrypted_sentence + " / "
      encrypted_word = ""
      # encrypt each word
      for char in word:
         encrypted_word = encrypted_word + encrypt_char(char) + " "
      # concatenate each word the sentence
      encrypted_sentence = encrypted_sentence + encrypted_word
   return encrypted_sentence, fully_encrypted