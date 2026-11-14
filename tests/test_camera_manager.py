
import pytest
import numpy as np
from unittest.mock import patch

from camera_manager import CameraManager


class FakeCamera:

    def __init__(self, opened=True):
        self.opened = opened
        self.released = False
        self.properties = {}

    def isOpened(self):
        return self.opened

    def read(self):
        if self.released:
            return False, None

        # Simulated 100x100 BGR image
        frame = np.zeros((100, 100, 3), dtype=np.uint8)

        return True, frame

    def get(self, prop):
        return self.properties.get(prop, 30.0)

    def set(self, prop, value):
        self.properties[prop] = value
        return True

    def release(self):
        self.released = True


@pytest.fixture
def manager():
    return CameraManager()


def test_open_camera(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        connection_id = manager.open_camera(0)

    assert connection_id is not None
    assert connection_id in manager.connections


def test_capture_frame(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        connection_id = manager.open_camera(0)

        frame = manager.capture_frame(connection_id)

    assert frame.shape == (100, 100, 3)

    manager.close_all()


def test_capture_flip(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        connection_id = manager.open_camera(0)

        frame = manager.capture_frame(connection_id, flip=True)

    assert frame.shape == (100, 100, 3)

    manager.close_all()


def test_get_properties(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        connection_id = manager.open_camera(0)

        properties = manager.get_properties(connection_id)

    assert "width" in properties
    assert "height" in properties
    assert "fps" in properties

    manager.close_all()


def test_set_property(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        connection_id = manager.open_camera(0)

        result = manager.set_property(
            connection_id,
            "width",
            1280
        )

    assert result is True
    manager.close_all()


def test_close_camera(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        connection_id = manager.open_camera(0)

        result = manager.close_camera(connection_id)

    assert result is True
    assert fake_camera.released is True
    assert connection_id not in manager.connections


def test_invalid_connection(manager):

    with pytest.raises(ValueError):
        manager.capture_frame("invalid-id")


def test_camera_not_available(manager):

    fake_camera = FakeCamera(opened=False)

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        with pytest.raises(RuntimeError):
            manager.open_camera(0)


def test_list_connections(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        connection_id = manager.open_camera(
            0,
            name="Test Webcam"
        )

        connections = manager.list_connections()

    assert len(connections) == 1
    assert connections[0]["name"] == "Test Webcam"
    assert connections[0]["connection_id"] == connection_id

    manager.close_all()


def test_close_all(manager):

    fake_camera = FakeCamera()

    with patch(
        "camera_manager.cv2.VideoCapture",
        return_value=fake_camera
    ):
        manager.open_camera(0)
        manager.close_all()

    assert fake_camera.released is True
    assert len(manager.connections) == 0
