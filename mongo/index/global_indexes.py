indexes = []


def register_collection_indexes(collection_name, meta_index):
    global indexes
    indexes.append({
        "collection_name": collection_name,
        "meta_index": meta_index
    })


def get_collection_indexes():
    return indexes
