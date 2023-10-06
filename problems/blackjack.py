###############################################################################
#### DO NOT EDIT THIS SECTION
###############################################################################
from typing import Dict, Any, List, Tuple, Optional
from shared_utils import set_weighted_score_data
from scaffolded_writing.cfg import ScaffoldedWritingCFG
from scaffolded_writing.student_submission import StudentSubmission
from shared_utils import grade_question_parameterized

def generate(data: Dict[str, Any]) -> None:
    data["params"]["subproblem_definition_cfg"] = PROBLEM_CONFIG.to_json_string()

def grade(data: Dict[str, Any]) -> None:
    grade_question_parameterized(data, "subproblem_definition", grade_statement)
    set_weighted_score_data(data)

###############################################################################
#### DO NOT EDIT ABOVE HERE, ONLY EDIT BELOW
###############################################################################

statement = 'Assume you are playing black jack against the devil for your chance to live.' + \
            'You have no prior knowledge about the deck. You have a pair of 5\'s and the devil has a 9 showing'

PROBLEM_CONFIG = ScaffoldedWritingCFG.fromstring(f"""
    START -> "Hit" UNTIL | "Stand at 10" | "Split hands.     First hand: " ACTION "      Second hand: " ACTION
    ACTION -> "Hit" UNTIL | "Stand at 5"
    UNTIL -> "until you have" VALUE
    VALUE -> "21" | "greater than" NUMBER
    NUMBER -> "18" | "16" | "11"
""")

def grade_statement(tokens: List[str]) -> Tuple[bool, Optional[str]]:
    submission = StudentSubmission(tokens, PROBLEM_CONFIG)

    if submission.does_path_exist("ACTION", "Stand at 5"):
        return False, 'You are at no danger when standing at 5. You might as well go higher.'
    
    if submission.does_path_exist("START", "Stand at 10"):
        return False, 'Not quite. You have high potential for a good score. You might as well go higher.'

    if "Split" in submission.token_list[0] and \
        (submission.does_path_exist("VALUE", "21") and not submission.does_path_exist("NUMBER", "18") and not submission.does_path_exist("NUMBER", "16") and not submission.does_path_exist("NUMBER", "11") \
    or    submission.does_path_exist("NUMBER", "18") and not submission.does_path_exist("VALUE", "21") and not submission.does_path_exist("NUMBER", "16") and not submission.does_path_exist("NUMBER", "11") \
    or    submission.does_path_exist("NUMBER", "16") and not submission.does_path_exist("VALUE", "21") and not submission.does_path_exist("NUMBER", "18") and not submission.does_path_exist("NUMBER", "11") \
    or    submission.does_path_exist("NUMBER", "11") and not submission.does_path_exist("VALUE", "21") and not submission.does_path_exist("NUMBER", "18") and not submission.does_path_exist("NUMBER", "16")):
    
        return False, 'It is usually wise to have different goals in mind when you split hands on a bad split.'

    if submission.does_path_exist("START", "Hit") and submission.does_path_exist("VALUE", "21"):
        return False, "This would be really unlikely to go exactly for 21."

    return True, None


