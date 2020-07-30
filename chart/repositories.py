from playrecipe.repositories import MongoDBDAO


class ChartDAO:

    def __init__(self):
        self.db = MongoDBDAO().get_client().get_database('playrecipe')

    def get_collection(self, collection_name):
        return self.db.get_collection(collection_name)

    def check(self, username):
        collection = self.get_collection('toptracks')
        check_toptracks = collection.count({'username': username})
        collection = self.get_collection('topartists')
        check_topartists = collection.count({'username': username})
        return check_toptracks, check_topartists

    def get_toptracks_avg(self, username):
        collection = self.get_collection('toptracks')
        pipeline = [{'$match': {'username': username}},
                    {'$project': {'_id': False, 'avgPopularity': {'$avg': '$toptracks.popularity'}}}]
        return collection.aggregate(pipeline)

    def get_topartists_avg(self, username):
        collection = self.get_collection('topartists')
        pipeline = [{'$match': {'username': username}},
                    {'$project': {'_id': False, 'avgPopularity': {'$avg': '$topartists.popularity'}}}]
        return collection.aggregate(pipeline)

    def get_fav_genres(self, username):
        collection = self.get_collection('topartists')
        pipeline = [{'$match': {'username': username}}, {'$unwind': '$topartists'}, {'$unwind': '$topartists.genres'},
                    {'$group': {'_id': '$topartists.genres', 'count': {'$sum': 1}}},
                    {'$project': {'_id': 0, 'genre': '$_id', 'count': 1}}, {'$sort': {'count': -1}}, {'$limit': 10}]
        return collection.aggregate(pipeline)

    def get_fav_artists(self, username):
        collection = self.get_collection('toptracks')
        pipeline = [{'$match': {'username': username}}, {'$unwind': '$toptracks'}, {'$unwind': '$toptracks.artists'},
                    {'$group': {'_id': '$toptracks.artists.name', 'count': {'$sum': 1}}},
                    {'$project': {'_id': 0, 'artist': '$_id', 'count': 1}}, {'$sort': {'count': -1}}, {'$limit': 10}]
        return collection.aggregate(pipeline)
