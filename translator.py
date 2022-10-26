import sys

import requests
from bs4 import BeautifulSoup

languages = ["Arabic", "German", "English", "Spanish", "French", "Hebrew", "Japanese", "Dutch", "Polish", "Portuguese",
             "Romanian", "Russian", "Turkish"]


class ConnectionException(Exception):
    pass


class LanguageNotSupportedException(Exception):
    pass


class WrongWordException(Exception):
    pass


def translate(language_source, language_transl):
    url = "https://context.reverso.net/translation/"
    url += languages[language_source - 1].lower() + "-" + languages[language_transl - 1].lower() + "/"
    url += str(word)

    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        page = requests.get(url, headers=headers)
        if page.status_code == 404:
            raise WrongWordException
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')
        sys.exit()
    except WrongWordException:
        print("Sorry, unable to find " + word)
        sys.exit()
    file.write(languages[language_transl - 1] + " Translations:" + '\n')
    print(languages[language_transl - 1] + " Translations:")
    soup = BeautifulSoup(page.content, 'html.parser')
    words = soup.find_all('span', {'class': 'display-term'})
    file.write(words[0].text + '\n')
    print(words[0].text)

    file.write(languages[language_transl - 1] + " Examples:" + '\n')
    print(languages[language_transl - 1] + " Examples:")

    phrases_source = soup.find_all('div', {'class': 'src'})
    list_of_phrases_source = [x.text for x in phrases_source]
    list_of_phrases_source = [x.replace("\r\n", "") for x in list_of_phrases_source]
    list_of_phrases_source = [x.replace("\n", "") for x in list_of_phrases_source]
    list_of_phrases_source = [x.replace("          ", "") for x in list_of_phrases_source]

    phrases_transl = soup.find_all('div', {'class': 'trg'})
    list_of_phrases_transl = [x.text for x in phrases_transl]
    list_of_phrases_transl = [x.replace("\r\n", "") for x in list_of_phrases_transl]
    list_of_phrases_transl = [x.replace("\n", "") for x in list_of_phrases_transl]
    list_of_phrases_transl = [x.replace("          ", "") for x in list_of_phrases_transl]

    file.write(list_of_phrases_source[0] + '\n')
    file.write(list_of_phrases_transl[0] + '\n\n')
    print(list_of_phrases_source[0])
    print(list_of_phrases_transl[0])
    print()


args = sys.argv

if len(args) == 1:
    print("Hello, welcome to the translator. Translator supports:")
    for count, ele in enumerate(languages, 1):
        print(str(count) + ". " + str(ele))
    # language_full_names = {"en": "English", "fr": "French"}
    print("Type the number of your language")
    languageSource = int(input())
    print("Type the number of language you want to translate to or '0' to translate to all languages:")
    languageTransl = int(input())
    print('Type the word you want to translate')
    word = input()
else:
    if len(args) != 4:
        print("The script should be called with two arguments, the first and the second number to be multiplied")

    else:
        try:
            if args[1].capitalize() not in languages:
                raise LanguageNotSupportedException
            else:
                languageSource = languages.index(args[1].capitalize()) + 1
        except LanguageNotSupportedException:
            print("Sorry, the program doesn't support " + args[1])
            sys.exit()
        if args[2] == "all":
            languageTransl = 0
        else:
            try:
                if args[2].capitalize() not in languages:
                    raise LanguageNotSupportedException
                else:
                    languageTransl = languages.index(args[2].capitalize()) + 1
            except LanguageNotSupportedException:
                print("Sorry, the program doesn't support " + args[2])
                sys.exit()
        word = args[3]

file = open(word + '.txt', 'a+', encoding='utf-8')
if languageTransl == 0:
    for i in range(13):
        if i + 1 != languageSource:
            translate(languageSource, i + 1)
else:
    translate(languageSource, languageTransl)
file.close()
