#!flask/bin/python
import os
from flask import Flask, request, jsonify, make_response, Response, abort, render_template_string, url_for, redirect, send_from_directory
from werkzeug import secure_filename
from Kensing import Kensing

UPLOAD_FOLDER = '/Users/jonathanlong/Documents/Hiro/BigHero-Photos/photo_storage/'
ALLOWED_EXTENSIONS = set(['tiff', 'png', 'jpg', 'jpeg', 'gif'])

CURRENT_USER = 'jonathan_long'
app = Flask(__name__)
database_manager = Kensing()
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return "Hello, these are not the droids you are looking for..."

##############
##	Photos  ##
##############
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/api/v1/photos', methods=['POST'])
##
# Test with Curl
# curl -X POST -F "photo=@shot.png" http://127.0.0.1:5000/api/v1/photos #
##
def photos():
	if request.method == 'POST':
		if not os.path.exists(UPLOAD_FOLDER + CURRENT_USER):
			os.mkdir(UPLOAD_FOLDER + CURRENT_USER)
		file = request.files['photo']
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			photo_url = os.path.join(os.path.join(app.config['UPLOAD_FOLDER'], CURRENT_USER), filename)
			file.save(photo_url)
			database_manager.insert_photo(filename)
			# database_manager.save()
			return redirect(url_for('photo_named', filename=str(filename)))

@app.route('/api/v1/photo/<filename>', methods=['GET'])
def photo_named(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=CURRENT_USER + '/' + filename)

@app.route('/api/v1/photos', methods=['GET'])
def get_photos():
	if 'album_name' in request.args:
		if 'upperbound' in request.args and 'lowerbound' in request.args:
			return photos_in_album_bounded(request.args.get('album_name'), request.args.get('upperbound'), request.args.get('lowerbound'))
		elif 'upperbound' in request.args:
			return photos_in_album_bounded(request.args.get('album_name'), request.args.get('upperbound'))
		else:
			return photos_in_album_named(request.args.get('album_name'))
	elif 'url' in request.args:
		return photo_for_URL(arts.get('url'))
	elif 'upperbound' in request.args and 'lowerbound' in request.args:
		return bounded_photos(request.args.get('upperbound'), request.args.get('lowerbound'))
	elif 'upperbound' in request.args:
		return bounded_photos((request.args.get('upperbound')))
	else:
		photos = database_manager.get_all_photos()
		return make_response(jsonify({"photos":photos}), 200)

def bounded_photos(upperbound, lowerbound=0):
	photos = database_manager.get_bounded_photos(upperbound, lowerbound)
	return make_response(jsonify({"bounded": [lowerbound, upperbound], "photos": photos}), 200)

def photo_for_URL(url):
	# url = args.get('url')
	photo = database_manager.photo_for_URL(url)
	return make_response(jsonify({"photo" : photo}), 200)

def photos_in_album_bounded(album_name, upperbound, lowerbound=0):
	photos = database_manager.get_bounded_photos_in_album(album_name, upperbound, lowerbound)
	return make_response(jsonify({"photos" : photos}), 200)

def photos_in_album_named(album_name):
	photos = database_manager.get_photos_for_album(album_name)
	return make_response(jsonify({"Album" : album_name, "Photo" : photos}), 200)

##############
##	Albums  ##
##############
#
#	curl -H "Content-Type: application/json" -X POST -d '{"album": {"name" : "AlbumName", "cover_photo" : "Climbing0.jpg", "photos" : [{"photoDestination" : "Climbing0.jpg"}]}' http://localhost:5000/api/v1/albums
#
@app.route('/api/v1/albums', methods=['GET', 'POST'])
def albums():
	if request.method == 'GET':
		albums = database_manager.get_all_albums()
		return make_response(jsonify({"albums":albums}), 200)
	elif request.method == 'POST':
		input_json = request.get_json()
		album_name = input_json['album']['name']
		database_manager.insert_album(album_name)
		album_photos = input_json['album']['photos']
		print "album_photos: " + str(input_json)
		for photo in album_photos:
			print photo['photoDestination']
			database_manager.add_photo_to_album(photo['photoDestination'], input_json['album']['name'])
		if 'cover_photo' in input_json['album']:
			database_manager.set_album_cover_photo(album_name, input_json['album']['cover_photo'])
		else:
			database_manager.set_album_cover_photo(album_name, album_photos[0]['photoDestination'])
		return make_response(jsonify({}), 200)


@app.route('/api/v1/albums', methods=['GET'])
def album_named():
	name = request.args.get('album_name')
	album = database_manager.get_album_for_name(name)
	return make_response(jsonify({"album": album}), 200)

#################
##	Favorites  ##
#################
@app.route('/api/v1/favorites', methods=['GET'])
def favorites():
	favorites = database_manager.get_all_favorites()
	return make_response(jsonify({"favorites":favorites}), 200)

if __name__ == '__main__':
    app.run(debug=True)