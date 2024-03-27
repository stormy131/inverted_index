import os
import re
from collections import defaultdict
from query_parser import Query
import lxml.etree as etree

class InvertedIndex:
    def __init__(self, doc_dir: str, language: str):
        self.data_dir = doc_dir
        self._data_files = os.listdir(doc_dir)
        self._index = defaultdict(list)
        self._doc_id_hash = dict()
        self._max_id = 0
        
        if language == 'cs':
            self.target_tags = ['TEXT', 'TITLE', 'HEADING']    
        else:
            self.target_tags = ['HD', 'TE', 'LD']

        self._build()


    def _build(self):
        doc_id = 0
        parser = etree.XMLParser(recover=True)
        
        print(f'Constructing inverted index for \'{self.data_dir}\' ...', end='  ')
        
        for file in self._data_files:
            file_tree: etree._ElementTree = etree.parse(f'{self.data_dir}/{file}', parser=parser)
            
            for doc in file_tree.iter('DOC'):
                # WARNING: skipping docs with empty targets in tagging
                processed_doc = False
                
                for doc_text in doc.itertext(tag=self.target_tags):
                    if doc_text is None: continue
                    
                    # TODO: Redundant normalization
                    # for token in set(map(str.lower, re.split(r"\W+", doc_text))):
                    for token in set(re.split(r"\W+", doc_text)):
                        if token in self._index and self._index[token][-1] == doc_id:
                            continue
                        
                        self._index[token].append(doc_id)
                        processed_doc = True

                if processed_doc:
                    self._doc_id_hash[doc_id] = doc.find('DOCID').text
                    doc_id += 1
        
        self._max_id = doc_id - 1
        print('done')
        

    def _negate(self, term_postings: list[int]) -> list[int]:
        return [i for i in range(self._max_id) if i not in term_postings]
        
    
    # TODO: compare to built-in set intersection
    def _intersect(self, postings_a: list[int], postings_b: list[int]) -> list[int]:
        idx_a, idx_b = 0, 0
        intersection = []
        
        while True:
            if postings_a[idx_a] == postings_b[idx_b]:
                intersection.append(postings_a[idx_a])
                idx_a, idx_b = idx_a + 1, idx_b + 1
            elif postings_a[idx_a] < postings_b[idx_b]:
                idx_a, idx_b = idx_a + 1, idx_b
            else:
                idx_a, idx_b = idx_a, idx_b + 1
            
            if idx_a >= len(postings_a) or idx_b >= len(postings_b):
                break
            
        return intersection
    
    
    def _union(self, postings_a: list[int], postings_b: list[int]) -> list[int]:
        return set([*postings_a, *postings_b])


    def process_query(self, query: Query) -> list[int]:
        if query.operator in ['NOT', None] and len(query.args) != 1:
            raise SyntaxError('Invalid number of operator arguments')
        
        if query.operator in ['AND', 'OR'] and len(query.args) != 2:
            raise SyntaxError('Invalid number of operator arguments')
        
        match query.operator:
            case 'NOT':
                return self._negate(self.process_query(query.args.pop()))
            case 'AND':
                return self._intersect(*[self.process_query(q) for q in query.args])
            case 'OR':
                return self._union(*[self.process_query(q) for q in query.args])
            case _:
                return self._index[query.args[0]]