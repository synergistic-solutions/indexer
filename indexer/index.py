import re
import string


class Indexer:
    hash_table = {}

    def tokenize(self, text):
        tokens = re.split("[" + string.punctuation + string.whitespace + "]+", text)
        tokens = [token.lower() for token in tokens if token]
        return tokens

    def search(self, text):
        results = {}

        for token in self.tokenize(text):
            urls = self.hash_table.get(token, {})
            # results = {**results, **urls}
            for url, value in urls.items():
                if url in results:
                    results[url] += value
                else:
                    results[url] = value
                    
        print(results)
        return sorted(results.keys(), key=lambda key: results[key], reverse=True)

    def index(self, url, text):
        tokens = self.tokenize(text)
        token_counts = {token:tokens.count(token) for token in tokens}

        for token, count in token_counts.items():
            if token in self.hash_table:
                self.hash_table[token][url] = count/len(tokens)
            else:
                self.hash_table[token] = {url: count/len(tokens)}
