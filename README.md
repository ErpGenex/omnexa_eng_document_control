### Omnexa Eng Document Control

Document control extraction stub. Depends on `omnexa_engineering_consulting`; use `consulting_bridge.get_document_control_hooks()` to reach `document_control_hooks` until DocTypes move here.

### Installation

You can install this app using the [bench](https://github.com/frappe/bench) CLI:

```bash
cd $PATH_TO_YOUR_BENCH
bench get-app $URL_OF_THIS_REPO --branch develop
bench install-app omnexa_eng_document_control
```

### Contributing

This app uses `pre-commit` for code formatting and linting. Please [install pre-commit](https://pre-commit.com/#installation) and enable it for this repository:

```bash
cd apps/omnexa_eng_document_control
pre-commit install
```

Pre-commit is configured to use the following tools for checking and formatting your code:

- ruff
- eslint
- prettier
- pyupgrade

### License

mit
