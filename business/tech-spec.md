# tech‑spec.md – **api‑sentry v1**

---

## 1. Stack  

| Layer | Choice | Rationale |
|-------|--------|-----------|
| **Language** | **Go 1.22** | Compiled binary → low cold‑start, cheap compute, excellent concurrency for polling many LLM endpoints. |
| **Web framework** | **Fiber (v2)** | Minimal overhead, familiar Express‑style routing, built‑in middleware for logging, rate‑limiting, JWT. |
| **ORM / DB driver** | **Ent (v0.13)** + **pgx** | Type‑safe schema generation, migrations as code, native PostgreSQL driver. |
| **Message queue** | **NATS JetStream** (optional for async alert dispatch) | Light‑weight, works on free tier of Fly.io/Render, decouples alert delivery from monitor polling. |
| **Runtime** | **Docker 20.10** (scratch + distroless) | Guarantees reproducible builds, easy to run on any container host. |
| **Testing** | **Testify**, **GoMock**, **httptest** | Unit + integration coverage ≥ 80 %. |
| **Lint/format** | **golangci‑lint**, **gofmt** | Enforce code quality automatically in CI. |

---

## 2. Hosting (free‑tier‑first)

| Component | Provider (Free Tier) | Deployment Model | Cost‑Control |
|-----------|----------------------|------------------|--------------|
| **API service** | **Fly.io** (Free VM ‑ 256 MiB RAM, 3 GB outbound) | Docker container, auto‑scale to 1 instance, region‑aware (US‑East, EU‑West) | Scale to 2‑node “pay‑as‑you‑go” after 30 days if > 10 k requests/day. |
| **PostgreSQL** | **Supabase** (Free tier: 500 MB, 2 GB bandwidth) | Managed PG‑14, SSL‑only. | Upgrade to hobby tier at $25/mo if > 5 M rows. |
| **Message queue** | **NATS Cloud** (Free tier: 1 GB storage, 10 k msgs/s) | Managed JetStream. | Fallback to in‑process queue if limit reached. |
| **Static assets (docs, UI)** | **Vercel** (Free) | Next.js static export, CDN edge. | Auto‑prune after 30 days of inactivity. |
| **CI/CD** | **GitHub Actions** (Free for public repos) | Build → Docker → Fly Deploy. | Use caching to stay under 2000 min/month. |

*All secrets are stored in the provider’s secret manager (Fly Secrets, Supabase env, GitHub Encrypted Secrets).*

---

## 3. Data Model  

| Table / Collection | Key Fields | Description |
|--------------------|------------|-------------|
| **users** | `id (uuid PK)`, `email (unique)`, `hashed_pwd`, `created_at` | Account owners. |
| **api_keys** | `id (uuid PK)`, `user_id (FK)`, `key (string, secret)`, `name`, `created_at`, `revoked_at` | Auth token for API calls. |
| **monitors** | `id (uuid PK)`, `user_id (FK)`, `name`, `target_url`, `method (GET/POST)`, `headers (json)`, `payload_template (json)`, `interval_sec`, `timeout_ms`, `created_at`, `last_check_at`, `status (UP/DOWN/DEGRADED)` | Definition of a LLM endpoint to watch. |
| **checks** | `id (uuid PK)`, `monitor_id (FK)`, `started_at`, `ended_at`, `latency_ms`, `http_status`, `error_msg (nullable)`, `response_hash (sha256)` | Raw poll results (retention 30 days). |
| **alert_rules** | `id (uuid PK)`, `monitor_id (FK)`, `type (latency|error_rate|status)`, `threshold`, `window_sec`, `notify_via (email|slack|webhook)`, `target (string)`, `created_at` | Conditions that trigger alerts. |
| **alerts** | `id (uuid PK)`, `monitor_id (FK)`, `rule_id (FK)`, `triggered_at`, `resolved_at (nullable)`, `severity (low|medium|high)`, `payload (json)` | Instances of a rule firing. |
| **audit_log** | `id (uuid PK)`, `user_id (FK)`, `action`, `resource_type`, `resource_id`, `timestamp`, `ip_addr` | Immutable trail for compliance. |

