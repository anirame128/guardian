import sys
import argparse
from victim_mas.graph import analyze_page

def main():
    parser = argparse.ArgumentParser(description="Analyze a webpage with LLM")
    parser.add_argument("url", help="URL to analyze")
    
    args = parser.parse_args()
    
    try:
        result = analyze_page(args.url)
        
        # Silent execution - no output
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
