# AirShare

**A simple copy-paste platform for sharing text, images, and documents without the need for login.**

## Table of Contents
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation](#installation)
- [Usage](#usage)
- [Background Cleanup and Deployment](#background-cleanup-and-deployment)
- [Contributing](#contributing)

## Features
- No login required: Easily paste your text and generate a unique code.
- Text sharing: Quickly share plain text snippets.
- File sharing: Upload and share images and documents.
- Unique code generation: Each pasted content generates a code for easy retrieval.

## Technologies Used
- **Backend**: Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite 

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/NitinYadav354/AirShare.git
   ```
2. Navigate to the project directory:
   ```bash
   cd online-clipboard
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```
4. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Apply migrations:
   ```bash
   python manage.py migrate
   ```
6. Start the development server:
   ```bash
   python manage.py runserver
   ```

## Usage
1. Open the application in your browser at `http://127.0.0.1:8000/`.
2. Paste your text or upload an image/document in the textbox.
3. Click the "Generate Code" button.
4. Share the generated code with others to allow them to access the content.

## Background Cleanup and Deployment
Clipboard items expire automatically after their configured lifetime.

During local development, AirShare uses Celery with Redis to schedule deletion tasks in the background. The production deployment did not provide a continuously running Celery worker at no additional cost, so relying on Celery and Redis there would make expiry cleanup unreliable.

For that reason, production performs cleanup synchronously during normal application requests, such as when a user submits or retrieves content. This keeps expired records and their uploaded files from being served without requiring a separate worker or Redis service. Because this approach is request-triggered, cleanup may wait until the next application request rather than running at an exact scheduled time.

## Contributing
Contributions are welcome! Please follow these steps to contribute:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature/YourFeatureName
   ```
3. Commit your changes:
   ```bash
   git commit -m 'Add some feature'
   ```
4. Push to the branch:
   ```bash
   git push origin feature/YourFeatureName
   ```
5. Open a pull request.

