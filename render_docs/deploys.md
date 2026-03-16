# Deploys on Render

Source: https://render.com/docs/deploys

## Auto-Deploys

Render can automatically deploy your application each time you merge a change to your codebase.

### Setting Up Auto-Deploys

As part of creating a service on Render, you link a branch of your GitHub/GitLab/Bitbucket repo (such as `main` or `production`). Whenever you push or merge a change to that branch, by default Render automatically rebuilds and redeploys your service.

### Auto-Deploy Options

- **On Commit** - Deploy immediately when code is pushed
- **After CI Checks Pass** - Wait for CI checks to complete before deploying
- **Off** - Disable auto-deploys

### Skip Phrases

Include a skip phrase in your Git commit message to prevent auto-deploy:

```bash
git commit -m "[skip render] Update README"
```

Valid skip phrases:
- `[skip render]`
- `[render skip]`
- `[skip deploy]`
- `[deploy skip]`
- `[skip cd]`
- `[cd skip]`

## Manual Deploys

### Via Dashboard

From your service's page in the Render Dashboard, open the **Manual Deploy** dropdown.

### Via CLI

```bash
render deploy
```

## Deploy Steps

With each deploy, Render proceeds through the following commands:

1. **Build command** - Compiles and installs dependencies
2. **Pre-deploy command** (optional) - Runs after build, before deploy
3. **Start command** - Starts your service

**If any command fails or times out, the entire deploy fails.**

### Command Timeouts

| Command Type | Timeout |
|--------------|---------|
| Build | 1 hour |
| Pre-deploy | 1 hour |
| Start | 60 seconds |

## Zero-Downtime Deploys

Render performs a sequence of steps to ensure your service stays available during deploys:

1. **Build** - Render attempts to build your code
2. **Spin up new instance** - If build succeeds, Render spins up a new instance
3. **Health check** - If new instance is healthy, traffic is routed to it
4. **Graceful shutdown** - Original instance receives `SIGTERM`
5. **Force terminate** - If needed, `SIGKILL` is sent
6. **Deploy complete**

**Note:** Adding a persistent disk to your service _disables_ zero-downtime deploys.

## Ephemeral Filesystem

By default, Render services have an **ephemeral filesystem**. Any changes a running service makes to its filesystem are _lost_ with each deploy.

To persist data across deploys:
- Use a Render-managed datastore (Postgres or Key Value)
- Connect to a custom datastore (MySQL, MongoDB, etc.)
- Attach a persistent disk to your service
