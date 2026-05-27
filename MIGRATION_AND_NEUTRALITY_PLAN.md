# DevOps Bench: Kubernetes SIGs Migration & Neutrality Plan

This plan outlines the strategic and technical transition of the **DevOps Bench** project from a Google-owned repository (`github.com/gke-labs/devops-bench`) to a neutral, community-driven Kubernetes Special Interest Group (SIG) repository (`github.com/kubernetes-sigs/devops-bench`).

To establish `devops-bench` as the gold standard for evaluating AI agents on DevOps tasks, we must ensure that **neutrality, cloud-agnosticism, and local-first developer experiences** are core to the architecture.

---

## 🎯 Executive Summary

Moving to `kubernetes-sigs` requires transitioning from a Google Cloud/GKE-centric showcase to a pluggable, vendor-neutral benchmark framework. The goal is to enable:
1. **Equal-footing support** for local environments (KinD, Minikube), cloud-managed offerings (GKE, EKS, AKS), and hybrid setups.
2. **Community-driven development** aligning with CNCF and Kubernetes governance, including the CNCF Contributor License Agreement (CLA).
3. **A core neutral task suite** that tests vanilla Kubernetes capabilities, alongside pluggable, optional provider-specific extensions (e.g., AWS-specific or GCP-specific suites).

---

## 🔍 Gap Analysis & Remediation Strategy

| Area | Current State (Google/GKE Tied) | Target SIGs State (Neutral & Pluggable) | Status / Strategy | Priority |
| :--- | :--- | :--- | :--- | :--- |
| **Branding & Docs** | Uses GKE Reliability branding and GKE logo. | Neutral Kubernetes Reliability Engineer branding. | **In Progress** (Refactoring SKILL rubrics) | **High** |
| **Infrastructure** | Only supports `GCPDeployer` via `kubetest2 gke`. Enforces GCP project/cluster env vars. | Pluggable deployers. KinD (Kubernetes in Docker) supported out of the box. | **Completed** (Created `KinDDeployer` and updated `infra.py`) | **Critical** |
| **Core Tasks** | Tasks like `create-deployment` or `deploy-hello-app` hardcode GCP Fuse, GCP Artifact Registry, and GCS buckets. | Split tasks into a `core` (vanilla K8s) folder and provider folders (`gcp/`, `aws/`). | **Planned** (Phase 2) | **High** |
| **Evaluation Skills** | `skills/` define prompt instructions as "You are an expert GKE Reliability Engineer". | Prompt instructions say "You are an expert Kubernetes Reliability Engineer". | **In Progress** (Refactoring) | **Medium** |
| **MCP Extensions** | Defaults to `gemini-cloud-assist-mcp` and `gke-mcp` tools. | Standardized, neutral MCP spec for Kubernetes operations (`kube-mcp`). | **Planned** (Phase 4) | **Medium** |
| **Repo Imports** | Hardcoded `github.com/gke-labs/devops-bench` in go/python imports/docs. | Neutral `github.com/kubernetes-sigs/devops-bench` imports. | **Planned** (Phase 1) | **High** |

---

## 🛠️ Completed Immediate Remediations

We have already implemented several critical technical modifications to neutralize the codebase:

### 1. Local Cluster Support via KinD Deployer
We created a brand new **`KinDDeployer`** located at `deployers/kind/kind_deployer.py`. This allows any contributor to spin up a standard Kubernetes-in-Docker cluster locally.
* **Zero-cloud footprint**: Requires no cloud credentials, no billing, and runs in under 60 seconds.
* **Integrated into infra CLI**: Added `kind` support directly to the provisioning manager `scripts/infra.py`.
  
  ```bash
  # Provision local KinD cluster
  python3 scripts/infra.py kind up
  
  # Check cluster status
  python3 scripts/infra.py kind info
  
  # Tear down
  python3 scripts/infra.py kind down
  ```

### 2. Neutralized Configuration & Environment Loading
We refactored the core evaluation engine in `pkg/evaluator/evaluate.py`:
* `GCP_PROJECT_ID` and `GKE_CLUSTER_NAME` are **no longer mandatory** environment variables.
* If `CLOUD_PROVIDER` is set to `kind` or any other local/neutral provider, the evaluator skips GCP checks and supplies neutral fallback context values (`local-project` and `local-cluster`).

---

## 📦 Phase-by-Phase Implementation Plan

### Phase 1: Sig Onboarding & Repository Move
1. **SIG Sponsorship**: Present the proposal to the relevant Kubernetes SIG (likely **SIG Usability** or **SIG Architecture / Conformance**).
2. **Transfer Request**: Open an issue on the `kubernetes/org` repository requesting the creation of `kubernetes-sigs/devops-bench` and project transfer.
3. **License & CLA**: Confirm the Apache 2.0 License is clean. Ensure all future PRs require the standard Linux Foundation / CNCF DCO (Developer Certificate of Origin) or CLA sign-off.
4. **Global Import Rename**: Search and replace all instances of `github.com/gke-labs/devops-bench` with `github.com/kubernetes-sigs/devops-bench`.

### Phase 2: Split Task Suite (Core vs. Provider-Specific)
Currently, core benchmark tasks are deeply intertwined with GKE/GCP capabilities. We should split them into a clean hierarchy:

```
tasks/
├── core/                    # Vanilla K8s tasks (runs on KinD, Minikube, any cloud)
│   ├── create-deployment/   # Uses standard volumes & deployment
│   ├── deploy-hello-app/    # Uses public registries and standard Secrets
│   └── modify-deployment/   # Standard scaling, resource requests/limits
└── providers/               # Cloud/vendor specific tasks
    ├── gcp/                 # Uses GKE-specific annotations (GCS Fuse, ComputeClasses)
    └── aws/                 # (Future) Uses EKS-specific features
```

### Phase 3: Neutralize Evaluation Prompting
Update prompt instructions in `skills/` directory to remove any cloud vendor bias:
* Refactor **`skills/outcome-validity-skill.md`**
* Refactor **`skills/outcome-validity-checklist.md`**
* Refactor **`skills/tool-invocation-skill.md`**

*Change from:*
> "You are an expert GKE Reliability Engineer evaluating..."

*Change to:*
> "You are an expert Kubernetes Reliability Engineer evaluating..."

### Phase 4: Open MCP Specification
Define a standard, open **Model Context Protocol (MCP) schema** for Kubernetes operations (e.g. `kube-mcp` or similar). Instead of locking agents into using proprietary tools, publish a clear OpenAPI / MCP spec that any community-developed Kubernetes agent can implement.

---

## 🚀 Next Steps

1. **Review and Merge**: Check in this migration plan and the completed `KinDDeployer` implementations.
2. **SIG DevOps / Usability Discussion**: Share this document with the steering committee of the sponsoring SIG.
3. **GitHub Org Issue**: Open the transfer request issue once SIG approval is granted.
