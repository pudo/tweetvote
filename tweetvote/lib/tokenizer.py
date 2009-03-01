
class TokenType:
    WORD = "WORD"
    PUNCTUATION = "PUNCT"
    NUMERIC = "NUM"
    OTHER = "MISC" 


## Character type definitions used internally
CHAR_IGNORE = 1
CHAR_WORD = 2
CHAR_SPLIT = 3 

class TokenizerException(Exception):
    """
    Dummy class for Tokenizer fuck-ups. 
    """
    pass

class Token():
    def __init__(self, surface, start = 0, end = 0, type = TokenType.WORD):
        self.surface = surface
        self.start = start 
        if end == start:
            self.end += len(surface)
        self.end = end 
        self.type = type
    
    def __unicode__(self):
        return self.surface

    def __str__(self):
        return str(self.__unicode__()) # good luck 

    def __repr__(self): 
        return "<%s[%d-%d:%s]>" % (self.surface, self.start, self.end, self.type)

    def __nonzero__(self):
        return self.__len__() > 0 
    
    def __len__(self):
        return self.end - self.start

    def __contains__(self, index):
        return self.end >= index and self.start <= index


#
# Tokenizer based on unicode character categories.
# 
import unicodedata
class UnicodeTokenizer:
    
    def __init__(self, char_types={}):
        self.unicode_categories = {
            'P' : CHAR_SPLIT,   # punctuation 
            'S' : CHAR_SPLIT,   # symbols 
            'L' : CHAR_WORD,    # letters
            'N' : CHAR_WORD,    # numbers 
            'M' : CHAR_WORD,    # marks
            'C' : CHAR_IGNORE,  # control 
            'Z' : CHAR_IGNORE,  # space 
            }
        self.char_types = char_types

    def tokenize(self, string):
        """
        Tokenize a string based on unicode character categories. 
        TODO: Exceptions like C++, 20km, Leutheusser-Schnarrenberger and that's. 

        Returns a generator of tokens over the given input stream. 
        """
        # We need to have unicode strings
        if not type(string) == type(u""):
            raise TokenizerException, 'Input was not given as unicode'
        start = 0 
        offset = 0 
        last_type = 0
        numeric = True
        for character in string:
            # find current character's type 
            cur_type = self.char_type(character)
            
            # on type change, emit a token 
            if not cur_type == last_type and offset > start:
                if not last_type == CHAR_IGNORE:
                    yield Token(string[start:offset], start, offset, self.token_type(last_type, numeric))
                start = offset
                numeric = True 

            # check for numeric token
            if cur_type == CHAR_WORD and numeric and not self.is_digit(character):
                numeric = False

            last_type = cur_type
            offset += 1

        # the last token:
        if not last_type == CHAR_IGNORE:
            yield Token(string[start:], start, len(string), self.token_type(last_type, numeric))

    def char_type(self, character):
        """
        Find a character type for a given character, either from cache or 
        using Python's unicodedata implementation. 
        TODO: maybe make this eager.
        """
        if character in self.char_types:
            return self.char_types[character]
        # try 'auto-detection':
        c_type = CHAR_WORD
        u_cat = unicodedata.category(character)[0]
        if u_cat in self.unicode_categories:
            c_type = self.unicode_categories[u_cat]
        self.char_types[character] = c_type
        return c_type

    def is_digit(self, character): 
        # better: unicodedata.category(character)[0] == 'N' 
        return character in u'0123456789'
            
    def token_type(self, type, numeric):
        if type == CHAR_SPLIT:
            return TokenType.PUNCTUATION 
        if type == CHAR_WORD:
            if numeric:
                return TokenType.NUMERIC
            return TokenType.WORD
        return TokenType.OTHER