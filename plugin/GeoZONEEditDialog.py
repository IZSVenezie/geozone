from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QGroupBox, QFormLayout, QDialogButtonBox, QComboBox, QDateEdit
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QDate

class GeoZONEEditDialog(QDialog):
    def __init__(self, layer, feature, parent=None):
        super(GeoZONEEditDialog, self).__init__(parent)
        self.layer = layer
        self.feature = feature
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.attribute_widgets = {}

        # Group "general" label and fields
        general_group_box = QGroupBox("General Zone Information")
        general_layout = QFormLayout()
        general_group_box.setLayout(general_layout)
        layout.addWidget(general_group_box)

        # Group "species" label and fields
        species_group_box = QGroupBox("Species")
        species_layout = QFormLayout()
        species_group_box.setLayout(species_layout)
        layout.addWidget(species_group_box)

        # Group "methodologies" label and fields
        methodologies_group_box = QGroupBox("Methodologies")
        methodologies_layout = QFormLayout()
        methodologies_group_box.setLayout(methodologies_layout)
        layout.addWidget(methodologies_group_box)

        group_counters = {'general': 0, 'species': 0, 'methodologies': 0}

        for field in self.feature.fields():
            if field.name() not in ['optype', 'uuid']:
                label = QLabel(field.name())

                if field.name() == "localid":
                    line_edit = QLineEdit(str(self.feature[field.name()]))
                    line_edit.setMaxLength(50)
                    group_layout = self._get_group_layout(field, general_layout, species_layout, methodologies_layout, group_counters)
                    group_layout.addRow(label, line_edit)
                    self.attribute_widgets[field.name()] = line_edit

                elif field.name() in ["datebegin", "dateend"]:
                    date_edit = QDateEdit()
                    date_edit.setCalendarPopup(True)
                    date_edit.setDate(QDate.currentDate())
                    group_layout = self._get_group_layout(field, general_layout, species_layout, methodologies_layout, group_counters)
                    group_layout.addRow(label, date_edit)
                    self.attribute_widgets[field.name()] = date_edit

                else:
                    options = self._get_combo_box_options(field)
                    combo_box = QComboBox()
                    combo_box.addItems(options)
                    group_layout = self._get_group_layout(field, general_layout, species_layout, methodologies_layout, group_counters)
                    group_layout.addRow(label, combo_box)
                    self.attribute_widgets[field.name()] = combo_box

        # Add button box
        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _get_group_layout(self, field, general_layout, species_layout, methodologies_layout, group_counters):
        if group_counters['general'] < 9:
            group_counters['general'] += 1
            return general_layout
        elif group_counters['species'] < 9:
            group_counters['species'] += 1
            return species_layout
        else:
            group_counters['methodologies'] += 1
            return methodologies_layout

    def _get_combo_box_options(self, field):
        if field.name() in ["s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go", "s_swine", "s_other", "s_wild", "m_dest", "m_surv_w", "m_surv_o", "m_trace", "m_stpout", "m_zoning", "m_movctrl", "m_quarant", "m_vectctrl", "m_selkill", "m_screen", "m_vacc"]:
            return ["NO", "YES"]
        elif field.name() == "disease":
            return ["Anthrax", "Bluetongue", "Brucellosis (Brucella abortus)", "Brucellosis (Brucella melitensis)", "Brucellosis (Brucella suis)", "Crimean Congo haemorrhagic fever", "Epizootic haemorrhagic disease", "Equine encephalomyelitis (Eastern)", "Foot and mouth disease", "Heartwater", "Infection with Aujeszky's disease virus", "Infection with Echinococcus granulosus", "Infection with Echinococcus multilocularis", "Infection with rabies virus", "Infection with Rift Valley fever virus", "Infection with rinderpest virus", "Infection with Trichinella spp.", "Japanese encephalitis", "New world screwworm (Cochliomyia hominivorax)", "Old world screwworm (Chrysomya bezziana)", "Paratuberculosis", "Q fever", "Surra (Trypanosoma evansi)", "Tularemia", "West Nile fever", "Bovine anaplasmosis", "Bovine babesiosis", "Bovine genital campylobacteriosis", "Bovine spongiform encephalopathy", "Bovine tuberculosis", "Bovine viral diarrhoea", "Enzootic bovine leukosis", "Haemorrhagic septicaemia", "Infectious bovine rhinotracheitis/infectious pustular vulvovaginitis", "Infection with Mycoplasma mycoides subsp. mycoides SC (Contagious bovine pleuropneumonia)", "Lumpy skin disease", "Theileriosis", "Trichomonosis", "Trypanosomosis (tsetse-transmitted)", "Caprine arthritis/encephalitis", "Contagious agalactia", "Contagious caprine pleuropneumonia", "Infection with Chlamydophila abortus (Enzootic abortion of ewes, ovine chlamydiosis)", "Infection with peste des petits ruminants virus", "Maedi-visna", "Nairobi sheep disease", "Ovine epididymitis (Brucella ovis)", "Salmonellosis (S. abortusovis)", "Scrapie", "Sheep pox and goat pox", "Contagious equine metritis", "Dourine", "Equine encephalomyelitis (Western)", "Equine infectious anaemia", "Equine influenza", "Equine piroplasmosis", "Glanders", "Infection with African horse sickness virus", "Infection with equid herpesvirus-1 (EHV-1)", "Infection with equine arteritis virus", "Venezuelan equine encephalomyelitis", "African swine fever", "Infection with classical swine fever virus", "Nipah virus encephalitis", "Porcine cysticercosis", "Porcine reproductive and respiratory syndrome", "Transmissible gastroenteritis", "Avian chlamydiosis", "Avian infectious bronchitis", "Avian infectious laryngotracheitis", "Avian mycoplasmosis (Mycoplasma gallisepticum)", "Avian mycoplasmosis (Mycoplasma synoviae)", "Duck virus hepatitis", "Fowl typhoid", "Infection with avian influenza viruses", "Infection with influenza A viruses of high pathogenicity in birds other than poultry including wild birds", "Infection with Newcastle disease virus", "Infectious bursal disease (Gumboro disease)", "Pullorum disease", "Turkey rhinotracheitis", "Myxomatosis", "Rabbit haemorrhagic disease", "Infection of honey bees with Melissococcus plutonius (European foulbrood)", "Infection of honey bees with Paenibacillus larvae (American foulbrood)", "Infestation of honey bees with Acarapis woodi", "Infestation of honey bees with Tropilaelaps spp.", "Infestation of honey bees with Varroa spp. (Varroosis)", "Infestation with Aethina tumida (Small hive beetle).", "Camelpox", "Leishmaniosis", "Epizootic haematopoietic necrosis", "Infection with Aphanomyces invadans (epizootic ulcerative syndrome)", "Infection with Gyrodactylus salaris", "Infection with HPR-deleted or HPR0 infectious salmon anaemia virus", "Infection with salmonid alphavirus", "Infectious haematopoietic necrosis", "Koi herpesvirus disease", "Red sea bream iridoviral disease", "Spring viraemia of carp", "Viral haemorrhagic septicaemia", "Infection with abalone herpesvirus", "Infection with Bonamia exitiosa", "Infection with Bonamia ostreae", "Infection with Marteilia refringens", "Infection with Perkinsus marinus", "Infection with Perkinsus olseni", "Infection with Xenohaliotis californiensis", "Infection with Batrachochytrium dendrobatidis", "Infection with ranavirus", "Crayfish plague (Aphanomyces astaci)", "Infection with Yellowhead virus", "Infectious hypodermal and haematopoietic necrosis", "Infectious myonecrosis", "Necrotising hepatopancreatitis", "Taura syndrome", "White spot disease", "White tail disease"]
        elif field.name() == "accuracy":
            return ["INACCURATE", "ACCURATE"]
        elif field.name() == "status":
            return ["PROPOSED", "OFFICIALLY RECOGNIZED", "SELF DECLARATION"]
        elif field.name() == "subtype":
            return ["NEGLIGIBLE RISK", "CONTROLLED RISK"]
        elif field.name() == "zonetype":
            return ["FREE", "CONTAINMENT", "INFECTED", "PROTECTION"]
        elif field.name() == "countryf":
            return ["Aruba", "Afghanistan", "Angola", "Anguilla", "Andorra", "United Arab Emirates", "Argentina", "Armenia", "American Samoa", "Antarctica", "French Southern Territories", "Barbados", "Albania", "Burkina Faso", "Bangladesh", "Bulgaria", "Bahrain", "Bahamas", "Bosnia and Herzegovina", "Brunei", "Bhutan", "Dominica", "Ireland", "Belarus", "Belize", "Bermuda", "Bolivia", "Brazil", "United Kingdom", "Antigua and Barbuda", "Australia", "Austria", "Azerbaijan", "Burundi", "Belgium", "Benin", "Bouvet Island", "Botswana", "Central African (Rep.)", "Canada", "Cocos (Keeling) Islands", "Spain", "Ceuta", "Switzerland", "Chile", "China (People's Rep. of)", "Cote D'Ivoire", "Cameroon", "Congo (Dem. Rep. of the)", "Congo (Rep. of the)", "Cook Islands", "Colombia", "Comoros", "Cabo verde", "Costa Rica", "Cuba", "CuraÃ§ao", "Estonia", "Ethiopia", "Finland", "Fiji", "Falkland Islands", "France", "Faeroe Islands", "Micronesia (Federated States of)", "Gabon", "India", "Djibouti", "Christmas Island", "Cayman Islands", "Cyprus", "Czech Republic", "Germany", "Denmark", "Dominican (Rep.)", "Algeria", "Ecuador", "Egypt", "Eritrea", "Georgia", "Ghana", "Gambia", "Guinea-Bissau", "Equatorial Guinea", "Greece", "Grenada", "Gibraltar", "Guinea", "Guadaloupe", "Greenland", "Guatemala", "French Guiana", "Guam", "Guyana", "Hong Kong", "Heard and McDonald Islands", "Honduras", "Croatia", "Haiti", "Hungary", "Indonesia", "British Indian Ocean Territory", "Iran", "Iraq", "Israel", "Japan", "Kazakhstan", "Kenya", "Kyrgyzstan", "Cambodia", "Kiribati", "St. Kitts and Nevis", "Korea (Rep. of)", "Kuwait", "Laos", "Lebanon", "Liberia", "Libya", "Marshall Islands", "Former Yug. Rep. of Macedonia", "Mali", "Malta", "Myanmar", "Iceland", "Italy", "Jamaica", "Jordan", "St. Lucia", "Mexico", "Liechtenstein", "Sri Lanka", "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Maldives", "Melilla", "Panama", "Macao", "Morocco", "Monaco", "Moldova", "Madagascar", "Montenegro", "Mongolia", "Northern Mariana Islands", "Mozambique", "Mauritania", "Martinique", "Mauritius", "Malawi", "Malaysia", "Mayotte", "Namibia", "New Caledonia", "Peru", "Philippines", "Palau", "Papua New Guinea", "Poland", "Montserrat", "Niger", "New Zealand", "Oman", "Pakistan", "Norfolk Island", "Nigeria", "Nicaragua", "Nepal", "Nauru", "Puerto Rico", "Niue", "Netherlands", "Norway", "Korea (Dem People's Rep. of)", "Portugal", "Paraguay", "Palestine", "French Polynesia", "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saudi Arabia", "Sudan", "Senegal", "Singapore", "South Georgia and the South Sandwich Islands", "St. Helena", "Solomon Islands", "Sierra Leone", "El Salvador", "San Marino", "Somalia", "Pitcairn Island", "St. Pierre and Miquelon", "Slovakia", "Slovenia", "Sweden", "Swaziland", "Seychelles", "Syria", "Thailand", "Tajikistan", "Tokelau", "Turkmenistan", "Timor-Leste", "British Virgin Islands", "Serbia", "South Sudan (Rep. of)", "Sao Tome and Principe", "Suriname", "Turks and Caicos Islands", "Chad", "Togo", "United States Minor Outlying Islands", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Tuvalu", "Chinese Taipei", "Tanzania", "Uganda", "Ukraine", "Uruguay", "United States of America", "Uzbekistan", "Vatican City", "St. Vincent and the Grenadines", "Venezuela", "US Virgin Islands", "Vietnam", "Vanuatu", "Wallis and Futuna Islands", "Samoa", "Yemen", "South Africa", "Zambia", "Zimbabwe"]
        else:
            return ["opt1", "opt2"]

    def get_edited_attributes(self):
        edited_attributes = {}


        for field_name, line_edit in self.attribute_widgets.items():
            if field_name == "localid":
                edited_attributes[field_name] = line_edit.text()
            elif field_name in ["datebegin", "dateend"]:
                edited_attributes[field_name] = line_edit.date()
            elif field_name in ["s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go", "s_swine", "s_other", "s_wild", "m_dest", "m_surv_w", "m_surv_o", "m_trace", "m_stpout", "m_zoning", "m_movctrl", "m_quarant", "m_vectctrl", "m_selkill", "m_screen", "m_vacc"]:
                bit_val = 0
                if line_edit.currentText() == 'YES':
                    bit_val = 1
                edited_attributes[field_name] = bit_val
            elif field_name == "countryf":
                countries = ["Aruba", "Afghanistan", "Angola", "Anguilla", "Andorra", "United Arab Emirates", "Argentina", "Armenia", "American Samoa", "Antarctica", "French Southern Territories", "Barbados", "Albania", "Burkina Faso", "Bangladesh", "Bulgaria", "Bahrain", "Bahamas", "Bosnia and Herzegovina", "Brunei", "Bhutan", "Dominica", "Ireland", "Belarus", "Belize", "Bermuda", "Bolivia", "Brazil", "United Kingdom", "Antigua and Barbuda", "Australia", "Austria", "Azerbaijan", "Burundi", "Belgium", "Benin", "Bouvet Island", "Botswana", "Central African (Rep.)", "Canada", "Cocos (Keeling) Islands", "Spain", "Ceuta", "Switzerland", "Chile", "China (People's Rep. of)", "Cote D'Ivoire", "Cameroon", "Congo (Dem. Rep. of the)", "Congo (Rep. of the)", "Cook Islands", "Colombia", "Comoros", "Cabo verde", "Costa Rica", "Cuba", "CuraÃ§ao", "Estonia", "Ethiopia", "Finland", "Fiji", "Falkland Islands", "France", "Faeroe Islands", "Micronesia (Federated States of)", "Gabon", "India", "Djibouti", "Christmas Island", "Cayman Islands", "Cyprus", "Czech Republic", "Germany", "Denmark", "Dominican (Rep.)", "Algeria", "Ecuador", "Egypt", "Eritrea", "Georgia", "Ghana", "Gambia", "Guinea-Bissau", "Equatorial Guinea", "Greece", "Grenada", "Gibraltar", "Guinea", "Guadaloupe", "Greenland", "Guatemala", "French Guiana", "Guam", "Guyana", "Hong Kong", "Heard and McDonald Islands", "Honduras", "Croatia", "Haiti", "Hungary", "Indonesia", "British Indian Ocean Territory", "Iran", "Iraq", "Israel", "Japan", "Kazakhstan", "Kenya", "Kyrgyzstan", "Cambodia", "Kiribati", "St. Kitts and Nevis", "Korea (Rep. of)", "Kuwait", "Laos", "Lebanon", "Liberia", "Libya", "Marshall Islands", "Former Yug. Rep. of Macedonia", "Mali", "Malta", "Myanmar", "Iceland", "Italy", "Jamaica", "Jordan", "St. Lucia", "Mexico", "Liechtenstein", "Sri Lanka", "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Maldives", "Melilla", "Panama", "Macao", "Morocco", "Monaco", "Moldova", "Madagascar", "Montenegro", "Mongolia", "Northern Mariana Islands", "Mozambique", "Mauritania", "Martinique", "Mauritius", "Malawi", "Malaysia", "Mayotte", "Namibia", "New Caledonia", "Peru", "Philippines", "Palau", "Papua New Guinea", "Poland", "Montserrat", "Niger", "New Zealand", "Oman", "Pakistan", "Norfolk Island", "Nigeria", "Nicaragua", "Nepal", "Nauru", "Puerto Rico", "Niue", "Netherlands", "Norway", "Korea (Dem People's Rep. of)", "Portugal", "Paraguay", "Palestine", "French Polynesia", "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saudi Arabia", "Sudan", "Senegal", "Singapore", "South Georgia and the South Sandwich Islands", "St. Helena", "Solomon Islands", "Sierra Leone", "El Salvador", "San Marino", "Somalia", "Pitcairn Island", "St. Pierre and Miquelon", "Slovakia", "Slovenia", "Sweden", "Swaziland", "Seychelles", "Syria", "Thailand", "Tajikistan", "Tokelau", "Turkmenistan", "Timor-Leste", "British Virgin Islands", "Serbia", "South Sudan (Rep. of)", "Sao Tome and Principe", "Suriname", "Turks and Caicos Islands", "Chad", "Togo", "United States Minor Outlying Islands", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Tuvalu", "Chinese Taipei", "Tanzania", "Uganda", "Ukraine", "Uruguay", "United States of America", "Uzbekistan", "Vatican City", "St. Vincent and the Grenadines", "Venezuela", "US Virgin Islands", "Vietnam", "Vanuatu", "Wallis and Futuna Islands", "Samoa", "Yemen", "South Africa", "Zambia", "Zimbabwe"]
                selected_country = line_edit.currentText()
                position = countries.index(selected_country)
                country_acronyms = ["ABW", "AFG", "AGO", "AIA", "AND", "ARE", "ARG", "ARM", "ASM", "ATA", "ATF", "BRB", "ALB", "BFA", "BGD", "BGR", "BHR", "BHS", "BIH", "BRN", "BTN", "DMA", "IRL", "BLR", "BLZ", "BMU", "BOL", "BRA", "GBR", "ATG", "AUS", "AUT", "AZE", "BDI", "BEL", "BEN", "BVT", "BWA", "CAF", "CAN", "CCK", "ESP", "CEU", "CHE", "CHL", "CHN", "CIV", "CMR", "COD", "COG", "COK", "COL", "COM", "CPV", "CRI", "CUB", "CUW", "EST", "ETH", "FIN", "FJI", "FLK", "FRA", "FRO", "FSM", "GAB", "IND", "DJI", "CXR", "CYM", "CYP", "CZE", "DEU", "DNK", "DOM", "DZA", "ECU", "EGY", "ERI", "GEO", "GHA", "GMB", "GNB", "GNQ", "GRC", "GRD", "GIB", "GIN", "GLP", "GRL", "GTM", "GUF", "GUM", "GUY", "HKG", "HMD", "HND", "HRV", "HTI", "HUN", "IDN", "IOT", "IRN", "IRQ", "ISR", "JPN", "KAZ", "KEN", "KGZ", "KHM", "KIR", "KNA", "KOR", "KWT", "LAO", "LBN", "LBR", "LBY", "MHL", "MKD", "MLI", "MLT", "MMR", "ISL", "ITA", "JAM", "JOR", "LCA", "MEX", "LIE", "LKA", "LSO", "LTU", "LUX", "LVA", "MDV", "MEL", "PAN", "MAC", "MAR", "MCO", "MDA", "MDG", "MNE", "MNG", "MNP", "MOZ", "MRT", "MTQ", "MUS", "MWI", "MYS", "MYT", "NAM", "NCL", "PER", "PHL", "PLW", "PNG", "POL", "MSR", "NER", "NZL", "OMN", "PAK", "NFK", "NGA", "NIC", "NPL", "NRU", "PRI", "NIU", "NLD", "NOR", "PRK", "PRT", "PRY", "PSE", "PYF", "QAT", "REU", "ROU", "RUS", "RWA", "SAU", "SDN", "SEN", "SGP", "SGS", "SHN", "SLB", "SLE", "SLV", "SMR", "SOM", "PCN", "SPM", "SVK", "SVN", "SWE", "SWZ", "SYC", "SYR", "THA", "TJK", "TKL", "TKM", "TLS", "VGB", "SRB", "SSD", "STP", "SUR", "TCA", "TCD", "TGO", "UMI", "TON", "TTO", "TUN", "TUR", "TUV", "TWN", "TZA", "UGA", "UKR", "URY", "USA", "UZB", "VAT", "VCT", "VEN", "VIR", "VNM", "VUT", "WLF", "WSM", "YEM", "ZAF", "ZMB", "ZWE"]
                selected_acronym = country_acronyms[position]
                edited_attributes[field_name] = selected_acronym
            elif field_name == "accuracy":
                if line_edit.currentText() == "INACCURATE":
                    edited_attributes[field_name] = 1
                else:
                    edited_attributes[field_name] = 2
            elif field_name == "status":
                if line_edit.currentText() == "PROPOSED":
                    edited_attributes[field_name] = 1
                elif line_edit.currentText() == "OFFICIALY RECOGNIZED":
                    edited_attributes[field_name] = 2
                else:
                    edited_attributes[field_name] = 3
            elif field_name == "subtype":
                if line_edit.currentText() == "NEGLIGIBLE RISK":
                    edited_attributes[field_name] = 1
                else:
                    edited_attributes[field_name] = 2
            elif field_name == "zonetype":
                if line_edit.currentText() == "FREE":
                    edited_attributes[field_name] = 1
                elif line_edit.currentText() == "CONTAINMENT":
                    edited_attributes[field_name] = 2
                elif line_edit.currentText() == "INFECTED":
                    edited_attributes[field_name] = 3
                else:
                    edited_attributes[field_name] = 4
            elif field_name == "disease":
                diseases = ["Anthrax", "Bluetongue", "Brucellosis (Brucella abortus)", "Brucellosis (Brucella melitensis)", "Brucellosis (Brucella suis)", "Crimean Congo haemorrhagic fever", "Epizootic haemorrhagic disease", "Equine encephalomyelitis (Eastern)", "Foot and mouth disease", "Heartwater", "Infection with Aujeszky's disease virus", "Infection with Echinococcus granulosus", "Infection with Echinococcus multilocularis", "Infection with rabies virus", "Infection with Rift Valley fever virus", "Infection with rinderpest virus", "Infection with Trichinella spp.", "Japanese encephalitis", "New world screwworm (Cochliomyia hominivorax)", "Old world screwworm (Chrysomya bezziana)", "Paratuberculosis", "Q fever", "Surra (Trypanosoma evansi)", "Tularemia", "West Nile fever", "Bovine anaplasmosis", "Bovine babesiosis", "Bovine genital campylobacteriosis", "Bovine spongiform encephalopathy", "Bovine tuberculosis", "Bovine viral diarrhoea", "Enzootic bovine leukosis", "Haemorrhagic septicaemia", "Infectious bovine rhinotracheitis/infectious pustular vulvovaginitis", "Infection with Mycoplasma mycoides subsp. mycoides SC (Contagious bovine pleuropneumonia)", "Lumpy skin disease", "Theileriosis", "Trichomonosis", "Trypanosomosis (tsetse-transmitted)", "Caprine arthritis/encephalitis", "Contagious agalactia", "Contagious caprine pleuropneumonia", "Infection with Chlamydophila abortus (Enzootic abortion of ewes, ovine chlamydiosis)", "Infection with peste des petits ruminants virus", "Maedi-visna", "Nairobi sheep disease", "Ovine epididymitis (Brucella ovis)", "Salmonellosis (S. abortusovis)", "Scrapie", "Sheep pox and goat pox", "Contagious equine metritis", "Dourine", "Equine encephalomyelitis (Western)", "Equine infectious anaemia", "Equine influenza", "Equine piroplasmosis", "Glanders", "Infection with African horse sickness virus", "Infection with equid herpesvirus-1 (EHV-1)", "Infection with equine arteritis virus", "Venezuelan equine encephalomyelitis", "African swine fever", "Infection with classical swine fever virus", "Nipah virus encephalitis", "Porcine cysticercosis", "Porcine reproductive and respiratory syndrome", "Transmissible gastroenteritis", "Avian chlamydiosis", "Avian infectious bronchitis", "Avian infectious laryngotracheitis", "Avian mycoplasmosis (Mycoplasma gallisepticum)", "Avian mycoplasmosis (Mycoplasma synoviae)", "Duck virus hepatitis", "Fowl typhoid", "Infection with avian influenza viruses", "Infection with influenza A viruses of high pathogenicity in birds other than poultry including wild birds", "Infection with Newcastle disease virus", "Infectious bursal disease (Gumboro disease)", "Pullorum disease", "Turkey rhinotracheitis", "Myxomatosis", "Rabbit haemorrhagic disease", "Infection of honey bees with Melissococcus plutonius (European foulbrood)", "Infection of honey bees with Paenibacillus larvae (American foulbrood)", "Infestation of honey bees with Acarapis woodi", "Infestation of honey bees with Tropilaelaps spp.", "Infestation of honey bees with Varroa spp. (Varroosis)", "Infestation with Aethina tumida (Small hive beetle).", "Camelpox", "Leishmaniosis", "Epizootic haematopoietic necrosis", "Infection with Aphanomyces invadans (epizootic ulcerative syndrome)", "Infection with Gyrodactylus salaris", "Infection with HPR-deleted or HPR0 infectious salmon anaemia virus", "Infection with salmonid alphavirus", "Infectious haematopoietic necrosis", "Koi herpesvirus disease", "Red sea bream iridoviral disease", "Spring viraemia of carp", "Viral haemorrhagic septicaemia", "Infection with abalone herpesvirus", "Infection with Bonamia exitiosa", "Infection with Bonamia ostreae", "Infection with Marteilia refringens", "Infection with Perkinsus marinus", "Infection with Perkinsus olseni", "Infection with Xenohaliotis californiensis", "Infection with Batrachochytrium dendrobatidis", "Infection with ranavirus", "Crayfish plague (Aphanomyces astaci)", "Infection with Yellowhead virus", "Infectious hypodermal and haematopoietic necrosis", "Infectious myonecrosis", "Necrotising hepatopancreatitis", "Taura syndrome", "White spot disease", "White tail disease"]
                selected_disease = line_edit.currentText()
                position = diseases.index(selected_disease)
                diseases_codes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113, 114, 115, 116, 117]
                selected_code = diseases_codes[position]
                edited_attributes[field_name] = selected_code
            else: 
                edited_attributes[field_name] = line_edit.currentText()

        # Update the feature attributes
        for field_name, edited_value in edited_attributes.items():
            self.feature[field_name] = edited_value

        return edited_attributes