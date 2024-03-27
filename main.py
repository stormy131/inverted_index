from invert_index import InvertedIndex
from query_parser import Parser
import lxml.etree as etree

query_parser = Parser()
# lxml_parser = etree.XMLParser(recover=True)
targets = [
    ('./data/topics-train_en.xml', './data/documents_en', 'en'), 
    ('./data/topics-train_cs.xml', './data/documents_cs', 'cs')
]

for test_file, train_dir, language in targets:
    idx = idx = InvertedIndex(train_dir, language)
    file_tree: etree._ElementTree = etree.parse(test_file)

    with open(f'./output/{language}.txt', mode='w') as output:
        for topic in file_tree.iter('top'):
            print(topic.find('query').text)
            q = query_parser.decode_query(topic.find('query').text)
            q_id = topic.find('num').text
            q_result =  idx.process_query(q)
            
            for doc in q_result:
                output.write(f'{q_id} {idx._doc_id_hash[doc]}\n')
