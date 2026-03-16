# Configuring Environment Variables on Render

Source: https://render.com/docs/configure-environment-variables

## Overview

You can (and should!) use **environment variables** to configure your Render services:

Environment variables enable you to customize a service's runtime behavior for different environments (such as development, staging, and production). They also protect you from committing secret credentials (such as API keys or database connection strings) to your application source.

## Setting Environment Variables

1. In the Render Dashboard, select the service you want to add an environment variable to.

2. Click **Environment** in the left pane.

3. Under **Environment Variables**, click **+ Add Environment Variable**.
   - You can also click **Add from .env** to add environment variables in bulk.

4. Provide a **Key** and **Value** for each new environment variable.

5. Save your changes. You can select one of three options from the dropdown:
   - **Save, rebuild, and deploy:** Render triggers a new build for your service and deploys it with the new environment variables.
   - **Save and deploy:** Render redeploys your service's _existing_ build with the new environment variables.
   - **Save only:** Render saves the new environment variables _without_ triggering a deploy. Your service will not use the new variables until its next deploy.

## Bulk Adding from .env File

If you have a local `.env` file, you can bulk-add its environment variables to your service by clicking **Add from .env** on your service's **Environment** page.

Your file must use valid `.env` syntax. Examples:

```
KEY_1=value_of_KEY_1
KEY_2="value of KEY_2"
KEY_3="-----BEGIN-----valueofKEY_3-----END-----"
```

**Don't commit your `.env` file to source control!** This file often contains secret credentials. To avoid accidentally committing it, add `.env` to your project's `.gitignore` file.

## Reading Environment Variables in Code

Each programming language provides its own mechanism for reading the value of an environment variable.

**Environment variable values are always strings.**

### Node.js
```javascript
const databaseUrl = process.env.DATABASE_URL
```

### Python
```python
import os
database_url = os.environ.get('DATABASE_URL')
```

### Ruby
```ruby
database_url = ENV['DATABASE_URL']
```

### Go
```go
package main
import "os"
func main() {
    databaseURL := os.Getenv("DATABASE_URL")
}
```

### Elixir
```elixir
database_url = System.get_env("DATABASE_URL")
```
