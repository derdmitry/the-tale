# coding: utf-8

from dext.common.utils.testcase import TestCase as DextTestCase, TransactionTestCase as DextTransactionTestCase
from dext.common.utils.urls import url

from dext.settings import settings


def setUp(self):
    from the_tale.accounts.achievements.storage import achievements_storage
    from the_tale.collections.storage import collections_storage, kits_storage, items_storage
    from the_tale.linguistics.storage import game_dictionary, game_lexicon

    from the_tale.game.prototypes import GameState
    from the_tale.game.persons.storage import persons_storage
    from the_tale.game.mobs.storage import mobs_storage
    from the_tale.game.artifacts.storage import artifacts_storage
    from the_tale.game.map.storage import map_info_storage
    from the_tale.game.map.places.storage import places_storage, buildings_storage, resource_exchange_storage
    from the_tale.game.map.roads.storage import roads_storage, waymarks_storage

    settings.refresh(force=True)

    places_storage.clear()
    buildings_storage.clear()
    persons_storage.clear()
    waymarks_storage.clear()
    roads_storage.clear()
    mobs_storage.clear()
    artifacts_storage.clear()
    map_info_storage.clear()
    resource_exchange_storage.clear()
    collections_storage.clear()
    kits_storage.clear()
    items_storage.clear()
    achievements_storage.clear()
    game_dictionary.clear()
    game_lexicon.clear()

    GameState.start()


class TestCaseMixin(object):

    def request_login(self, email, password='111111', remember=False):
        data = {'email': email, 'password': password}
        if remember:
            data['remember'] = 'remember'
        response = self.client.post(url('accounts:auth:api-login', api_version='1.0', api_client='test-1.0'), data)
        self.check_ajax_ok(response)

    def request_logout(self):
        response = self.client.post(url('accounts:auth:api-logout', api_version='1.0', api_client='test-1.0'))
        self.check_ajax_ok(response)


class TestCase(DextTestCase, TestCaseMixin):
    def setUp(self):
        super(TestCase, self).setUp()
        setUp(self)

class TransactionTestCase(DextTransactionTestCase, TestCaseMixin):
    def setUp(self):
        super(TransactionTestCase, self).setUp()
        setUp(self)
