import re
#re means regular expression, it is a powerful tool for searching and manipulating strings based on specific patterns. In this code snippet, we are using the re module to perform text processing on a given string.
text = "congratulations !!! you won $100 today. "
text = text.lower()
#substitute all non-alphanumeric characters (except whitespace) with an empty string, effectively removing them from the text. This is done using the re.sub() function, which takes a regular expression pattern and a replacement string as arguments.
text = re.sub(r'[^\w\s]', '', text)
print(text)