# AWS Domain

**Important**: If the project requirements indicate a non-AWS deployment target (GCP, Azure, self-hosted), respond with a brief note that AWS research is not applicable and skip all research.

## Categories

- **Compute** (RESEARCH): Lambda, ECS Fargate, App Runner, EC2, EKS — depends on workload pattern
- **Database** (RESEARCH): Aurora (PostgreSQL/MySQL), DynamoDB, RDS, ElastiCache/Valkey, Neptune, Timestream, MemoryDB — depends on data model
- **Storage**: S3 (default), EFS, EBS — S3 is almost always the right choice for object storage
- **CDN**: CloudFront (default)
- **Messaging**: SQS (default), SNS, EventBridge, Kinesis, MSK — SQS for simple queuing, research for event-driven patterns
- **API Layer** (RESEARCH): API Gateway (REST/HTTP/WebSocket), ALB, AppSync, CloudFront Functions — depends on API style
- **Auth** (RESEARCH): Cognito, IAM Identity Center, custom with JWT — depends on user model
- **DNS**: Route 53 (default)
- **AI/ML** (RESEARCH if applicable): Bedrock, SageMaker, Comprehend, Textract, Rekognition — only if AI requirements exist
- **Networking**: VPC, PrivateLink, Transit Gateway — research based on architecture complexity

## Search Workflow Override

Use this tool priority instead of the base search workflow:

1. **awsknowledge MCP** (ALWAYS start here for AWS decisions)
   - Query with architecture decisions and service comparisons
   - Key topics: `general` for architecture, `amplify_docs` for static sites/SPAs, `cdk_docs` for IaC patterns, `cdk_constructs` for CDK construct references
2. **nova_web_grounding** (for current data points)
   - Use for latest pricing, recent feature announcements, service limit updates
   - Parameters: `topic` (specific question), `recency: "latest"` or `"recent"`, `output_style: "bullets"`
3. **exa / brave / tavily** (for community experience and comparisons)
   - Real-world production reports, "AWS X vs Y" blog posts, cost analyses

### Research Steps for Each RESEARCH Category

1. **Understand requirements**: What workload pattern, data model, scale, latency needs?
2. **Identify candidates**: List applicable AWS services for the category
3. **Query awsknowledge**: Get authoritative AWS guidance on service selection and architecture patterns
4. **Supplement with nova_web_grounding**: Get current pricing, recent announcements, and latest feature launches
5. **Find community experience**: Use exa/brave for "AWS {service_a} vs {service_b} production experience {current_year}"
6. **Evaluate pricing**: Research pricing models and estimate relative cost at stated scale
7. **Check limits**: Verify service quotas won't be a bottleneck at expected scale
8. **Build comparison matrix**: Score services on weighted criteria

## Compute Selection Context

| Workload Pattern             | Leans Toward        |
| ---------------------------- | ------------------- |
| Bursty, short-lived (<15min) | Lambda              |
| Steady-state, long-running   | ECS Fargate         |
| Simple HTTP services         | App Runner          |
| GPU workloads, custom AMIs   | EC2                 |
| Kubernetes requirement       | EKS                 |
| Batch processing             | Lambda or AWS Batch |

Lambda runtime defaults:

- Node: `nodejs24.x` (current LTS). Drop any `nodejs22.x` / `nodejs20.x` defaults.
- Python: `python3.13`.

## Database Selection Context

| Data Pattern                          | Leans Toward                                     |
| ------------------------------------- | ------------------------------------------------ |
| Relational, serverless-first Postgres | **Aurora DSQL** (GA, serverless-Postgres-wire)   |
| Relational, complex queries / joins   | Aurora PostgreSQL (Serverless v2 or provisioned) |
| Key-value, high throughput            | DynamoDB                                         |
| Session/cache data                    | ElastiCache (Valkey) or DynamoDB                 |
| Time-series data                      | Timestream                                       |
| Graph relationships                   | Neptune                                          |
| Full-text search                      | OpenSearch                                       |

## Health Check Override

AWS managed services don't have traditional OSS health checks. Instead evaluate:

- **Service maturity**: GA vs preview, how long in production
- **Region availability**: Available in required regions
- **SLA**: Published SLA percentage
- **Recent incidents**: Any major outages in last 6 months
- **Pricing stability**: Any recent pricing changes or new pricing tiers
- **Feature velocity**: Recent feature launches relevant to the use case

Use HEALTHY for GA services with strong SLAs, CAUTION for newer/preview services or those with known limitations, WARNING for services with deprecation signals.

## Output Format Override

Use the base output format for Section 1 (Category Recommendations), but replace Sections 2-4 with:

### 2. Architecture Notes

- Recommended VPC layout (if applicable)
- Security group strategy
- IAM role boundaries
- Cross-service integration patterns

### 3. Cost Considerations

Brief cost analysis at the stated scale, highlighting:

- Which services are pay-per-use vs provisioned
- Potential cost traps (data transfer, API calls, etc.)
- Cost optimization recommendations

### 4. Compatibility Notes

List any interoperability considerations between AWS services and the application stack (SDK versions, connection pooling, IAM auth for databases, etc.).

### 5. Sources

Numbered list of all sources consulted (AWS docs, re:Post, blog posts, pricing pages).

## Comparison Matrix Override

For AWS services, use these criteria weights:

| Criteria (weight)            | Service A | Service B | Service C |
| ---------------------------- | --------- | --------- | --------- |
| Fit for Workload (0.25)      | rating    | rating    | rating    |
| Operational Overhead (0.20)  | ...       | ...       | ...       |
| Cost at Scale (0.20)         | ...       | ...       | ...       |
| Ecosystem Integration (0.15) | ...       | ...       | ...       |
| Scalability Headroom (0.10)  | ...       | ...       | ...       |
| Team Familiarity (0.10)      | ...       | ...       | ...       |

## Additional Quality Checks

- [ ] Every recommendation includes pricing context
- [ ] Service limits checked against expected scale
- [ ] Region availability confirmed for target region
- [ ] Security best practices noted (IAM, encryption, VPC)