*All tables use `uuid_generate_v4()` for PKs. JSONB columns enable flexible payload storage without schema churn.*

---

## 4. API Surface  

| Method | Path | Auth | Purpose | Request Body (JSON) | Response (JSON) |
|--------|------|------|---------|---------------------|-----------------|
| **POST** | `/v1/api-keys` | JWT (user) | Create a new API key for the caller. | `{ "name": "prod‑key" }` | `{ "key": "sk_…", "id": "...", "created_at": "…" }` |
| **GET** | `/v1/api-keys` | JWT | List caller’s API keys (masked). | – | `[{ "id":"…","name":"…","created_at":"…","masked":"sk_****"}]` |
| **POST** | `/v1/monitors` | API‑Key | Register a new LLM endpoint monitor. | `{ "name":"ChatGPT‑4", "target_url":"https://api.openai.com/v1/chat/completions", "method":"POST", "headers":{ "Authorization":"Bearer …" }, "payload_template":{ "model":"gpt-4","messages":[{"role":"user","content":"{{prompt}}"}] }, "interval_sec":60, "timeout_ms":5000 }` | `{ "id":"…","status":"CREATED","next_check_at":"…" }` |
| **GET** | `/v1/monitors` | API‑Key | List all monitors owned by the key. | – | `[{ "id":"…","name":"…","status":"UP","latency_ms":123,"last_check_at":"…" }]` |
| **GET** | `/v1/monitors/{id}` | API‑Key | Retrieve detailed monitor status & recent checks. | – | `{ "monitor":{…}, "recent_checks":[{…}] }` |
| **PUT** | `/v1/monitors/{id}` | API‑Key | Update monitor config (partial). | `{ "interval_sec":30 }` | `{ "id":"…","updated_at":"…" }` |
| **DELETE** | `/v1/monitors/{id}` | API‑Key | Delete monitor (soft‑delete). | – | `{ "deleted":true }` |
| **POST** | `/v1/alert-rules` | API‑Key | Create an alert rule for a monitor. | `{ "monitor_id":"…","type":"latency","threshold":2000,"window_sec":300,"notify_via":"slack","target":"https://hooks.slack.com/…"} ` | `{ "id":"…","created_at":"…" }` |
| **GET** | `/v1/alerts` | API‑Key | List active alerts (filter by severity). | `?severity=high` | `[{ "id":"…","monitor_id":"…","severity":"high","triggered_at":"…"}]` |
| **POST** | `/v1/webhooks/receive` | None (public) | Endpoint for external services (e.g., Slack) to acknowledge alert actions. | `{ "alert_id":"…","action":"acknowledge"} ` | `{ "status":"ok" }` |
| **GET** | `/healthz` | None | Liveness / readiness probe. | – | `{ "status":"ok","uptime_sec":12345 }` |

*All non‑GET endpoints require **API‑Key** header `X-Api-Key`. Rate‑limit: 100 req/s per key (burst 200).*

---

## 5. Security Model  

| Aspect | Implementation |
|--------|----------------|
| **Authentication** | API keys are **HMAC‑SHA256** signed tokens (`sk_` prefix). Stored hashed with **bcrypt(12)**. JWT (access token) only for UI login; short‑lived (15 min) with refresh token rotation. |
| **Authorization (IAM)** | Row‑level security (RLS) enforced by PostgreSQL: each query filters by `user_id` derived from the API key. No cross‑tenant data leakage. |
| **Transport** | All inbound/outbound traffic forced over **TLS 1.3**. HTTP Strict Transport Security (HSTS) header set. |
| **Secret Management** | - LLM provider keys & internal API keys kept in **Fly Secrets** (encrypted at rest). <br> - Slack/webhook URLs stored encrypted with **AWS KMS**‑compatible envelope (via `github.com/aws/aws-sdk-go-v2/kms`). |
| **Input Validation** | - JSON schema validation on `payload_template` and monitor definitions (using `gojsonschema`). <br> - Strict whitelist of allowed HTTP methods (GET/POST). |
| **Audit & Compliance** | Immutable `audit_log` table; write‑only from application layer. Exportable CSV for SOC‑2 style review. |
| **Pen‑test / Hardening** | - Dependency scanning via **GitHub Dependabot** and **Trivy**. <br> - Container built from **distroless** base, no shell. |
| **DDoS Mitigation** | Fly.io edge rate‑limiting (default 10 k req/min per IP) + per‑key quota. |

