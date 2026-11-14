
import cv2

from mcp.server.fastmcp import FastMCP, Image

from camera_manager import camera_manager


# ==========================================
# Initialize MCP Server
# ==========================================

mcp = FastMCP("Video Still Capture MCP")


# ==========================================
# Helper Function: Convert OpenCV frame to MCP Image
# ==========================================

def frame_to_image(frame):
    """
    Convert an OpenCV image (NumPy array)
    into an MCP Image object.
    """

    success, encoded_image = cv2.imencode(".jpg", frame)

    if not success:
        raise RuntimeError("Failed to encode image")

    return Image(
        data=encoded_image.tobytes(),
        format="jpeg"
    )


# ==========================================
# TOOL 1: Quick Capture
# ==========================================

@mcp.tool()
def quick_capture(
    device_index: int = 0,
    flip: bool = False
) -> Image:
    """
    Capture a single image from a webcam.

    Opens the camera, captures one frame,
    and automatically releases the camera.
    """

    connection_id = camera_manager.open_camera(device_index)

    try:
        frame = camera_manager.capture_frame(
            connection_id,
            flip
        )

        return frame_to_image(frame)

    finally:
        camera_manager.close_camera(connection_id)


# ==========================================
# TOOL 2: Open Camera
# ==========================================

@mcp.tool()
def open_camera(
    device_index: int = 0,
    name: str = "My Webcam"
) -> str:
    """
    Open a persistent camera connection.

    Returns a unique connection ID.
    """

    connection_id = camera_manager.open_camera(
        device_index,
        name
    )

    return connection_id


# ==========================================
# TOOL 3: Capture Frame
# ==========================================

@mcp.tool()
def capture_frame(
    connection_id: str,
    flip: bool = False
) -> Image:
    """
    Capture an image from an existing camera connection.
    """

    frame = camera_manager.capture_frame(
        connection_id,
        flip
    )

    return frame_to_image(frame)


# ==========================================
# TOOL 4: Get Video Properties
# ==========================================

@mcp.tool()
def get_video_properties(connection_id: str) -> dict:
    """
    Retrieve webcam properties such as:
    width, height, FPS, brightness, contrast and saturation.
    """

    return camera_manager.get_properties(connection_id)


# ==========================================
# TOOL 5: Set Video Property
# ==========================================

@mcp.tool()
def set_video_property(
    connection_id: str,
    property_name: str,
    value: float
) -> bool:
    """
    Change a webcam property.

    Supported properties:
    width, height, fps, brightness, contrast, saturation.
    """

    return camera_manager.set_property(
        connection_id,
        property_name,
        value
    )


# ==========================================
# TOOL 6: Close Connection
# ==========================================

@mcp.tool()
def close_connection(connection_id: str) -> bool:
    """
    Close an existing webcam connection
    and release camera resources.
    """

    return camera_manager.close_camera(connection_id)


# ==========================================
# TOOL 7: List Active Connections
# ==========================================

@mcp.tool()
def list_active_connections() -> list:
    """
    Return information about all active camera connections.
    """

    return camera_manager.list_connections()



# ==========================================
# TOOL 8: Capture Grayscale Image
# ==========================================

@mcp.tool()
def capture_grayscale(connection_id: str) -> Image:
    """
    Capture an image and convert it to grayscale.
    """

    frame = camera_manager.capture_frame(connection_id)

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    return frame_to_image(gray)


# ==========================================
# TOOL 9: Capture Resized Image
# ==========================================

@mcp.tool()
def capture_resized(
    connection_id: str,
    width: int,
    height: int
) -> Image:
    """
    Capture an image and resize it to the requested dimensions.
    """

    if not (1 <= width <= 4096 and 1 <= height <= 4096):
        raise ValueError("Width and height must be between 1 and 4096")

    frame = camera_manager.capture_frame(connection_id)

    resized = cv2.resize(
        frame,
        (width, height),
        interpolation=cv2.INTER_AREA
    )

    return frame_to_image(resized)


# ==========================================
# TOOL 10: Capture Rotated Image
# ==========================================

@mcp.tool()
def capture_rotated(
    connection_id: str,
    angle: int
) -> Image:
    """
    Capture an image and rotate it by 90, 180 or 270 degrees.
    """

    frame = camera_manager.capture_frame(connection_id)

    rotations = {
        90: cv2.ROTATE_90_CLOCKWISE,
        180: cv2.ROTATE_180,
        270: cv2.ROTATE_90_COUNTERCLOCKWISE
    }

    if angle not in rotations:
        raise ValueError("Angle must be 90, 180 or 270")

    rotated = cv2.rotate(frame, rotations[angle])

    return frame_to_image(rotated)


# ==========================================
# TOOL 11: Capture Cropped Image
# ==========================================

@mcp.tool()
def capture_cropped(
    connection_id: str,
    x: int,
    y: int,
    width: int,
    height: int
) -> Image:
    """
    Capture an image and return a selected cropped region.

    x and y represent the top-left corner.
    """

    frame = camera_manager.capture_frame(connection_id)

    image_height, image_width = frame.shape[:2]

    if x < 0 or y < 0 or width <= 0 or height <= 0:
        raise ValueError("Invalid crop coordinates or dimensions")

    if x + width > image_width or y + height > image_height:
        raise ValueError("Crop region exceeds image boundaries")

    cropped = frame[y:y + height, x:x + width]

    return frame_to_image(cropped)



# ==========================================
# Start MCP Server
# ==========================================

if __name__ == "__main__":

    try:
        print("Starting Video Still Capture MCP Server...")

        mcp.run(transport="stdio")

    finally:
        print("Releasing all camera resources...")

        camera_manager.close_all()
