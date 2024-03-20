import os
import re
import lxml.etree as etree
from collections import defaultdict

class InvertedIndex:
    def __init__(self, doc_dir: str, language: str):
        self.data_dir = doc_dir
        self._data_files = os.listdir(doc_dir)
        self._index = defaultdict(list)
        self._doc_id_hash = {}
        if language == 'cs':
            self.target_tags = ['TEXT', 'TITLE', 'HEADING']    
        else:
            self.target_tags = ['HD', 'TE', 'LD']

        self._build()


    def _build(self):
        doc_id = 0
        parser = etree.XMLParser(recover=True)
        
        print('Constructing inverted index...', end='  ')
        
        for file in self._data_files:
            file_tree: etree._ElementTree = etree.parse(f'{self.data_dir}/{file}', parser=parser)
            
            for doc in file_tree.iter('DOC'):
                for doc_text in doc.itertext(tag=self.target_tags):
                    if doc_text is None: continue
                    
                    for token in set(map(str.lower, re.split(r"\W+", doc_text))):
                        if token in self._index and self._index[token][-1] == doc_id:
                            continue
                        
                        self._index[token].append(doc_id)

                self._doc_id_hash[doc.find('DOCID').text] = doc_id
                doc_id += 1
                
        print('done')


    def query_intersection(self):
        pass