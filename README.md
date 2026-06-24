### Omnexa Eng Document Control

Global document registry hub. **Reports for this app only** — sector reports stay in their own apps.

`Documants/` is documentation SSOT only; see `Documants/Bench-Docs/AUDIT/05_ARCHITECTURE_POLICY.md`.

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
