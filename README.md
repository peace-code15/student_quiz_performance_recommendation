# Quiz Performance Analysis Application

Overview  
A Flask-based web application for analyzing quiz performance. It provides insights into student accuracy, identifies weak topics, generates visualizations, and offers personalized recommendations.

Features  
- Analyze quiz data for accuracy by difficulty and topic.  
- Identify weak topics and frequent errors.  
- Generate bar chart visualizations.  
- Provide personalized improvement suggestions.  

Setup Instructions  
1. Install Python 3.7+ and set up a virtual environment.  
2. Install dependencies:  
   ```bash  
   pip install flask requests pandas matplotlib  
   ```  
3. Run the application:  
   ```bash  
   python app.py  
   ```  
4. Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser.  

Workflow  
1. Fetch quiz data from APIs or JSON input.  
2. Analyze performance by difficulty and topic.  
3. Generate visualizations saved in the `visualizations/` folder.  
4. Provide recommendations based on user trends.  

Visualizations  
- **Accuracy by Difficulty**: Displays accuracy for Easy, Medium, and Hard questions.  
- **Weak Topics**: Highlights topics with less than 60% accuracy.  

Project Structure  
- **app.py**: Main application file.  
- **templates/**: Contains the `index.html` file for the frontend.  
- **visualizations/**: Stores generated charts.  

Insights  
- Students excel in Easy and Medium questions but struggle with Hard ones.  
- Weak topics (e.g., Algebra, Physics) require focused practice.  

Contact  
For queries, contact Nikita at nikitanodal343@gmail.com  
