import sys
import json
import swisseph as swe
import datetime
from typing import Dict, List, Tuple
from util import KundaliSVGGenerator, EnhancedKundliGenerator

def generate_kundali_charts(date: str, time: str, place: str, gender: str, timezone: str,
                          lagna_file: str = "lagna_chart.svg",
                          navamsa_file: str = "navamsa_chart.svg") -> Dict:
    """
    Generate and save Lagna and Navamsa charts as separate SVG files.
    Returns the result of kundli.generate_full_analysis() as a dictionary.
    """
    kundli = EnhancedKundliGenerator(date, time, place, gender, timezone)
    analysis_result = kundli.generate_full_analysis()  # Capture the analysis result

    svg_generator = KundaliSVGGenerator(kundli)
    svg_generator.save_charts(lagna_file, navamsa_file)

    return analysis_result  # Return the analysis result

if __name__ == "__main__":
    # Parse command-line arguments
    date = sys.argv[1]
    time = sys.argv[2]
    place = sys.argv[3]
    gender = sys.argv[4]
    timezone = sys.argv[5]
    lagna_file = sys.argv[6] if len(sys.argv) > 6 else "lagna_chart.svg"
    navamsa_file = sys.argv[7] if len(sys.argv) > 7 else "navamsa_chart.svg"

    # Generate charts and get the analysis result
    analysis_result = generate_kundali_charts(date, time, place, gender, timezone, lagna_file, navamsa_file)

    # Print the analysis result as JSON
    print(json.dumps(analysis_result))