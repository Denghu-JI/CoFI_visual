valid_name = "__main__"
methods_path = "cofi/src/cofi/tools"
applications_path = "espresso/contrib"
problems_path = "cofi-examples/examples"
ignore_list = ['__init__.py', '_base_inference_tool.py']


legal_anzsrc_names = {
    37: {
        "Earth Sciences": {
            3701: "Atmospheric sciences",
            3702: "Climate change science",
            3703: "Geochemistry",
            3704: "Geoinformatics",
            3705: "Geology",
            3706: "Geophysics",
            3707: "Hydrology",
            3708: "Oceanography",
            3709: "Physical geography and environmental geoscience",
            3799: "Other earth sciences"
        }
    },
    3701: {
        "Atmospheric sciences": {
            370101: "Adverse weather events",
            370102: "Air pollution processes and air quality measurement",
            370103: "Atmospheric aerosols",
            370104: "Atmospheric composition, chemistry and processes",
            370105: "Atmospheric dynamics",
            370106: "Atmospheric radiation",
            370107: "Cloud physics",
            370108: "Meteorology",
            370109: "Tropospheric and stratospheric physics",
            370199: "Atmospheric sciences not elsewhere classified"
        }
    },
    3702: {
        "Climate change science": {
            370201: "Climate change processes",
            370202: "Climatology",
            370203: "Greenhouse gas inventories and fluxes",
            370299: "Climate change science not elsewhere classified"
        }
    },
    3703: {
        "Geochemistry": {
            370301: "Exploration geochemistry",
            370302: "Inorganic geochemistry",
            370303: "Isotope geochemistry",
            370304: "Organic geochemistry",
            370399: "Geochemistry not elsewhere classified"
        }
    },
    3704: {
        "Geoinformatics": {
            370401: "Computational modelling and simulation in earth sciences",
            370402: "Earth and space science informatics",
            370403: "Geoscience data visualisation",
            370499: "Geoinformatics not elsewhere classified"
        }
    },
    3705: {
        "Geology": {
            370501: "Biomineralisation",
            370502: "Geochronology",
            370503: "Igneous and metamorphic petrology",
            370504: "Marine geoscience",
            370505: "Mineralogy and crystallography",
            370506: "Palaeontology (incl. palynology)",
            370507: "Planetary geology",
            370508: "Resource geoscience",
            370509: "Sedimentology",
            370510: "Stratigraphy (incl. biostratigraphy, sequence stratigraphy and basin analysis)",
            370511: "Structural geology and tectonics",
            370512: "Volcanology",
            370599: "Geology not elsewhere classified"
        }
    },
    3706: {
        "Geophysics": {
            370601: "Applied geophysics",
            370602: "Electrical and electromagnetic methods in geophysics",
            370603: "Geodesy",
            370604: "Geodynamics",
            370605: "Geothermics and radiometrics",
            370606: "Gravimetrics",
            370607: "Magnetism and palaeomagnetism",
            370608: "Petrophysics and rock mechanics",
            370609: "Seismology and seismic exploration",
            370699: "Geophysics not elsewhere classified"
        }
    },
    3707: {
        "Hydrology": {
            370701: "Contaminant hydrology",
            370702: "Ecohydrology",
            370703: "Groundwater hydrology",
            370704: "Surface water hydrology",
            370705: "Urban hydrology",
            370799: "Hydrology not elsewhere classified"
        }
    },
    3708: {
        "Oceanography": {
            370801: "Biological oceanography",
            370802: "Chemical oceanography",
            370803: "Physical oceanography",
            370899: "Oceanography not elsewhere classified"
        }
    },
    3709: {
        "Physical geography and environmental geoscience": {
            370901: "Geomorphology and earth surface processes",
            370902: "Glaciology",
            370903: "Natural hazards",
            370904: "Palaeoclimatology",
            370905: "Quaternary environments",
            370906: "Regolith and landscape evolution",
            370999: "Physical geography and environmental geoscience not elsewhere classified"
        }
    },
    3799: {
        "Other earth sciences": {
            379901: "Earth system sciences",
            379999: "Other earth sciences not elsewhere classified"
        }
    }
}
    
    

