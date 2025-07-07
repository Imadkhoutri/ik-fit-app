import streamlit as st
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from PIL import Image
import base64
from reportlab.lib.utils import ImageReader

# --- PAGE SETUP --- (MUST BE FIRST STREAMLIT COMMAND)
st.set_page_config(page_title="IK Fit", layout="wide", initial_sidebar_state="collapsed")

# Enhanced CSS with centered logo and improved styling
st.markdown("""
<style>
    .logo-container {
        display: flex;
        justify-content: center;
        margin-bottom: 2rem;
    }
    .logo-img {
        border-radius: 50%;
        box-shadow: 0 4px 20px rgba(255, 107, 53, 0.3);
        transition: transform 0.3s ease;
    }
    .logo-img:hover {
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)
# Enhanced CSS for gym-themed professional styling
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    
    .main { 
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
        padding: 2rem;
        font-family: 'Inter', sans-serif;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    .main-title {
        background: linear-gradient(45deg, #ff6b35, #f7931e, #ffd23f);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 0 30px rgba(255, 107, 53, 0.3);
    }
    
    .subtitle {
        color: #a0a0a0;
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    
    .stButton>button {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        color: white;
        border-radius: 50px;
        padding: 1rem 3rem;
        font-weight: 700;
        font-size: 1.1rem;
        transition: all 0.3s ease;
        border: none;
        box-shadow: 0 8px 25px rgba(255, 107, 53, 0.3);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        background: linear-gradient(45deg, #e55a2b, #e8841a);
        transform: translateY(-3px);
        box-shadow: 0 12px 35px rgba(255, 107, 53, 0.4);
    }
    
    .input-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin-bottom: 2rem;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .section-title {
        color: #ffffff;
        font-size: 2rem;
        font-weight: 700;
        margin-bottom: 1.5rem;
        text-align: center;
        position: relative;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: -10px;
        left: 50%;
        transform: translateX(-50%);
        width: 60px;
        height: 3px;
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        border-radius: 2px;
    }
    
    .stSelectbox>div>div>div {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: black !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .stTextInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: black !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
        font-weight: 500 !important;
    }
    
    .stNumberInput>div>div>input {
        background-color: rgba(255, 255, 255, 0.1) !important;
        color: black !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 10px !important;
    }
    
    .stSlider>div>div>div>div {
        background: linear-gradient(45deg, #ff6b35, #f7931e) !important;
    }
    
    label {
        color: #ffffff !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
    }
    
    .plan-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    .plan-header {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 1rem;
    }
    
    .plan-info {
        color: #a0a0a0;
        text-align: center;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    
    .stExpander {
        background: rgba(255, 255, 255, 0.08) !important;
        border: 1px solid rgba(255, 255, 255, 0.15) !important;
        border-radius: 15px !important;
        margin-bottom: 1rem !important;
    }
    
    .stExpander summary {
        font-weight: 700 !important;
        color: #ffffff !important;
        font-size: 1.1rem !important;
        padding: 1rem !important;
    }
    
    .exercise-item {
        color: #e0e0e0;
        font-size: 1rem;
        margin: 0.5rem 0;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        font-weight: 500;
    }
    
    .notes {
        background: rgba(255, 107, 53, 0.1);
        border: 1px solid rgba(255, 107, 53, 0.3);
        padding: 1.5rem;
        border-left: 5px solid #ff6b35;
        border-radius: 15px;
        margin: 1rem 0;
        color: #ffffff;
    }
    
    .notes h4 {
        color: #ff6b35;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    
    .footer {
        text-align: center;
        color: #666;
        padding: 3rem 0;
        font-size: 1rem;
        font-weight: 500;
    }
    
    .motivational-message {
        background: linear-gradient(45deg, #ff6b35, #f7931e);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 1.5rem;
        font-weight: 700;
        text-align: center;
        margin: 2rem 0;
        padding: 1rem;
        border: 2px solid rgba(255, 107, 53, 0.3);
        border-radius: 15px;
        background-color: rgba(255, 107, 53, 0.05);
    }
    
    .name-highlight {
        color: #ff6b35;
        font-weight: 800;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Function to convert image to base64
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    except FileNotFoundError:
        return None

# Alternative method if you want to use PIL
def get_base64_from_pil(image_path):
    try:
        img = Image.open(image_path)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    except FileNotFoundError:
        return None

# --- LOGO + TITLE --- (Updated version)
logo_base64 = get_base64_image("logo.png")

if logo_base64:
    st.markdown(f"""
    <div style="display: flex; flex-direction: column; align-items: center; margin-top: 1rem; margin-bottom: 2rem;">
        <img src="data:image/png;base64,{logo_base64}" class="logo-img" width="120">
        <h1 class="main-title">IK Fit</h1>
        <p class="subtitle">Transform your body with a personalized training plan designed just for you!</p>
    </div>
    """, unsafe_allow_html=True)
else:
    # Fallback if logo file is not found
    st.markdown("""
    <div style="display: flex; flex-direction: column; align-items: center; margin-top: 1rem; margin-bottom: 2rem;">
        <div class="logo-placeholder" style="width: 120px; height: 120px; background: linear-gradient(45deg, #ff6b35, #f7931e); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold; color: white; margin-bottom: 1rem;">IK</div>
        <h1 class="main-title">IK Fit</h1>
        <p class="subtitle">Transform your body with a personalized training plan designed just for you!</p>
    </div>
    """, unsafe_allow_html=True)

# --- USER INPUTS ---
st.markdown('<div class="section-title">Let\'s get started!</div>', unsafe_allow_html=True)

user_name = st.text_input("How do you want us to call you?", "Champion", help="Enter your preferred name")

col1, col2 = st.columns(2)

with col1:
    weight = st.number_input(
        "Your current weight (kg)", 
        min_value=30, 
        max_value=200, 
        value=70, 
        step=1,
        help="Enter your weight in kilograms"
    )
    goal = st.selectbox(
        "What's your main goal?", 
        ["Hypertrophy", "Strength", "Powerbuilding", "Calisthenics / Street Lifting", "Running"],
        help="Select your primary fitness goal"
    )
    
    if goal == "Running":
        running_goal = st.selectbox(
            "Running goal type",
            ["5K Race", "10K Race", "Half Marathon", "Marathon", "General Fitness"],
            help="Select your running goal"
        )
        
        current_distance = st.selectbox(
            "Current weekly running distance",
            ["Less than 10 km", "10-20 km", "20-30 km", "30-40 km", "40+ km"],
            help="Select your current weekly running volume"
        )
    else:
        experience = st.selectbox(
            "Your experience level", 
            ["Beginner", "Intermediate", "Advanced"],
            help="Choose your training experience level"
        )

with col2:
    # Training days selection
    if goal == "Running":
        running_level = st.selectbox(
            "Current running level",
            ["Beginner", "Intermediate", "Advanced"],
            help="Select your current running experience"
        )
        
        if running_goal in ["Half Marathon", "Marathon"]:
            min_days = 4
        else:
            min_days = 3
            
        training_days = st.selectbox(
            "Training days per week", 
            list(range(min_days, 8)),  # Now goes up to 7 days
            index=0,
            help="How many days can you commit to training?"
        )
        
        if training_days == 7:
            st.warning("⚠️ Training 7 days a week is not recommended - your body needs rest days to recover!")
        
        if running_goal in ["Marathon"] and training_days < 4:
            st.warning("Marathon training typically requires at least 4 days per week for best results")
    else:
        # Allow 1-3 days for beginners, 3-7 for others
        if experience == "Beginner":
            training_days = st.selectbox(
                "Training days per week", 
                list(range(1, 4)),  # Allow 1, 2, or 3 days
                index=2,  # Default to 3 days
                help="How many days can you commit to training?"
            )
            if training_days < 3:
                st.warning("⚠️ 3 days per week is recommended for beginners. Research (Schoenfeld et al., 2017) shows training each muscle group at least twice per week optimizes hypertrophy and strength gains, and 3 days allows better frequency and recovery.")
        else:
            training_days = st.selectbox(
                "Training days per week", 
                list(range(3, 8)),  # Now goes up to 7 days
                index=1,  # Default to 4 days
                help="How many days can you commit to training?"
            )
            
            if training_days == 7:
                st.warning("⚠️ Training 7 days a week is not recommended - your body needs rest days to recover!")
    
    gender = st.selectbox(
        "👤 Your gender", 
        ["Male", "Female"],
        help="Select your gender"
    )
    
    # Split preference for intermediate and advanced users for all training days
    split_preference = None
    if goal != "Running" and experience in ["Intermediate", "Advanced"] and goal != "Calisthenics / Street Lifting":
        split_preference = st.selectbox(
            "🔄 Preferred training split", 
            ["Push/Pull/Legs (PPL)", "Upper/Lower"],
            help="Choose your preferred workout split"
        )

st.markdown('</div>', unsafe_allow_html=True)

# ------------------- RUNNING PLAN GENERATOR -------------------
def generate_running_plan(running_goal, running_level, training_days, current_distance, user_name):
    plan = {}
    base_speed = "easy pace (can hold conversation)"
    interval_pace = "5K race pace"
    tempo_pace = "slightly slower than 10K pace"
    long_run_pace = "30-60 sec/km slower than marathon pace"
    
    # Adjust paces based on level
    if running_level == "Intermediate":
        base_speed = "moderate pace (can speak in short sentences)"
        interval_pace = "slightly faster than 5K race pace"
        tempo_pace = "10K race pace"
        long_run_pace = "marathon pace"
    elif running_level == "Advanced":
        base_speed = "steady pace (comfortable but challenging)"
        interval_pace = "mile race pace"
        tempo_pace = "slightly faster than 10K race pace"
        long_run_pace = "slightly faster than marathon pace"
    
    # General Fitness Plan
    if running_goal == "General Fitness":
        for day in range(1, training_days + 1):
            if day == 1:
                plan[f"Day {day} - Easy Run"] = [
                    f"30-45 minutes at {base_speed}",
                    "Focus on consistent pace and breathing",
                    "Include 5-10 min dynamic warmup and cooldown"
                ]
            elif day == 2:
                plan[f"Day {day} - Interval Training"] = [
                    "10 min warmup at easy pace",
                    f"6-8 x 400m at {interval_pace} with 90s recovery jogs",
                    "10 min cooldown at easy pace",
                    "Total workout: 40-50 minutes"
                ]
            elif day == 3:
                plan[f"Day {day} - Recovery Run"] = [
                    "20-30 minutes very easy pace",
                    "Focus on form and relaxation",
                    "Can include walking breaks if needed"
                ]
            elif day == 4:
                plan[f"Day {day} - Tempo Run"] = [
                    "10 min warmup",
                    f"20 minutes at {tempo_pace}",
                    "10 min cooldown",
                    "Total workout: 40-45 minutes"
                ]
            elif day == 5:
                plan[f"Day {day} - Fartlek Training"] = [
                    "30-40 minutes with random speed bursts",
                    "Mix short (30sec) and long (2-3min) speed segments",
                    "Recovery between bursts should be equal or double the burst time"
                ]
            elif day == 6:
                plan[f"Day {day} - Long Run"] = [
                    f"60-75 minutes at {long_run_pace}",
                    "Build endurance gradually",
                    "Bring hydration/nutrition for runs over 60 minutes"
                ]
    
    # 5K Race Plan
    elif running_goal == "5K Race":
        if training_days == 3:
            plan = {
                "Day 1 - Base Run": [
                    f"30-40 minutes at {base_speed}",
                    "Focus on form and breathing",
                    "Include 4-6 strideouts at the end"
                ],
                "Day 2 - Speed Work": [
                    "10 min warmup",
                    f"6 x 400m at {interval_pace} with 200m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 45-50 minutes"
                ],
                "Day 3 - Long Run": [
                    f"45-60 minutes at {long_run_pace}",
                    "Build endurance",
                    "Last 10 minutes at goal 5K pace"
                ]
            }
        elif training_days == 4:
            plan = {
                "Day 1 - Base Run": [
                    f"30-40 minutes at {base_speed}",
                    "Include 6-8 x 20sec hill sprints at the end"
                ],
                "Day 2 - Speed Work": [
                    "10 min warmup",
                    f"8 x 400m at slightly faster than {interval_pace}",
                    "200m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 50-55 minutes"
                ],
                "Day 3 - Recovery Run": [
                    "20-30 minutes very easy pace",
                    "Optional: Include 4-5 x 30sec pickups"
                ],
                "Day 4 - Tempo Run": [
                    "10 min warmup",
                    f"20 minutes at {tempo_pace}",
                    "10 min cooldown",
                    "Total workout: 40-45 minutes"
                ]
            }
        elif training_days >= 5:
            plan = {
                "Day 1 - Base Run": [
                    f"40-50 minutes at {base_speed}",
                    "Include 6 x 30sec hill repeats at the end"
                ],
                "Day 2 - Speed Work": [
                    "10 min warmup",
                    f"5 x 800m at {interval_pace} with 400m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 50-60 minutes"
                ],
                "Day 3 - Recovery Run": [
                    "30 minutes very easy pace",
                    "Focus on smooth form"
                ],
                "Day 4 - Tempo Run": [
                    "10 min warmup",
                    f"25 minutes at {tempo_pace}",
                    "10 min cooldown",
                    "Total workout: 45-50 minutes"
                ],
                "Day 5 - Hill Repeats": [
                    "10 min warmup",
                    "6-8 x 45sec hill repeats at hard effort",
                    "Walk/jog down for recovery",
                    "10 min cooldown",
                    "Total workout: 40-45 minutes"
                ]
            }
            if training_days == 6:
                plan["Day 6 - Long Run"] = [
                    f"60-75 minutes at {long_run_pace}",
                    "Gradually increase distance",
                    "Last 15 minutes at goal 5K pace"
                ]
    
    # 10K Race Plan
    elif running_goal == "10K Race":
        if training_days == 3:
            plan = {
                "Day 1 - Base Run": [
                    f"40-50 minutes at {base_speed}",
                    "Include 4-6 x 30sec pickups at the end"
                ],
                "Day 2 - Speed Work": [
                    "10 min warmup",
                    f"5 x 1km at {interval_pace} with 400m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 50-60 minutes"
                ],
                "Day 3 - Long Run": [
                    f"60-75 minutes at {long_run_pace}",
                    "Build endurance",
                    "Last 20 minutes at goal 10K pace"
                ]
            }
        elif training_days >= 4:
            plan = {
                "Day 1 - Base Run": [
                    f"40-50 minutes at {base_speed}",
                    "Include 6 x 30sec hill sprints at the end"
                ],
                "Day 2 - Interval Work": [
                    "10 min warmup",
                    f"6 x 800m at {interval_pace} with 400m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 50-60 minutes"
                ],
                "Day 3 - Recovery Run": [
                    "30-40 minutes very easy pace",
                    "Focus on form and relaxation"
                ],
                "Day 4 - Tempo Run": [
                    "10 min warmup",
                    f"30 minutes at {tempo_pace}",
                    "10 min cooldown",
                    "Total workout: 50-55 minutes"
                ]
            }
            if training_days >= 5:
                plan["Day 5 - Fartlek"] = [
                    "10 min warmup",
                    "5 x 3min at 10K pace with 2min easy jog recovery",
                    "10 min cooldown",
                    "Total workout: 45-50 minutes"
                ]
            if training_days == 6:
                plan["Day 6 - Long Run"] = [
                    f"75-90 minutes at {long_run_pace}",
                    "Include 4 x 5min at goal 10K pace in second half",
                    "Bring hydration/nutrition"
                ]
    
    # Half Marathon Plan
    elif running_goal == "Half Marathon":
        if training_days == 4:
            plan = {
                "Day 1 - Base Run": [
                    f"45-60 minutes at {base_speed}",
                    "Include 6 x 30sec hill repeats at the end"
                ],
                "Day 2 - Speed Work": [
                    "10 min warmup",
                    f"6 x 1km at {interval_pace} with 400m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 60-70 minutes"
                ],
                "Day 3 - Recovery Run": [
                    "30-40 minutes very easy pace",
                    "Focus on form and relaxation"
                ],
                "Day 4 - Long Run": [
                    f"75-105 minutes at {long_run_pace}",
                    "Alternate between easy and goal HM pace",
                    "Bring hydration/nutrition"
                ]
            }
        elif training_days >= 5:
            plan = {
                "Day 1 - Base Run": [
                    f"50-60 minutes at {base_speed}",
                    "Include 6 x 30sec hill sprints at the end"
                ],
                "Day 2 - Interval Work": [
                    "10 min warmup",
                    f"5 x 1.5km at {interval_pace} with 600m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 70-80 minutes"
                ],
                "Day 3 - Recovery Run": [
                    "40 minutes very easy pace",
                    "Optional: Include 4-5 x 30sec pickups"
                ],
                "Day 4 - Tempo Run": [
                    "10 min warmup",
                    f"40 minutes at {tempo_pace}",
                    "10 min cooldown",
                    "Total workout: 60-65 minutes"
                ],
                "Day 5 - Fartlek": [
                    "10 min warmup",
                    "6 x 4min at HM pace with 2min easy jog recovery",
                    "10 min cooldown",
                    "Total workout: 60 minutes"
                ]
            }
            if training_days == 6:
                plan["Day 6 - Long Run"] = [
                    f"90-120 minutes at {long_run_pace}",
                    "Include 20-30min at goal HM pace in second half",
                    "Practice race day nutrition"
                ]
    
    # Marathon Plan
    elif running_goal == "Marathon":
        if training_days == 4:
            plan = {
                "Day 1 - Base Run": [
                    f"60-75 minutes at {base_speed}",
                    "Include 6 x 45sec hill repeats at the end"
                ],
                "Day 2 - Speed Work": [
                    "10 min warmup",
                    f"5 x 2km at {interval_pace} with 800m recovery jogs",
                    "10 min cooldown",
                    "Total workout: 80-90 minutes"
                ],
                "Day 3 - Recovery Run": [
                    "40-50 minutes very easy pace",
                    "Focus on form and relaxation"
                ],
                "Day 4 - Long Run": [
                    f"120-150 minutes at {long_run_pace}",
                    "Alternate between easy and goal marathon pace",
                    "Practice race day nutrition and hydration"
                ]
            }
        elif training_days >= 5:
            plan = {
                "Day 1 - Base Run": [
                    f"60-80 minutes at {base_speed}",
                    "Include 6 x 45sec hill sprints at the end"
                ],
                "Day 2 - Interval Work": [
                    "10 min warmup",
                    f"4 x 2.5km at {interval_pace} with 1km recovery jogs",
                    "10 min cooldown",
                    "Total workout: 90-100 minutes"
                ],
                "Day 3 - Recovery Run": [
                    "50 minutes very easy pace",
                    "Optional: Include 4-5 x 30sec pickups"
                ],
                "Day 4 - Tempo Run": [
                    "10 min warmup",
                    f"50-60 minutes at {tempo_pace}",
                    "10 min cooldown",
                    "Total workout: 70-80 minutes"
                ],
                "Day 5 - Fartlek": [
                    "10 min warmup",
                    "5 x 5min at marathon pace with 3min easy jog recovery",
                    "10 min cooldown",
                    "Total workout: 70 minutes"
                ]
            }
            if training_days == 6:
                plan["Day 6 - Long Run"] = [
                    f"150-180 minutes at {long_run_pace}",
                    "Include 30-40min at goal marathon pace in second half",
                    "Full race day simulation (nutrition, gear)"
                ]
    
    return plan

# ------------------- ENHANCED PLAN GENERATOR -------------------
def generate_custom_plan(goal, experience, training_days, gender, split_preference=None, user_name="Champion"):
    plan = {}
    
    # Helper function to determine sets and reps based on goal and experience
    def get_sets_reps(goal, experience, exercise_type="compound"):
        # Science-based set/rep schemes (Wernbom et al., 2007; Schoenfeld et al., 2017)
        if goal == "Strength":
            if exercise_type == "compound":
                return "4x3-5" if experience == "Advanced" else "3x5-6"
            else:
                return "2x8-10"  # Reduced to 2 sets for isolation
        elif goal == "Hypertrophy":
            if exercise_type == "compound":
                return "3x8-10" if experience == "Advanced" else "3x8-12"
            else:
                return "2x10-12"  # Reduced to 2 sets for isolation
        elif goal == "Powerbuilding":
            if exercise_type == "compound":
                return "3x6-8"
            else:
                return "2x10-12"  # Reduced to 2 sets for isolation
        else:  # Calisthenics
            if exercise_type == "bodyweight":
                return "3x8-12" if experience == "Intermediate" else "3x10-15"
            elif exercise_type == "hold":
                return "2x20-30s"  # Reduced to 2 sets for holds
            else:
                return "2x10-15"  # Reduced to 2 sets for isolation
    
    # Helper function to create exercise entry
    def create_exercise_entry(exercise, sets_reps):
        return f"{exercise} – {sets_reps}"
    
    # Calisthenics program
    if goal == "Calisthenics / Street Lifting":
        if experience == "Beginner":
            if training_days < 3:
                plan["note"] = "⚠️ 3 days per week is recommended for beginners. Research (Schoenfeld et al., 2017) shows training each muscle group at least twice per week optimizes hypertrophy and strength gains, and 3 days allows better frequency and recovery."
            if training_days >= 1:
                plan["Day 1 – Full Body"] = [
                    create_exercise_entry("Incline Push-ups", "3x10"),
                    create_exercise_entry("Australian Rows", "3x8"),
                    create_exercise_entry("Bodyweight Squats", "3x20"),
                    create_exercise_entry("Wall Plank Hold", "2x20s"),  # Reduced to 2 sets
                    create_exercise_entry("Hollow Body Hold", "2x20s"),  # Reduced to 2 sets
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
            if training_days >= 2:
                plan["Day 2 – Full Body"] = [
                    create_exercise_entry("Knee Push-ups", "3x10"),
                    create_exercise_entry("Negative Chin-ups", "2x3"),  # Reduced to 2 sets
                    create_exercise_entry("Glute Bridges", "2x15"),  # Reduced to 2 sets
                    create_exercise_entry("Wall Sit", "2x30s"),  # Reduced to 2 sets
                    create_exercise_entry("Dead Hangs", "2x20s"),  # Traps/grip accessory
                    create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                ]
            if training_days == 3:
                plan["Day 3 – Full Body"] = [
                    create_exercise_entry("Push-ups", "3x10"),
                    create_exercise_entry("Inverted Rows", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Step-ups", "2x10/leg"),  # Reduced to 2 sets
                    create_exercise_entry("Superman Hold", "2x30s"),  # Reduced to 2 sets
                    create_exercise_entry("Plank to Side Plank", "2x30s"),  # Reduced to 2 sets
                ]
        else:  # Intermediate
            if training_days == 3:
                if split_preference == "Push/Pull/Legs (PPL)":
                    plan["Day 1 – Push"] = [
                        create_exercise_entry("Dips", "3x8"),
                        create_exercise_entry("Pike Push-ups", "3x8"),
                        create_exercise_entry("Decline Push-ups", "2x10"),  # Reduced to 2 sets
                        create_exercise_entry("Diamond Push-ups", "2x10"),  # Reduced to 2 sets
                        create_exercise_entry("Hanging Knee Raises", "2x10"),  # Reduced to 2 sets
                        create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                    ]
                    plan["Day 2 – Pull"] = [
                        create_exercise_entry("Pull-ups", "3x5"),
                        create_exercise_entry("Chin-ups", "2x6"),  # Reduced to 2 sets
                        create_exercise_entry("Dead Hangs", "2x30s"),  # Reduced to 2 sets
                        create_exercise_entry("Reverse Snow Angels", "2x15"),  # Reduced to 2 sets
                    ]
                    plan["Day 3 – Legs + Core"] = [
                        create_exercise_entry("Bulgarian Split Squats", "3x8/leg"),
                        create_exercise_entry("Jump Squats", "2x12"),  # Reduced to 2 sets
                        create_exercise_entry("Nordic Curl Negatives", "2x5"),  # Reduced to 2 sets
                        create_exercise_entry("Hanging Leg Raises", "2x8"),  # Reduced to 2 sets
                        create_exercise_entry("L-sit (tuck)", "2x10s"),  # Reduced to 2 sets
                        create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                    ]
                else:  # Upper/Lower
                    plan["Day 1 – Upper"] = [
                        create_exercise_entry("Dips", "3x8"),
                        create_exercise_entry("Pull-ups", "3x5"),
                        create_exercise_entry("Pike Push-ups", "2x8"),  # Reduced to 2 sets
                        create_exercise_entry("Chin-ups", "2x6"),  # Reduced to 2 sets
                        create_exercise_entry("Dead Hangs", "2x30s"),  # Traps/grip accessory
                        create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                    ]
                    plan["Day 2 – Lower"] = [
                        create_exercise_entry("Bulgarian Split Squats", "3x8/leg"),
                        create_exercise_entry("Bodyweight Squats", "3x15"),
                        create_exercise_entry("Jump Squats", "2x12"),  # Reduced to 2 sets
                        create_exercise_entry("Wall Sit", "2x30s"),  # Reduced to 2 sets
                        create_exercise_entry("Calf Raises", "2x20"),  # Reduced to 2 sets
                        create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                    ]
                    plan["Day 3 – Upper + Core"] = [
                        create_exercise_entry("Push-ups", "3x10"),
                        create_exercise_entry("Inverted Rows", "2x10"),  # Reduced to 2 sets
                        create_exercise_entry("Hanging Knee Raises", "2x10"),  # Reduced to 2 sets
                        create_exercise_entry("Plank", "2x30s"),  # Reduced to 2 sets
                        create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                    ]
            elif training_days == 4:
                plan["Day 1 – Push (Chest/Shoulders/Triceps)"] = [
                    create_exercise_entry("Dips", "3x10"),
                    create_exercise_entry("Elevated Pike Push-ups", "2x8"),  # Reduced to 2 sets
                    create_exercise_entry("Diamond Push-ups", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Triceps Extensions (on bar)", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
                plan["Day 2 – Legs"] = [
                    create_exercise_entry("Pistol Squats (assisted)", "3x6/leg"),
                    create_exercise_entry("Bulgarian Split Squats", "3x8"),
                    create_exercise_entry("Calf Raises", "2x20"),  # Reduced to 2 sets
                    create_exercise_entry("Lateral Lunges", "2x10/leg"),  # Reduced to 2 sets
                    create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                ]
                plan["Day 3 – Pull (Back/Biceps)"] = [
                    create_exercise_entry("Pull-ups", "3x6"),
                    create_exercise_entry("Chin-ups", "2x8"),  # Reduced to 2 sets
                    create_exercise_entry("Inverted Rows", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Archer Pull-ups", "2x3/side"),  # Reduced to 2 sets
                    create_exercise_entry("Dead Hangs", "2x30s")  # Traps/grip accessory
                ]
                plan["Day 4 – Core + Skills"] = [
                    create_exercise_entry("Hanging Knee-to-Elbows", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("L-sit (tuck or advanced)", "2x10-20s"),  # Reduced to 2 sets
                    create_exercise_entry("Plank Walkouts", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Handstand Wall Hold", "2x20-30s"),  # Reduced to 2 sets
                    create_exercise_entry("Hollow Rocks", "2x10"),  # Reduced to 2 sets
                ]
            elif training_days == 5:
                plan["Day 1 – Push"] = [
                    create_exercise_entry("Dips", "3x10"),
                    create_exercise_entry("Pseudo Planche Push-ups", "3x8"),
                    create_exercise_entry("Decline Push-ups", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Pike Push-ups", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
                plan["Day 2 – Pull"] = [
                    create_exercise_entry("Pull-ups", "3x6"),
                    create_exercise_entry("Chin-ups", "3x8"),
                    create_exercise_entry("Front Lever Tuck Hold", "2x10s"),  # Reduced to 2 sets
                    create_exercise_entry("Dead Hangs", "2x30s")  # Traps/grip accessory
                ]
                plan["Day 3 – Legs"] = [
                    create_exercise_entry("Pistol Squats", "3x6/leg"),
                    create_exercise_entry("Jump Lunges", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Wall Sit", "2x1 min"),  # Reduced to 2 sets
                    create_exercise_entry("Calf Raises", "2x20"),  # Reduced to 2 sets
                    create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                ]
                plan["Day 4 – Core + Skills"] = [
                    create_exercise_entry("L-sit Progressions", "2x15s"),  # Reduced to 2 sets
                    create_exercise_entry("Hanging Windshield Wipers", "2x8"),  # Reduced to 2 sets
                    create_exercise_entry("Planche Leans", "2x20s"),  # Reduced to 2 sets
                    create_exercise_entry("Hollow Hold", "2x30s"),  # Reduced to 2 sets
                ]
                plan["Day 5 – Full Body Strength"] = [
                    create_exercise_entry("Circuit (3 Rounds): 10 Pull-ups, 15 Push-ups, 20 Squats, 10 Dips, 10 Hanging Leg Raises", "3 rounds"),
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
            elif training_days == 6:
                plan["Day 1 – Push"] = [
                    create_exercise_entry("Dips", "3x10"),
                    create_exercise_entry("Decline Push-ups", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Pike Push-ups", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Wall Handstand Hold", "2x30s"),  # Reduced to 2 sets
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
                plan["Day 2 – Pull"] = [
                    create_exercise_entry("Pull-ups", "3x6"),
                    create_exercise_entry("Inverted Rows", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Chin-ups", "2x8"),  # Reduced to 2 sets
                    create_exercise_entry("Dead Hang", "2x30s"),  # Reduced to 2 set
                                                    ]
                plan["Day 3 – Legs"] = [
                    create_exercise_entry("Pistol Squats", "3x6"),
                    create_exercise_entry("Nordic Curl Negatives", "2x5"),  # Reduced to 2 sets
                    create_exercise_entry("Wall Sit", "2x1 min"),  # Reduced to 2 sets
                    create_exercise_entry("Calf Raises", "2x20"),  # Reduced to 2 sets
                    create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                ]
                plan["Day 4 – Push"] = [
                    create_exercise_entry("Pseudo Planche Push-ups", "3x8"),
                    create_exercise_entry("Elevated Pike Push-ups", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Dips", "2x8"),  # Reduced to 2 sets
                    create_exercise_entry("Diamond Push-ups", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
                plan["Day 5 – Pull"] = [
                    create_exercise_entry("Chin-ups", "3x8"),
                    create_exercise_entry("Archer Pull-ups", "2x3/side"),  # Reduced to 2 sets
                    create_exercise_entry("Australian Rows", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Tuck Front Lever Holds", "2x10s"),  # Reduced to 2 sets
                    create_exercise_entry("Dead Hangs", "2x30s")  # Traps/grip accessory
                ]
                plan["Day 6 – Legs"] = [
                    create_exercise_entry("Jump Squats", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Bulgarian Split Squats", "3x10"),
                    create_exercise_entry("Calf Raises", "2x25"),  # Reduced to 2 sets
                    create_exercise_entry("Side Lunges", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                ]
            elif training_days == 7:
                plan["Day 1 – Weighted Push"] = [
                    create_exercise_entry("Weighted Dips", "3x6"),
                    create_exercise_entry("Wall HSPU", "2x6"),  # Reduced to 2 sets
                    create_exercise_entry("Pseudo Planche Push-ups", "2x8"),  # Reduced to 2 sets
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
                plan["Day 2 – Weighted Pull"] = [
                    create_exercise_entry("Weighted Pull-ups", "3x6"),
                    create_exercise_entry("Chin-ups", "2x10"),  # Reduced to 2 sets
                    create_exercise_entry("Front Lever Rows", "2x5"),  # Reduced to 2 sets
                    create_exercise_entry("Dead Hangs", "2x30s")  # Traps/grip accessory
                ]
                plan["Day 3 – Legs"] = [
                    create_exercise_entry("Pistol Squats", "3x6"),
                    create_exercise_entry("Nordic Curls", "2x5"),  # Reduced to 2 sets
                    create_exercise_entry("Wall Sit", "2x60s"),  # Reduced to 2 sets
                    create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                ]
                plan["Day 4 – Core + Planche"] = [
                    create_exercise_entry("Planche Leans", "2x30s"),  # Reduced to 2 sets
                    create_exercise_entry("L-sit to Tuck Planche", "2x5"),  # Reduced to 2 sets
                    create_exercise_entry("Hanging Knee-to-Elbows", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("V-ups", "2x20"),  # Reduced to 2 sets
                ]
                plan["Day 5 – Front Lever & Pull"] = [
                    create_exercise_entry("Tuck Front Lever Hold", "2x10-15s"),  # Reduced to 2 sets
                    create_exercise_entry("Archer Pull-ups", "2x4"),  # Reduced to 2 sets
                    create_exercise_entry("Hanging Leg Raises", "2x12"),  # Reduced to 2 sets
                    create_exercise_entry("Dead Hangs", "2x30s")  # Traps/grip accessory
                ]
                plan["Day 6 – Explosive Work"] = [
                    create_exercise_entry("Clap Push-ups", "2x8"),  # Reduced to 2 sets
                    create_exercise_entry("Jump Squats", "2x15"),  # Reduced to 2 sets
                    create_exercise_entry("Muscle-up Progression (Negatives or Banded)", "2x3"),  # Reduced to 2 sets
                    create_exercise_entry("Burpees", "2x15"),  # Reduced to 2 sets
                    create_exercise_entry("Jumping Jacks", "2x20")  # Cardio accessory
                ]
                plan["Day 7 – Freestyle + Active Recovery"] = [
                    create_exercise_entry("Flow session (bar combos, handstand balance, etc.)", "15-20 min"),
                    create_exercise_entry("Stretching & mobility drills", "15-20 min"),
                    create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Cardio accessory
                ]
        return plan
    
    # For beginners, use full body workouts (1-3 days)
    if experience == "Beginner":
        if training_days >= 1:
            if goal == "Hypertrophy":
                if gender == "Male":
                    plan["Day 1 – Full Body "] = [
                        create_exercise_entry("Squat", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Lat Pulldown", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Dumbbell Shoulder Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Cable Triceps Pushdown", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Dumbbell Curl", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Wrist Curls", "2x15")  # Accessory for forearms
                    ]
                else:  # Female
                    plan["Day 1 – Full Body "] = [
                        create_exercise_entry("Hip Thrust", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Goblet Squat", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Dumbbell Shoulder Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Seated Leg Curl", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Cable Glute Kickback", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Standing Calf Raises", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Wrist Curls", "2x15")  # Accessory for forearms
                    ]
            else:  # Strength or Powerbuilding
                if gender == "Male":
                    plan["Day 1 – Full Body "] = [
                        create_exercise_entry("Squat", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Cable Triceps Pushdown", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
                    ]
                else:  # Female
                    plan["Day 1 – Full Body "] = [
                        create_exercise_entry("Barbell Hip Thrust", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Dumbbell Bench Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Dumbbell Row", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Walking Lunges", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Cable Kickback", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
                    ]
        if training_days >= 2:
            if goal == "Hypertrophy":
                if gender == "Male":
                    plan["Day 2 – Full Body "] = [
                        create_exercise_entry("Romanian Deadlift", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Leg Extensions", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Hammer Curl", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
                    ]
                else:  # Female
                    plan["Day 2 – Full Body "] = [
                        create_exercise_entry("Bulgarian Split Squat", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Cable Pull-through", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Lat Pulldown", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Dumbbell Bench Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Lateral Raise", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
                    ]
            else:  # Strength or Powerbuilding
                if gender == "Male":
                    plan["Day 2 – Full Body "] = [
                        create_exercise_entry("Deadlift", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Chest Fly", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
                    ]
                else:  # Female
                    plan["Day 2 – Full Body "] = [
                        create_exercise_entry("Trap Bar Deadlift", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Lat Pulldown", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Curtsy Lunge", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Cable Side Raises", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Accessory for balance
                    ]
        if training_days == 3:
            if goal == "Hypertrophy":
                if gender == "Male":
                    plan["Day 3 – Full Body "] = [
                        create_exercise_entry("Leg Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Chest Fly (Machine or Cable)", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Pull-ups (Assisted)", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Arnold Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Leg Curl", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Rope Face Pull", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Shrugs", "2x15")  # Accessory for traps
                    ]
                else:  # Female
                    plan["Day 3 – Full Body "] = [
                        create_exercise_entry("Goblet Squat", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Glute Bridge", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Hanging Leg Raise", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
                    ]
            else:  # Strength or Powerbuilding
                if gender == "Male":
                    plan["Day 3 – Full Body "] = [
                        create_exercise_entry("Front Squat", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Incline DB Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Row Machine", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Skullcrushers", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Cable Rear Delt Pulls", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
                    ]
                else:  # Female
                    plan["Day 3 – Full Body "] = [
                        create_exercise_entry("Goblet Squat", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Glute Bridge", get_sets_reps(goal, experience, "compound")),
                        create_exercise_entry("Hanging Leg Raise", "2x10-12"),  # Reduced to 2 sets
                        create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
                    ]
        return plan
    
    # For intermediate and advanced users, use selected split (PPL or Upper/Lower)
    use_ppl = split_preference == "Push/Pull/Legs (PPL)"
    use_upper_lower = split_preference == "Upper/Lower"
    
    if training_days == 3:
        if use_ppl:
            plan["Day 1 – Push"] = [
                create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Weighted Dips", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
            plan["Day 2 – Pull"] = [
                create_exercise_entry("Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("T Bar Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Lat Pulldown", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Straight Bar Cable Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 3 – Legs"] = [
                create_exercise_entry("Squats", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Romanian Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Leg Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
            ]
        else:  # Upper/Lower
            plan["Day 1 – Upper"] = [
                create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Pull-ups (Assisted)", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 2 – Lower"] = [
                create_exercise_entry("Back Squat", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Deadlift", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Accessory for balance
            ]
            plan["Day 3 – Upper"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Dumbbell Shoulder Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Lat Pulldown", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Chest Fly (Machine or Cable)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
    
    elif training_days == 4:
        if use_upper_lower:
            plan["Day 1 – Upper"] = [
                create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Pull-ups (Assisted)", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 2 – Lower"] = [
                create_exercise_entry("Back Squat", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Deadlift", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Front Squat", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Accessory for balance
            ]
            plan["Day 3 – Upper"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Dumbbell Shoulder Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Lat Pulldown", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Chest Fly (Machine or Cable)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
            plan["Day 4 – Lower"] = [
                create_exercise_entry("Leg Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Romanian Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Bulgarian Split Squat", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Leg Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Cable Glute Kickback", "3x15" if gender == "Female" else "2x12")
            ]
        else:
            # Default to PPL for 4 days
            plan["Day 1 – Push"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Incline Machine Chest Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Pec Deck (or Cable Fly)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Push-ups", "1 set to failure"),
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Overhead Triceps Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 2 – Pull"] = [
                create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Lat Pulldown", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Cable Pullovers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Straight Bar Cable Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Dumbbell Hammer Curls", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 3 – Legs"] = [
                create_exercise_entry("Squats", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Leg Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Walking Lunges", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Quad Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
            ]
            plan["Day 4 – Accessory & Cardio"] = [
                create_exercise_entry("Shrugs", "2x12"),  # Traps
                create_exercise_entry("Wrist Curls", "2x12"),  # Forearms
                create_exercise_entry("Rope Face Pull", "2x15"),  # Rear delts
                create_exercise_entry("Barbell Curl", "2x12"),  # Arms
                create_exercise_entry("Skullcrushers", "2x12"),  # Arms
                create_exercise_entry("Light Cardio (e.g., Walking)", "30 min")  # Cardio
            ]
    
    elif training_days == 5:
        if use_upper_lower:
            plan["Day 1 – Upper"] = [
                create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Pull-ups", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 2 – Lower"] = [
                create_exercise_entry("Back Squat", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Deadlift", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Accessory for balance
            ]
            plan["Day 3 – Upper"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Dumbbell Shoulder Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Lat Pulldown", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Chest Fly (Machine or Cable)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
            plan["Day 4 – Lower"] = [
                create_exercise_entry("Leg Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Romanian Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Bulgarian Split Squat", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Leg Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Cable Glute Kickback", "3x15" if gender == "Female" else "2x12")
            ]
            plan["Day 5 – Arms & Cardio"] = [
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Skullcrushers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hammer Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Rope Face Pull", "2x15"),  # Rear delts
                create_exercise_entry("Light Cardio (e.g., Cycling)", "30 min")  # Cardio
            ]
        else:
            # Default to PPL
            plan["Day 1 – Push (Heavy)"] = [
                create_exercise_entry("Bench Press", "4x5" if goal == "Strength" else "3x6-8"),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Incline Bench Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Weighted Dips", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
            plan["Day 2 – Pull (Heavy)"] = [
                create_exercise_entry("Deadlifts", "4x5" if goal == "Strength" else "3x6-8"),
                create_exercise_entry("Pull-ups", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Barbell Rows", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("T Bar Row", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Barbell Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 3 – Legs (Heavy)"] = [
                create_exercise_entry("Squats", "4x5" if goal == "Strength" else "3x6-8"),
                create_exercise_entry("Romanian Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Leg Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
            ]
            plan["Day 4 – Push"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Incline Machine Chest Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Pec Deck (or Cable Fly)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Push-ups", "1 set to failure"),
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Overhead Triceps Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 5 – Pull"] = [
                create_exercise_entry("Lat Pulldown", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Cable Pullovers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Straight Bar Cable Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Dumbbell Hammer Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
    
    elif training_days == 6:
        if use_upper_lower:
            plan["Day 1 – Upper"] = [
                create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Pull-ups", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 2 – Lower"] = [
                create_exercise_entry("Back Squat", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Deadlift", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Accessory for balance
            ]
            plan["Day 3 – Upper"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Dumbbell Shoulder Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Lat Pulldown", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Chest Fly (Machine or Cable)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
            plan["Day 4 – Lower"] = [
                create_exercise_entry("Leg Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Romanian Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Bulgarian Split Squat", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Leg Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Cable Glute Kickback", "3x15" if gender == "Female" else "2x12")
            ]
            plan["Day 5 – Upper"] = [
                create_exercise_entry("Weighted Dips", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("T Bar Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Cable Pullovers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Incline Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Overhead Triceps Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 6 – Arms & Cardio"] = [
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Skullcrushers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hammer Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Rope Face Pull", "2x15"),  # Rear delts
                create_exercise_entry("Light Cardio (e.g., Cycling)", "30 min")  # Cardio
            ]
        else:
            # Default to PPL
            plan["Day 1 – Push"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Incline Machine Chest Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Pec Deck (or Cable Fly)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Push-ups", "1 set to failure"),
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Overhead Triceps Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 2 – Pull"] = [
                create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Lat Pulldown", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Cable Pullovers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Straight Bar Cable Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Dumbbell Hammer Curls", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 3 – Legs"] = [
                create_exercise_entry("Squats", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Leg Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Walking Lunges", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Quad Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
            ]
            plan["Day 4 – Push"] = [
                create_exercise_entry("Weighted Dips", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Dumbbell Shoulder Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Machine Chest Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Pec Deck", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Overhead Triceps Extensions", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 5 – Pull "] = [
                create_exercise_entry("Weighted Pull-ups", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("T Bar Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Lat Pulldown", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Cable Pullovers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Incline Curls (or Rope Curls)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("EZ Bar Curls", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 6 – Legs"] = [
                create_exercise_entry("Stiff Leg Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hack Squats", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Quad Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
    
    elif training_days == 7:
        if use_upper_lower:
            plan["Day 1 – Upper"] = [
                create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Barbell Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Pull-ups", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 2 – Lower"] = [
                create_exercise_entry("Back Squat", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Deadlift", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Walking)", "20 min")  # Accessory for balance
            ]
            plan["Day 3 – Upper"] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Seated Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Dumbbell Shoulder Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Lat Pulldown", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Chest Fly (Machine or Cable)", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
            plan["Day 4 – Lower"] = [
                create_exercise_entry("Leg Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Romanian Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Bulgarian Split Squat", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Leg Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Cable Glute Kickback", "3x15" if gender == "Female" else "2x12")
            ]
            plan["Day 5 – Upper"] = [
                create_exercise_entry("Weighted Dips", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("T Bar Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Cable Pullovers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Incline Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Overhead Triceps Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 6 – Lower"] = [
                create_exercise_entry("Front Squat", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hack Squats", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Leg Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10")
            ]
            plan["Day 7 – Arms & Cardio"] = [
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Skullcrushers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hammer Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),
                create_exercise_entry("Rope Face Pull", "2x15"),  # Rear delts
                create_exercise_entry("Light Cardio (e.g., Cycling)", "30 min")  # Cardio
            ]
        else:
            # Default to PPL with additional focus for 7 days
            plan["Day 1 – Push "] = [
                create_exercise_entry("Bench Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Overhead Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Incline Dumbbell Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Weighted Dips", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Wrist Curls", "2x12")  # Accessory for forearms
            ]
            plan["Day 2 – Pull"] = [
                create_exercise_entry("Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Pull-ups", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Barbell Rows", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("T Bar Row", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Barbell Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Shrugs", "2x12")  # Accessory for traps
            ]
            plan["Day 3 – Legs"] = [
                create_exercise_entry("Squats", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Leg Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Walking Lunges", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
            ]
            plan["Day 4 – Push "] = [
                create_exercise_entry("Incline Dumbbell Press", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Dumbbell Shoulder Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Cable Lateral Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Machine Chest Press", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Pec Deck", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Overhead Triceps Extensions", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 5 – Pull "] = [
                create_exercise_entry("Weighted Pull-ups", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("T Bar Row", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Lat Pulldown", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Cable Pullovers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Face Pulls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Incline Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("EZ Bar Curls", "2x10-12")  # Reduced to 2 sets
            ]
            plan["Day 6 – Legs "] = [
                create_exercise_entry("Stiff Leg Deadlifts", get_sets_reps(goal, experience, "compound")),
                create_exercise_entry("Hack Squats", "2x8-10"),  # Reduced to 2 sets
                create_exercise_entry("Hamstring Curls", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Quad Extensions", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hip Thrusts", "3x12" if gender == "Female" else "2x10"),
                create_exercise_entry("Calf Raises", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Light Cardio (e.g., Cycling)", "20 min")  # Accessory for balance
            ]
            plan["Day 7 – Arms & Cardio"] = [
                create_exercise_entry("Barbell Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Skullcrushers", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Hammer Curl", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Triceps Pushdowns", "2x10-12"),  # Reduced to 2 sets
                create_exercise_entry("Rope Face Pull", "2x15"),  # Rear delts
                create_exercise_entry("Light Cardio (e.g., Cycling)", "30 min")  # Cardio
            ]

    return plan
# ---------------------- PLAN EXECUTION ----------------------
if st.button("Generate My Plan"):
    with st.spinner("Building your perfect workout plan..."):
        if goal == "Running":
            plan = generate_running_plan(running_goal, running_level, training_days, current_distance, user_name)
        else:
            plan = generate_custom_plan(goal, experience, training_days, gender, split_preference, user_name)
        
        st.markdown('<div class="plan-header">Your Custom Training Plan</div>', unsafe_allow_html=True)
        
        if goal == "Running":
            split_type = running_goal
            st.markdown(f'<div class="plan-info"><strong>{running_level} Runner • {gender} • {training_days} Days/Week • {split_type}</strong></div>', unsafe_allow_html=True)
        else:
            split_type = split_preference if split_preference else ("Full Body" if experience == "Beginner" else "Custom Split")
            st.markdown(f'<div class="plan-info"><strong>{experience} Level • {gender} • {training_days} Days/Week • {split_type}</strong></div>', unsafe_allow_html=True)

        for day, exercises in plan.items():
            with st.expander(day, expanded=True):
                for ex in exercises:
                    st.markdown(f'<div class="exercise-item">• {ex}</div>', unsafe_allow_html=True)   
        
        # --- PDF Export ---
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        width, height = letter

        # --- Add Logo ---
        logo_path = "logo.png" 
        try:
            # Draw the image (x, y, width, height)
            # (50, height - 100) positions the image at the top-left
            c.drawImage(logo_path, 50, height - 100, width=80, preserveAspectRatio=True, mask='auto')
        except:
            # If the logo file is not found, it will just skip it.
            pass

        # --- Add Text ---
        # Adjust the starting position of the text to be below the logo
        c.setFont("Helvetica-Bold", 16)
        c.drawString(150, height - 60, f"Custom Training Plan for {user_name}")
        c.setFont("Helvetica", 12)
        
        if goal == "Running":
            c.drawString(150, height - 80, f"Goal: {running_goal} | Level: {running_level} | Gender: {gender} | Days: {training_days}")
        else:
            c.drawString(150, height - 80, f"Goal: {goal} | Level: {experience} | Gender: {gender} | Days: {training_days}")

        y = height - 150 # Adjusted initial y-position for the plan details
        for day, exercises in plan.items():
            if y < 100: # Check if there is enough space for the day's title
                c.showPage()
                y = height - 50
            c.setFont("Helvetica-Bold", 14)
            c.drawString(50, y, day)
            y -= 20

            c.setFont("Helvetica", 12)
            for ex in exercises:
                if y < 50:
                    c.showPage()
                    y = height - 50
                c.drawString(70, y, f"- {ex}")
                y -= 18
            y -= 10

        c.save()
        pdf_buffer.seek(0)

        st.download_button(
            label="Download Plan as PDF",
            data=pdf_buffer,
            file_name=f"{user_name}_training_plan.pdf",
            mime="application/pdf"
        )
                  

        # Motivational message with user's name
        st.markdown(f'<div class="motivational-message">You got this, <span class="name-highlight">{user_name}</span>! Time to crush your goals!</div>', unsafe_allow_html=True)
        
        st.divider()
        st.markdown('<div class="section-title">Training Guidelines</div>', unsafe_allow_html=True)
        
        # Goal-specific notes
        if goal == "Running":
            st.markdown("""
            <div class='notes'>
            <h4>Running Training Focus:</h4>
            • Always warm up for 5-10 minutes before speed work<br>
            • Cool down with easy jogging and stretching<br>
            • Increase weekly mileage by no more than 10%<br>
            • Include strength training 2x/week for injury prevention<br>
            • Listen to your body and adjust pace as needed<br>
            • Stay hydrated and fuel properly for long runs<br>
            • Invest in proper running shoes and replace every 500-800 km<br>
            • Track your progress with a running log or app
            </div>
            """, unsafe_allow_html=True)
            
            if running_goal in ["5K Race", "10K Race"]:
                st.markdown("""
                <div class='notes'>
                <h4>Race Preparation Tips:</h4>
                • Practice your race pace in some workouts<br>
                • Do a dress rehearsal with your race day gear<br>
                • Taper your training in the final week before race day<br>
                • Study the race course and elevation profile<br>
                • Plan your pre-race nutrition and hydration strategy
                </div>
                """, unsafe_allow_html=True)
            elif running_goal in ["Half Marathon", "Marathon"]:
                st.markdown("""
                <div class='notes'>
                <h4>Long Distance Tips:</h4>
                • Gradually increase your long run distance<br>
                • Practice your fueling strategy during long runs<br>
                • Include race-pace segments in some long runs<br>
                • Build mental toughness with visualization<br>
                • Schedule recovery weeks every 3-4 weeks
                </div>
                """, unsafe_allow_html=True)
        elif goal == "Strength":
            st.markdown("""
            <div class='notes'>
            <h4>Strength Training Focus:</h4>
            • Rest 3-5 minutes between compound sets<br>
            • Focus on progressive overload with weight<br>
            • Maintain strict form on heavy lifts<br>
            • Track your 1RM progress monthly
            </div>
            """, unsafe_allow_html=True)
        elif goal == "Hypertrophy":
            st.markdown("""
            <div class='notes'>
            <h4>Hypertrophy Training Focus:</h4>
            • Rest 2-3 minutes between sets<br>
            • Focus on mind-muscle connection<br>
            • Progressive overload through reps, weight, or volume<br>
            • Take sets close to muscle failure
            </div>
            """, unsafe_allow_html=True)
        elif goal == "Powerbuilding":
            st.markdown("""
            <div class='notes'>
            <h4>Powerbuilding Focus:</h4>
            • Heavy compounds first, accessories after<br>
            • Rest 3-4 minutes for compounds, 2-3 for accessories<br>
            • Balance strength and size gains<br>
            • Track both strength and physique progress
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class='notes'>
            <h4>Calisthenics Focus:</h4>
            • Progress through exercise variations<br>
            • Focus on perfect form and control<br>
            • Work towards advanced movements<br>
            • Include skill practice sessions
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class='notes'>
        <h4>General Guidelines:</h4>
        • Warm up thoroughly before each session<br>
        • Progress weight/reps gradually each week<br>
        • Listen to your body and adjust as needed<br>
        • Get adequate sleep and nutrition for recovery<br>
        • Deload every 4-6 weeks for optimal progress
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    Built by KHOUTRI Imad — Train smart. Stay consistent.<br>
    <em>Remember: Consistency beats perfection every time!</em>
</div>
""", unsafe_allow_html=True)