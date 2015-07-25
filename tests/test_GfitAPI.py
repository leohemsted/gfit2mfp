from unittest.mock import Mock, patch, call

import pytest

from gfit2mfp.data_collection import GfitAPI


def test_get_time_range():
    start = Mock(timestamp=Mock(return_value=1))
    end = Mock(timestamp=Mock(return_value=2))
    expected = '1000000000-2000000000'
    assert GfitAPI.get_time_range_str(start, end) == expected

@patch('gfit2mfp.data_collection.datetime')
@patch('gfit2mfp.data_collection.DateRange')
@patch.object(GfitAPI, 'process_datapoint')
def test_preprocess_data_correct_daterange(proc_datapoint, daterange, datetime):
    data = {
        'minStartTimeNs': 1000000000,
        'maxEndTimeNs': 2000000000,
    }
    datetime.fromtimestamp=str

    GfitAPI(Mock(), Mock(), Mock()).preprocess_data(data, Mock())

    assert daterange.call_args_list == [call('1.0', '2.0')]

@patch('gfit2mfp.data_collection.datetime')
@patch('gfit2mfp.data_collection.DateRange')
@patch.object(GfitAPI, 'process_datapoint')
def test_preprocess_data_calls_datapoint(proc_datapoint, daterange, datetime):
    data = {
        'minStartTimeNs': 1,
        'maxEndTimeNs': 1,
        'point': ['a', 'b']
    }
    d_t = Mock()

    GfitAPI(Mock(), Mock(), Mock()).preprocess_data(data, d_t)

    assert proc_datapoint.call_args_list  == [call('a', d_t), call('b', d_t)]

@patch('gfit2mfp.data_collection.datetime')
@patch('gfit2mfp.data_collection.DateRange')
@patch.object(GfitAPI, 'process_datapoint')
def test_preprocess_data_no_points(proc_datapoint, daterange, datetime):
    data = {
        'minStartTimeNs': 1,
        'maxEndTimeNs': 1,
    }

    GfitAPI(Mock(), Mock(), Mock()).preprocess_data(data, Mock())

    assert not proc_datapoint.called

@patch.object(GfitAPI, 'login')
def test_enter_returns_self(login_mock):
    api = GfitAPI(Mock(), Mock(), Mock())
    ret = api.__enter__()

    assert login_mock.call_args_list == [call()]
    assert ret == api

@patch('gfit2mfp.data_collection.httplib2')
@patch.object(GfitAPI, 'get_credentials')
@patch('gfit2mfp.data_collection.build')
def test_login(build, get_creds, httplib):
    creds = get_creds.return_value
    api = GfitAPI(Mock(), Mock(), Mock())

    api.login()

    assert creds.authorize.call_args_list == [call(httplib.Http.return_value)]
    assert build.call_args_list == [call('fitness', 'v1', http=creds.authorize.return_value)]
    assert api.api == build.return_value
