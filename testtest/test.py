from pymongo import MongoClient
client = MongoClient()
db = client.get_database('playrecipe')
collection = db.get_collection('playlists')
projection = {}
projection["_id"] = False
projection["playlists.name"] = 1
projection["playlists.owner"] = 1
projection["playlists.image"] = 1
projection["playlists.url"] = 1
projection["playlists.tracks.album.image"] = 1
projection["playlists.tracks.name"] = 1
projection["playlists.tracks.artists.name"]  = 1


findOne = collection.find_one({},projection=projection) # cursor

for playlist in findOne['playlists'] :
    print('playlist :',playlist["name"])
    for track in playlist['tracks'] :
        print(track["name"],'song by',', '.join([artist["name"] for artist in track["artists"]]))
    print()