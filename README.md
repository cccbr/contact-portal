# Bell Ringing Contact Portal

**Multi Use Server Side Portal for Ringing 2030 Contact forms**

Support for forms built into static sites.

## Data Model

Any form using this portal, must post data matching the schema, otherwise it will be rejected and may be lost.

See [SCHEMA.md](SCHEMA.md)

## Integration

To integrate with the Portal, you must come from an approved domain, and if you are using Content-Security-Policies, you must register the portal instance within your HTTP server, otherwise you cannot post data.
Instance Details: 

## Development

This project uses virtualenv for dependency management, tox as a test runner and playright for acceptance testing

To set up your development environment, create and activate a virtualenv, if required.

Install the development dependencies: `pip install -r requirements.txt`

### Testing

#### Unittest with Coverage

#### Acceptance Testing

Deploy Fast API and test with Playwright

Install Playwright: `playwright install`
Deploy Portal: `fastapi run portal/main.py`, ensure server starts
Launch Tests: `pytest test_portal`
You can now terminate the fastapi server

##### Types

Type checking uses `mypy` # TODO - Not working yet

Install Types: `pip install -r requirements-mypy.txt`

Check Types: `mypy portal --config-file=tox.ini`
