import sys
import os
import glob
from agents.vyakarana_rakshak import VyakaranRakshak
from agents.bandharan_rakshak import BandharanRakshak
from agents.shaili_rakshak import ShailiRakshak
from agents.suraksha_rakshak import SurakshaRakshak
from agents.karyakshamata_rakshak import KaryakshamataRakshak
from agents.jatilata_rakshak import JatilataRakshak

def analyze_file(file_path):
    try:
        from rich.console import Console
        from rich.table import Table
        from rich.panel import Panel
        console = Console()
    except ImportError:
        console = None
        
    print(f"\nચકાસણી ચાલુ છે: {file_path}")
    print("-" * 50)
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        if console:
            console.print(f"[bold red]ફાઈલ વાંચવામાં ભૂલ: {e}[/]")
        else:
            print(f"ફાઈલ વાંચવામાં ભૂલ: {e}")
        return

    agents = [
        VyakaranRakshak(),
        BandharanRakshak(),
        ShailiRakshak(),
        SurakshaRakshak(),
        KaryakshamataRakshak(),
        JatilataRakshak()
    ]
    
    all_issues = []
    for agent in agents:
        all_issues.extend(agent.check_file(content))
        
    full_clean = True
    
    if not all_issues:
        if console:
             console.print(Panel("[bold green]✅ કોઈ સમસ્યા મળી નથી. કોડ ઉત્તમ છે![/]", title="પરિણામ"))
        else:
             print("✅ કોઈ સમસ્યા મળી નથી. કોડ ઉત્તમ છે!")
    else:
        full_clean = False
        all_issues.sort(key=lambda x: x.get('line', 0))
        
        if console:
            table = Table(title=f"અહેવાલ: {os.path.basename(file_path)}")
            table.add_column("Line", justify="right", style="cyan", no_wrap=True)
            table.add_column("Type", style="magenta")
            table.add_column("Message", style="white")

            for issue in all_issues:
                severity_color = "yellow" if issue['severity'] == 'warning' else "blue"
                severity_icon = "⚠️" if issue['severity'] == 'warning' else "ℹ️"
                table.add_row(
                    str(issue['line']), 
                    f"[{severity_color}]{severity_icon} {issue['severity'].upper()}[/]",
                    issue['message']
                )
            console.print(table)
        else:
            for issue in all_issues:
                icon = "⚠️" if issue['severity'] == 'warning' else "ℹ️"
                print(f"{icon}  Line {issue['line']}: {issue['message']}")
            
    return full_clean

def main():
    if len(sys.argv) < 2:
        print("ઉપયોગ: python run_agents.py <ફાઈલ_અથવા_ડાયરેક્ટરી>")
        sys.exit(1)
        
    target = sys.argv[1]
    
    if os.path.isfile(target):
        analyze_file(target)
    elif os.path.isdir(target):
        # Find all .py files recursively
        files = glob.glob(os.path.join(target, "**/*.py"), recursive=True)
        # Also include files directly in dir
        # If target has gujarati chars, glob might be tricky, walk is safer
        files = []
        for root, dirs, filenames in os.walk(target):
            for filename in filenames:
                if filename.endswith(".py"):
                    files.append(os.path.join(root, filename))
        
        if not files:
            print(f"'{target}' માં કોઈ પાયથોન ફાઈલો મળી નથી.")
            return

        for f in files:
            analyze_file(f)
    else:
        print(f"ખરાબ પાથ: {target}")

if __name__ == "__main__":
    main()
