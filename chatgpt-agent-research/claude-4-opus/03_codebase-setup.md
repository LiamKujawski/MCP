# O3 ChatGPT Agent Codebase Setup

## Prerequisites

### System Requirements
- Node.js 20.x or higher
- Python 3.11+ (for AI tools)
- Docker & Docker Compose
- Kubernetes (for production)
- AWS CLI configured

### Required API Keys
```bash
# .env.example
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
DEEPSEEK_API_KEY=...
GOOGLE_AI_API_KEY=...
AWS_ACCESS_KEY_ID=...
AWS_SECRET_ACCESS_KEY=...
AWS_REGION=us-east-1
```

## Initial Setup

### 1. Clone Repository and Install Dependencies

```bash
# Clone the repository
git clone https://github.com/your-org/o3-chatgpt-agent.git
cd o3-chatgpt-agent

# Install root dependencies
npm install

# Install Python dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Install CLI tools
npm install -g @astrojs/cli @cloudflare/wrangler
```

### 2. Project Structure

```
o3-chatgpt-agent/
├── apps/
│   ├── web/                 # Astro frontend
│   ├── api/                 # FastAPI backend
│   └── edge/                # CloudFlare Workers
├── packages/
│   ├── shared/              # Shared types and utilities
│   ├── ai-core/             # AI model integrations
│   └── mcp-tools/           # MCP tool implementations
├── infrastructure/
│   ├── docker/              # Dockerfiles
│   ├── k8s/                 # Kubernetes manifests
│   └── terraform/           # Infrastructure as code
├── scripts/
│   ├── setup.sh             # Initial setup script
│   └── deploy.sh            # Deployment script
└── docs/
    └── architecture.md      # Architecture documentation
```

### 3. Frontend Setup (Astro)

```bash
cd apps/web

# Install dependencies
npm install

# Configure Astro
cat > astro.config.mjs << 'EOF'
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import tailwind from '@astrojs/tailwind';
import cloudflare from '@astrojs/cloudflare';

export default defineConfig({
  output: 'hybrid',
  adapter: cloudflare(),
  integrations: [
    react({ include: ['**/components/chat/**'] }),
    tailwind(),
  ],
  vite: {
    ssr: {
      external: ['@prisma/client']
    }
  }
});
EOF

# Create main layout
mkdir -p src/layouts
cat > src/layouts/Layout.astro << 'EOF'
---
export interface Props {
  title: string;
}

const { title } = Astro.props;
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <title>{title}</title>
  </head>
  <body>
    <slot />
  </body>
</html>
EOF

# Create chat component
mkdir -p src/components/chat
cat > src/components/chat/ChatInterface.tsx << 'EOF'
import { useState, useEffect } from 'react';

export function ChatInterface() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [isStreaming, setIsStreaming] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsStreaming(true);

    const eventSource = new EventSource('/api/chat/stream', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: input })
    });

    let assistantMessage = { role: 'assistant', content: '' };

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      
      if (data.type === 'token') {
        assistantMessage.content += data.content;
        setMessages(prev => [...prev.slice(0, -1), assistantMessage]);
      } else if (data.type === 'done') {
        eventSource.close();
        setIsStreaming(false);
      }
    };

    eventSource.onerror = () => {
      eventSource.close();
      setIsStreaming(false);
    };
  };

  return (
    <div className="flex flex-col h-screen">
      <div className="flex-1 overflow-y-auto p-4">
        {messages.map((msg, idx) => (
          <div key={idx} className={`mb-4 ${msg.role === 'user' ? 'text-right' : 'text-left'}`}>
            <div className={`inline-block p-3 rounded-lg ${
              msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
      </div>
      <div className="p-4 border-t">
        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
            className="flex-1 p-2 border rounded"
            placeholder="Type your message..."
            disabled={isStreaming}
          />
          <button
            onClick={sendMessage}
            disabled={isStreaming}
            className="px-4 py-2 bg-blue-500 text-white rounded disabled:bg-gray-300"
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
EOF
```

### 4. Backend Setup (FastAPI)

```bash
cd apps/api

# Create main application
cat > main.py << 'EOF'
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import asyncio
from ai_core import ModelOrchestrator
from mcp_tools import MCPRegistry

# Initialize components
orchestrator = ModelOrchestrator()
mcp_registry = MCPRegistry()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await orchestrator.initialize()
    await mcp_registry.load_tools()
    yield
    # Shutdown
    await orchestrator.cleanup()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/chat")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    session_id = await create_session()
    
    try:
        while True:
            data = await websocket.receive_json()
            
            # Process message through orchestrator
            async for chunk in orchestrator.process_stream(
                message=data['message'],
                session_id=session_id,
                tools=mcp_registry
            ):
                await websocket.send_json(chunk)
                
    except WebSocketDisconnect:
        await cleanup_session(session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
EOF

# Create AI core module
mkdir -p ai_core
cat > ai_core/__init__.py << 'EOF'
from .orchestrator import ModelOrchestrator

__all__ = ['ModelOrchestrator']
EOF

cat > ai_core/orchestrator.py << 'EOF'
import asyncio
from typing import AsyncIterator, Dict, Any
import boto3
from anthropic import AsyncAnthropic

class ModelOrchestrator:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime')
        self.anthropic = AsyncAnthropic()
        self.model_router = ModelRouter()
        
    async def initialize(self):
        await self.model_router.load_routing_rules()
        
    async def process_stream(
        self,
        message: str,
        session_id: str,
        tools: Any
    ) -> AsyncIterator[Dict[str, Any]]:
        # Determine best model for request
        model_choice = await self.model_router.route(message)
        
        # Get context from memory
        context = await self.get_context(session_id)
        
        # Stream response
        if model_choice == 'claude-opus':
            async for chunk in self.stream_claude(message, context, tools):
                yield chunk
        elif model_choice == 'bedrock':
            async for chunk in self.stream_bedrock(message, context, tools):
                yield chunk
                
    async def stream_claude(self, message, context, tools):
        stream = await self.anthropic.messages.create(
            model="claude-3-opus-20240229",
            messages=[{"role": "user", "content": message}],
            stream=True,
            max_tokens=4096
        )
        
        async for chunk in stream:
            if chunk.type == 'content_block_delta':
                yield {
                    'type': 'token',
                    'content': chunk.delta.text
                }
EOF
```

### 5. Edge Worker Setup

```bash
cd apps/edge

# Create worker
cat > src/index.ts << 'EOF'
export interface Env {
  CACHE: KVNamespace;
  AI_GATEWAY: string;
}

export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
    const url = new URL(request.url);
    
    // Handle CORS
    if (request.method === 'OPTIONS') {
      return new Response(null, {
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Methods': 'GET, POST, OPTIONS',
          'Access-Control-Allow-Headers': 'Content-Type',
        },
      });
    }
    
    // Check cache for GET requests
    if (request.method === 'GET') {
      const cached = await env.CACHE.get(url.pathname);
      if (cached) {
        return new Response(cached, {
          headers: {
            'Content-Type': 'application/json',
            'X-Cache': 'HIT',
          },
        });
      }
    }
    
    // Forward to backend
    const backendUrl = `${env.AI_GATEWAY}${url.pathname}`;
    const response = await fetch(backendUrl, {
      method: request.method,
      headers: request.headers,
      body: request.body,
    });
    
    // Cache successful responses
    if (response.ok && request.method === 'GET') {
      const body = await response.text();
      ctx.waitUntil(
        env.CACHE.put(url.pathname, body, { expirationTtl: 300 })
      );
      return new Response(body, response);
    }
    
    return response;
  },
};
EOF

