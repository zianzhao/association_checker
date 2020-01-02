from association_generator.conceptnet import get_synonyms_conceptnet
from association_generator.smallword import get_synonyms_smallword


def load_association(file_name):
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
    stats['asso_num'] += 1
    stats['cand_num'] += len(cands)
    if ans in cands:
        stats['asso_hit'] += 1
    return stats


def result_printe(results, degree, infile, outfile=None):
    if outfile:
        out = open(outfile, 'w')
        out.write('File name:%s\n' % infile)
        for methods in results:
            out.write('Method name:%s ' % methods)
            out.write('Number of degree:%s\n' % degree)

            out.write('\tTotal number of keywords:%d\n' % results[methods]['asso_num'])
            out.write('\tTarget association hit:%d\n' % results[methods]['asso_hit'])
            out.write('\tTotal number of candidates:%d\n' % results[methods]['cand_num'])
            out.write('\tSuccess rate:%f\n' % results[methods]['asso_hit'] / results[methods]['asso_num'])
            out.write('\tHit / candidates:%f\n' % results[methods]['asso_hit'] / results[methods]['cand_num'])
        out.close()
    else:
        print('File name:%s\n' % infile)
        for methods in results:
            print('Method name:%s ' % methods)
            print('Number of degree:%s\n' % degree)

            print('\tTotal number of keywords:%d\n' % results[methods]['asso_num'])
            print('\tTarget association hit:%d\n' % results[methods]['asso_hit'])
            print('\tTotal number of candidates:%d\n' % results[methods]['cand_num'])
            print('\tSuccess rate:%f\n' % results[methods]['asso_hit'] / results[methods]['asso_num'])
            print('\tHit / candidates:%f\n' % results[methods]['asso_hit'] / results[methods]['cand_num'])

    return


def association_tester(infile, methods, degree=1, outfile=None):

    associations = load_association(infile)

    method_stats = {}
    for item in methods:
        stats = {'cand_num': 0, 'asso_num': 0, 'asso_hit': 0}
        if item == 'swow':
            stats['name'] = 'SmallWorldOfWords'
            for concept in associations:
                cands = get_synonyms_smallword(concept=concept, degree=degree)
                stats = result_checker(stats, cands, associations[concept])
        elif item == 'cn':
            stats['name'] = 'ConceptNet'
            for concept in associations:
                cands = get_synonyms_conceptnet(concept=concept, degree=degree)
                stats = result_checker(stats, cands, associations[concept])

        method_stats[item] = stats

    result_printe(method_stats, degree, infile, outfile)
    return


association_tester('1.tsv', ['cn', 'swow'])
