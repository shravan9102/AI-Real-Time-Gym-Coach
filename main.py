# import streamlit as st
# import os
# import time
# import pandas as pd
# from services.auth.login_wall import render_login_wall
# from services.state.session_defaults import initial_session_defaults
# from services.config.workout_config import EXERCISE_OPTIONS
# from services.ui.style_loader import load_css, inject_local_font, inject_webrtc_styles
# from services.persistence.exercise_repository import init_db
# from streamlit_webrtc import webrtc_streamer, WebRtcMode
# from services.vision.exercise_video_processor import VideoProcessorClass
# from services.tracking.metrics import sync_metrics_update
# from services.persistence.exercise_repository import get_users_exercises
# from groq import Groq
# from services.coaching.llm import LLMCoach
# from services.coaching.tts import TextToSpeech
# from services.coaching.voice_pipeline import VoicePipeline, autoplay_audio

  
# def main():
#     st.set_page_config(
#         page_icon="🏋️‍♀️",
#         page_title="AI Real-time GYM Coach",
#         initial_sidebar_state="expanded",
#         layout="centered"
#     )

#     load_css(os.path.join(os.getcwd(), "static", "style.css"))
#     inject_local_font(os.path.join(os.getcwd(), "static", "AdobeClean.otf"), "AdobeClean")

#     init_db()

#     if not render_login_wall():
#         return 

#     initial_session_defaults()

#     if "voice_pipeline" not in st.session_state:
#         try:
#             api_key = os.environ.get("GROQ_API_KEY", "")

#             if not api_key and hasattr(st, "secrets") and "GROQ_API_KEY" in st.secrets:
#                 api_key = st.secrets["GROQ_API_KEY"]
            
#             groq_client = Groq(api_key=api_key)
#             llm_coach = LLMCoach(groq_client)
#             tts = TextToSpeech()
#             st.session_state.voice_pipeline = VoicePipeline(llm_coach, tts)
#         except Exception as e:
#             st.session_state.voice_pipeline = None

#     workout_started = st.session_state.get("workout_started", False)
    
#     with st.sidebar:
#         st.title("🏋️‍♂️ Apna AI Coach")

#         if st.session_state.username:
#             st.caption(f"👤 Login as {st.session_state.username}")

#         st.divider()

#         st.subheader("Workout Plan")

#         if not workout_started:
#             plan_exercise = st.selectbox("Exercise", options=EXERCISE_OPTIONS, key="plan_exercise")

#             plan_sets = st.number_input("Sets", min_value=0, max_value=50, key="plan_sets", step=1)

#             plan_reps = st.number_input("Reps per Set", min_value=0, max_value=50, key="plan_reps", step=1)

#             st.markdown("")

#             start_session_button = st.button("Start Workout", width="stretch", key="start_session_button")

#             if start_session_button:
#                 st.session_state.exercise_type = plan_exercise
#                 st.session_state.target_sets = int(plan_sets)
#                 st.session_state.reps_per_set = int(plan_reps)
#                 st.session_state.reps = 0
#                 st.session_state.workout_started = True
#                 st.session_state.set_cycle_started_at = time.time()
#                 st.session_state.last_saved_sets_completed = 0

#                 if st.session_state.voice_pipeline:
#                     result = st.session_state.voice_pipeline.process_event(
#                         event="workout_started",
#                         exercise=plan_exercise,
#                         metrics={}
#                     )
                    
#                     if result:
#                         st.session_state.audio_to_play, st.session_state.coach_feedback = result

#                 st.session_state.last_notified_sets_completed = 0
#                 st.session_state.last_notified_workout_complete = False
#                 st.rerun()
#         else:
#             exercise = st.session_state.get("exercise_type")
#             sets = st.session_state.get("target_sets")
#             reps = st.session_state.get("reps_per_set")

#             st.info(f"**{exercise}** -- {sets} Sets / {reps} Reps")

#             end_session_button = st.button("End Workout", key="end_session_button", width="stretch")

#             if end_session_button:
#                 st.session_state.workout_started = False
                
#                 if st.session_state.voice_pipeline:
#                     result = st.session_state.voice_pipeline.process_event(
#                         event="workout_completed",
#                         exercise=exercise,
#                         metrics={}
#                     )
#                     if result:
#                         st.session_state.audio_to_play, st.session_state.coach_feedback = result

