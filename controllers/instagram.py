# -*- coding: utf-8 -*-
# Controller for all things Instagram related
import json
import images
import urllib, os


def callback():
	''' Function that handles the Instagram callback when a new image is posted '''

	# Helper Functions
	def generateEmail(name, url):
		path = os.path.join(request.folder, 'static/emails/postcard.html')
		email = open(path, 'r').read()
		head, body = email.split('</head>')
		body = body.format(name=name, url=url)
		return head + '</head>' + body

	print 'Instagram: "Hi Server, I\'ve got a new photo for you."'	# Log message for demo presentation
	photoDetails = request.body.read()	# Read the JSON body
	api = auth.settings.login_form.api
	# photoDetails = '[{"changed_aspect": "media", "object": "user", "object_id": "654823838", "time": 1386213869, "subscription_id": 3953547, "data": {"media_id": "603928152342527153_654823838"}}]'
	try:
		photos = json.loads(photoDetails)	# Parse the JSON
	except:
		raise HTTP(400)		# Bad Request, raise error
	for photo in photos:				# Iterate over all photos (there is likely only one)
		media_id = photo['data']['media_id']
		p = api.media(media_id)
		url = p.get_standard_resolution_url()

		## Download photo
		print 'Downloading Photo...'
		base = os.path.join(request.folder, 'static/uploads/', media_id)
		path = dict(jpg = base + '.jpg', pdf = base + '.pdf')
		urllib.urlretrieve(url, path['jpg'])

		## Save Photo in DB
		print 'Saving Photo Details to DB...'
		db.photos.insert(instagram_username=p.user.username, media_id=media_id, standard_url=url, caption = p.caption)

		## Decide what to do with Photo
		user = db(db.auth_user.username == p.user.username).select().first()
		print user

		for rule in db(db.mailing_rules.user_id == user).select():
			print rule
			# Check for keyword
			if rule.keyword and p.caption and rule.keyword not in p.caption:
				# Keyword isn't there, skip this photo
				print 'Skipping'
				print rule
				print ''
				continue

			if rule.digital_address:
				print 'Sending Email...'
				address = db(db.digital_addresses.id == rule.digital_address).select().first()
				print address
				print path['jpg']

				mail.send(address.email,
					  subject='New Photo from %s' % user.first_name,
					  message=generateEmail(user.first_name, url))

			if rule.physical_address:
				print 'Creating Snail Mail...'

				print 'Creating PDF...'
				from reportlab.pdfgen.canvas import Canvas
				from reportlab.lib.units import inch
				from PIL import Image
				pdf = Canvas(path['pdf'], pagesize = (6*inch, 4*inch))
				pdf.drawImage(path['jpg'], inch, 0, width=288, height=288, preserveAspectRatio=True)
				pdf.save()

				dlURL = URL('static', 'uploads', args = [media_id + '.pdf'], scheme=True);
				print 'PDF Available at: %s' % dURL

				print 'Sending Snail Mail Request...'				
				# Create Lob Object
				setting_id = 500			# 4x6 gloss photo
				# lob.Object.create(name=media_id, file=dlURL,
				                # setting_id=setting_id, quantity=1)
				
				print 'Snail Mail Sent'
	

	print 'Server: "Thanks for the photo Instagram, talk soon!"'		# Log message for demo presentation
	return

