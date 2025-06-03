import streamlit as st
import pandas as pd
import uuid
import base64
import io
import streamlit.components.v1 as components
import os
from datetime import datetime

# Define the quiz questions
quiz_data = [
    {
        "question": "What is the output of the following code?\n```python\nnumbers = [1, 2, 3, 4, 5]\nresult = sum([x * 2 for x in numbers])\nprint(result)\n```",
        "options": ["15", "20", "30", "25"],
        "correct": "30",
        "explanation": "The list comprehension [x * 2 for x in numbers] doubles each element in numbers ([1, 2, 3, 4, 5] → [2, 4, 6, 8, 10]). The sum() function adds these values: 2 + 4 + 6 + 8 + 10 = 30."
    },
    {
        "question": "What is the result of the following expression?\n```python\ntext = \"Python\"\nprint(text[1:4])\n```",
        "options": ["Pyt", "yth", "tho", "ytho"],
        "correct": "yth",
        "explanation": "String slicing text[1:4] extracts characters from index 1 to 3 (4 is excluded). For \"Python\", indices are: P(0), y(1), t(2), h(3), o(4), n(5). Thus, text[1:4] gives \"yth\"."
    },
    {
        "question": "What is the value of total after executing this code?\n```python\ntotal = 0\nfor i in range(1, 5):\n    total += i ** 2\nprint(total)\n```",
        "options": ["10", "14", "30", "20"],
        "correct": "30",
        "explanation": "The loop iterates over range(1, 5) (1, 2, 3, 4). For each i, i ** 2 is added to total: 1² + 2² + 3² + 4² = 1 + 4 + 9 + 16 = 30."
    },
    {
        "question": "Which of the following operations can be performed on a tuple?",
        "options": ["Appending a new element", "Modifying an existing element", "Accessing an element by index", "Deleting the entire tuple and reassigning"],
        "correct": "Accessing an element by index",
        "explanation": "Tuples are immutable, so appending (A) or modifying elements (B) is not allowed. Accessing elements by index (C) is possible. Deleting a tuple and reassigning (D) is not a single operation on the tuple itself."
    },
    {
        "question": "What does the following function return when called with calculate(5)?\n```python\ndef calculate(n):\n    return n + n * 2\n```",
        "options": ["10", "15", "7", "25"],
        "correct": "15",
        "explanation": "For n = 5, the function computes n + n * 2 = 5 + (5 * 2) = 5 + 10 = 15."
    },
    {
        "question": "What is the output of the following code?\n```python\nset1 = {1, 2, 3}\nset2 = {2, 3, 4}\nprint(set1.union(set2))\n```",
        "options": ["{1, 2, 3}", "{2, 3}", "{1, 2, 3, 4}", "{1, 4}"],
        "correct": "{1, 2, 3, 4}",
        "explanation": "The union() method combines all unique elements from set1 and set2: {1, 2, 3} ∪ {2, 3, 4} = {1, 2, 3, 4}."
    },
    {
        "question": "What is the value of count after this code executes?\n```python\ncount = 0\ni = 1\nwhile i <= 3:\n    count += i * 3\n    i += 1\nprint(count)\n```",
        "options": ["9", "12", "18", "6"],
        "correct": "18",
        "explanation": "The loop runs for i = 1, 2, 3. Each iteration adds i * 3 to count: (1 * 3) + (2 * 3) + (3 * 3) = 3 + 6 + 9 = 18."
    },
    {
        "question": "What is the output of the following code?\n```python\ndata = {\"a\": 1, \"b\": 2, \"c\": 3}\nprint(data.get(\"b\", 0))\n```",
        "options": ["0", "1", "2", "3"],
        "correct": "2",
        "explanation": "The get() method returns the value for key \"b\", which is 2. The default value 0 is returned only if the key is not found."
    },
    {
        "question": "What is the output of this code?\n```python\nx = 10\nif x > 5:\n    x = x - 3\nelse:\n    x = x + 3\nprint(x)\n```",
        "options": ["13", "7", "10", "5"],
        "correct": "7",
        "explanation": "Since x = 10 and 10 > 5, the if block executes: x = x - 3 = 10 - 3 = 7."
    },
    {
        "question": "What is the result of the expression True and not False?",
        "options": ["True", "False", "None", "0"],
        "correct": "True",
        "explanation": "not False evaluates to True. Then, True and True results in True."
    },
    {
        "question": "What is the result of the following expression?\n```python\nresult = 5.0 / 2 + 1.5\nprint(result)\n```",
        "options": ["3.5", "4.0", "2.5", "3.0"],
        "correct": "4.0",
        "explanation": "Division 5.0 / 2 yields 2.5 (float). Adding 1.5 gives 2.5 + 1.5 = 4.0."
    },
    {
        "question": "Which of the following creates a list with elements [1, 4, 9]?",
        "options": ["[x**2 for x in range(1, 4)]", "[x**2 for x in range(4)]", "[x**2 for x in range(1, 3)]", "[x*2 for x in range(1, 4)]"],
        "correct": "[x**2 for x in range(1, 4)]",
        "explanation": "range(1, 4) gives [1, 2, 3]. Squaring each element (x**2) produces [1, 4, 9]."
    },
    {
        "question": "What is the output of the following code?\n```python\ndef multiply(x, y=2):\n    return x * y\nprint(multiply(3))\n```",
        "options": ["3", "6", "9", "5"],
        "correct": "6",
        "explanation": "The function uses the default value y=2 when only x=3 is provided. Thus, 3 * 2 = 6."
    },
    {
        "question": "What is the result of the following code?\n```python\nset1 = {1, 2, 3, 4}\nset2 = {3, 4, 5}\nprint(set1.intersection(set2))\n```",
        "options": ["{1, 2, 3, 4, 5}", "{3, 4}", "{1, 2}", "{5}"],
        "correct": "{3, 4}",
        "explanation": "The intersection() method returns elements common to both sets: {3, 4}."
    },
    {
        "question": "What is the value of sum_squares after this code executes?\n```python\nsum_squares = 0\nfor i in range(2, 5):\n    sum_squares += i ** 3\nprint(sum_squares)\n```",
        "options": ["27", "98", "64", "36"],
        "correct": "98",
        "explanation": "The loop iterates over range(2, 5) (2, 3, 4). Compute i ** 3: 2³ + 3³ + 4³ = 8 + 27 + 64 = 98."
    },
    {
        "question": "What is the output of this code?\n```python\nx = 0\nif x > 0:\n    print(\"Positive\")\nelif x == 0:\n    print(\"Zero\")\nelse:\n    print(\"Negative\")\n```",
        "options": ["Positive", "Zero", "Negative", "None"],
        "correct": "Zero",
        "explanation": "Since x = 0, the elif x == 0 condition is true, printing \"Zero\"."
    },
    {
        "question": "What is the output of the following code?\n```python\nscores = {\"Alice\": 10, \"Bob\": 20}\ntotal = sum(scores.values())\nprint(total)\n```",
        "options": ["10", "20", "30", "40"],
        "correct": "30",
        "explanation": "scores.values() returns [10, 20]. The sum() function adds them: 10 + 20 = 30."
    },
    {
        "question": "How many times will the following loop execute?\n```python\nx = 10\nwhile x > 5:\n    x -= 2\n```",
        "options": ["2", "3", "4", "5"],
        "correct": "3",
        "explanation": "Start with x = 10. The loop runs while x > 5: 1st: x = 10 → 8, 2nd: x = 8 → 6, 3rd: x = 6 → 4 (stops, as 4 ≤ 5). The loop executes 3 times."
    },
    {
        "question": "What is the result of the following expression?\n```python\na = 5\nb = \"2\"\nprint(a + int(b))\n```",
        "options": ["7", "52", "10", "Error"],
        "correct": "7",
        "explanation": "int(b) converts the string \"2\" to the integer 2. Then, a + int(b) computes 5 + 2 = 7."
    },
    {
        "question": "What is the output of the following code?\n```python\nt = (1, 2, 3, 4)\nprint(t[2:])\n```",
        "options": ["(1, 2)", "(3, 4)", "(2, 3, 4)", "(1, 2, 3)"],
        "correct": "(3, 4)",
        "explanation": "Slicing t[2:] starts from index 2 to the end. For t = (1, 2, 3, 4), index 2 is 3, so t[2:] gives (3, 4)."
    }
]

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_role' not in st.session_state:
    st.session_state.user_role = "student"
