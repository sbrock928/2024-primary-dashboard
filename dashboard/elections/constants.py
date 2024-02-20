from collections import OrderedDict

color_mapping_dict = dict(
    Trump="red",
    DeSantis="blue",
    Pence="green",
    Haley="goldenrod",
    Scott="magenta",
    Hutchinson="purple",
    Ramaswamy="yellow",
    Burgum="orange",
    Christie="teal",
    Undecided="gray",
)

states = OrderedDict()

# Initialize States and Delegate Counts
states["IA"] = {"Delegates": 40}
states["NH"] = {"Delegates": 22}
states["NV"] = {"Delegates": 26}
states["SC"] = {"Delegates": 50}
states["MI"] = {"Delegates": 55}
states["ID"] = {"Delegates": 32}
states["VI"] = {"Delegates": 9}
states["DC"] = {"Delegates": 19}
states["AK"] = {"Delegates": 28}
states["AR"] = {"Delegates": 40}
states["MN"] = {"Delegates": 39}
states["TN"] = {"Delegates": 58}
states["AL"] = {"Delegates": 49}
states["CA"] = {"Delegates": 169}
states["CO"] = {"Delegates": 37}
states["ME"] = {"Delegates": 20}
states["MA"] = {"Delegates": 40}
states["NC"] = {"Delegates": 75}
states["OK"] = {"Delegates": 43}
states["TX"] = {"Delegates": 162}
states["UT"] = {"Delegates": 40}
states["VT"] = {"Delegates": 17}
states["VA"] = {"Delegates": 48}
states["GU"] = {"Delegates": 9}
states["ND"] = {"Delegates": 29}
states["WY"] = {"Delegates": 29}
states["PR"] = {"Delegates": 23}
states["MP"] = {"Delegates": 9}
states["GA"] = {"Delegates": 59}
states["HI"] = {"Delegates": 19}
states["MS"] = {"Delegates": 39}
states["WA"] = {"Delegates": 43}
states["MO"] = {"Delegates": 54}
states["AZ"] = {"Delegates": 43}
states["FL"] = {"Delegates": 125}
states["IL"] = {"Delegates": 64}
states["OH"] = {"Delegates": 78}
states["KS"] = {"Delegates": 39}
states["AS"] = {"Delegates": 9}
states["LA"] = {"Delegates": 46}
states["NY"] = {"Delegates": 91}
states["RI"] = {"Delegates": 19}
states["WI"] = {"Delegates": 41}
states["DE"] = {"Delegates": 16}
states["PA"] = {"Delegates": 67}
states["CT"] = {"Delegates": 28}
states["IN"] = {"Delegates": 58}
states["MD"] = {"Delegates": 37}
states["NE"] = {"Delegates": 36}
states["WV"] = {"Delegates": 31}
states["KY"] = {"Delegates": 46}
states["OR"] = {"Delegates": 31}
states["MT"] = {"Delegates": 31}
states["NJ"] = {"Delegates": 49}
states["NM"] = {"Delegates": 22}
states["SD"] = {"Delegates": 29}

# State Order
state_order_list = [
    "IA",
    "NH",
    "NV",
    "SC",
    "MI",
    "ID",
    "VI",
    "DC",
    "AK",
    "AR",
    "MN",
    "TN",
    "AL",
    "CA",
    "CO",
    "ME",
    "MA",
    "NC",
    "OK",
    "TX",
    "UT",
    "VT",
    "VA",
    "GU",
    "ND",
    "WY",
    "PR",
    "MP",
    "GA",
    "HI",
    "MS",
    "WA",
    "MO",
    "AZ",
    "FL",
    "IL",
    "OH",
    "KS",
    "AS",
    "LA",
    "NY",
    "RI",
    "WI",
    "DE",
    "PA",
    "CT",
    "IN",
    "MD",
    "NE",
    "WV",
    "KY",
    "OR",
    "MT",
    "NJ",
    "NM",
    "SD",
]

electoral_votes = [
    9,
    3,
    11,
    6,
    54,
    10,
    7,
    3,
    3,
    30,
    16,
    4,
    4,
    19,
    11,
    6,
    6,
    8,
    8,
    4,
    10,
    11,
    15,
    10,
    6,
    10,
    4,
    5,
    6,
    4,
    14,
    5,
    28,
    16,
    3,
    17,
    7,
    8,
    19,
    4,
    9,
    3,
    11,
    40,
    6,
    3,
    13,
    12,
    4,
    10,
    3,
]

electoral_state_order = [
    "AL",
    "AK",
    "AZ",
    "AR",
    "CA",
    "CO",
    "CT",
    "DE",
    "DC",
    "FL",
    "GA",
    "HI",
    "ID",
    "IL",
    "IN",
    "IA",
    "KS",
    "KY",
    "LA",
    "ME",
    "MD",
    "MA",
    "MI",
    "MN",
    "MS",
    "MO",
    "MT",
    "NE",
    "NV",
    "NH",
    "NJ",
    "NM",
    "NY",
    "NC",
    "ND",
    "OH",
    "OK",
    "OR",
    "PA",
    "RI",
    "SC",
    "SD",
    "TN",
    "TX",
    "UT",
    "VT",
    "VA",
    "WA",
    "WV",
    "WI",
    "WY",
]


state_code_mapping = {
    "Alabama": "AL",
    "Alaska": "AK",
    "Arizona": "AZ",
    "Arkansas": "AR",
    "California": "CA",
    "Colorado": "CO",
    "Connecticut": "CT",
    "Delaware": "DE",
    "District of Columbia": "DC",
    "Florida": "FL",
    "Georgia": "GA",
    "Hawaii": "HI",
    "Idaho": "ID",
    "Illinois": "IL",
    "Indiana": "IN",
    "Iowa": "IA",
    "Kansas": "KS",
    "Kentucky": "KY",
    "Louisiana": "LA",
    "Maine": "ME",
    "Maryland": "MD",
    "Massachusetts": "MA",
    "Michigan": "MI",
    "Minnesota": "MN",
    "Mississippi": "MS",
    "Missouri": "MO",
    "Montana": "MT",
    "Nebraska": "NE",
    "Nevada": "NV",
    "New Hampshire": "NH",
    "New Jersey": "NJ",
    "New Mexico": "NM",
    "New York": "NY",
    "North Carolina": "NC",
    "North Dakota": "ND",
    "Ohio": "OH",
    "Oklahoma": "OK",
    "Oregon": "OR",
    "Pennsylvania": "PA",
    "Rhode Island": "RI",
    "South Carolina": "SC",
    "South Dakota": "SD",
    "Tennessee": "TN",
    "Texas": "TX",
    "Utah": "UT",
    "Vermont": "VT",
    "Virginia": "VA",
    "Washington": "WA",
    "West Virginia": "WV",
    "Wisconsin": "WI",
    "Wyoming": "WY",
}

candidate_names = {"Nikki Haley": "Haley", "Donald Trump": "Trump"}
import_columns = [
    "candidate",
    "date",
    "pct_estimate",
    "state",
    "pct_trend_adjusted",
    "cycle",
]
