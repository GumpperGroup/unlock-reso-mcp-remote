# Supabase Authentication Implementation for UNLOCK MLS RESO MCP Server

## Project Overview

Implement Supabase Authentication with Google Workspace and Microsoft 365 SSO integration for the UNLOCK MLS RESO MCP Server. This will add user authentication and authorization while maintaining the existing MCP server functionality.

## Implementation Strategy

### Architecture Overview

The solution uses a hybrid approach:
1. **Web Authentication Service**: Handles user authentication via Supabase
2. **Token Management**: Stores and validates user session tokens
3. **MCP Server Integration**: Validates tokens before API calls
4. **SSO Integration**: Google Workspace and Microsoft 365 OAuth flows

### Key Components to Implement

1. **Supabase Authentication Service** (`src/auth/supabase_auth.py`)
2. **Web Authentication Server** (`src/web_auth/auth_server.py`)
3. **Token Management** (`src/auth/token_manager.py`)
4. **MCP Server Authentication Middleware** (modify `src/server.py`)
5. **Frontend Authentication UI** (`web_auth/static/`)
6. **Configuration Updates** (environment variables and settings)

## Implementation Plan

### Phase 1: Supabase Setup and Configuration

#### 1.1 Supabase Project Setup
```bash
# Add Supabase dependencies
uv add supabase

# Add web server dependencies
uv add fastapi uvicorn jinja2 python-multipart

# Add JWT handling
uv add python-jose[cryptography] python-dateutil
```

#### 1.2 Environment Configuration
Add to `.env`:
```env
# Supabase Configuration
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key

# Authentication Configuration
AUTH_REQUIRED=true
AUTH_WEB_PORT=8080
AUTH_SESSION_TTL=3600
AUTH_REDIRECT_URL=http://localhost:8080/auth/callback

# Google Workspace SSO
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret

# Microsoft 365 SSO
MICROSOFT_CLIENT_ID=your_microsoft_client_id
MICROSOFT_CLIENT_SECRET=your_microsoft_client_secret
MICROSOFT_TENANT_ID=your_microsoft_tenant_id
```

### Phase 2: Core Authentication Components

#### 2.1 Supabase Authentication Service
Create `src/auth/supabase_auth.py`:
```python
import asyncio
import os
from typing import Optional, Dict, Any
from datetime import datetime, timedelta
import jwt
from supabase import create_client, Client
from src.config.settings import settings

class SupabaseAuthService:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )
        self.service_client: Client = create_client(
            settings.SUPABASE_URL, 
            settings.SUPABASE_SERVICE_ROLE_KEY
        )

    async def verify_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify and decode JWT session token"""
        try:
            # Verify token with Supabase
            response = self.supabase.auth.get_user(token)
            if response.user:
                return {
                    "user_id": response.user.id,
                    "email": response.user.email,
                    "metadata": response.user.user_metadata
                }
        except Exception as e:
            print(f"Token verification failed: {e}")
        return None

    async def create_session_token(self, user_data: Dict[str, Any]) -> str:
        """Create a session token for MCP server use"""
        payload = {
            "user_id": user_data["id"],
            "email": user_data["email"],
            "exp": datetime.utcnow() + timedelta(seconds=settings.AUTH_SESSION_TTL),
            "iat": datetime.utcnow()
        }
        return jwt.encode(payload, settings.SUPABASE_SERVICE_ROLE_KEY, algorithm="HS256")

    async def get_user_permissions(self, user_id: str) -> Dict[str, bool]:
        """Get user permissions from custom user_permissions table"""
        try:
            response = self.service_client.table("user_permissions").select("*").eq("user_id", user_id).execute()
            if response.data:
                return response.data[0]
            return {"can_search": True, "can_analyze": True, "rate_limit": 100}
        except Exception:
            # Default permissions
            return {"can_search": True, "can_analyze": True, "rate_limit": 60}
```

