from tg import expose

@expose('resetpassword.templates.little_partial')
def something(name):
    return dict(name=name)