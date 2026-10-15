# import time
# import streamlit as st


# class VoicePipeline:
#     def __init__(self, llm, tts):
#         self.llm = llm
#         self.tts = tts
#         self.last_spoken_at = 0

#     def _find_form_issue(self, exercise, metrics):
#         if "issue" in metrics:
#             return metrics["issue"]

#         if exercise == "Squats":
#             depth = metrics.get("depth_status", "")
#             back_angle = metrics.get("back_angle", 180)
            
#             if depth == "TOO HIGH":
#                 return "The user's squat is not deep enough — knees are not bending sufficiently."

#             if isinstance(back_angle, (int, float)) and back_angle < 130:
#                 return "The user is leaning too far forward during the squat."

#         elif exercise == "Push-ups":
#             alignment = metrics.get("body_alignment", "")
#             hip_status = metrics.get("hip_status", "")
            
#             if alignment == "Poor Form":
#                 return "The user's body is not straight during the push-up."

#             if hip_status == "SAGGING":
#                 return "The user's hips are sagging down during the push-up."

#             if hip_status == "PIKED UP":
#                 return "The user's hips are too high — lower them to form a straight line."

#         elif exercise == "Biceps Curls (Dumbbell)":
#             swing = metrics.get("swing_status", "")
#             shoulder = metrics.get("shoulder_status", "")
            
#             if swing == "SWINGING":
#                 return "The user is swinging their torso during the curl — keep the body still."

#             if shoulder == "ELBOW DRIFTING":
#                 return "The user's elbow is drifting away from their side during the curl."

#         elif exercise == "Shoulder Press":
#             back_arch = metrics.get("back_arch_status", "")
#             extension = metrics.get("extension_status", "")
            
#             if back_arch == "Excessive Arch":
#                 return "The user is arching their lower back excessively during the press."

#             if back_arch == "Slight Arch":
#                 return "Slight back arch detected — encourage the user to brace their core."

#         elif exercise == "Lunges":
#             balance = metrics.get("balance_status", "")
            
#             if balance == "OFF BALANCE":
#                 return "The user is losing balance during the lunge — feet should be hip-width apart."

#         return None

#     def process_event(self, event, exercise, metrics):
#         issue = self._find_form_issue(exercise, metrics)

#         now = time.time()

#         is_major_issue = event in ["workout_started", "set_completed", "workout_completed"]

#         if not is_major_issue:
#             if not issue:
#                 return None
            
#             if now - self.last_spoken_at < 5:
#                 return None
            
#         text = self.llm.give_feedback(event, issue)
#         voice = self.tts.speak(text)

#         self.last_spoken_at = now

#         return voice, text
    

# def autoplay_audio(audio_bytes):
#     if not audio_bytes:
#         return
    
#     st.markdown("<style>[data-testid='stAudio'] {display: none;}</style>", unsafe_allow_html=True)
    
#     st.audio(audio_bytes, format="audio/mp3", autoplay=True)


import time
import streamlit as st


class VoicePipeline:
    def __init__(self, llm, tts):
        self.llm = llm
        self.tts = tts
        self.last_spoken_at = 0

    def _find_form_issue(self, exercise, metrics):
        metrics = metrics or {}

        if "issue" in metrics:
            return metrics["issue"]

        if exercise == "Squats":
            depth = metrics.get("depth_status", "")
            back_angle = metrics.get("back_angle", 180)

            if depth == "TOO HIGH":
                return (
                    "Your squat is not deep enough. "
                    "Bend your knees a little more."
                )

            if isinstance(back_angle, (int, float)) and back_angle < 130:
                return (
                    "You are leaning too far forward. "
                    "Keep your chest lifted."
                )

        elif exercise == "Push-ups":
            alignment = metrics.get("body_alignment", "")
            hip_status = metrics.get("hip_status", "")

            if alignment == "Poor Form":
                return "Keep your body straight during the push-up."

            if hip_status == "SAGGING":
                return "Your hips are sagging. Keep your body straight."

            if hip_status == "PIKED UP":
                return "Lower your hips and maintain a straight body line."

        elif exercise == "Biceps Curls (Dumbbell)":
            swing = metrics.get("swing_status", "")
            shoulder = metrics.get("shoulder_status", "")

            if swing == "SWINGING":
                return "Avoid swinging your body during the curl."

            if shoulder == "ELBOW DRIFTING":
                return "Keep your elbows close to your sides."

        elif exercise == "Shoulder Press":
            back_arch = metrics.get("back_arch_status", "")

            if back_arch == "Excessive Arch":
                return "Avoid arching your lower back. Brace your core."

            if back_arch == "Slight Arch":
                return "Brace your core and keep your back stable."

        elif exercise == "Lunges":
            balance = metrics.get("balance_status", "")

            if balance == "OFF BALANCE":
                return "Slow down and maintain your balance during the lunge."

        return None

    def process_event(self, event, exercise, metrics=None):
        metrics = metrics or {}

        try:
            issue = self._find_form_issue(exercise, metrics)
            now = time.time()

            major_events = {
                "workout_started",
                "set_completed",
                "workout_completed",
            }

            # Speak for major events; for form corrections,
            # speak only when an issue is detected.
            if event not in major_events:
                if not issue:
                    return None

                if now - self.last_spoken_at < 5:
                    return None

            # Generate coaching text.
            text = self.llm.give_feedback(event, issue)

            if not isinstance(text, str) or not text.strip():
                raise ValueError("The AI coach returned empty feedback.")

            # Convert text to speech.
            audio_bytes = self.tts.speak(text)

            if not audio_bytes:
                raise ValueError(
                    "Text-to-speech returned no audio. "
                    "Check the internet connection and gTTS."
                )

            self.last_spoken_at = now

            return audio_bytes, text

        except Exception as exc:
            st.error(
                f"Voice coach error: {type(exc).__name__}: {exc}"
            )
            return None


def autoplay_audio(audio_bytes):
    """Display audio controls so the user can play the coach's voice."""
    if not audio_bytes:
        st.warning("No coach audio was generated.")
        return

    st.audio(
        audio_bytes,
        format="audio/mp3",
        autoplay=False,
    )
