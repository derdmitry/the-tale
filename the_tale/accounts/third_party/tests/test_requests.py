# coding: utf-8
import mock

from django.conf import settings as project_settings

from dext.common.utils.urls import url

from the_tale.common.utils.testcase import TestCase

from the_tale.accounts.logic import login_page_url

from the_tale.game.logic import create_test_map

from the_tale.accounts.third_party import prototypes
from the_tale.accounts.third_party.conf import third_party_settings
from the_tale.accounts.third_party.tests import helpers

class BaseRequestsTests(TestCase, helpers.ThirdPartyTestsMixin):

    def setUp(self):
        super(BaseRequestsTests, self).setUp()

        create_test_map()

        self.account_1 = self.accounts_factory.create_account()

        self.request_login(self.account_1.email)



class IndexRequestsTests(BaseRequestsTests):

    def setUp(self):
        super(IndexRequestsTests, self).setUp()

        self.requested_url = url('accounts:third-party:tokens:')


    def test_refuse_third_party(self):
        self.request_third_party_token(account=self.account_1)
        self.check_html_ok(self.request_html(self.requested_url), texts=['third_party.access_restricted'])


    def test_login_required(self):
        self.request_logout()
        self.check_redirect(self.requested_url, login_page_url(self.requested_url))

    def test_success(self):
        account_2 = self.accounts_factory.create_account()

        prototypes.AccessTokenPrototype.create(account=self.account_1, application_name='app-name-1', application_info='app-info-1', application_description='app-descr-1')
        prototypes.AccessTokenPrototype.create(account=account_2, application_name='app-name-2', application_info='app-info-2', application_description='app-descr-2')
        prototypes.AccessTokenPrototype.create(account=self.account_1, application_name='app-name-3', application_info='app-info-3', application_description='app-descr-3')

        self.check_html_ok(self.request_html(self.requested_url), texts=['app-name-1', 'app-info-1', ('app-descr-1', 0),
                                                                          'app-name-3', 'app-info-3', ('app-descr-3', 0),
                                                                          ('app-name-2', 0), ('app-info-2', 0), ('app-descr-2', 0)])

    def test_no_tokens_message(self):
        self.check_html_ok(self.request_html(self.requested_url), texts=['pgf-no-tokens-message'])


class ShowRequestsTests(BaseRequestsTests):

    def setUp(self):
        super(ShowRequestsTests, self).setUp()
        self.token = prototypes.AccessTokenPrototype.create(application_name='app-name-1',
                                                            application_info='app-info-1',
                                                            application_description='app-descr-1')

        self.requested_url = url('accounts:third-party:tokens:show', self.token.uid)

    def test_refuse_third_party(self):
        self.request_third_party_token(account=self.account_1)
        self.check_html_ok(self.request_html(self.requested_url), texts=['third_party.access_restricted'])

    def test_login_required(self):
        self.request_logout()
        self.check_redirect(self.requested_url, login_page_url(self.requested_url))

    def test_wrong_owner(self):
        account_2 = self.accounts_factory.create_account()
        self.token.accept(account_2)

        self.check_html_ok(self.request_html(self.requested_url), texts=['third_party.tokens.token.wrong_owner',
                                                                         ('app-name-1', 0), ('app-info-1', 0), ('app-descr-1', 0)])

    def test_success__unaccepted(self):
        self.check_html_ok(self.request_html(self.requested_url), texts=['app-name-1',
                                                                         'app-info-1',
                                                                         'app-descr-1',
                                                                         'pgf-accept-button',
                                                                         'pgf-remove-button'])

    def test_success__accepted(self):
        self.token.accept(self.account_1)
        self.check_html_ok(self.request_html(self.requested_url), texts=['app-name-1',
                                                                         'app-info-1',
                                                                         'app-descr-1',
                                                                         ('pgf-accept-button', 0),
                                                                         'pgf-remove-button'])



