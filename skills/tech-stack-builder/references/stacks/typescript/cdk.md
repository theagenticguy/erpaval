# AWS CDK Stack

Infrastructure as Code using AWS CDK with TypeScript.

> **CDK v2 is the stable track** (`aws-cdk-lib` v2.251.x). There is no public CDK v3 roadmap. For Node-based Lambdas, default to `lambda.Runtime.NODEJS_24_X`. For Python Lambdas, default to `PYTHON_3_13`.

## Project Setup

```bash
# New CDK project
mkdir my-infra && cd my-infra
npx cdk init app --language typescript

# Or with projen (recommended for long-lived projects)
npx projen new awscdk-app-ts
```

## Key Patterns

### L2 Constructs Over L1

Always prefer L2 constructs (e.g., `lambda.Function`) over L1 CloudFormation resources (`CfnFunction`). L2 constructs provide sensible defaults, grant helpers, and type-safe props.

```typescript
import { Stack, Duration } from 'aws-cdk-lib'
import * as lambda from 'aws-cdk-lib/aws-lambda'
import * as apigateway from 'aws-cdk-lib/aws-apigateway'

const fn = new lambda.Function(this, 'Handler', {
  runtime: lambda.Runtime.PYTHON_3_13,
  handler: 'index.handler',
  code: lambda.Code.fromAsset('lambda'),
  timeout: Duration.seconds(30),
  memorySize: 256,
})

const api = new apigateway.RestApi(this, 'Api')
api.root.addMethod('GET', new apigateway.LambdaIntegration(fn))
```

### Grant Pattern

Use `.grant*()` methods instead of manually creating IAM policies:

```typescript
bucket.grantRead(fn)          // S3 read access
table.grantReadWriteData(fn)  // DynamoDB access
queue.grantSendMessages(fn)   // SQS send access
```

### Stack Organization

```text
lib/
  constructs/       # Reusable L3 constructs
  stacks/           # Stack definitions
    api-stack.ts
    database-stack.ts
    monitoring-stack.ts
bin/
  app.ts            # App entry point, stack instantiation
```

### Testing

```typescript
import { Template } from 'aws-cdk-lib/assertions'

test('creates Lambda function', () => {
  const template = Template.fromStack(stack)
  template.hasResourceProperties('AWS::Lambda::Function', {
    Runtime: 'python3.13',
    Timeout: 30,
  })
  template.resourceCountIs('AWS::Lambda::Function', 1)
})
```

## projen (Project Generator)

Manages project config files (tsconfig, package.json, .gitignore, etc.) from code. Prevents config drift.

```typescript
// .projenrc.ts
import { awscdk } from 'projen'

const project = new awscdk.AwsCdkTypeScriptApp({
  cdkVersion: '2.251.0',                    // current stable floor
  defaultReleaseBranch: 'main',
  name: 'my-infra',
  deps: ['@aws-cdk/aws-lambda-python-alpha'],
})

project.synth()
```

Run `npx projen` to regenerate all config files.
