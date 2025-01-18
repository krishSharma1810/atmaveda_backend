import swisseph as swe
import datetime
from typing import Dict, List, Tuple

class KundaliSVGGenerator:
    def __init__(self, kundli):
        self.kundli = kundli
        self.planet_colors = {
            swe.SUN: "red",
            swe.MOON: "blue",
            swe.MARS: "green",
            swe.MERCURY: "blue",
            swe.JUPITER: "purple",
            swe.VENUS: "green",
            swe.SATURN: "red",
            swe.MEAN_NODE: "red",  # Rahu
            swe.MEAN_NODE + 1: "brown",  # Ketu
        }
        self.planet_symbols = {
            swe.SUN: "Su",
            swe.MOON: "Mo",
            swe.MARS: "Ma",
            swe.MERCURY: "Me",
            swe.JUPITER: "Ju",
            swe.VENUS: "Ve",
            swe.SATURN: "Sa",
            swe.MEAN_NODE: "Ra",
            swe.MEAN_NODE + 1: "Ke",
        }
        
    def get_house_coordinates(self, house_num: int, planet_index: int = 0) -> Tuple[float, float]:
        """Calculate coordinates for planet placement in a house."""
        # Define the base positions and spacing for each house segment
        house_positions = {
            1: {'x': 180, 'y': 320, 'dx': 25, 'dy': -15},  # Bottom center
            2: {'x': 320, 'y': 320, 'dx': 25, 'dy': -15},  # Bottom right
            3: {'x': 320, 'y': 180, 'dx': 25, 'dy': -15},  # Right center
            4: {'x': 320, 'y': 40, 'dx': 25, 'dy': 15},    # Top right
            5: {'x': 180, 'y': 40, 'dx': 25, 'dy': 15},    # Top center
            6: {'x': 40, 'y': 40, 'dx': 25, 'dy': 15},     # Top left
            7: {'x': 40, 'y': 180, 'dx': 25, 'dy': 15},    # Left center
            8: {'x': 40, 'y': 320, 'dx': 25, 'dy': -15},   # Bottom left
            9: {'x': 180, 'y': 320, 'dx': -25, 'dy': -15}, # Bottom center
            10: {'x': 320, 'y': 320, 'dx': -25, 'dy': -15},# Bottom right
            11: {'x': 320, 'y': 40, 'dx': -25, 'dy': 15},  # Top right
            12: {'x': 180, 'y': 40, 'dx': -25, 'dy': 15},  # Top center
        }
        
        pos = house_positions[house_num]
        x = pos['x'] + (planet_index * pos['dx'])
        y = pos['y'] + (planet_index * pos['dy'])
        
        return (x, y)

    def generate_single_chart_svg(self, chart_type: str = "lagna") -> str:
        """Generate SVG string for a single chart."""
        chart_title = "Lagna Chart" if chart_type == "lagna" else "Navamsa Chart"
        
        svg_template = f"""
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400">
            <!-- Title Text -->
            <text x="20" y="30" font-family="Arial" font-size="16" font-weight="bold">{chart_title}</text>
            
            <!-- Chart -->
            <g transform="translate(20, 40)">
                <!-- Outer square -->
                <rect x="0" y="0" width="360" height="360" fill="none" stroke="red" stroke-width="1"/>
                
                <!-- Diagonal lines -->
                <line x1="0" y1="0" x2="360" y2="360" stroke="red" stroke-width="1"/>
                <line x1="360" y1="0" x2="0" y2="360" stroke="red" stroke-width="1"/>
                
                <!-- Cross lines -->
                <line x1="0" y1="180" x2="360" y2="180" stroke="red" stroke-width="1"/>
                <line x1="180" y1="0" x2="180" y2="360" stroke="red" stroke-width="1"/>
                
                <!-- Rhombus -->
                <line x1="180" y1="0" x2="360" y2="180" stroke="red" stroke-width="1"/>
                <line x1="360" y1="180" x2="180" y2="360" stroke="red" stroke-width="1"/>
                <line x1="180" y1="360" x2="0" y2="180" stroke="red" stroke-width="1"/>
                <line x1="0" y1="180" x2="180" y2="0" stroke="red" stroke-width="1"/>
                
                <!-- House numbers -->
                {self.generate_house_numbers()}
                
                <!-- Planets -->
                {self.generate_planet_positions(chart_type)}
            </g>
        </svg>
        """
        return svg_template

    def generate_house_numbers(self) -> str:
        """Generate SVG elements for house numbers."""
        house_positions = [
            (170, 30, "12"),   # Top center
            (320, 30, "11"),   # Top right
            (170, 330, "1"),   # Bottom center
            (320, 330, "10"),  # Bottom right
            (30, 30, "6"),     # Top left
            (30, 330, "8"),    # Bottom left
        ]
        
        return "\n".join([
            f'<text x="{x}" y="{y}" font-family="Arial" font-size="14" text-anchor="middle">{num}</text>'
            for x, y, num in house_positions
        ])

    def generate_planet_positions(self, chart_type: str = "lagna") -> str:
        """Generate SVG elements for planet positions."""
        planet_elements = []
        house_planets = {}
        
        # Get positions based on chart type
        if chart_type == "lagna":
            positions = self.kundli.planetary_positions
        else:  # navamsa
            positions = {planet: chart['D9'] for planet, chart in self.kundli.divisional_charts.items()}
        
        # Group planets by house
        for planet, longitude in positions.items():
            house_num = 1 + int(longitude / 30)
            if house_num not in house_planets:
                house_planets[house_num] = []
            house_planets[house_num].append(planet)
        
        # Generate planet elements with proper positioning
        for house_num, planets in house_planets.items():
            for idx, planet in enumerate(planets):
                x, y = self.get_house_coordinates(house_num, idx)
                color = self.planet_colors.get(planet, "black")
                symbol = self.planet_symbols.get(planet, "??")
                
                # Add a subtle background circle for better visibility
                planet_elements.append(
                    f'<circle cx="{x}" cy="{y-5}" r="8" fill="white" fill-opacity="0.7"/>'
                )
                planet_elements.append(
                    f'<text x="{x}" y="{y}" fill="{color}" '
                    f'font-family="Arial" font-size="14" text-anchor="middle">{symbol}</text>'
                )
        
        return "\n".join(planet_elements)

    def save_charts(self, lagna_file: str = "lagna_chart.svg", navamsa_file: str = "navamsa_chart.svg"):
            """Save both charts as separate SVG files."""
            # Save Lagna chart
            with open(lagna_file, 'w') as f:
                f.write(self.generate_single_chart_svg("lagna"))
                
            # Save Navamsa chart
            with open(navamsa_file, 'w') as f:
                f.write(self.generate_single_chart_svg("navamsa"))


