import requests

base_url = 'https://smallworldofwords.org/search/en/dictionary/all/'


def get_synonyms_smallword(concept, degree=1, min_backward=-1, min_forward=-1, min_freq=-1):
    """

    :param concept: String
    :param degree: Int degree for association exploration
    :param min_backward: Int
    :param min_forward: Int
    :param min_freq: Float minimum frequency to be considered as
    :return syms: List of String

    """

    syms = list()

    # replace underscore with whitespace
    if '_' in concept:
        concept = concept.replace('_', ' ')

    # request the result
    link = base_url + concept
    sym_list = eval(requests.get(url=link).text)

    if len(sym_list):
        # association_types: 'forward', 'backward', 'synonyms'

        if min_forward == -1 or len(sym_list['forward']) <= 5 :
            syms += sym_list['forward']
        else:
            for words in sym_list['forward']:
                if words['freq'] > min_forward:
                    syms.append(words['word'])

        if min_backward == -1 or len(sym_list['backward']) <= 5:
            syms += sym_list['backward']
        else:
            for words in sym_list['backward']:
                if words['freq'] > min_backward:
                    syms.append(words['word'])

        related = sym_list['synonyms']

        if len(related) > 5 and min_freq != -1:
            for i in range(5):
                syms.append(related[str(i + 1)]['word'])
            for i in range(5, len(related)):
                if related[str(i + 1)]["S"] > min_freq:
                    syms.append(related[str(i + 1)]['word'])
        else:
            for item in related:
                syms.append(related[item]['word'])
    return list(set(syms))
