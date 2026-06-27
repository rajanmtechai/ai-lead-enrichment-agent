# Deployment Guide

## Recommended Topology

- Next.js web app on Vercel or a container host
- FastAPI API on AWS ECS, Railway, or DigitalOcean App Platform
- PostgreSQL on managed Postgres
- Redis on managed Redis or ElastiCache
- Qdrant as managed service or a separate containerized node

## Environment Setup

Set the variables from [../.env.example](../.env.example) in your deployment platform.

## Build Steps

1. Build and push the API image.
2. Run Alembic migrations against the target database.
3. Build and deploy the web image.
4. Configure webhook secrets for n8n and CRM providers.

## Operational Checks

- Verify `/healthz` on the API
- Verify login with the seeded admin account
- Confirm Qdrant collection creation on the first research run
- Review audit logs after approval and CRM sync actions