# 370609 Seismology And Seismic Exploration -> Fast Marching Method

# legal_anzsrc_names = {
#     "37 Earth Sciences": {
#         "3701 Atmospheric sciences": {
#             "370101 Adverse weather events": {},
#             "370102 Air pollution processes and air quality measurement": {},
#             "370103 Atmospheric aerosols": {},
#             "370104 Atmospheric composition, chemistry and processes": {},
#             "370105 Atmospheric dynamics": {},
#             "370106 Atmospheric radiation": {},
#             "370107 Cloud physics": {},
#             "370108 Meteorology": {},
#             "370109 Tropospheric and stratospheric physics": {},
#             "370199 Atmospheric sciences not elsewhere classified": {}
#         },
#         "3702 Climate change science": {
#             "370201 Climate change processes": {},
#             "370202 Climatology": {},
#             "370203 Greenhouse gas inventories and fluxes": {},
#             "370299 Climate change science not elsewhere classified": {}
#         },
#         "3703 Geochemistry": {
#             "370301 Exploration geochemistry": {},
#             "370302 Inorganic geochemistry": {},
#             "370303 Isotope geochemistry": {},
#             "370304 Organic geochemistry": {},
#             "370399 Geochemistry not elsewhere classified": {}
#         },
#         "3704 Geoinformatics": {
#             "370401 Computational modelling and simulation in earth sciences": {},
#             "370402 Earth and space science informatics": {},
#             "370403 Geoscience data visualisation": {},
#             "370499 Geoinformatics not elsewhere classified": {}
#         },
#         "3705 Geology": {
#             "370501 Biomineralisation": {},
#             "370502 Geochronology": {},
#             "370503 Igneous and metamorphic petrology": {},
#             "370504 Marine geoscience": {},
#             "370505 Mineralogy and crystallography": {},
#             "370506 Palaeontology (incl. palynology)": {},
#             "370507 Planetary geology": {},
#             "370508 Resource geoscience": {},
#             "370509 Sedimentology": {},
#             "370510 Stratigraphy (incl. biostratigraphy, sequence stratigraphy and basin analysis)": {},
#             "370511 Structural geology and tectonics": {},
#             "370512 Volcanology": {},
#             "370599 Geology not elsewhere classified": {}
#         },
#         "3706 Geophysics": {
#             "370601 Applied geophysics": {},
#             "370602 Electrical and electromagnetic methods in geophysics": {},
#             "370603 Geodesy": {},
#             "370604 Geodynamics": {},
#             "370605 Geothermics and radiometrics": {},
#             "370606 Gravimetrics": {},
#             "370607 Magnetism and palaeomagnetism": {},
#             "370608 Petrophysics and rock mechanics": {},
#             "370609 Seismology and seismic exploration": {
#                 "Fast Marching Method": {}
#             },
#             "370699 Geophysics not elsewhere classified": {}
#         },
#         "3707 Hydrology": {
#             "370701 Contaminant hydrology": {},
#             "370702 Ecohydrology": {},
#             "370703 Groundwater hydrology": {},
#             "370704 Surface water hydrology": {},
#             "370705 Urban hydrology": {},
#             "370799 Hydrology not elsewhere classified": {}
#         },
#         "3708 Oceanography": {
#             "370801 Biological oceanography": {},
#             "370802 Chemical oceanography": {},
#             "370803 Physical oceanography": {},
#             "370899 Oceanography not elsewhere classified": {}
#         },
#         "3709 Physical geography and environmental geoscience": {
#             "370901 Geomorphology and earth surface processes": {},
#             "370902 Glaciology": {},
#             "370903 Natural hazards": {},
#             "370904 Palaeoclimatology": {},
#             "370905 Quaternary environments": {},
#             "370906 Regolith and landscape evolution": {},
#             "370999 Physical geography and environmental geoscience not elsewhere classified": {}
#         },
#         "3799 Other earth sciences": {
#             "379901 Earth system sciences": {},
#             "379999 Other earth sciences not elsewhere classified": {}
#         }
#     }
# }