import csv
import tempfile
from datetime import datetime

import gradio as gr


MODEL_NAME = "yolov8n.pt"
MAX_EVENTS = 500
_model = None


def _get_model():
    global _model
    if _model is None:
        from ultralytics import YOLO

        _model = YOLO(MODEL_NAME)
    return _model


def process_frame(frame, confidence, session):
    session = session or {"events": [], "total": 0}
    events = list(session.get("events", []))
    total = int(session.get("total", 0))

    if frame is None:
        return (
            None,
            "Tiada frame kamera diterima. Sila beri akses kamera dan cuba lagi.",
            events,
            total,
            session,
        )

    try:
        result = _get_model().predict(
            source=frame,
            conf=float(confidence),
            verbose=False,
        )[0]
    except (ImportError, OSError, RuntimeError, ValueError) as error:
        return (
            frame,
            f"Could not load or run the detection model: {error}",
            events,
            total,
            session,
        )

    annotated = result.plot()[..., ::-1].copy()
    timestamp = datetime.now().astimezone().isoformat(timespec="seconds")
    names = result.names
    new_events = [
        [timestamp, str(names[int(box.cls[0])]), round(float(box.conf[0]), 3)]
        for box in result.boxes
    ]
    events.extend(new_events)
    events = events[-MAX_EVENTS:]
    total += len(new_events)
    updated_session = {"events": events, "total": total}

    if new_events:
        status = f"{len(new_events)} objek dikesan dalam frame ini."
    else:
        status = "Tiada objek dikesan. Cuba turunkan ambang keyakinan."

    return annotated, status, events, total, updated_session


def export_events(session):
    events = (session or {}).get("events", [])
    with tempfile.NamedTemporaryFile(
        mode="w",
        newline="",
        encoding="utf-8",
        suffix=".csv",
        prefix="webcam-detections-",
        delete=False,
    ) as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Timestamp", "Object", "Confidence"])
        writer.writerows(events)
        return csv_file.name


with gr.Blocks(title="Webcam Object Detection") as demo:
    gr.Markdown(
        "# Webcam Object Detection\n"
        "Allow camera access when your browser asks. If the camera is "
        "unavailable or access was denied, enable camera permission in the "
        "browser's site settings and reload this page."
    )

    with gr.Row():
        webcam = gr.Image(
            label="Live webcam",
            sources=["webcam"],
            type="numpy",
            streaming=True,
        )
        preview = gr.Image(label="Detections (YOLOv8n)", type="numpy")

    confidence = gr.Slider(
        minimum=0.1,
        maximum=0.9,
        value=0.45,
        step=0.05,
        label="Minimum confidence score",
    )
    status = gr.Textbox(
        label="Status",
        value="Allow camera access to start detecting objects.",
        interactive=False,
    )
    total_detections = gr.Number(
        label="Detections this session",
        value=0,
        precision=0,
        interactive=False,
    )
    event_log = gr.Dataframe(
        headers=["Timestamp", "Object", "Confidence"],
        value=[],
        label="Detection event log (up to the latest 500 events)",
        interactive=False,
    )
    session_state = gr.State({"events": [], "total": 0})
    download = gr.DownloadButton("Download event log (CSV)")
    download.click(export_events, inputs=session_state, outputs=download)

    gr.Markdown(
        "### How it works\n"
        "Webcam frames are processed by **YOLOv8n** (Ultralytics), a lightweight "
        "model pretrained on COCO to detect 80 object classes. Labels and "
        "confidence scores are shown on the image. The confidence threshold "
        "sets the minimum score for a detection. The model runs on CPU, and "
        "frames are not permanently stored. It may miss small or occluded "
        "objects and is not intended for safety-critical use."
    )

    webcam.stream(
        fn=process_frame,
        inputs=[webcam, confidence, session_state],
        outputs=[preview, status, event_log, total_detections, session_state],
        stream_every=0.5,
        time_limit=3600,
    )


if __name__ == "__main__":
    demo.queue().launch()
