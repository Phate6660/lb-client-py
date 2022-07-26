from colorama import Fore, Style
from shared_functions import StyleApplyer
import sys

argv_count: int = len(sys.argv)
# Missing first argument
if argv_count == 1:
    print("Please enter a username")
    sys.exit(1)
# Missing second argument
elif argv_count == 2:
    print("Please enter an operation")
    sys.exit(1)
# Arg 1: Username
user: str = sys.argv[1]
# Arg 2: Operation
op: str = sys.argv[2]

# URLs
base_url: str               = 'https://api.listenbrainz.org/1/'
"""The base url used for the API."""
stats_base_url: str         = 'https://api.listenbrainz.org/1/stats/'
"""The base url used for the stats API."""
user_url: str               = base_url       + '/user/'       + user + '/'
"""The base url for the user API."""
listening_url: str          = user_url       + 'playing-now'
"""The url for fetching the current song."""
listen_count_url: str       = user_url       + 'listen-count'
"""The url for fetching the total listen count."""
listens_url: str            = user_url       + 'listens'
similar_users_url: str      = user_url       + '/similar-users'
artist_map_url: str         = stats_base_url + 'user/' + user + '/artist-map'
top_tracks_url: str         = stats_base_url + 'user/' + user + '/recordings'
top_releases_url: str       = stats_base_url + 'user/' + user + '/releases'
top_artists_url: str        = stats_base_url + 'user/' + user + '/artists'
listening_activity_url: str = stats_base_url + 'user/' + user + '/listening-activity'
daily_activity_url: str     = stats_base_url + 'user/' + user + '/daily-activity'

# Define the colors to use for the various styles
LightWhite = StyleApplyer(Fore.LIGHTWHITE_EX, Style.BRIGHT)
"""Light white color with bold."""
LightBlack = StyleApplyer(Fore.LIGHTBLACK_EX, Style.BRIGHT)
"""Light black (essentially grey) color with bold."""
LightCyan  = StyleApplyer(Fore.LIGHTCYAN_EX,  Style.BRIGHT)
"""Light cyan color with bold."""
LightGreen = StyleApplyer(Fore.LIGHTGREEN_EX, Style.BRIGHT)
"""Light green color with bold."""
Green      = StyleApplyer(Fore.GREEN,         Style.BRIGHT)
"""Green color with bold."""
Red        = StyleApplyer(Fore.RED,           Style.BRIGHT)
"""Red color with bold."""
Yellow     = StyleApplyer(Fore.YELLOW,        Style.BRIGHT)
"""Yellow color with bold."""
White      = StyleApplyer(Fore.WHITE,         Style.BRIGHT)
"""White color with bold."""

