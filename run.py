import sys
import argparse
from victim_mas.graph_mas import analyze_page_mas

def main():
    parser = argparse.ArgumentParser(description="Analyze a webpage with Multi-Agent System")
    parser.add_argument("url", help="URL to analyze")
    parser.add_argument("--verbose", "-v", action="store_true", help="Show detailed output")
    
    args = parser.parse_args()
    
    try:
        result = analyze_page_mas(args.url)
        
        # Silent execution - no output
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
