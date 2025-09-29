import string
import re


def normalize_str(s:str) -> str:
    """ Remove whitespaces & punctuation and lowercase """
    return re.sub(r"\s", "", s.lower().translate(str.maketrans("","",string.punctuation)))