class RemoveTokenRequestsTests(BaseRequestsTests):

    def setUp(self):
        super(RemoveTokenRequestsTests, self).setUp()

        self.token = prototypes.AccessTokenPrototype.create(account=self.account_1,
                                                            application_name='app-name-1',
                                                            application_info='app-info-1',
                                                            application_description='app-descr-1')

        self.requested_url = url('accounts:third-party:tokens:remove', self.token.uid)

    def test_refuse_third_party(self):
        self.request_third_party_token(account=self.account_1)
        self.check_ajax_error(self.client.post(self.requested_url), 'third_party.access_restricted')


    def test_wrong_token_id(self):
        with self.check_not_changed(prototypes.AccessTokenPrototype._db_count):
            self.check_ajax_error(self.client.post(url('accounts:third-party:tokens:remove', 'wrong-uid')), 'third_party.tokens.token.not_found')

    def test_login_required(self):
        self.request_logout()
        with self.check_not_changed(prototypes.AccessTokenPrototype._db_count):
            self.check_ajax_error(self.client.post(self.requested_url), 'common.login_required')

    def test_wrong_owner(self):
        account_2 = self.accounts_factory.create_account()
        self.request_login(account_2.email)

        with self.check_not_changed(prototypes.AccessTokenPrototype._db_count):
            self.check_ajax_error(self.client.post(self.requested_url), 'third_party.tokens.token.wrong_owner')

    def test_success(self):
        with mock.patch('dext.common.utils.cache.delete') as cache_delete:
            with self.check_delta(prototypes.AccessTokenPrototype._db_count, -1):
                self.check_ajax_ok(self.client.post(self.requested_url))

        self.assertEqual(cache_delete.call_args_list, [mock.call(third_party_settings.ACCESS_TOKEN_CACHE_KEY % self.token.uid)])

        self.assertEqual(prototypes.AccessTokenPrototype.get_by_uid(self.token.uid), None)



class AcceptTokenRequestsTests(BaseRequestsTests):

    def setUp(self):
        super(AcceptTokenRequestsTests, self).setUp()

        self.token = prototypes.AccessTokenPrototype.create(application_name='app-name-1',
                                                            application_info='app-info-1',
                                                            application_description='app-descr-1')

        self.requested_url = url('accounts:third-party:tokens:accept', self.token.uid)

    def test_refuse_third_party(self):
        self.request_third_party_token(account=self.account_1)
        self.check_ajax_error(self.client.post(self.requested_url), 'third_party.access_restricted')

    def test_wrong_token_id(self):
        self.check_ajax_error(self.client.post(url('accounts:third-party:tokens:remove', 'wrong-uid')), 'third_party.tokens.token.not_found')

        self.token.reload()
        self.assertEqual(self.token.account_id, None)
        self.assertTrue(self.token.state.is_UNACCEPTED)

    def test_login_required(self):
        self.request_logout()

        self.check_ajax_error(self.client.post(self.requested_url), 'common.login_required')

        self.token.reload()
        self.assertEqual(self.token.account_id, None)
        self.assertTrue(self.token.state.is_UNACCEPTED)

    def test_success(self):
        with mock.patch('dext.common.utils.cache.delete') as cache_delete:
            self.check_ajax_ok(self.client.post(self.requested_url))

        self.assertEqual(cache_delete.call_args_list, [mock.call(third_party_settings.ACCESS_TOKEN_CACHE_KEY % self.token.uid)])

        self.token.reload()
        self.assertEqual(self.token.account_id, self.account_1.id)
        self.assertTrue(self.token.state.is_ACCEPTED)


class RequestAccessRequestsTests(BaseRequestsTests):

    def setUp(self):
        super(RequestAccessRequestsTests, self).setUp()

        self.requested_url = url('accounts:third-party:tokens:request-access', api_version='1.0', api_client=project_settings.API_CLIENT)


    def test_form_errors(self):
        with self.check_not_changed(prototypes.AccessTokenPrototype._db_count):
            self.check_ajax_error(self.client.post(self.requested_url, {}), 'third_party.tokens.request_access.form_errors')

    def test_success(self):
        with self.check_delta(prototypes.AccessTokenPrototype._db_count, 1):
            response = self.client.post(self.requested_url, {'application_name': 'app-name',
                                                             'application_info': 'app-info',
                                                             'application_description': 'app-descr'})

        token = prototypes.AccessTokenPrototype._db_latest()

        self.assertEqual(token.application_name, 'app-name')
        self.assertEqual(token.application_info, 'app-info')
        self.assertEqual(token.application_description, 'app-descr')

        self.assertEqual(self.client.session[third_party_settings.ACCESS_TOKEN_SESSION_KEY], token.uid)

        self.check_ajax_ok(response,
                           data={'authorisation-page': url('accounts:third-party:tokens:show', token.uid)})


    def test_success_rerequest(self):
        self.request_third_party_token(account=self.account_1)

        with self.check_delta(prototypes.AccessTokenPrototype._db_count, 1):
            response = self.client.post(self.requested_url, {'application_name': 'xxx-name',
                                                             'application_info': 'xxx-info',
                                                             'application_description': 'xxx-descr'})

        token = prototypes.AccessTokenPrototype._db_latest()

        self.assertEqual(token.application_name, 'xxx-name')
        self.assertEqual(token.application_info, 'xxx-info')
        self.assertEqual(token.application_description, 'xxx-descr')

        self.assertEqual(self.client.session[third_party_settings.ACCESS_TOKEN_SESSION_KEY], token.uid)

        self.check_ajax_ok(response,
                           data={'authorisation-page': url('accounts:third-party:tokens:show', token.uid)})