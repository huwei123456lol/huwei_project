from werkzeug.contrib.cache import SimpleCache
cache = SimpleCache()
def get_my_item():
	rv = cache.get('my_item')
	if rv is None:
		rv = caculate_value()
		cache.set('my_item',rv,timeout=5*60)
	return rv