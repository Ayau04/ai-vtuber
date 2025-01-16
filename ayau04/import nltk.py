import nltk
from nltk.data import find

try:
    find('corpora/words.zip')  # Check if 'words' is already installed
except LookupError:
    nltk.download('words')  # Download only if not installed
