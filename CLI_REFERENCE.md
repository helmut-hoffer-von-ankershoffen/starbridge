# CLI Reference

Run MCP Server - alias for &#x27;mcp serve&#x27;.

Args:
    ctx (typer.Context): Typer context
    host (str): Host to run the server on
    port (int): Port to run the server on
    debug (bool): Debug mode
    env (list): Environment variables in key=value format. Can be used multiple times in one call.
        Only STARBRIDGE_ prefixed vars are used. Example --env
        &#x27;STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;&#x27;

**Usage**:

```console
$ starbridge [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--host TEXT`: Host to run the server on
* `--port INTEGER`: Port to run the server on
* `--debug / --no-debug`: Debug mode  [default: debug]
* `--env TEXT`: Environment variables in key=value format. Can be used multiple times in one call. Only STARBRIDGE_ prefixed vars are evaluated. Example --env STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;
* `--install-completion`: Install completion for the current shell.
* `--show-completion`: Show completion for the current shell, to copy it or customize the installation.
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Check health of services and their...
* `info`: Info about Starbridge and it&#x27;s environment.
* `create-dot-env`: Create .env file for Starbridge.
* `install`: Install starbridge within Claude Desktop...
* `uninstall`: Uninstall starbridge from Claude Desktop...
* `claude`: Claude Desktop application operations
* `Starbridge CLI`: Run MCP Server - alias for &#x27;mcp serve&#x27;.
* `confluence`: Confluence operations
* `hello`: Hello operations
* `mcp`: MCP operations
* `search`: Search operations
* `web`: Web operations

## `starbridge health`

Check health of services and their dependencies.

**Usage**:

```console
$ starbridge health [OPTIONS]
```

**Options**:

