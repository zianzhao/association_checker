import requests
from nltk.corpus import wordnet as wn

relations = ['MannerOf', 'UsedFor', 'IsA', 'Causes', 'HasContext', 'FormOf',
             'HasPrerequisite', 'CapableOf', 'HasProperty', 'ReceivesAction',
             'CreatedBy', 'Desires', 'MotivatedByGoal', 'HasLastSubevent',
             'HasSubevent', 'HasFirstSubevent', 'Synonym']


def get_synonyms_conceptnet(concept, degree=1):
    '''
    Get synonym candidates via ConceptNet
    :param concept: String
    :param degree: Int degree for related concept exploration
    :return syms: List of String
    '''
    final_syms = []

    syms = set()

    for relation in relations:
        # limits = min(max(3, 30 - len(syms)), 15)

        # link = 'http://api.conceptnet.io/query?start=/c/en/%s&end=/c/en&rel=/r/%s&limit=%d' % (concept, relation, limits)
        link = 'http://api.conceptnet.io/query?start=/c/en/%s&end=/c/en&rel=/r/%s' % (concept, relation)
        obj = requests.get(link).json()

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
        # print(relation, list(syms))

    # print(len(syms))
    return list(syms)
