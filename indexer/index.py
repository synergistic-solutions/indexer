hash_table = {}


def tokenize(text):
    tokens = text.split(' ')
    return tokens


def search(text):
    results = {}

    for token in tokenize(text):
        urls = hash_table.get(token, None)
        if urls:
            for url in urls:
                if url in results:
                    results[url] += 1
                else:
                    results[url] = 1

    return sorted(results.keys(), key=lambda key: results[key], reverse=True)


def index(url, text):
    for token in tokenize(text):

        # checking if not in the hash table then creating an empty list requires another look up in hash table
        if token in hash_table:
            hash_table[token].append(url)
        else:
            hash_table[token] = [url]