if 'current_index' not in st.session_state:
    st.session_state.current_index = 0
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'responses' not in st.session_state:
    st.session_state.responses = [None] * len(quiz_data)
if 'user_details' not in st.session_state:
    st.session_state.user_details = {}
if 'timer_started' not in st.session_state:
    st.session_state.timer_started = False
if 'time_up' not in st.session_state:
    st.session_state.time_up = False
if 'start_time' not in st.session_state:
    st.session_state.start_time = None

# Function to reset quiz
def reset_quiz():
    st.session_state.current_index = 0
    st.session_state.score = 0
    st.session_state.responses = [None] * len(quiz_data)
    st.session_state.user_details = {}
    st.session_state.timer_started = False
    st.session_state.time_up = False
    st.session_state.start_time = None

# Function to create CSV download link
def create_download_link(df, filename):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()
    return f'<a href="data:file/csv;base64,{b64}" download="{filename}">Download {filename}</a>'

# Function to save cumulative results
def save_cumulative_results(student_data):
    results_file = "all_quiz_results.csv"
    new_row = pd.DataFrame([student_data])
    if os.path.exists(results_file):
        existing_df = pd.read_csv(results_file)
        if student_data["Index Number"] in existing_df["Index Number"].values:
            existing_df = existing_df[existing_df["Index Number"] != student_data["Index Number"]]
        existing_df = pd.concat([existing_df, new_row], ignore_index=True)
        existing_df.to_csv(results_file, index=False)
    else:
        new_row.to_csv(results_file, index=False)

