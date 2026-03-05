#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ગુજરાતી અનુવાદક માટે ટેસ્ટ

આ ફાઈલ અનુવાદક મોડ્યુલનું ટેસ્ટિંગ કરે છે.
"""

import sys
import os
import pytest

# પ્રોજેક્ટ પાથ ઉમેરો
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ગુજરાતી_પાઈથન import ગુજરાતી_કોડ_ચલાવો
from ગુજરાતી_પાઈથન.અનુવાદક import કીવર્ડ_અનુવાદક, કોડ_અનુવાદ_કરો, વેલિડેશન_કરો


class ટેસ્ટ_કીવર્ડ_અનુવાદક:
    """
    કીવર્ડ અનુવાદકના ટેસ્ટ
    """
    
    def setup_method(self):
        """
        ટેસ્ટ માટે સેટઅપ
        """
        self.અનુવાદક = કીવર્ડ_અનુવાદક()
    
    def test_basic_keywords(self):
        """
        મૂળભૂત કીવર્ડ્સનું ટેસ્ટ
        """
        # ગુજરાતી કોડ
        ગુજરાતી_કોડ = """
ડેફ નમસ્કાર():
    છાપો("નમસ્તે!")
    
નમસ્કાર()
        """.strip()
        
        # અપેક્ષિત અંગ્રેજી કોડ
        અપેક્ષિત = """
def નમસ્કાર():
    print("નમસ્તે!")
    
નમસ્કાર()
        """.strip()
        
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()
    
    def test_control_structures(self):
        """
        કન્ટ્રોલ સ્ટ્રક્ચર્સનું ટેસ્ટ
        """
        ગુજરાતી_કોડ = """
જો સાચું:
    છાપો("હા")
નહીં તો:
    છાપો("ના")
        """.strip()
        
        અપેક્ષિત = """
if True:
    print("હા")
else:
    print("ના")
        """.strip()
        
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()
    
    def test_loops(self):
        """
        લૂપ્સનું ટેસ્ટ
        """
        ગુજરાતી_કોડ = """
ફોર i ઇન રેંજ(3):
    છાપો(i)
    
સંખ્યા = 0
વ્હાઈલ સંખ્યા < 3:
    છાપો(સંખ્યા)
    સંખ્યા += 1
        """.strip()
        
        અપેક્ષિત = """
for i in range(3):
    print(i)
    
સંખ્યા = 0
while સંખ્યા < 3:
    print(સંખ્યા)
    સંખ્યા += 1
        """.strip()
        
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()
    
    def test_class_definition(self):
        """
        ક્લાસ ડેફિનેશનનું ટેસ્ટ
        """
        ગુજરાતી_કોડ = """
ક્લાસ ટેસ્ટ:
    ડેફ __init__(સ્વ):
        સ્વ.નામ = "ટેસ્ટ"
    
    ડેફ પરિચય(સ્વ):
        પરત આપો સ્વ.નામ
        """.strip()
        
        અપેક્ષિત = """
class ટેસ્ટ:
    def __init__(સ્વ):
        સ્વ.નામ = "ટેસ્ટ"
    
    def પરિચય(સ્વ):
        return સ્વ.નામ
        """.strip()
        
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()
    
    def test_import_statements(self):
        """
        ઇમ્પોર્ટ સ્ટેટમેન્ટ્સનું ટેસ્ટ
        """
        ગુજરાતી_કોડ = """
ઈમ્પોર્ટ ગણિત
માંથી os ઈમ્પોર્ટ path
ઈમ્પોર્ટ numpy આસ np
        """.strip()
        
        અપેક્ષિત = """
import math
from os import path
import numpy as np
        """.strip()
        
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()
    
    def test_exception_handling(self):
        """
        એક્સેપ્શન હેન્ડલિંગનું ટેસ્ટ
        """
        ગુજરાતી_કોડ = """
પ્રયત્ન કરો:
    પરિણામ = 10 / 0
સિવાય ZeroDivisionError:
    છાપો("એરર!")
અંતે:
    છાપો("પૂર્ણ")
        """.strip()
        
        અપેક્ષિત = """
try:
    પરિણામ = 10 / 0
