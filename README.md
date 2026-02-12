# Mashup Generator

A web-based service for generating audio mashups from multiple online video sources based on user input parameters.

---

## Problem Statement

This project implements **Program 2 (Required): Develop a Web Service for Mashup Generation**.

The web service allows users to create a mashup by providing:
- Singer name  
- Number of videos  
- Duration of each video clip  
- Email ID  

The system fetches multiple video sources, extracts audio, trims each clip, and merges them into a single mashup file.

---

## Live Web Application

The Mashup Generator is deployed as an online web service and is accessible at:

**Live URL:**  
https://mashup-production-df6f.up.railway.app/

---

## Features

- Accepts singer name as input  
- User-defined number of videos  
- Custom duration for each audio clip  
- Automatic audio extraction from videos  
- Audio trimming and merging  
- Mashup file generation  
- Output packaged in compressed format  
- Accessible via a web interface  

---

## Technology Stack

- Backend: Python (Flask)  
- Frontend: HTML  
- Video Processing: yt-dlp  
- Audio Processing: FFmpeg, Pydub  
- Deployment: Railway Cloud Platform  
- Version Control: GitHub  

---

## Project Structure
mashup/
│
├── mashup_proj/
│ └── mashup_web/
│ ├── app.py
│ ├── requirements.txt
│ ├── runtime.txt
│ └── render.yaml
│
└── README.md


---

## How the System Works

1. The user fills out the web form with the required inputs.
2. The server fetches multiple online videos related to the singer.
3. Audio is extracted from each source.
4. Each clip is trimmed to the specified duration.
5. All clips are merged into a single mashup audio file.
6. The final output is generated and packaged for delivery.

---

## Input Validation

- Number of videos must be greater than 10  
- Duration of each clip must be greater than 20 seconds  
- Email ID must be valid  

---

## Deployment

The application is deployed on a cloud platform and runs as a live web service.  
Deployment configuration and environment settings are managed within the repository.

---

## Author

Sayyam Wadhwa  

---

## License

This project is created for academic and learning purposes.

