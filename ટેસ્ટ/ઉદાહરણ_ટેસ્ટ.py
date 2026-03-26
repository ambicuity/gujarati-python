#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
ઉદાહરણ ટેસ્ટ - ગુજરાતી પાઈથન

આ ફાઈલ બધા ઉદાહરણોનું ટેસ્ટિંગ કરે છે અને તેમની કાર્યક્ષમતા ચકાસે છે.
"""

import os
import sys
import pytest
import subprocess
from pathlib import Path

# પ્રોજેક્ટ પાથ ઉમેરો
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ગુજરાતી_પાઈથન import કોડ_અનુવાદ_કરો


class ઉદાહરણ_ટેસ્ટ:
    """બધા ઉદાહરણ ફાઈલોના ટેસ્ટ"""

    def setup_method(self):
        """ટેસ્ટ માટે સેટઅપ"""
        self.પ્રોજેક્ટ_પાથ = Path(__file__).parent.parent
        self.ઉદાહરણ_પાથ = self.પ્રોજેક્ટ_પાથ / "ઉદાહરણો"
        self.મુખ્ય_ફાઈલ = self.પ્રોજેક્ટ_પાથ / "મુખ્ય.py"
        
        # ખાતરી કરો કે ફાઈલો અસ્તિત્વમાં છે
        assert self.ઉદાહરણ_પાથ.exists(), f"ઉદાહરણ ડિરેક્ટરી મળી નથી: {self.ઉદાહરણ_પાથ}"
        assert self.મુખ્ય_ફાઈલ.exists(), f"મુખ્ય ફાઈલ મળી નથી: {self.મુખ્ય_ફાઈલ}"

    def _ફાઈલ_ચલાવો(self, ઉદાહરણ_નામ):
        """
        ઉદાહરણ ફાઈલ ચલાવે છે અને તેનું પરિણામ પરત કરે છે
        
        પેરામીટર:
            ઉદાહરણ_નામ (str): ઉદાહરણ ફાઈલનું નામ
            
        પરત:
            dict: {'returncode': int, 'stdout': str, 'stderr': str}
        """
        ફાઈલ_પાથ = self.ઉદાહરણ_પાથ / ઉદાહરણ_નામ
        assert ફાઈલ_પાથ.exists(), f"ઉદાહરણ ફાઈલ મળી નથી: {ફાઈલ_પાથ}"
        
        # Windows encoding issues માટે environment વેરિએબલ સેટ કરો
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'  # Python 3.7+ માટે UTF-8 mode
        
        # Python subprocess ઉપયોગ કરીને ફાઈલ ચલાવો
        પરિણામ = subprocess.run(
            [sys.executable, str(self.મુખ્ય_ફાઈલ), str(ફાઈલ_પાથ)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Unicode encode/decode errors ને handle કરો
            cwd=str(self.પ્રોજેક્ટ_પાથ),
            env=env
        )
        
        return {
            'returncode': પરિણામ.returncode,
            'stdout': પરિણામ.stdout,
            'stderr': પરિણામ.stderr
        }

    def test_સરળ_ડેમો(self):
        """સરળ ડેમો ફાઈલનું ટેસ્ટ"""
        પરિણામ = self._ફાઈલ_ચલાવો("સરળ_ડેમો.py")
        
        assert પરિણામ['returncode'] == 0, \
            f"સરળ ડેમો fail થયો. Error: {પરિણામ['stderr']}"
        
        આઉટપુટ = પરિણામ['stdout']
        
        # મુખ્ય આઉટપુટ ચકાસો
        assert "નમસ્તે! આ ગુજરાતી પાઈથન છે!" in આઉટપુટ
        assert "મારું નામ રામ છે" in આઉટપુટ
        assert "10 + 20 = 30" in આઉટપુટ
        assert "તમે પુખ્ત છો" in આઉટપુટ
        assert "ગુજરાતી પાઈથન ડેમો પૂર્ણ!" in આઉટપુટ

    def test_મૂળભૂત_ઉદાહરણ(self):
        """મૂળભૂત ઉદાહરણ ફાઈલનું ટેસ્ટ"""
        પરિણામ = self._ફાઈલ_ચલાવો("મૂળભૂત_ઉદાહરણ.py")
        
        assert પરિણામ['returncode'] == 0, \
            f"મૂળભૂત ઉદાહરણ fail થયો. Error: {પરિણામ['stderr']}"
        
        આઉટપુટ = પરિણામ['stdout']
        
        # મુખ્ય આઉટપુટ ચકાસો
        assert "સ્વાગત છે ગુજરાતી પાઈથન" in આઉટપુટ
        assert "ગણિતના ઓપરેશન" in આઉટપુટ
        assert "શરત પરીક્ષણ" in આઉટપુટ
        assert "લૂપ્સ" in આઉટપુટ
        assert "ડેટા સ્ટ્રક્ચર" in આઉટપુટ
        assert "એરર હેન્ડલિંગ" in આઉટપુટ
        assert "ગુજરાતી પાઈથનનો ડેમો પૂર્ણ!" in આઉટપુટ

    def test_ક્લાસ_ઉદાહરણ(self):
        """ક્લાસ ઉદાહરણ ફાઈલનું ટેસ્ટ"""
        પરિણામ = self._ફાઈલ_ચલાવો("ક્લાસ_ઉદાહરણ.py")
        
        assert પરિણામ['returncode'] == 0, \
            f"ક્લાસ ઉદાહરણ fail થયો. Error: {પરિણામ['stderr']}"
        
        આઉટપુટ = પરિણામ['stdout']
        
        # મુખ્ય આઉટપુટ ચકાસો
        assert "ગુજરાતી પાઈથન - ક્લાસ ડેમો" in આઉટપુટ
        assert "કુલ વ્યક્તિઓ" in આઉટપુટ
        assert "હું રાજેશ છું" in આઉટપુટ
        assert "હું પ્રિયા છું" in આઉટપુટ
        assert "હવે મિત્રો છે" in આઉટપુટ
        assert "રીપોર્ટ કાર્ડ" in આઉટપુટ
        assert "ક્લાસ ડેમો પૂર્ણ!" in આઉટપુટ

    def test_બધા_ઉદાહરણો_યાદી(self):
        """ખાતરી કરો કે બધા અપેક્ષિત ઉદાહરણ ફાઈલો અસ્તિત્વમાં છે"""
        અપેક્ષિત_ફાઈલો = [
            "સરળ_ડેમો.py",
            "મૂળભૂત_ઉદાહરણ.py", 
            "ક્લાસ_ઉદાહરણ.py",
            "અડવાન્સ_ઉદાહરણ.py",
            "સંપૂર્ણ_ઉદાહરણ.py"
        ]
        
        for ફાઈલ_નામ in અપેક્ષિત_ફાઈલો:
            ફાઈલ_પાથ = self.ઉદાહરણ_પાથ / ફાઈલ_નામ
            assert ફાઈલ_પાથ.exists(), \
                f"ઉદાહરણ ફાઈલ મળી નથી: {ફાઈલ_નામ}"

    @pytest.mark.parametrize("ફાઈલ_નામ", [
        "સરળ_ડેમો.py",
        "મૂળભૂત_ઉદાહરણ.py", 
        "ક્લાસ_ઉદાહરણ.py"
    ])
    def test_ઉદાહરણ_ફાઈલ_વાચન(self, ફાઈલ_નામ):
        """ખાતરી કરો કે ઉદાહરણ ફાઈલો UTF-8 માં વાંચી શકાય છે"""
        ફાઈલ_પાથ = self.ઉદાહરણ_પાથ / ફાઈલ_નામ
        # ફાઈલ વાંચો
        સામગ્રી = ફાઈલ_પાથ.read_text(encoding='utf-8')
        assert સામગ્રી is not None, f"ફાઈલ સામગ્રી null છે: {ફાઈલ_નામ}"
        assert len(સામગ્રી) > 0, f"ફાઈલ ખાલી છે: {ફાઈલ_નામ}"
        
        # ગુજરાતી યુનિકોડ અક્ષરો છે કે નહીં
        assert any(ord(char) > 127 for char in સામગ્રી), \
            f"ગુજરાતી અક્ષરો મળ્યા નથી: {ફાઈલ_નામ}"

    @pytest.mark.parametrize("ફાઈલ_નામ", [
        "સરળ_ડેમો.py",
        "મૂળભૂત_ઉદાહરણ.py", 
        "ક્લાસ_ઉદાહરણ.py"
    ])
    def test_અનુવાદ_ક્ષમતા(self, ફાઈલ_નામ):
        """ખાતરી કરો કે કામ કરતા ઉદાહરણો સફળતાપૂર્વક અનુવાદ થાય છે"""
        ફાઈલ_પાથ = self.ઉદાહરણ_પાથ / ફાઈલ_નામ
        # ફાઈલ વાંચો
        ગુજરાતી_કોડ = ફાઈલ_પાથ.read_text(encoding='utf-8')
        
        # અનુવાદ કરો
        અંગ્રેજી_કોડ = કોડ_અનુવાદ_કરો(ગુજરાતી_કોડ)
        
        # ખાતરી કરો કે અનુવાદ થયો છે
        assert અંગ્રેજી_કોડ is not None, f"અનુવાદ નહીં થયો: {ફાઈલ_નામ}"
        assert len(અંગ્રેજી_કોડ) > 0, f"અનુવાદ ખાલી છે: {ફાઈલ_નામ}"
        
        # મૂળભૂત કીવર્ડ અનુવાદ ચકાસો
        if "છાપો(" in ગુજરાતી_કોડ:
            assert "print(" in અંગ્રેજી_કોડ, f"છાપોનો અનુવાદ નહીં થયો: {ફાઈલ_નામ}"


class પ્રદર્શન_ટેસ્ટ:
    """ઉદાહરણો માટે પ્રદર્શન ટેસ્ટ"""

    def setup_method(self):
        """ટેસ્ટ માટે સેટઅપ"""
        self.પ્રોજેક્ટ_પાથ = Path(__file__).parent.parent
        self.ઉદાહરણ_પાથ = self.પ્રોજેક્ટ_પાથ / "ઉદાહરણો"
        self.મુખ્ય_ફાઈલ = self.પ્રોજેક્ટ_પાથ / "મુખ્ય.py"

    @pytest.mark.parametrize("ફાઈલ_નામ, મહત્તમ_સમય", [
        ("સરળ_ડેમો.py", 5.0),  # મહત્તમ 5 સેકન્ડ
        ("મૂળભૂત_ઉદાહરણ.py", 10.0),  # મહત્તમ 10 સેકન્ડ
        ("ક્લાસ_ઉદાહરણ.py", 15.0)  # મહત્તમ 15 સેકન્ડ
    ])
    def test_ઉદાહરણ_એક્ઝિક્યુશન_સમય(self, ફાઈલ_નામ, મહત્તમ_સમય):
        """ખાતરી કરો કે ઉદાહરણો વ્યાજબી સમયમાં ચાલે છે"""
        import time
        
        ફાઈલ_પાથ = self.ઉદાહરણ_પાથ / ફાઈલ_નામ
        શરુઆત_સમય = time.time()
        # Windows encoding issues માટે environment વેરિએબલ સેટ કરો
        env = os.environ.copy()
        env['PYTHONIOENCODING'] = 'utf-8'
        env['PYTHONUTF8'] = '1'  # Python 3.7+ માટે UTF-8 mode
        
        પરિણામ = subprocess.run(
            [sys.executable, str(self.મુખ્ય_ફાઈલ), str(ફાઈલ_પાથ)],
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace',  # Unicode encode/decode errors ને handle કરો
            cwd=str(self.પ્રોજેક્ટ_પાથ),
            env=env,
            timeout=મહત્તમ_સમય  # Timeout protection
        )
        
        અંત_સમય = time.time()
        કુલ_સમય = અંત_સમય - શરુઆત_સમય
        
        assert પરિણામ.returncode == 0, \
            f"{ફાઈલ_નામ} execute નહીં થયો"
        assert કુલ_સમય < મહત્તમ_સમય, \
            f"{ફાઈલ_નામ} વધુ પડતો સમય લીધો: {કુલ_સમય:.2f}s"


if __name__ == "__main__":
    print("=" * 60)
    print("ગુજરાતી પાઈથન - ઉદાહરણ ટેસ્ટ")  
    print("=" * 60)
    print()
    
    # UTF-8 આઉટપુટ માટે encoding set કરો
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')
    
    pytest.main(['-v', __file__])