except ZeroDivisionError:
    print("એરર!")
finally:
    print("પૂર્ણ")
        """.strip()
        
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()
    
    def test_reverse_translation(self):
        """
        રિવર્સ ટ્રાન્સલેશનનું ટેસ્ટ
        """
        અંગ્રેજી_કોડ = """
def test():
    print("Hello")
    return True
        """.strip()
        
        અપેક્ષિત = """
ડેફ test():
    છાપો("Hello")
    પરત આપો સાચું
        """.strip()
        
        પરિણામ = self.અનુવાદક.અંગ્રેજીથી_ગુજરાતી(અંગ્રેજી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()

    def test_round_alias_forward_translation(self):
        """
        ગોળ ફંક્શન round() માં અનુવાદ થાય છે
        """
        ગુજરાતી_કોડ = "ગોળ(2.5)"
        અપેક્ષિત = "round(2.5)"

        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()

    def test_round_alias_reverse_translation(self):
        """
        round() નો કેનોનિકલ ગુજરાતી અનુવાદ ગોળ રહે છે
        """
        અંગ્રેજી_કોડ = "round(2.5)"
        અપેક્ષિત = "ગોળ(2.5)"

        પરિણામ = self.અનુવાદક.અંગ્રેજીથી_ગુજરાતી(અંગ્રેજી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()

    def test_round_alias_execution_matches_python_round(self):
        """
        ગોળ ફંક્શન Python round() જેવી જ વર્તણૂક રાખે છે
        """
        test_cases = [
            ("અ = ગોળ(2.5)\nછાપો(અ)\n", f"{round(2.5)}\n"),
            ("અ = ગોળ(12.5, -1)\nછાપો(અ)\n", f"{round(12.5, -1)}\n"),
        ]

        for ગુજરાતી_કોડ, અપેક્ષિત_આઉટપુટ in test_cases:
            પરિણામ = ગુજરાતી_કોડ_ચલાવો(ગુજરાતી_કોડ)
            assert પરિણામ['સફળતા'], પરિણામ['એરર']
            assert પરિણામ['આઉટપુટ'] == અપેક્ષિત_આઉટપુટ
    def test_validation(self):
        """
        વેલિડેશનનું ટેસ્ટ
        """
        # સાચો કોડ
        સાચો_કોડ = "ડેફ ટેસ્ટ(): છાપો('હેલો')"
        errors = વેલિડેશન_કરો(સાચો_કોડ)
        assert len(errors) == 0


class ટેસ્ટ_યાદી_મેથડ્સ:
    """
    યાદી (list) મેથડ મેપિંગ ટેસ્ટ — Issue #30
    """

    def setup_method(self):
        self.અનુવાદક = કીવર્ડ_અનુવાદક()

    def test_append_basic(self):
        """ઉમેરો → append મૂળભૂત ટેસ્ટ"""
        ગુજરાતી_કોડ = 'ફળો.ઉમેરો("સફરજન")'
        અપેક્ષિત = 'ફળો.append("સફરજન")'
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()

    def test_pop_basic(self):
        """કાઢો → pop મૂળભૂત ટેસ્ટ"""
        ગુજરાતી_કોડ = 'ફળો.કાઢો()'
        અપેક્ષિત = 'ફળો.pop()'
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()

    def test_pop_with_index(self):
        """કાઢો(0) → pop(0) ઇન્ડેક્સ સાથે"""
        ગુજરાતી_કોડ = 'ફળો.કાઢો(0)'
        અપેક્ષિત = 'ફળો.pop(0)'
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()

    def test_append_in_loop(self):
        """લૂપ અંદર ઉમેરો ટેસ્ટ"""
        ગુજરાતી_કોડ = """\
ફોર i ઇન રેંજ(5):
    ફળો.ઉમેરો(i)""".strip()
        અપેક્ષિત = """\
