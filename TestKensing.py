#!flask/bin/python
from Kensing import Kensing
import urllib, cStringIO, sqlite3, os
import json

k = Kensing(os.path.join(os.getcwd(), 'TestData.json'))
photo_url = os.path.join(os.getcwd(), 'photo_storage/jonathan_long/Climbing90.jpg')

# k.insert_photo(photo_url)
# k.insert_album('Album 1')
k.add_photo_to_album(photo_url, 'Album 1')
# print k.get_photoID_from_URL(photo_url)
