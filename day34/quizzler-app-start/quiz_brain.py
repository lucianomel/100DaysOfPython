import html
from data import api_call
from question_model import Question


class QuizBrain:

    def __init__(self):
        self.question_number = 0
        self.score = 0
        self.question_list = []
        self.current_question = None
        self.set_game_category("General Knowledge")

    def still_has_questions(self):
        return self.question_number < len(self.question_list)

    def next_question(self):
        self.current_question = self.question_list[self.question_number]
        self.question_number += 1
        q_text = html.unescape(self.current_question.text)
        return f"Q.{self.question_number}: {q_text}"

    def check_answer(self, user_answer):
        correct_answer = self.current_question.answer
        if user_answer.lower() == correct_answer.lower():
            self.score += 1
            return True
        else:
            return False

    def set_game_category(self, category):
        """Returns true if category could be modified, false if not"""
        question_data = api_call(category)
        can_modify_category = question_data != []
        if can_modify_category:
            self.question_list = []
            self.question_number = 0
            for question in question_data:
                question_text = question["question"]
                question_answer = question["correct_answer"]
                new_question = Question(question_text, question_answer)
                self.question_list.append(new_question)
        return can_modify_category
