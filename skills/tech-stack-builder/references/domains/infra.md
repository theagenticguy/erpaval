# Infrastructure Domain

## Categories

- **Containerization**: Docker with BuildKit (default), Podman, etc.
- **Orchestration** (RESEARCH): ECS Fargate, EKS, Docker Compose, Nomad, etc. — depends on scale and ops capacity
- **Infrastructure as Code** (RESEARCH): AWS CDK, Pulumi, Terraform/OpenTofu, SAM, CloudFormation — depends on cloud and team
- **CI/CD**: GitHub Actions (default), GitLab CI, CircleCI, Dagger, etc.
- **Observability**: OpenTelemetry (default) + backend selection (RESEARCH): Grafana stack, Datadog, AWS CloudWatch, Honeycomb, etc.
- **Service Mesh** (RESEARCH if microservices): AWS App Mesh, Istio, Linkerd, Consul Connect — only if microservices architecture
- **Secret Management** (RESEARCH): AWS Secrets Manager, HashiCorp Vault, SOPS, doppler, infisical, etc.
- **Dev Tool Management**: mise (default)

## Conditional Logic

| Condition                     | Action                                         |
| ----------------------------- | ---------------------------------------------- |
| Single service / monolith     | Skip service mesh entirely                     |
| Serverless-only deployment    | Skip orchestration, minimal container research |
| "No Kubernetes" in avoid list | Exclude EKS from orchestration candidates      |
| Team size < 5                 | Favor simpler IaC (CDK) over Terraform         |
| Multi-cloud requirement       | Favor Terraform/Pulumi over CDK                |
| AWS-only                      | Favor CDK                                      |

## IaC Evaluation Context

| Signal                       | Leans Toward          |
| ---------------------------- | --------------------- |
| AWS-only, TypeScript team    | AWS CDK               |
| AWS-only, serverless focus   | AWS CDK or SAM        |
| Multi-cloud or hybrid        | Terraform / OpenTofu  |
| General-purpose, TypeScript  | Pulumi                |
| Simple AWS deployments       | SAM or CloudFormation |
| Team already knows Terraform | Terraform / OpenTofu  |

## Domain-Specific Artifacts

Provide:

- `Dockerfile` skeleton (if containers are recommended)
- `mise.toml` snippet with tool versions and tasks
- CI/CD workflow skeleton (e.g., `.github/workflows/ci.yml` outline)

## Container Security Tooling

| Tool        | Purpose                                                     | Default                |
| ----------- | ----------------------------------------------------------- | ---------------------- |
| hadolint    | Dockerfile linting (best practices + ShellCheck)            | Default                |
| grype       | Container image vulnerability scanning (EPSS + KEV scoring) | Default                |
| trivy image | Container image scanning (vulns + misconfig + secrets)      | Default                |
| cosign      | Keyless container image signing (Sigstore OIDC)             | Default for production |
| checkov     | IaC scanning (Terraform, CloudFormation, K8s, Dockerfiles)  | Default                |
| syft        | SBOM generation (CycloneDX + SPDX)                          | Default                |

See `references/stacks/shared/containers.md` for Dockerfile templates and tool configuration.

## Additional Quality Checks

- [ ] Conditional logic applied (skipped irrelevant categories)
- [ ] License implications noted (especially Terraform BSL)
- [ ] Container security tools included if containers in stack
