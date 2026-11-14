
from camera_manager import camera_manager
import cv2

connection_id = None

try:
    # Open webcam
    connection_id = camera_manager.open_camera(
        device_index=0,
        name="My Webcam"
    )

    print("Camera opened!")
    print("Connection ID:", connection_id)

    # Get camera properties
    properties = camera_manager.get_properties(connection_id)

    print("\nCamera Properties:")
    print(properties)

    # Capture image
    frame = camera_manager.capture_frame(connection_id)

    # Save image
    cv2.imwrite("test_capture.jpg", frame)

    print("\nImage captured successfully!")

    # List connections
    print("\nActive Connections:")
    print(camera_manager.list_connections())

finally:
    if connection_id:
        camera_manager.close_camera(connection_id)

    print("\nCamera released!")


