# 🏋️ AI Real-Time Gym Coach

**An AI-powered fitness coaching application designed to help users track exercises, monitor workout performance, and receive real-time coaching assistance.**

## 📌 Overview

AI Real-Time Gym Coach is a Python-based fitness application that brings together computer vision, pose detection, exercise tracking, and AI-powered coaching into one project.

The goal is to help users perform workouts with better awareness of their exercise movements and progress through intelligent tracking and coaching features.

## ✨ Features

- 🎯 **Pose Detection:** Uses pose-landmark detection to identify body keypoints for movement analysis.
- 🏋️ **Exercise Tracking:** Supports the development of real-time exercise monitoring and repetition tracking.
- 🤖 **AI Coaching:** Integrates an AI coaching service to provide workout-related assistance.
- 🔊 **Voice Assistance:** Includes text-to-speech and voice-pipeline components for audio-based interaction.
- 📊 **Workout Metrics:** Organizes exercise performance metrics for tracking and feedback.
- 🔐 **Authentication:** Includes an authentication interface.
- ⚙️ **Modular Architecture:** Separates computer vision, coaching, configuration, persistence, and UI logic into dedicated modules.

> Feature availability and accuracy depend on the current implementation, supported exercises, model configuration, and runtime environment.

## 🛠️ Tech Stack

- **Language:** Python
- **Computer Vision:** Pose landmark detection
- **AI/LLM:** AI-powered coaching integration
- **Audio:** Text-to-speech and voice-processing pipeline
- **Application UI:** Streamlit (if configured in the current application entry point)
- **Data & Persistence:** Python-based persistence components and SQLite database
- **Development Tools:** Git, GitHub, VS Code

## 📂 Project Structure

```text
AI-Real-Time-Gym-Coach/
├── .streamlit/              # Streamlit configuration
├── core/                    # Core application logic
├── detectors/               # Detection modules
├── ml_models/               # ML models and pose-landmarker assets
├── services/
│   ├── auth/                 # Authentication
│   ├── coaching/             # AI coaching and voice pipeline
│   ├── config/               # Workout configuration
│   ├── persistence/          # Data persistence
│   ├── state/                # Session defaults and state
│   ├── tracking/              # Workout metrics
│   ├── ui/                    # UI utilities
│   └── vision/                # Vision and exercise processing
├── static/                   # CSS and static assets
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
├── data.db                   # Local database, if required
├── .gitignore
└── README.md
```

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/shravan9102/AI-Real-Time-Gym-Coach.git
cd AI-Real-Time-Gym-Coach
```

### 2. Create a virtual environment

**Windows PowerShell**

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, you can use:

```powershell
.\venv\Scripts\python.exe -m pip install --upgrade pip
```

### 3. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 4. Configure environment variables

If the application uses a Groq API key or other external service credentials, create a local `.env` file or configure the environment variables required by your code.

Example:

```env
GROQ_API_KEY=your_groq_api_key_here
```

Use the exact variable names expected by your application. Never commit real API keys, passwords, or private credentials to GitHub.

### 5. Run the application

From the project root, run the entry point appropriate for your implementation.

For a Streamlit application:

```bash
streamlit run main.py
```

If `main.py` is a regular Python entry point instead, use:

```bash
python main.py
```

Open the local URL displayed in your terminal after the application starts.

## 🧠 How It Works

1. **Input:** The application receives the inputs required for a workout session.
2. **Pose Analysis:** Pose landmarks are used to analyze body positioning and movement.
3. **Exercise Processing:** Vision and tracking components process supported exercise movements and metrics.
4. **AI Coaching:** The coaching service can use an LLM integration to generate workout-related assistance.
5. **Voice Feedback:** Audio components support voice-based interaction where configured.
6. **Persistence:** Relevant application data can be stored through the persistence layer.

## 🔒 Security & Privacy

- Keep API keys and credentials in environment variables or local secrets configuration.
- Never commit `.env`, private database contents, or Streamlit secrets.
- Exclude virtual environments, Python cache files, and generated artifacts from version control.
- Review database contents before publishing the repository publicly.
- Do not rely on AI-generated exercise guidance as a substitute for professional medical advice.

## 🔮 Future Improvements

- Expand support for additional exercises.
- Improve repetition counting and movement-quality analysis.
- Add personalized workout plans and progress dashboards.
- Enhance voice interaction and coaching personalization.
- Add automated testing and model evaluation.
- Deploy a public demo with secure secret management.

## 👨‍💻 Author

**Shravan Kumar**

- GitHub: [@shravan9102](https://github.com/shravan9102)
- Project: [AI-Real-Time-Gym-Coach](https://github.com/shravan9102/AI-Real-Time-Gym-Coach)

## ⭐ Support

If you find this project interesting, consider giving the repository a ⭐ on GitHub.

---

*Built as an AI/ML project exploring computer vision, exercise tracking, and AI-powered fitness assistance.*
