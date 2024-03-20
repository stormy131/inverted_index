import re

class Parser:
    def __init__(self):
        self.operators = ['AND', 'OR', 'NOT']
    
    # @staticmethod
    def decode(self, query: str) -> dict:        
        parts = []
        result = dict()
        
        token = ""
        length_iter = iter(range(len(query)))
        for i in length_iter:
            print(f'[{query}] --> {query[i]}')
            match query[i]:
                case '(':
                    # Find closing parenthesis. Should search in the remaining part of the query
                    closes_at = query[i+1:].index(')')
                    sub_query = self.decode(query[i+1 : (i+1) + closes_at])
                    parts.append(sub_query)
                    
                    # TODO: [relative] Indexing rework
                    for _ in range(closes_at - i):
                        next(length_iter)
                case ' ':
                    parts.append(token)
                    token = ""
                case _:
                    token += query[i]
        
        # TODO: Returning of simple token
        for i in range(len(parts)):
            if parts[i] not in self.operators: continue
            result[parts[i]] = [parts[i - 1], parts[i + 1]]
            
        return result
                

if __name__ == '__main__':
    p = Parser()
    
    while True:
        print(p.decode(input('?: ')))