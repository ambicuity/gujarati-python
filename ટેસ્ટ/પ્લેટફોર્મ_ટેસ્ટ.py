#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
પ્લેટફોર્મ સુસંગતતા ટેસ્ટ - ગુજરાતી પાઈથન

આ ટેસ્ટ વિવિધ પ્લેટફોર્મ પર ગુજરાતી પાઈથનની સુસંગતતા ચકાસે છે.
"""

import os
import sys
import platform
import tempfile
from pathlib import Path

# પ્રોજેક્ટ પાથ ઉમેરો
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from ગુજરાતી_પાઈથન import કોડ_અનુવાદ_કરો, ગુજરાતી_કોડ_ચલાવો

def પ્લેટફોર્મ_માહિતી_બતાવો():
    """પ્લેટફોર્મની માહિતી દેખાડે છે"""
    print("🖥️ પ્લેટફોર્મ માહિતી:")
    print(f"   OS: {platform.system()} {platform.release()}")
    print(f"   Architecture: {platform.machine()}")
    print(f"   Python: {sys.version}")
    print(f"   Encoding: {sys.getdefaultencoding()}")
    print()

def ફાઇલ_પાથ_ટેસ્ટ():
    """ફાઇલ પાથ હેન્ડલિંગ ટેસ્ટ કરે છે"""
    print("📁 ફાઇલ પાથ ટેસ્ટ:")
    
    # ટેમ્પરરી ફાઇલ બનાવો
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False, encoding='utf-8') as f:
        f.write('છાપો("હેલો વર્લ્ડ!")\n')
        temp_file = f.name
    
    try:
        # PathLib ઉપયોગ કરીને ફાઇલ વાંચો
        path = Path(temp_file)
        if path.exists():
            content = path.read_text(encoding='utf-8')
            print(f"   ✅ ફાઇલ સફળતાપૂર્વક વાંચી: {path.name}")
            print(f"   કન્ટેન્ટ: {content.strip()}")
        else:
            print(f"   ❌ ફાઇલ મળી નથી: {path}")
            
    finally:
        # ક્લીનઅપ
        os.unlink(temp_file)
    
    print()

def એન્કોડિંગ_ટેસ્ટ():
    """ગુજરાતી અક્ષરોની એન્કોડિંગ ટેસ્ટ કરે છે"""
    print("🔤 એન્કોડિંગ ટેસ્ટ:")
    
    # ગુજરાતી કોડ
    ગુજરાતી_કોડ = """
છાપો("નમસ્કાર! આ ગુજરાતી છે.")  
નામ = "રામ"
ઉંમર = 25
છાપો(f"{નામ} ની ઉંમર {ઉંમર} વર્ષ છે.")
    """.strip()
    
    try:
        # કોડ અનુવાદ કરો
        અનુવાદિત = કોડ_અનુવાદ_કરો(ગુજરાતી_કોડ)
        print("   ✅ ગુજરાતી કોડ સફળતાપૂર્વક અનુવાદ થયો")
        
        # કોડ ચલાવો  
        પરિણામ = ગુજરાતી_કોડ_ચલાવો(ગુજરાતી_કોડ)
        if પરિણામ['સફળતા']:
            print("   ✅ ગુજરાતી કોડ સફળતાપૂર્વક ચાલ્યો")
            print(f"   આઉટપુટ: {પરિણામ['આઉટપુટ'].strip()}")
        else:
            print(f"   ❌ કોડ ચલાવવામાં એરર: {પરિણામ['એરર']}")
            
    except Exception as e:
        print(f"   ❌ એન્કોડિંગ એરર: {e}")
    
    print()

def main():
    """મુખ્ય ટેસ્ટ ફંક્શન"""
    print("=" * 60)
    print("🧪 ગુજરાતી પાઈથન - પ્લેટફોર્મ સુસંગતતા ટેસ્ટ")  
    print("=" * 60)
    print()
    
    પ્લેટફોર્મ_માહિતી_બતાવો()
    ફાઇલ_પાથ_ટેસ્ટ()
    એન્કોડિંગ_ટેસ્ટ()
    
    print("=" * 60)
    print("🎉 પ્લેટફોર્મ સુસંગતતા ટેસ્ટ પૂર્ણ!")
    print("=" * 60)

if __name__ == "__main__":
    main()