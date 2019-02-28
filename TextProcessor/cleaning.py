import re
from pymystem3 import Mystem
import nltk
from nltk.corpus import stopwords

stopwords = stopwords.words('russian') + stopwords.words('english')


def find_urls(text):
    """Find all mentioned urls in a piece of text"""
    print('Searching for URLs')
    url_list = []
    myString_list = [item for item in text.split(" ")]

    # Re search for urls
    for item in myString_list:
        try:
            var = re.search("(?P<url>https?://[^\s]+)", item).group("url")
            url_list.append(var)
        except:
            var = ''
            url_list.append(var)

    # Filter out blanks
    url_list = list(filter(None, url_list))

    return url_list


def find_nicknames(text):
    print('Searching for nicknames')
    nickname_list = []
    myString_list = [item for item in text.split(" ")]

    for item in myString_list:
        try:
            var = re.search(
                "([A-Za-z0-9.,:\'-]+@[A-Za-z0-9.,:\'-]+)|(@[A-Za-z0-9.,:\'-]+)",
                item).group(0)
            nickname_list.append(var)
        except:
            var = ''
            nickname_list.append(var)

    # Filter out blanks
    nickname_list = list(filter(None, nickname_list))

    return (nickname_list)


def find_hashtags(text):

    hashtag_list = []
    myString_list = [item for item in text.split(" ")]

    for item in myString_list:
        try:
            var = re.search(
                "([A-Za-z0-9.,:\'-]+#[A-Za-z0-9.,:\'-]+)|(#[A-Za-z0-9.,:\'-]+)",
                item).group(0)
            hashtag_list.append(var)
        except:
            var = ''
            hashtag_list.append(var)

    # Filter out blanks
    hashtag_list = list(filter(None, hashtag_list))

    return (hashtag_list)


# def find_prices(text):
#     price_list = []
#     try:
#         var = re.search("(цена[ :0-9рублейтгтеньге-]+)|(цина[ :0-9рублейтгтеньге-]+)|(\w+:\/\/\S+)",
#                         text).group(0)
#         price_list.append(var[:5])
#     except:
#         var = ''
#         price_list.append(var)
#
#     # Filter out blanks
#     price_list = list(filter(None, price_list))
#
#     return price_list


# добавление ссылок в отдельный столбик при их наличии
def url_tagging(texts):
    found_urls = [find_urls(doc) if find_urls(doc) else '' for doc in texts]
    return (found_urls)


# добавление ников типа @saledealer в отдельный столбик при их наличии (на всякий случай)
def nickname_tagging(texts):
    found_nicknames = [find_nicknames(doc) if find_nicknames(doc) else '' for doc in texts]
    return (found_nicknames)

# добавление хэштэгов типа в отдельный столбик при их наличии (на всякий случай)
def hashtag_tagging(texts):
    found_hashtags = [find_hashtags(doc) if find_hashtags(doc) else '' for doc in texts]
    return (found_hashtags)


# добавление цен в отдельный столбик при их наличии
# def price_tagging(texts):
#     found_prices = [find_prices(doc) if find_prices(doc) else '' for doc in texts]
#     return (found_prices)


def clean_text(text):
    text = str(text)

    ### Remove URLs
    urls = find_urls(text)
    for url in urls:
        text = text.replace(url, '')

    ### Remove Hashtags
    text = ' '.join(re.sub("([A-Za-z0-9.,:\'-]+#[A-Za-z0-9.,:\'-]+)|(#[A-Za-z0-9.,:\'-]+)", " ", text).split())

    ### Remove nicknames
    text = ' '.join(re.sub("([A-Za-z0-9.,:\'-]+@[A-Za-z0-9.,:\'-]+)|(@[A-Za-z0-9.,:\'-]+)", " ", text).split())

    cleantext = re.sub(re.compile('<.*?>'), '', text)
    removers = ['<p>', '</p>', '<br>', '<em>', '</em>', '<a>', '<span>', '</span>',
                '</a>', '/n', '\n', '\t', '[', ']', "\'\\n", '=', '\n', '&quot',
                ':', '*', '/', 'h04', 'h01', 'h02', 'h03', 'h07', 'h08', 'h09', 'h10',
                'h12', 'h13', 'h14', 'h15', 'h20', 'h23', '</li>', '<li>', '<ul>', '</ul>',
                '\0', '\a', '\b', '\v', '\f', '\r', '&nbsp;', '&/gt;', '&rarr', '&larr', '&#160;',
                '&#8212;', '_xd83d_', '_xdd25_', '_x005f', '|', '@', '#', '...', '"', "'", '. .', '…',
                '. . .', '..', '. . . . .', '..', '.....', '........', '. . ', '?', '!', ';', ':', '•', '&']

    for remove in removers:
        cleantext = cleantext.replace(remove, '')

    cleantext = re.sub(r'<[^=>]*?>', '', cleantext)
    cleantext = re.sub('\s+', ' ', cleantext).strip()
    cleantext = re.sub(r'([^\s\w]|_)+', '', cleantext.lower())

    # translit = {'ё' : 'e', 'a' : 'а', 'b' : 'б', 'c' : 'с/ц', 'd' : 'д', 'e' : 'е',
    #             'f' : 'ф', 'g' : 'г', 'h' : 'х', 'i' : 'и', 'j' : 'дж', 'k' : 'к',
    #             'l' : 'л', 'n' : 'н', 'p' : 'п', 'q' : 'к', 'r' : 'р', 's' : 'с',
    #             't' : 'т', 'u' : 'а/у/и', 'v' : 'в', 'w' : 'в', 'x' : 'кс/х', 'y' : 'и/й/у',
    #             'z' : 'з', 'o' : 'о', 'm' : 'м'}
    # for i in translit:
    # 	cleantext = cleantext.lower().replace(i, translit[i])

    m = Mystem()

    tokens = m.lemmatize(cleantext)
    tokens = [token for token in tokens if len(token) > 1 and token not in stopwords]
    cleantext = ' '.join(tokens)

    return cleantext
