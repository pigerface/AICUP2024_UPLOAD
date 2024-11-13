"""Module for handling TBrain dataset processing and evaluation tasks."""

import json
import os

class Question:
    """
    A class representing a question in the TBrain dataset.
    
    Attributes:
        question_id: Unique identifier for the question
        category: Category of the question
        content: The question text content
        choices: List of possible answer choices
        answer: Selected answer (-1 if unanswered)
    """
    def __init__(self, question_id, category, content, choices):
        self.question_id = question_id
        self.category = category
        self.content = content
        self.choices = choices
        self.answer = -1

    def __str__(self):
        return f'\033[1mQ.{self.question_id} ({self.category})\033[0m  {self.content}\n' + \
            (f'Unsolved: {", ".join(map(str, self.choices))}\n' if self.answer == -1 else f'Our Answer: {self.answer}')
    
    __repr__ = __str__

class Reference:
    """
    A class representing a reference document in the TBrain dataset.
    
    Attributes:
        ref_id: Unique identifier for the reference
        category: Category of the reference document
        content: The reference document content
    """
    def __init__(self, category, ref_id, content):
        self.ref_id = ref_id
        self.category = category
        self.content = content
    
    def __str__(self):
        return f'== \033[1m{self.category} | {self.ref_id}\033[0m ==\n{self.content}'
    
    __repr__ = __str__

class Tbrain:
    """
    Main class for managing TBrain dataset operations.
    
    Attributes:
        reference_dir_path: Path to reference documents directory
        question_json_path: Path to questions JSON file
        output_json_path: Path to output answers JSON file
        summary_dir_path: Path to summary documents directory
        truth_json_path: Path to ground truth answers JSON file
    """
    def __init__(self, reference_dir_path, question_json_path, output_json_path, summary_dir_path, truth_json_path = None):
        """
        Initialize Tbrain instance with necessary file paths.
        
        Args:
            reference_dir_path: Path to reference documents
            question_json_path: Path to questions file
            output_json_path: Path to save answers
            summary_dir_path: Path to summary documents
            truth_json_path: Optional path to ground truth file
        """
        self.reference_dir_path = reference_dir_path
        self.question_json_path = question_json_path
        self.output_json_path = output_json_path
        self.summary_dir_path = summary_dir_path
        self.truth_json_path = truth_json_path
        self.references = {}
        self.questions = {}
        self.truths = {}
        self.summaries = {}
        self._preprocess_dataset()
        self._preprocess_summary()

    def _preprocess_dataset(self):
        """Load and process reference documents, questions, and ground truth data."""
        for root, _, files in os.walk(self.reference_dir_path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                category = os.path.basename(os.path.dirname(file_path))
                if file_path.endswith('.txt'):
                    ref_id = os.path.splitext(file)[0]
                    if os.path.isfile(file_path) and ref_id.isdigit():
                        with open(file_path, 'r') as file:
                            content = file.read()
                            if (category not in self.references):
                                self.references[category] = {}
                            self.references[category][int(ref_id)] = Reference(
                                category, int(ref_id), content)

        with open(self.question_json_path, 'r') as file:
            data = json.load(file)
        for question in data['questions']:
            self.questions[question['qid']] = Question(
                question['qid'], question['category'], question['query'], question['source'])
        
        with open(self.truth_json_path, 'r') as file:
            data = json.load(file)
        for truth in data['ground_truths']:
            self.truths[truth['qid']] = truth['retrieve']

        # assert set(self.questions.keys()) == set(self.truths.keys())
        
    def _preprocess_summary(self):
        """Load and process summary documents."""
        for root, _, files in os.walk(self.summary_dir_path):
            for file in sorted(files):
                file_path = os.path.join(root, file)
                category = os.path.basename(os.path.dirname(file_path))
                if file_path.endswith('.txt'):
                    ref_id = os.path.splitext(file)[0]
                    if os.path.isfile(file_path) and ref_id.isdigit():
                        with open(file_path, 'r') as file:
                            content = file.read()
                            if (category not in self.summaries):
                                self.summaries[category] = {}
                            self.summaries[category][int(ref_id)] = content

    def _write_output_json(self):
        """Write answered questions to output JSON file."""
        data = {'answers': []}
        for question in self.questions.values():
            if question.answer != -1:
                data['answers'].append({
                    'qid': question.question_id,
                    'retrieve': question.answer,
                })
        data['answers'] = sorted(
            data['answers'], key=lambda x: x['qid'])
        with open(self.output_json_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

    def get_reference(self, category, id):
        """
        Get a reference document by category and ID.
        
        Args:
            category: Document category
            id: Document ID
        
        Returns:
            Reference: The requested reference document
        """
        return self.references[category][id]
    
    def get_question(self, id):
        """
        Get a question by ID.
        
        Args:
            id: Question ID
        
        Returns:
            Question: The requested question
        """
        return self.questions[id]
    
    def get_answer(self, id):
        """
        Get ground truth answer for a question.
        
        Args:
            id: Question ID
        
        Returns:
            int: The correct answer
        """
        return self.truths[id]

    def get_question_list(self, unsolved_only=False):
        """
        Get list of questions.
        
        Args:
            unsolved_only: If True, return only unanswered questions
        
        Returns:
            list[Question]: List of questions
        """
        return [question for question in self.questions.values() if not unsolved_only or question.answer == -1]
    
    def get_specific_question(self, question_id_list):
        """
        Get specific questions by their IDs.
        
        Args:
            question_id_list: List of question IDs
        
        Returns:
            list[Question]: List of requested questions
        """
        return [self.questions[question_id] for question_id in question_id_list]
    
    def get_summary(self, category, id):
        """
        Get a summary document by category and ID.
        
        Args:
            category: Document category
            id: Document ID
        
        Returns:
            str: The summary content
        """
        return self.summaries[category][id]
    
    def answer_question(self, question_id, answer):
        """
        Submit an answer for a question.
        
        Args:
            question_id: Question ID
            answer: Selected answer choice
            
        Raises:
            ValueError: If answer is not in valid choices
        """
        if answer not in self.questions[question_id].choices:
            raise ValueError(f'Invalid answer: {answer}')
        self.questions[question_id].answer = answer
        self._write_output_json()

    def evaluate(self):
        """
        Evaluate current answers against ground truth and print results.
        
        Prints:
            - Number of correct answers
            - Accuracy percentage
            - Number of unanswered questions
        """
        not_answered = 0
        correct = 0
        not_correct = 0
        for question in self.questions.values():
            if question.answer == -1:
                not_answered += 1
            elif question.answer == self.truths[question.question_id]:
                correct += 1
            else:
                not_correct += 1
        print("=== Evaluation ===")
        print(f"Correct: {correct} / {correct + not_correct} ({correct / (correct + not_correct) * 100:.2f}%)")
        if not_answered > 0:
            print(f"({not_answered} questions not answered)")
        print("==================")
