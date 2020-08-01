import re
from nltk.corpus import stopwords


def clean_tweets(text):
    remove_links = ' '.join(re.sub(r"http(s)?://((\w+).?){1,}", " ",text).split())
    remove_piclink = re.sub('pic.twitter.com/[A-Za-z0-9]+','',remove_links)
    remove_handles = re.sub(r'@[A-Za-z0-9_]+', '', remove_piclink)
    remove_hashtags = ' '.join(re.sub("#[A-Za-z0-9]+"," ",remove_handles).split())
    remove_dots = re.sub(r'…', '', remove_hashtags)
    text = re.sub('<[^>]*>', '', remove_dots) #remove all html markup
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)', text) #keep emoticon character
    text = re.sub('[\W]+', ' ', text.lower())+' '.join(emoticons).replace('-', '') #remove non-word character, convert to lower case 
    return text


stop = stopwords.words('english')

def tokenizer(text):
    text = re.sub('<[^>]*>', '', text)
    emoticons = re.findall('(?::|;|=)(?:-)?(?:\)|\(|D|P)',text.lower())
    text = re.sub('[\W]+', ' ', text.lower())+ ' '.join(emoticons).replace('-', '')
    tokenized = [w for w in text.split() if w not in stop]
    return tokenized