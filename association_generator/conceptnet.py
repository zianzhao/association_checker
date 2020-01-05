import requests
from nltk.corpus import wordnet as wn

relations = ['MannerOf', 'UsedFor', 'IsA', 'Causes', 'HasContext', 'FormOf',
             'HasPrerequisite', 'CapableOf', 'HasProperty', 'ReceivesAction',
             'CreatedBy', 'Desires', 'MotivatedByGoal', 'HasLastSubevent',
             'HasSubevent', 'HasFirstSubevent', 'Synonym']


def get_synonyms(concept, limits=None, degree=1):
    '''
    :param concept: String
    :param limits: Int maximum number of related word returned
    :param degree: Int degree for related concept exploration
    :return syms: List of String
    '''

    final_syms = []

    syms = set()

    for relation in relations:
        link = 'http://api.conceptnet.io/query?start=/c/en/%s&end=/c/en&rel=/r/%s' % (concept, relation)

        if limits:
            link += '&limit=%d' % limits

        try:
            obj = requests.get(link).json()
        except:
            continue

        edges = obj['edges']
        if not len(edges):
            continue

        for item in edges:
            if relation == 'FormOf':
                # Filtering out words that are not correctly spelled
                if len(wn.lemmas(item['end']['label'].lower())):
                    if 2 < len(item['end']['label'].lower()) < 50:
                        syms.add(item['end']['label'].lower())
            else:
                if 2 < len(item['end']['label'].lower()) < 50:
                    syms.add(item['end']['label'].lower())

        final_syms += syms

    all_syms = list(syms)
    if degree > 1:
        for item in list(syms):
            all_syms += get_synonyms(item, limits, degree-1)
    return list(set(all_syms))


def get_synonyms_conceptnet(concept, limits=None, degree=1):
    '''
    :param concept: String
    :param limits: Int maximum number of related word returned
    :param degree: Int degree for related concept exploration
    :return syms: List of String
    '''

    return get_synonyms(concept, limits, degree)