#                 st.rerun()

#         if workout_started:
#             st.divider()

#             exercise = st.session_state.get("exercise_type")
#             total_reps = st.session_state.get("reps")
#             current_set_reps = st.session_state.get("current_set_reps")
#             reps_per_set = st.session_state.get("reps_per_set")
#             sets_completed = st.session_state.get("sets_completed")
#             target_sets = st.session_state.get("target_sets")

#             st.subheader("Progress")

#             st.metric("Total Reps", f"{total_reps}")
#             st.metric("Current Set Reps", f"{current_set_reps} / {reps_per_set}")
#             st.metric("Sets Completed", f"{sets_completed} / {target_sets}")

#             st.divider()

#             if exercise == "Squats":
#                 st.subheader("Squat Metrics")
#                 st.metric("Knee Angle", f"{st.session_state.knee_angle}°")
#                 st.metric("Back Angle", f"{st.session_state.back_angle}°")
#                 st.metric("Depth Status", st.session_state.depth_status)

#             elif exercise == "Push-ups":
#                 st.subheader("Push-up Metrics")
#                 st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
#                 st.metric("Body Alignment", st.session_state.body_alignment)
#                 st.metric("Hip Position", st.session_state.hip_status)

#             elif exercise == "Biceps Curls (Dumbbell)":
#                 st.subheader("Curl Metrics")
#                 st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
#                 st.metric("Shoulder Stability", st.session_state.shoulder_status)
#                 st.metric("Swing Detection", st.session_state.swing_status)

#             elif exercise == "Shoulder Press":
#                 st.subheader("Shoulder Press Metrics")
#                 st.metric("Elbow Angle", f"{st.session_state.elbow_angle}°")
#                 st.metric("Arm Extension", st.session_state.extension_status)
#                 st.metric("Back Arch", st.session_state.back_arch_status)

#             elif exercise == "Lunges":
#                 st.subheader("Lunge Metrics")
#                 st.metric("Front Knee Angle", f"{st.session_state.front_knee_angle}°")
#                 st.metric("Torso Angle", f"{st.session_state.torso_angle}°")
#                 st.metric("Balance Status", st.session_state.balance_status)

#     st.title("AI Real-time GYM Coach")
#     st.markdown("#### Real-time pose detection with proactive AI voice coaching")
 
#     if st.session_state.get("audio_to_play"):
#         st.audio(
#         st.session_state.audio_to_play,
#         format="audio/mp3",
#         autoplay=False
#     )

#     if st.session_state.get("coach_feedback"):
#         st.markdown("")
#         st.success(f"🤖 **Coach:** {st.session_state.coach_feedback}")

#     if not workout_started:
#         st.markdown(
#             """
#             <div style="
#                 border: 10px dashed #444;
#                 border-radius: 0px;
#                 padding: 48px 32px;
#                 text-align: center;
#                 color: #888;
#                 margin-top: 32px;
#                 margin-bottom: 32px;
#             ">
#                 <h2 style="color:#ccc; margin-bottom:8px;">👈 Set your workout plan</h2>
#                 <p style="font-size:1.05rem;">
#                     Choose your exercise, sets and reps in the sidebar,<br>
#                     then click <strong>Start Workout</strong> to activate the camera and AI coach.
#                 </p>
#             </div>
#             """,
#             unsafe_allow_html=True,
#         )
#     else:
#         context = webrtc_streamer(
#             key="exercise-analysis",
#             mode=WebRtcMode.SENDRECV,
#             video_processor_factory=VideoProcessorClass,
#             rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
#             media_stream_constraints={
#                 "video": True,
#                 "audio": False
#             },
#             async_processing=True
#         )

#         sync_metrics_update(context)

#         if context.state.playing:
#             time.sleep(0.25)
#             st.rerun()

#         inject_webrtc_styles()

#     st.divider()

#     st.markdown("#### Workout History")

#     user_id = st.session_state.get("user_id", 0)

#     if isinstance(user_id, int):
#         history_rows = get_users_exercises(user_id)

#         arr = [
#             {
#                 "Exercise": row['exercise_name'],
#                 "Reps": row['reps'],
#                 "Sets": row['sets'],
#                 "Time (sec)": row['time'],
#                 "Date": row['created_at']
#             }
#             for row in history_rows
#         ]

#         df = pd.DataFrame(arr)

