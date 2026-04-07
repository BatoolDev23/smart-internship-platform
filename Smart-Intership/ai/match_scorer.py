from ai.recommendation_engine import RecommendationEngine
import pandas as pd
import numpy as np

class MatchScorer:
    def __init__(self):
        self.engine = RecommendationEngine()
        
    def score_applications(self, student_data, internships_df):
        """
        Calculate match scores for a student against all internships.
        Weights: Skills 50%, Experience 20%, Knowledge 20%, Location 10%.
        """
        if internships_df.empty:
            return pd.DataFrame()
            
        scores_df = internships_df.copy()
        n_internships = len(internships_df)
        
        # 1. Skills Score (50%)
        student_skills = student_data.get('skills', '')
        internship_skills = internships_df['required_skills'].fillna('').tolist()
        skills_sim = self.engine.calculate_text_similarity(student_skills, internship_skills)
        
        # 2. Knowledge Score (20%)
        student_knowledge = student_data.get('knowledge_areas', '')
        internship_knowledge = internships_df['knowledge_areas'].fillna('').tolist()
        knowledge_sim = self.engine.calculate_text_similarity(student_knowledge, internship_knowledge)
        
        # 3. Experience Score (20%)
        # Normalization: If student exp >= required exp, score is 1.0
        # Otherwise, partial credit based on how close they are.
        student_exp = float(student_data.get('experience_years', 0))
        required_exp = internships_df['required_experience'].fillna(0).astype(float).values
        
        exp_scores = np.ones(n_internships)
        for i, req_exp in enumerate(required_exp):
            if req_exp > 0:
                if student_exp >= req_exp:
                    exp_scores[i] = 1.0
                else:
                    exp_scores[i] = max(0, student_exp / req_exp)
            else:
                exp_scores[i] = 1.0 # If no experience required
                
        # 4. Location Score (10%)
        student_location = student_data.get('location', '').lower()
        locations = internships_df['location'].fillna('').str.lower().values
        is_remote = internships_df['is_remote'].fillna(False).astype(bool).values
        
        location_scores = np.zeros(n_internships)
        for i in range(n_internships):
            if is_remote[i]:
                location_scores[i] = 1.0 # Remote matches perfectly
            elif student_location and student_location in locations[i] or locations[i] in student_location:
                location_scores[i] = 1.0
            else:
                location_scores[i] = 0.0

        # University Filter Adjustment
        # If an internship specifies a university and it doesn't match the student's, heavy penalty
        student_uni = student_data.get('university', '')
        uni_filters = internships_df['university_filter'].fillna('all').values
        uni_penalty = np.ones(n_internships)
        for i, uni in enumerate(uni_filters):
            if uni.lower() != 'all' and uni != student_uni:
                uni_penalty[i] = 0.0 # Strict filter

        # Calculate Final Weighted Score (0-100)
        final_scores = (
            (skills_sim * 0.5) + 
            (exp_scores * 0.2) + 
            (knowledge_sim * 0.2) + 
            (location_scores * 0.1)
        ) * 100 * uni_penalty
        
        scores_df['match_score'] = final_scores
        scores_df['skills_score'] = skills_sim * 100
        scores_df['experience_score'] = exp_scores * 100
        scores_df['knowledge_score'] = knowledge_sim * 100
        scores_df['location_score'] = location_scores * 100
        
        # Sort by match score descending
        scores_df = scores_df.sort_values('match_score', ascending=False)
        return scores_df
