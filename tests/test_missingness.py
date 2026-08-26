import unittest

from parameterized import parameterized

import odm_validation.odm as odm
from odm_validation.reports import ErrorKind, get_error_kind
from odm_validation.rules import RuleId
from odm_validation.schemas import import_schema
from odm_validation.utils import import_dataset, import_json_file
from odm_validation.validation import (
    _generate_validation_schema_ext,
    _validate_data_ext,
)

import common
from common import asset, gen_v2_testschemas, param_range


class Assets():
    def __init__(self, rule_id: RuleId):
        rule_dirname = rule_id.name.replace('_', '-')
        common.ASSET_SUBDIR = f'validation-rules/{rule_dirname}'

        # parts and sets
        self.parts = import_dataset(asset('parts.csv'))
        self.sets = import_dataset(asset('sets.csv'))

        # schemas
        v2_schema = import_schema(asset('schema-v2.yml'))
        self.schemas = gen_v2_testschemas(v2_schema)
        self.schemas['1.0.0'] = import_schema(asset('schema-v1.yml'))

        # datasets and error reports
        self.data_pass = {
            'sites': import_dataset(asset('valid-dataset.csv')),
            'samples': import_dataset(asset('valid-dataset-samples.csv')),
        }
        self.data_fail = {}
        self.reports = {}
        for i in range(1, 2):
            self.data_fail[i] = \
                {'sites': import_dataset(asset(f'invalid-dataset-{i}.csv'))}
            self.reports[i] = import_json_file(asset(f'error-report-{i}.json'))


def get_error_ids(report) -> list[tuple]:
    """Returns a (rule-id, column, row) tuple per error and warning in
    `report`."""
    result = []
    for e in (report.errors + report.warnings):
        kind = get_error_kind(e)
        rule_name = e[kind.value + 'Type']
        result.append((rule_name, e['columnName'], e['rowNumber']))
    return result


class TestMissingness(common.OdmTestCase):
    rule_id = RuleId.missingness

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.assets = Assets(cls.rule_id)
        cls.whitelist = [cls.rule_id]

    @parameterized.expand(['1.0.0'] + odm.CURRENT_VERSION_STRS)
    def test_schema_generation(self, vstr):
        result = _generate_validation_schema_ext(parts=self.assets.parts,
                                                 sets=self.assets.sets,
                                                 schema_version=vstr,
                                                 rule_whitelist=self.whitelist)
        self.assertDictEqual(self.assets.schemas[vstr], result)

    @parameterized.expand(odm.CURRENT_VERSION_STRS)
    def test_passing_datasets(self, vstr):
        report = _validate_data_ext(self.assets.schemas[vstr],
                                    self.assets.data_pass)
        self.assertTrue(report.valid())

    @parameterized.expand(param_range(1, 2))
    def test_failing_datasets(self, i):
        report = _validate_data_ext(schema=self.assets.schemas['2.0.0'],
                                    data=self.assets.data_fail[i])
        expected = self.assets.reports[i]
        self.assertReportEqual(expected, report)

    def test_rule_without_sets(self):
        '''without the contents of the missingness sets, the rule can only be
        generated for the primary keys, which can't have missingness values
        anyway'''
        result = _generate_validation_schema_ext(parts=self.assets.parts,
                                                 schema_version='2.0.0',
                                                 rule_whitelist=self.whitelist)
        self.assertEqual(['sites'], list(result['schema']))
        columns = result['schema']['sites']['schema']['schema']
        self.assertEqual(['siteID'], list(columns))
        self.assertEqual({'allowed': [], 'forbidden': ['NA', 'nan', 'nr']},
                         columns['siteID']['missingness'])


class TestMissingnessExemption(common.OdmTestCase):
    '''An allowed missingness value must not trigger any of the other
    validation rules, not even in a mandatory column.'''

    @classmethod
    def setUpClass(cls):
        cls.maxDiff = None
        cls.assets = Assets(RuleId.missingness)
        # `geoLat` is a mandatory float column with the `nrNAMissingnessSet`
        # missingness set, so all rules are relevant for it
        cls.schema = _generate_validation_schema_ext(
            parts=cls.assets.parts, sets=cls.assets.sets,
            schema_version='2.0.0')

    def test_allowed_values(self):
        report = _validate_data_ext(self.schema,
                                    {'sites': self.assets.data_pass['sites']})
        self.assertEqual([], report.errors)
        self.assertEqual([], get_error_ids(report))

    def test_identifier(self):
        '''an identifier can't take on any missingness value'''
        data = {'sites': [{'siteID': 'NA', 'geoLat': 1.0, 'country': 'CA'}]}
        report = _validate_data_ext(self.schema, data)
        self.assertEqual([('missingness', 'siteID', 1)],
                         get_error_ids(report))
        self.assertEqual(ErrorKind.ERROR, get_error_kind(report.errors[0]))

    def test_values_outside_the_set(self):
        '''a missingness value that isn't allowed isn't a missingness value in
        that column, so the other rules decide whether it's valid'''
        data = {'sites': [{'siteID': '1', 'geoLat': 1.0, 'country': 'NA'},
                          {'siteID': '2', 'geoLat': 1.0, 'country': 'nan'}]}
        report = _validate_data_ext(self.schema, data)
        # `NA` is a legitimate country code, while `nan` is too long
        self.assertEqual([('greater_than_max_length', 'country', 2)],
                         get_error_ids(report))

    def test_missing_mandatory_value(self):
        '''an empty value in a mandatory column is still missing, even when
        the column can take on missingness values'''
        data = {'sites': [{'siteID': '', 'geoLat': 1.0}]}
        report = _validate_data_ext(self.schema, data)
        self.assertEqual([], report.errors)
        self.assertEqual([('missing_values_found', 'siteID', 1)],
                         get_error_ids(report))


if __name__ == '__main__':
    unittest.main()
