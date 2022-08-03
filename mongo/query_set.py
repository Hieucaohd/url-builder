from copy import copy
from pymongo import ReturnDocument


class QuerySet(object):
    def __init__(self, collection):
        self.collection = collection
        self.conn_primary = self.collection
        self.conn_secondary = self.collection

    def find_by_query(self, query, obj_project=None, page=None, per_page=None, sort=None):
        if obj_project:
            cursor = self.conn_secondary.find(query, obj_project)
        else:
            cursor = self.conn_secondary.find(query)
        if sort:
            cursor = cursor.sort(sort)
        if per_page and page:
            cursor = cursor.limit(limit=per_page).skip(page)
        return list(cursor)

    def delete_one(self, query):
        return self.conn_primary.delete_one(query).deleted_count

    def delete_many(self, query):
        return self.conn_primary.delete_many(query).deleted_count

    def insert_one(self, data):
        d = copy(data)  # make sure that data not be modified after this function
        inserted_id = self.conn_primary.insert_one(d).inserted_id
        return inserted_id

    def update_many(self, query, data):
        return self.conn_primary.update_many(query, {"$set": data})

    def update_one(self, query, data):
        return self.conn_primary.update_one(query, {"$set": data}).matched_count

    def update_one_manual(self, query, data):
        return self.conn_primary.update_one(query, data).matched_count

    def find_one_and_update(self, query, data, return_document=ReturnDocument.BEFORE, upsert=False):
        updated_instance = self.conn_primary.find_one_and_update(query, {"$set": data}, return_document=return_document, upsert=upsert)
        return updated_instance

    def bulk_inserts(self, data):
        return self.conn_primary.insert_many(data, ordered=True).inserted_ids

    def bulk_write(self, list_data):
        return self.conn_primary.bulk_write(list_data).acknowledged

    def find_one(self, query, fields=None):
        # query = self.__rebuild_query__(query=query)
        if fields:
            result = self.conn_secondary.find_one(query, fields)
        else:
            result = self.conn_secondary.find_one(query)
        return result

    def count(self, query):
        # query = self.__rebuild_query__(query=query)
        return self.conn_secondary.count(query)
