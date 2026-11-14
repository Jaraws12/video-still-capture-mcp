# Video Still Capture MCP

An MCP (Model Context Protocol) server that enables AI assistants to access and control webcams through OpenCV. It supports still-image capture, camera connection management, camera property controls, and image processing.

## Features

- **Quick Image Capture:** Capture a single image without maintaining a persistent connection.
- **Camera Connection Management:** Open, manage, and close webcam connections.
- **Multiple Camera Support:** Connect to different camera devices using device indices.
- **Camera Properties:** Read and modify resolution, FPS, brightness, contrast, and saturation.
- **Image Processing:** Capture grayscale, resized, rotated, and cropped images.
- **Horizontal Flipping:** Flip captured images.
- **Resource Management:** Explicitly release camera connections and clean up resources.
- **MCP Integration:** Expose webcam operations as tools that MCP-compatible AI assistants can discover and invoke.

## Architecture

```text
          AI Assistant
                |
                | MCP Protocol
                |
        Python MCP Server
        (FastMCP / STDIO)
                |
        Camera Manager
                |
             OpenCV
                |
             Webcam
                |
         Captured Image
```

The MCP server exposes Python functions as tools. The CameraManager handles webcam operations, while OpenCV handles image capture and processing. Captured images are JPEG-encoded and returned as MCP image content.

## Technology Stack

- Python 3.10+
- Model Context Protocol (MCP)
- FastMCP
- OpenCV
- NumPy
- Pytest

## Project Structure

```text
video-still-capture-mcp/
│
├── camera_manager.py
├── videocapture_mcp.py
├── manual_camera_test.py
│
├── tests/
│   └── test_camera_manager.py
│
├── requirements.txt
├── pyproject.toml
├── README.md
├── LICENSE
└── .gitignore
```

## Installation

### Prerequisites

- Python 3.10 or higher
- A webcam or compatible video capture device
- Windows, macOS, or Linux

### 1. Clone the repository

```bash
git clone YOUR_REPOSITORY_URL
cd video-still-capture-mcp
```

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the MCP Server

Start the MCP server using:

```bash
mcp dev videocapture_mcp.py
```

This launches the MCP Inspector, allowing you to connect to the server and test its tools.

The server also supports direct STDIO execution:

```bash
python videocapture_mcp.py
```

For MCP host integration, configure the host to launch the Python server using the absolute path to your Python interpreter and `videocapture_mcp.py`.

## Available MCP Tools

The server exposes 11 tools.

| Tool | Description |
|---|---|
| `quick_capture` | Capture one image and release the camera |
| `open_camera` | Open a persistent webcam connection |
| `capture_frame` | Capture an image from an existing connection |
| `get_video_properties` | Retrieve camera properties |
| `set_video_property` | Modify camera properties |
| `close_connection` | Close a camera connection |
| `list_active_connections` | List active camera connections |
| `capture_grayscale` | Capture an image in grayscale |
| `capture_resized` | Capture and resize an image |
| `capture_rotated` | Capture and rotate an image |
| `capture_cropped` | Capture and crop a selected region |

### Example Tool Usage

**Quick capture**

```python
quick_capture(
    device_index=0,
    flip=False
)
```

**Open camera**

```python
open_camera(
    device_index=0,
    name="My Webcam"
)
```

**Capture a frame**

```python
capture_frame(
    connection_id="YOUR_CONNECTION_ID",
    flip=True
)
```

**Get camera properties**

```python
get_video_properties(
    connection_id="YOUR_CONNECTION_ID"
)
```

**Change camera resolution**

```python
set_video_property(
    connection_id="YOUR_CONNECTION_ID",
    property_name="width",
    value=1280
)
```

**Capture grayscale image**

```python
capture_grayscale(
    connection_id="YOUR_CONNECTION_ID"
)
```

**Resize an image**

```python
capture_resized(
    connection_id="YOUR_CONNECTION_ID",
    width=320,
    height=240
)
```

**Rotate an image**

```python
capture_rotated(
    connection_id="YOUR_CONNECTION_ID",
    angle=90
)
```

Supported rotation angles: 90, 180, and 270 degrees.

**Crop an image**

```python
capture_cropped(
    connection_id="YOUR_CONNECTION_ID",
    x=100,
    y=100,
    width=200,
    height=200
)
```

## Testing

The project includes automated tests using Pytest and mocked camera objects.

Run the tests:

```bash
python -m pytest tests/ -v
```

The tests cover:

- Camera initialization
- Frame capture
- Horizontal flipping
- Camera property retrieval
- Camera property modification
- Connection closure
- Invalid connection handling
- Camera initialization failures
- Active connection listing
- Resource cleanup

The mocked tests do not require a physical webcam.

## Troubleshooting

**Camera not detected**

- Check whether the webcam is connected.
- Verify camera permissions.
- Try another device index, such as 1.
- Close applications currently using the webcam.

**Camera property modification fails**

Camera drivers and hardware may not support every property. A successful property-setting request does not necessarily guarantee that the requested value was applied.

**MCP Inspector connection issues**

- Verify the Python environment.
- Check that all dependencies are installed.
- Ensure the MCP server launches successfully.
- Check the MCP host configuration.

## Limitations

- This project supports still-image capture, not continuous video streaming.
- Camera property support depends on the hardware and OpenCV backend.
- Camera access requires appropriate operating-system permissions.
- Multiple cameras require separate device indices and available hardware.

## Future Improvements

- Additional image-processing operations.
- Better camera discovery and device enumeration.
- Expanded automated test coverage.
- Improved error reporting and structured tool responses.
- Support for additional video capture backends.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.