country_codes: dict = {
    "ABW": "Aruba",
    "AFG": "Afghanistan",
    "AGO": "Angola",
    "AIA": "Anguilla",
    "ALA": "Åland Islands",
    "ALB": "Albania",
    "AND": "Andorra",
    "ARE": "United Arab Emirates",
    "ARG": "Argentina",
    "ARM": "Armenia",
    "ASM": "American Samoa",
    "ATA": "Antarctica",
    "ATF": "French Southern Territories",
    "ATG": "Antigua and Barbuda",
    "AUS": "Australia",
    "AUT": "Austria",
    "AZE": "Azerbaijan",
    "BDI": "Burundi",
    "BEL": "Belgium",
    "BEN": "Benin",
    "BES": "Bonaire, Sint Eustatius and Saba",
    "BFA": "Burkina Faso",
    "BGD": "Bangladesh",
    "BGR": "Bulgaria",
    "BHR": "Bahrain",
    "BHS": "Bahamas",
    "BIH": "Bosnia and Herzegovina",
    "BIN": "Burundi",
    "BLM": "Saint Barthélemy",
    "BLR": "Belarus",
    "BLZ": "Belize",
    "BMU": "Bermuda",
    "BOL": "Bolivia, Plurinational State of",
    "BRA": "Brazil",
    "BRB": "Barbados",
    "BRN": "Brunei Darussalam",
    "BTN": "Bhutan",
    "BVT": "Bouvet Island",
    "BWA": "Botswana",
    "CAF": "Central African Republic",
    "CAN": "Canada",
    "CCK": "Cocos (Keeling) Islands",
    "CHE": "Switzerland",
    "CHL": "Chile",
    "CHN": "China",
    "CIV": "Côte d'Ivoire",
    "CMR": "Cameroon",
    "COD": "Congo, the Democratic Republic of the",
    "COG": "Congo",
    "COK": "Cook Islands",
    "COL": "Colombia",
    "COM": "Comoros",
    "CPV": "Cabo Verde",
    "CRI": "Costa Rica",
    "CUB": "Cuba",
    "CUW": "Curaçao",
    "CXR": "Christmas Island",
    "CYM": "Cayman Islands",
    "CYP": "Cyprus",
    "CZE": "Czech Republic",
    "DEU": "Germany",
    "DJI": "Djibouti",
    "DMA": "Dominica",
    "DNK": "Denmark",
    "DOM": "Dominican Republic",
    "DZA": "Algeria",
    "ECU": "Ecuador",
    "EGY": "Egypt",
    "ERI": "Eritrea",
    "ESH": "Western Sahara",
    "ESP": "Spain",
    "EST": "Estonia",
    "ETH": "Ethiopia",
    "FIN": "Finland",
    "FJI": "Fiji",
    "FLK": "Falkland Islands (Malvinas)",
    "FRA": "France",
    "FRO": "Faroe Islands",
    "FSM": "Micronesia, Federated States of",
    "GAB": "Gabon",
    "GBR": "United Kingdom",
    "GEO": "Georgia",
    "GGY": "Guernsey",
    "GHA": "Ghana",
    "GIB": "Gibraltar",
    "GIN": "Guinea",
    "GLP": "Guadeloupe",
    "GMB": "Gambia",
    "GNB": "Guinea-Bissau",
    "GNQ": "Equatorial Guinea",
    "GRC": "Greece",
    "GRD": "Grenada",
    "GRL": "Greenland",
    "GTM": "Guatemala",
    "GUF": "French Guiana",
    "GUM": "Guam",
    "GUY": "Guyana",
    "HKG": "Hong Kong",
    "HMD": "Heard Island and McDonald Islands",
    "HND": "Honduras",
    "HRV": "Croatia",
    "HTI": "Haiti",
    "HUN": "Hungary",
    "IDN": "Indonesia",
    "IMN": "Isle of Man",
    "IND": "India",
    "IOT": "British Indian Ocean Territory",
    "IRL": "Ireland",
    "IRN": "Iran",
    "IRQ": "Iraq",
    "ISL": "Iceland",
    "ISR": "Israel",
    "ITA": "Italy",
    "JAM": "Jamaica",
    "JEY": "Jersey",
    "JOR": "Jordan",
    "JPN": "Japan",
    "KAZ": "Kazakhstan",
    "KEN": "Kenya",
    "KGZ": "Kyrgyzstan",
    "KHM": "Cambodia",
    "KIR": "Kiribati",
    "KNA": "Saint Kitts and Nevis",
    "KOR": "Korea",
    "KWT": "Kuwait",
    "LAO": "Lao People's Democratic Republic",
    "LBN": "Lebanon",
    "LBR": "Liberia",
    "LBY": "Libya",
    "LCA": "Saint Lucia",
    "LIE": "Liechtenstein",
    "LKA": "Sri Lanka",
    "LSO": "Lesotho",
    "LTU": "Lithuania",
    "LUX": "Luxembourg",
    "LVA": "Latvia",
    "MAC": "Macao",
    "MAF": "Saint Martin",
    "MAR": "Morocco",
    "MCO": "Monaco",
    "MDA": "Moldova",
    "MDG": "Madagascar",
    "MDV": "Maldives",
    "MEX": "Mexico",
    "MHL": "Marshall Islands",
    "MKD": "Macedonia",
    "MLI": "Mali",
    "MLT": "Malta",
    "MMR": "Myanmar",
    "MNE": "Montenegro",
    "MNG": "Mongolia",
    "MNP": "Northern Mariana Islands",
    "MOZ": "Mozambique",
    "MRT": "Mauritania",
    "MSR": "Montserrat",
    "MTQ": "Martinique",
    "MUS": "Mauritius",
    "MWI": "Malawi",
    "MYS": "Malaysia",
    "MYT": "Mayotte",
    "NAM": "Namibia",
    "NCL": "New Caledonia",
    "NER": "Niger",
    "NFK": "Norfolk Island",
    "NGA": "Nigeria",
    "NIC": "Nicaragua",
    "NIU": "Niue",
    "NLD": "Netherlands",
    "NOR": "Norway",
    "NPL": "Nepal",
    "NRU": "Nauru",
    "NZL": "New Zealand",
    "OMN": "Oman",
    "PAK": "Pakistan",
    "PAN": "Panama",
    "PCN": "Pitcairn",
    "PER": "Peru",
    "PHL": "Philippines",
    "PLW": "Palau",
    "PNG": "Papua New Guinea",
    "POL": "Poland",
    "PRI": "Puerto Rico",
    "PRK": "Korea, Democratic People's Republic of",
    "PRT": "Portugal",
    "PRY": "Paraguay",
    "PSE": "Palestine, State of",
    "PYF": "French Polynesia",
    "QAT": "Qatar",
    "REU": "Réunion",
    "ROU": "Romania",
    "RUS": "Russian Federation",
    "RWA": "Rwanda",
    "SAU": "Saudi Arabia",
    "SDN": "Sudan",
    "SEN": "Senegal",
    "SGP": "Singapore",
    "SGS": "South Georgia and the South Sandwich Islands",
    "SHN": "Saint Helena, Ascension and Tristan da Cunha",
    "SJM": "Svalbard and Jan Mayen",
    "SLB": "Solomon Islands",
    "SLE": "Sierra Leone",
    "SLV": "El Salvador",
    "SMR": "San Marino",
    "SOM": "Somalia",
    "SPM": "Saint Pierre and Miquelon",
    "SRB": "Serbia",
    "SSD": "South Sudan",
    "STP": "Sao Tome and Principe",
    "SUR": "Suriname",
    "SVK": "Slovakia",
    "SVN": "Slovenia",
    "SWE": "Sweden",
    "SWZ": "Swaziland",
    "SXM": "Sint Maarten (Dutch part)",
    "SYC": "Seychelles",
    "SYR": "Syrian Arab Republic",
    "TCA": "Turks and Caicos Islands",
    "TCD": "Chad",
    "TGO": "Togo",
    "THA": "Thailand",
    "TJK": "Tajikistan",
    "TKL": "Tokelau",
    "TKM": "Turkmenistan",
    "TLS": "Timor-Leste",
    "TON": "Tonga",
    "TTO": "Trinidad and Tobago",
    "TUN": "Tunisia",
    "TUR": "Turkey",
    "TUV": "Tuvalu",
    "TWN": "Taiwan, Province of China",
    "TZA": "Tanzania, United Republic of",
    "UGA": "Uganda",
    "UKR": "Ukraine",
    "UMI": "United States Minor Outlying Islands",
    "URY": "Uruguay",
    "USA": "United States",
    "UZB": "Uzbekistan",
    "VAT": "Holy See (Vatican City State)",
    "VCT": "Saint Vincent and the Grenadines",
    "VEN": "Venezuela, Bolivarian Republic of",
    "VGB": "Virgin Islands, British",
    "VIR": "Virgin Islands, U.S.",
    "VNM": "Viet Nam",
    "VUT": "Vanuatu",
    "WLF": "Wallis and Futuna",
    "WSM": "Samoa",
    "YEM": "Yemen",
    "ZAF": "South Africa",
    "ZMB": "Zambia",
    "ZWE": "Zimbabwe",
}