# JavaScript for timer (20 minutes = 1200 seconds)
timer_html = """
<script>
let timeLeft = 1200; // 20 minutes in seconds
function startTimer() {
    let timerElement = document.getElementById("timer");
    timerElement.innerHTML = formatTime(timeLeft);
    let timer = setInterval(function() {
        timeLeft--;
        timerElement.innerHTML = formatTime(timeLeft);
        if (timeLeft <= 0) {
            clearInterval(timer);
            timerElement.innerHTML = "Time's Up!";
            document.getElementById("submit_form").click();
        }
    }, 1000);
}
function formatTime(seconds) {
    let minutes = Math.floor(seconds / 60);
    let secs = seconds % 60;
    return minutes + ":" + (secs < 10 ? "0" : "") + secs;
}
</script>
"""

# Main app
st.title("Python Programming Quiz")

# Left sidebar for role selection
with st.sidebar:
    role = st.selectbox("Select Role", ["Student", "Lecturer"])
    if role == "Lecturer" and not st.session_state.authenticated:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if username == "lecturer" and password == "securepass123":  # Replace with secure credentials
                st.session_state.authenticated = True
                st.session_state.user_role = "lecturer"
                st.rerun()
            else:
                st.error("Invalid credentials")
    if st.session_state.authenticated and role == "Lecturer" and os.path.exists("all_quiz_results.csv"):
        cumulative_df = pd.read_csv("all_quiz_results.csv")
        st.write("Cumulative Results for All Students:")
        st.dataframe(cumulative_df)
        st.markdown(create_download_link(cumulative_df, "all_quiz_results.csv"), unsafe_allow_html=True)

