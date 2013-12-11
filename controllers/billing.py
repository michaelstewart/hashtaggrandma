# -*- coding: utf-8 -*-
# charge.py

@auth.requires_login()
def applyCharge():
	''' User is redirect to this controller  '''

	# Get the credit card details submitted by the form
	token = request.get_vars['tok']
	amount = request.get_vars['amt']
	email = auth.user.email

	# Create the charge on Stripe's servers - this will charge the user's card
	try:
		charge = stripe.Charge.create(
		  amount=amount, # amount in cents, again
		  currency="usd",
		  card=token,
		  description=email
		)
		print charge
		session.flash = 'Your payment has been processed, thanks!'
		print 'Payment successful, updating DB...'
		user = db(db.auth_user.id == auth.user_id).select().first()
		balance = user.account_balance + float(amount)/100.0
		user.update_record(account_balance=balance)
		print 'DB updated'
		print 'Sending receipt email...'
		if auth.user.email:
			mail.send(auth.user.email,
					  subject='Thank you for your Payment!',
					  message='Hi %s,\n\nThank you for your payment of $%.2f to Hashtag Grandma\n\nRegards,\nThe Hashtag Grandma Team' % (auth.user.first_name, float(amount)/100.0)
					  )
		print 'Email sent'

	except stripe.CardError, e:
		# The card has been declined
		session.flash = 'There was an error with your payment, please contact support'

	redirect(URL('default', 'user', args=['profile']))

	raise HTTP(400)		# If this executes, something is wrong.