---

## 6. Observability  

| Signal | Tooling | Export |
|--------|---------|--------|
| **Logs** | `zerolog` (JSON) → stdout → captured by Fly.io logs. Include request ID, user ID, monitor ID, latency, error. | Centralised in **Logtail** (Fly) + optional **Grafana Loki** via webhook. |
| **Metrics** | **Prometheus client** (`github.com/prometheus/client_golang`). Exported at `/metrics`. Key metrics: <br> - `api_sentry_monitor_up_total` (counter) <br> - `api_sentry_monitor_latency_seconds` (histogram) <br> - `api_sentry_alerts_fired_total` (counter) <br> - `api_sentry_requests_total` (counter with labels `method,endpoint,status`). | Scraped by **Fly.io Prometheus** integration; can be forwarded to **Grafana Cloud** (free tier). |
| **Traces** | **OpenTelemetry** (Go SDK) → **OTLP** exporter to **Jaeger** (hosted on Fly.io free tier). | End‑to‑end request trace from API ingress → monitor poll → alert dispatch. |
| **Health** | `/healthz` returns JSON + Prometheus `up` metric. | Monitored by Fly.io health checks. |
| **Alerting** | **Prometheus Alertmanager** rules: latency > threshold, error_rate > 5 % over 5 min → send to Slack channel `#api-sentry-ops`. | Ops team notified via existing incident pipeline. |

---

## 7. Build / CI  

```yaml
# .github/workflows/ci.yml
name: CI / CD

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  lint-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Set up Go
        uses: actions/setup-go@v5
        with:
          go-version: '1.22'
      - name: Cache modules
        uses: actions/cache@v3
        with:
          path: |
            ~/.cache/go-build
            ~/go/pkg/mod
          key: ${{ runner.os }}-go-${{ hashFiles('go.sum') }}
      - name: Lint
        run: golangci-lint run ./...
      - name: Unit tests
        run: go test ./... -coverprofile=cover.out
      - name: Upload coverage
        uses: actions/upload-artifact@v4
        with:
          name: coverage
          path: cover.out

  build-docker:
    needs: lint-test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Login to Docker Hub
        uses: docker/login-action@v3
        with:
          username: ${{ secrets.DOCKERHUB_USER }}
          password: ${{ secrets.DOCKERHUB_TOKEN }}
      - name: Build image
        run: |
          docker build -t ghcr.io/arkashira/api-sentry:${{ github.sha }} .
      - name: Push to GitHub Container Registry
        run: |
          docker push ghcr.io/arkashira/api-sentry:${{ github.sha }}

  deploy-fly:
    needs: build-docker
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    steps:
      - uses: actions/checkout@v4
      - name: Install Flyctl
        run: |
          curl -L https://fly.io/install.sh | sh
          export PATH=$HOME/.fly/bin:$PATH
      - name: Deploy
        env:
          FLY_API_TOKEN: ${{ secrets.FLY_API_TOKEN }}
        run: |
          flyctl deploy --image ghcr.io/arkashira/api-sentry:${{ github.sha }} --remote-only
```

*Key CI steps*  

1. **Static analysis** – `golangci-lint` (all linters).  
2. **Unit + integration tests** – `go test ./...` with a Docker‑compose Postgres fixture.  
3. **Docker build** – multi‑stage: `builder` (golang) → `distroless` final image (~30 MB).  
4. **Container scan** – `trivy image` (fails on CVE > 7).  
5. **Deploy** – Fly.io `flyctl` with zero‑downtime rolling release.  

---

### End of Document

*All sections are version‑controlled in the `tech-spec.md` file at the repo root. Future iterations should update the **Data Model** and **API Surface** as new alert rule types (e.g., token‑quota, response‑schema drift) are added.*