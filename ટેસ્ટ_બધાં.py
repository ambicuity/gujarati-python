#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
સંપૂર્ણ ટેસ્ટ સ્ક્રિપ્ટ - ગુજરાતી પાઈથન

આ સ્ક્રિપ્ટ બધા ટેસ્ટ ચલાવે છે જે GitHub Actions વર્કફ્લોમાં ચાલશે.
"""

import os
import sys
import subprocess
import platform
import locale
from pathlib import Path

def પ્લેટફોર્મ_માહિતી_દર્શાવો():
    """પ્લેટફોર્મની માહિતી દર્શાવે છે"""
    print("🖥️ Platform Information:")
    print(f"  OS: {platform.system()} {platform.release()}")
    print(f"  Architecture: {platform.machine()}")
    print(f"  Python: {sys.version}")
    print(f"  Encoding: {sys.getdefaultencoding()}")
    try:
        # Use the newer method instead of deprecated getdefaultlocale()
        current_locale = locale.getlocale()
        print(f"  Locale: {current_locale}")
    except Exception:
        print("  Locale: Unable to determine")
    print(f"  File system encoding: {sys.getfilesystemencoding()}")
    print()

    # Gujarati Unicode support test
    print("🔤 Unicode Support Test:")
    gujarati_text = "ગુજરાતી પાઈથન"
    print(f"  Gujarati text: {gujarati_text}")
    print(f"  Length: {len(gujarati_text)} characters")
    print(f"  Encoded length: {len(gujarati_text.encode('utf-8'))} bytes")
    print()

def કમાંડ_ચલાવો(કમાંડ, વર્ણન):
    """કમાંડ ચલાવે છે અને પરિણામ બતાવે છે"""
    print(f"{વર્ણન}")
    print(f"Running: {' '.join(કમાંડ)}")
    
    try:
        result = subprocess.run(
            કમાંડ,
            capture_output=True,
            text=True,
            encoding='utf-8',
            check=True
        )
        if result.stdout.strip():
            print("આઉટપુટ:")
            print(result.stdout[:500])  # પ્રથમ 500 characters
            if len(result.stdout) > 500:
                print("... (આઉટપુટ કાપવામાં આવ્યું)")
        print("સફળ")
    except subprocess.CalledProcessError as e:
        print(f"નિષ્ફળ: {e}")
        if e.stdout:
            print(f"STDOUT: {e.stdout}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        return False
    except Exception as e:
        print(f"એરર: {e}")
        return False
    
    print()
    return True

def મુખ્ય():
    """મુખ્ય ફંક્શન"""
    print("=" * 60)
    print("ગુજરાતી પાઈથન - સંપૂર્ણ ટેસ્ટ સ્યુટ")
    print("=" * 60)
    print()

    # UTF-8 encoding set કરો
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    if hasattr(sys.stderr, 'reconfigure'):
        sys.stderr.reconfigure(encoding='utf-8')

    # પ્લેટફોર્મ માહિતી
    પ્લેટફોર્મ_માહિતી_દર્શાવો()

    # પ્રોજેક્ટ ડિરેક્ટરી
    project_dir = Path(__file__).parent
    os.chdir(project_dir)

    # સફળતાનો સ્કોર
    સફળ_ટેસ્ટ = 0
    કુલ_ટેસ્ટ = 0

    # 1. મૂળભૂત ટેસ્ટ (Basic tests)
    print("મૂળભૂત ટેસ્ટ (Basic Tests)")
    print("-" * 30)
    
    કુલ_ટેસ્ટ += 1
    if કમાંડ_ચલાવો([sys.executable, "-m", "unittest", "ટેસ્ટ.ટેસ્ટ_અનુવાદક", "-v"], 
                    "અનુવાદક ટેસ્ટ"):
        સફળ_ટેસ્ટ += 1
    
    કુલ_ટેસ્ટ += 1
    if કમાંડ_ચલાવો([sys.executable, "-m", "unittest", "ટેસ્ટ.પ્લેટફોર્મ_ટેસ્ટ", "-v"],
                    "પ્લેટફોર્મ ટેસ્ટ"):
        સફળ_ટેસ્ટ += 1

    # 2. ઉદાહરણ ટેસ્ટ (Example tests)
    print("ઉદાહરણ ટેસ્ટ (Example Tests)")
    print("-" * 30)
    
    કુલ_ટેસ્ટ += 1
    if કમાંડ_ચલાવો([sys.executable, "-m", "unittest", "ટેસ્ટ.ઉદાહરણ_ટેસ્ટ", "-v"],
                    "ઉદાહરણ ટેસ્ટ"):
        સફળ_ટેસ્ટ += 1

    # 3. CLI ઈન્ટરફેસ ટેસ્ટ (CLI Interface tests)
    print("CLI ઈન્ટરફેસ ટેસ્ટ (Command Line Interface Tests)")
    print("-" * 50)
    
    cli_tests = [
        ([sys.executable, "મુખ્ય.py", "--help"], "હેલ્પ કમાંડ"),
        ([sys.executable, "મુખ્ય.py", "--keywords"], "કીવર્ડ લિસ્ટ"),
        ([sys.executable, "મુખ્ય.py", "--search", "છાપો"], "કીવર્ડ સર્ચ"),
        ([sys.executable, "મુખ્ય.py", "ઉદાહરણો/સરળ_ડેમો.py"], "સરળ ઉદાહરણ"),
        ([sys.executable, "મુખ્ય.py", "--translate", "ઉદાહરણો/સરળ_ડેમો.py"], "અનુવાદ ટેસ્ટ")
    ]
    
    for કમાંડ, વર્ણન in cli_tests:
        કુલ_ટેસ્ટ += 1
        if કમાંડ_ચલાવો(કમાંડ, વર્ણન):
            સફળ_ટેસ્ટ += 1

    # 4. બધા ટેસ્ટ એકસાથે (All tests together)
    print("બધા ટેસ્ટ એકસાથે (All Tests Together)")
    print("-" * 40)
    
    કુલ_ટેસ્ટ += 1
    if કમાંડ_ચલાવો([sys.executable, "-m", "unittest", 
                     "ટેસ્ટ.ટેસ્ટ_અનુવાદક", "ટેસ્ટ.પ્લેટફોર્મ_ટેસ્ટ", "ટેસ્ટ.ઉદાહરણ_ટેસ્ટ", "-v"],
                    "બધા ટેસ્ટ એકસાથે"):
        સફળ_ટેસ્ટ += 1

    # પરિણામ
    print("=" * 60)
    print("ટેસ્ટ પરિણામ (Test Results)")
    print("=" * 60)
    
    print(f"સફળ ટેસ્ટ: {સફળ_ટેસ્ટ}")
    print(f"નિષ્ફળ ટેસ્ટ: {કુલ_ટેસ્ટ - સફળ_ટેસ્ટ}")
    print(f"📊 કુલ ટેસ્ટ: {કુલ_ટેસ્ટ}")
    print(f"📈 સફળતા દર: {(સફળ_ટેસ્ટ / કુલ_ટેસ્ટ * 100):.1f}%")
    
    if સફળ_ટેસ્ટ == કુલ_ટેસ્ટ:
        print("\nબધા ટેસ્ટ સફળ! ગુજરાતી પાઈથન તૈયાર છે!")
        return True
    else:
        print(f"\n{કુલ_ટેસ્ટ - સફળ_ટેસ્ટ} ટેસ્ટ નિષ્ફળ. કૃપા કરીને સમસ્યાઓ ઠીક કરો.")
        return False

if __name__ == "__main__":
    સફળતા = મુખ્ય()
    sys.exit(0 if સફળતા else 1)