# Deploy to CloudFlare
wrangler publish
```

### 6. Docker Configuration

```bash
# Create Docker Compose for local development
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15-alpine
    environment:
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: chatgpt_agent
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"

  api:
    build:
      context: ./apps/api
      dockerfile: Dockerfile
    environment:
      DATABASE_URL: postgresql://postgres:postgres@postgres:5432/chatgpt_agent
      REDIS_URL: redis://redis:6379
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - redis
    volumes:
      - ./apps/api:/app
    command: uvicorn main:app --reload --host 0.0.0.0

  web:
    build:
      context: ./apps/web
      dockerfile: Dockerfile
    ports:
      - "3000:3000"
    environment:
      API_URL: http://api:8000
    depends_on:
      - api

volumes:
  postgres_data:
EOF
```

### 7. Kubernetes Deployment

```bash
# Create namespace
kubectl create namespace o3-agent

# Create secrets
kubectl create secret generic o3-secrets \
  --from-env-file=.env \
  -n o3-agent

# Deploy application
kubectl apply -f infrastructure/k8s/ -n o3-agent

# Check deployment status
kubectl get pods -n o3-agent
kubectl get svc -n o3-agent
```

### 8. Monitoring Setup

```bash
# Install Prometheus and Grafana
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm install prometheus prometheus-community/kube-prometheus-stack -n o3-agent

# Configure dashboards
kubectl apply -f infrastructure/monitoring/dashboards/
```

### 9. Testing

```bash
# Run unit tests
npm test

# Run integration tests
npm run test:integration

# Run end-to-end tests
npm run test:e2e

# Load testing
npm run test:load
```

### 10. Production Deployment

```bash
# Build production images
./scripts/build-prod.sh

# Deploy to production
./scripts/deploy-prod.sh

# Monitor deployment
kubectl rollout status deployment/chatgpt-agent -n production
```

## Next Steps

1. Configure SSL certificates
2. Set up CI/CD pipeline
3. Configure monitoring alerts
4. Implement backup strategy
5. Set up auto-scaling policies

For detailed configuration options, see the [architecture documentation](../docs/architecture.md).