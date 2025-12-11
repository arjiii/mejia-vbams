from fastapi import WebSocket, WebSocketDisconnect
from typing import Dict, List
import json
import asyncio

class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
        self.user_rooms: Dict[str, List[str]] = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
        print(f"Client {client_id} connected")

    def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
        
        # Remove from all rooms
        for room, clients in self.user_rooms.items():
            if client_id in clients:
                clients.remove(client_id)
        
        print(f"Client {client_id} disconnected")

    async def send_personal_message(self, message: str, client_id: str):
        if client_id in self.active_connections:
            websocket = self.active_connections[client_id]
            try:
                await websocket.send_text(message)
            except Exception as e:
                print(f"Error sending message to {client_id}: {e}")
                self.disconnect(client_id)

    async def send_to_room(self, message: str, room: str):
        if room in self.user_rooms:
            for client_id in self.user_rooms[room]:
                await self.send_personal_message(message, client_id)

    async def join_room(self, client_id: str, room: str):
        if room not in self.user_rooms:
            self.user_rooms[room] = []
        
        if client_id not in self.user_rooms[room]:
            self.user_rooms[room].append(client_id)
        
        print(f"Client {client_id} joined room {room}")

    async def leave_room(self, client_id: str, room: str):
        if room in self.user_rooms and client_id in self.user_rooms[room]:
            self.user_rooms[room].remove(client_id)
        
        print(f"Client {client_id} left room {room}")

    async def handle_message(self, client_id: str, message: str):
        try:
            data = json.loads(message)
            message_type = data.get("type")
            
            if message_type == "join_room":
                room = data.get("room")
                if room:
                    await self.join_room(client_id, room)
            
            elif message_type == "leave_room":
                room = data.get("room")
                if room:
                    await self.leave_room(client_id, room)
            
            elif message_type == "location_update":
                room = data.get("room")
                if room:
                    await self.send_to_room(message, room)
            
            elif message_type == "assistance_status":
                room = data.get("room")
                if room:
                    await self.send_to_room(message, room)
            
            elif message_type == "chat_message":
                room = data.get("room")
                if room:
                    await self.send_to_room(message, room)
            
            else:
                # Echo back unknown message types
                await self.send_personal_message(message, client_id)
                
        except json.JSONDecodeError:
            await self.send_personal_message("Invalid JSON format", client_id)
        except Exception as e:
            print(f"Error handling message from {client_id}: {e}")
            await self.send_personal_message("Error processing message", client_id)

# Global WebSocket manager instance
websocket_manager = ConnectionManager()
