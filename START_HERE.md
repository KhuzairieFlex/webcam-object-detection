# START HERE

This is the beginner-friendly guide for the assignment and for this project.

## 1) Assignment goal

Build a real AI app that:
- takes a live input source (webcam recommended)
- runs it through a model in Python
- shows the result live in a web UI
- publishes it on Hugging Face Spaces
- auto-deploys from GitHub on every push to main

The recommended track is:
- Track A: Webcam + YOLOv8 object detection

## 2) What this project does

This repository is a webcam object detection app using:
- Python
- Gradio
- Ultralytics YOLOv8n
- a live browser webcam stream

The app:
- captures frames from the browser
- runs YOLOv8n on each frame
- draws bounding boxes and labels
- shows confidence scores
- logs detections
- lets you export the event log as CSV

## 3) Rules you must follow

### GitHub requirements
- repo must be public
- default branch must be main
- commit history should show real work over multiple days
- at least 10 meaningful commits
- README.md must explain the project and how to run it
- .gitignore must exclude virtualenvs, caches, secrets, and large model files
- no API keys or tokens in repo history

### CI/CD requirements
- workflow must be in .github/workflows
- workflow should run on push to main
- verify job must check:
  - required files exist
  - pip install -r requirements.txt works
  - Python imports succeed
  - Python files compile
- deploy job should push to Hugging Face using a GitHub secret named HF_TOKEN
- keep evidence of at least one failed pipeline run and then a fixed run

### Hugging Face Space requirements
- app must work for a stranger with little instruction
- README front matter should include sdk and app_file
- requirements.txt must pin or bound dependency versions
- app should handle no-camera / permission-denied gracefully

### App requirements
- live input must work in real time
- confidence or score must be shown
- include one extra engineering feature such as:
  - event log
  - CSV export
  - threshold control
  - class filter
  - session statistics
- include a short explanation of how the model works and its limitations

## 4) Recommended workflow for this project

1. Create GitHub repository
2. Create empty Hugging Face Space
3. Make the Gradio app run locally
4. Verify webcam access works
5. Add YOLOv8 detection and confidence filter
6. Add event log and export
7. Add README and .gitignore
8. Set up CI verify workflow
9. Add deploy workflow using HF_TOKEN
10. Push to main and confirm auto-deployment
11. Keep screenshots or links showing CI fail and fix

## 5) Project structure

This repo currently contains:
- app.py — main Gradio app
- README.md — project overview and deployment notes
- requirements.txt — Python dependencies
- .github/workflows — GitHub Action workflows
- tests — verification checks

## 6) How to run locally

Open PowerShell in the project folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python app.py
```

Then open the local URL shown in the terminal and allow the browser to use the webcam.

## 7) How the app works

The app sends webcam frames to the YOLOv8n model from Ultralytics.
- YOLOv8n is a lightweight object detection model
- it is trained on COCO classes
- it detects common objects like person, cup, laptop, phone, etc.
- it returns label + confidence score
- the app filters out low-confidence detections according to the selected threshold

Important limitations:
- CPU-only environments can be slower
- small or partially visible objects may be missed
- this is not a safety-critical system

## 8) What to prepare for submission

For the final assignment email, you should have:
- GitHub repo URL
- live Hugging Face Space URL
- a short note explaining the hardest problem and how you solved it

## 9) What to check before you submit

Make sure you have:
- repo is public and on main branch
- README has all required sections
- workflow runs successfully
- deploy uses a secret token, not a hardcoded one
- app gives real-time detection with confidence
- app handles camera permission issues gracefully
- there is evidence of a failed CI run that was fixed
- there are multiple commits across time, not one giant final commit

## 10) One-sentence summary

This assignment is not only about building an AI app — it is about building a real engineering workflow from GitHub to CI to deployment and public hosting.
