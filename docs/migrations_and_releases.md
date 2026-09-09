# Migration and release inventory

An inventory of the Django migrations in the `meta_*` apps and of the tagged
releases in this repository.

Snapshot: 2026-09-01, branch `develop` at `d41d88f`, most recent tag `3.12.0`.

Scope: only migrations under `src/meta_*/migrations/`. Migrations belonging to
`clinicedc` / `edc_*` dependencies are not counted. The `meta_*` apps in `src/`
that have no `migrations/` directory (`meta_analytics`, `meta_auth`,
`meta_dashboard`, `meta_data_manager`, `meta_edc`, `meta_export`, `meta_labs`,
`meta_sites`, `meta_stats`, `meta_visit_schedule`) contribute nothing.

## Method

Each migration file is parsed with `ast` and the `Migration.operations` list is
read directly, rather than grepped. Grepping under-counts, because several data
migrations import the operation bare (`from django.db.migrations import
RunPython`) instead of referencing `migrations.RunPython`.

Files are then classified by the operations they actually contain:

- **schema**: `CreateModel`, `AddField`, `AlterField`, `RemoveField`,
  `DeleteModel`, `RenameField`, `RenameModel`, `AlterModelOptions`,
  `AlterUniqueTogether`, `AlterIndexTogether`, `AddIndex`, `RemoveIndex`,
  `RenameIndex`, `AddConstraint`, `RemoveConstraint`, `AlterModelManagers`,
  `AlterModelTable`, `AlterOrderWithRespectTo`, `SeparateDatabaseAndState`.
- **data**: `RunPython` or `RunSQL`.
- **db_views**: `django_db_views.operations.ViewRunPython`, which creates and
  drops SQL views. This is DDL despite the name, so it is reported in its own
  column rather than folded into either of the two above.
- **no-op**: `operations = []`. These are `..._auto_...` files Django generated
  with nothing in them.

No migration in the repository mixes schema and data operations in the same
file.

## Migrations

### Migrations by kind

| app | total | schema | data | db_views | no-op |
|---|---:|---:|---:|---:|---:|
| `meta_subject` | 256 | 232 | 21 | 0 | 3 |
| `meta_reports` | 96 | 40 | 4 | 48 | 4 |
| `meta_prn` | 78 | 69 | 7 | 0 | 2 |
| `meta_screening` | 68 | 65 | 2 | 0 | 1 |
| `meta_consent` | 36 | 32 | 3 | 0 | 1 |
| `meta_ae` | 24 | 23 | 1 | 0 | 0 |
| `meta_lists` | 22 | 20 | 2 | 0 | 0 |
| `meta_spfq` | 12 | 12 | 0 | 0 | 0 |
| `meta_pharmacy` | 10 | 7 | 2 | 0 | 1 |
| `meta_rando` | 8 | 7 | 1 | 0 | 0 |
| **total** | **610** | **507** | **43** | **48** | **12** |

### Schema migrations by app

| app | migrations | operations | dominant operations |
|---|---:|---:|---|
| `meta_subject` | 232 | 4781 | `AlterField` 3006, `AddField` 864, `RemoveField` 197 |
| `meta_prn` | 69 | 1031 | `AlterField` 651, `AddField` 113, `RemoveField` 74 |
| `meta_screening` | 65 | 1473 | `AlterField` 904, `AddField` 310, `RenameField` 173 |
| `meta_reports` | 40 | 106 | `AlterField` 37, `AddField` 24, `CreateModel` 17 |
| `meta_consent` | 32 | 217 | `AlterField` 154, `AddField` 26, `CreateModel` 10 |
| `meta_ae` | 23 | 545 | `AlterField` 429, `AddField` 40, `CreateModel` 20 |
| `meta_lists` | 20 | 245 | `AlterField` 93, `AlterModelOptions` 52, `AddIndex` 29 |
| `meta_spfq` | 12 | 112 | `AddField` 37, `RemoveField` 30, `AlterModelOptions` 18 |
| `meta_pharmacy` | 7 | 61 | `AlterField` 48, `CreateModel` 8, `RemoveField` 2 |
| `meta_rando` | 7 | 38 | `AlterField` 23, `AddField` 4, `CreateModel` 3 |
| **total** | **507** | **8609** | |

