import simplejson

class Entry(object):
	def __init__(self, app_tag, locale, msg_id, msg_str):
		self.locale = locale
		self.msg_id = msg_id
		self.msg_str = msg_str
		self.app_tag = app_tag

class Serializer(simplejson.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Entry):
            return obj.__dict__
        return simplejson.JSONEncoder.default(self, obj)