class EnhancedKundliGenerator:
    def __init__(self, date, time, place, gender, timezone):
        self.date = date  # Format: 'DD/MM/YYYY'
        self.time = time  # Format: 'HH:MM'
        self.place = place  # Format: 'City, State, Country'
        self.gender = gender  # 'Male' or 'Female'
        self.timezone = timezone  # Format: 'UTC±HH:MM'
        self.julian_day = None
        self.ascendant = None
        self.planetary_positions = {}
        self.houses = {}
        self.aspects = []
        self.dasha_periods = []
        self.nakshatras = {}
        self.divisional_charts = {}
        self.yogas = []

        self.sign_lords = {
            0: swe.SUN,    # Aries - Mars
            1: swe.VENUS,  # Taurus - Venus
            2: swe.MERCURY,# Gemini - Mercury
            3: swe.MOON,   # Cancer - Moon
            4: swe.SUN,    # Leo - Sun
            5: swe.MERCURY,# Virgo - Mercury
            6: swe.VENUS,  # Libra - Venus
            7: swe.MARS,   # Scorpio - Mars
            8: swe.JUPITER,# Sagittarius - Jupiter
            9: swe.SATURN, # Capricorn - Saturn
            10: swe.SATURN,# Aquarius - Saturn
            11: swe.JUPITER # Pisces - Jupiter
        }


        # Constants
        self.NAKSHATRA_NAMES = [
            "Ashwini", "Bharani", "Krittika", "Rohini", "Mrigashira", "Ardra",
            "Punarvasu", "Pushya", "Ashlesha", "Magha", "Purva Phalguni", 
            "Uttara Phalguni", "Hasta", "Chitra", "Swati", "Vishakha", 
            "Anuradha", "Jyeshtha", "Mula", "Purva Ashadha", "Uttara Ashadha",
            "Shravana", "Dhanishta", "Shatabhisha", "Purva Bhadrapada",
            "Uttara Bhadrapada", "Revati"
        ]
    
    
    def calculate_julian_day(self):
        """Convert the given date and time to Julian Day in UT."""
        date_parts = list(map(int, self.date.split('/')))
        time_parts = list(map(int, self.time.split(':')))
        
        # Parse timezone offset
        tz_str = self.timezone
        if tz_str.startswith('UTC'):
            # Remove 'UTC' prefix
            tz_str = tz_str[3:]
            # Split on colon to separate hours and minutes
            parts = tz_str.split(':')
            if len(parts) >= 2:
                sign = parts[0][0]
                hours = parts[0][1:]
                minutes = parts[1]
            else:
                sign = parts[0][0]
                hours = parts[0][1:]
                minutes = '00'
            tz_hours = int(hours)
            tz_minutes = int(minutes)
            tz_offset = (tz_hours + tz_minutes / 60.0) * (-1 if sign == '-' else 1)
        else:
            raise ValueError("Timezone must be in 'UTC±HH:MM' format.")
            
        # Create datetime object in local time
        dt = datetime.datetime(date_parts[2], date_parts[1], date_parts[0], 
                             time_parts[0], time_parts[1])
        # Convert to UT by subtracting timezone offset
        dt_ut = dt - datetime.timedelta(hours=tz_offset)
        self.julian_day = swe.julday(dt_ut.year, dt_ut.month, dt_ut.day, 
                                   dt_ut.hour + dt_ut.minute / 60.0)
    def calculate_ascendant(self):
        """Calculate the ascendant (Lagna) based on the place and time."""
        # Get latitude and longitude of the place (you can use a geocoding API for this)
        # For simplicity, we'll use New Delhi's coordinates
        lat, lon = 28.6139, 77.2090  # Latitude and longitude of New Delhi
        # swe.houses() returns a tuple where the first element is a tuple containing cusps
        # The second element is a tuple containing ascmc (ascendant, MC, ARMC, and vertex)
        houses_cusps, ascmc = swe.houses(self.julian_day, lat, lon, b'P')
        # ascmc[0] contains the ascendant value
        self.ascendant = float(ascmc[0])

    def calculate_planetary_positions(self):
        """Calculate the positions of planets in the sidereal zodiac."""
        # Set the sidereal mode (Lahiri Ayanamsa)
        swe.set_sid_mode(swe.SIDM_LAHIRI)
        planets = [swe.SUN, swe.MOON, swe.MARS, swe.MERCURY, swe.JUPITER, swe.VENUS, swe.SATURN, swe.MEAN_NODE]
        for planet in planets:
            pos, _ = swe.calc_ut(self.julian_day, planet)
            self.planetary_positions[planet] = pos[0]  # Position in degrees
        # Calculate Ketu (South Node) as 180 degrees from Rahu (North Node)
        rahu_pos = self.planetary_positions[swe.MEAN_NODE]
        ketu_pos = (rahu_pos + 180) % 360
        self.planetary_positions[swe.MEAN_NODE + 1] = ketu_pos

    def determine_houses(self):
        """Determine the house system (Whole Sign)."""
        if self.ascendant is None:
            raise ValueError("Ascendant must be calculated before determining houses")
        
        for house in range(12):
            self.houses[house + 1] = float((self.ascendant + 30 * house) % 360)


    def calculate_aspects(self):
        """Calculate aspects between planets."""
        planets = list(self.planetary_positions.keys())
        for i in range(len(planets)):
            for j in range(i + 1, len(planets)):
                planet1 = planets[i]
                planet2 = planets[j]
                angle = abs(self.planetary_positions[planet1] - self.planetary_positions[planet2]) % 360
                if angle == 0:
                    self.aspects.append((planet1, planet2, "Conjunction"))
                elif angle == 60:
                    self.aspects.append((planet1, planet2, "Sextile"))
                elif angle == 90:
                    self.aspects.append((planet1, planet2, "Square"))
                elif angle == 120:
                    self.aspects.append((planet1, planet2, "Trine"))
                elif angle == 180:
                    self.aspects.append((planet1, planet2, "Opposition"))

    def calculate_vimshottari_dasha(self):
        """Calculate Vimshottari Dasha periods."""
        # For simplicity, we'll use a basic calculation
        self.dasha_periods = [
            ("Venus", 20),
            ("Sun", 6),
            ("Moon", 7),
            ("Mars", 10),
            ("Rahu", 18),
            ("Jupiter", 16),
            ("Saturn", 19),
            ("Mercury", 17),
            ("Ketu", 7),
        ]

    def generate_kundli_chart(self):
        """Generate the Kundli chart."""
        self.calculate_julian_day()
        self.calculate_ascendant()
        self.calculate_planetary_positions()
        self.determine_houses()
        self.calculate_aspects()
        self.calculate_vimshottari_dasha()

    def get_descriptive_summary(self) -> str:
        """Generate a comprehensive descriptive summary of the Kundli."""
        planet_names = {
            swe.SUN: "Sun", swe.MOON: "Moon", swe.MARS: "Mars",
            swe.MERCURY: "Mercury", swe.JUPITER: "Jupiter",
            swe.VENUS: "Venus", swe.SATURN: "Saturn",
            swe.MEAN_NODE: "Rahu", swe.MEAN_NODE + 1: "Ketu"
        }

        rashi_names = [
            "Mesha", "Vrishabha", "Mithuna", "Karka",
            "Simha", "Kanya", "Tula", "Vrishchika",
            "Dhanu", "Makara", "Kumbha", "Meena"
        ]

        def get_rashi(degree):
            return rashi_names[int(degree / 30)]

        def format_degree(degree):
            rashi_deg = degree % 30
            return f"{int(rashi_deg)}°{int((rashi_deg % 1) * 60)}'"

        summary = [
            "BIRTH DETAILS",
            f"Date: {self.date} , Time: {self.time} , Place: {self.place}, Gender: {self.gender}",
            "LAGNA / ASCENDANT",
            f"Ascendant: {get_rashi(self.ascendant)} ({format_degree(self.ascendant)})",
            f"Nakshatra: {self.calculate_nakshatra(self.ascendant)['nakshatra']}, Pada: {self.calculate_nakshatra(self.ascendant)['pada']}",
            "",
            # "PLANETARY POSITIONS",
            # "──────────────────"
        ]

        # Planetary positions with detailed information
        # for planet, pos in self.planetary_positions.items():
        #     nakshatra_info = self.calculate_nakshatra(pos)
        #     house_num = self.get_planet_house(planet)
            
        #     planet_info = [
        #         f"\n{planet_names[planet]}:",
        #         f"  • Rashi: {get_rashi(pos)} ({format_degree(pos)})",
        #         f"  • House: {house_num}",
        #         f"  • Nakshatra: {nakshatra_info['nakshatra']}, Pada: {nakshatra_info['pada']}",
        #         f"  • Degrees in Nakshatra: {nakshatra_info['degrees_traversed']:.2f}°"
        #     ]
        #     summary.extend(planet_info)

        summary.extend([
            "DIVISIONAL CHARTS (VARGA)",
        ])

        # Important divisional charts
        important_vargas = ['D9', 'D10', 'D12', 'D24', 'D60']
        varga_names = {
            'D9': 'Navamsa (Marriage/Dharma)',
            'D10': 'Dasamsa (Career)',
            'D12': 'Dwadasamsa (Parents/Ancestors)',
            'D24': 'Chaturvimshamsa (Education/Learning)',
            'D60': 'Shastiamsa (General Results)'
        }

        for varga in important_vargas:
            summary.append(f"\n{varga_names[varga]}:")
            for planet in self.planetary_positions:
                pos = self.divisional_charts[planet][varga]
                summary.append(f"  • {planet_names[planet]}: {get_rashi(pos)} ({format_degree(pos)})")

        summary.extend([
            "YOGAS PRESENT",
            ])

        if self.yogas:
            for yoga in self.yogas:
                summary.append(f"• {yoga}")
        else:
            summary.append("No major yogas detected")

        summary.extend([
            "DASHA PERIODS"
        ])

        for dasha, years in self.dasha_periods:
            summary.append(f"• {dasha}: {years} years")

        summary.extend([
            "PLANETARY ASPECTS"
        ])

        aspect_types = {
            0: "Conjunction",
            60: "Sextile",
            90: "Square",
            120: "Trine",
            180: "Opposition"
        }

        for aspect in self.aspects:
            planet1, planet2, aspect_type = aspect
            summary.append(f"• {planet_names[planet1]} {aspect_type} {planet_names[planet2]}")

        

        return "\n".join(summary)

    def calculate_nakshatra(self, longitude: float) -> Dict:
        """Calculate Nakshatra position for given longitude."""
        nakshatra_degree = 13 + (20/60)  # 13°20'
        nakshatra_number = int(longitude / nakshatra_degree)
        pada = int((longitude % nakshatra_degree) / (nakshatra_degree/4)) + 1
        
        return {
            'nakshatra': self.NAKSHATRA_NAMES[nakshatra_number],
            'pada': pada,
            'degrees_traversed': longitude % nakshatra_degree
        }

    def calculate_divisional_chart(self, longitude: float, division: int) -> float:
        """Calculate position in divisional chart (D-charts)."""
        sign = int(longitude / 30)
        degree_in_sign = longitude % 30
        division_size = 30 / division
        division_number = int(degree_in_sign / division_size)
        new_sign = (sign * division + division_number) % 12
        return new_sign * 30 + (degree_in_sign % division_size) * division

    def calculate_all_divisional_charts(self):
        """Calculate positions for important divisional charts."""
        important_divisions = {
            'D1': 1,    # Rashi (Birth chart)
            'D2': 2,    # Hora (Wealth)
            'D3': 3,    # Drekkana (Siblings)
            'D4': 4,    # Chaturthamsa (Fortune)
            'D7': 7,    # Saptamsa (Children)
            'D9': 9,    # Navamsa (Spouse)
            'D10': 10,  # Dasamsa (Career)
            'D12': 12,  # Dwadasamsa (Parents)
            'D16': 16,  # Shodasamsa (Vehicles)
            'D20': 20,  # Vimshamsa (Spiritual)
            'D24': 24,  # Chaturvimshamsa (Education)
            'D27': 27,  # Saptavimshamsa (Strength)
            'D30': 30,  # Trimshamsa (Misfortune)
            'D40': 40,  # Khavedamsa (Auspicious effects)
            'D45': 45,  # Akshavedamsa (General indications)
            'D60': 60   # Shashtyamsa (All-round results)
        }

        for planet, pos in self.planetary_positions.items():
            self.divisional_charts[planet] = {}
            for chart_name, division in important_divisions.items():
                self.divisional_charts[planet][chart_name] = self.calculate_divisional_chart(pos, division)

    def calculate_shad_bala(self) -> Dict:
        """Calculate Shad Bala (six-fold strength) of planets."""
        strengths = {}
        for planet in self.planetary_positions:
            # Simplified calculation - in reality this is much more complex
            strengths[planet] = {
                'sthana_bala': self.calculate_positional_strength(planet),
                'dig_bala': self.calculate_directional_strength(planet),
                'kala_bala': self.calculate_temporal_strength(planet),
                'naisargika_bala': self.calculate_natural_strength(planet),
                'chesta_bala': self.calculate_motional_strength(planet),
                'drik_bala': self.calculate_aspectual_strength(planet)
            }
        return strengths

    def get_house_lord(self, house_number: int) -> int:
        """Get the lord of a specific house."""
        # Convert house number to zodiac sign (0-11)
        house_sign = int((self.ascendant + (house_number - 1) * 30) / 30) % 12
        return self.sign_lords[house_sign]

    def get_planet_house(self, planet: int) -> int:
        """Get the house number where a planet is located."""
        planet_pos = self.planetary_positions[planet]
        for house_num, house_start in self.houses.items():
            house_end = (house_start + 30) % 360
            if house_start <= planet_pos < house_end:
                return house_num
        return 1  # Default to first house if not found

    def is_planet_in_house(self, planet: int, house_number: int) -> bool:
        """Check if a planet is in a specific house."""
        return self.get_planet_house(planet) == house_number

    def calculate_positional_strength(self, planet: int) -> float:
        """Calculate Sthana Bala (positional strength)."""
        # Simplified calculation
        house_num = self.get_planet_house(planet)
        # Planets are strong in angles (1,4,7,10)
        if house_num in [1, 4, 7, 10]:
            return 1.0
        # Planets are moderate in trines (5,9)
        elif house_num in [5, 9]:
            return 0.75
        # Planets are weak in 6,8,12
        elif house_num in [6, 8, 12]:
            return 0.25
        return 0.5

    def calculate_directional_strength(self, planet: int) -> float:
        """Calculate Dig Bala (directional strength)."""
        house_num = self.get_planet_house(planet)
        # Simplified directional strength
        return 0.5  # Placeholder

    def calculate_temporal_strength(self, planet: int) -> float:
        """Calculate Kala Bala (temporal strength)."""
        # Simplified temporal strength
        return 0.5  # Placeholder

    def calculate_natural_strength(self, planet: int) -> float:
        """Calculate Naisargika Bala (natural strength)."""
        # Natural strengths of planets
        natural_strengths = {
            swe.SUN: 0.6,
            swe.MOON: 0.5,
            swe.MARS: 0.7,
            swe.MERCURY: 0.4,
            swe.JUPITER: 0.8,
            swe.VENUS: 0.5,
            swe.SATURN: 0.3
        }
        return natural_strengths.get(planet, 0.5)

    def calculate_motional_strength(self, planet: int) -> float:
        """Calculate Chesta Bala (motional strength)."""
        # Simplified motional strength
        return 0.5  # Placeholder

    def calculate_aspectual_strength(self, planet: int) -> float:
        """Calculate Drik Bala (aspectual strength)."""
        # Simplified aspect strength
        return 0.5  # Placeholder

    

    def check_yogas(self) -> List[str]:
        """Check for presence of major Yogas."""
        yogas = []
        
        # Raja Yoga (Lords of Kendra and Trikona houses in mutual aspect)
        kendra_houses = [1, 4, 7, 10]
        trikona_houses = [1, 5, 9]
        
        # Dhana Yoga (2nd lord in a kendra)
        second_lord = self.get_house_lord(2)
        if any(self.is_planet_in_house(second_lord, house) for house in kendra_houses):
            yogas.append("Dhana Yoga")
        
        # Gajakesari Yoga (Jupiter and Moon in kendra from each other)
        moon_house = self.get_planet_house(swe.MOON)
        jupiter_house = self.get_planet_house(swe.JUPITER)
        if abs(moon_house - jupiter_house) % 3 == 0:
            yogas.append("Gajakesari Yoga")
        
        # Budha-Aditya Yoga (Sun and Mercury in same house)
        if self.get_planet_house(swe.SUN) == self.get_planet_house(swe.MERCURY):
            yogas.append("Budha-Aditya Yoga")
        
        return yogas

    
    def generate_full_analysis(self):
        """Generate complete horoscope analysis."""
        self.calculate_julian_day()
        self.calculate_ascendant()
        self.calculate_planetary_positions()
        self.determine_houses()
        self.calculate_aspects()
        self.calculate_vimshottari_dasha()
        self.calculate_all_divisional_charts()
        self.yogas = self.check_yogas()
        return self.get_descriptive_summary()
