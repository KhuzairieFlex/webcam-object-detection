import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import numpy as np

import app


class FakeModel:
    def __init__(self, result):
        self.result = result
        self.confidence = None

    def predict(self, source, conf, verbose):
        self.confidence = conf
        return [self.result]


class AppTests(unittest.TestCase):
    def test_process_frame_draws_and_records_detections(self):
        frame = np.zeros((2, 2, 3), dtype=np.uint8)
        result = SimpleNamespace(
            plot=lambda: frame,
            names={0: "person"},
            boxes=[SimpleNamespace(cls=[0], conf=[0.91])],
        )
        model = FakeModel(result)

        with patch.object(app, "_model", model):
            annotated, status, events, total, session = app.process_frame(
                frame,
                0.6,
                {"events": [], "total": 0},
            )

        self.assertEqual(model.confidence, 0.6)
        self.assertTrue(np.array_equal(annotated, frame[:, :, ::-1]))
        self.assertIn("1 objek dikesan", status)
        self.assertEqual(events[0][1:], ["person", 0.91])
        self.assertEqual(total, 1)
        self.assertEqual(session["total"], 1)

    def test_missing_frame_returns_clear_camera_message(self):
        annotated, status, events, total, session = app.process_frame(
            None,
            0.45,
            {"events": [["time", "cup", 0.8]], "total": 1},
        )

        self.assertIsNone(annotated)
        self.assertIn("akses kamera", status)
        self.assertEqual(events, [["time", "cup", 0.8]])
        self.assertEqual(total, 1)
        self.assertEqual(session["total"], 1)

    def test_export_events_creates_csv(self):
        path = app.export_events(
            {"events": [["2026-01-01T12:00:00+08:00", "person", 0.91]]}
        )
        try:
            content = Path(path).read_text(encoding="utf-8")
        finally:
            Path(path).unlink(missing_ok=True)

        self.assertIn("Timestamp,Object,Confidence", content)
        self.assertIn("person", content)


if __name__ == "__main__":
    unittest.main()
