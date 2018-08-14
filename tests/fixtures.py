from pytz import utc
from bson import ObjectId
from pytest import fixture
from datetime import datetime, timedelta

from tests.test_users import test_login_succeeds_for_admin, init as users_init


items = [
    {
        '_id': 'tag:foo',
        'type': 'text',
        'version': 2,
        'headline': 'Amazon Is Opening More Bookstores',
        'slugline': 'AMAZON-BOOKSTORE-OPENING',
        'body_html': '<p>New stores will open in DC and Austin in 2018.</p><p>Next line</p>',
        'firstcreated': '2017-11-27T08:00:57+0000',
        'versioncreated': datetime.now(),
        'service': [{'code': 'a', 'name': 'Service A'}],
        'products': [{'code': 1, 'name': 'product-1'}, {'id': 3, 'name': 'product-3'}]
    },
    {
        '_id': 'urn:localhost:weather',
        'type': 'text',
        'version': 1,
        'headline': 'Weather',
        'slugline': 'WEATHER',
        'body_html': '<p>Weather report</p>',
        'ancestors': ['tag:weather', 'tag:weather:old'],
        'firstcreated': datetime.now() - timedelta(days=5),
        'versioncreated': datetime.now().replace(hour=23, minute=55) - timedelta(days=5),
        'service': [{'code': 'b', 'name': 'Service B'}],
        'products': [{'code': 2, 'name': 'product-2'}]
    },
    {
        '_id': 'urn:localhost:flood',
        'type': 'text',
        'version': 1,
        'headline': 'Flood Waters',
        'slugline': 'Disaster',
        'body_html': '<p>Water levels keep rising</p>',
        'firstcreated': datetime.now() - timedelta(days=5),
        'versioncreated': datetime.now().replace(hour=23, minute=55) - timedelta(days=5),
        'service': [{'code': 'c', 'name': 'Service C'}],
        'products': [{'code': 7, 'name': 'product-7'}]
    },
    {
        '_id': 'tag:weather',
        'type': 'text',
        'version': 2,
        'nextversion': 'urn:localhost:weather',
        'versioncreated': datetime.now() - timedelta(days=8),
    },
    {
        '_id': 'tag:weather:old',
        'type': 'text',
        'version': 2,
        'nextversion': 'tag:weather',
        'versioncreated': datetime.now() - timedelta(days=10),
    }
]

agenda_items = [{
    'type': 'agenda',
    '_id': 'urn:conference',
    'versioncreated': datetime(2018, 6, 27, 11, 12, 4, tzinfo=utc),
    'name': 'Conference Planning',
    'slugline': 'Prime Conference',
    'planning_items': [
        {
            'versioncreated': '2018-06-27T11:07:17+0000',
            'planning_date': '2018-07-20T04:00:00+0000',
            'expired': False,
            'flags': {
                'marked_for_not_publication': False
            },
            'slugline': 'Prime Conference',
            'item_class': 'plinat:newscoverage',
            'pubstatus': 'usable',
            'item_id': 'urn:planning',
            'name': 'Conference Planning',
            '_id': 'urn:planning',
            'firstcreated': '2018-06-27T11:07:17+0000',
            'state': 'draft',
            'guid': 'urn:planning',
            'agendas': [],
            '_current_version': 1,
            'coverages': [],
            'type': 'planning'
        }
    ],
    '_created': '2018-06-27T11:12:07+0000',
    'coverages': [],
    'dates': {
        'end': datetime(2018, 7, 20, 4, 0, 0, tzinfo=utc),
        'start': datetime(2018, 7, 20, 4, 0, 0, tzinfo=utc),
    },
    'firstcreated': '2018-06-27T11:12:04+0000',
    '_current_version': 1,
    'headline': 'test headline',
}
]


@fixture(autouse=True)
def init_items(app):
    app.data.insert('items', items)


@fixture(autouse=True)
def init_agenda_items(app):
    app.data.insert('agenda', agenda_items)


@fixture(autouse=True)
def init_auth(app, client):
    users_init(app)
    test_login_succeeds_for_admin(client)


@fixture(autouse=True)
def init_company(app, client):
    app.data.insert('companies', [{
        '_id': 1,
        'name': 'Grain Corp'
    }])

    app.data.insert('users', [{
        '_id': ObjectId('59b4c5c61d41c8d736852fbf'),
        'email': 'foo@bar.com',
        'first_name': 'Foo',
        'last_name': 'Bar',
        'company': 1,
    }])