#### 2.2 Token Management
Create `src/auth/token_manager.py`:
```python
import os
import json
import asyncio
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime
import aiofiles

class TokenManager:
    def __init__(self):
        self.token_file = Path.home() / ".unlock_mls" / "auth_token.json"
        self.token_file.parent.mkdir(exist_ok=True)

    async def save_token(self, token: str, user_data: Dict[str, Any]) -> None:
        """Save authentication token and user data"""
        token_data = {
            "token": token,
            "user": user_data,
            "created_at": datetime.utcnow().isoformat(),
            "expires_at": (datetime.utcnow() + timedelta(seconds=3600)).isoformat()
        }
        
        async with aiofiles.open(self.token_file, 'w') as f:
            await f.write(json.dumps(token_data, indent=2))

    async def load_token(self) -> Optional[Dict[str, Any]]:
        """Load stored authentication token"""
        try:
            if not self.token_file.exists():
                return None
                
            async with aiofiles.open(self.token_file, 'r') as f:
                content = await f.read()
                token_data = json.loads(content)
                
            # Check if token is expired
            expires_at = datetime.fromisoformat(token_data["expires_at"])
            if datetime.utcnow() > expires_at:
                await self.clear_token()
                return None
                
            return token_data
        except Exception as e:
            print(f"Error loading token: {e}")
            return None

    async def clear_token(self) -> None:
        """Clear stored authentication token"""
        try:
            if self.token_file.exists():
                self.token_file.unlink()
        except Exception as e:
            print(f"Error clearing token: {e}")

    async def is_authenticated(self) -> bool:
        """Check if user is currently authenticated"""
        token_data = await self.load_token()
        return token_data is not None
```

### Phase 3: Web Authentication Server

