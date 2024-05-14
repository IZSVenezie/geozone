from PyQt5.QtWidgets import QDialog, QVBoxLayout, QLabel, QLineEdit, QGroupBox, QFormLayout, QDialogButtonBox, QComboBox, QDateEdit, QCheckBox
from PyQt5.QtCore import Qt
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QDate

class GeoZoneEditDialog(QDialog):
    def __init__(self, layer, feature, existing_attributes_dict, parent=None):
        super(GeoZoneEditDialog, self).__init__(parent)
        self.layer = layer
        self.feature = feature
        self.existing_attributes_dict = existing_attributes_dict
        self.init_ui()
        self.validate_fields()  # Initial validation check

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

        # Group "measures" label and fields
        measures_group_box = QGroupBox("Measures")
        measures_layout = QFormLayout()
        measures_group_box.setLayout(measures_layout)
        layout.addWidget(measures_group_box)

        group_counters = {'general': 0, 'species': 0, 'measures': 0}

        label_dict = {
            "countryf": "Country from *",
            "localid": "Local ID *",
            "geoname": "Geographical name",
            "accuracy": "Accuracy",
            "zonetype": "Zone type *",
            "subtype": "Zone subtype",
            "status": "Zone status",
            "disease": "Disease *",
            "datebegin": "From *",
            "dateend": "To",
            "s_avian": "Avian species",
            "s_bee": "Bees",
            "s_bovine": "Bovines",
            "s_equine": "Equines",
            "s_lago": "Lagomorphs",
            "s_sh_go": "Sheeps/Goats",
            "s_swine": "Swines",
            "s_other": "Other species",
            "s_wild": "Wild species",
            "m_dest": "Official destruction of animal products",
            "m_surv_w": "Surveillance within the restricted zone",
            "m_surv_o": "Surveillance outside the restricted zone",
            "m_trace": "Traceability",
            "m_stpout": "Stamping out",
            "m_zoning": "Zoning",
            "m_movctrl": "Movement control",
            "m_quarant": "Quarantine",
            "m_vectctrl": "Vector surveillance",
            "m_selkill": "Selective killing and disposal",
            "m_screen": "Screening",
            "m_vacc": "Vaccination during outbreak(s)"

        }

        for field in self.feature.fields():
            if field.name() not in ['optype', 'uuid']:
                label = QLabel(label_dict[field.name()])

                if field.name() in ["localid", "geoname"]:
                    line_edit = QLineEdit(str(self.feature[field.name()]))
                    line_edit.setMaxLength(50)
                    if self.existing_attributes_dict[field.name()] != None:
                        line_edit.setText(self.existing_attributes_dict[field.name()])
                    else:
                        line_edit.setText("")
                    group_layout = self._get_group_layout(field, general_layout, species_layout, measures_layout, group_counters)
                    group_layout.addRow(label, line_edit)
                    self.attribute_widgets[field.name()] = line_edit

                elif field.name() in ["datebegin", "dateend"]:
                    date_edit = QDateEdit()
                    date_edit.setCalendarPopup(True)

                    if field.name() == "dateend":
                        # Checkbox to enable/disable the "To" date
                        self.date_checkbox = QCheckBox("Specify End Date")
                        self.date_checkbox.setChecked(False)  # Default as not specified
                        date_edit.setEnabled(False)  # Disable by default
                        self.date_checkbox.toggled.connect(lambda checked, de=date_edit: de.setEnabled(checked))
                        group_layout = self._get_group_layout(field, general_layout, species_layout, measures_layout, group_counters)
                        group_layout.addRow(self.date_checkbox)
                        date_edit.setDate(QDate().currentDate())  

                    else:  # Handle "datebegin" field which must have a date
                        date_value = self.existing_attributes_dict.get(field.name())
                        # Attempt to convert directly if it's already a string, or use a default value
                        if isinstance(date_value, str):
                            converted_date = QDate.fromString(date_value, 'yyyy-MM-dd')
                            if converted_date.isValid():
                                date_edit.setDate(converted_date)
                            else:
                                date_edit.setDate(QDate.currentDate())
                        elif date_value is not None:
                            # Fall back to current date if conversion is not possible
                            date_edit.setDate(QDate.currentDate())
                        else:
                            date_edit.setDate(QDate.currentDate())

                    group_layout = self._get_group_layout(field, general_layout, species_layout, measures_layout, group_counters)
                    group_layout.addRow(label, date_edit)
                    self.attribute_widgets[field.name()] = date_edit

                else:
                    options = self._get_combo_box_options(field)
                    combo_box = QComboBox()
                    combo_box.addItems(options)
                    if self.existing_attributes_dict[field.name()] != None:
                        if field.name() in ["s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go", "s_swine", "s_other", "s_wild", "m_dest", "m_surv_w", "m_surv_o", "m_trace", "m_stpout", "m_zoning", "m_movctrl", "m_quarant", "m_vectctrl", "m_selkill", "m_screen", "m_vacc"]:
                            combo_box.setCurrentIndex(self.existing_attributes_dict[field.name()])
                        elif field.name() == "disease":
                            combo_box.setCurrentIndex(int(self.existing_attributes_dict[field.name()]) - 1)
                        elif field.name() == "accuracy":
                            accuracy = ["INACCURATE", "ACCURATE"]
                            position = accuracy.index(self.existing_attributes_dict[field.name()])
                            combo_box.setCurrentIndex(position)
                        elif field.name() == "status":
                            status = ["PROPOSED", "OFFICIALLY_RECOGNIZED", "NULL"]
                            position = status.index(self.existing_attributes_dict[field.name()])
                            combo_box.setCurrentIndex(position)
                        elif field.name() == "subtype":
                            subtype = ["NEGLIGIBLE_RISK", "CONTROLLED_RISK", "UNDETERMINED_RISK", "NULL"]
                            position = subtype.index(self.existing_attributes_dict[field.name()])
                            combo_box.setCurrentIndex(position)
                        elif field.name() == "zonetype":
                            zonetype = ["FREE", "CONTAINMENT", "INFECTED", "PROTECTION"]
                            position = zonetype.index(self.existing_attributes_dict[field.name()])
                            combo_box.setCurrentIndex(position)
                        elif field.name() == "countryf":
                            countryf = ["ABW", "AFG", "AGO", "AIA", "AND", "ARE", "ARG", "ARM", "ASM", "ATA", "ATF", "BRB", "ALB", "BFA", "BGD", "BGR", "BHR", "BHS", "BIH", "BRN", "BTN", "DMA", "IRL", "BLR", "BLZ", "BMU", "BOL", "BRA", "GBR", "ATG", "AUS", "AUT", "AZE", "BDI", "BEL", "BEN", "BVT", "BWA", "CAF", "CAN", "CCK", "ESP", "CEU", "CHE", "CHL", "CHN", "CIV", "CMR", "COD", "COG", "COK", "COL", "COM", "CPV", "CRI", "CUB", "CUW", "EST", "ETH", "FIN", "FJI", "FLK", "FRA", "FRO", "FSM", "GAB", "IND", "DJI", "CXR", "CYM", "CYP", "CZE", "DEU", "DNK", "DOM", "DZA", "ECU", "EGY", "ERI", "GEO", "GHA", "GMB", "GNB", "GNQ", "GRC", "GRD", "GIB", "GIN", "GLP", "GRL", "GTM", "GUF", "GUM", "GUY", "HKG", "HMD", "HND", "HRV", "HTI", "HUN", "IDN", "IOT", "IRN", "IRQ", "ISR", "JPN", "KAZ", "KEN", "KGZ", "KHM", "KIR", "KNA", "KOR", "KWT", "LAO", "LBN", "LBR", "LBY", "MHL", "MKD", "MLI", "MLT", "MMR", "ISL", "ITA", "JAM", "JOR", "LCA", "MEX", "LIE", "LKA", "LSO", "LTU", "LUX", "LVA", "MDV", "MEL", "PAN", "MAC", "MAR", "MCO", "MDA", "MDG", "MNE", "MNG", "MNP", "MOZ", "MRT", "MTQ", "MUS", "MWI", "MYS", "MYT", "NAM", "NCL", "PER", "PHL", "PLW", "PNG", "POL", "MSR", "NER", "NZL", "OMN", "PAK", "NFK", "NGA", "NIC", "NPL", "NRU", "PRI", "NIU", "NLD", "NOR", "PRK", "PRT", "PRY", "PSE", "PYF", "QAT", "REU", "ROU", "RUS", "RWA", "SAU", "SDN", "SEN", "SGP", "SGS", "SHN", "SLB", "SLE", "SLV", "SMR", "SOM", "PCN", "SPM", "SVK", "SVN", "SWE", "SWZ", "SYC", "SYR", "THA", "TJK", "TKL", "TKM", "TLS", "VGB", "SRB", "SSD", "STP", "SUR", "TCA", "TCD", "TGO", "UMI", "TON", "TTO", "TUN", "TUR", "TUV", "TWN", "TZA", "UGA", "UKR", "URY", "USA", "UZB", "VAT", "VCT", "VEN", "VIR", "VNM", "VUT", "WLF", "WSM", "YEM", "ZAF", "ZMB", "ZWE"]
                            position = countryf.index(self.existing_attributes_dict[field.name()])
                            combo_box.setCurrentIndex(position)
                    else:
                        combo_box.setCurrentIndex(0)
                    group_layout = self._get_group_layout(field, general_layout, species_layout, measures_layout, group_counters)
                    group_layout.addRow(label, combo_box)
                    self.attribute_widgets[field.name()] = combo_box

        # Add button box
        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.ok_button = self.button_box.button(QDialogButtonBox.Ok)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)
        layout.addWidget(self.button_box)

        # Set up validation connections
        for name, widget in self.attribute_widgets.items():
            if isinstance(widget, QLineEdit):
                widget.textChanged.connect(self.validate_fields)
            elif isinstance(widget, QComboBox):
                widget.currentIndexChanged.connect(self.validate_fields)



    def validate_fields(self):
        required_fields = ['localid', 'zonetype', 'datebegin', 'disease', 'countryf']
        all_filled = True
        for field in required_fields:
            widget = self.attribute_widgets.get(field)
            if isinstance(widget, QLineEdit):
                if not widget.text().strip():
                    all_filled = False
            elif isinstance(widget, QComboBox):
                if widget.currentIndex() == -1 or widget.currentText() == "":
                    all_filled = False
            elif isinstance(widget, QDateEdit):
                # Assume date is always filled, customize as needed
                pass
        self.ok_button.setEnabled(all_filled)



    def _get_group_layout(self, field, general_layout, species_layout, measures_layout, group_counters):
        if group_counters['general'] < 11:
            group_counters['general'] += 1
            return general_layout
        elif group_counters['species'] < 9:
            group_counters['species'] += 1
            return species_layout
        else:
            group_counters['measures'] += 1
            return measures_layout
        


    def _get_combo_box_options(self, field):
        if field.name() in ["s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go", "s_swine", "s_other", "s_wild", "m_dest", "m_surv_w", "m_surv_o", "m_trace", "m_stpout", "m_zoning", "m_movctrl", "m_quarant", "m_vectctrl", "m_selkill", "m_screen", "m_vacc"]:
            return ["NO", "YES"]
        elif field.name() == "disease":
            return ["Anthrax", "Bluetongue", "Brucellosis (Brucella abortus)", "Brucellosis (Brucella melitensis)", "Brucellosis (Brucella suis)", "Crimean Congo haemorrhagic fever", "Epizootic haemorrhagic disease", "Equine encephalomyelitis (Eastern)", "Foot and mouth disease", "Heartwater", "Infection with Aujeszky's disease virus", "Infection with Echinococcus granulosus", "Infection with Echinococcus multilocularis", "Infection with rabies virus", "Infection with Rift Valley fever virus", "Infection with rinderpest virus", "Infection with Trichinella spp.", "Japanese encephalitis", "New world screwworm (Cochliomyia hominivorax)", "Old world screwworm (Chrysomya bezziana)", "Paratuberculosis", "Q fever", "Surra (Trypanosoma evansi)", "Tularemia", "West Nile fever", "Bovine anaplasmosis", "Bovine babesiosis", "Bovine genital campylobacteriosis", "Bovine spongiform encephalopathy", "Bovine tuberculosis", "Bovine viral diarrhoea", "Enzootic bovine leukosis", "Haemorrhagic septicaemia", "Infectious bovine rhinotracheitis/infectious pustular vulvovaginitis", "Infection with Mycoplasma mycoides subsp. mycoides SC (Contagious bovine pleuropneumonia)", "Lumpy skin disease", "Theileriosis", "Trichomonosis", "Trypanosomosis (tsetse-transmitted)", "Caprine arthritis/encephalitis", "Contagious agalactia", "Contagious caprine pleuropneumonia", "Infection with Chlamydophila abortus (Enzootic abortion of ewes, ovine chlamydiosis)", "Infection with peste des petits ruminants virus", "Maedi-visna", "Nairobi sheep disease", "Ovine epididymitis (Brucella ovis)", "Salmonellosis (S. abortusovis)", "Scrapie", "Sheep pox and goat pox", "Contagious equine metritis", "Dourine", "Equine encephalomyelitis (Western)", "Equine infectious anaemia", "Equine influenza", "Equine piroplasmosis", "Glanders", "Infection with African horse sickness virus", "Infection with equid herpesvirus-1 (EHV-1)", "Infection with equine arteritis virus", "Venezuelan equine encephalomyelitis", "African swine fever", "Infection with classical swine fever virus", "Nipah virus encephalitis", "Porcine cysticercosis", "Porcine reproductive and respiratory syndrome", "Transmissible gastroenteritis", "Avian chlamydiosis", "Avian infectious bronchitis", "Avian infectious laryngotracheitis", "Avian mycoplasmosis (Mycoplasma gallisepticum)", "Avian mycoplasmosis (Mycoplasma synoviae)", "Duck virus hepatitis", "Fowl typhoid", "Infection with avian influenza viruses", "Infection with influenza A viruses of high pathogenicity in birds other than poultry including wild birds", "Infection with Newcastle disease virus", "Infectious bursal disease (Gumboro disease)", "Pullorum disease", "Turkey rhinotracheitis", "Myxomatosis", "Rabbit haemorrhagic disease", "Infection of honey bees with Melissococcus plutonius (European foulbrood)", "Infection of honey bees with Paenibacillus larvae (American foulbrood)", "Infestation of honey bees with Acarapis woodi", "Infestation of honey bees with Tropilaelaps spp.", "Infestation of honey bees with Varroa spp. (Varroosis)", "Infestation with Aethina tumida (Small hive beetle).", "Camelpox", "Leishmaniosis", "Epizootic haematopoietic necrosis", "Infection with Aphanomyces invadans (epizootic ulcerative syndrome)", "Infection with Gyrodactylus salaris", "Infection with HPR-deleted or HPR0 infectious salmon anaemia virus", "Infection with salmonid alphavirus", "Infectious haematopoietic necrosis", "Koi herpesvirus disease", "Red sea bream iridoviral disease", "Spring viraemia of carp", "Viral haemorrhagic septicaemia", "Infection with abalone herpesvirus", "Infection with Bonamia exitiosa", "Infection with Bonamia ostreae", "Infection with Marteilia refringens", "Infection with Perkinsus marinus", "Infection with Perkinsus olseni", "Infection with Xenohaliotis californiensis", "Infection with Batrachochytrium dendrobatidis", "Infection with ranavirus", "Crayfish plague (Aphanomyces astaci)", "Infection with Yellowhead virus", "Infectious hypodermal and haematopoietic necrosis", "Infectious myonecrosis", "Necrotising hepatopancreatitis", "Taura syndrome", "White spot disease", "White tail disease"]
        elif field.name() == "accuracy":
            return ["Inaccurate", "Accurate"]
        elif field.name() == "status":
            return ["Proposed", "Officially recognized", "NULL"]
        elif field.name() == "subtype":
            return ["BSE - Negligible risk", "BSE - Controlled risk", "BSE - Undetermined", "NULL"]
        elif field.name() == "zonetype":
            return ["Free zone", "Containment zone", "Infected zone", "Protection zone"]
        elif field.name() == "countryf":
            return ["Aruba", "Afghanistan", "Angola", "Anguilla", "Andorra", "United Arab Emirates", "Argentina", "Armenia", "American Samoa", "Antarctica", "French Southern Territories", "Barbados", "Albania", "Burkina Faso", "Bangladesh", "Bulgaria", "Bahrain", "Bahamas", "Bosnia and Herzegovina", "Brunei", "Bhutan", "Dominica", "Ireland", "Belarus", "Belize", "Bermuda", "Bolivia", "Brazil", "United Kingdom", "Antigua and Barbuda", "Australia", "Austria", "Azerbaijan", "Burundi", "Belgium", "Benin", "Bouvet Island", "Botswana", "Central African (Rep.)", "Canada", "Cocos (Keeling) Islands", "Spain", "Ceuta", "Switzerland", "Chile", "China (People's Rep. of)", "Cote D'Ivoire", "Cameroon", "Congo (Dem. Rep. of the)", "Congo (Rep. of the)", "Cook Islands", "Colombia", "Comoros", "Cabo verde", "Costa Rica", "Cuba", "CuraÃ§ao", "Estonia", "Ethiopia", "Finland", "Fiji", "Falkland Islands", "France", "Faeroe Islands", "Micronesia (Federated States of)", "Gabon", "India", "Djibouti", "Christmas Island", "Cayman Islands", "Cyprus", "Czech Republic", "Germany", "Denmark", "Dominican (Rep.)", "Algeria", "Ecuador", "Egypt", "Eritrea", "Georgia", "Ghana", "Gambia", "Guinea-Bissau", "Equatorial Guinea", "Greece", "Grenada", "Gibraltar", "Guinea", "Guadaloupe", "Greenland", "Guatemala", "French Guiana", "Guam", "Guyana", "Hong Kong", "Heard and McDonald Islands", "Honduras", "Croatia", "Haiti", "Hungary", "Indonesia", "British Indian Ocean Territory", "Iran", "Iraq", "Israel", "Japan", "Kazakhstan", "Kenya", "Kyrgyzstan", "Cambodia", "Kiribati", "St. Kitts and Nevis", "Korea (Rep. of)", "Kuwait", "Laos", "Lebanon", "Liberia", "Libya", "Marshall Islands", "Former Yug. Rep. of Macedonia", "Mali", "Malta", "Myanmar", "Iceland", "Italy", "Jamaica", "Jordan", "St. Lucia", "Mexico", "Liechtenstein", "Sri Lanka", "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Maldives", "Melilla", "Panama", "Macao", "Morocco", "Monaco", "Moldova", "Madagascar", "Montenegro", "Mongolia", "Northern Mariana Islands", "Mozambique", "Mauritania", "Martinique", "Mauritius", "Malawi", "Malaysia", "Mayotte", "Namibia", "New Caledonia", "Peru", "Philippines", "Palau", "Papua New Guinea", "Poland", "Montserrat", "Niger", "New Zealand", "Oman", "Pakistan", "Norfolk Island", "Nigeria", "Nicaragua", "Nepal", "Nauru", "Puerto Rico", "Niue", "Netherlands", "Norway", "Korea (Dem People's Rep. of)", "Portugal", "Paraguay", "Palestine", "French Polynesia", "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saudi Arabia", "Sudan", "Senegal", "Singapore", "South Georgia and the South Sandwich Islands", "St. Helena", "Solomon Islands", "Sierra Leone", "El Salvador", "San Marino", "Somalia", "Pitcairn Island", "St. Pierre and Miquelon", "Slovakia", "Slovenia", "Sweden", "Swaziland", "Seychelles", "Syria", "Thailand", "Tajikistan", "Tokelau", "Turkmenistan", "Timor-Leste", "British Virgin Islands", "Serbia", "South Sudan (Rep. of)", "Sao Tome and Principe", "Suriname", "Turks and Caicos Islands", "Chad", "Togo", "United States Minor Outlying Islands", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Tuvalu", "Chinese Taipei", "Tanzania", "Uganda", "Ukraine", "Uruguay", "United States of America", "Uzbekistan", "Vatican City", "St. Vincent and the Grenadines", "Venezuela", "US Virgin Islands", "Vietnam", "Vanuatu", "Wallis and Futuna Islands", "Samoa", "Yemen", "South Africa", "Zambia", "Zimbabwe"]
        else:
            return ["opt1", "opt2"]
        


    def get_edited_attributes(self):
        edited_attributes = {}


        for field_name, line_edit in self.attribute_widgets.items():
            if field_name in ["localid", "geoname"]:
                edited_attributes[field_name] = line_edit.text()
            elif field_name in ["datebegin", "dateend"]:
                if field_name == "dateend" and not self.date_checkbox.isChecked():
                    # Set the attribute to None or another placeholder for a null value
                    edited_attributes[field_name] = None
                else:
                    # Retrieve the date from the QDateEdit widget
                    qdate = line_edit.date()
                    # Convert QDate to a string or another format if necessary
                    if qdate.isValid():
                        edited_attributes[field_name] = qdate.toString("yyyy-MM-dd")
                    else:
                        edited_attributes[field_name] = None
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
                if line_edit.currentText() == "Inaccurate":
                    edited_attributes[field_name] = "INACCURATE"
                else:
                    edited_attributes[field_name] = "ACCURATE"
            elif field_name == "status":
                if line_edit.currentText() == "Proposed":
                    edited_attributes[field_name] = "PROPOSED"
                elif line_edit.currentText() == "Officially recognized":
                    edited_attributes[field_name] = "OFFICIALLY_RECOGNIZED"
                else:
                    edited_attributes[field_name] = None
            elif field_name == "subtype":
                if line_edit.currentText() == "BSE - Negligible risk":
                    edited_attributes[field_name] = "NEGLIGIBLE_RISK"
                elif line_edit.currentText() == "BSE - Controlled risk":
                    edited_attributes[field_name] = "CONTROLLED_RISK"
                elif line_edit.currentText() == "BSE - Undetermined":
                    edited_attributes[field_name] = "UNDETERMINED_RISK"
                else:
                    edited_attributes[field_name] = None
            elif field_name == "zonetype":
                if line_edit.currentText() == "Free zone":
                    edited_attributes[field_name] = "FREE"
                elif line_edit.currentText() == "Containment zone":
                    edited_attributes[field_name] = "CONTAINMENT"
                elif line_edit.currentText() == "Infected zone":
                    edited_attributes[field_name] = "INFECTED"
                else:
                    edited_attributes[field_name] = "PROTECTION"
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