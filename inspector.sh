#!/bin/sh
source .env
npx @modelcontextprotocol/inspector uv --directory $(pwd) run starbridge mcp serve --confluence-url=${CONFLUENCE_URL} --confluence-email-address=${CONFLUENCE_EMAIL_ADDRESS} --confluence-api-token=${CONFLUENCE_API_TOKEN}