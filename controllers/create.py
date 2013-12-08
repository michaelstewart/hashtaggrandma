# -*- coding: utf-8 -*-
# create.py

@auth.requires_login()
def address():

    digital_form = SQLFORM(db.digital_addresses, submit_button = 'Next')
    if digital_form.process().accepted:
        session.address_type = 'digital'
        session.address_id = digital_form.vars.id
        session.flash = 'Thanks!'
        redirect(URL('create', 'rule_type'))
    elif digital_form.errors:
        response.flash = 'Please fix any errors and try again'


    physical_form = SQLFORM(db.physical_addresses, submit_button = 'Next')
    if physical_form.process().accepted:
        session.address_type = 'physical'
        session.address_id = physical_form.vars.id
        session.flash = 'Thanks!'
        redirect(URL('create', 'rule_type'))
    elif physical_form.errors:
        response.flash = 'Please fix any errors and try again'

    return dict(digital_form=digital_form, physical_form=physical_form)

@auth.requires_login()
def rule_type():
    return dict()

@auth.requires_login()
def set_rule():
    rule_type = request.args(0, cast=int)
    if rule_type == 0:
        if session.address_type == 'digital':
            db.mailing_rules.insert(digital_address=session.address_id, always_send=True)
        elif session.address_type == 'physical':
            db.mailing_rules.insert(physical_address=session.address_id, always_send=True)   
        session.flash = 'Your mailing rule has been added'
        redirect(URL('view','addresses'))
        
    elif rule_type == 1:
        keyword = request.vars['keyword']
        if session.address_type == 'digital':
            db.mailing_rules.insert(digital_address=session.address_id, keyword=keyword, always_send=False)
        elif session.address_type == 'physical':
            db.mailing_rules.insert(physical_address=session.address_id, keyword=keyword, always_send=False)
        session.flash = 'Your mailing rule has been added'
        redirect(URL('view','addresses'))

    # If this runs the page has been accessed incorrectly
    raise HTTP(400)

@auth.requires_login()
def success():
    
    return dict()