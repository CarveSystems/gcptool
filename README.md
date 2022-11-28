# Carve Systems GCP Assessment Tooling

## Installation

This tool requires Python 3.8 or newer.

Additionally, the [`gcloud` CLI](https://cloud.google.com/sdk/docs/install) is required for authentication against Google user accounts.

## Usage

### Prerequisites

To use this tool against a Google Cloud environment, you must be have a user account with the `Security Reviewer` role granted across all relevant projects. The use of a service account with these permissions is recommended if possible; regular user accounts are subject to stricter rate-limiting by Google.

Currently, gcptool authenticates using Google Application Default Credentials. If you are using a regular user account for testing, the `gcloud auth application-default login` command will properly configure credentials for you. In the case of a service account, setting the `GOOGLE_APPLICATION_CREDENTIALS` environment variable to a path containing a service account keypair will be required.

You can verify access is working correctly using two commands within the tool; `gcptool list-projects` will print a list of projects you can currently access, and `gcptool check <PROJECT-NAME>` will verify your account has the necessary set of permissions to perform all scans.


### Running Tests

Once you've verified access, the `gcptool scan` command can be used to perform testing. To run a basic scan, the command can be used as follows:

`gcptool scan PROJECT-NAME,PROJECT-NAME-2 path/to/report/findings/folder`

This will produce several outputs:

- A JSON inventory of Google Cloud Resources in `gcptool_cache.json` in the current directory (NOTE: this file should be handled with care, as it may contain sensitive information)
- CDPS-format Markdown findings ready for editing and use in a report (Note that some of these are guidance to possible points of interest for manual testing)
- `gcptool.log` log file with more detailed information

gcptool will use the generated cache file when possible to avoid making extraneous API requests; the `--cache-only` option can be used to exit with an error if any scan would required fresh data from the API. This is convenient, for example, to run new scans against already-collected data.

Other useful arguments are:

- `--service`: only run scans for a specific GCP service. For example, `--scan compute` will only run Compute Engine tests.
- `--scan`: only run a specific scan. One particularly useful use for this argument is `--scan inventory`, which will gather data or a complete cache file but will not run any analysis. (`gcptool list-scans` provides a helpful list of scans and services)

## Development

### Development dependencies

Code formatting is handled using the [pre-commit](https://pre-commit.com/) tool. Please install and configure it before making any commits!
