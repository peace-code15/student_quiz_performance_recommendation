# from flask import Flask, render_template, request, jsonify
# import requests
# import pandas as pd

# app = Flask(__name__)

# # Function to fetch current quiz data from the API
# def fetch_current_quiz_data():
#     current_quiz_url = "https://jsonkeeper.com/b/LLQT"
#     response = requests.get(current_quiz_url)
#     return response.json()

# # Function to fetch historical quiz data from the API
# def fetch_historical_quiz_data():
#     historical_quiz_url = "https://api.jsonserve.com/XgAgFJ"
#     response = requests.get(historical_quiz_url)
#     return response.json()

# @app.route('/')
# def index():
#     return render_template('index.html')

# @app.route('/analyze', methods=['POST'])
# def analyze():
#     # Get the data from the JSON request
#     historical_quiz_api = request.json.get("historical_quiz_data")
#     current_quiz_api = request.json.get("current_quiz_data")
    
#     # Debugging: Print data to ensure it's being received correctly
#     print(f"Historical Quiz Data: {historical_quiz_api}")
#     print(f"Current Quiz Data: {current_quiz_api}")
    
#     # Fetch data from APIs if not provided in the request
#     if not historical_quiz_api or not current_quiz_api:
#         historical_quiz_api = fetch_historical_quiz_data()
#         current_quiz_api = fetch_current_quiz_data()

#     # Debugging: Print the fetched data
#     print(f"Fetched Historical Quiz Data: {historical_quiz_api}")
#     print(f"Fetched Current Quiz Data: {current_quiz_api}")

#     # Perform the analysis
#     result = analyze_quiz_data(historical_quiz_api, current_quiz_api)
    
#     # Return the analysis result as JSON
#     return jsonify(result)

# # Function to analyze quiz data and generate insights
# def analyze_quiz_data(historical_quiz, current_quiz):
#     historical_df = pd.DataFrame(historical_quiz)
#     current_df = pd.DataFrame(current_quiz)

#     # Difficulty accuracy: Calculate the accuracy based on difficulty
#     difficulty_accuracy = historical_df.groupby('difficulty')['is_correct'].mean().reset_index()

#     # Topic accuracy: Calculate accuracy based on topic
#     topic_accuracy = historical_df.groupby('topic')['is_correct'].mean().reset_index()

#     # Weak topics: Find topics where the accuracy is less than 60%
#     weak_topics = topic_accuracy[topic_accuracy['is_correct'] < 0.6]['topic'].tolist()

#     # Frequent errors: Find the most common errors made by the user (incorrect questions)
#     frequent_errors = historical_df[historical_df['is_correct'] == False]['question_id'].value_counts().head(5).index.tolist()

#     # Generate the persona based on historical quiz data and current quiz responses
#     persona = analyze_persona(historical_df, current_df)

#     return {
#         "difficulty_accuracy": difficulty_accuracy.set_index('difficulty').to_dict()['is_correct'],
#         "topic_accuracy": topic_accuracy.set_index('topic').to_dict()['is_correct'],
#         "weak_topics": weak_topics,
#         "frequent_errors": frequent_errors,
#         "persona": persona
#     }

# # Function to analyze the student's persona based on quiz performance
# def analyze_persona(historical_quiz, current_quiz):
#     # Track the total score and topic performance over time
#     total_scores = historical_quiz.groupby('quiz_id')['score'].mean()
#     average_score = total_scores.mean()

#     # Track frequent weak areas in topics
#     weak_areas = historical_quiz[historical_quiz['is_correct'] == False]['topic'].value_counts().head(3).index.tolist()

#     # Persona logic (this is just a simple example, can be enhanced)
#     if average_score > 80:
#         persona = "Strong Performer"
#     elif 60 <= average_score <= 80:
#         persona = "Needs Improvement"
#     else:
#         persona = "Hardcore Learner"

#     # Output persona and improvement suggestions
#     return {
#         "persona": persona,
#         "average_score": average_score,
#         "weak_areas": weak_areas,
#         "suggested_improvements": generate_suggestions(persona, weak_areas)
#     }

# # Function to generate suggestions based on persona and weak areas
# def generate_suggestions(persona, weak_areas):
#     suggestions = []
#     if persona == "Strong Performer":
#         suggestions.append("Keep up the good work! Focus on maintaining consistency across topics.")
#     elif persona == "Needs Improvement":
#         suggestions.append("Focus on revising the weak topics and practice more questions.")
#     elif persona == "Hardcore Learner":
#         suggestions.append("You’re challenging yourself with harder topics, but focus on improving accuracy.")

#     if "Math" in weak_areas:
#         suggestions.append("Focus on algebra and equations.")
#     if "Science" in weak_areas:
#         suggestions.append("Revisit basic physics and chemistry concepts.")

#     return suggestions

# # Run the Flask app
# if __name__ == '__main__':
#     app.run(debug=True)


from flask import Flask, render_template, request, jsonify
import requests
import pandas as pd
import matplotlib.pyplot as plt
import os

app = Flask(__name__)

# Function to fetch current quiz data from the API
def fetch_current_quiz_data():
    current_quiz_url = "https://jsonkeeper.com/b/LLQT"
    response = requests.get(current_quiz_url)
    return response.json()

