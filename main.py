import os
from invert_index import InvertedIndex
from query_parser import Parser
import lxml.etree as etree

def decompose_relevance(line: str) -> list[str, str, bool]:
    parts = line.split(' ')
    parts[1:2] = []
    parts[-1] = parts[-1] == '1\n'
    return parts

query_parser = Parser()
output_dir = './output'
targets = [
    ('en', './data/documents_en', './data/topics-train_en.xml', './data/qrels-train_en.txt'), 
    ('cs', './data/documents_cs', './data/topics-train_cs.xml', './data/qrels-train_cs.txt')
]

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

scores_file = open('./output/evaluation.txt', mode='w+')

for language, train_dir, test_file, evaluate_file in targets:
    idx = idx = InvertedIndex(train_dir, language)
    file_tree: etree._ElementTree = etree.parse(test_file)
    relevance = list(map(decompose_relevance, open(evaluate_file, mode='r').readlines()))
    
    precisions = []
    recalls = []

    with open(f'./output/{language}.txt', mode='w+') as output:
        for topic in file_tree.iter('top'):
            q = query_parser.decode_query(topic.find('query').text)
            q_id = topic.find('num').text
            
            q_true = list(
                map(lambda x: x[1], filter(lambda x: x[0] == q_id and x[2], relevance))
            )
            q_result = [
                idx._doc_id_hash[doc_hash] for doc_hash in idx.process_query(q)
            ]
            
            
            TP = len([x for x in q_true if x in q_result])
            FP = len([x for x in q_result if x not in q_true])
            FN = len([x for x in q_true if x not in q_result])
            
            for doc_id in q_result:
                output.write(f'{q_id} {doc_id}\n')

            # Handling edge cases where (TP+FP) or (TP+FN) equals 0
            precisions.append(1 if FP == 0 else TP / (TP + FP))
            recalls.append(1 if FN == 0 else TP / (TP + FN))
            
    scores_file.write(f'{language.upper()}:\n')
    scores_file.write(f'Precision per query: {["%.2f" % x for x in precisions]}\n')
    scores_file.write(f'Recall per query: {["%.2f" % x for x in recalls]}\n')
    scores_file.write(f'AVG precision in {language.upper()} corpora {sum(precisions) / len(precisions):.2f}\n')
    scores_file.write(f'AVG recall in {language.upper()} corpora {sum(recalls) / len(recalls):.2f}\n\n')


scores_file.close()