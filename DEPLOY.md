# Deployment Guide

Your project is ready for deployment on Vercel!

## Prerequisites
- You have Vercel CLI installed (checked, version 32.x available).
- You are logged into Vercel CLI.

## Deployment Steps

1. **Open your terminal** in this directory.
2. **Run the deployment command**:
   ```bash
   vercel
   ```
   - Follow the prompts (Select scope, Link to existing project: No, Project Name: feature-extraction, Directory: . (default)).
   - It should auto-detect the configuration from `vercel.json`.

3. **For Production**:
   ```bash
   vercel --prod
   ```

## Project Structure Changes
- **Updated UI**: The frontend has been revamped with a modern, dark-themed design.
- **Backend Reorganization**: Created an `api` directory containing the Flask backend logic (`index.py` and `main.py`) specifically for Vercel Serverless Functions.
- **Configuration**: Added `vercel.json` to handle routing between the React frontend and Python backend.

## Local Development
- Frontend: `cd frontend` then `npm run dev`
- Backend: `cd api` then `python index.py` (Frontend will need to point to localhost:5000)
- Note: The `vercel.json` rewrites only apply when deployed on Vercel or running `vercel dev`.
