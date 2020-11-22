from bs4 import BeautifulSoup
import requests
import sys


def get_input():
    """
    Get input languages and words using sys.argv
    :return string src_lang, dst_lang, trans_word:
    """
    all_langs = ["arabic", "german", "english", "french",
                 "hebrew", "japanese", "dutch", "polish",
                 "portuguese", "romanian", "russian", "turkish",
                 "spanish"]

    src_lang = sys.argv[1]
    lang2_input = sys.argv[2]

    # Handle wrong input for translation language
    if lang2_input not in all_langs + ["all"]:
        print(f"Sorry, the program doesn't support {lang2_input}")
        sys.exit()

    if lang2_input == "all":
        dst_lang = all_langs
        dst_lang.remove(src_lang)
    else:
        dst_lang = lang2_input
    trans_word = sys.argv[3]

    return src_lang, dst_lang, trans_word


def translate_word(src_lang, dst_lang, trans_word, file):
    """
    Get page content, parse for translations and examples
    Print to console and write to file
    :param src_lang:
    :param dst_lang:
    :param trans_word:
    :param file:
    :return None:
    """
    page = "https://context.reverso.net/translation/"

    url = page + src_lang + '-' + dst_lang + '/' + word
    headers = {'User-Agent': 'Mozilla/5.0'}

    # Handle connection error
    try:
        page = requests.get(url, headers=headers)
    except requests.exceptions.ConnectionError:
        print('Something wrong with your internet connection')

    # Handle 404 for unsupported language or other http error codes
    if page.status_code == 404:
        print(f"Sorry, unable to find {trans_word}")
        sys.exit()
    elif page.status_code != 200:
        sys.exit(f"{page.status_code} ERROR")

    soup = BeautifulSoup(page.content, 'html.parser')

    # Get and print translations
    print(f"{dst_lang.capitalize()} Translations:")
    file.write(f"\n{dst_lang.capitalize()} Translations:\n")

    words = soup.select('#translations-content a[class^="translation ltr dict"]')
    translations = [e.text.replace('\n', '').strip() for e in words]

    print(*translations[:5], sep='\n')
    for item in translations:
        file.write("%s\n" % item)

    # Get and print translation examples
    print(f"\n{dst_lang.capitalize()} Examples:")
    file.write(f"\n{dst_lang.capitalize()} Examples:\n")

    sentences = soup.select("#examples-content span.text")
    examples = [e.text.replace('\n', '').strip() for e in sentences]

    print(*examples[:10], sep='\n')
    for item in examples:
        file.write("%s\n" % item)


if __name__ == '__main__':

    # Get translation languages and word
    lang1, lang2, word = get_input()

    file = word + '.txt'
    f = open(file, 'w')

    # Call translate function with single or multiple languages
    if type(lang2) == list:
        for lang in lang2:
            translate_word(lang1, lang, word, f)
    else:
        translate_word(lang1, lang2, word, f)

    f.close()