* `--json / --no-json`: Output health as JSON  [default: no-json]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge info`

Info about Starbridge and it&#x27;s environment.

**Usage**:

```console
$ starbridge info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge create-dot-env`

Create .env file for Starbridge. You will be prompted for settings.

Raises:
    RuntimeError: If not running in development mode.

**Usage**:

```console
$ starbridge create-dot-env [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge install`

Install starbridge within Claude Desktop application.

Adds starbridge configuration and restarts Claude Desktop app.

Args:
    restart_claude (bool): Restart Claude Desktop application post installation
    image (str): Docker image to use for Starbridge. Only applies if started as container

**Usage**:

```console
$ starbridge install [OPTIONS]
```

**Options**:

* `--restart-claude / --no-restart-claude`: Restart Claude Desktop application post installation  [default: restart-claude]
* `--image TEXT`: Docker image to use for Starbridge. Only applies if started as container.  [default: helmuthva/starbridge:latest]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge uninstall`

Uninstall starbridge from Claude Desktop application.

Removes starbridge configuration and restarts Claude Desktop app.

Args:
    restart_claude (bool): Restart Claude Desktop application post installation

**Usage**:

```console
$ starbridge uninstall [OPTIONS]
```

**Options**:

* `--restart-claude / --no-restart-claude`: Restart Claude Desktop application post installation  [default: restart-claude]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge claude`

Claude Desktop application operations

**Usage**:

```console
$ starbridge claude [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of Claude.
* `info`: Info about Claude.
* `config`: Print config of Claude Desktop application.
* `log`: Show logs.
* `restart`: Restart Claude Desktop application.

### `starbridge claude health`

Health of Claude.

**Usage**:

```console
$ starbridge claude health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge claude info`

Info about Claude.

**Usage**:

```console
$ starbridge claude info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge claude config`

Print config of Claude Desktop application.

**Usage**:

```console
$ starbridge claude config [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge claude log`

Show logs.

Args:
    tail: Tail logs
    last: Number of lines to show
    name: Name of the MCP server - use &#x27;main&#x27; for main mcp.log of Claude Desktop application

**Usage**:

```console
$ starbridge claude log [OPTIONS]
```

**Options**:

* `--tail / --no-tail`: Tail logs  [default: no-tail]
* `--last INTEGER`: Number of lines to show  [default: 100]
* `--name TEXT`: Name of the MCP server - use &#x27;main&#x27; for main mcp.log of Claude Desktop application  [default: starbridge]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge claude restart`

Restart Claude Desktop application.

**Usage**:

```console
$ starbridge claude restart [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge Starbridge CLI`

Run MCP Server - alias for &#x27;mcp serve&#x27;.

Args:
    ctx (typer.Context): Typer context
    host (str): Host to run the server on
    port (int): Port to run the server on
    debug (bool): Debug mode
    env (list): Environment variables in key=value format. Can be used multiple times in one call.
        Only STARBRIDGE_ prefixed vars are used. Example --env
        &#x27;STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;&#x27;

**Usage**:

```console
$ starbridge Starbridge CLI [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--host TEXT`: Host to run the server on
* `--port INTEGER`: Port to run the server on
* `--debug / --no-debug`: Debug mode  [default: debug]
* `--env TEXT`: Environment variables in key=value format. Can be used multiple times in one call. Only STARBRIDGE_ prefixed vars are evaluated. Example --env STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Check health of services and their...
* `info`: Info about Starbridge and it&#x27;s environment.
* `create-dot-env`: Create .env file for Starbridge.
* `install`: Install starbridge within Claude Desktop...
* `uninstall`: Uninstall starbridge from Claude Desktop...
* `claude`: Claude Desktop application operations
* `confluence`: Confluence operations
* `hello`: Hello operations
* `mcp`: MCP operations
* `search`: Search operations
* `web`: Web operations

### `starbridge Starbridge CLI health`

Check health of services and their dependencies.

**Usage**:

```console
$ starbridge Starbridge CLI health [OPTIONS]
```

**Options**:

* `--json / --no-json`: Output health as JSON  [default: no-json]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI info`

Info about Starbridge and it&#x27;s environment.

**Usage**:

```console
$ starbridge Starbridge CLI info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI create-dot-env`

Create .env file for Starbridge. You will be prompted for settings.

Raises:
    RuntimeError: If not running in development mode.

**Usage**:

```console
$ starbridge Starbridge CLI create-dot-env [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI install`

Install starbridge within Claude Desktop application.

Adds starbridge configuration and restarts Claude Desktop app.

Args:
    restart_claude (bool): Restart Claude Desktop application post installation
    image (str): Docker image to use for Starbridge. Only applies if started as container

**Usage**:

```console
$ starbridge Starbridge CLI install [OPTIONS]
```

**Options**:

* `--restart-claude / --no-restart-claude`: Restart Claude Desktop application post installation  [default: restart-claude]
* `--image TEXT`: Docker image to use for Starbridge. Only applies if started as container.  [default: helmuthva/starbridge:latest]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI uninstall`

Uninstall starbridge from Claude Desktop application.

Removes starbridge configuration and restarts Claude Desktop app.

Args:
    restart_claude (bool): Restart Claude Desktop application post installation

**Usage**:

```console
$ starbridge Starbridge CLI uninstall [OPTIONS]
```

**Options**:

* `--restart-claude / --no-restart-claude`: Restart Claude Desktop application post installation  [default: restart-claude]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI claude`

Claude Desktop application operations

**Usage**:

```console
$ starbridge Starbridge CLI claude [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of Claude.
* `info`: Info about Claude.
* `config`: Print config of Claude Desktop application.
* `log`: Show logs.
* `restart`: Restart Claude Desktop application.

#### `starbridge Starbridge CLI claude health`

Health of Claude.

**Usage**:

```console
$ starbridge Starbridge CLI claude health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI claude info`

Info about Claude.

**Usage**:

```console
$ starbridge Starbridge CLI claude info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI claude config`

Print config of Claude Desktop application.

**Usage**:

```console
$ starbridge Starbridge CLI claude config [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI claude log`

Show logs.

Args:
    tail: Tail logs
    last: Number of lines to show
    name: Name of the MCP server - use &#x27;main&#x27; for main mcp.log of Claude Desktop application

**Usage**:

```console
$ starbridge Starbridge CLI claude log [OPTIONS]
```

**Options**:

* `--tail / --no-tail`: Tail logs  [default: no-tail]
* `--last INTEGER`: Number of lines to show  [default: 100]
* `--name TEXT`: Name of the MCP server - use &#x27;main&#x27; for main mcp.log of Claude Desktop application  [default: starbridge]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI claude restart`

Restart Claude Desktop application.

**Usage**:

```console
$ starbridge Starbridge CLI claude restart [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI confluence`

Confluence operations

**Usage**:

```console
$ starbridge Starbridge CLI confluence [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of Confluence.
* `info`: Info about Confluence.
* `mcp`: MCP endpoints.
* `space`: Operations on Confluence spaces.
* `page`: Operations on Confluence pages.

#### `starbridge Starbridge CLI confluence health`

Health of Confluence.

**Usage**:

```console
$ starbridge Starbridge CLI confluence health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI confluence info`

Info about Confluence.

**Usage**:

```console
$ starbridge Starbridge CLI confluence info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI confluence mcp`

MCP endpoints.

**Usage**:

```console
$ starbridge Starbridge CLI confluence mcp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `tools`: List tools exposed via MCP.
* `resources`: List resources exposed via MCP.
* `resource-types`: List resources exposed via MCP.
* `space`: Get space resource as exposed via MCP.
* `prompts`: List prompts exposed via MCP.
* `space-summary`: Prompt to generate summary of spaces.

##### `starbridge Starbridge CLI confluence mcp tools`

List tools exposed via MCP.

**Usage**:

```console
$ starbridge Starbridge CLI confluence mcp tools [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence mcp resources`

List resources exposed via MCP.

**Usage**:

```console
$ starbridge Starbridge CLI confluence mcp resources [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence mcp resource-types`

List resources exposed via MCP.

**Usage**:

```console
$ starbridge Starbridge CLI confluence mcp resource-types [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence mcp space`

Get space resource as exposed via MCP.

**Usage**:

```console
$ starbridge Starbridge CLI confluence mcp space [OPTIONS] KEY
```

**Arguments**:

* `KEY`: Key of the space to retrieve as resource  [required]

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence mcp prompts`

List prompts exposed via MCP.

**Usage**:

```console
$ starbridge Starbridge CLI confluence mcp prompts [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence mcp space-summary`

Prompt to generate summary of spaces.

Args:
    style (str): Style of summary

**Usage**:

```console
$ starbridge Starbridge CLI confluence mcp space-summary [OPTIONS]
```

**Options**:

* `--style TEXT`: Style of summary  [default: brief]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI confluence space`

Operations on Confluence spaces.

**Usage**:

```console
$ starbridge Starbridge CLI confluence space [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `list`: Get info about all space.

##### `starbridge Starbridge CLI confluence space list`

Get info about all space.

**Usage**:

```console
$ starbridge Starbridge CLI confluence space list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI confluence page`

Operations on Confluence pages.

**Usage**:

```console
$ starbridge Starbridge CLI confluence page [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `list`: List pages in a space.
* `search`: Search pages in a space.
* `create`: Create a new page.
* `read`: Read a page.
* `update`: Update a page.
* `delete`: Delete a page.

##### `starbridge Starbridge CLI confluence page list`

List pages in a space.

Args:
    space_key (str): Key of the space to list pages from

**Usage**:

```console
$ starbridge Starbridge CLI confluence page list [OPTIONS]
```

**Options**:

* `--space-key TEXT`: Space key  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence page search`

Search pages in a space.

Args:
    query (str): Confluence query language (CQL) query to search for pages

**Usage**:

```console
$ starbridge Starbridge CLI confluence page search [OPTIONS]
```

**Options**:

* `--query TEXT`: Confluence query language (CQL) query to search for pages  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence page create`

Create a new page.

Args:
    space_key (str): Key of the space to create the page in
    title (str): Title of the page
    body (str): Body of the page
    page_id (str): Parent page

**Usage**:

```console
$ starbridge Starbridge CLI confluence page create [OPTIONS]
```

**Options**:

* `--space-key TEXT`: Space key  [required]
* `--title TEXT`: Title of the page  [required]
* `--body TEXT`: Body of the page  [required]
* `--page-id TEXT`: Parent page id
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence page read`

Read a page.

**Usage**:

```console
$ starbridge Starbridge CLI confluence page read [OPTIONS]
```

**Options**:

* `--page-id TEXT`: Page id
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence page update`

Update a page.

Args:
    page_id (str): Page id
    title (str): Title of the page
    body (str): Body of the page

**Usage**:

```console
$ starbridge Starbridge CLI confluence page update [OPTIONS]
```

**Options**:

* `--page-id TEXT`: Pager id  [required]
* `--title TEXT`: Title of the page  [required]
* `--body TEXT`: Body of the page  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

##### `starbridge Starbridge CLI confluence page delete`

Delete a page.

Args:
    page_id (str): Page id

**Usage**:

```console
$ starbridge Starbridge CLI confluence page delete [OPTIONS]
```

**Options**:

* `--page-id TEXT`: Pager id  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI hello`

Hello operations

**Usage**:

```console
$ starbridge Starbridge CLI hello [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of Hello World.
* `info`: Info about Hello World.
* `hello`: Print Hello World.
* `bridge`: Show image of starbridge.
* `pdf`: Show pdf of starbridge.

#### `starbridge Starbridge CLI hello health`

Health of Hello World.

**Usage**:

```console
$ starbridge Starbridge CLI hello health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI hello info`

Info about Hello World.

**Usage**:

```console
$ starbridge Starbridge CLI hello info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI hello hello`

Print Hello World.

Args:
    locale (str): Locale to use

**Usage**:

```console
$ starbridge Starbridge CLI hello hello [OPTIONS]
```

**Options**:

* `--locale TEXT`: Locale to use  [default: en_US]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI hello bridge`

Show image of starbridge.

Args:
    dump (bool): If set, will dump to file starbridge.png in current working directory.
        Defaults to opening viewer to show the image.

**Usage**:

```console
$ starbridge Starbridge CLI hello bridge [OPTIONS]
```

**Options**:

* `--dump / --no-dump`: If set, will dump to file starbridge.png in current working directory. Defaults to opening viewer to show the image.  [default: no-dump]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI hello pdf`

Show pdf of starbridge.

Args:
    dump (bool): If set, will dump to file starbridge.pdf in current working directory.
        Defaults to opening viewer to show the document.

**Usage**:

```console
$ starbridge Starbridge CLI hello pdf [OPTIONS]
```

**Options**:

* `--dump / --no-dump`: If set, will dump to file starbridge.pdf in current working directory. Defaults to opening viewer to show the document.  [default: no-dump]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI mcp`

MCP operations

**Usage**:

```console
$ starbridge Starbridge CLI mcp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Check health of the services and their...
* `services`: Services exposed by modules.
* `tools`: Tools exposed by modules.
* `tool`: Get tool by name with optional arguments.
* `resources`: Resources exposed by modules.
* `resource`: Get resource by URI.
* `prompts`: Prompts exposed by modules.
* `prompt`: Get a prompt by name with optional arguments.
* `resource-types`: Resource types exposed by modules.
* `serve`: Run MCP server.
* `inspect`: Run inspector.

#### `starbridge Starbridge CLI mcp health`

Check health of the services and their dependencies.

**Usage**:

```console
$ starbridge Starbridge CLI mcp health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp services`

Services exposed by modules.

**Usage**:

```console
$ starbridge Starbridge CLI mcp services [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp tools`

Tools exposed by modules.

**Usage**:

```console
$ starbridge Starbridge CLI mcp tools [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp tool`

Get tool by name with optional arguments.

Args:
    name (str): Name of the tool
    arguments (list): Arguments in key=value format

**Usage**:

```console
$ starbridge Starbridge CLI mcp tool [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--arguments TEXT`: Arguments in key=value format
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp resources`

Resources exposed by modules.

**Usage**:

```console
$ starbridge Starbridge CLI mcp resources [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp resource`

Get resource by URI.

Args:
    uri (str): URI of the resources

**Usage**:

```console
$ starbridge Starbridge CLI mcp resource [OPTIONS] URI
```

**Arguments**:

* `URI`: [required]

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp prompts`

Prompts exposed by modules.

**Usage**:

```console
$ starbridge Starbridge CLI mcp prompts [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp prompt`

Get a prompt by name with optional arguments.

Args:
    name (str): Name of the prompt
    arguments (list): Arguments in key=value format

**Usage**:

```console
$ starbridge Starbridge CLI mcp prompt [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--arguments TEXT`: Arguments in key=value format
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp resource-types`

Resource types exposed by modules.

**Usage**:

```console
$ starbridge Starbridge CLI mcp resource-types [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp serve`

Run MCP server.

Args:
    host (str): Host to run the server on
    port (int): Port to run the server on
    debug (bool): Debug mode
    env (list): Environment variables in key=value format. Can be used multiple times in one call.
        Only `STARBRIDGE_` prefixed vars are used. Example --env
        `STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;`

**Usage**:

```console
$ starbridge Starbridge CLI mcp serve [OPTIONS]
```

**Options**:

* `--host TEXT`: Host to run the server on
* `--port INTEGER`: Port to run the server on
* `--debug / --no-debug`: Debug mode  [default: debug]
* `--env TEXT`: Environment variables in key=value format. Can be used multiple times in one call. Only STARBRIDGE_ prefixed vars are used. Example --env STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI mcp inspect`

Run inspector.

**Usage**:

```console
$ starbridge Starbridge CLI mcp inspect [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI search`

Search operations

**Usage**:

```console
$ starbridge Starbridge CLI search [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of the search module.
* `info`: Info about the search module.
* `web`: Search the web.

#### `starbridge Starbridge CLI search health`

Health of the search module.

**Usage**:

```console
$ starbridge Starbridge CLI search health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI search info`

Info about the search module.

**Usage**:

```console
$ starbridge Starbridge CLI search info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI search web`

Search the web.

Args:
    q (str): Query

**Usage**:

```console
$ starbridge Starbridge CLI search web [OPTIONS] Q
```

**Arguments**:

* `Q`: Query  [required]

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge Starbridge CLI web`

Web operations

**Usage**:

```console
$ starbridge Starbridge CLI web [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of the web module.
* `info`: Info about the web module.
* `get`: Fetch content from the world wide web via...

#### `starbridge Starbridge CLI web health`

Health of the web module.

**Usage**:

```console
$ starbridge Starbridge CLI web health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI web info`

Info about the web module.

**Usage**:

```console
$ starbridge Starbridge CLI web info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge Starbridge CLI web get`

Fetch content from the world wide web via HTTP GET.

Converts to content type as a best effort, extracts links, and provides additional context.

Args:
    url (str): URL to fetch
    accept_language (str): Accept-Language header value to send in the request
    transform_to_markdown (bool): if possible transform content to markdown
    extract_links (bool): include extracted links in the response
    additional_context (bool): include additional context in the response
    llms_full_txt (bool): provide llms-full.txt in contexts
    force_not_respecting_robots_txt (bool): do not respect robots.txt
        If False, the agent will respect robots.txt if the environment variable
            STARBRIDGE_WEB_RESPPECT_ROBOTS_TXT is set to 1.
        Defaults to False

**Usage**:

```console
$ starbridge Starbridge CLI web get [OPTIONS] URL
```

**Arguments**:

* `URL`: URL to fetch  [required]

**Options**:

* `--accept-language TEXT`: Accept-Language header value to send in the request  [default: en-US,en;q=0.9,de;q=0.8]
* `--transform-to-markdown / --no-transform-to-markdown`: if possible transform content to markdown  [default: transform-to-markdown]
* `--extract-links / --no-extract-links`: include extracted links in the response  [default: extract-links]
* `--additional-context / --no-additional-context`: include additional context in the response  [default: additional-context]
* `--llms-full-txt / --no-llms-full-txt`: provide llms-full.txt in contexts  [default: no-llms-full-txt]
* `--force-not-respecting-robots-txt`: Force not respecting robots.txt. If True, the agent will ignore robots.txt.If False, the agent will respect robots.txt if the environment variableSTARBRIDGE_WEB_RESPPECT_ROBOTS_TXT is set to 1.Defaults to False.
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge confluence`

Confluence operations

**Usage**:

```console
$ starbridge confluence [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of Confluence.
* `info`: Info about Confluence.
* `mcp`: MCP endpoints.
* `space`: Operations on Confluence spaces.
* `page`: Operations on Confluence pages.

### `starbridge confluence health`

Health of Confluence.

**Usage**:

```console
$ starbridge confluence health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge confluence info`

Info about Confluence.

**Usage**:

```console
$ starbridge confluence info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge confluence mcp`

MCP endpoints.

**Usage**:

```console
$ starbridge confluence mcp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `tools`: List tools exposed via MCP.
* `resources`: List resources exposed via MCP.
* `resource-types`: List resources exposed via MCP.
* `space`: Get space resource as exposed via MCP.
* `prompts`: List prompts exposed via MCP.
* `space-summary`: Prompt to generate summary of spaces.

#### `starbridge confluence mcp tools`

List tools exposed via MCP.

**Usage**:

```console
$ starbridge confluence mcp tools [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence mcp resources`

List resources exposed via MCP.

**Usage**:

```console
$ starbridge confluence mcp resources [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence mcp resource-types`

List resources exposed via MCP.

**Usage**:

```console
$ starbridge confluence mcp resource-types [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence mcp space`

Get space resource as exposed via MCP.

**Usage**:

```console
$ starbridge confluence mcp space [OPTIONS] KEY
```

**Arguments**:

* `KEY`: Key of the space to retrieve as resource  [required]

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence mcp prompts`

List prompts exposed via MCP.

**Usage**:

```console
$ starbridge confluence mcp prompts [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence mcp space-summary`

Prompt to generate summary of spaces.

Args:
    style (str): Style of summary

**Usage**:

```console
$ starbridge confluence mcp space-summary [OPTIONS]
```

**Options**:

* `--style TEXT`: Style of summary  [default: brief]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge confluence space`

Operations on Confluence spaces.

**Usage**:

```console
$ starbridge confluence space [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `list`: Get info about all space.

#### `starbridge confluence space list`

Get info about all space.

**Usage**:

```console
$ starbridge confluence space list [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge confluence page`

Operations on Confluence pages.

**Usage**:

```console
$ starbridge confluence page [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `list`: List pages in a space.
* `search`: Search pages in a space.
* `create`: Create a new page.
* `read`: Read a page.
* `update`: Update a page.
* `delete`: Delete a page.

#### `starbridge confluence page list`

List pages in a space.

Args:
    space_key (str): Key of the space to list pages from

**Usage**:

```console
$ starbridge confluence page list [OPTIONS]
```

**Options**:

* `--space-key TEXT`: Space key  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence page search`

Search pages in a space.

Args:
    query (str): Confluence query language (CQL) query to search for pages

**Usage**:

```console
$ starbridge confluence page search [OPTIONS]
```

**Options**:

* `--query TEXT`: Confluence query language (CQL) query to search for pages  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence page create`

Create a new page.

Args:
    space_key (str): Key of the space to create the page in
    title (str): Title of the page
    body (str): Body of the page
    page_id (str): Parent page

**Usage**:

```console
$ starbridge confluence page create [OPTIONS]
```

**Options**:

* `--space-key TEXT`: Space key  [required]
* `--title TEXT`: Title of the page  [required]
* `--body TEXT`: Body of the page  [required]
* `--page-id TEXT`: Parent page id
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence page read`

Read a page.

**Usage**:

```console
$ starbridge confluence page read [OPTIONS]
```

**Options**:

* `--page-id TEXT`: Page id
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence page update`

Update a page.

Args:
    page_id (str): Page id
    title (str): Title of the page
    body (str): Body of the page

**Usage**:

```console
$ starbridge confluence page update [OPTIONS]
```

**Options**:

* `--page-id TEXT`: Pager id  [required]
* `--title TEXT`: Title of the page  [required]
* `--body TEXT`: Body of the page  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

#### `starbridge confluence page delete`

Delete a page.

Args:
    page_id (str): Page id

**Usage**:

```console
$ starbridge confluence page delete [OPTIONS]
```

**Options**:

* `--page-id TEXT`: Pager id  [required]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge hello`

Hello operations

**Usage**:

```console
$ starbridge hello [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of Hello World.
* `info`: Info about Hello World.
* `hello`: Print Hello World.
* `bridge`: Show image of starbridge.
* `pdf`: Show pdf of starbridge.

### `starbridge hello health`

Health of Hello World.

**Usage**:

```console
$ starbridge hello health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge hello info`

Info about Hello World.

**Usage**:

```console
$ starbridge hello info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge hello hello`

Print Hello World.

Args:
    locale (str): Locale to use

**Usage**:

```console
$ starbridge hello hello [OPTIONS]
```

**Options**:

* `--locale TEXT`: Locale to use  [default: en_US]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge hello bridge`

Show image of starbridge.

Args:
    dump (bool): If set, will dump to file starbridge.png in current working directory.
        Defaults to opening viewer to show the image.

**Usage**:

```console
$ starbridge hello bridge [OPTIONS]
```

**Options**:

* `--dump / --no-dump`: If set, will dump to file starbridge.png in current working directory. Defaults to opening viewer to show the image.  [default: no-dump]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge hello pdf`

Show pdf of starbridge.

Args:
    dump (bool): If set, will dump to file starbridge.pdf in current working directory.
        Defaults to opening viewer to show the document.

**Usage**:

```console
$ starbridge hello pdf [OPTIONS]
```

**Options**:

* `--dump / --no-dump`: If set, will dump to file starbridge.pdf in current working directory. Defaults to opening viewer to show the document.  [default: no-dump]
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge mcp`

MCP operations

**Usage**:

```console
$ starbridge mcp [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Check health of the services and their...
* `services`: Services exposed by modules.
* `tools`: Tools exposed by modules.
* `tool`: Get tool by name with optional arguments.
* `resources`: Resources exposed by modules.
* `resource`: Get resource by URI.
* `prompts`: Prompts exposed by modules.
* `prompt`: Get a prompt by name with optional arguments.
* `resource-types`: Resource types exposed by modules.
* `serve`: Run MCP server.
* `inspect`: Run inspector.

### `starbridge mcp health`

Check health of the services and their dependencies.

**Usage**:

```console
$ starbridge mcp health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp services`

Services exposed by modules.

**Usage**:

```console
$ starbridge mcp services [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp tools`

Tools exposed by modules.

**Usage**:

```console
$ starbridge mcp tools [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp tool`

Get tool by name with optional arguments.

Args:
    name (str): Name of the tool
    arguments (list): Arguments in key=value format

**Usage**:

```console
$ starbridge mcp tool [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--arguments TEXT`: Arguments in key=value format
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp resources`

Resources exposed by modules.

**Usage**:

```console
$ starbridge mcp resources [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp resource`

Get resource by URI.

Args:
    uri (str): URI of the resources

**Usage**:

```console
$ starbridge mcp resource [OPTIONS] URI
```

**Arguments**:

* `URI`: [required]

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp prompts`

Prompts exposed by modules.

**Usage**:

```console
$ starbridge mcp prompts [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp prompt`

Get a prompt by name with optional arguments.

Args:
    name (str): Name of the prompt
    arguments (list): Arguments in key=value format

**Usage**:

```console
$ starbridge mcp prompt [OPTIONS] NAME
```

**Arguments**:

* `NAME`: [required]

**Options**:

* `--arguments TEXT`: Arguments in key=value format
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp resource-types`

Resource types exposed by modules.

**Usage**:

```console
$ starbridge mcp resource-types [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp serve`

Run MCP server.

Args:
    host (str): Host to run the server on
    port (int): Port to run the server on
    debug (bool): Debug mode
    env (list): Environment variables in key=value format. Can be used multiple times in one call.
        Only `STARBRIDGE_` prefixed vars are used. Example --env
        `STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;`

**Usage**:

```console
$ starbridge mcp serve [OPTIONS]
```

**Options**:

* `--host TEXT`: Host to run the server on
* `--port INTEGER`: Port to run the server on
* `--debug / --no-debug`: Debug mode  [default: debug]
* `--env TEXT`: Environment variables in key=value format. Can be used multiple times in one call. Only STARBRIDGE_ prefixed vars are used. Example --env STARBRIDGE_ATLASSIAN_URL=&quot;https://your-domain.atlassian.net&quot; --env STARBRIDGE_ATLASSIAN_EMAIL=&quot;YOUR_EMAIL&quot;
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge mcp inspect`

Run inspector.

**Usage**:

```console
$ starbridge mcp inspect [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge search`

Search operations

**Usage**:

```console
$ starbridge search [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of the search module.
* `info`: Info about the search module.
* `web`: Search the web.

### `starbridge search health`

Health of the search module.

**Usage**:

```console
$ starbridge search health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge search info`

Info about the search module.

**Usage**:

```console
$ starbridge search info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge search web`

Search the web.

Args:
    q (str): Query

**Usage**:

```console
$ starbridge search web [OPTIONS] Q
```

**Arguments**:

* `Q`: Query  [required]

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

## `starbridge web`

Web operations

**Usage**:

```console
$ starbridge web [OPTIONS] COMMAND [ARGS]...
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

**Commands**:

* `health`: Health of the web module.
* `info`: Info about the web module.
* `get`: Fetch content from the world wide web via...

### `starbridge web health`

Health of the web module.

**Usage**:

```console
$ starbridge web health [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge web info`

Info about the web module.

**Usage**:

```console
$ starbridge web info [OPTIONS]
```

**Options**:

* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻

### `starbridge web get`

Fetch content from the world wide web via HTTP GET.

Converts to content type as a best effort, extracts links, and provides additional context.

Args:
    url (str): URL to fetch
    accept_language (str): Accept-Language header value to send in the request
    transform_to_markdown (bool): if possible transform content to markdown
    extract_links (bool): include extracted links in the response
    additional_context (bool): include additional context in the response
    llms_full_txt (bool): provide llms-full.txt in contexts
    force_not_respecting_robots_txt (bool): do not respect robots.txt
        If False, the agent will respect robots.txt if the environment variable
            STARBRIDGE_WEB_RESPPECT_ROBOTS_TXT is set to 1.
        Defaults to False

**Usage**:

```console
$ starbridge web get [OPTIONS] URL
```

**Arguments**:

* `URL`: URL to fetch  [required]

**Options**:

* `--accept-language TEXT`: Accept-Language header value to send in the request  [default: en-US,en;q=0.9,de;q=0.8]
* `--transform-to-markdown / --no-transform-to-markdown`: if possible transform content to markdown  [default: transform-to-markdown]
* `--extract-links / --no-extract-links`: include extracted links in the response  [default: extract-links]
* `--additional-context / --no-additional-context`: include additional context in the response  [default: additional-context]
* `--llms-full-txt / --no-llms-full-txt`: provide llms-full.txt in contexts  [default: no-llms-full-txt]
* `--force-not-respecting-robots-txt`: Force not respecting robots.txt. If True, the agent will ignore robots.txt.If False, the agent will respect robots.txt if the environment variableSTARBRIDGE_WEB_RESPPECT_ROBOTS_TXT is set to 1.Defaults to False.
* `--help`: Show this message and exit.

⭐ Starbridge v0.10.10 - built with love in Berlin 🐻
