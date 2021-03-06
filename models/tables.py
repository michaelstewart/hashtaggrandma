# tables.py
import datetime

#########################################################################
## Table Definitions
#########################################################################

## Please note:
## I have not defined the web2py field properties such as readable, writable, requited, label etc..
## as I won't be using web2py generated forms and views.

## Auth 
# Add additional fields to auth_user table
auth.settings.extra_fields['auth_user']= [
  Field('account_balance', 'double', default=0)
  ]

# create all tables needed by auth if not custom tables
auth.define_tables(username=True, signature=False)

db.auth_user.account_balance.writable = False
db.auth_user.username.writable = False

# Make fields optional
db.auth_user.email.requires = IS_EMPTY_OR(IS_EMAIL())
db.auth_user.first_name.requires = IS_EMPTY_OR(IS_NOT_EMPTY())
db.auth_user.last_name.requires = IS_EMPTY_OR(IS_NOT_EMPTY())
db.auth_user.account_balance.represent = lambda amt,row: '$%.2f' % amt


## List of possible countries for shipping
db.define_table('country',
                Field('iso'),
                Field('name'),
                Field('printable_name'),
                Field('iso3'),
                Field('numcode'))

## physical_addresses Table
# 
db.define_table('physical_addresses',
	Field('user_id', db.auth_user, default=auth.user_id),
	# Field('nick_name', 'string'),		# What the user calls the address eg. Grandma's House
	Field('name', 'string'),			# Name that the envelope will be addressed to
	Field('line1', 'string'),
	Field('line2', 'string'),
	Field('city', 'string'),
	Field('state_name', 'string'),
	Field('zip_code', 'string'),
	Field('country', 'string'),
)

db.physical_addresses.user_id.writable = db.physical_addresses.user_id.readable = False
db.physical_addresses.id.readable = False
db.physical_addresses.line1.label = 'Address Line 1'
db.physical_addresses.line2.label = 'Address Line 2'
# db.physical_addresses.country.requires = IS_IN_DB(db, 'country.iso')
db.physical_addresses.country.widget = SQLFORM.widgets.autocomplete(request,
				db.country.printable_name, limitby=(0,10), min_length=2, id_field=db.country.iso)


# Address Validator
def validate_address(form):
	import sys
	print form.vars.country
	try:
		address = lob.Address.create(name=form.vars.name, address_line1=form.vars.line1,
								 address_line2=form.vars.line2, 
	                             address_city=form.vars.ctiy, address_state=form.vars.state_name, 
	                             address_country=form.vars.country,
	                             address_zip=form.vars.zip_code)
		print address.to_dict()
	except lob.exceptions.InvalidRequestError as e:
		session.flash = e.message[0]['message']
		# form.errors.country = 'Please enter a valid country'
		form.errors.random = True
		print e.message[0]['message']



## digital_addresses Table
db.define_table('digital_addresses',
	Field('user_id', db.auth_user, default=auth.user_id),
	Field('name', 'string'),			# Name that the email will be addressed to
	Field('email', 'string', requires=IS_EMAIL(error_message='invalid email!'))
)
db.digital_addresses.user_id.writable = db.digital_addresses.user_id.readable = False
db.digital_addresses.email.requires = (IS_EMAIL(error_message='invalid email!'), IS_NOT_IN_DB(db, 'digital_addresses.email'))
db.digital_addresses.id.readable = False

## mailing_rules Table
db.define_table('mailing_rules', 
	Field('user_id', db.auth_user, default=auth.user_id),
	Field('physical_address', db.physical_addresses),	# There will be a physical or digital address but not both.
	Field('digital_address', db.digital_addresses),
	Field('keyword', 'string'), 						# On what posts should the rule be applied.
	Field('always_send', 'boolean', default=False)		# Set to true if the rule is applied on all posts.
)

## photos Table
db.define_table('photos',
	Field('instagram_username', 'string'),
	Field('media_id', 'string'),			# instagram id of the photo
	Field('standard_url', 'text'),			# link to the photo
	Field('caption', 'text'),				# the description attached to the image
	Field('posted_on', 'datetime', default=datetime.datetime.now())
)

## mail_items Table
db.define_table('mail_items',
	Field('user_id', db.auth_user, default=auth.user_id),
	Field('photo_id', db.photos),
	Field('physical_address', db.physical_addresses),	# There will be a physical or digital address but not both.
	Field('digital_address', db.digital_addresses),
	Field('sent_on', 'datetime'),
	Field('status', 'string')							# Response from send API request
)

## paypal_payments
# All from the PayPal API response to a Payment request
db.define_table('paypal_payments',
	Field('id', 'string', unique=True),			# paypal ID
	Field('intent', 'string'),					# 
	Field('payer_id', 'string'),				# id of payer
	Field('redirect_urls', 'string'),			# where the user is sent to after payment
	Field('create_time', 'datetime'),
	Field('payment_state', 'string'),			# status of the payment
	Field('update_time', 'datetime'),			# when the payment status was updated
	primarykey=['id']
)

## payments Table
db.define_table('payments',
	Field('user_id', db.auth_user, default=auth.user_id),
	Field('amount', 'double'),
	Field('amount_paid', 'double'),					# amount paid will be less than amount if they have a coupon code
	Field('coupon_code', 'string'),
	Field('paypal_id', db.paypal_payments)			# link the payment to the details about the paypal transaction
)





