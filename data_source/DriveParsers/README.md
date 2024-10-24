# Google Drive Parser

## Overview
The Google Drive Parser  allows users to parse their Google Drive docs

## Prerequisites
Before you start using the Google Drive Parser, ensure you have the following set up:

1. **Google Cloud Project**: You need to create a new Google Cloud project or use an existing one. This project will enable access to the Google Drive API.
   
2. **Enable the Google Drive API**: 
   - Navigate to the [Google Cloud Console](https://console.cloud.google.com/flows/enableapi?apiid=drive.googleapis.com).
   - Follow the prompts to enable the Google Drive API for your project.

3. **Authorize Credentials for Desktop App**: 
   - Follow the instructions in the [Google Drive API Quickstart](https://developers.google.com/drive/api/quickstart/python#authorize_credentials_for_a_desktop_application) to set up your OAuth 2.0 credentials.
   - Download the `credentials.json` file provided by Google.

4. **Environment Setup**:
   - Save the `credentials.json` file in your project directory.
   - Set the path to the `credentials.json` file in your environment variables. Create a `.env` file in your project directory and include the following line:
     ```
     GOOGLE_ACCOUNT_FILE=/path/to/credentials.json
     ```

5. **Install Requirements**:
   - Install the necessary Python packages listed in the `requirements.txt` file. You can do this by running:
     ```bash
     pip install -r requirements.txt
     ```

## Usage
Once you have completed the setup, you can start using the Google Drive Parser:

1. **Run the Parser**: Execute the following command to start the parsing process:
   ```bash
   python3 init.py
