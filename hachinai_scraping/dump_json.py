import json


class DumpJson:
    def __init__(self, card_info, rank):
        # self.card_info = card_info
        self.card_info = card_info
        self.rank = rank

    def main(self):
        with open('../json/' + self.rank + '.json', 'w', encoding='utf-8') as f:
            json.dump(self.card_info, f, indent='\t', ensure_ascii=False)
        print('complete dump' + self.rank)
