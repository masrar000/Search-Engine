import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

nltk.download("stopwords")
text="This is an example text showing removal of stopwords"

#Built in command containing all English stopwords
stop_words=set(stopwords.words('english'))

words=word_tokenize(text) #tokenizes text into words

#Remove stop words from tokenized words by list comprehension
filtered_words=[word for word in words if word.lower() not in stop_words]
filtered_text=" ".join(filtered_words) #Convert this into string
print(f"Original text: {text}")
print(f"After removal of stopwords: {filtered_text}")
