from PyQt5.QtWidgets import QDialog, QGridLayout, QLabel, QLineEdit, QDialogButtonBox, QComboBox, QDateEdit
from qgis.core import QgsVectorLayer
from qgis.PyQt.QtCore import QDate

class GeoZONEEditDialog(QDialog):
    def __init__(self, layer, feature, parent=None):
        super(GeoZONEEditDialog, self).__init__(parent)
        self.layer = layer
        self.feature = feature
        self.init_ui()

    def init_ui(self):
        layout = QGridLayout(self)

        row = 0
        col = 0

        self.attribute_widgets = {}

        for field in self.feature.fields():
            if field.name() not in ['optype', 'uuid']:
                label = QLabel(field.name())

                if field.name() == "localid":
                    line_edit = QLineEdit(str(self.feature[field.name()])) #TEXTFIELD
                    line_edit.setMaxLength(50)
                    layout.addWidget(label, row, col)
                    layout.addWidget(line_edit, row, col + 1)
                    self.attribute_widgets[field.name()] = line_edit #TEXTFIELD       

                elif field.name() in ["datebegin", "dateend"]:
                    layout.addWidget(label, row, col)
                    date_edit = QDateEdit()
                    date_edit.setCalendarPopup(True)  # Enable calendar popup for easier date selection
                    date_edit.setDate(QDate.currentDate())  # Convert QVariant to QDateTime, then extract date
                    layout.addWidget(date_edit, row, col + 1)
                    # Store the QDateEdit object for date fields
                    self.attribute_widgets[field.name()] = date_edit 
                
                else:
                    options = []
                    combo_box = QComboBox()
                    layout.addWidget(label, row, col)
                    
                    if field.name() in ["s_avian", "s_bee", "s_bovine", "s_equine", "s_lago", "s_sh_go", "s_swine", "s_other", "s_wild", "m_dest", "m_surv_w", "m_surv_o", "m_trace", "m_stpout", "m_zoning", "m_movctrl", "m_quarant", "m_vectctrl", "m_selkill", "m_screen", "m_vacc"]:
                        options = ["NO", "YES"]

                    elif field.name() == "disease":
                        options = ["Anthrax", "Bluetongue", "Brucellosis (Brucella abortus)", "Brucellosis (Brucella melitensis)", "Brucellosis (Brucella suis)", "Crimean Congo haemorrhagic fever", "Epizootic haemorrhagic disease", "Equine encephalomyelitis (Eastern)", "Foot and mouth disease", "Heartwater", "Infection with Aujeszky's disease virus", "Infection with Echinococcus granulosus", "Infection with Echinococcus multilocularis", "Infection with rabies virus", "Infection with Rift Valley fever virus", "Infection with rinderpest virus", "Infection with Trichinella spp.", "Japanese encephalitis", "New world screwworm (Cochliomyia hominivorax)", "Old world screwworm (Chrysomya bezziana)", "Paratuberculosis", "Q fever", "Surra (Trypanosoma evansi)", "Tularemia", "West Nile fever", "Bovine anaplasmosis", "Bovine babesiosis", "Bovine genital campylobacteriosis", "Bovine spongiform encephalopathy", "Bovine tuberculosis", "Bovine viral diarrhoea", "Enzootic bovine leukosis", "Haemorrhagic septicaemia", "Infectious bovine rhinotracheitis/infectious pustular vulvovaginitis", "Infection with Mycoplasma mycoides subsp. mycoides SC (Contagious bovine pleuropneumonia)", "Lumpy skin disease", "Theileriosis", "Trichomonosis", "Trypanosomosis (tsetse-transmitted)", "Caprine arthritis/encephalitis", "Contagious agalactia", "Contagious caprine pleuropneumonia", "Infection with Chlamydophila abortus (Enzootic abortion of ewes, ovine chlamydiosis)", "Infection with peste des petits ruminants virus", "Maedi-visna", "Nairobi sheep disease", "Ovine epididymitis (Brucella ovis)", "Salmonellosis (S. abortusovis)", "Scrapie", "Sheep pox and goat pox", "Contagious equine metritis", "Dourine", "Equine encephalomyelitis (Western)", "Equine infectious anaemia", "Equine influenza", "Equine piroplasmosis", "Glanders", "Infection with African horse sickness virus", "Infection with equid herpesvirus-1 (EHV-1)", "Infection with equine arteritis virus", "Venezuelan equine encephalomyelitis", "African swine fever", "Infection with classical swine fever virus", "Nipah virus encephalitis", "Porcine cysticercosis", "Porcine reproductive and respiratory syndrome", "Transmissible gastroenteritis", "Avian chlamydiosis", "Avian infectious bronchitis", "Avian infectious laryngotracheitis", "Avian mycoplasmosis (Mycoplasma gallisepticum)", "Avian mycoplasmosis (Mycoplasma synoviae)", "Duck virus hepatitis", "Fowl typhoid", "Infection with avian influenza viruses", "Infection with influenza A viruses of high pathogenicity in birds other than poultry including wild birds", "Infection with Newcastle disease virus", "Infectious bursal disease (Gumboro disease)", "Pullorum disease", "Turkey rhinotracheitis", "Myxomatosis", "Rabbit haemorrhagic disease", "Infection of honey bees with Melissococcus plutonius (European foulbrood)", "Infection of honey bees with Paenibacillus larvae (American foulbrood)", "Infestation of honey bees with Acarapis woodi", "Infestation of honey bees with Tropilaelaps spp.", "Infestation of honey bees with Varroa spp. (Varroosis)", "Infestation with Aethina tumida (Small hive beetle).", "Camelpox", "Leishmaniosis", "Epizootic haematopoietic necrosis", "Infection with Aphanomyces invadans (epizootic ulcerative syndrome)", "Infection with Gyrodactylus salaris", "Infection with HPR-deleted or HPR0 infectious salmon anaemia virus", "Infection with salmonid alphavirus", "Infectious haematopoietic necrosis", "Koi herpesvirus disease", "Red sea bream iridoviral disease", "Spring viraemia of carp", "Viral haemorrhagic septicaemia", "Infection with abalone herpesvirus", "Infection with Bonamia exitiosa", "Infection with Bonamia ostreae", "Infection with Marteilia refringens", "Infection with Perkinsus marinus", "Infection with Perkinsus olseni", "Infection with Xenohaliotis californiensis", "Infection with Batrachochytrium dendrobatidis", "Infection with ranavirus", "Crayfish plague (Aphanomyces astaci)", "Infection with Yellowhead virus", "Infectious hypodermal and haematopoietic necrosis", "Infectious myonecrosis", "Necrotising hepatopancreatitis", "Taura syndrome", "White spot disease", "White tail disease"]
                        
                    elif field.name() == "accuracy":
                        options = ["INACCURATE", "ACCURATE"]
                    
                    elif field.name() == "status":
                        options = ["PROPOSED", "OFFICIALY RECOGNIZED"]
                    
                    elif field.name() == "subtype":
                        options = ["NEGLIGIBLE RISK", "CONTROLLED RISK"]

                    elif field.name() == "zonetype":
                        options = ["FREE", "CONTAINMENT", "INFECTED", "PROTECTION"]
                    
                    elif field.name() == "countryf":
                        options = ["Aruba", "Afghanistan", "Angola", "Anguilla", "Andorra", "United Arab Emirates", "Argentina", "Armenia", "American Samoa", "Antarctica", "French Southern Territories", "Barbados", "Albania", "Burkina Faso", "Bangladesh", "Bulgaria", "Bahrain", "Bahamas", "Bosnia and Herzegovina", "Brunei", "Bhutan", "Dominica", "Ireland", "Belarus", "Belize", "Bermuda", "Bolivia", "Brazil", "United Kingdom", "Antigua and Barbuda", "Australia", "Austria", "Azerbaijan", "Burundi", "Belgium", "Benin", "Bouvet Island", "Botswana", "Central African (Rep.)", "Canada", "Cocos (Keeling) Islands", "Spain", "Ceuta", "Switzerland", "Chile", "China (People's Rep. of)", "Cote D'Ivoire", "Cameroon", "Congo (Dem. Rep. of the)", "Congo (Rep. of the)", "Cook Islands", "Colombia", "Comoros", "Cabo verde", "Costa Rica", "Cuba", "CuraÃ§ao", "Estonia", "Ethiopia", "Finland", "Fiji", "Falkland Islands", "France", "Faeroe Islands", "Micronesia (Federated States of)", "Gabon", "India", "Djibouti", "Christmas Island", "Cayman Islands", "Cyprus", "Czech Republic", "Germany", "Denmark", "Dominican (Rep.)", "Algeria", "Ecuador", "Egypt", "Eritrea", "Georgia", "Ghana", "Gambia", "Guinea-Bissau", "Equatorial Guinea", "Greece", "Grenada", "Gibraltar", "Guinea", "Guadaloupe", "Greenland", "Guatemala", "French Guiana", "Guam", "Guyana", "Hong Kong", "Heard and McDonald Islands", "Honduras", "Croatia", "Haiti", "Hungary", "Indonesia", "British Indian Ocean Territory", "Iran", "Iraq", "Israel", "Japan", "Kazakhstan", "Kenya", "Kyrgyzstan", "Cambodia", "Kiribati", "St. Kitts and Nevis", "Korea (Rep. of)", "Kuwait", "Laos", "Lebanon", "Liberia", "Libya", "Marshall Islands", "Former Yug. Rep. of Macedonia", "Mali", "Malta", "Myanmar", "Iceland", "Italy", "Jamaica", "Jordan", "St. Lucia", "Mexico", "Liechtenstein", "Sri Lanka", "Lesotho", "Lithuania", "Luxembourg", "Latvia", "Maldives", "Melilla", "Panama", "Macao", "Morocco", "Monaco", "Moldova", "Madagascar", "Montenegro", "Mongolia", "Northern Mariana Islands", "Mozambique", "Mauritania", "Martinique", "Mauritius", "Malawi", "Malaysia", "Mayotte", "Namibia", "New Caledonia", "Peru", "Philippines", "Palau", "Papua New Guinea", "Poland", "Montserrat", "Niger", "New Zealand", "Oman", "Pakistan", "Norfolk Island", "Nigeria", "Nicaragua", "Nepal", "Nauru", "Puerto Rico", "Niue", "Netherlands", "Norway", "Korea (Dem People's Rep. of)", "Portugal", "Paraguay", "Palestine", "French Polynesia", "Qatar", "Reunion", "Romania", "Russia", "Rwanda", "Saudi Arabia", "Sudan", "Senegal", "Singapore", "South Georgia and the South Sandwich Islands", "St. Helena", "Solomon Islands", "Sierra Leone", "El Salvador", "San Marino", "Somalia", "Pitcairn Island", "St. Pierre and Miquelon", "Slovakia", "Slovenia", "Sweden", "Swaziland", "Seychelles", "Syria", "Thailand", "Tajikistan", "Tokelau", "Turkmenistan", "Timor-Leste", "British Virgin Islands", "Serbia", "South Sudan (Rep. of)", "Sao Tome and Principe", "Suriname", "Turks and Caicos Islands", "Chad", "Togo", "United States Minor Outlying Islands", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Tuvalu", "Chinese Taipei", "Tanzania", "Uganda", "Ukraine", "Uruguay", "United States of America", "Uzbekistan", "Vatican City", "St. Vincent and the Grenadines", "Venezuela", "US Virgin Islands", "Vietnam", "Vanuatu", "Wallis and Futuna Islands", "Samoa", "Yemen", "South Africa", "Zambia", "Zimbabwe"]

                    else:
                        options = ["opt1", "opt2"]

                    combo_box.addItems(options)
                    layout.addWidget(combo_box, row, col + 1)
                    self.attribute_widgets[field.name()] = combo_box



                row += 1

                if row > 3:
                    row = 0
                    col += 2

        button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        button_box.accepted.connect(self.accept)
        button_box.rejected.connect(self.reject)

        layout.addWidget(button_box, row, col)

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
            else: 
                edited_attributes[field_name] = line_edit.currentText()

        # Update the feature attributes
        for field_name, edited_value in edited_attributes.items():
            self.feature[field_name] = edited_value

        return edited_attributes