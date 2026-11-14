
import cv2
import uuid
import threading
import math


class CameraManager:

    def __init__(self):
        # Stores all active camera connections
        self.connections = {}

        # Prevents simultaneous operations from interfering
        self.lock = threading.RLock()

    # 1. Open camera connection
    def open_camera(self, device_index=0, name=None):
        
        if device_index < 0:
            raise ValueError("Device index cannot be negative")

        with self.lock:

            camera = cv2.VideoCapture(
                device_index,
                cv2.CAP_DSHOW
            )

            if not camera.isOpened():
                camera.release()
                raise RuntimeError(
                    f"Could not open camera {device_index}"
                )

            connection_id = str(uuid.uuid4())

            self.connections[connection_id] = {
                "camera": camera,
                "name": name or f"Camera {device_index}",
                "device_index": device_index
            }

            return connection_id

    # 2. Capture an image
    def capture_frame(self, connection_id, flip=False):

        with self.lock:

            if connection_id not in self.connections:
                raise ValueError("Invalid camera connection ID")

            camera = self.connections[connection_id]["camera"]

            success, frame = camera.read()

            if not success:
                raise RuntimeError("Failed to capture image")

            if flip:
                frame = cv2.flip(frame, 1)

            return frame

    # 3. Get camera properties
    def get_properties(self, connection_id):

        with self.lock:

            if connection_id not in self.connections:
                raise ValueError("Invalid connection ID")

            camera = self.connections[connection_id]["camera"]

            return {
                "width": camera.get(cv2.CAP_PROP_FRAME_WIDTH),
                "height": camera.get(cv2.CAP_PROP_FRAME_HEIGHT),
                "fps": camera.get(cv2.CAP_PROP_FPS),
                "brightness": camera.get(cv2.CAP_PROP_BRIGHTNESS),
                "contrast": camera.get(cv2.CAP_PROP_CONTRAST),
                "saturation": camera.get(cv2.CAP_PROP_SATURATION)
            }

    # 4. Set camera properties
    
    def set_property(self, connection_id, property_name, value):

        import math

        properties = {
            "width": cv2.CAP_PROP_FRAME_WIDTH,
            "height": cv2.CAP_PROP_FRAME_HEIGHT,
            "fps": cv2.CAP_PROP_FPS,
            "brightness": cv2.CAP_PROP_BRIGHTNESS,
            "contrast": cv2.CAP_PROP_CONTRAST,
            "saturation": cv2.CAP_PROP_SATURATION
        }

        # Validate property name
        if property_name not in properties:
            raise ValueError("Unsupported camera property")

        # Validate numeric value
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Property value must be numeric")

        if not math.isfinite(value):
            raise ValueError("Property value must be finite")

        if property_name in ("width", "height", "fps") and value <= 0:
            raise ValueError("Resolution and FPS must be positive")

        with self.lock:

            if connection_id not in self.connections:
                raise ValueError("Invalid connection ID")

            camera = self.connections[connection_id]["camera"]

            result = camera.set(
                properties[property_name],
                value
            )

            return bool(result)


    # 5. Close a camera connection
    def close_camera(self, connection_id):

        with self.lock:

            if connection_id not in self.connections:
                return False

            camera = self.connections[connection_id]["camera"]

            camera.release()

            del self.connections[connection_id]

            return True

    # 6. List active connections
    def list_connections(self):

        with self.lock:

            return [
                {
                    "connection_id": connection_id,
                    "name": details["name"],
                    "device_index": details["device_index"]
                }
                for connection_id, details in self.connections.items()
            ]

    # 7. Close all cameras
    def close_all(self):

        with self.lock:

            for details in self.connections.values():
                details["camera"].release()

            self.connections.clear()


# Shared camera manager instance
camera_manager = CameraManager()
