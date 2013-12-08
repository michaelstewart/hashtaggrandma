# -*- coding: utf-8 -*-
# Controller for all things Instagram related
import json
import processImages

def callback():
	print "CALLBACK"
	photoDetails = request.body.read()	# Read the JSON body
	api = auth.settings.login_form.api
	# photoDetails = '[{"changed_aspect": "media", "object": "user", "object_id": "654823838", "time": 1386213869, "subscription_id": 3953547, "data": {"media_id": "603928152342527153_654823838"}}]'
	photos = json.loads(photoDetails)	# Parse the JSON
	for photo in photos:				# Iterate over all photos (there is likely only one)
		media_id = photo['data']['media_id']
		print media_id
		p = api.media(media_id)

		print p.user.username
		print p.get_standard_resolution_url()
		print p.caption 
		url = p.get_standard_resolution_url()

		import urllib, os
		base = os.path.join(request.folder, 'static/uploads/', media_id)
		path = dict(jpg = base + '.jpg', pdf = base + '.pdf')
		print path
		urllib.urlretrieve (url, path['jpg'])

		from reportlab.pdfgen.canvas import Canvas
		from reportlab.lib.units import inch
		from PIL import Image
		pdf = Canvas(path['pdf'], pagesize = (6*inch, 4*inch))
		pdf.drawImage(path['jpg'], inch, 0, width=288, height=288, preserveAspectRatio=True)
		pdf.save()

		dlURL = URL('static', 'uploads', args = [media_id + '.pdf'], scheme=True)

		# Create Lob Object
		setting_id = 500			# 4x6 gloss photo

		print dlURL

		lob.Object.create(name=media_id, file=dlURL,
		                setting_id=setting_id, quantity=1)

	return "OK"

def test():
	print "IN TEST"
	# mail.send('stewartizer@gmail.com',
	  # 'Hashtag Grandma',
	  # 'This is the message body')

	url = "http://distilleryimage6.ak.instagram.com/a6ad322012c111e39e0322000ab69bdf_7.jpg"
	media_id = "1"

	import urllib, os
	base = os.path.join(request.folder, 'static/uploads/', media_id)
	path = dict(jpg = base + '.jpg', pdf = base + '.pdf')
	print path
	urllib.urlretrieve (url, path['jpg'])

	from reportlab.pdfgen.canvas import Canvas
	from reportlab.lib.units import inch
	from PIL import Image
	pdf = Canvas(path['pdf'], pagesize = (6*inch, 4*inch))
	pdf.drawImage(path['jpg'], inch, 0, width=288, height=288, preserveAspectRatio=True)
	pdf.save()

	dlURL = URL('static', 'uploads', args = [media_id + '.pdf'], scheme=True)
	
	# Create Lob Object
	setting_id = 500			# 4x6 gloss photo

	print dlURL

	# lob.Object.create(name=media_id, file=dlURL,
	                # setting_id=setting_id, quantity=1)

	return "OK"


@cache.action()
def download():
	import os

	# media_id = "603928152342527153_654823838"	
	media_id = request.args[0]
	print media_id
	path = os.path.join(request.folder, 'uploads', media_id + '.pdf')

	return response.stream(path, request=request)


