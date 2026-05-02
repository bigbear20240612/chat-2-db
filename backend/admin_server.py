import uvicorn
import logging
import sys
import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
# type: ignore  MC8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZURKQk9BPT06ZTIwNGUzMjQ=

# 添加当前目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.api.api_v1.api import api_router
from app.core.config import settings

# 注释掉过度的日志过滤，保持正常日志显示
# 这样我们可以看到完整的连接信息来诊断问题

app = FastAPI(
    title="ChatDB API",
    description="Text2SQL API for intelligent database querying",
    version="0.1.0",
)

# Set up CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API router
app.include_router(api_router, prefix="/api")

# pylint: disable  MS8yOmFIVnBZMlhucUx2b2pZbmt1cm82ZURKQk9BPT06ZTIwNGUzMjQ=

# 强制重新加载 - 修复路由问题

if __name__ == "__main__":
    uvicorn.run("admin_server:app", host="0.0.0.0", port=8000, reload=True, timeout_keep_alive=120)  # 120秒的keep-alive超时
