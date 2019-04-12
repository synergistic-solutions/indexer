import re
import string


from synergistic.indexer.parser import Parser


class Indexer:
    hash_table = {}
    unique_count = 1

    @staticmethod
    def tokenize(text):
        tokens = re.split("[" + string.punctuation + string.whitespace + "]+", text)
        tokens = [token.lower() for token in tokens if token]
        return tokens

    def search(self, text):
        results = {}

        for token in self.tokenize(text):
            count, urls = self.hash_table.get(token, (0, {}))
            inverse_doc_freq = 1 - (count / self.unique_count)
            for url, value in urls.items():
                if url in results:
                    results[url] += value * inverse_doc_freq
                else:
                    results[url] = value * inverse_doc_freq

        return sorted(results.keys(), key=lambda key: results[key], reverse=True)

    def index(self, url, text):
        self.unique_count += 1
        parser = Parser()
        parser.feed(text)

        tokens = {}
        for score, line in parser.data.items():
            line_tokens = self.tokenize(line)
            for token in line_tokens:
                count = line_tokens.count(token) * score
                if token in tokens:
                    tokens[token] += count
                else:
                    tokens[token] = count

        for token, count in tokens:
            if token not in self.hash_table:
                self.hash_table[token] = (0, {})

            self.hash_table[token][0] += 1
            self.hash_table[token][url] = (count, 1, 1)
