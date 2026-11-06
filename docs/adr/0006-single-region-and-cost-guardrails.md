# 0006. Use a single AWS region and cost guardrails

- **Date:** 2026-11-06
- **Status:** Accepted

## Context

This is a personal project on a new AWS account, with a budget close to zero. Resources spread across regions are easy to forget, and they keep costing money. Region-specific settings (CodeBuild's `AWS_DEFAULT_REGION`, ECR registry URIs, S3 bucket locations) also break when resources live in different regions.

## Decision

We will run everything in **`eu-north-1`**, with these guardrails:
- an AWS Budgets alert at **$1**
- lifecycle rules on ECR (expire old images) and S3 (abort incomplete uploads; expire old model versions once they exist)
- the smallest CodeBuild compute size (`general1.small`), so builds stay within the free minutes
- for Phase 5, a single-instance Elastic Beanstalk environment with no load balancer, terminated during breaks of a week or more

## Consequences

- A forgotten resource is easy to find, because there's only one region to check.
- Some services or features may not be available in `eu-north-1`. **Check before starting Phase 5 (Elastic Beanstalk) and Phase 7 (SageMaker).** If something is missing, either use a fallback (Lambda with the ECR image) or write a new ADR for a second region.
- The $1 alert goes off early. That's intended: it's a tripwire, not a spending limit.
- An idle environment has to be terminated by hand. Write that down as a step when pausing work.
