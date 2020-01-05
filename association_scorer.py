import argparse

from association_generator.conceptnet import get_synonyms_conceptnet
from association_generator.smallword import get_synonyms_smallword


def load_association(file_name):
    """
    :param file_name: String
    :return: Dictionary word-association pairs
    """
    with open('./test_file/'+file_name, 'r') as infile:
        associations = infile.readlines()[1:]

    test_association = {}
    for line in associations:
        line = line.split('\t')
        if len(line) > 1:
            if len(line[0]) and line[1]:
                test_association[line[0].strip()] = line[1].strip()
    return test_association


def result_checker(stats, cands, ans):
    """
    Check and update evaluation statistics on one association case
    :param stats: Dictionary
    :param cands: List
    :param ans: String
    :return: Dictionary
    """
    stats['asso_num'] += 1
    stats['cand_num'] += len(cands)

    ans = ans.replace('\"', '')
    ans = ans.replace('/', ',')
    ans = ans.split(',')
    for item in ans:
        item = item.strip()
        if item in cands:
            stats['asso_hit'] += 1
    return stats


def result_printer(results, degree, infile, outfile=None):
    """
    print the result of the evaluation
    :param results: Dictionary
    :param degree: Int
    :param infile: String
    :param outfile: String
    :return: None
    """
    if outfile:
        out = open(outfile, 'w')
        out.write('File name:%s\n' % infile)
        for methods in results:
            out.write('\nMethod name:%s ' % methods)
            out.write('Number of degree:%s\n' % degree)

            out.write('\tTotal number of keywords:%d\n' % results[methods]['asso_num'])
            out.write('\tTarget association hit:%d\n' % results[methods]['asso_hit'])
            out.write('\tTotal number of candidates:%d\n' % results[methods]['cand_num'])
            out.write('\tSuccess rate:%f\n' % (results[methods]['asso_hit'] / results[methods]['asso_num']))
            out.write('\tHit / candidates:%f\n' % (results[methods]['asso_hit'] / results[methods]['cand_num']))
        out.close()
    else:
        print('File name:%s' % infile)
        for methods in results:
            print('\nMethod name:%s ' % methods)
            print('Number of degree:%s' % degree)

            print('\tTotal number of keywords:%d' % results[methods]['asso_num'])
            print('\tTarget association hit:%d' % results[methods]['asso_hit'])
            print('\tTotal number of candidates:%d' % results[methods]['cand_num'])
            print('\tSuccess rate:%f' % (results[methods]['asso_hit'] / results[methods]['asso_num']))
            print('\tHit / candidates:%f' % (results[methods]['asso_hit'] / results[methods]['cand_num']))

    return


def association_tester(infile, methods, degree=1, args=None, outfile=None):
    """

    :param infile: String file name for the test associations
    :param methods: List list of methods to be tested
    :param degree: Int number of degree for searching
    :param args: Dictionary arguments for association methods
    :param outfile: String path and file name for the report
    :return: None
    """
    associations = load_association(infile)

    method_stats = {}
    for item in methods:
        stats = {'cand_num': 0, 'asso_num': 0, 'asso_hit': 0}
        if item == 'swow':
            # small worlds of words
            stats['name'] = 'SmallWorldOfWords'
            for concept in associations:
                cands = get_synonyms_smallword(concept=concept, degree=degree, args=args)
                stats = result_checker(stats, cands, associations[concept])
        elif item == 'cn':
            # concept net
            stats['name'] = 'ConceptNet'
            for concept in associations:
                if args and 'limits' in args:
                    cands = get_synonyms_conceptnet(concept=concept, degree=degree, limits=args['limits'])
                else:
                    cands = get_synonyms_conceptnet(concept=concept, degree=degree)
                stats = result_checker(stats, cands, associations[concept])

        method_stats[item] = stats

    result_printer(method_stats, degree, infile, outfile)
    return


arg_dict = {'limits': 1}
association_tester('1.tsv', ['swow'], args=arg_dict, degree=2)