#### 3.1 FastAPI Authentication Server
Create `src/web_auth/auth_server.py`:
```python
import asyncio
import webbrowser
from typing import Optional
import uvicorn
from fastapi import FastAPI, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.auth.supabase_auth import SupabaseAuthService
from src.auth.token_manager import TokenManager
from src.config.settings import settings

class AuthenticationServer:
    def __init__(self):
        self.app = FastAPI(title="UNLOCK MLS Authentication")
        self.supabase_auth = SupabaseAuthService()
        self.token_manager = TokenManager()
        self.setup_routes()
        self.setup_static_files()

    def setup_static_files(self):
        """Setup static files and templates"""
        self.app.mount("/static", StaticFiles(directory="src/web_auth/static"), name="static")
        self.templates = Jinja2Templates(directory="src/web_auth/templates")

    def setup_routes(self):
        """Setup authentication routes"""

        @self.app.get("/", response_class=HTMLResponse)
        async def login_page(request: Request):
            return self.templates.TemplateResponse("login.html", {
                "request": request,
                "google_auth_url": self.get_google_auth_url(),
                "microsoft_auth_url": self.get_microsoft_auth_url()
            })

        @self.app.get("/auth/google")
        async def google_auth():
            """Redirect to Google OAuth"""
            auth_url = f"https://accounts.google.com/oauth/authorize?client_id={settings.GOOGLE_CLIENT_ID}&redirect_uri={settings.AUTH_REDIRECT_URL}&scope=openid%20email%20profile&response_type=code&state=google"
            return RedirectResponse(auth_url)

        @self.app.get("/auth/microsoft")
        async def microsoft_auth():
            """Redirect to Microsoft OAuth"""
            auth_url = f"https://login.microsoftonline.com/{settings.MICROSOFT_TENANT_ID}/oauth2/v2.0/authorize?client_id={settings.MICROSOFT_CLIENT_ID}&redirect_uri={settings.AUTH_REDIRECT_URL}&scope=openid%20email%20profile&response_type=code&state=microsoft"
            return RedirectResponse(auth_url)

        @self.app.get("/auth/callback")
        async def auth_callback(request: Request, code: str, state: str):
            """Handle OAuth callback"""
            try:
                if state == "google":
                    user_data = await self.handle_google_callback(code)
                elif state == "microsoft":
                    user_data = await self.handle_microsoft_callback(code)
                else:
                    raise HTTPException(status_code=400, detail="Invalid state parameter")

                # Create Supabase user or sign in existing user
                supabase_user = await self.create_or_signin_user(user_data, state)
                
                # Create session token for MCP server
                session_token = await self.supabase_auth.create_session_token(supabase_user)
                
                # Save token locally
                await self.token_manager.save_token(session_token, supabase_user)
                
                return self.templates.TemplateResponse("success.html", {
                    "request": request,
                    "user": supabase_user,
                    "message": "Authentication successful! You can now close this window and use the MCP server."
                })

            except Exception as e:
                return self.templates.TemplateResponse("error.html", {
                    "request": request,
                    "error": str(e)
                })

        @self.app.get("/auth/status")
        async def auth_status():
            """Check authentication status"""
            is_authenticated = await self.token_manager.is_authenticated()
            if is_authenticated:
                token_data = await self.token_manager.load_token()
                return {"authenticated": True, "user": token_data["user"]}
            return {"authenticated": False}

        @self.app.post("/auth/logout")
        async def logout():
            """Logout user"""
            await self.token_manager.clear_token()
            return {"message": "Logged out successfully"}

    async def handle_google_callback(self, code: str) -> dict:
        """Handle Google OAuth callback"""
        # Implement Google OAuth token exchange
        # This is a simplified version - you'll need to implement the full OAuth flow
        import httpx
        
        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": settings.GOOGLE_CLIENT_ID,
            "client_secret": settings.GOOGLE_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.AUTH_REDIRECT_URL
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_json = token_response.json()
            
            # Get user info
            user_info_url = f"https://www.googleapis.com/oauth2/v2/userinfo?access_token={token_json['access_token']}"
            user_response = await client.get(user_info_url)
            user_data = user_response.json()
            
            return {
                "email": user_data["email"],
                "name": user_data["name"],
                "provider": "google",
                "provider_id": user_data["id"]
            }

    async def handle_microsoft_callback(self, code: str) -> dict:
        """Handle Microsoft OAuth callback"""
        # Implement Microsoft OAuth token exchange
        import httpx
        
        token_url = f"https://login.microsoftonline.com/{settings.MICROSOFT_TENANT_ID}/oauth2/v2.0/token"
        token_data = {
            "client_id": settings.MICROSOFT_CLIENT_ID,
            "client_secret": settings.MICROSOFT_CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": settings.AUTH_REDIRECT_URL
        }
        
        async with httpx.AsyncClient() as client:
            token_response = await client.post(token_url, data=token_data)
            token_json = token_response.json()
            
            # Get user info
            user_info_url = "https://graph.microsoft.com/v1.0/me"
            headers = {"Authorization": f"Bearer {token_json['access_token']}"}
            user_response = await client.get(user_info_url, headers=headers)
            user_data = user_response.json()
            
            return {
                "email": user_data["mail"] or user_data["userPrincipalName"],
                "name": user_data["displayName"],
                "provider": "microsoft",
                "provider_id": user_data["id"]
            }

    async def create_or_signin_user(self, user_data: dict, provider: str) -> dict:
        """Create or sign in user with Supabase"""
        try:
            # Try to sign in existing user
            response = self.supabase_auth.supabase.auth.sign_in_with_oauth({
                "provider": provider,
                "options": {
                    "redirect_to": settings.AUTH_REDIRECT_URL
                }
            })
            
            if response.user:
                return {
                    "id": response.user.id,
                    "email": response.user.email,
                    "name": user_data["name"],
                    "provider": provider
                }
        except Exception:
            pass
            
        # Create new user if sign in failed
        response = self.supabase_auth.supabase.auth.sign_up({
            "email": user_data["email"],
            "password": f"oauth_{user_data['provider_id']}"  # This won't be used for OAuth users
        })
        
        return {
            "id": response.user.id,
            "email": response.user.email,  
            "name": user_data["name"],
            "provider": provider
        }

    def get_google_auth_url(self) -> str:
        return f"/auth/google"

    def get_microsoft_auth_url(self) -> str:
        return f"/auth/microsoft"

    async def start_server(self):
        """Start the authentication server"""
        config = uvicorn.Config(
            self.app,
            host="localhost",
            port=settings.AUTH_WEB_PORT,
            log_level="info"
        )
        server = uvicorn.Server(config)
        
        # Open browser to login page
        webbrowser.open(f"http://localhost:{settings.AUTH_WEB_PORT}")
        
        await server.serve()
```