### Operation totals

| operation | count | share |
|---|---:|---:|
| `AlterField` | 5355 | 62.2% |
| `AddField` | 1441 | 16.7% |
| `RenameField` | 391 | 4.5% |
| `RemoveField` | 384 | 4.5% |
| `AlterModelOptions` | 329 | 3.8% |
| `CreateModel` | 243 | 2.8% |
| `AddIndex` | 193 | 2.2% |
| `AlterModelManagers` | 126 | 1.5% |
| `RemoveIndex` | 64 | 0.7% |
| `DeleteModel` | 31 | 0.4% |
| `RenameModel` | 18 | 0.2% |
| `AlterModelTable` | 10 | 0.1% |
| `RenameIndex` | 9 | 0.1% |
| `AlterUniqueTogether` | 8 | 0.1% |
| `AddConstraint` | 6 | 0.1% |
| `RemoveConstraint` | 1 | 0.0% |
| **total** | **8609** | |

### Schema migrations by year generated

| year | migrations |
|---|---:|
| 2019 | 39 |
| 2020 | 48 |
| 2021 | 68 |
| 2022 | 137 |
| 2023 | 10 |
| 2024 | 109 |
| 2025 | 53 |
| 2026 | 43 |

### Largest schema migrations

| operations | file |
|---:|---|
| 370 | `src/meta_subject/migrations/0161_alter_birthoutcomes_options_and_more.py` |
| 335 | `src/meta_subject/migrations/0163_alter_birthoutcomes_options_and_more.py` |
| 294 | `src/meta_subject/migrations/0228_bloodresultshba1c_hba1c_datetime_and_more.py` |
| 284 | `src/meta_prn/migrations/0067_alter_offschedule_managers_and_more.py` |
| 225 | `src/meta_subject/migrations/0231_alter_historicalmedicationadherence_consent_model_and_more.py` |
| 223 | `src/meta_subject/migrations/0229_alter_glucosefbg_consent_model_and_more.py` |
| 220 | `src/meta_ae/migrations/0023_alter_aefollowup_action_identifier_and_more.py` |
| 187 | `src/meta_subject/migrations/0230_alter_historicaldelivery_action_identifier_and_more.py` |
| 159 | `src/meta_screening/migrations/0068_alter_historicalscreeningpartone_acute_condition_and_more.py` |
| 156 | `src/meta_subject/migrations/0179_alter_birthoutcomes_consent_model_and_more.py` |

## Releases

The repository carries **313** annotated tags, of which **234** are dated on
or after 2021-12-01.

| year | tags | on/after 2021-12-01 |
|---|---:|---:|
| 2019 | 42 | 0 |
| 2020 | 21 | 0 |
| 2021 | 16 | 0 |
| 2022 | 56 | 56 |
| 2023 | 6 | 6 |
| 2024 | 46 | 46 |
| 2025 | 47 | 47 |
| 2026 | 79 | 79 |
| **total** | **313** | **234** |

The 234 releases in range run from `0.1.79` (2022-04-11) through `3.12.0`
(2026-08-27). The last release before the cut-off is `0.1.78` (2021-10-25).

## Notes

### The schema history is dominated by field alterations

`AlterField` alone accounts for 62% of all schema operations, against only 243
`CreateModel` operations in the whole history. The cause is structural rather
than clinical: `simple_history` mirrors every model with a `historical*`
counterpart, so a framework level change (widening `consent_model`, swapping a
manager, adjusting `action_identifier`) fans out across every model and its
mirror at once. The ten largest files hold 2,433 operations between them.

### Release cadence has a gap at the cut-off

There are no tags at all in December 2021. The last release before the cut-off
is `0.1.78` on 2021-10-25 and the first one on or after it is `0.1.79` on
2022-04-11, a gap of roughly five and a half months. All 313 tags are
annotated, and each tag date matches the date of the commit it points at, so
counting by tag date and by commit date gives the same answer.

The lull in 2023 (6 tags, 10 schema migrations) and the spikes in 2022 and 2024
track the clinicedc upgrade waves rippling through the project rather than
schema churn driven by the trial itself.

### Where a squash would pay

`meta_subject` holds 46% of the migrations and 56% of the schema operations. It
is the only app where a squash would meaningfully shorten a fresh `migrate`.
