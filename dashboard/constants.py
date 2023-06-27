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
