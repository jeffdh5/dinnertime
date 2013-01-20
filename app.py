import os
from flask import Flask, render_template, request
from random import choice
from search import Search

app = Flask(__name__)

@app.route('/', methods=['POST', 'GET'])
def index():
	def address_return(address_lst):
		address = ''
		for item in address_lst:
			address = address + str(item) + ', '
		return address[:-2]
			
	def photo_enlarge(photo_url):
		if photo_url[-6:] == 'ms.jpg':
			return photo_url[:-6] + 'l.jpg'

	if request.method == 'GET':
		return render_template('index.html')
	if request.method == 'POST':
		if request.form['location'] == '':
			return render_template('index.html', error='Enter a location!')
		elif request.form['term'] == '':
			return render_template('index.html', error='Enter a search term!')
		else:
			location = request.form['location']
			term = request.form['term']
			results = Search(url_params={'term':term, 'location':location})
			businesses = results["businesses"]
			if businesses == []:
				return render_template('index.html', error='Well shoot. Our system could not find anything with those search terms. Try again?')
			else:
				random_choice = choice(businesses)
				name = random_choice["name"]
				address = (address_return(random_choice["location"]["display_address"]))
				picture = photo_enlarge(random_choice["image_url"])
				latitude = random_choice["location"]["coordinate"]["latitude"]
				longitude = random_choice["location"]["coordinate"]["longitude"]
    			return render_template('page2.html', name=name, address=address, picture=picture, latitude=latitude, longitude=longitude)

    			
if __name__ == '__main__':
    # Bind to PORT if defined, otherwise default to 5000.
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)