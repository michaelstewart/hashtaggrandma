# -*- coding: utf-8 -*-
# create.py

@auth.requires_login()
def addresses():
    """
    List returns a list of all addresses digital and physical that the user has registered.
    The view will iterate over the items of the list and display them all.
    """
    fields = ['']
    q = db.physical_addresses.user_id == auth.user_id
    physical_list = SQLFORM.grid(q,
    	searchable=False,
        # fields=fields,
        csv=False,
        create=False, details=False, editable=True, deletable=True)
    if len(db(q).select()) == 0:
    	physical_list = False 

    fields = ['name', 'email']
    q = db.digital_addresses.user_id == auth.user_id
    digital_list = SQLFORM.grid(q,
    	searchable=False,
        # fields=fields,
        csv=False,
        create=False, details=False, editable=True, deletable=True)
    if len(db(q).select()) == 0:
    	digital_list = False 

    return dict(physical_list=physical_list, digital_list=digital_list)


@auth.requires_login()
def items():
    pass

