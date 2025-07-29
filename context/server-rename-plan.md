# Server Rename Plan: UNLOCK MLS MCP → UNLOCK MLS RESO Reference MCP

## Summary
Change all references to the server name from "UNLOCK MLS MCP" to "UNLOCK MLS RESO Reference MCP" throughout the codebase, documentation, and configuration files. This includes updating various naming patterns like "unlock-mls-mcp" to "unlock-mls-reso-reference-mcp".

## Key Questions Before Implementation:
1. **Package name**: Should we also change the package name from `unlock-reso-mcp` to `unlock-mls-reso-reference-mcp` in pyproject.toml? This would be a breaking change for installations.
2. **User Agent string**: Should we update the User-Agent from `UNLOCK-MLS-MCP-Server/1.0` to `UNLOCK-MLS-RESO-Reference-Server/1.0`?
3. **Directory paths**: Should deployment paths change from `/opt/unlock-mls-mcp` to `/opt/unlock-mls-reso-reference-mcp`?

## Files to Update (in order of priority):

### 1. Core Configuration Files
- **src/config/settings.py**: Change default `mcp_server_name` from `"unlock-mls-mcp"` to `"unlock-mls-reso-reference-mcp"`
- **src/server.py**: Update Server constructor from `Server("unlock-mls-mcp")` to `Server("unlock-mls-reso-reference-mcp")`
- **.env.example**: Update `MCP_SERVER_NAME=unlock-mls-mcp` to `MCP_SERVER_NAME=unlock-mls-reso-reference-mcp`

### 2. Package Metadata (if desired)
- **pyproject.toml**: 
  - Update `name = "unlock-reso-mcp"` to `name = "unlock-mls-reso-reference-mcp"`
  - Update `description` to include "RESO Reference"
  - Update script name from `unlock-reso-mcp` to `unlock-mls-reso-reference-mcp`

### 3. Code Comments and Strings
- **main.py**: Update file docstring
- **src/server.py**: Update class docstring and log messages
- **src/reso_client.py**: Update User-Agent string (if desired)

### 4. Documentation Files (25+ files)
- **README.md**: Update title and all references
- **CLAUDE.md**: Update project description and Claude Desktop config examples
- **docs/README.md**: Update title and descriptions
- **docs/api-reference.md**: Update references throughout
- **docs/configuration.md**: Update examples and default values
- **docs/deployment-configuration.md**: Update service names, paths, and container names
- **docs/mcp-*.md**: Update titles and references in all MCP documentation files
- **docs/error-handling-troubleshooting.md**: Update service commands and paths
- **docs/authentication.md**: Update User-Agent examples
- **context/*.md**: Update all context files

### 5. Test Files
- **tests/test_*.py**: Update any hardcoded server name references
- **context/test-execution-summary.md**: Update title

## Implementation Strategy:

### Phase 1: Core Functionality (Critical)
1. Update core configuration files (settings.py, server.py, .env.example)
2. Test server startup to ensure no breaking changes

### Phase 2: Package Identity (Optional)
1. Update pyproject.toml if package renaming is desired
2. Update User-Agent string if desired

### Phase 3: Documentation (Important)
1. Update all README and documentation files
2. Update deployment guides and examples
3. Update Claude Desktop integration examples

### Phase 4: Context Files (Cleanup)
1. Update context and troubleshooting files
2. Update test documentation

## Backward Compatibility Notes:
- Existing Claude Desktop configurations using "unlock-mls-mcp" will need to be updated
- If package name changes, existing installations will need to be updated
- Environment variables can remain backward compatible through the settings system

## Recommended Approach:
1. Keep the package name as `unlock-reso-mcp` to avoid breaking installations
2. Update the MCP server name to `unlock-mls-reso-reference-mcp`
3. Update User-Agent to `UNLOCK-MLS-RESO-Reference-Server/1.0`
4. Keep deployment paths flexible through environment variables
5. Update all documentation consistently

## Affected Files List:

### Core Files (3):
- src/config/settings.py
- src/server.py
- .env.example

### Documentation Files (25+):
- README.md
- CLAUDE.md
- docs/README.md
- docs/api-reference.md
- docs/configuration.md
- docs/deployment-configuration.md
- docs/mcp-server-architecture.md
- docs/mcp-resources.md
- docs/mcp-tools-api.md
- docs/error-handling-troubleshooting.md
- docs/authentication.md
- docs/reso-api-client.md
- docs/data-mapping-validation.md
- context/test-execution-summary.md
- context/technical-error-analysis.md
- context/comprehensive-test-errors.md
- context/claude-code-development-prompt.md
- context/troubleshooting-guide.md
- context/error-resolution-plan.md

### Optional Files:
- pyproject.toml (if package rename desired)
- src/reso_client.py (User-Agent string)
- main.py (docstring)

### Test Files:
- tests/test_tools.py
- tests/test_load.py
- tests/test_performance.py
- tests/test_error_scenarios.py

## Name Mapping Reference:
- "UNLOCK MLS MCP" → "UNLOCK MLS RESO Reference MCP"
- "unlock-mls-mcp" → "unlock-mls-reso-reference-mcp"
- "UNLOCK-MLS-MCP-Server" → "UNLOCK-MLS-RESO-Reference-Server"
- "UnlockMlsServer" → (keep class name unchanged for code compatibility)

## Implementation Notes:
- Search and replace operations should be done carefully to avoid false positives
- Test all changes in development environment before deployment
- Update Claude Desktop configurations after deployment
- Consider creating migration guide for existing users