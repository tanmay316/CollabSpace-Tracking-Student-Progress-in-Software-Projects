# CollabSpace - Software Engineering Project
A project portal for students, instructors and teaching assistants to submit, create and track projects.

This project consists of a frontend built using **Vue 3** and a backend developed with **Flask**. The app enables users to upload files, summarize content, and interact with a conversational AI.

---


## Setup Instructions

### Backend

1. **Navigate to the Backend Directory**:

   ```bash
   cd backend
   ```

2. **Create a Virtual Environment**:

   ```bash
   pip install virtualenv
   ```
   
   ```bash
   python -m venv venv
   ```

3. **Activate the Virtual Environment**:

   - **Windows**:

     ```bash
     venv\Scripts\activate
     ```

   - **Mac/Linux**:

     ```bash
     source venv/bin/activate
     ```

4. **Install Dependencies**:

   ```bash
   pip install -r requirements.txt
   ```

5. **Set Up Environment Variables**:

   Create a `.env` file in the `backend` directory with the following content:

   ```env
   GOOGLE_API_KEY=your_google_api_key_here
   ```

   Replace `your_google_api_key_here` with your actual Google API key.

6. **Run the Backend**:

   ```bash
   python app.py
   ```

   The backend will be available at `http://127.0.0.1:5000`.

---
### Redis-Server

1. **Run Redis-Server on Docker:**

   ```bash
   docker run --name my-redis -p 6379:6379 -d redis
   ```
2. **Stop Redis-Server:**

   ```bash
   docker stop my-redis
   ```

---
### MailHog SMTP

1. **Install MailHog**
   - **Mac/Linux**:
   ```bash
     brew install mailhog
   ```

2. **Run MailHog**
   - **To start mailhog now and restart at login**:
   ```bash
   brew services start mailhog
   ```

   - **To start mailhog now**:
   ```bash
   /opt/homebrew/opt/mailhog/bin/MailHog -api-bind-addr 127.0.0.1:8025 -smtp-bind-addr 127.0.0.1:1025 -ui-bind-addr 127.0.0.1:8025
   ```

---
### Frontend

1. **Navigate to the Frontend Directory**:

   ```bash
   cd frontend
   ```

2. **Install Node Modules**:

   ```bash
   npm install
   ```

3. **Run the Frontend**:

   ```bash
   npm run dev
   ```

   The frontend will be available at `http://localhost:5173`.

---

## How to Use

1. **Access the Application**:

   Open your web browser and navigate to `http://localhost:5173`.

2. **Upload Files or Provide a GitHub Link**:

   - Use the **sidebar** on the left to upload files (PDFs or code files) or input a GitHub repository link.

3. **Chat or Summarize**:

   - **Chat**: Ask questions related to the uploaded files or repository in the chatbox.
   - **Summarize**: Use the **Summarize** button to generate a summary of the uploaded content.

---


## Project Structure

```
project-root/
├── backend/
│   ├── app.py
│   ├── models.py
│   ├── requirements.txt
│   ├── .env
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── student_routes.py
│   │   ├── instructor_routes.py
│   │   ├── TA_routes.py
│   │   ├── admin_routes.py
│   │   ├── authentication.py
│   │   ├── rag_routes.py
│   │   └── pdf_routes.py
│   └── utils/
│       ├── __init__.py
│       ├── repo_utils.py
│       ├── chat_utils.py
│       ├── search_utils.py
│       └── pdf_utils.py
└── frontend/
    ├── index.html
    ├── package.json
    ├── vite.config.js
    └── src/
        ├── main.js
        ├── App.vue
        ├── router/
        │   └── index.js
        ├── components/
        │   ├── Navbar.vue
        │   ├── ChatInterface.vue
        │   └── AIChatIcon.vue
        └── views/
            ├── ProjectView.vue
            ├── RegisterView.vue
            ├── LoginView.vue
            ├── MilestoneView.vue
            ├── MilestoneSubmissionFeedbackView.vue
            ├── MentorshipView.vue
            ├── ChatUsersView.vue
            ├── ChatInterfaceView.vue
            └── SummaryAI.vue
```