# Student mode
if role == "Student":
    if not st.session_state.user_details:
        with st.form("user_details_form"):
            st.header("Enter Your Details")
            name = st.text_input("Name")
            course_title = st.text_input("Course Title")
            index_number = st.text_input("Index Number")
            submit_details = st.form_submit_button("Start Quiz")
            if submit_details:
                if name and course_title and index_number:
                    st.session_state.user_details = {
                        "name": name,
                        "course_title": course_title,
                        "index_number": index_number
                    }
                    st.session_state.timer_started = True
                    st.session_state.start_time = datetime.now()
                else:
                    st.error("Please fill in all fields.")
    else:
        # Timer display
        if st.session_state.timer_started and not st.session_state.time_up:
            components.html(f"""
            {timer_html}
            <div style="font-size: 24px; font-weight: bold; color: #FF4B4B; position: fixed; top: 10px; right: 10px; background-color: white; padding: 10px; border: 2px solid #FF4B4B; border-radius: 5px;">
                Time Remaining: <span id="timer">20:00</span>
            </div>
            <button id="submit_form" style="display:none;" onclick="document.getElementById('end_quiz').click();"></button>
            <script>startTimer();</script>
            """, height=50)

        # Check if time is up
        if st.session_state.timer_started and not st.session_state.time_up:
            elapsed_time = (datetime.now() - st.session_state.start_time).total_seconds()
            if elapsed_time >= 1200:  # 20 minutes
                st.session_state.time_up = True

        # Quiz logic
        if not st.session_state.time_up and st.session_state.current_index < len(quiz_data):
            question_data = quiz_data[st.session_state.current_index]
            st.header(f"Question {st.session_state.current_index + 1} of {len(quiz_data)}")
            st.write(question_data["question"])
            
            with st.form(key=f"question_{st.session_state.current_index}"):
                default_answer = st.session_state.responses[st.session_state.current_index]["selected"] if st.session_state.responses[st.session_state.current_index] else None
                selected = st.radio("Select an option:", question_data["options"], key=f"q{st.session_state.current_index}", index=question_data["options"].index(default_answer) if default_answer else None)
                col1, col2 = st.columns(2)
                with col1:
                    previous_button = st.form_submit_button("Previous")
                with col2:
                    next_button = st.form_submit_button("Next")
                
                if next_button:
                    if selected:
                        is_correct = selected == question_data["correct"]
                        st.session_state.responses[st.session_state.current_index] = {
                            "question": question_data["question"],
                            "selected": selected,
                            "correct": question_data["correct"],
                            "is_correct": is_correct,
                            "explanation": question_data["explanation"]
                        }
                        st.session_state.current_index += 1
                        st.rerun()
                    else:
                        st.error("Please select an option.")
                
                if previous_button and st.session_state.current_index > 0:
                    st.session_state.current_index -= 1
                    st.rerun()

        # Handle time up or quiz completion
        if st.button("End Quiz", key="end_quiz") or st.session_state.time_up or st.session_state.current_index >= len(quiz_data):
            st.session_state.time_up = True
            st.header("Quiz Completed!")
            st.write(f"Name: {st.session_state.user_details['name']}")
            st.write(f"Course Title: {st.session_state.user_details['course_title']}")
            st.write(f"Index Number: {st.session_state.user_details['index_number']}")
            start_time_str = st.session_state.start_time.strftime("%Y-%m-%d %H:%M:%S") if st.session_state.start_time else "N/A"
            st.write(f"Start Time: {start_time_str}")
            
            st.session_state.score = sum(1 for r in st.session_state.responses if r and r["is_correct"])
            st.write(f"Your Score: {st.session_state.score} out of {len(quiz_data)} ({st.session_state.score / len(quiz_data) * 100:.2f}%)")
            
            detailed_responses = [
                {
                    "Question": r["question"],
                    "Selected Answer": r["selected"],
                    "Correct Answer": r["correct"],
                    "Is Correct": r["is_correct"],
                    "Explanation": r["explanation"]
                } for r in st.session_state.responses if r
            ]
            detailed_df = pd.DataFrame(detailed_responses)
            detailed_df.insert(0, "Index Number", st.session_state.user_details["index_number"])
            detailed_df.insert(0, "Course Title", st.session_state.user_details["course_title"])
            detailed_df.insert(0, "Name", st.session_state.user_details["name"])
            st.write("Your Responses:")
            st.dataframe(detailed_df)
            
            student_data = {
                "Name": st.session_state.user_details["name"],
                "Course Title": st.session_state.user_details["course_title"],
                "Index Number": st.session_state.user_details["index_number"],
                "Score": st.session_state.score,
                "Percentage": f"{st.session_state.score / len(quiz_data) * 100:.2f}%",
                "Start Time": start_time_str
            }
            summary_df = pd.DataFrame([student_data])
            
            save_cumulative_results(student_data)
            
            filename = f"quiz_results_{st.session_state.user_details['index_number']}_{uuid.uuid4().hex[:8]}.csv"
            st.markdown(create_download_link(summary_df, filename), unsafe_allow_html=True)
            
            if st.button("Restart Quiz"):
                reset_quiz()
                st.rerun()
