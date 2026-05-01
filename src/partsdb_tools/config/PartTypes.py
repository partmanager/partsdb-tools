part_types = {
    'Balun': {'subcategory': {}},
    'Battery': {'subcategory': {}},
    'Battery Holder': {'subcategory': {}},
    'Bolt': {'subcategory': {}},
    'Bridge Rectifier': {'subcategory': {}},
    'Common Mode Choke': {'subcategory': {}},
    'Capacitor': {
        'subcategory': {
            'Aluminium Electrolytic Capacitor': {'required_parameters': []},
            'MLCC': {'required_parameters': []},
        }
    },
    'Connector': {
        'required_parameters': [],
        'subcategory': {
            'Connector Bus': {'required_parameters': []},
            'Connector Accessory': {'required_parameters': []},
            'Connector IDC': {'required_parameters': []},
            'Connector Terminal Block': {'required_parameters': []},
            'Connector microSD Card': {'required_parameters': []},
            'Connector Pins': {'required_parameters': []}
        },
    },
    'Crystal': {
        'required_fields': [],
        'required_parameters': ['Frequency'],
        'subcategory': {}
    },
    'Crystal Oscillator': {'subcategory': {}},
    'Display': {
        'subcategory': {
            'LCD Display': {'required_parameters': []}
        }
    },
    'Diode': {
        'required_parameters': [],
        'subcategory': {
            'Schottky Diode': {'required_parameters': []},
            'Small Signal Diode': {'required_parameters': []},
            'Zener Diode': {'required_parameters': []},
            'LED': {'required_parameters': []},
            'TVS': {'required_parameters': []}
        }
    },
    'Enclosure': {'subcategory': {}},
    'Enclosure Accessory': {'subcategory': {}},
    'ESD Suppressor': {'subcategory': {}},
    'Fuse': {
        'subcategory': {
            'PTC Fuse': {'required_parameters': []}
        }
    },
    'IC': {
        'required_fields': ["description"],
        'required_parameters': [],
        'subcategory': {
            'IC Voltage Reference': {'required_parameters': []},
            'IC LDO': {'required_parameters': []},
            'IC Voltage Regulator': {'required_parameters': []},
            'IC Voltage Regulator Switching': {'required_parameters': []},
            'IC MCU': {'required_parameters': []},
            'IC Comparator': {'required_parameters': []},
            'IC Opamp': {'required_parameters': []},
            'IC Level translator': {'required_parameters': []},
            'IC Current Sense': {'required_parameters': []},
            'IC Load Switch': {'required_parameters': []},
            'IC RF Amplifier': {'required_parameters': []},
            'IC RF Synthesizer': {'required_parameters': []},
            'IC DAC': {'required_parameters': []},
            'IC ADC': {'required_parameters': []},
            'IC Sensor': {'required_parameters': []},
        }
    },
    'Inductor': {
        'subcategory': {
        }
    },
    'Lightpipe': {
        'required_fields': ["description"],
        'subcategory': {
        }
    },
    'Module': {
        'required_fields': ["description"],
        'subcategory': {}
    },
    'Resistor': {
        'subcategory': {
            'Resistor Thick Film': {'required_parameters': []},
            'Resistor Thin Film': {'required_parameters': []},
            'Resistor Array': {'required_parameters': []}
        }
    },
    'Relay': {'subcategory': {}},
    'Transistor': {
        'required_parameters': [],
        'subcategory': {
            'Transistor MOSFET P': {'required_parameters': []},
            'Transistor MOSFET N': {'required_parameters': []}
        }
    },
    'Surge arrester': {
        'subcategory': {}
    },
    'Switch': {
        'required_fields': ["description"],
        'subcategory': {}
    },
    'Varistor': {'subcategory': {}}
}