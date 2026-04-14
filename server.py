import logging
import socketio
import uvicorn

# --- Logging ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
logger = logging.getLogger(__name__)

# --- Socket.IO async server (ASGI mode) ---
sio = socketio.AsyncServer(
    async_mode="asgi",
    cors_allowed_origins="*",  # tighten this in production
    logger=False,
    engineio_logger=False,
)

# --- Serve static HTML files ---
app = socketio.ASGIApp(
    sio,
    static_files={
        "/": {"content_type": "text/html", "filename": "frontend.html"},
        "/backoffice": {"content_type": "text/html", "filename": "backoffice.html"},
    },
)

# ---------------------------------------------------------------------------
# Socket.IO events
# ---------------------------------------------------------------------------

@sio.event
async def connect(sid, environ, auth):
    """
    Clients identify their role via query string:
      - Frontend:   ws://localhost:8000/socket.io/?role=frontend
      - Backoffice: ws://localhost:8000/socket.io/?role=backoffice
    """
    query = environ.get("QUERY_STRING", "")
    role = "frontend"
    for part in query.split("&"):
        if part.startswith("role="):
            role = part.split("=", 1)[1]
            break

    if role == "backoffice":
        await sio.enter_room(sid, "backoffice")
        logger.info("Backoffice connected — sid=%s joined room:backoffice", sid)
    else:
        logger.info("Frontend connected  — sid=%s", sid)


@sio.event
async def place_order(sid, data):
    """
    Payload expected from frontend:
      { "item": "Burger", "quantity": 2 }
    """
    item = data.get("item", "Unknown")
    quantity = data.get("quantity", 1)

    logger.info("Order received from sid=%s — item=%s qty=%s", sid, item, quantity)

    # Broadcast only to backoffice room
    await sio.emit(
        "new_order",
        {"item": item, "quantity": quantity},
        room="backoffice",
    )


@sio.event
async def disconnect(sid):
    logger.info("Client disconnected — sid=%s", sid)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info",
    )
