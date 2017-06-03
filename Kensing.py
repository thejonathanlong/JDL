from JLFoundationData import FoundationData
from datetime import datetime
import os, base64

class KensingData(FoundationData):
	#############
	#Table Names#
	#############
	PHOTOS_TABLE = "Photos"
	ALBUMS_TABLE = "Albums"
	COMMENTS_TABLE = "Comments"
	PHOTOALBUM_TABLE = "PhotoAlbum"
	PHOTOTAG_TABLE = "PhotoTag"
	TAG_TABLE = "Tag"

	PHOTO_BASE_STORAGE = os.path.expanduser(os.path.join(os.getcwd(), 'photo_storage/'))

	def DB_NAME(self):
		'''
			@returns (str): The name of our database.
		'''
		return "BigHeroPhotos.db"
	
	#Mark: Album Methods
	def insert_album(self, name, cover_photo=""):
		values = {'name' : name, 'cover_photo':cover_photo}
		self.insert_statement(self.ALBUMS_TABLE, values)

	def set_album_cover_photo(self, album_name, photoDestination):
		set_statement = 'cover_photo=\'' + str(photoDestination) + '\''
		condition = 'ID=' + str(album_id)
		self.update_table(self.ALBUMS_TABLE, set_statement, condition)
	
	def get_all_albums(self):
		return self.select_all(self.ALBUMS_TABLE)

	def get_id_for_album(self, name):
		condition = 'name=\'' + str(name) + '\''
		return self.select_all(self.ALBUMS_TABLE, condition)[0]['ID']
		
	def get_album_for_name(self, name):
		condition = 'name=\'' + str(name) + '\''
		return self.select_all(self.ALBUMS_TABLE, condition);

############################################ Mark: Photo Methods
	def insert_photo(self, photo_URL, favorite=0):
		values = {"photoDestination" : photo_URL, "dateCreated" : str(datetime.now()), "favorite" : favorite}
		self.insert_statement(self.PHOTOS_TABLE, values)


	def get_photos_for_album(self, name):
		album_id = self.get_id_for_album(name)
		join_on_statement = '%1.id=%2.photoID'
		condition = 'albumID=' + str(album_id)
		photos = self.select_all_photos(condition, self.PHOTOALBUM_TABLE, join_on_statement)
		return photos

	def get_bounded_photos_in_album(self, albumName, upperbound, lowerbound=0):
		album_id = self.get_id_for_album(albumName)
		join_on_statement = '%1.id=%2.photoID'
		condition = 'albumID=' + str(album_id)
		photos = self.select_all_photos(condition, self.PHOTOALBUM_TABLE, join_on_statement, upperbound, lowerbound)
		return photos

	def add_photo_to_album_by_id(self, photoID, albumName):
		album_id = self.get_id_for_album(albumName)
		values = {'photoID' : photoID, 'albumID' : album_id}
		self.insert_statement(self.PHOTOALBUM_TABLE, values)

	def add_photo_to_album(self, photoURL, albumName):
		self.add_photo_to_album_by_id(self.get_photoID_from_URL(photoURL), albumName)

	def get_photoID_from_URL(self, url):
		condition = 'photoDestination=\''+str(url)+'\''
		return self.select_all_photos(condition)[0]['ID']

	def get_all_photos(self):
		return self.select_all_photos()

	def get_photo_for_id(self, photoID):
		condition = 'id=' + str(photoID)
		return self.select_all_photos(condition)

	def select_all_photos(self, condition=None, second_table_name = None, join_on_statement=None, upperbound=None, lowerbound=0, include_data=True):
		photos = self.select_all(self.PHOTOS_TABLE, condition, second_table_name, join_on_statement, upperbound, lowerbound)
		if include_data:
			for photo in photos:
				data = base64.b64encode(open(photo["photoDestination"]).read())
				photo['photo_data'] = data
				photo['photoDestination'] = 'redacted'
		return photos

	def get_all_favorites(self):
		condition = 'favorite=1'
		return self.select_all_photos(condition)

	def favorite_photo(self, photoID):
		set_statement = 'favorite=1'
		condition = 'photoID=' + str(photoID)
		self.update_table(self.PHOTOTAG_TABLE, set_statement, condition)

	def get_bounded_photos(self, upperbound, lowerbound=0):
		return self.select_all_photos(None, None, upperbound, lowerbound)

	def get_photo_for_url(self, url):
		condition = 'photoDestination=\'' + url + '\''
		return self.select_all_photos(condition)

	def get_photos_with_tag(self, tagName):
		condition = 'tagID=' + str(tagID)
		join_on_statement = 'F.id=S.photoID'
		return self.select_all_photos(condition, self.PHOTOTAG_TABLE, join_on_statement)

##################################################################Mark: Tag Methods
	def get_id_for_tag_named(self, name):
		condition = 'name=\'' + str(name) + '\''
		return self.select_all(self.TAG_TABLE, condition)

	def add_tag_to_photo(self, photoID, tagName):
		tagID = self.get_id_for_tag_named(tagName)
		values = {'tagID' : tagID, 'photoID' : photoID}
		self.insert_statement(self.PHOTOTAG_TABLE, values)

	def add_tag(self, tagName):
		values = {'name' : tagName}
		self.insert_statement(self.TAG_TABLE, values)

	#Mark: Comment Methods
	def get_comments_for_photoID(photoID):
		condition = 'photoID=' + str(photoID)
		return self.select_all(self.COMMENTS_TABLE, condition)