# Function to fetch historical quiz data from the API
def fetch_historical_quiz_data():
    historical_quiz_url = "https://api.jsonserve.com/XgAgFJ"
    response = requests.get(historical_quiz_url)
    return response.json()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    # Get the data from the JSON request
    historical_quiz_api = request.json.get("historical_quiz_data")
    current_quiz_api = request.json.get("current_quiz_data")
    
    # Debugging: Print data to ensure it's being received correctly
    print(f"Historical Quiz Data: {historical_quiz_api}")
    print(f"Current Quiz Data: {current_quiz_api}")
    
    # Fetch data from APIs if not provided in the request
    if not historical_quiz_api or not current_quiz_api:
        historical_quiz_api = fetch_historical_quiz_data()
        current_quiz_api = fetch_current_quiz_data()

    # Debugging: Print the fetched data
    print(f"Fetched Historical Quiz Data: {historical_quiz_api}")
    print(f"Fetched Current Quiz Data: {current_quiz_api}")

    # Perform the analysis
    result = analyze_quiz_data(historical_quiz_api, current_quiz_api)
    
    # Generate visualizations
    generate_visualization(result)

    # Return the analysis result as JSON
    return jsonify(result)

# Function to analyze quiz data and generate insights
def analyze_quiz_data(historical_quiz, current_quiz):
    historical_df = pd.DataFrame(historical_quiz)
    current_df = pd.DataFrame(current_quiz)

    # Difficulty accuracy: Calculate the accuracy based on difficulty
    difficulty_accuracy = historical_df.groupby('difficulty')['is_correct'].mean().reset_index()

    # Topic accuracy: Calculate accuracy based on topic
    topic_accuracy = historical_df.groupby('topic')['is_correct'].mean().reset_index()

    # Weak topics: Find topics where the accuracy is less than 60%
    weak_topics = topic_accuracy[topic_accuracy['is_correct'] < 0.6]['topic'].tolist()

    # Frequent errors: Find the most common errors made by the user (incorrect questions)
    frequent_errors = historical_df[historical_df['is_correct'] == False]['question_id'].value_counts().head(5).index.tolist()

    # Generate the persona based on historical quiz data and current quiz responses
    persona = analyze_persona(historical_df, current_df)

    return {
        "difficulty_accuracy": difficulty_accuracy.set_index('difficulty').to_dict()['is_correct'],
        "topic_accuracy": topic_accuracy.set_index('topic').to_dict()['is_correct'],
        "weak_topics": weak_topics,
        "frequent_errors": frequent_errors,
        "persona": persona
    }

# Function to analyze the student's persona based on quiz performance
def analyze_persona(historical_quiz, current_quiz):
    # Track the total score and topic performance over time
    total_scores = historical_quiz.groupby('quiz_id')['score'].mean()
    average_score = total_scores.mean()

    # Track frequent weak areas in topics
    weak_areas = historical_quiz[historical_quiz['is_correct'] == False]['topic'].value_counts().head(3).index.tolist()

    # Persona logic (this is just a simple example, can be enhanced)
    if average_score > 80:
        persona = "Strong Performer"
    elif 60 <= average_score <= 80:
        persona = "Needs Improvement"
    else:
        persona = "Hardcore Learner"

    # Output persona and improvement suggestions
    return {
        "persona": persona,
        "average_score": average_score,
        "weak_areas": weak_areas,
        "suggested_improvements": generate_suggestions(persona, weak_areas)
    }

# Function to generate suggestions based on persona and weak areas
def generate_suggestions(persona, weak_areas):
    suggestions = []
    if persona == "Strong Performer":
        suggestions.append("Keep up the good work! Focus on maintaining consistency across topics.")
    elif persona == "Needs Improvement":
        suggestions.append("Focus on revising the weak topics and practice more questions.")
    elif persona == "Hardcore Learner":
        suggestions.append("You’re challenging yourself with harder topics, but focus on improving accuracy.")

    if "Math" in weak_areas:
        suggestions.append("Focus on algebra and equations.")
    if "Science" in weak_areas:
        suggestions.append("Revisit basic physics and chemistry concepts.")

    return suggestions

# Function to generate the visualizations and save the plot
def generate_visualization(data):
    try:
        # Ensure the visualizations directory exists
        if not os.path.exists('visualizations'):
            os.makedirs('visualizations')

        # Difficulty Accuracy Plot
        difficulty_accuracy = data["difficulty_accuracy"]
        difficulty_names = list(difficulty_accuracy.keys())
        difficulty_values = list(difficulty_accuracy.values())

        plt.figure(figsize=(8, 5))
        plt.bar(difficulty_names, difficulty_values, color='skyblue')
        plt.xlabel('Difficulty Level')
        plt.ylabel('Accuracy')
        plt.title('Difficulty Level vs Accuracy')

        # Save the plot to the visualizations directory
        plot_path = 'visualizations/difficulty_accuracy.png'
        plt.savefig(plot_path)
        plt.close()

        print(f"Difficulty accuracy plot saved to {plot_path}")

        # Weak Topics Plot
        weak_topics = data["weak_topics"]
        weak_topics_counts = [1 for _ in weak_topics]  # Just for illustration, you can modify as needed

        plt.figure(figsize=(8, 5))
        plt.bar(weak_topics, weak_topics_counts, color='lightcoral')
        plt.xlabel('Weak Topics')
        plt.ylabel('Count')
        plt.title('Weak Topics')

        # Save the weak topics plot
        weak_topics_path = 'visualizations/weak_topics.png'
        plt.savefig(weak_topics_path)
        plt.close()

        print(f"Weak topics plot saved to {weak_topics_path}")

    except Exception as e:
        print(f"Error generating visualization: {e}")

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
