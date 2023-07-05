# SaaS Subscription Dashboard

A modular monolith SaaS subscription management platform built with **FastAPI** and **React**, featuring Stripe/PayPal payment integration and AI-powered business insights.

## Architecture

- **Backend**: FastAPI (Python 3.11) — Service-Repository pattern, Pydantic v2, async SQLAlchemy
- **Frontend**: React 18 + TypeScript — Feature-based architecture, TanStack Query, Recharts
- **Database**: PostgreSQL 16, Redis 7
- **Payments**: Stripe & PayPal (Strategy pattern)
- **AI**: OpenAI GPT-4o for business insights

## Quick Start

```bash
# Clone and start infrastructure
make up

# Backend
cd backend && pip install -e ".[dev]"
alembic upgrade head
uvicorn app.main:app --reload

# Frontend
cd frontend && npm install && npm run dev
```

## Project Structure

```
backend/app/
  modules/          # Domain modules (auth, billing, subscriptions, analytics, ai_insights)
  middleware/        # Request logging, rate limiting, CORS, error handling
  shared/           # Database, security, pagination, idempotency
  tasks/            # Background workers (webhook retry, subscription sync)

frontend/src/
  features/         # Feature modules (auth, billing, dashboard, insights)
  shared/           # Atomic design components, hooks, utilities
  pages/            # Page-level compositions
```

## API Endpoints

| Module          | Endpoint                           | Method |
|-----------------|------------------------------------|--------|
| Auth            | `/api/v1/auth/register`            | POST   |
| Auth            | `/api/v1/auth/login`               | POST   |
| Auth            | `/api/v1/auth/refresh`             | POST   |
| Auth            | `/api/v1/auth/me`                  | GET    |
| Billing         | `/api/v1/billing/plans`            | GET    |
| Billing         | `/api/v1/billing/subscriptions`    | POST   |
| Billing         | `/api/v1/billing/invoices`         | GET    |
| Subscriptions   | `/api/v1/subscriptions/detail`     | GET    |
| Subscriptions   | `/api/v1/subscriptions/change-plan`| POST   |
| Analytics       | `/api/v1/analytics/dashboard`      | GET    |
| AI Insights     | `/api/v1/insights/generate`        | GET    |
| AI Insights     | `/api/v1/insights/ask`             | POST   |
| Webhooks        | `/webhooks/stripe`                 | POST   |
| Webhooks        | `/webhooks/paypal`                 | POST   |

## License

MIT
