import spacy

nlp = spacy.load("en_core_web_md")
doc = nlp("Hello, how are you?")
for token in doc:
    print(token.text)
