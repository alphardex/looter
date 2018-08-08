# validation rules: http://docs.python-cerberus.org/en/stable/validation-rules.html
jav = {
    'datasource': {
        'source': 'torrents',
        'default_sort': [('date', -1)]
    }
}
ALLOW_UNKNOWN = True
DOMAIN = {'jav': jav}
MONGO_DBNAME = 'jav'
MONGO_QUERY_BLACKLIST = ['$where']
RENDERERS = ['eve.render.JSONRenderer']