#         if not df.empty:
#             df["Date"] = pd.to_datetime(df["Date"]).dt.date
#             agg_df = df.groupby(["Exercise", "Date"]).agg({
#                 "Reps": 'sum',
#                 "Sets": "sum",
#                 "Time (sec)": "sum"
#             }).reset_index()
#             agg_df.index += 1
#             st.table(agg_df, border="horizontal")
#         else:
#             st.info("No workout history found.")


# if __name__ == "__main__":
#     main()
    
    
 
import os
import time
import base64

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

from dotenv import load_dotenv
from groq import Groq
from streamlit_webrtc import webrtc_streamer, WebRtcMode

from services.auth.login_wall import render_login_wall
from services.state.session_defaults import initial_session_defaults
from services.config.workout_config import EXERCISE_OPTIONS
from services.ui.style_loader import (
    load_css,
    inject_local_font,
    inject_webrtc_styles,
)
from services.persistence.exercise_repository import (
    init_db,
    get_users_exercises,
)
from services.vision.exercise_video_processor import VideoProcessorClass
from services.tracking.metrics import sync_metrics_update
from services.coaching.llm import LLMCoach
from services.coaching.tts import TextToSpeech
from services.coaching.voice_pipeline import VoicePipeline


# Load .env from the same folder as main.py.
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))


def initialize_voice_pipeline(force=False):
    """Initialize the AI voice coach."""

    if (
        not force
        and st.session_state.get("voice_pipeline") is not None
    ):
        return True

    st.session_state.voice_pipeline = None
    st.session_state.voice_error = None

    try:
        api_key = os.environ.get("GROQ_API_KEY", "").strip()

        if not api_key:
            try:
                api_key = str(
                    st.secrets.get("GROQ_API_KEY", "")
                ).strip()
            except Exception:
                api_key = ""

        if not api_key:
            raise ValueError(
                "GROQ_API_KEY is missing. Add it to your .env file "
                "or Streamlit secrets."
            )

        groq_client = Groq(api_key=api_key)
        llm_coach = LLMCoach(groq_client)
        tts = TextToSpeech()

        st.session_state.voice_pipeline = VoicePipeline(
            llm_coach,
            tts,
        )
        st.session_state.voice_error = None

        print("Voice pipeline initialized successfully.")
        return True

    except Exception as exc:
        st.session_state.voice_pipeline = None
        st.session_state.voice_error = (
            f"{type(exc).__name__}: {exc}"
        )

        print(
            f"VOICE INITIALIZATION ERROR: "
            f"{type(exc).__name__}: {exc}"
        )
        return False


def generate_coach_feedback(event, exercise, metrics=None):
    """Generate coach feedback and save its audio."""

    pipeline = st.session_state.get("voice_pipeline")

    if pipeline is None:
        st.session_state.audio_to_play = None

        if not st.session_state.get("voice_error"):
            st.session_state.voice_error = (
                "Voice pipeline is not initialized."
            )
        return

    try:
        result = pipeline.process_event(
            event=event,
            exercise=exercise,
            metrics=metrics or {},
        )

        if result is None:
            return

        if not isinstance(result, (tuple, list)) or len(result) != 2:
            raise ValueError(
                "VoicePipeline.process_event() must return "
                "(audio_bytes, feedback_text)."
            )

        audio_data, feedback_text = result

        if feedback_text:
            st.session_state.coach_feedback = feedback_text

        if not audio_data:
            st.session_state.audio_to_play = None
            st.session_state.voice_error = (
                "Coach feedback was generated, but TTS returned "
                "empty audio. Check TTS and internet connectivity."
            )
            return

        if not isinstance(audio_data, (bytes, bytearray)):
            st.session_state.audio_to_play = None
            st.session_state.voice_error = (
                f"Unexpected audio type: {type(audio_data).__name__}"
            )
            return

        # Generate a new playback ID for each new voice response.
        st.session_state.audio_to_play = bytes(audio_data)
        st.session_state.audio_play_id = (
            st.session_state.get("audio_play_id", 0) + 1
        )
        st.session_state.voice_error = None

    except Exception as exc:
        st.session_state.voice_error = (
            f"{type(exc).__name__}: {exc}"
        )

        print(
            f"VOICE GENERATION ERROR: "
            f"{type(exc).__name__}: {exc}"
        )


