import os
import string

from synergistic import poller, broker, indexer

broker_client = broker.client.Client("127.0.0.1", 8891, broker.Type.INDEXER)
main_indexer = indexer.Indexer()


def index(channel, msg_id, payload):
    main_indexer.index(payload['url'], payload['content'])
    print(len(main_indexer.hash_table))


def search(channel, msg_id, payload):
    results = main_indexer.search(payload['query'])
    data = {'results': results, 'msg_id': payload['msg_id'], 'query': payload['query']}
    broker_client.respond(msg_id, data)


if __name__ == "__main__":
    poller = poller.Poll(catch_errors=False)

    poller.add_client(broker_client)
    broker_client.subscribe('index', index)
    broker_client.subscribe('search', search)

    poller.serve_forever()
