import numpy as np
import pandas as pd

# Analyze quiz data and generate performance metrics
def analyze_quiz_data(historical_quiz, current_quiz):
    # Historical quiz data analysis
    topic_accuracy = historical_quiz.groupby('topic')['is_correct'].mean().reset_index()
    difficulty_accuracy = historical_quiz.groupby('difficulty')['is_correct'].mean().reset_index()

    # Weak topics based on accuracy
    weak_topics = topic_accuracy[topic_accuracy['is_correct'] < 0.6]['topic'].tolist()

    # Frequent errors (questions that were answered incorrectly more than once)
    frequent_errors = historical_quiz[historical_quiz['is_correct'] == False]['question_id'].value_counts().head(5).index.tolist()

    # Student Persona Analysis (New)
    persona = analyze_persona(historical_quiz, current_quiz)

    return {
        "difficulty_accuracy": difficulty_accuracy.set_index('difficulty').to_dict()['is_correct'],
        "topic_accuracy": topic_accuracy.set_index('topic').to_dict()['is_correct'],
        "weak_topics": weak_topics,
        "frequent_errors": frequent_errors,
        "persona": persona
    }

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

def generate_suggestions(persona, weak_areas):
    # Suggest actions based on persona and weak areas
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
