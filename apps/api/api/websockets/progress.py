"""WebSocket handler for real-time progress updates."""

import json
import logging
from typing import Dict, Set

from fastapi import WebSocket, WebSocketDisconnect, status

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manages WebSocket connections for progress updates."""

    def __init__(self):
        # Map user_id to set of active connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, user_id: str, authenticated_user_id: str | None = None):
        """Accept and store a new connection.
        
        Args:
            websocket: The WebSocket connection
            user_id: The requested user_id from the path
            authenticated_user_id: The authenticated user's ID (None if not authenticated)
            
        Raises:
            WebSocketDisconnect: If authentication fails
        """
        # SECURITY: Reject anonymous connections or mismatched user IDs
        if authenticated_user_id is None:
            await websocket.accept()
            await websocket.send_json({
                "type": "error",
                "message": "Authentication required"
            })
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            logger.warning(f"WebSocket connection rejected: anonymous user attempted to connect for user_id={user_id}")
            return False
            
        # SECURITY: Ensure users can only connect to their own progress channel
        if authenticated_user_id != user_id:
            await websocket.accept()
            await websocket.send_json({
                "type": "error",
                "message": "Not authorized to access this user's progress"
            })
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            logger.warning(f"WebSocket connection rejected: user {authenticated_user_id} attempted to access user {user_id}'s progress")
            return False
        
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = set()
        
        self.active_connections[user_id].add(websocket)
        logger.debug(f"WebSocket connected for user {user_id}. Total connections: {len(self.active_connections[user_id])}")
        return True

    def disconnect(self, websocket: WebSocket, user_id: str):
        """Remove a disconnected WebSocket."""
        if user_id in self.active_connections:
            self.active_connections[user_id].discard(websocket)
            
            # Clean up empty sets
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
        
        logger.debug(f"WebSocket disconnected for user {user_id}")

    async def send_to_user(self, user_id: str, message: dict):
        """Send a message to all connections for a user."""
        if user_id not in self.active_connections:
            return

        disconnected = set()
        for connection in self.active_connections[user_id]:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.warning(f"Failed to send message to user {user_id}: {e}")
                disconnected.add(connection)

        # Clean up failed connections
        for conn in disconnected:
            self.active_connections[user_id].discard(conn)

    async def broadcast(self, message: dict):
        """Broadcast a message to all connected users."""
        for user_id in list(self.active_connections.keys()):
            await self.send_to_user(user_id, message)


# Global connection manager instance
manager = ConnectionManager()


class ProgressWebSocket:
    """WebSocket endpoint handler for progress updates."""

    @staticmethod
    async def handle(websocket: WebSocket, user_id: str, authenticated_user_id: str | None = None):
        """Handle WebSocket connection for a user."""
        await manager.connect(websocket, user_id, authenticated_user_id)
        
        try:
            while True:
                # Receive and process messages from client
                data = await websocket.receive_text()
                
                try:
                    message = json.loads(data)
                    await ProgressWebSocket._handle_message(websocket, user_id, message)
                except json.JSONDecodeError:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Invalid JSON"
                    })
                    
        except WebSocketDisconnect:
            manager.disconnect(websocket, user_id)

    @staticmethod
    async def _handle_message(websocket: WebSocket, user_id: str, message: dict):
        """Handle incoming WebSocket messages."""
        msg_type = message.get("type")
        
        if msg_type == "ping":
            await websocket.send_json({"type": "pong"})
            
        elif msg_type == "subscribe_progress":
            # Client wants to receive progress updates
            await websocket.send_json({
                "type": "subscribed",
                "channel": "progress"
            })
            
        elif msg_type == "progress_update":
            # Client is sending a progress update
            # Broadcast to other tabs/devices
            await manager.send_to_user(user_id, {
                "type": "progress_updated",
                "data": message.get("data")
            })
            
        elif msg_type == "draft_update":
            # Client is sending a draft update
            await manager.send_to_user(user_id, {
                "type": "draft_updated",
                "data": message.get("data")
            })
            
        else:
            await websocket.send_json({
                "type": "error",
                "message": f"Unknown message type: {msg_type}"
            })

    @staticmethod
    async def notify_progress_update(user_id: str, problem_slug: str, status: str):
        """Notify all connections for a user about a progress update."""
        await manager.send_to_user(user_id, {
            "type": "progress_updated",
            "data": {
                "problem_slug": problem_slug,
                "status": status,
                "timestamp": json.dumps({"now": True})  # Client can use Date.now()
            }
        })

    @staticmethod
    async def notify_draft_update(user_id: str, problem_slug: str, code: str):
        """Notify all connections for a user about a draft update."""
        await manager.send_to_user(user_id, {
            "type": "draft_updated",
            "data": {
                "problem_slug": problem_slug,
                "code_preview": code[:100] if code else "",  # Send preview only
                "timestamp": json.dumps({"now": True})
            }
        })


# Convenience function to get the manager
async def broadcast_progress_update(user_id: str, problem_slug: str, status: str):
    """Broadcast a progress update to all user connections."""
    await ProgressWebSocket.notify_progress_update(user_id, problem_slug, status)


async def broadcast_draft_update(user_id: str, problem_slug: str, code: str):
    """Broadcast a draft update to all user connections."""
    await ProgressWebSocket.notify_draft_update(user_id, problem_slug, code)
