from pprint import pprint
from dataclasses import dataclass, asdict

# Difference between dict??
@dataclass
class Query:
    args: list[str]
    operator: str | None = ""
    
    def __str__(self) -> str:
        return str(asdict(self))


class Parser:
    def __init__(self):
        self.operators = ['AND', 'OR']
        self.negation = 'NOT'
        
    
    def _decompose(self, query: str) -> list:
        parts = []
        current_token = ""
        char_iter = iter(range(len(query)))
        
        for i in char_iter:
            match query[i]:
                case '(':
                    closes_at = query[i+1:].index(')')
                    parts.append(self.decode_query(query[i+1 : (i+1) + closes_at]))
                    for _ in range(closes_at + 1):
                        next(char_iter)
                case ' ':
                    if len(current_token) > 0:
                        parts.append(current_token)
                        current_token = ""
                case _:
                    current_token += query[i]
                
        if len(current_token) > 0: 
            parts.append(current_token)
            
        return parts
    
    
    def decode_query(self, query: str) -> Query:
        parts = self._decompose(query)
        
        if len(parts) == 1:
            return Query(args=[parts.pop()], operator=None)
        
        # Preparsae negations
        negation_idx = [i for i, x in enumerate(parts) if x == self.negation]
        offset = 0
        for i in negation_idx:
            idx = i-offset
            parts[idx : idx+2] = [
                Query(args=[parts[i+1]], operator=self.negation)
            ]
            offset += 1
        
        # Parse logical opeartions
        opeartion_idx = [i for i, x in enumerate(parts) if x in self.operators]
        offset = 0
        for i in opeartion_idx:
            idx = i - offset
            parts[idx-1 : idx+2] = [
                Query(args=[parts[idx-1], parts[idx+1]], operator=parts[idx])
            ]
            offset += 2
            
        if len(parts != 1):
            raise SyntaxError('Incorrect boolean structure [unhandled pair]')

        return parts.pop()


if __name__ == '__main__':
    p = Parser()
    
    while True:
        pprint(p.decode_query(input('?: ')))