# MLOps: Portuguese electricity demand forecaster

Forecasts the next 24 hours of electricity demand, hour by hour. It's trained on real Portuguese smart-meter data, retrained automatically, and deployed on AWS through a CI/CD pipeline.

## Docs

- [Product requirements and roadmap](docs/prd/0001-demand-forecaster.md)
- [Architecture decisions (ADRs)](docs/adr/README.md)
- [GitHub workflow: issues, branches and PRs](docs/github-workflow.md)
- [Instructions for AI agents](AGENTS.md)

## Data

- Source: UCI ElectricityLoadDiagrams20112014 (CC BY 4.0), Trindade, A. (2015), https://doi.org/10.24432/C58C86
- Versioning: DVC, with its remote in the project's S3 bucket ([ADR-0008](docs/adr/0008-version-data-with-dvc.md)). Run `dvc pull` to fetch the data once it's tracked (plan step 1.5).
- SHA256 of the original UCI download (`electricityloaddiagrams20112014.zip`): `F6C4D0E0DF12ECDB9EA008DD6EEF3518ADB52C559D04A9BAC2E1B81DCFC8D4E1`
