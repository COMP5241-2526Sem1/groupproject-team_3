"""
Points Service Module
Manages student points, rankings, and achievements
"""

from datetime import datetime
from bson import ObjectId
from services.db_service import db_service
from models.activity import Activity
from models.student import Student
from models.course import Course
import logging

logger = logging.getLogger(__name__)

class PointsService:
    """Service for managing student points and rankings"""
    
    # Point values for different actions
    POINTS = {
        'poll_response': 10,           # Completing a poll
        'short_answer_response': 20,   # Submitting a short answer
        'word_cloud_response': 15,     # Contributing to word cloud
        'poll_correct': 30,            # Getting poll answer correct (with auto-grading)
        'early_submission': 5,         # Bonus for being among first submissions
        'feedback_received': 5,        # Receiving teacher feedback
    }
    
    @staticmethod
    def calculate_student_points(student_identifier, course_id=None):
        """
        Calculate total points for a student
        
        Args:
            student_identifier (str): student_id or student_name
            course_id (str, optional): Filter by specific course
            
        Returns:
            dict: Points breakdown and total
        """
        try:
            points_breakdown = {
                'poll_responses': 0,
                'short_answer_responses': 0,
                'word_cloud_responses': 0,
                'correct_answers': 0,
                'early_submissions': 0,
                'feedback_received': 0,
                'total': 0
            }
            
            # Build query for activities
            query = {}
            if course_id:
                query['course_id'] = course_id
            
            # Get all activities
            activities = db_service.find_many(Activity.COLLECTION_NAME, query)
            
            for activity in activities:
                responses = activity.get('responses', [])
                
                for response in responses:
                    # Check if this response belongs to the student
                    if (response.get('student_id') == student_identifier or 
                        response.get('student_name') == student_identifier):
                        
                        activity_type = activity.get('type')
                        
                        # Points for poll responses
                        if activity_type == Activity.TYPE_POLL:
                            points_breakdown['poll_responses'] += PointsService.POINTS['poll_response']
                            
                            # Check if answer is correct (for auto-graded polls)
                            if response.get('is_correct'):
                                points_breakdown['correct_answers'] += PointsService.POINTS['poll_correct']
                        
                        # Points for short answer
                        elif activity_type == Activity.TYPE_SHORT_ANSWER:
                            points_breakdown['short_answer_responses'] += PointsService.POINTS['short_answer_response']
                        
                        # Points for word cloud
                        elif activity_type == Activity.TYPE_WORD_CLOUD:
                            points_breakdown['word_cloud_responses'] += PointsService.POINTS['word_cloud_response']
                        
                        # Bonus for early submission (first 5 responses)
                        response_index = responses.index(response)
                        if response_index < 5:
                            points_breakdown['early_submissions'] += PointsService.POINTS['early_submission']
                        
                        # Points for receiving feedback
                        if response.get('feedback'):
                            points_breakdown['feedback_received'] += PointsService.POINTS['feedback_received']
            
            # Calculate total
            points_breakdown['total'] = sum([
                points_breakdown['poll_responses'],
                points_breakdown['short_answer_responses'],
                points_breakdown['word_cloud_responses'],
                points_breakdown['correct_answers'],
                points_breakdown['early_submissions'],
                points_breakdown['feedback_received']
            ])
            
            return points_breakdown
            
        except Exception as e:
            logger.error(f"Error calculating points for {student_identifier}: {e}")
            return {'total': 0}
    
    @staticmethod
    def get_course_leaderboard(course_id, limit=50):
        """
        Get leaderboard for a specific course
        
        Args:
            course_id (str): Course ID
            limit (int): Maximum number of students to return
            
        Returns:
            list: Ranked list of students with their points
        """
        try:
            # Get all students in the course
            students = Student.find_by_course(course_id)
            
            leaderboard = []
            
            for student in students:
                student_id = student.get('student_id')
                student_name = student.get('name', 'Anonymous')
                
                # Calculate points
                points_data = PointsService.calculate_student_points(student_id, course_id)
                
                # Count activities completed
                activities_count = PointsService.count_student_activities(student_id, course_id)
                
                leaderboard.append({
                    '_id': student.get('_id'),
                    'student_id': student_id,
                    'name': student_name,
                    'points': points_data['total'],
                    'points_breakdown': points_data,
                    'activities_completed': activities_count,
                    'rank': 0  # Will be set after sorting
                })
            
            # Sort by points (descending)
            leaderboard.sort(key=lambda x: x['points'], reverse=True)
            
            # Assign ranks
            for i, entry in enumerate(leaderboard):
                entry['rank'] = i + 1
            
            return leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"Error getting course leaderboard: {e}")
            return []
    
    @staticmethod
    def get_global_leaderboard(limit=100):
        """
        Get global leaderboard across all courses
        
        Args:
            limit (int): Maximum number of students to return
            
        Returns:
            list: Ranked list of students with their points
        """
        try:
            # Get all students
            students = db_service.find_many(Student.COLLECTION_NAME, {})
            
            leaderboard = []
            
            for student in students:
                student_id = student.get('student_id')
                student_name = student.get('name', 'Anonymous')
                course_id = student.get('course_id')
                
                # Calculate points (all courses)
                points_data = PointsService.calculate_student_points(student_id)
                
                # Count activities completed
                activities_count = PointsService.count_student_activities(student_id)
                
                # Get course name
                course = Course.find_by_id(course_id)
                course_name = course.get('name', 'Unknown') if course else 'Unknown'
                
                leaderboard.append({
                    '_id': student.get('_id'),
                    'student_id': student_id,
                    'name': student_name,
                    'course_name': course_name,
                    'points': points_data['total'],
                    'activities_completed': activities_count,
                    'rank': 0  # Will be set after sorting
                })
            
            # Sort by points (descending)
            leaderboard.sort(key=lambda x: x['points'], reverse=True)
            
            # Assign ranks
            for i, entry in enumerate(leaderboard):
                entry['rank'] = i + 1
            
            return leaderboard[:limit]
            
        except Exception as e:
            logger.error(f"Error getting global leaderboard: {e}")
            return []
    
    @staticmethod
    def count_student_activities(student_identifier, course_id=None):
        """
        Count number of activities a student has participated in
        
        Args:
            student_identifier (str): student_id or student_name
            course_id (str, optional): Filter by specific course
            
        Returns:
            int: Number of activities completed
        """
        try:
            query = {}
            if course_id:
                query['course_id'] = course_id
            
            # Get all activities
            activities = db_service.find_many(Activity.COLLECTION_NAME, query)
            
            count = 0
            for activity in activities:
                responses = activity.get('responses', [])
                for response in responses:
                    if (response.get('student_id') == student_identifier or 
                        response.get('student_name') == student_identifier):
                        count += 1
                        break  # Count each activity only once
            
            return count
            
        except Exception as e:
            logger.error(f"Error counting activities for {student_identifier}: {e}")
            return 0
    
    @staticmethod
    def get_student_rank(student_identifier, course_id):
        """
        Get a student's rank in a course
        
        Args:
            student_identifier (str): student_id or student_name
            course_id (str): Course ID
            
        Returns:
            dict: Rank information including position and total students
        """
        try:
            leaderboard = PointsService.get_course_leaderboard(course_id, limit=1000)
            
            for entry in leaderboard:
                if entry['student_id'] == student_identifier:
                    return {
                        'rank': entry['rank'],
                        'total_students': len(leaderboard),
                        'points': entry['points'],
                        'percentile': round((1 - (entry['rank'] - 1) / len(leaderboard)) * 100, 1)
                    }
            
            return {
                'rank': None,
                'total_students': len(leaderboard),
                'points': 0,
                'percentile': 0
            }
            
        except Exception as e:
            logger.error(f"Error getting student rank: {e}")
            return {'rank': None, 'total_students': 0, 'points': 0, 'percentile': 0}
    
    @staticmethod
    def get_achievements(student_identifier, course_id=None):
        """
        Get achievements/badges earned by a student
        
        Args:
            student_identifier (str): student_id or student_name
            course_id (str, optional): Filter by specific course
            
        Returns:
            list: List of earned achievements
        """
        points_data = PointsService.calculate_student_points(student_identifier, course_id)
        activities_count = PointsService.count_student_activities(student_identifier, course_id)
        
        achievements = []
        
        # Activity milestones
        if activities_count >= 1:
            achievements.append({'name': '🎯 First Step', 'description': 'Completed first activity'})
        if activities_count >= 5:
            achievements.append({'name': '🔥 Active Learner', 'description': 'Completed 5 activities'})
        if activities_count >= 10:
            achievements.append({'name': '⭐ Dedicated Student', 'description': 'Completed 10 activities'})
        if activities_count >= 25:
            achievements.append({'name': '💎 Master Learner', 'description': 'Completed 25 activities'})
        
        # Points milestones
        total_points = points_data['total']
        if total_points >= 100:
            achievements.append({'name': '💯 Century Club', 'description': 'Earned 100 points'})
        if total_points >= 500:
            achievements.append({'name': '🏅 Point Champion', 'description': 'Earned 500 points'})
        if total_points >= 1000:
            achievements.append({'name': '👑 Point Legend', 'description': 'Earned 1000 points'})
        
        # Correct answers
        if points_data.get('correct_answers', 0) >= PointsService.POINTS['poll_correct'] * 5:
            achievements.append({'name': '🎓 Quiz Master', 'description': 'Got 5+ correct answers'})
        
        # Early bird
        if points_data.get('early_submissions', 0) >= PointsService.POINTS['early_submission'] * 5:
            achievements.append({'name': '⚡ Early Bird', 'description': 'Early submission 5+ times'})
        
        return achievements

# Create a singleton instance
points_service = PointsService()