def render_automatic_audio():
    """Render audio without visible player controls."""

    audio_data = st.session_state.get("audio_to_play")
    play_id = st.session_state.get("audio_play_id", 0)

    if not audio_data:
        return

    audio_base64 = base64.b64encode(audio_data).decode("utf-8")

    # A unique key lets Streamlit create a fresh player for each response.
    components.html(
        f"""
        <!DOCTYPE html>
        <html>
        <body style="margin:0;padding:0;overflow:hidden;">
            <audio id="coach-audio-{play_id}" autoplay playsinline>
                <source
                    src="data:audio/mpeg;base64,{audio_base64}"
                    type="audio/mpeg"
                >
            </audio>

            <script>
                const audio = document.getElementById(
                    "coach-audio-{play_id}"
                );

                if (audio) {{
                    audio.play().catch((error) => {{
                        console.warn(
                            "Coach audio autoplay was blocked:",
                            error
                        );
                    }});
                }}
            </script>
        </body>
        </html>
        """,
        height=0,
        scrolling=False,
    )


def main():
    st.set_page_config(
        page_icon="🏋️‍♀️",
        page_title="AI Real-time GYM Coach",
        initial_sidebar_state="expanded",
        layout="centered",
    )

    load_css(
        os.path.join(os.getcwd(), "static", "style.css")
    )

    inject_local_font(
        os.path.join(os.getcwd(), "static", "AdobeClean.otf"),
        "AdobeClean",
    )

    init_db()

    if not render_login_wall():
        return

    initial_session_defaults()

    st.session_state.setdefault("voice_pipeline", None)
    st.session_state.setdefault("voice_error", None)
    st.session_state.setdefault("audio_to_play", None)
    st.session_state.setdefault("audio_play_id", 0)
    st.session_state.setdefault("coach_feedback", None)

    if st.session_state.voice_pipeline is None:
        initialize_voice_pipeline()

    workout_started = st.session_state.get(
        "workout_started", False
    )

    with st.sidebar:
        st.title("🏋️‍♂️ Apna AI Coach")

        username = st.session_state.get("username")
        if username:
            st.caption(f"👤 Login as {username}")

        st.divider()
        st.subheader("Workout Plan")

        if not workout_started:
            plan_exercise = st.selectbox(
                "Exercise",
                options=EXERCISE_OPTIONS,
                key="plan_exercise",
            )

            plan_sets = st.number_input(
                "Sets",
                min_value=0,
                max_value=50,
                key="plan_sets",
                step=1,
            )

            plan_reps = st.number_input(
                "Reps per Set",
                min_value=0,
                max_value=50,
                key="plan_reps",
                step=1,
            )

            start_session_button = st.button(
                "Start Workout",
                use_container_width=True,
                key="start_session_button",
            )

            if start_session_button:
                st.session_state.exercise_type = plan_exercise
                st.session_state.target_sets = int(plan_sets)
                st.session_state.reps_per_set = int(plan_reps)
                st.session_state.reps = 0
                st.session_state.workout_started = True
                st.session_state.set_cycle_started_at = time.time()
                st.session_state.last_saved_sets_completed = 0
                st.session_state.last_notified_sets_completed = 0
                st.session_state.last_notified_workout_complete = False

                st.session_state.audio_to_play = None
                st.session_state.coach_feedback = None

                generate_coach_feedback(
                    event="workout_started",
                    exercise=plan_exercise,
                )

                st.rerun()

        else:
            exercise = st.session_state.get("exercise_type")
            sets = st.session_state.get("target_sets", 0)
            reps = st.session_state.get("reps_per_set", 0)

            st.info(
                f"**{exercise}** -- {sets} Sets / {reps} Reps"
            )

            end_session_button = st.button(
                "End Workout",
                key="end_session_button",
                use_container_width=True,
            )

            if end_session_button:
                generate_coach_feedback(
                    event="workout_completed",
                    exercise=exercise,
                )

                st.session_state.workout_started = False
                st.rerun()

        if workout_started:
            exercise = st.session_state.get("exercise_type")

            st.divider()
            st.subheader("Progress")

            st.metric(
                "Total Reps",
                st.session_state.get("reps", 0),
            )

            st.metric(
                "Current Set Reps",
                f"{st.session_state.get('current_set_reps', 0)} / "
                f"{st.session_state.get('reps_per_set', 0)}",
            )

            st.metric(
                "Sets Completed",
                f"{st.session_state.get('sets_completed', 0)} / "
                f"{st.session_state.get('target_sets', 0)}",
            )

            metric_map = {
                "Squats": [
                    ("Knee Angle", "knee_angle", "°"),
                    ("Back Angle", "back_angle", "°"),
                    ("Depth Status", "depth_status", ""),
                ],
                "Push-ups": [
                    ("Elbow Angle", "elbow_angle", "°"),
                    ("Body Alignment", "body_alignment", ""),
                    ("Hip Position", "hip_status", ""),
                ],
                "Biceps Curls (Dumbbell)": [
                    ("Elbow Angle", "elbow_angle", "°"),
                    ("Shoulder Stability", "shoulder_status", ""),
                    ("Swing Detection", "swing_status", ""),
                ],
                "Shoulder Press": [
                    ("Elbow Angle", "elbow_angle", "°"),
                    ("Arm Extension", "extension_status", ""),
                    ("Back Arch", "back_arch_status", ""),
                ],
                "Lunges": [
                    ("Front Knee Angle", "front_knee_angle", "°"),
                    ("Torso Angle", "torso_angle", "°"),
                    ("Balance Status", "balance_status", ""),
                ],
            }

            if exercise in metric_map:
                st.divider()
                st.subheader(f"{exercise} Metrics")

                for label, key, suffix in metric_map[exercise]:
                    value = st.session_state.get(key, "N/A")
                    st.metric(label, f"{value}{suffix}")

    st.title("AI Real-time GYM Coach")

    st.markdown(
        "#### Real-time pose detection with proactive AI voice coaching"
    )

    voice_error = st.session_state.get("voice_error")

    if voice_error:
        st.warning(f"Voice diagnostic: {voice_error}")

        if st.button(
            "Retry Voice Initialization",
            key="retry_voice_initialization",
        ):
            initialize_voice_pipeline(force=True)
            st.rerun()

    # Automatically attempt playback without showing a Play control.
    render_automatic_audio()

    feedback = st.session_state.get("coach_feedback")

    if feedback:
        st.success(f"🤖 **Coach:** {feedback}")

    if not workout_started:
        st.markdown(
            """
            <div style="
                border: 10px dashed #444;
                border-radius: 0;
                padding: 48px 32px;
                text-align: center;
                color: #888;
                margin-top: 32px;
                margin-bottom: 32px;
            ">
                <h2 style="color:#ccc; margin-bottom:8px;">
                    👈 Set your workout plan
                </h2>
                <p style="font-size:1.05rem;">
                    Choose your exercise, sets and reps in the sidebar,
                    then click <strong>Start Workout</strong>
                    to activate the camera and AI coach.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    else:
        context = webrtc_streamer(
            key="exercise-analysis",
            mode=WebRtcMode.SENDRECV,
            video_processor_factory=VideoProcessorClass,
            rtc_configuration={
                "iceServers": [
                    {"urls": ["stun:stun.l.google.com:19302"]}
                ]
            },
            media_stream_constraints={
                "video": True,
                "audio": False,
            },
            async_processing=True,
        )

        sync_metrics_update(context)

        # Preserve the existing camera refresh behavior.
        if context.state.playing:
            time.sleep(0.25)
            st.rerun()

        inject_webrtc_styles()

    st.divider()
    st.markdown("#### Workout History")

    user_id = st.session_state.get("user_id", 0)

    if isinstance(user_id, int):
        history_rows = get_users_exercises(user_id)

        rows = [
            {
                "Exercise": row["exercise_name"],
                "Reps": row["reps"],
                "Sets": row["sets"],
                "Time (sec)": row["time"],
                "Date": row["created_at"],
            }
            for row in history_rows
        ]

        df = pd.DataFrame(rows)

        if not df.empty:
            df["Date"] = pd.to_datetime(df["Date"]).dt.date

            agg_df = (
                df.groupby(["Exercise", "Date"])
                .agg({
                    "Reps": "sum",
                    "Sets": "sum",
                    "Time (sec)": "sum",
                })
                .reset_index()
            )

            agg_df.index += 1
            st.table(agg_df, border="horizontal")
        else:
            st.info("No workout history found.")


if __name__ == "__main__":
    main()
   

 
