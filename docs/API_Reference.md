# API Reference

## VutriumSDK Class

The main SDK class providing access to all Vutrium features.

### Constructor

```python
VutriumSDK(host="localhost", port=8080, auto_reconnect=True)
```

**Parameters:**
- `host` (str): The hostname to connect to. Default: "localhost"
- `port` (int): The port number to connect to. Default: 8080
- `auto_reconnect` (bool): Enable automatic reconnection. Default: True

### Core Methods

#### `connect() -> bool`

Establish connection to Vutrium service.

**Returns:**
- `bool`: True if connection successful, False otherwise

**Raises:**
- `ConnectionError`: If unable to establish connection

**Example:**
```python
sdk = VutriumSDK()
if sdk.connect():
    print("Connected successfully!")
else:
    print("Connection failed")
```

#### `disconnect() -> None`

Close connection and cleanup resources.

**Example:**
```python
sdk.disconnect()
```

#### `is_connected() -> bool`

Check if currently connected to the service.

**Returns:**
- `bool`: True if connected, False otherwise

#### `get_game_data() -> dict`

Retrieve current game state information.

**Returns:**
- `dict`: Game state data including player positions, ball location, score, etc.

**Example:**
```python
data = sdk.get_game_data()
print(f"Ball position: {data['ball_position']}")
print(f"Score: {data['score']}")
```

### Event System

#### `on_game_state_change(callback: callable) -> None`

Register callback for game state change events.

**Parameters:**
- `callback` (callable): Function to call when game state changes

**Callback Signature:**
```python
def callback(event_data: dict) -> None:
    pass
```

**Example:**
```python
def on_state_change(data):
    print(f"Game state changed: {data}")

sdk.on_game_state_change(on_state_change)
```

## GameBoost Class

Performance optimization and game enhancement features.

**Access:** `sdk.game_boost`

### Methods

#### `enable() -> bool`

Enable game performance boost.

**Returns:**
- `bool`: True if boost enabled successfully

#### `disable() -> bool`

Disable boost features.

**Returns:**
- `bool`: True if boost disabled successfully

#### `set_boost_level(level: int) -> bool`

Set boost intensity level.

**Parameters:**
- `level` (int): Boost level from 1-10

**Returns:**
- `bool`: True if level set successfully

#### `is_enabled() -> bool`

Check if boost is currently active.

**Returns:**
- `bool`: True if boost is enabled

### Properties

#### `is_full_boost -> bool`

Indicates if boost is at maximum level.

**Example:**
```python
sdk.game_boost.enable()
sdk.game_boost.set_boost_level(10)
if sdk.game_boost.is_full_boost:
    print("Maximum boost active!")
```

## BotManager Class

Rocket League bot integration and management.

**Access:** `sdk.bot_manager`

### Methods

#### `register_bot(bot_config: dict) -> str`

Register a new bot with the system.

**Parameters:**
- `bot_config` (dict): Bot configuration data

**Returns:**
- `str`: Unique bot ID

**Example:**
```python
bot_config = {
    "name": "MyBot",
    "team": 0,
    "type": "rlbot",
    "config_path": "/path/to/bot/config"
}
bot_id = sdk.bot_manager.register_bot(bot_config)
```

#### `unregister_bot(bot_id: str) -> bool`

Remove bot registration.

**Parameters:**
- `bot_id` (str): The bot ID to unregister

**Returns:**
- `bool`: True if successfully unregistered

#### `get_bot_list() -> list`

Retrieve list of all registered bots.

**Returns:**
- `list`: List of bot information dictionaries

#### `start_bot(bot_id: str) -> bool`

Start bot execution.

**Parameters:**
- `bot_id` (str): The bot ID to start

**Returns:**
- `bool`: True if bot started successfully

#### `stop_bot(bot_id: str) -> bool`

Stop bot execution.

**Parameters:**
- `bot_id` (str): The bot ID to stop

**Returns:**
- `bool`: True if bot stopped successfully

## Process Management

### Methods

#### `get_process_list() -> list`

Get list of all running processes.

**Returns:**
- `list`: List of process information

#### `kill_process(process_name: str) -> bool`

Terminate a specific process.

**Parameters:**
- `process_name` (str): Name of process to terminate

**Returns:**
- `bool`: True if process terminated successfully

## Constants

### Connection States
```python
CONNECTED = "connected"
DISCONNECTED = "disconnected"
CONNECTING = "connecting"
RECONNECTING = "reconnecting"
```

### Boost Levels
```python
BOOST_LEVEL_MIN = 1
BOOST_LEVEL_MAX = 10
BOOST_LEVEL_DEFAULT = 5
```

### Event Types
```python
EVENT_GAME_STATE_CHANGE = "game_state_change"
EVENT_BOT_ACTION = "bot_action"
EVENT_BOOST_CHANGE = "boost_change"
EVENT_CONNECTION_CHANGE = "connection_change"
```

## Error Handling

### Exception Types

#### `VutriumConnectionError`
Raised when connection-related errors occur.

#### `VutriumBoostError`
Raised when boost-related operations fail.

#### `VutriumBotError`
Raised when bot management operations fail.

### Example Error Handling

```python
from VutriumSDK import VutriumSDK, VutriumConnectionError, VutriumBoostError

try:
    sdk = VutriumSDK()
    sdk.connect()
    sdk.game_boost.enable()
except VutriumConnectionError as e:
    print(f"Connection error: {e}")
except VutriumBoostError as e:
    print(f"Boost error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    sdk.disconnect()
```

## Complete Usage Example

```python
from VutriumSDK import VutriumSDK
import time

def main():
    # Initialize SDK
    sdk = VutriumSDK(host="localhost", port=8080)
    
    try:
        # Connect to service
        if not sdk.connect():
            print("Failed to connect")
            return
        
        print("Connected to Vutrium service")
        
        # Setup event handlers
        def on_game_change(data):
            print(f"Game state: {data}")
        
        sdk.on_game_state_change(on_game_change)
        
        # Enable game boost
        sdk.game_boost.enable()
        sdk.game_boost.set_boost_level(8)
        
        # Register a bot
        bot_config = {
            "name": "TestBot",
            "team": 0,
            "type": "rlbot"
        }
        bot_id = sdk.bot_manager.register_bot(bot_config)
        print(f"Bot registered: {bot_id}")
        
        # Start the bot
        sdk.bot_manager.start_bot(bot_id)
        
        # Monitor for 30 seconds
        for i in range(30):
            game_data = sdk.get_game_data()
            print(f"Tick {i}: {game_data}")
            time.sleep(1)
        
        # Cleanup
        sdk.bot_manager.stop_bot(bot_id)
        sdk.bot_manager.unregister_bot(bot_id)
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        sdk.disconnect()
        print("Disconnected")

if __name__ == "__main__":
    main()
```