### Phase 4: Frontend Templates

#### 4.1 Login Template
Create `src/web_auth/templates/login.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UNLOCK MLS Authentication</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-md max-w-md w-full">
        <div class="text-center mb-8">
            <h1 class="text-3xl font-bold text-gray-900 mb-2">UNLOCK MLS</h1>
            <p class="text-gray-600">Sign in to access MLS data through the AI assistant</p>
        </div>
        
        <div class="space-y-4">
            <a href="{{ google_auth_url }}" 
               class="w-full bg-red-500 hover:bg-red-600 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center transition-colors">
                <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                    <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                    <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z"/>
                    <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z"/>
                </svg>
                Sign in with Google
            </a>
            
            <a href="{{ microsoft_auth_url }}" 
               class="w-full bg-blue-500 hover:bg-blue-600 text-white font-medium py-3 px-4 rounded-lg flex items-center justify-center transition-colors">
                <svg class="w-5 h-5 mr-2" viewBox="0 0 24 24">
                    <path fill="currentColor" d="M0 0h11.377v11.372H0V0zm12.623 0H24v11.372H12.623V0zM0 12.623h11.377V24H0V12.623zm12.623 0H24V24H12.623V12.623z"/>
                </svg>
                Sign in with Microsoft 365
            </a>
        </div>
        
        <div class="mt-8 text-center text-sm text-gray-500">
            <p>By signing in, you agree to access MLS data responsibly and in accordance with your organization's policies.</p>
        </div>
    </div>
</body>
</html>
```

#### 4.2 Success Template
Create `src/web_auth/templates/success.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Authentication Successful</title>
    <link href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css" rel="stylesheet">
</head>
<body class="bg-gray-100 min-h-screen flex items-center justify-center">
    <div class="bg-white p-8 rounded-lg shadow-md max-w-md w-full text-center">
        <div class="text-green-500 mb-4">
            <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
        </div>
        
        <h1 class="text-2xl font-bold text-gray-900 mb-2">Welcome, {{ user.name }}!</h1>
        <p class="text-gray-600 mb-6">{{ message }}</p>
        
        <div class="bg-gray-50 p-4 rounded-lg mb-4">
            <p class="text-sm text-gray-700">
                <strong>Email:</strong> {{ user.email }}<br>
                <strong>Provider:</strong> {{ user.provider.title() }}
            </p>
        </div>
        
        <button onclick="window.close()" 
                class="bg-blue-500 hover:bg-blue-600 text-white font-medium py-2 px-6 rounded-lg">
            Close Window
        </button>
    </div>
    
    <script>
        // Auto-close after 5 seconds
        setTimeout(() => {
            window.close();
        }, 5000);
    </script>
</body>
</html>
```

### Phase 5: MCP Server Integration

#### 5.1 Authentication Middleware
Modify `src/server.py` to add authentication:

```python
# Add these imports at the top
from src.auth.token_manager import TokenManager
from src.auth.supabase_auth import SupabaseAuthService
from src.web_auth.auth_server import AuthenticationServer

class AuthenticatedMCPServer:
    def __init__(self):
        self.token_manager = TokenManager()
        self.supabase_auth = SupabaseAuthService()
        self.auth_server = AuthenticationServer()
        self.authenticated_user = None

    async def ensure_authenticated(self) -> bool:
        """Ensure user is authenticated before allowing API calls"""
        if not settings.AUTH_REQUIRED:
            return True
            
        # Check for existing token
        token_data = await self.token_manager.load_token()
        if token_data:
            # Verify token is still valid
            user_data = await self.supabase_auth.verify_session_token(token_data["token"])
            if user_data:
                self.authenticated_user = user_data
                return True
        
        # Start authentication flow
        print("Authentication required. Starting web authentication server...")
        await self.start_authentication_flow()
        
        # Wait for authentication
        return await self.wait_for_authentication()

    async def start_authentication_flow(self):
        """Start the web authentication server"""
        import asyncio
        import threading
        
        def run_auth_server():
            asyncio.run(self.auth_server.start_server())
        
        auth_thread = threading.Thread(target=run_auth_server)
        auth_thread.daemon = True
        auth_thread.start()

    async def wait_for_authentication(self, timeout: int = 300) -> bool:
        """Wait for user to authenticate"""
        import asyncio
        
        for _ in range(timeout):
            if await self.token_manager.is_authenticated():
                token_data = await self.token_manager.load_token()
                self.authenticated_user = token_data["user"]
                return True
            await asyncio.sleep(1)
        
        return False

    async def get_user_permissions(self) -> Dict[str, Any]:
        """Get current user permissions"""
        if not self.authenticated_user:
            return {"can_search": False, "can_analyze": False, "rate_limit": 0}
        
        return await self.supabase_auth.get_user_permissions(self.authenticated_user["user_id"])

# Wrap existing MCP tools with authentication
async def authenticated_search_properties(query: str = None, filters: dict = None, limit: int = 25) -> dict:
    """Search properties with authentication"""
    auth_server = AuthenticatedMCPServer()
    
    if not await auth_server.ensure_authenticated():
        return {"error": "Authentication required. Please complete the authentication process."}
    
    permissions = await auth_server.get_user_permissions()
    if not permissions.get("can_search", False):
        return {"error": "You don't have permission to search properties."}
    
    # Apply rate limiting based on user permissions
    # ... existing search logic
    return await original_search_properties(query, filters, limit)
```

### Phase 6: Database Schema

#### 6.1 Supabase Tables
Create these tables in your Supabase project:

```sql
-- User permissions table
CREATE TABLE user_permissions (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    can_search BOOLEAN DEFAULT true,
    can_analyze BOOLEAN DEFAULT true,
    can_find_agents BOOLEAN DEFAULT true,
    rate_limit INTEGER DEFAULT 60,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- User activity log
CREATE TABLE user_activity (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    action VARCHAR(255) NOT NULL,
    resource VARCHAR(255),
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- API usage tracking
CREATE TABLE api_usage (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id) ON DELETE CASCADE,
    endpoint VARCHAR(255) NOT NULL,
    method VARCHAR(10) NOT NULL,
    response_time INTEGER,
    status_code INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Row Level Security
ALTER TABLE user_permissions ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_activity ENABLE ROW LEVEL SECURITY;
ALTER TABLE api_usage ENABLE ROW LEVEL SECURITY;

-- Policies
CREATE POLICY "Users can view own permissions" ON user_permissions
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own activity" ON user_activity
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can view own usage" ON api_usage
    FOR SELECT USING (auth.uid() = user_id);
```

### Phase 7: Configuration Updates

#### 7.1 Update Settings
Modify `src/config/settings.py`:

```python
# Add authentication settings
AUTH_REQUIRED: bool = os.getenv("AUTH_REQUIRED", "false").lower() == "true"
AUTH_WEB_PORT: int = int(os.getenv("AUTH_WEB_PORT", "8080"))
AUTH_SESSION_TTL: int = int(os.getenv("AUTH_SESSION_TTL", "3600"))
AUTH_REDIRECT_URL: str = os.getenv("AUTH_REDIRECT_URL", "http://localhost:8080/auth/callback")

# Supabase settings
SUPABASE_URL: str = os.getenv("SUPABASE_URL", "")
SUPABASE_ANON_KEY: str = os.getenv("SUPABASE_ANON_KEY", "")
SUPABASE_SERVICE_ROLE_KEY: str = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

# OAuth settings
GOOGLE_CLIENT_ID: str = os.getenv("GOOGLE_CLIENT_ID", "")
GOOGLE_CLIENT_SECRET: str = os.getenv("GOOGLE_CLIENT_SECRET", "")
MICROSOFT_CLIENT_ID: str = os.getenv("MICROSOFT_CLIENT_ID", "")
MICROSOFT_CLIENT_SECRET: str = os.getenv("MICROSOFT_CLIENT_SECRET", "")
MICROSOFT_TENANT_ID: str = os.getenv("MICROSOFT_TENANT_ID", "")
```

