# tap-suiteql

`tap-suiteql` is a Singer tap for Netsuite SuiteQL API.

Built with the [Meltano Tap SDK](https://sdk.meltano.com) for Singer Taps.

## Installation

- [ ] `Developer TODO:` Update the below as needed to correctly describe the install procedure. For instance, if you do not have a PyPi repo, or if you want users to directly install from your git repo, you can modify this step as appropriate.

```bash
pipx install tap-suiteql
```

## Configuration

### Accepted Config Options

- [ ] `Developer TODO:` Provide a list of config options accepted by the tap.

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-suiteql --about
```

### Configure using environment variables

This Singer tap will automatically import any environment variables within the working directory's
`.env` if the `--config=ENV` is provided, such that config values will be considered if a matching
environment variable is set either in the terminal context or in the `.env` file.

### Source Authentication and Authorization

- [ ] `Developer TODO:` If your tap requires special access on the source system, or any special authentication requirements, provide those here.

## Usage

You can easily run `tap-suiteql` by itself or in a pipeline using [Meltano](https://meltano.com/).

### Executing the Tap Directly

```bash
tap-suiteql --version
tap-suiteql --help
tap-suiteql --config CONFIG --discover > ./catalog.json
```

## Developer Resources

- [ ] `Developer TODO:` As a first step, scan the entire project for the text "`TODO:`" and complete any recommended steps, deleting the "TODO" references once completed.

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```

### Create and Run Tests

Create tests within the `tap_suiteql/tests` subfolder and
  then run:

```bash
poetry run pytest
```

You can also test the `tap-suiteql` CLI interface directly using `poetry run`:

```bash
poetry run tap-suiteql --help
```

### Testing with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano.
Examples here are for convenience and to streamline end-to-end orchestration scenarios._

Your project comes with a custom `meltano.yml` project file already created. Open the `meltano.yml` and follow any _"TODO"_ items listed in
the file.

Next, install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-suiteql
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Test invocation:
meltano invoke tap-suiteql --version
# OR run a test `elt` pipeline:
meltano elt tap-suiteql target-jsonl
```

### Adding Streams
There are 2 ways in which we can map entities in this tap

the first is discovering there schema by using the meta-data suiteql endpoint (dinamically), and the second is by manually mapping the properties on the stream (static).
We extract the following entities with its respective method
* Subscription -> dynamically
* Customer -> dinamically
* Invoice -> dinamically
* SubscriptionLine -> dinamically
* SubscriptionPriceInterval -> static
* SubscriptionPlanStream -> dinamically
* ChangeOrderLine -> static
* CustomerPayment -> static
* CustomlistGpyCompanysize -> dinamically
* CustomlistGpyReadjustmentindex -> dinamically
* SubscriptionChangeOrder -> static

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to
develop your own taps and targets.
