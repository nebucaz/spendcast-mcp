# spendcast-mcp Phase 1 Project Plan
## Overview
Phase 1.0 creates a functional MVP. The focus is to .

## Story Status Legend

    ⏳ Pending - Not started
    🔄 In Progress - Currently being worked on
    ✅ Completed - Implemented and verified
    🧪 Testing - Implementation complete, awaiting verification

## Story 1.1: Implement the mcp server framework and connet to the graphdb instance
Status: ✅ Completed

### Acceptance Criteria:
 - MCP Server with one tool `execute_sparql`

### Technical Implementation:
 - Create `server.py` instantiate fasrmcp
 - Connect to the graphdb-Server API defined in .env 'GRAPHDB_URL'
 - Add the `execute_sparql` - tool

### Testing:
 - Unittest: Create an MCP client and query the graphdb instance `select ?s ?p ?o where {?s ? p ?} limit 10` and ensure it returns a error-free response of 10 entities when using authentication

## Story 1.2: Graphdb API Authentication
Status: ⏳ Pending

### Acceptance Criteria
- The MCP-Server can connect to the graphdb instance using the credentials defined in the .env file

### Technical Implementation
- Extend the `execute_sparql` tool to pick up the required credentials and perform Basic authentication for the httpx-request to the graphdb instance

### Testing
- Extend the Unittest with a mock, that requires basic authentication