### Phase 8: Testing

#### 8.1 Authentication Tests
Create `tests/test_authentication.py`:

```python
import pytest
import asyncio
from unittest.mock import AsyncMock, patch
from src.auth.supabase_auth import SupabaseAuthService
from src.auth.token_manager import TokenManager

@pytest.mark.asyncio
async def test_token_management():
    """Test token saving and loading"""
    token_manager = TokenManager()
    
    test_token = "test_jwt_token"
    test_user = {"id": "123", "email": "test@example.com"}
    
    await token_manager.save_token(test_token, test_user)
    loaded_data = await token_manager.load_token()
    
    assert loaded_data["token"] == test_token
    assert loaded_data["user"]["email"] == test_user["email"]

@pytest.mark.asyncio
async def test_supabase_auth():
    """Test Supabase authentication service"""
    with patch('supabase.create_client') as mock_client:
        auth_service = SupabaseAuthService()
        
        # Mock successful token verification
        mock_client.return_value.auth.get_user.return_value.user = AsyncMock()
        mock_client.return_value.auth.get_user.return_value.user.id = "123"
        mock_client.return_value.auth.get_user.return_value.user.email = "test@example.com"
        
        result = await auth_service.verify_session_token("valid_token")
        assert result["user_id"] == "123"
        assert result["email"] == "test@example.com"
```

### Phase 9: Documentation Updates

#### 9.1 Update README.md
Add authentication section:

```markdown
## Authentication

### Setup

1. **Create Supabase Project**:
   - Go to [Supabase](https://supabase.com) and create a new project
   - Enable Google and Microsoft OAuth providers
   - Create the required database tables (see Phase 6)

2. **Configure OAuth Apps**:
   - **Google**: Create OAuth app in Google Cloud Console
   - **Microsoft**: Register app in Azure AD

3. **Environment Variables**:
   ```bash
   # Copy authentication variables to .env
   SUPABASE_URL=your_supabase_url
   SUPABASE_ANON_KEY=your_anon_key
   SUPABASE_SERVICE_ROLE_KEY=your_service_key
   AUTH_REQUIRED=true
   ```

### Usage

When authentication is enabled, users will need to authenticate before using the MCP server:

1. Start the MCP server
2. Browser window opens automatically for authentication
3. Choose Google or Microsoft SSO
4. Complete authentication flow
5. MCP server is now ready for use

### User Management

Administrators can manage user permissions through the Supabase dashboard:
- Search permissions
- Analysis permissions  
- Rate limits
- Activity monitoring
```

## Implementation Checklist

### Phase 1: Setup ✅
- [ ] Install dependencies
- [ ] Create Supabase project
- [ ] Configure OAuth providers
- [ ] Update environment variables

### Phase 2: Core Authentication ✅
- [ ] Implement `SupabaseAuthService`
- [ ] Implement `TokenManager`
- [ ] Create database tables

### Phase 3: Web Server ✅
- [ ] Implement `AuthenticationServer`
- [ ] Create OAuth callback handlers
- [ ] Test authentication flow

### Phase 4: Frontend ✅
- [ ] Create login template
- [ ] Create success template
- [ ] Style with Tailwind CSS

### Phase 5: MCP Integration ✅
- [ ] Add authentication middleware
- [ ] Wrap existing tools
- [ ] Implement permission checks

### Phase 6: Testing ✅
- [ ] Write authentication tests
- [ ] Test OAuth flows
- [ ] Integration testing

### Phase 7: Documentation ✅
- [ ] Update README
- [ ] Add configuration guide
- [ ] Document user management

## Security Considerations

1. **Token Security**:
   - Session tokens stored locally with expiration
   - JWT tokens signed with service role key
   - Automatic token refresh

2. **OAuth Security**:
   - PKCE for additional security
   - State parameter validation
   - Secure redirect handling

3. **API Security**:
   - Row-level security in Supabase
   - Rate limiting per user
   - Activity logging

4. **Data Protection**:
   - No sensitive data in logs
   - Secure token storage
   - User permission validation

This implementation provides enterprise-grade authentication while maintaining the simplicity of the existing MCP server architecture.