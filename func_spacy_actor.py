
def takelyrics(homeurl):
    """
    inputed an lyrics.com band url
    output list of dictionaries with song name, url, and lyric

    """
    import requests
    from bs4 import BeautifulSoup as soup
    import re
    import time
    import random
    prefix = 'https://www.lyrics.com/lyric'
    html = requests.get(homeurl)
    page = soup(html.text, 'html.parser')

    albums = page.find_all(attrs = {'class': 'tdata'})
    list_of_musics = []
    for i in albums:
        music = i.find_all('strong')
        if len(music) != 0:
            list_of_musics.append(music)
    music_names = []
    list_of_links = []
    for i in list_of_musics:
        for j in i:
            j = str(j)
            music_names.append(re.findall('"\>(.+?)</a>',j))
            link = re.findall('href="/lyric(.+?)">',j)
            if len(link) != 0:
                list_of_links.append(link)
    lyrics = []
    count = 0
    if len(list_of_links)>100:
        for i in list_of_links[0:100]:
            count +=1
            musicurl = prefix+i[0]
            musichtml = requests.get(musicurl)
            musicpage = soup(musichtml.text, 'html.parser')
            x = musicpage.find_all(attrs = { "id":"lyric-body-text"})
            musiclyric = x[0].text
            musiclyric = [re.sub(r'[^\w\.]', ' ', musiclyric).lower()]
            lyrics.append(musiclyric)

        Discography = []
        for i in range(0, len(list_of_links[0:100])):
            song = {}
            song = {'link':list_of_links[i] ,'name': music_names[i] , 'lyrics': lyrics[i]}
            Discography.append(song)
        return Discography

    else:
        print('Artist doesnt have enough musics')

def unify_to_train_test(list):
    """
    input list of files
    output X_train X_test y_train and y_test

    """
    from sklearn.model_selection import train_test_split
    import pickle
    X_trainall = []
    X_testall = []
    y_trainall = []
    y_testall = []
    for i in list:
        file_Name = i
        fileObject = open('picklefiles/'+file_Name, 'rb')
        sliceartist = pickle.load(fileObject)[0:100]
        X_trainartist, X_testartist = train_test_split(sliceartist, random_state=42)
        X_trainall=X_trainall+X_trainartist
        X_testall=X_testall+X_testartist
        y_trainall=y_trainall+[i]*len(X_trainartist)
        y_testall=y_testall+[i]*len(X_testartist)

    return X_trainall , X_testall, y_trainall, y_testall



def spacy_actor(lisdictrain):
    """
    takes X_train/X_test dictionaries with url, song name and lyric
    out puts lyrics tokenized, lemmazied and without stopwords
    """
    import spacy
    import re
    nlp = spacy.load('en_core_web_md')
    def spacy_cleaner(document):
        new_doc = []
        tokenize_doc = nlp(document)
        for word in tokenize_doc:
            if not word.is_stop and not word.is_punct:
                lemma = word.lemma_
                new_doc.append(lemma)
        return new_doc
    new_token_corpus = []
    words = 0
    for music in lisdictrain:
        x = spacy_cleaner(music['lyrics'][0])
        x = ' '.join(x)
        x = re.sub('\s+', ' ',x)
        x = re.sub(r'\w*\d\w*', ' ',x)
        new_token_corpus.append(x)
        words+=len(x)
    print(words)
    return(new_token_corpus)
