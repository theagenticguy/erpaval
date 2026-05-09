# AWS Amplify Gen 2 + Aurora PostgreSQL

Amplify Gen 2 natively supports Aurora PostgreSQL as a BYOD (bring your own database) data source. The architecture is: AppSync (GraphQL) -> Lambda -> Aurora PostgreSQL.

> **Aurora DSQL is GA** across 15 regions (3 US, 5 APAC, 2 Canada, 4 Europe; multi-region clusters are restricted within the same continent group). DSQL is the serverless-Postgres-wire default worth evaluating before defaulting to Aurora Serverless v2 + RDS Proxy. Amplify Gen 2 doesn't yet ship a first-class DSQL template, but DSQL can be wired in as a custom data source.

## Setup

```bash
# 1. Store connection secret
npx ampx sandbox secret set SQL_CONNECTION_STRING
# Enter: postgres://user:password@hostname:port/db-name

# 2. Generate TypeScript schema from existing database
npx ampx generate schema-from-database \
  --connection-uri-secret SQL_CONNECTION_STRING \
  --out amplify/data/schema.sql.ts
```

## Configuration

`amplify/data/resource.ts`:

```typescript
import { type ClientSchema, a, defineData } from '@aws-amplify/backend'
import { schema as generatedSqlSchema } from './schema.sql'

// SQL-backed models from Aurora PostgreSQL
const sqlSchema = generatedSqlSchema
  .authorization(allow => allow.guest())
  .renameModels(() => [['notes', 'Note']])
  .setAuthorization((models) => [
    models.Note.authorization(allow => allow.ownerDefinedIn('owner'))
  ])

// DynamoDB-backed models can coexist
const dynamoSchema = a.schema({
  Todo: a.model({
    content: a.string(),
  }).authorization(allow => [allow.guest()])
})

// Combine both
const combinedSchema = a.combine([dynamoSchema, sqlSchema])
export type Schema = ClientSchema<typeof combinedSchema>
export const data = defineData({ schema: combinedSchema })
```

## Custom SQL Queries

```typescript
const sqlSchema = generatedSqlSchema
  .addToSchema({
    listWithGeo: a.query()
      .returns(a.ref('LocationWithCoord').array())
      .authorization(allow => allow.authenticated())
      .handler(a.handler.inlineSql(`
        SELECT id, name, ST_X(geom) AS lng, ST_Y(geom) AS lat FROM locations;
      `)),
  })
```

## Key Rules

- All SQL models must be generated via `npx ampx generate schema-from-database` — cannot add `a.model()` directly for SQL tables
- Tables without primary keys are silently skipped during generation
- Use RDS Proxy for connection pooling (each GraphQL query opens a new DB connection otherwise)
- DynamoDB and PostgreSQL can coexist in the same schema via `a.combine()`
- For Aurora in a VPC: configure security groups for Lambda access on port 5432
- Since Amplify Gen 2 is built on CDK, you can add custom CDK constructs in `amplify/backend.ts`
