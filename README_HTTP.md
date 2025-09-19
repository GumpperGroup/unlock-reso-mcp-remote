# UNLOCK MLS MCP Server - HTTP Remote Transport

A Model Context Protocol (MCP) server for accessing UNLOCK MLS real estate data via Bridge Interactive's RESO API, now with HTTP Remote transport for containerized deployment.

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Bridge Interactive API credentials
- Python 3.10+ (for local development)

### 1. Environment Setup
```bash
# Copy environment template
cp env.example .env

# Edit .env with your Bridge Interactive credentials
# BRIDGE_API_BASE_URL=https://api.bridgeinteractive.com
# BRIDGE_MLS_ID=your-mls-id-here
# BRIDGE_SERVER_TOKEN=your-server-token-here
```

### 2. Docker Deployment
```bash
# Build and start the server
docker-compose up -d

# Check logs
docker-compose logs -f

# Stop the server
docker-compose down
```

### 3. Local Development
```bash
# Install dependencies
pip install -e .

# Run the server
python main.py

# Or with custom host/port
python -c "from src.server_http import UnlockMlsHttpServer; import asyncio; asyncio.run(UnlockMlsHttpServer().run(host='127.0.0.1', port=8000))"
```

## 🔧 Configuration

### Environment Variables
| Variable | Description | Default |
|----------|-------------|---------|
| `BRIDGE_API_BASE_URL` | Bridge Interactive API base URL | `https://api.bridgeinteractive.com` |
| `BRIDGE_MLS_ID` | Your MLS ID | Required |
| `BRIDGE_SERVER_TOKEN` | Your server token | Required |
| `MCP_SERVER_NAME` | MCP server name | `unlock-reso-remote-mcp` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |

### Docker Configuration
- **Port**: 8000 (configurable)
- **Health Check**: `/health` endpoint
- **Logs**: Mounted to `./logs` directory
- **Restart Policy**: `unless-stopped`

## 📡 API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Root Endpoint
```bash
curl http://localhost:8000/
```

### List Tools
```bash
curl http://localhost:8000/tools
```

## 🛠️ MCP Tools

### 1. `search_properties`
Search for properties using natural language or specific criteria.

**Parameters:**
- `query` (string): Natural language search query
- `filters` (object): Specific search criteria
- `limit` (integer): Maximum results (default: 50, max: 100)
- `offset` (integer): Pagination offset (default: 0)

**Example:**
```json
{
  "query": "3 bedroom house under $500k in Austin TX",
  "filters": {
    "min_bedrooms": 3,
    "max_price": 500000,
    "city": "Austin",
    "state": "TX"
  },
  "limit": 25
}
```

### 2. `get_property_details`
Get detailed information about a specific property.

**Parameters:**
- `mls_id` (string): MLS ID of the property

**Example:**
```json
{
  "mls_id": "12345678"
}
```

### 3. `get_market_analysis`
Get market analysis and trends for a specific area.

**Parameters:**
- `city` (string): City name
- `state` (string): State abbreviation
- `zip_code` (string): ZIP code
- `property_type` (string): Property type
- `analysis_type` (string): Type of analysis

**Example:**
```json
{
  "city": "Austin",
  "state": "TX",
  "property_type": "single_family",
  "analysis_type": "comprehensive"
}
```

## 🔄 Transport Comparison

### Original (stdio)
- **Transport**: Standard input/output
- **Deployment**: Local process
- **Scaling**: Single instance
- **Use Case**: Development, CLI tools

### HTTP Remote (New)
- **Transport**: HTTP/JSON over TCP
- **Deployment**: Containerized, cloud-ready
- **Scaling**: Multiple instances, load balancing
- **Use Case**: Production, microservices

## 🐳 Docker Commands

### Build Image
```bash
docker build -t unlock-reso-remote-mcp .
```

### Run Container
```bash
docker run -p 8000:8000 --env-file .env unlock-reso-remote-mcp
```

### View Logs
```bash
docker logs unlock-reso-remote-mcp
```

### Execute Commands
```bash
docker exec -it unlock-reso-remote-mcp /bin/bash
```

## 🧪 Testing

### Health Check
```bash
curl http://localhost:8000/health
```

### Tool Listing
```bash
curl http://localhost:8000/tools
```

### MCP Protocol Test
```bash
# Test with MCP client
mcp --server http://localhost:8000 list-tools
```

## 📊 Monitoring

### Health Metrics
- Server uptime
- Request count
- Error rate
- Response time

### Logs
- Application logs: `./logs/app.log`
- Docker logs: `docker-compose logs`

## 🔒 Security

### Environment Variables
- Never commit `.env` files
- Use secrets management in production
- Rotate API tokens regularly

### Network Security
- Use HTTPS in production
- Implement authentication/authorization
- Configure firewall rules

## 🚀 Production Deployment

### Kubernetes
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: unlock-reso-remote-mcp
spec:
  replicas: 3
  selector:
    matchLabels:
      app: unlock-reso-remote-mcp
  template:
    metadata:
      labels:
        app: unlock-reso-remote-mcp
    spec:
      containers:
      - name: mcp-server
        image: unlock-reso-remote-mcp:latest
        ports:
        - containerPort: 8000
        env:
        - name: BRIDGE_API_BASE_URL
          valueFrom:
            secretKeyRef:
              name: bridge-credentials
              key: api-url
        - name: BRIDGE_MLS_ID
          valueFrom:
            secretKeyRef:
              name: bridge-credentials
              key: mls-id
        - name: BRIDGE_SERVER_TOKEN
          valueFrom:
            secretKeyRef:
              name: bridge-credentials
              key: server-token
```

### Docker Swarm
```bash
docker stack deploy -c docker-compose.yml mcp-stack
```

## 🔧 Development

### Project Structure
```
unlock-reso-mcp/
├── src/
│   ├── server.py          # Original stdio server
│   ├── server_http.py     # New HTTP server
│   ├── reso_client.py     # Bridge API client
│   ├── utils/             # Utilities
│   └── config/            # Configuration
├── tests/                 # Test files
├── main.py               # Entry point
├── Dockerfile            # Container definition
├── docker-compose.yml    # Orchestration
├── pyproject.toml       # Python configuration
└── env.example          # Environment template
```

### Adding New Tools
1. Add tool definition in `_setup_handlers()`
2. Implement handler method
3. Add tests
4. Update documentation

### Testing
```bash
# Run tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test
pytest tests/test_server_http.py
```

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation
- Review the logs for debugging