for i in range(5):
    ફળો.append(i)""".strip()
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()

    def test_method_with_variable_prefix(self):
        """કોઈપણ વેરિએબલ નામ સાથે મેથડ ટેસ્ટ"""
        ગુજરાતી_કોડ = 'મારી_યાદી.ઉમેરો(42)'
        અપેક્ષિત = 'મારી_યાદી.append(42)'
        પરિણામ = self.અનુવાદક.ગુજરાતીથી_અંગ્રેજી(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()


class ટેસ્ટ_ગ્લોબલ_ફંક્શન્સ:
    """
    ગ્લોબલ ફંક્શન્સના ટેસ્ટ
    """
    
    def test_કોડ_અનુવાદ_કરો(self):
        """
        કોડ અનુવાદ ફંક્શનનું ટેસ્ટ
        """
        ગુજરાતી_કોડ = "છાપો('નમસ્તે')"
        અપેક્ષિત = "print('નમસ્તે')"
        
        પરિણામ = કોડ_અનુવાદ_કરો(ગુજરાતી_કોડ)
        assert પરિણામ.strip() == અપેક્ષિત.strip()


from ગુજરાતી_પાઈથન.અનુવાદક import TranslationResult, _અનુવાદક
from ગુજરાતી_પાઈથન import ગુજરાતી_કોડ_ચલાવો


class ટેસ્ટ_સ્ત્રોત_નકશો:
    """
    Source map: traceback remapping tests.
    Verifies that errors raised during execution of Gujarati code
    are attributed to the correct Gujarati line and show Gujarati source text.
    """

    def test_translation_result_has_line_map(self):
        """TranslationResult carries a line_map dict."""
        result = _અનુવાદક.ગુજરાતીથી_અંગ્રેજી_સ_નકશો("છાપો('નમસ્તે')")
        assert isinstance(result, TranslationResult)
        assert result.code.strip() == "print('નમસ્તે')"
        assert isinstance(result.line_map, dict)
        assert result.line_map.get(1) == 1  # identity for single-line code

    def test_line_map_covers_all_lines(self):
        """line_map has an entry for every generated line."""
        code = "ક = 1\nખ = 2\nછાપો(ક + ખ)"
        result = _અનુવાદક.ગુજરાતીથી_અંગ્રેજી_સ_નકશો(code)
        n_generated = result.code.count('\n') + 1
        for i in range(1, n_generated + 1):
            assert i in result.line_map

    @pytest.mark.parametrize("code, bad_line", [
        # NameError on line 2 (undefined variable)
        ("ક = 1\nછાપો(અવ્યાખ્યાયિત)\n", 2),
        # ZeroDivisionError on line 1
        ("છાપો(1 // 0)\n", 1),
        # NameError inside a Gujarati def block — line 3
        ("ડેફ foo():\n    x = 1\n    છાપો(undefined)\nfoo()\n", 3),
    ])
    def test_traceback_points_to_gujarati_line(self, code, bad_line):
        """Error output must reference the correct Gujarati source line number."""
        result = ગુજરાતી_કોડ_ચલાવો(code)
        assert not result['સફળતા'], "Expected execution to fail"
        assert f"લાઈન {bad_line}" in result['એરર'], (
            f"Expected 'લાઈન {bad_line}' in error output, got:\n{result['એરર']}"
        )

    @pytest.mark.parametrize("code, expected_gujarati_text", [
        # The error output should show the Gujarati source line, not 'print(undefined)'
        ("છાપો(અવ્યાખ્યાયિત)\n", "છાપો(અવ્યાખ્યાયિત)"),
    ])
    def test_traceback_shows_gujarati_source_line(self, code, expected_gujarati_text):
        """Error output must show the Gujarati source text, not the translated Python."""
        result = ગુજરાતી_કોડ_ચલાવો(code)
        assert not result['સફળતા']
        assert expected_gujarati_text in result['એરર'], (
            f"Expected Gujarati source text in error, got:\n{result['એરર']}"
        )

    def test_error_message_back_translates_keyword(self):
        """NameError message should use the Gujarati keyword name, not the English one."""
        # છાપો(ક્ષ) → NameError references 'print' internally, but should show 'છાપો'
        result = ગુજરાતી_કોડ_ચલાવો("છાપો(ક્ષ)\n")
        assert not result['સફળતા']
        # The error message must contain the Gujarati name, not 'print'
        assert 'print' not in result['એરર'], (
            f"Error message still exposes English keyword:\n{result['એરર']}"
        )
