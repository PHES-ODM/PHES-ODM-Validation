# Changelog

## [Unreleased]

### General

- Added validation rule `missingness`, which identifies the missingness values
  a column can take on, as listed by its `missingnessSet`. A missingness value
  outside that set isn't a missingness value in that column, so it is left to
  the other rules to validate. Primary key columns can't contain any
  missingness value, which is the only case this rule reports, and is enforced
  even when they have no `missingnessSet`.
- Changed the rules that constrain the shape of a value (`invalid_type`,
  `invalid_category`, the min/max rules and `duplicate_entries_found`) to
  exempt a column's allowed missingness values. Type coercion is skipped for
  them as well.
- Fixed `missing_values_found` reporting a missingness value in a mandatory
  column as a missing value. A missingness value states why a value is absent
  and is a valid way of populating a mandatory column. The rule now only
  reports mandatory columns that are empty. Missingness values in identifier
  (primary key) columns are reported by the new `missingness` rule instead.

### Validation schemas

- Added `missingness` rule to the v2 schemas, and to the primary keys of the
  v1 schemas. Its `forbidden` constraint is only non-empty for primary keys
- Removed the `forbidden` constraint from the `missing_values_found` rule,
  together with its `missingness` metadata entries

## [0.6.0] - 2024-12-03

### General

- Added CLI command `odm-validate`
- Changed location of tools to `src/odm_validation/tools`
- Fixed documentation generation
- Fixed issue where empty values triggered rules "less-than-min-length" and
  "invalid_category"
- Fixed json serialization of summarized report
- Fixed misc bugs and errors

### API

- Added verbosity parameter to `_validate_data_ext`

### Validation schemas

- Added `anyof` with `empty` for fields with `allowed` or `minlength`
- Fixed boolean-set values

#### v2.0.0

- Removed tables:
    - languages
    - parts
    - sets
    - translations

## [0.5.0] - 2024-01-03

### General

- Added integration test for package import
- Added missing assets dir in package distribution
- Changed required Python version to 3.8
- Changed rule id type from string to enum
- Fixed misc bugs and errors
- Fixed table-attribute mapping in ODM version 1

### API

- Added function summarization.summarize_report for validation report
  summarization

### Tools

- Added a CLI frontend (`tools/validate.py`) for the validate_data function,
  which replaces the old validate_xlsx tool
- Added a CLI frontend (`tools/summarize.py`) for the summarize_report

### Validation schemas

#### v1.1.0

- Added CovidPublicHealthData
- Added SiteMeasure.accessToAllOrg
- Added SiteMeasure.accessToDetails
- Added SiteMeasure.accessToLocalHA
- Added SiteMeasure.accessToOtherProv
- Added SiteMeasure.accessToPHAC
- Added SiteMeasure.accessToProvHA
- Added SiteMeasure.accessToPublic
- Added SiteMeasure.accessToSelf
- Added SiteMeasure.analysisDate
- Added SiteMeasure.assayID
- Added SiteMeasure.cphdID
- Added SiteMeasure.date
- Added SiteMeasure.dateType
- Added SiteMeasure.franctionAnalysed
- Added SiteMeasure.index
- Added SiteMeasure.reportDate
- Added SiteMeasure.siteMeasureID
- Added SiteMeasure.type
- Added SiteMeasure.uWwMeasureID
- Added WWMeasure.accessToAllOrg
- Added WWMeasure.accessToDetails
- Added WWMeasure.accessToLocalHA
- Added WWMeasure.accessToOtherProv
- Added WWMeasure.accessToPHAC
- Added WWMeasure.accessToProvHA
- Added WWMeasure.accessToPublic
- Added WWMeasure.accessToSelf
- Added WWMeasure.assayID
- Added WWMeasure.cphdID
- Added WWMeasure.date
- Added WWMeasure.dateTime
- Added WWMeasure.dateType
- Added WWMeasure.siteMeasureID

## [0.4.0] - 2023-04-11

### General

- Added parameter to validate_data function for specifying spreadsheet input
- Added rule blacklist for disabling individual rules
- Added support for the final ODM v2.0.0 release
- Changed error report message format, to make it more consistent
- Fixed docs, parts and schemas

### Spreadsheet validation

- Fixed redundant coercion warnings (from string to other types)
- Fixed redundant column errors
- Fixed row numbers in the error report so that they match Excel

### Excel validation tool

- Fixed writing of empty error/warning files
- Changed output dir for csv files to decrease clutter

### Validation schemas

#### v1.1.0

- Added AssayMethod.unit.allowed
- Added SiteMeasure.siteID.maxlength
- Added WWMeasure.siteID.maxlength
- Changed Sample.pooled.allowed to [False, True]
- Removed Site.siteID
- Removed Site.type.allowed.wwtpMuS
- Removed WWMeasure.fractionAnalyzed.allowed
- Removed WWMeasure.index.coerce
- Removed WWMeasure.type.allowed

## [0.3.0] - 2023-03-10

### General

- Changed license to CC BY 4.0
- Fixed mapping of tables/attributes in ODM v1
- Fixed parts and schemas

### Excel validation tool

- Addded a summary output file
- Fixed sheet name detection
- Fixed a bug where spreadsheets with many empty lines slowed down validation

### Validation schemas

#### v1.1.0

- Added Sample.collection.allowed
- Added SiteMeasure
- Added WWMeasure.fractionAnalyzed.allowed
- Changed Sample.pooled.allowed
- Removed AssayMethod.aggregation
- Removed AssayMethod.instrumentID
- Removed AssayMethod.organization
- Removed AssayMethod.type
- Removed AssayMethod.updateDate
- Removed Instrument.index
- Removed Instrument.organization
- Removed Instrument.updateDate
- Removed Lab.organization
- Removed Lookup
- Removed Polygon.organization
- Removed Polygon.referenceLink
- Removed Polygon.updateDate
- Removed Sample.organization
- Removed Sample.siteID
- Removed Sample.updateDate
- Removed Site.organization
- Removed Site.polygonID
- Removed Site.updateDate
- Removed WWMeasure.dateTime
- Removed WWMeasure.organization
- Removed WWMeasure.polygonID
- Removed WWMeasure.referenceLink
- Removed WWMeasure.sampleID
- Removed WWMeasure.siteID
- Removed WWMeasure.updateDate
