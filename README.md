---
title: Webcam Object Detection
emoji: 📷
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 5.23.3
app_file: app.py
pinned: false
---

# Webcam Object Detection

A live webcam demo that runs **YOLOv8n** object detection and draws labeled
boxes with confidence scores on each processed frame. It also provides a
confidence threshold, a rolling event log, session totals, and CSV export.

**Live Hugging Face Space:** create the Space under your Hugging Face account,
then replace this placeholder with its URL:
`https://huggingface.co/spaces/<HF_USERNAME>/webcam-object-detection`

## How it works

The app sends webcam frames from the browser to Python, where Ultralytics
YOLOv8n predicts objects from the COCO dataset's 80 classes. The model weights
(`yolov8n.pt`) are downloaded automatically by Ultralytics the first time
detection runs; they are not stored in this repository. Detections below the
selected confidence threshold are filtered out. Frames are processed on CPU
and are not saved by the app. This small model can miss small or occluded
objects and is not intended for safety-critical use.

If no camera is available or permission is denied, allow camera access in the
browser's site settings and reload the page. A webcam must be connected and
available to the browser.

## Run locally

In PowerShell, from the repository folder:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Open the local URL printed in the terminal and allow the browser to use the
webcam.

## Hugging Face auto-deploy

1. Create a Gradio Space named `webcam-object-detection` in your Hugging Face
   account.
2. In the GitHub repository's **Settings → Secrets and variables → Actions**,
   add the repository secret `HF_TOKEN` with a Hugging Face token that has
   write access to the Space.
3. Add the repository variable `HF_SPACE_ID` with the value
   `<HF_USERNAME>/webcam-object-detection`.
4. Replace the live Space URL above with the URL of the Space you created.

Every push to `main` runs the verification job first. The deploy job runs only
after verification succeeds and pushes the repository to the configured Space.
Never commit or print the Hugging Face token.

## CI evidence

The GitHub Actions workflow records verification and deployment results in the
repository's **Actions** tab. Keep a link or screenshot of a failed run and the
subsequent fixed run for the assignment submission; do not fabricate a failed
run.
