from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from .forms import CustomUserCreationForm, LoginForm, ContactMeForm, AddProjectForm, ProfileForm
from .models import Country, City, Profile, Project, ProjectComment, ContactMe
from .models import UserAccount as User
from blogger.models import Post

all_countries = [
    ['AW', 'Aruba'],
    ['AF', 'Afghanistan'],
    ['AO', 'Angola'],
    ['AI', 'Anguilla'],
    ['AX', 'Åland Islands'],
    ['AL', 'Albania'],
    ['AD', 'Andorra'],
    ['AE', 'United Arab Emirates'],
    ['AR', 'Argentina'],
    ['AM', 'Armenia'],
    ['AS', 'American Samoa'],
    ['AQ', 'Antarctica'],
    ['TF', 'French Southern Territories'],
    ['AG', 'Antigua and Barbuda'],
    ['AU', 'Australia'],
    ['AT', 'Austria'],
    ['AZ', 'Azerbaijan'],
    ['BI', 'Burundi'],
    ['BE', 'Belgium'],
    ['BJ', 'Benin'],
    ['BQ', 'Bonaire, Sint Eustatius and Saba'],
    ['BF', 'Burkina Faso'],
    ['BD', 'Bangladesh'],
    ['BG', 'Bulgaria'],
    ['BH', 'Bahrain'],
    ['BS', 'Bahamas'],
    ['BA', 'Bosnia and Herzegovina'],
    ['BL', 'Saint Barthélemy'],
    ['BY', 'Belarus'],
    ['BZ', 'Belize'],
    ['BM', 'Bermuda'],
    ['BO', 'Bolivia, Plurinational State of'],
    ['BR', 'Brazil'],
    ['BB', 'Barbados'],
    ['BN', 'Brunei Darussalam'],
    ['BT', 'Bhutan'],
    ['BV', 'Bouvet Island'],
    ['BW', 'Botswana'],
    ['CF', 'Central African Republic'],
    ['CA', 'Canada'],
    ['CC', 'Cocos (Keeling) Islands'],
    ['CH', 'Switzerland'],
    ['CL', 'Chile'],
    ['CN', 'China'],
    ['CI', "Côte d'Ivoire"],
    ['CM', 'Cameroon'],
    ['CD', 'Congo, The Democratic Republic of the'],
    ['CG', 'Congo'],
    ['CK', 'Cook Islands'],
    ['CO', 'Colombia'],
    ['KM', 'Comoros'],
    ['CV', 'Cabo Verde'],
    ['CR', 'Costa Rica'],
    ['CU', 'Cuba'],
    ['CW', 'Curaçao'],
    ['CX', 'Christmas Island'],
    ['KY', 'Cayman Islands'],
    ['CY', 'Cyprus'],
    ['CZ', 'Czechia'],
    ['DE', 'Germany'],
    ['DJ', 'Djibouti'],
    ['DM', 'Dominica'],
    ['DK', 'Denmark'],
    ['DO', 'Dominican Republic'],
    ['DZ', 'Algeria'],
    ['EC', 'Ecuador'],
    ['EG', 'Egypt'],
    ['ER', 'Eritrea'],
    ['EH', 'Western Sahara'],
    ['ES', 'Spain'],
    ['EE', 'Estonia'],
    ['ET', 'Ethiopia'],
    ['FI', 'Finland'],
    ['FJ', 'Fiji'],
    ['FK', 'Falkland Islands (Malvinas)'],
    ['FR', 'France'],
    ['FO', 'Faroe Islands'],
    ['FM', 'Micronesia, Federated States of'],
    ['GA', 'Gabon'],
    ['GB', 'United Kingdom'],
    ['GE', 'Georgia'],
    ['GG', 'Guernsey'],
    ['GH', 'Ghana'],
    ['GI', 'Gibraltar'],
    ['GN', 'Guinea'],
    ['GP', 'Guadeloupe'],
    ['GM', 'Gambia'],
    ['GW', 'Guinea-Bissau'],
    ['GQ', 'Equatorial Guinea'],
    ['GR', 'Greece'],
    ['GD', 'Grenada'],
    ['GL', 'Greenland'],
    ['GT', 'Guatemala'],
    ['GF', 'French Guiana'],
    ['GU', 'Guam'],
    ['GY', 'Guyana'],
    ['HK', 'Hong Kong'],
    ['HM', 'Heard Island and McDonald Islands'],
    ['HN', 'Honduras'],
    ['HR', 'Croatia'],
    ['HT', 'Haiti'],
    ['HU', 'Hungary'],
    ['ID', 'Indonesia'],
    ['IM', 'Isle of Man'],
    ['IN', 'India'],
    ['IO', 'British Indian Ocean Territory'],
    ['IE', 'Ireland'],
    ['IR', 'Iran, Islamic Republic of'],
    ['IQ', 'Iraq'],
    ['IS', 'Iceland'],
    ['IL', 'Israel'],
    ['IT', 'Italy'],
    ['JM', 'Jamaica'],
    ['JE', 'Jersey'],
    ['JO', 'Jordan'],
    ['JP', 'Japan'],
    ['KZ', 'Kazakhstan'],
    ['KE', 'Kenya'],
    ['KG', 'Kyrgyzstan'],
    ['KH', 'Cambodia'],
    ['KI', 'Kiribati'],
    ['KN', 'Saint Kitts and Nevis'],
    ['KR', 'Korea, Republic of'],
    ['KW', 'Kuwait'],
    ['LA', "Lao People's Democratic Republic"],
    ['LB', 'Lebanon'],
    ['LR', 'Liberia'],
    ['LY', 'Libya'],
    ['LC', 'Saint Lucia'],
    ['LI', 'Liechtenstein'],
    ['LK', 'Sri Lanka'],
    ['LS', 'Lesotho'],
    ['LT', 'Lithuania'],
    ['LU', 'Luxembourg'],
    ['LV', 'Latvia'],
    ['MO', 'Macao'],
    ['MF', 'Saint Martin (French part)'],
    ['MA', 'Morocco'],
    ['MC', 'Monaco'],
    ['MD', 'Moldova, Republic of'],
    ['MG', 'Madagascar'],
    ['MV', 'Maldives'],
    ['MX', 'Mexico'],
    ['MH', 'Marshall Islands'],
    ['MK', 'North Macedonia'],
    ['ML', 'Mali'],
    ['MT', 'Malta'],
    ['MM', 'Myanmar'],
    ['ME', 'Montenegro'],
    ['MN', 'Mongolia'],
    ['MP', 'Northern Mariana Islands'],
    ['MZ', 'Mozambique'],
    ['MR', 'Mauritania'],
    ['MS', 'Montserrat'],
    ['MQ', 'Martinique'],
    ['MU', 'Mauritius'],
    ['MW', 'Malawi'],
    ['MY', 'Malaysia'],
    ['YT', 'Mayotte'],
    ['NA', 'Namibia'],
    ['NC', 'New Caledonia'],
    ['NE', 'Niger'],
    ['NF', 'Norfolk Island'],
    ['NG', 'Nigeria'],
    ['NI', 'Nicaragua'],
    ['NU', 'Niue'],
    ['NL', 'Netherlands'],
    ['NO', 'Norway'],
    ['NP', 'Nepal'],
    ['NR', 'Nauru'],
    ['NZ', 'New Zealand'],
    ['OM', 'Oman'],
    ['PK', 'Pakistan'],
    ['PA', 'Panama'],
    ['PN', 'Pitcairn'],
    ['PE', 'Peru'],
    ['PH', 'Philippines'], ['PW', 'Palau'], ['PG', 'Papua New Guinea'], ['PL', 'Poland'], ['PR', 'Puerto Rico'],
    ['KP', "Korea, Democratic People's Republic of"], ['PT', 'Portugal'], ['PY', 'Paraguay'],
    ['PS', 'Palestine, State of'], ['PF', 'French Polynesia'], ['QA', 'Qatar'], ['RE', 'Réunion'],
    ['RO', 'Romania'], ['RU', 'Russian Federation'], ['RW', 'Rwanda'], ['SA', 'Saudi Arabia'], ['SD', 'Sudan'],
    ['SN', 'Senegal'], ['SG', 'Singapore'], ['GS', 'South Georgia and the South Sandwich Islands'],
    ['SH', 'Saint Helena, Ascension and Tristan da Cunha'], ['SJ', 'Svalbard and Jan Mayen'],
    ['SB', 'Solomon Islands'], ['SL', 'Sierra Leone'], ['SV', 'El Salvador'], ['SM', 'San Marino'],
    ['SO', 'Somalia'], ['PM', 'Saint Pierre and Miquelon'], ['RS', 'Serbia'], ['SS', 'South Sudan'],
    ['ST', 'Sao Tome and Principe'], ['SR', 'Suriname'], ['SK', 'Slovakia'], ['SI', 'Slovenia'], ['SE', 'Sweden'],
    ['SZ', 'Eswatini'], ['SX', 'Sint Maarten (Dutch part)'], ['SC', 'Seychelles'], ['SY', 'Syrian Arab Republic'],
    ['TC', 'Turks and Caicos Islands'], ['TD', 'Chad'], ['TG', 'Togo'], ['TH', 'Thailand'], ['TJ', 'Tajikistan'],
    ['TK', 'Tokelau'], ['TM', 'Turkmenistan'], ['TL', 'Timor-Leste'], ['TO', 'Tonga'],
    ['TT', 'Trinidad and Tobago'], ['TN', 'Tunisia'], ['TR', 'Turkey'], ['TV', 'Tuvalu'],
    ['TW', 'Taiwan, Province of China'], ['TZ', 'Tanzania, United Republic of'], ['UG', 'Uganda'],
    ['UA', 'Ukraine'], ['UM', 'United States Minor Outlying Islands'], ['UY', 'Uruguay'], ['US', 'United States'],
    ['UZ', 'Uzbekistan'], ['VA', 'Holy See (Vatican City State)'], ['VC', 'Saint Vincent and the Grenadines'],
    ['VE', 'Venezuela, Bolivarian Republic of'], ['VG', 'Virgin Islands, British'], ['VI', 'Virgin Islands, U.S.'],
    ['VN', 'Viet Nam'], ['VU', 'Vanuatu'], ['WF', 'Wallis and Futuna'], ['WS', 'Samoa'], ['YE', 'Yemen'],
    ['ZA', 'South Africa'], ['ZM', 'Zambia'], ['ZW', 'Zimbabwe']]

all_states = [
    [['AF', 'Ghaznī'], ['AF', 'Sar-e Pul'], ['AF', 'Ghōr'], ['AF', 'Takhār'], ['AF', 'Helmand'], ['AF', 'Uruzgān'],
     ['AF', 'Herāt'], ['AF', 'Wardak'], ['AF', 'Jowzjān'], ['AF', 'Zābul'], ['AF', 'Kābul'], ['AF', 'Kandahār'],
     ['AF', 'Kāpīsā'], ['AF', 'Kunduz'], ['AF', 'Khōst'], ['AF', 'Kunar'], ['AF', 'Laghmān'], ['AF', 'Lōgar'],
     ['AF', 'Nangarhār'], ['AF', 'Balkh'], ['AF', 'Nīmrōz'], ['AF', 'Bāmyān'], ['AF', 'Nūristān'],
     ['AF', 'Bādghīs'], ['AF', 'Panjshayr'], ['AF', 'Badakhshān'], ['AF', 'Parwān'], ['AF', 'Baghlān'],
     ['AF', 'Paktiyā'], ['AF', 'Dāykundī'], ['AF', 'Paktīkā'], ['AF', 'Farāh'], ['AF', 'Samangān'],
     ['AF', 'Fāryāb']],

    [['AO', 'Benguela'], ['AO', 'Cuanza Sul'], ['AO', 'Zaire'], ['AO', 'Bié'], ['AO', 'Luanda'], ['AO', 'Huambo'],
     ['AO', 'Uíge'], ['AO', 'Cabinda'], ['AO', 'Malange'], ['AO', 'Namibe'], ['AO', 'Huíla'],
     ['AO', 'Cuando-Cubango'], ['AO', 'Moxico'], ['AO', 'Lunda Norte'], ['AO', 'Cunene'], ['AO', 'Bengo'],
     ['AO', 'Lunda Sul'], ['AO', 'Cuanza Norte']],

    [['AL', 'Librazhd'], ['AL', 'Dibër'], ['AL', 'Lezhë'], ['AL', 'Shkodër'], ['AL', 'Lushnjë'], ['AL', 'Tiranë'],
     ['AL', 'Mallakastër'], ['AL', 'Vlorë'], ['AL', 'Malësi e Madhe'], ['AL', 'Berat'], ['AL', 'Mirditë'],
     ['AL', 'Bulqizë'], ['AL', 'Dibër'], ['AL', 'Mat'], ['AL', 'Delvinë'], ['AL', 'Durrës'], ['AL', 'Pogradec'],
     ['AL', 'Devoll'], ['AL', 'Peqin'], ['AL', 'Elbasan'], ['AL', 'Përmet'], ['AL', 'Kolonjë'], ['AL', 'Pukë'],
     ['AL', 'Fier'], ['AL', 'Shkodër'], ['AL', 'Gjirokastër'], ['AL', 'Skrapar'], ['AL', 'Gramsh'],
     ['AL', 'Sarandë'], ['AL', 'Berat'], ['AL', 'Has'], ['AL', 'Tepelenë'], ['AL', 'Durrës'], ['AL', 'Kavajë'],
     ['AL', 'Tropojë'], ['AL', 'Elbasan'], ['AL', 'Kurbin'], ['AL', 'Tiranë'], ['AL', 'Fier'], ['AL', 'Kuçovë'],
     ['AL', 'Vlorë'], ['AL', 'Gjirokastër'], ['AL', 'Korçë'], ['AL', 'Korçë'], ['AL', 'Krujë'], ['AL', 'Kukës'],
     ['AL', 'Kukës'], ['AL', 'Lezhë']],

    [['AD', 'Escaldes-Engordany'], ['AD', 'La Massana'], ['AD', 'Ordino'], ['AD', 'Canillo'],
     ['AD', 'Sant Julià de Lòria'], ['AD', 'Encamp'], ['AD', 'Andorra la Vella']],

    [['AE', 'Ra’s al Khaymah'], ['AE', 'Ash Shāriqah'], ['AE', "'Ajmān"], ['AE', 'Umm al Qaywayn'],
     ['AE', 'Abū Ȥaby [Abu Dhabi]'], ['AE', 'Dubayy'], ['AE', 'Al Fujayrah']],

    [['AR', 'Santa Fe'], ['AR', 'Tucuman'], ['AR', 'Chubut'], ['AR', 'Tierra del Fuego'], ['AR', 'Corrientes'],
     ['AR', 'Cordoba'], ['AR', 'Jujuy'], ['AR', 'Salta'], ['AR', 'Santa Cruz'], ['AR', 'Buenos Aires'],
     ['AR', 'Ciudad Autónoma de Buenos Aires'], ['AR', 'San Luis'], ['AR', 'Entre Rios'],
     ['AR', 'Santiago del Estero'], ['AR', 'Chaco'], ['AR', 'San Juan'], ['AR', 'Catamarca'], ['AR', 'La Pampa'],
     ['AR', 'Mendoza'], ['AR', 'Misiones'], ['AR', 'Formosa'], ['AR', 'Neuquen'], ['AR', 'Rio Negro']],

    [['AM', 'Armavir'], ['AM', 'Sirak'], ['AM', "Syunik'"], ['AM', 'Erevan'], ['AM', 'Tavus'], ['AM', 'Aragacotn'],
     ['AM', "Gegarkunik'"], ['AM', 'Vayoc Jor'], ['AM', 'Ararat'], ['AM', "Kotayk'"], ['AM', 'Lory']],

    [['AG', 'Saint Philip'], ['AG', 'Saint George'], ['AG', 'Barbuda'], ['AG', 'Saint John'], ['AG', 'Redonda'],
     ['AG', 'Saint Mary'], ['AG', 'Saint Paul'], ['AG', 'Saint Peter']],

    [['AU', 'South Australia'], ['AU', 'Australian Capital Territory'], ['AU', 'Tasmania'],
     ['AU', 'New South Wales'], ['AU', 'Victoria'], ['AU', 'Northern Territory'], ['AU', 'Western Australia'],
     ['AU', 'Queensland']],

    [['AT', 'Niederösterreich'], ['AT', 'Wien'], ['AT', 'Oberösterreich'], ['AT', 'Salzburg'], ['AT', 'Steiermark'],
     ['AT', 'Burgenland'], ['AT', 'Tirol'], ['AT', 'Kärnten'], ['AT', 'Vorarlberg']],

    [['AZ', 'Naxçıvan'], ['AZ', 'Oğuz'], ['AZ', 'Ordubad'], ['AZ', 'Qəbələ'], ['AZ', 'Qax'], ['AZ', 'Abşeron'],
     ['AZ', 'Qazax'], ['AZ', 'Ağstafa'], ['AZ', 'Ağcabədi'], ['AZ', 'Quba'], ['AZ', 'Ağdam'], ['AZ', 'Qubadlı'],
     ['AZ', 'Ağdaş'], ['AZ', 'Qobustan'], ['AZ', 'Ağsu'], ['AZ', 'Qusar'], ['AZ', 'Astara'], ['AZ', 'Şəki'],
     ['AZ', 'Bakı'], ['AZ', 'Sabirabad'], ['AZ', 'Babək'], ['AZ', 'Sədərək'], ['AZ', 'Balakən'], ['AZ', 'Şahbuz'],
     ['AZ', 'Bərdə'], ['AZ', 'Şəki'], ['AZ', 'Salyan'], ['AZ', 'Beyləqan'], ['AZ', 'Şərur'], ['AZ', 'Biləsuvar'],
     ['AZ', 'Cəbrayıl'], ['AZ', 'Saatlı'], ['AZ', 'Şabran'], ['AZ', 'Cəlilabab'], ['AZ', 'Siyəzən'],
     ['AZ', 'Culfa'], ['AZ', 'Şəmkir'], ['AZ', 'Daşkəsən'], ['AZ', 'Füzuli'], ['AZ', 'Sumqayıt'], ['AZ', 'Gəncə'],
     ['AZ', 'Şamaxı'], ['AZ', 'Gədəbəy'], ['AZ', 'Samux'], ['AZ', 'Goranboy'], ['AZ', 'Şirvan'], ['AZ', 'Göyçay'],
     ['AZ', 'Şuşa'], ['AZ', 'Göygöl'], ['AZ', 'Tərtər'], ['AZ', 'Hacıqabul'], ['AZ', 'Tovuz'], ['AZ', 'İmişli'],
     ['AZ', 'Ucar'], ['AZ', 'İsmayıllı'], ['AZ', 'Xankəndi'], ['AZ', 'Kəlbəcər'], ['AZ', 'Xaçmaz'],
     ['AZ', 'Kǝngǝrli'], ['AZ', 'Xocalı'], ['AZ', 'Kürdəmir'], ['AZ', 'Xızı'], ['AZ', 'Lənkəran'],
     ['AZ', 'Xocavənd'], ['AZ', 'Laçın'], ['AZ', 'Yardımlı'], ['AZ', 'Lənkəran'], ['AZ', 'Yevlax'], ['AZ', 'Lerik'],
     ['AZ', 'Yevlax'], ['AZ', 'Masallı'], ['AZ', 'Zəngilan'], ['AZ', 'Mingəçevir'], ['AZ', 'Zaqatala'],
     ['AZ', 'Naftalan'], ['AZ', 'Zərdab'], ['AZ', 'Neftçala'], ['AZ', 'Naxçıvan']],

    [['BI', 'Bujumbura Mairie'], ['BI', 'Karuzi'], ['BI', 'Bururi'], ['BI', 'Ngozi'], ['BI', 'Kayanza'],
     ['BI', 'Cankuzo'], ['BI', 'Rutana'], ['BI', 'Makamba'], ['BI', 'Cibitoke'], ['BI', 'Ruyigi'],
     ['BI', 'Bubanza'], ['BI', 'Muramvya'], ['BI', 'Gitega'], ['BI', 'Bujumbura Rural'], ['BI', 'Mwaro'],
     ['BI', 'Kirundo']],

    [['BE', 'wallonne, Région'], ['BE', 'Antwerpen'], ['BE', 'Brabant wallon'], ['BE', 'Vlaams-Brabant'],
     ['BE', 'Vlaams Gewest'], ['BE', 'Limburg'], ['BE', 'Hainaut'], ['BE', 'Liège'], ['BE', 'Oost-Vlaanderen'],
     ['BE', 'Luxembourg'], ['BE', 'Namur'], ['BE', 'Bruxelles-Capitale, Région de;Brussels Hoofdstedelijk Gewest'],
     ['BE', 'West-Vlaanderen']],

    [['BJ', 'Littoral'], ['BJ', 'Atlantique'], ['BJ', 'Mono'], ['BJ', 'Borgou'], ['BJ', 'Ouémé'],
     ['BJ', 'Collines'], ['BJ', 'Plateau'], ['BJ', 'Donga'], ['BJ', 'Atakora'], ['BJ', 'Zou'], ['BJ', 'Kouffo'],
     ['BJ', 'Alibori']],

    [['BQ', 'Sint Eustatius'], ['BQ', 'Saba'], ['BQ', 'Bonaire']],

    [['BF', 'Cascades'], ['BF', 'Passoré'], ['BF', 'Gnagna'], ['BF', 'Poni'], ['BF', 'Gourma'], ['BF', 'Centre'],
     ['BF', 'Séno'], ['BF', 'Houet'], ['BF', 'Sissili'], ['BF', 'Ioba'], ['BF', 'Centre-Est'], ['BF', 'Sanmatenga'],
     ['BF', 'Kadiogo'], ['BF', 'Centre-Nord'], ['BF', 'Sanguié'], ['BF', 'Kénédougou'], ['BF', 'Centre-Ouest'],
     ['BF', 'Soum'], ['BF', 'Komondjari'], ['BF', 'Centre-Sud'], ['BF', 'Sourou'], ['BF', 'Kompienga'],
     ['BF', 'Est'], ['BF', 'Tapoa'], ['BF', 'Koulpélogo'], ['BF', 'Hauts-Bassins'], ['BF', 'Tui'], ['BF', 'Kossi'],
     ['BF', 'Nord'], ['BF', 'Yagha'], ['BF', 'Kouritenga'], ['BF', 'Plateau-Central'], ['BF', 'Yatenga'],
     ['BF', 'Kourwéogo'], ['BF', 'Sahel'], ['BF', 'Ziro'], ['BF', 'Léraba'], ['BF', 'Sud-Ouest'], ['BF', 'Zondoma'],
     ['BF', 'Loroum'], ['BF', 'Balé'], ['BF', 'Zoundwéogo'], ['BF', 'Mouhoun'], ['BF', 'Bam'], ['BF', 'Banwa'],
     ['BF', 'Namentenga'], ['BF', 'Bazèga'], ['BF', 'Bougouriba'], ['BF', 'Naouri'], ['BF', 'Boulgou'],
     ['BF', 'Nayala'], ['BF', 'Oudalan'], ['BF', 'Boulkiemdé'], ['BF', 'Noumbiel'], ['BF', 'Comoé'],
     ['BF', 'Oubritenga'], ['BF', 'Ganzourgou'], ['BF', 'Boucle du Mouhoun']],

    [['BD', 'Natore'], ['BD', 'Jhenaidah'], ['BD', 'Bandarban'], ['BD', 'Barisal'], ['BD', 'Nawabganj'],
     ['BD', 'Jaipurhat'], ['BD', 'Barguna'], ['BD', 'Chittagong'], ['BD', 'Bogra'], ['BD', 'Nilphamari'],
     ['BD', 'Jhalakati'], ['BD', 'Brahmanbaria'], ['BD', 'Bagerhat'], ['BD', 'Noakhali'], ['BD', 'Kishorganj'],
     ['BD', 'Dhaka'], ['BD', 'Barisal'], ['BD', 'Naogaon'], ['BD', 'Khulna'], ['BD', 'Khulna'], ['BD', 'Bhola'],
     ['BD', 'Pabna'], ['BD', 'Kurigram'], ['BD', 'Rajshahi'], ['BD', 'Comilla'], ['BD', 'Pirojpur'],
     ['BD', 'Khagrachari'], ['BD', 'Rangpur'], ['BD', 'Chandpur'], ['BD', 'Patuakhali'], ['BD', 'Kushtia'],
     ['BD', 'Sylhet'], ['BD', 'Chittagong'], ['BD', 'Panchagarh'], ['BD', 'Lakshmipur'], ['BD', "Cox's Bazar"],
     ['BD', 'Rajbari'], ['BD', 'Lalmonirhat'], ['BD', 'Chuadanga'], ['BD', 'Rajshahi'], ['BD', 'Manikganj'],
     ['BD', 'Dhaka'], ['BD', 'Rangpur'], ['BD', 'Mymensingh'], ['BD', 'Tangail'], ['BD', 'Dinajpur'],
     ['BD', 'Rangamati'], ['BD', 'Munshiganj'], ['BD', 'Faridpur'], ['BD', 'Sherpur'], ['BD', 'Madaripur'],
     ['BD', 'Feni'], ['BD', 'Satkhira'], ['BD', 'Magura'], ['BD', 'Gopalganj'], ['BD', 'Sirajganj'],
     ['BD', 'Moulvibazar'], ['BD', 'Gazipur'], ['BD', 'Sylhet'], ['BD', 'Meherpur'], ['BD', 'Thakurgaon'],
     ['BD', 'Gaibandha'], ['BD', 'Sunamganj'], ['BD', 'Narayanganj'], ['BD', 'Habiganj'], ['BD', 'Shariatpur'],
     ['BD', 'Netrakona'], ['BD', 'Jamalpur'], ['BD', 'Narsingdi'], ['BD', 'Jessore'], ['BD', 'Narail']],

    [['BG', 'Haskovo'], ['BG', 'Vidin'], ['BG', 'Shumen'], ['BG', 'Vratsa'], ['BG', 'Yambol'], ['BG', 'Gabrovo'],
     ['BG', 'Dobrich'], ['BG', 'Kardzhali'], ['BG', 'Kyustendil'], ['BG', 'Lovech'], ['BG', 'Montana'],
     ['BG', 'Pazardzhik'], ['BG', 'Pernik'], ['BG', 'Pleven'], ['BG', 'Plovdiv'], ['BG', 'Razgrad'], ['BG', 'Ruse'],
     ['BG', 'Silistra'], ['BG', 'Sliven'], ['BG', 'Blagoevgrad'], ['BG', 'Smolyan'], ['BG', 'Burgas'],
     ['BG', 'Sofia-Grad'], ['BG', 'Sofia'], ['BG', 'Varna'], ['BG', 'Stara Zagora'], ['BG', 'Veliko Tarnovo'],
     ['BG', 'Targovishte']],

    [['BH', 'Al Muḩarraq'], ['BH', 'Al Wusţá'], ['BH', 'Ash Shamālīyah'], ['BH', 'Al Manāmah (Al ‘Āşimah)'],
     ['BH', 'Al Janūbīyah']],

    [['BS', 'Central Eleuthera'], ['BS', 'South Andros'], ['BS', 'Cat Island'], ['BS', 'South Eleuthera'],
     ['BS', 'Crooked Island and Long Cay'], ['BS', 'South Abaco'], ['BS', 'Central Abaco'], ['BS', 'San Salvador'],
     ['BS', 'Central Andros'], ['BS', 'Spanish Wells'], ['BS', 'East Grand Bahama'], ['BS', 'West Grand Bahama'],
     ['BS', 'Exuma'], ['BS', 'City of Freeport'], ['BS', 'Grand Cay'], ['BS', 'Harbour Island'],
     ['BS', 'Hope Town'], ['BS', 'Inagua'], ['BS', 'Long Island'], ['BS', 'Mangrove Cay'], ['BS', 'Mayaguana'],
     ['BS', "Moore's Island"], ['BS', 'North Eleuthera'], ['BS', 'North Abaco'], ['BS', 'Acklins'],
     ['BS', 'North Andros'], ['BS', 'Bimini'], ['BS', 'Rum Cay'], ['BS', 'Black Point'], ['BS', 'Ragged Island'],
     ['BS', 'Berry Islands']],

    [['BA', 'Republika Srpska'], ['BA', 'Zeničko-dobojski kanton'], ['BA', 'Kanton br. 10 (Livanjski kanton)'],
     ['BA', 'Bosansko-podrinjski kanton'], ['BA', 'Federacija Bosne i Hercegovine'],
     ['BA', 'Srednjobosanski kanton'], ['BA', 'Brčko distrikt'], ['BA', 'Hercegovačko-neretvanski kanton'],
     ['BA', 'Unsko-sanski kanton'], ['BA', 'Zapadnohercegovački kanton'], ['BA', 'Posavski kanton'],
     ['BA', 'Tuzlanski kanton'], ['BA', 'Kanton Sarajevo']],

    [['BY', 'Homieĺskaja voblasć'], ['BY', 'Hrodzienskaja voblasć'], ['BY', 'Mahilioŭskaja voblasć'],
     ['BY', 'Minskaja voblasć'], ['BY', 'Bresckaja voblasć'], ['BY', 'Viciebskaja voblasć'], ['BY', 'Horad Minsk']],

    [['BZ', 'Toledo'], ['BZ', 'Belize'], ['BZ', 'Cayo'], ['BZ', 'Corozal'], ['BZ', 'Orange Walk'],
     ['BZ', 'Stann Creek']],

    [['BO', 'Santa Cruz'], ['BO', 'Chuquisaca'], ['BO', 'Tarija'], ['BO', 'La Paz'], ['BO', 'Pando'],
     ['BO', 'Oruro'], ['BO', 'El Beni'], ['BO', 'Potosí'], ['BO', 'Cochabamba']],

    [['BR', 'Minas Gerais'], ['BR', 'Mato Grosso do Sul'], ['BR', 'Mato Grosso'], ['BR', 'Pará'], ['BR', 'Paraíba'],
     ['BR', 'Pernambuco'], ['BR', 'Piauí'], ['BR', 'Paraná'], ['BR', 'Rio de Janeiro'],
     ['BR', 'Rio Grande do Norte'], ['BR', 'Acre'], ['BR', 'Rondônia'], ['BR', 'Alagoas'], ['BR', 'Roraima'],
     ['BR', 'Amazonas'], ['BR', 'Rio Grande do Sul'], ['BR', 'Amapá'], ['BR', 'Santa Catarina'], ['BR', 'Bahia'],
     ['BR', 'Sergipe'], ['BR', 'Ceará'], ['BR', 'São Paulo'], ['BR', 'Distrito Federal'], ['BR', 'Tocantins'],
     ['BR', 'Espírito Santo'], ['BR', 'Fernando de Noronha'], ['BR', 'Goiás'], ['BR', 'Maranhão']],

    [['BB', 'Saint Thomas'], ['BB', 'Saint Joseph'], ['BB', 'Christ Church'], ['BB', 'Saint Lucy'],
     ['BB', 'Saint Andrew'], ['BB', 'Saint Michael'], ['BB', 'Saint George'], ['BB', 'Saint Peter'],
     ['BB', 'Saint James'], ['BB', 'Saint Philip'], ['BB', 'Saint John']],

    [['BN', 'Tutong'], ['BN', 'Temburong'], ['BN', 'Brunei-Muara'], ['BN', 'Belait']],

    [['BT', 'Pemagatshel'], ['BT', 'Lhuentse'], ['BT', 'Samdrup Jongkha'], ['BT', 'Gasa'], ['BT', 'Trashi Yangtse'],
     ['BT', 'Paro'], ['BT', 'Chhukha'], ['BT', 'Ha'], ['BT', 'Samtee'], ['BT', 'Thimphu'], ['BT', 'Tsirang'],
     ['BT', 'Dagana'], ['BT', 'Punakha'], ['BT', 'Wangdue Phodrang'], ['BT', 'Sarpang'], ['BT', 'Trongsa'],
     ['BT', 'Bumthang'], ['BT', 'Zhemgang'], ['BT', 'Trashigang'], ['BT', 'Monggar']],

    [['BW', 'Central'], ['BW', 'North-West'], ['BW', 'Ghanzi'], ['BW', 'South-East'], ['BW', 'Kgalagadi'],
     ['BW', 'Southern'], ['BW', 'Kgatleng'], ['BW', 'Kweneng'], ['BW', 'North-East']],

    [['CF', 'Gribingui'], ['CF', 'Bangui'], ['CF', 'Nana-Mambéré'], ['CF', 'Vakaga'], ['CF', 'Kémo-Gribingui'],
     ['CF', 'Basse-Kotto'], ['CF', 'Ouham-Pendé'], ['CF', 'Lobaye'], ['CF', 'Haute-Kotto'], ['CF', 'Sangha'],
     ['CF', 'Mbomou'], ['CF', 'Haut-Mbomou'], ['CF', 'Ouaka'], ['CF', 'Ouham'], ['CF', "Ombella-M'poko"],
     ['CF', 'Haute-Sangha / Mambéré-Kadéï'], ['CF', 'Bamingui-Bangoran']],

    [['CA', 'Newfoundland and Labrador'], ['CA', 'Quebec'], ['CA', 'Nova Scotia'], ['CA', 'Alberta'],
     ['CA', 'Saskatchewan'], ['CA', 'Northwest Territories'], ['CA', 'British Columbia'], ['CA', 'Yukon Territory'],
     ['CA', 'Nunavut'], ['CA', 'Manitoba'], ['CA', 'Ontario'], ['CA', 'New Brunswick'],
     ['CA', 'Prince Edward Island']],

    [['CH', 'Basel-Stadt'], ['CH', 'Fribourg'], ['CH', 'Genève'], ['CH', 'Glarus'], ['CH', 'Graubünden'],
     ['CH', 'Jura'], ['CH', 'Luzern'], ['CH', 'Neuchâtel'], ['CH', 'Nidwalden'], ['CH', 'Obwalden'],
     ['CH', 'Sankt Gallen'], ['CH', 'Schaffhausen'], ['CH', 'Solothurn'], ['CH', 'Schwyz'], ['CH', 'Thurgau'],
     ['CH', 'Ticino'], ['CH', 'Uri'], ['CH', 'Aargau'], ['CH', 'Vaud'], ['CH', 'Appenzell Innerrhoden'],
     ['CH', 'Valais'], ['CH', 'Appenzell Ausserrhoden'], ['CH', 'Zug'], ['CH', 'Bern'], ['CH', 'Zürich'],
     ['CH', 'Basel-Landschaft']],

    [['CL', "Libertador General Bernardo O'Higgins"], ['CL', 'Arica y Parinacota'], ['CL', 'Tarapacá'],
     ['CL', 'Los Lagos'], ['CL', 'Araucanía'], ['CL', 'Valparaíso'], ['CL', 'Los Ríos'], ['CL', 'Atacama'],
     ['CL', 'Magallanes y Antártica Chilena'], ['CL', 'Bío-Bío'],
     ['CL', 'Aisén del General Carlos Ibáñez del Campo'], ['CL', 'Maule'], ['CL', 'Coquimbo'],
     ['CL', 'Antofagasta'], ['CL', 'Región Metropolitana de Santiago']],

    [['CN', 'Macao SAR (see also separate country code entry under MO)'], ['CN', 'Nei Mongol Zizhiqu'],
     ['CN', 'Ningxia Huizi Zizhiqu'], ['CN', 'Anhui Sheng'], ['CN', 'Qinghai Sheng'], ['CN', 'Beijing Shi'],
     ['CN', 'Sichuan Sheng'], ['CN', 'Chongqing Shi'], ['CN', 'Shandong Sheng'], ['CN', 'Fujian Sheng'],
     ['CN', 'Shanghai Shi'], ['CN', 'Guangdong Sheng'], ['CN', 'Shaanxi Sheng'], ['CN', 'Gansu Sheng'],
     ['CN', 'Shanxi Sheng'], ['CN', 'Guangxi Zhuangzu Zizhiqu'], ['CN', 'Tianjin Shi'], ['CN', 'Guizhou Sheng'],
     ['CN', 'Taiwan Sheng (see also separate country code entry under TW)'], ['CN', 'Henan Sheng'],
     ['CN', 'Xinjiang Uygur Zizhiqu'], ['CN', 'Hubei Sheng'], ['CN', 'Xizang Zizhiqu'], ['CN', 'Hebei Sheng'],
     ['CN', 'Yunnan Sheng'], ['CN', 'Hainan Sheng'], ['CN', 'Zhejiang Sheng'],
     ['CN', 'Hong Kong SAR (see also separate country code entry under HK)'], ['CN', 'Heilongjiang Sheng'],
     ['CN', 'Hunan Sheng'], ['CN', 'Jilin Sheng'], ['CN', 'Jiangsu Sheng'], ['CN', 'Jiangxi Sheng'],
     ['CN', 'Liaoning Sheng']],

    [['CI', 'Lagunes (Région des)'], ['CI', 'Haut-Sassandra (Région du)'], ['CI', 'Savanes (Région des)'],
     ['CI', 'Vallée du Bandama (Région de la)'], ['CI', 'Moyen-Comoé (Région du)'],
     ['CI', '18 Montagnes (Région des)'], ['CI', 'Lacs (Région des)'], ['CI', 'Zanzan (Région du)'],
     ['CI', 'Bas-Sassandra (Région du)'], ['CI', 'Denguélé (Région du)'], ['CI', 'Nzi-Comoé (Région)'],
     ['CI', 'Marahoué (Région de la)'], ['CI', 'Sud-Comoé (Région du)'], ['CI', 'Worodouqou (Région du)'],
     ['CI', 'Sud-Bandama (Région du)'], ['CI', "Agnébi (Région de l')"], ['CI', 'Bafing (Région du)'],
     ['CI', 'Fromager (Région du)'], ['CI', 'Moyen-Cavally (Région du)']],

    [['CM', 'East'], ['CM', 'South'], ['CM', 'Littoral'], ['CM', 'South-West'], ['CM', 'North'], ['CM', 'Adamaoua'],
     ['CM', 'North-West (Cameroon)'], ['CM', 'Centre'], ['CM', 'West'], ['CM', 'Far North']],

    [['CD', 'Maniema'], ['CD', 'Équateur'], ['CD', 'Nord-Kivu'], ['CD', 'Katanga'], ['CD', 'Orientale'],
     ['CD', 'Kasai-Oriental'], ['CD', 'Sud-Kivu'], ['CD', 'Kinshasa'], ['CD', 'Bas-Congo'],
     ['CD', 'Kasai-Occidental'], ['CD', 'Bandundu']],

    [['CG', 'Lékoumou'], ['CG', 'Bouenza'], ['CG', 'Kouilou'], ['CG', 'Pool'], ['CG', 'Likouala'], ['CG', 'Sangha'],
     ['CG', 'Cuvette'], ['CG', 'Plateaux'], ['CG', 'Niari'], ['CG', 'Cuvette-Ouest'], ['CG', 'Brazzaville']],

    [['CO', 'San Andrés, Providencia y Santa Catalina'], ['CO', 'Caldas'], ['CO', 'Sucre'], ['CO', 'Caquetá'],
     ['CO', 'Tolima'], ['CO', 'Casanare'], ['CO', 'Valle del Cauca'], ['CO', 'Cauca'], ['CO', 'Vaupés'],
     ['CO', 'Cesar'], ['CO', 'Vichada'], ['CO', 'Chocó'], ['CO', 'Córdoba'], ['CO', 'Cundinamarca'],
     ['CO', 'Distrito Capital de Bogotá'], ['CO', 'Guainía'], ['CO', 'Guaviare'], ['CO', 'Huila'],
     ['CO', 'La Guajira'], ['CO', 'Magdalena'], ['CO', 'Meta'], ['CO', 'Amazonas'], ['CO', 'Nariño'],
     ['CO', 'Antioquia'], ['CO', 'Norte de Santander'], ['CO', 'Arauca'], ['CO', 'Putumayo'], ['CO', 'Atlántico'],
     ['CO', 'Quindío'], ['CO', 'Bolívar'], ['CO', 'Risaralda'], ['CO', 'Boyacá'], ['CO', 'Santander']],

    [['KM', 'Andjouân (Anjwān)'], ['KM', 'Moûhîlî (Mūhīlī)'], ['KM', 'Andjazîdja (Anjazījah)']],

    [['CV', 'São Filipe'], ['CV', 'Sal'], ['CV', 'São Miguel'], ['CV', 'São Lourenço dos Órgãos'],
     ['CV', 'São Salvador do Mundo'], ['CV', 'São Vicente'], ['CV', 'Tarrafal'], ['CV', 'Ilhas de Barlavento'],
     ['CV', 'Tarrafal de São Nicolau'], ['CV', 'Brava'], ['CV', 'Boa Vista'], ['CV', 'Santa Catarina'],
     ['CV', 'Santa Catarina de Fogo'], ['CV', 'Santa Cruz'], ['CV', 'Maio'], ['CV', 'Mosteiros'], ['CV', 'Paul'],
     ['CV', 'Porto Novo'], ['CV', 'Praia'], ['CV', 'Ribeira Brava'], ['CV', 'Ribeira Grande'],
     ['CV', 'Ribeira Grande de Santiago'], ['CV', 'Ilhas de Sotavento'], ['CV', 'São Domingos']],

    [['CR', 'Puntarenas'], ['CR', 'Alajuela'], ['CR', 'San José'], ['CR', 'Cartago'], ['CR', 'Guanacaste'],
     ['CR', 'Heredia'], ['CR', 'Limón']],

    [['CU', 'Matanzas'], ['CU', 'Guantánamo'], ['CU', 'Camagüey'], ['CU', 'Villa Clara'],
     ['CU', 'Isla de la Juventud'], ['CU', 'Las Tunas'], ['CU', 'Santiago de Cuba'], ['CU', 'Cienfuegos'],
     ['CU', 'Pinar del Rio'], ['CU', 'Holguín'], ['CU', 'Sancti Spíritus'], ['CU', 'La Habana'], ['CU', 'Granma'],
     ['CU', 'Ciego de Ávila'], ['CU', 'Ciudad de La Habana']],

    [['CY', 'Lárnaka'], ['CY', 'Ammóchostos'], ['CY', 'Lefkosía'], ['CY', 'Páfos'], ['CY', 'Lemesós'],
     ['CY', 'Kerýneia']],

    [['CZ', 'Plzeň-jih'], ['CZ', 'Plzeň-sever'], ['CZ', 'Rokycany'], ['CZ', 'Tachov'], ['CZ', 'Karlovarský kraj'],
     ['CZ', 'Cheb'], ['CZ', 'Karlovy Vary'], ['CZ', 'Sokolov'], ['CZ', 'Ústecký kraj'], ['CZ', 'Děčín'],
     ['CZ', 'Chomutov'], ['CZ', 'Litoměřice'], ['CZ', 'Louny'], ['CZ', 'Most'], ['CZ', 'Teplice'],
     ['CZ', 'Ústí nad Labem'], ['CZ', 'Liberecký kraj'], ['CZ', 'Česká Lípa'], ['CZ', 'Jablonec nad Nisou'],
     ['CZ', 'Liberec'], ['CZ', 'Semily'], ['CZ', 'Královéhradecký kraj'], ['CZ', 'Hradec Králové'], ['CZ', 'Jičín'],
     ['CZ', 'Náchod'], ['CZ', 'Rychnov nad Kněžnou'], ['CZ', 'Trutnov'], ['CZ', 'Pardubický kraj'],
     ['CZ', 'Chrudim'], ['CZ', 'Pardubice'], ['CZ', 'Svitavy'], ['CZ', 'Ústí nad Orlicí'], ['CZ', 'Kraj Vysočina'],
     ['CZ', 'Havlíčkův Brod'], ['CZ', 'Jihlava'], ['CZ', 'Pelhřimov'], ['CZ', 'Třebíč'], ['CZ', 'Žďár nad Sázavou'],
     ['CZ', 'Praha, Hlavní mešto'], ['CZ', 'Jihomoravský kraj'], ['CZ', 'Praha 1'], ['CZ', 'Blansko'],
     ['CZ', 'Praha 2'], ['CZ', 'Praha 3'], ['CZ', 'Praha 4'], ['CZ', 'Praha 5'], ['CZ', 'Brno-město'],
     ['CZ', 'Praha 6'], ['CZ', 'Brno-venkov'], ['CZ', 'Břeclav'], ['CZ', 'Praha 7'], ['CZ', 'Hodonín'],
     ['CZ', 'Praha 8'], ['CZ', 'Vyškov'], ['CZ', 'Praha 9'], ['CZ', 'Znojmo'], ['CZ', 'Praha 10'],
     ['CZ', 'Olomoucký kraj'], ['CZ', 'Praha 11'], ['CZ', 'Jeseník'], ['CZ', 'Praha 12'], ['CZ', 'Praha 13'],
     ['CZ', 'Olomouc'], ['CZ', 'Praha 14'], ['CZ', 'Prostějov'], ['CZ', 'Přerov'], ['CZ', 'Praha 15'],
     ['CZ', 'Šumperk'], ['CZ', 'Praha 16'], ['CZ', 'Zlínský kraj'], ['CZ', 'Praha 17'], ['CZ', 'Kroměříž'],
     ['CZ', 'Praha 18'], ['CZ', 'Praha 19'], ['CZ', 'Uherské Hradiště'], ['CZ', 'Praha 20'], ['CZ', 'Vsetín'],
     ['CZ', 'Zlín'], ['CZ', 'Praha 21'], ['CZ', 'Moravskoslezský kraj'], ['CZ', 'Praha 22'], ['CZ', 'Bruntál'],
     ['CZ', 'Středočeský kraj'], ['CZ', 'Benešov'], ['CZ', 'Frýdek Místek'], ['CZ', 'Karviná'],
     ['CZ', 'Nový Jičín'], ['CZ', 'Beroun'], ['CZ', 'Opava'], ['CZ', 'Kladno'], ['CZ', 'Ostrava-město'],
     ['CZ', 'Kolín'], ['CZ', 'Kutná Hora'], ['CZ', 'Mělník'], ['CZ', 'Mladá Boleslav'], ['CZ', 'Nymburk'],
     ['CZ', 'Praha-východ'], ['CZ', 'Praha-západ'], ['CZ', 'Příbram'], ['CZ', 'Rakovník'], ['CZ', 'Jihočeský kraj'],
     ['CZ', 'České Budějovice'], ['CZ', 'Český Krumlov'], ['CZ', 'Jindřichův Hradec'], ['CZ', 'Písek'],
     ['CZ', 'Prachatice'], ['CZ', 'Strakonice'], ['CZ', 'Tábor'], ['CZ', 'Plzeňský kraj'], ['CZ', 'Domažlice'],
     ['CZ', 'Klatovy'], ['CZ', 'Plzeň-město']],

    [['DE', 'Bayern'], ['DE', 'Sachsen-Anhalt'], ['DE', 'Nordrhein-Westfalen'], ['DE', 'Brandenburg'],
     ['DE', 'Bremen'], ['DE', 'Thüringen'], ['DE', 'Rheinland-Pfalz'], ['DE', 'Berlin'], ['DE', 'Hessen'],
     ['DE', 'Schleswig-Holstein'], ['DE', 'Hamburg'], ['DE', 'Saarland'], ['DE', 'Baden-Württemberg'],
     ['DE', 'Mecklenburg-Vorpommern'], ['DE', 'Sachsen'], ['DE', 'Niedersachsen']],

    [['DJ', 'Djibouti'], ['DJ', 'Obock'], ['DJ', 'Arta'], ['DJ', 'Tadjourah'], ['DJ', 'Ali Sabieh'],
     ['DJ', 'Dikhil']],

    [['DM', 'Saint David'], ['DM', 'Saint Patrick'], ['DM', 'Saint George'], ['DM', 'Saint Paul'],
     ['DM', 'Saint John'], ['DM', 'Saint Joseph'], ['DM', 'Saint Peter'], ['DM', 'Saint Luke'],
     ['DM', 'Saint Andrew'], ['DM', 'Saint Mark']],

    [['DK', 'Syddanmark'], ['DK', 'Hovedstaden'], ['DK', 'Sjælland'], ['DK', 'Nordjylland'], ['DK', 'Midtjylland']],

    [['DO', 'Barahona'], ['DO', 'Santiago'], ['DO', 'Dajabón'], ['DO', 'Santiago Rodríguez'], ['DO', 'Duarte'],
     ['DO', 'Valverde'], ['DO', 'La Estrelleta [Elías Piña]'], ['DO', 'Monseñor Nouel'],
     ['DO', 'El Seybo [El Seibo]'], ['DO', 'Monte Plata'], ['DO', 'Espaillat'], ['DO', 'Hato Mayor'],
     ['DO', 'Independencia'], ['DO', 'La Altagracia'], ['DO', 'La Romana'], ['DO', 'La Vega'],
     ['DO', 'María Trinidad Sánchez'], ['DO', 'Monte Cristi'], ['DO', 'Pedernales'], ['DO', 'Peravia'],
     ['DO', 'Puerto Plata'], ['DO', 'Salcedo'], ['DO', 'Samaná'], ['DO', 'San Cristóbal'], ['DO', 'San Juan'],
     ['DO', 'Distrito Nacional (Santo Domingo)'], ['DO', 'San Pedro de Macorís'], ['DO', 'Azua'],
     ['DO', 'Sánchez Ramírez'], ['DO', 'Bahoruco']],

    [['DZ', 'Alger'], ['DZ', 'Tindouf'], ['DZ', 'Djelfa'], ['DZ', 'Tissemsilt'], ['DZ', 'Jijel'], ['DZ', 'El Oued'],
     ['DZ', 'Sétif'], ['DZ', 'Khenchela'], ['DZ', 'Saïda'], ['DZ', 'Souk Ahras'], ['DZ', 'Skikda'],
     ['DZ', 'Tipaza'], ['DZ', 'Sidi Bel Abbès'], ['DZ', 'Adrar'], ['DZ', 'Mila'], ['DZ', 'Annaba'], ['DZ', 'Chlef'],
     ['DZ', 'Aïn Defla'], ['DZ', 'Guelma'], ['DZ', 'Laghouat'], ['DZ', 'Naama'], ['DZ', 'Constantine'],
     ['DZ', 'Oum el Bouaghi'], ['DZ', 'Aïn Témouchent'], ['DZ', 'Médéa'], ['DZ', 'Batna'], ['DZ', 'Ghardaïa'],
     ['DZ', 'Mostaganem'], ['DZ', 'Béjaïa'], ['DZ', 'Relizane'], ['DZ', 'Msila'], ['DZ', 'Biskra'],
     ['DZ', 'Mascara'], ['DZ', 'Béchar'], ['DZ', 'Ouargla'], ['DZ', 'Blida'], ['DZ', 'Oran'], ['DZ', 'Bouira'],
     ['DZ', 'El Bayadh'], ['DZ', 'Tamanghasset'], ['DZ', 'Illizi'], ['DZ', 'Tébessa'], ['DZ', 'Bordj Bou Arréridj'],
     ['DZ', 'Tlemcen'], ['DZ', 'Boumerdès'], ['DZ', 'Tiaret'], ['DZ', 'El Tarf'], ['DZ', 'Tizi Ouzou']],

    [['EC', 'Loja'], ['EC', 'Manabí'], ['EC', 'Napo'], ['EC', 'El Oro'], ['EC', 'Pichincha'], ['EC', 'Los Ríos'],
     ['EC', 'Morona-Santiago'], ['EC', 'Santo Domingo de los Tsáchilas'], ['EC', 'Santa Elena'],
     ['EC', 'Tungurahua'], ['EC', 'Sucumbíos'], ['EC', 'Galápagos'], ['EC', 'Cotopaxi'], ['EC', 'Azuay'],
     ['EC', 'Pastaza'], ['EC', 'Bolívar'], ['EC', 'Zamora-Chinchipe'], ['EC', 'Carchi'], ['EC', 'Orellana'],
     ['EC', 'Esmeraldas'], ['EC', 'Cañar'], ['EC', 'Guayas'], ['EC', 'Chimborazo'], ['EC', 'Imbabura']],

    [['EG', 'Ḩulwān'], ['EG', 'Al Ismā`īlīyah'], ['EG', "Janūb Sīnā'"], ['EG', 'Al Qalyūbīyah'],
     ['EG', 'Kafr ash Shaykh'], ['EG', 'Qinā'], ['EG', 'Al Minyā'], ['EG', 'Al Minūfīyah'], ['EG', 'Matrūh'],
     ['EG', 'Būr Sa`īd'], ['EG', 'Al Iskandarīyah'], ['EG', 'Sūhāj'], ['EG', 'Aswān'], ['EG', 'Ash Sharqīyah'],
     ['EG', 'Asyūt'], ['EG', "Shamal Sīnā'"], ['EG', 'Al Bahr al Ahmar'], ['EG', 'As Sādis min Uktūbar'],
     ['EG', 'Al Buhayrah'], ['EG', 'As Suways'], ['EG', 'Banī Suwayf'], ['EG', 'Al Wādī al Jadīd'],
     ['EG', 'Al Qāhirah'], ['EG', 'Ad Daqahlīyah'], ['EG', 'Dumyāt'], ['EG', 'Al Fayyūm'], ['EG', 'Al Gharbīyah'],
     ['EG', 'Al Jīzah']],

    [['ER', 'Ansabā'], ['ER', 'Shimālī al Baḩrī al Aḩmar'], ['ER', 'Janūbī al Baḩrī al Aḩmar'], ['ER', 'Al Janūbī'],
     ['ER', 'Qāsh-Barkah'], ['ER', 'Al Awsaţ']],

    [['ES', 'Ciudad Real'], ['ES', 'Castellón'], ['ES', 'Valladolid'], ['ES', 'Melilla'], ['ES', 'Catalunya'],
     ['ES', 'Alicante'], ['ES', 'Cuenca'], ['ES', 'Valenciana, Comunidad / Valenciana, Comunitat'],
     ['ES', 'Albacete'], ['ES', 'Murcia'], ['ES', 'Álava'], ['ES', 'Almería'], ['ES', 'Andalucía'],
     ['ES', 'Extremadura'], ['ES', 'Navarra / Nafarroa'], ['ES', 'Aragón'],
     ['ES', 'Navarra, Comunidad Foral de / Nafarroako Foru Komunitatea'], ['ES', 'Asturias'], ['ES', 'Galicia'],
     ['ES', 'Zaragoza'], ['ES', 'Las Palmas'], ['ES', 'Zamora'], ['ES', 'Asturias, Principado de'],
     ['ES', 'Ourense'], ['ES', 'Palencia'], ['ES', 'Girona'], ['ES', 'Ávila'], ['ES', 'Granada'], ['ES', 'Balears'],
     ['ES', 'Pontevedra'], ['ES', 'Guadalajara'], ['ES', 'Barcelona'], ['ES', 'Huelva'], ['ES', 'Badajoz'],
     ['ES', 'País Vasco / Euskal Herria'], ['ES', 'Bizkaia'], ['ES', 'Huesca'], ['ES', 'Burgos'],
     ['ES', 'La Rioja'], ['ES', 'Illes Balears'], ['ES', 'A Coruña'], ['ES', 'Jaén'], ['ES', 'Cádiz'],
     ['ES', 'Cantabria'], ['ES', 'Cantabria'], ['ES', 'Salamanca'], ['ES', 'Lleida'], ['ES', 'Cáceres'],
     ['ES', 'Sevilla'], ['ES', 'Segovia'], ['ES', 'León'], ['ES', 'Soria'], ['ES', 'La Rioja'], ['ES', 'Lugo'],
     ['ES', 'Ceuta'], ['ES', 'Gipuzkoa'], ['ES', 'Madrid'], ['ES', 'Castilla y León'], ['ES', 'Tarragona'],
     ['ES', 'Málaga'], ['ES', 'Castilla-La Mancha'], ['ES', 'Teruel'], ['ES', 'Murcia, Región de'],
     ['ES', 'Santa Cruz de Tenerife'], ['ES', 'Canarias'], ['ES', 'Madrid, Comunidad de'], ['ES', 'Toledo'],
     ['ES', 'Córdoba'], ['ES', 'Valencia / València']],

    [['EE', 'Hiiumaa'], ['EE', 'Tartumaa'], ['EE', 'Lääne-Virumaa'], ['EE', 'Ida-Virumaa'], ['EE', 'Valgamaa'],
     ['EE', 'Põlvamaa'], ['EE', 'Jõgevamaa'], ['EE', 'Viljandimaa'], ['EE', 'Pärnumaa'], ['EE', 'Järvamaa'],
     ['EE', 'Saaremaa'], ['EE', 'Raplamaa'], ['EE', 'Võrumaa'], ['EE', 'Läänemaa'], ['EE', 'Harjumaa']],

    [['ET', 'Sumalē'], ['ET', 'Dirē Dawa'], ['ET', 'Ādīs Ābeba'], ['ET', 'Tigray'], ['ET', 'Āfar'],
     ['ET', 'Gambēla Hizboch'], ['ET', 'Hārerī Hizb'], ['ET', 'Āmara'], ['ET', 'Oromīya'],
     ['ET', 'YeDebub Bihēroch Bihēreseboch na Hizboch'], ['ET', 'Bīnshangul Gumuz']],

    [['FI', 'Etelä-Savo'], ['FI', 'Kainuu'], ['FI', 'Kanta-Häme'], ['FI', 'Keski-Pohjanmaa'], ['FI', 'Keski-Suomi'],
     ['FI', 'Kymenlaakso'], ['FI', 'Lappi'], ['FI', 'Pirkanmaa'], ['FI', 'Pohjanmaa'], ['FI', 'Pohjois-Karjala'],
     ['FI', 'Pohjois-Pohjanmaa'], ['FI', 'Pohjois-Savo'], ['FI', 'Päijät-Häme'], ['FI', 'Satakunta'],
     ['FI', 'Uusimaa'], ['FI', 'Varsinais-Suomi'], ['FI', 'Ahvenanmaan maakunta'], ['FI', 'Etelä-Karjala'],
     ['FI', 'Etelä-Pohjanmaa']],

    [['FJ', 'Central'], ['FJ', 'Eastern'], ['FJ', 'Northern'], ['FJ', 'Rotuma'], ['FJ', 'Western']],

    [['FR', 'Clipperton'], ['FR', 'Centre-Val de Loire'], ['FR', 'Grand-Est'], ['FR', 'Guyane (française)'],
     ['FR', 'Guadeloupe'], ['FR', 'Guadeloupe'], ['FR', 'Hauts-de-France'], ['FR', 'Île-de-France'],
     ['FR', 'La Réunion'], ['FR', 'Mayotte'], ['FR', 'Saint-Martin'], ['FR', 'Martinique'],
     ['FR', 'Nouvelle-Aquitaine'], ['FR', 'Nouvelle-Calédonie'], ['FR', 'Normandie'], ['FR', 'Occitanie'],
     ['FR', 'Provence-Alpes-Côte-d’Azur'], ['FR', 'Pays-de-la-Loire'], ['FR', 'Polynésie française'],
     ['FR', 'Saint-Pierre-et-Miquelon'], ['FR', 'La Réunion'], ['FR', 'Terres australes françaises'],
     ['FR', 'Wallis-et-Futuna'], ['FR', 'Mayotte'], ['FR', 'Ain'], ['FR', 'Aisne'], ['FR', 'Allier'],
     ['FR', 'Alpes-de-Haute-Provence'], ['FR', 'Hautes-Alpes'], ['FR', 'Alpes-Maritimes'], ['FR', 'Ardèche'],
     ['FR', 'Ardennes'], ['FR', 'Ariège'], ['FR', 'Aube'], ['FR', 'Aude'], ['FR', 'Aveyron'],
     ['FR', 'Bouches-du-Rhône'], ['FR', 'Calvados'], ['FR', 'Cantal'], ['FR', 'Charente'],
     ['FR', 'Charente-Maritime'], ['FR', 'Cher'], ['FR', 'Corrèze'], ['FR', "Côte-d'Or"], ['FR', 'Orne'],
     ['FR', "Côtes-d'Armor"], ['FR', 'Pas-de-Calais'], ['FR', 'Creuse'], ['FR', 'Puy-de-Dôme'], ['FR', 'Dordogne'],
     ['FR', 'Pyrénées-Atlantiques'], ['FR', 'Doubs'], ['FR', 'Hautes-Pyrénées'], ['FR', 'Drôme'],
     ['FR', 'Pyrénées-Orientales'], ['FR', 'Eure'], ['FR', 'Bas-Rhin'], ['FR', 'Eure-et-Loir'], ['FR', 'Haut-Rhin'],
     ['FR', 'Finistère'], ['FR', 'Rhône'], ['FR', 'Corse-du-Sud'], ['FR', 'Haute-Saône'], ['FR', 'Haute-Corse'],
     ['FR', 'Saône-et-Loire'], ['FR', 'Gard'], ['FR', 'Sarthe'], ['FR', 'Haute-Garonne'], ['FR', 'Savoie'],
     ['FR', 'Gers'], ['FR', 'Haute-Savoie'], ['FR', 'Gironde'], ['FR', 'Paris'], ['FR', 'Hérault'],
     ['FR', 'Seine-Maritime'], ['FR', 'Ille-et-Vilaine'], ['FR', 'Seine-et-Marne'], ['FR', 'Indre'],
     ['FR', 'Yvelines'], ['FR', 'Indre-et-Loire'], ['FR', 'Deux-Sèvres'], ['FR', 'Isère'], ['FR', 'Somme'],
     ['FR', 'Jura'], ['FR', 'Tarn'], ['FR', 'Landes'], ['FR', 'Tarn-et-Garonne'], ['FR', 'Loir-et-Cher'],
     ['FR', 'Var'], ['FR', 'Loire'], ['FR', 'Vaucluse'], ['FR', 'Haute-Loire'], ['FR', 'Vendée'],
     ['FR', 'Loire-Atlantique'], ['FR', 'Vienne'], ['FR', 'Loiret'], ['FR', 'Haute-Vienne'], ['FR', 'Lot'],
     ['FR', 'Vosges'], ['FR', 'Lot-et-Garonne'], ['FR', 'Yonne'], ['FR', 'Lozère'], ['FR', 'Territoire de Belfort'],
     ['FR', 'Maine-et-Loire'], ['FR', 'Essonne'], ['FR', 'Manche'], ['FR', 'Hauts-de-Seine'], ['FR', 'Marne'],
     ['FR', 'Seine-Saint-Denis'], ['FR', 'Haute-Marne'], ['FR', 'Val-de-Marne'], ['FR', 'Mayenne'],
     ['FR', "Val-d'Oise"], ['FR', 'Meurthe-et-Moselle'], ['FR', 'Auvergne-Rhône-Alpes'], ['FR', 'Meuse'],
     ['FR', 'Bourgogne-Franche-Comté'], ['FR', 'Morbihan'], ['FR', 'Moselle'], ['FR', 'Saint-Barthélemy'],
     ['FR', 'Nièvre'], ['FR', 'Bretagne'], ['FR', 'Nord'], ['FR', 'Corse'], ['FR', 'Oise']],

    [['FM', 'Pohnpei'], ['FM', 'Kosrae'], ['FM', 'Yap'], ['FM', 'Chuuk']],

    [['GA', 'Woleu-Ntem'], ['GA', 'Ngounié'], ['GA', 'Nyanga'], ['GA', 'Ogooué-Ivindo'], ['GA', 'Estuaire'],
     ['GA', 'Haut-Ogooué'], ['GA', 'Ogooué-Lolo'], ['GA', 'Moyen-Ogooué'], ['GA', 'Ogooué-Maritime']],

    [['GB', 'Doncaster'], ['GB', 'West Sussex'], ['GB', 'Dundee City'], ['GB', 'York'], ['GB', 'Dorset'],
     ['GB', 'Shetland Islands'], ['GB', 'Derry and Strabane'], ['GB', 'Dudley'], ['GB', 'Durham County'],
     ['GB', 'Ealing'], ['GB', 'England and Wales'], ['GB', 'East Ayrshire'], ['GB', 'Edinburgh, City of'],
     ['GB', 'East Dunbartonshire'], ['GB', 'East Lothian'], ['GB', 'Eilean Siar'], ['GB', 'Enfield'],
     ['GB', 'England'], ['GB', 'East Renfrewshire'], ['GB', 'East Riding of Yorkshire'], ['GB', 'Essex'],
     ['GB', 'East Sussex'], ['GB', 'Falkirk'], ['GB', 'Fife'], ['GB', 'Flintshire; Sir y Fflint'],
     ['GB', 'Fermanagh and Omagh'], ['GB', 'Gateshead'], ['GB', 'Great Britain'], ['GB', 'Glasgow City'],
     ['GB', 'Blackburn with Darwen'], ['GB', 'Gloucestershire'], ['GB', 'Greenwich'], ['GB', 'Gwynedd'],
     ['GB', 'Halton'], ['GB', 'Hampshire'], ['GB', 'Bedford'], ['GB', 'Havering'], ['GB', 'Hackney'],
     ['GB', 'Herefordshire'], ['GB', 'Hillingdon'], ['GB', 'Highland'], ['GB', 'Hammersmith and Fulham'],
     ['GB', 'Hounslow'], ['GB', 'Hartlepool'], ['GB', 'Hertfordshire'], ['GB', 'Harrow'], ['GB', 'Haringey'],
     ['GB', 'Barking and Dagenham'], ['GB', 'Isles of Scilly'], ['GB', 'Newry, Mourne and Down'],
     ['GB', 'North Somerset'], ['GB', 'Solihull'], ['GB', 'Brent'], ['GB', 'Isle of Wight'],
     ['GB', 'Northamptonshire'], ['GB', 'Somerset'], ['GB', 'Bexley'], ['GB', 'Islington'],
     ['GB', 'Neath Port Talbot; Castell-nedd Port Talbot'], ['GB', 'Southend-on-Sea'], ['GB', 'Belfast'],
     ['GB', 'Inverclyde'], ['GB', 'Nottinghamshire'], ['GB', 'Surrey'], ['GB', 'Bridgend; Pen-y-bont ar Ogwr'],
     ['GB', 'Kensington and Chelsea'], ['GB', 'North Tyneside'], ['GB', 'Stoke-on-Trent'], ['GB', 'Blaenau Gwent'],
     ['GB', 'Kent'], ['GB', 'Newham'], ['GB', 'Stirling'], ['GB', 'Birmingham'], ['GB', 'Kingston upon Hull'],
     ['GB', 'Newport; Casnewydd'], ['GB', 'Southampton'], ['GB', 'Buckinghamshire'], ['GB', 'Kirklees'],
     ['GB', 'North Yorkshire'], ['GB', 'Sutton'], ['GB', 'Bournemouth'], ['GB', 'Kingston upon Thames'],
     ['GB', 'Oldham'], ['GB', 'Staffordshire'], ['GB', 'Barnet'], ['GB', 'Knowsley'], ['GB', 'Orkney Islands'],
     ['GB', 'Stockton-on-Tees'], ['GB', 'Brighton and Hove'], ['GB', 'Lancashire'], ['GB', 'Oxfordshire'],
     ['GB', 'South Tyneside'], ['GB', 'Barnsley'], ['GB', 'Lisburn and Castlereagh'],
     ['GB', 'Pembrokeshire; Sir Benfro'], ['GB', 'Swansea; Abertawe'], ['GB', 'Bolton'], ['GB', 'Lambeth'],
     ['GB', 'Perth and Kinross'], ['GB', 'Swindon'], ['GB', 'Blackpool'], ['GB', 'Leicester'], ['GB', 'Plymouth'],
     ['GB', 'Southwark'], ['GB', 'Bracknell Forest'], ['GB', 'Leeds'], ['GB', 'Poole'], ['GB', 'Tameside'],
     ['GB', 'Bradford'], ['GB', 'Leicestershire'], ['GB', 'North Lincolnshire'], ['GB', 'Portsmouth'],
     ['GB', 'Telford and Wrekin'], ['GB', 'Bromley'], ['GB', 'Lewisham'], ['GB', 'Powys'], ['GB', 'Thurrock'],
     ['GB', 'Bristol, City of'], ['GB', 'Lincolnshire'], ['GB', 'Peterborough'], ['GB', 'Torbay'], ['GB', 'Bury'],
     ['GB', 'Liverpool'], ['GB', 'Redcar and Cleveland'], ['GB', 'Torfaen; Tor-faen'], ['GB', 'Cambridgeshire'],
     ['GB', 'London, City of'], ['GB', 'Rochdale'], ['GB', 'Trafford'], ['GB', 'Caerphilly; Caerffili'],
     ['GB', 'Luton'], ['GB', 'Rhondda, Cynon, Taff; Rhondda, Cynon, Taf'], ['GB', 'Tower Hamlets'],
     ['GB', 'South Lanarkshire'], ['GB', 'Central Bedfordshire'], ['GB', 'Manchester'], ['GB', 'Redbridge'],
     ['GB', 'United Kingdom'], ['GB', 'Causeway Coast and Glens'], ['GB', 'Middlesbrough'], ['GB', 'Reading'],
     ['GB', 'Vale of Glamorgan, The; Bro Morgannwg'], ['GB', 'Ceredigion; Sir Ceredigion'], ['GB', 'Medway'],
     ['GB', 'Renfrewshire'], ['GB', 'Cheshire East'], ['GB', 'Mid and East Antrim'], ['GB', 'Richmond upon Thames'],
     ['GB', 'Warwickshire'], ['GB', 'Cheshire West and Chester'], ['GB', 'Milton Keynes'], ['GB', 'Rotherham'],
     ['GB', 'West Berkshire'], ['GB', 'Sunderland'], ['GB', 'West Dunbartonshire'], ['GB', 'Calderdale'],
     ['GB', 'Midlothian'], ['GB', 'Rutland'], ['GB', 'Waltham Forest'], ['GB', 'Clackmannanshire'],
     ['GB', 'Monmouthshire; Sir Fynwy'], ['GB', 'Sandwell'], ['GB', 'Wigan'], ['GB', 'Cumbria'], ['GB', 'Merton'],
     ['GB', 'South Ayrshire'], ['GB', 'Wiltshire'], ['GB', 'Wrexham; Wrecsam'], ['GB', 'Camden'], ['GB', 'Moray'],
     ['GB', 'Scottish Borders, The'], ['GB', 'Wakefield'], ['GB', 'Carmarthenshire; Sir Gaerfyrddin'],
     ['GB', 'Merthyr Tydfil; Merthyr Tudful'], ['GB', 'Scotland'], ['GB', 'Walsall'], ['GB', 'Cornwall'],
     ['GB', 'Mid Ulster'], ['GB', 'Suffolk'], ['GB', 'West Lothian'], ['GB', 'Coventry'], ['GB', 'North Ayrshire'],
     ['GB', 'Wales; Cymru'], ['GB', 'Armagh, Banbridge and Craigavon'], ['GB', 'Cardiff; Caerdydd'],
     ['GB', 'Northumberland'], ['GB', 'Sefton'], ['GB', 'Aberdeenshire'], ['GB', 'Wolverhampton'],
     ['GB', 'Westminster'], ['GB', 'Aberdeen City'], ['GB', 'Croydon'], ['GB', 'North East Lincolnshire'],
     ['GB', 'Argyll and Bute'], ['GB', 'South Gloucestershire'], ['GB', 'Sheffield'],
     ['GB', 'Isle of Anglesey; Sir Ynys Môn'], ['GB', 'Conwy'], ['GB', 'Newcastle upon Tyne'], ['GB', 'St. Helens'],
     ['GB', 'Wandsworth'], ['GB', 'Ards and North Down'], ['GB', 'Darlington'], ['GB', 'Norfolk'],
     ['GB', 'Shropshire'], ['GB', 'Windsor and Maidenhead'], ['GB', 'Wokingham'], ['GB', 'Antrim and Newtownabbey'],
     ['GB', 'Derbyshire'], ['GB', 'Nottingham'], ['GB', 'Stockport'], ['GB', 'Worcestershire'], ['GB', 'Angus'],
     ['GB', 'Denbighshire; Sir Ddinbych'], ['GB', 'Northern Ireland'], ['GB', 'Salford'], ['GB', 'Wirral'],
     ['GB', 'Bath and North East Somerset'], ['GB', 'Derby'], ['GB', 'North Lanarkshire'], ['GB', 'Slough'],
     ['GB', 'Warrington'], ['GB', 'Devon'], ['GB', 'Dumfries and Galloway']],

    [['GE', 'Shida K’art’li'], ['GE', 'Kakhet’i'], ['GE', 'Samegrelo-Zemo Svanet’i'], ['GE', 'K’vemo K’art’li'],
     ['GE', 'Abkhazia'], ['GE', 'T’bilisi'], ['GE', 'Mts’khet’a-Mt’ianet’i'], ['GE', 'Ajaria'],
     ['GE', 'Racha-Lech’khumi-K’vemo Svanet’i'], ['GE', 'Guria'], ['GE', 'Samts’khe-Javakhet’i'],
     ['GE', 'Imeret’i']],

    [['GH', 'Brong-Ahafo'], ['GH', 'Upper West'], ['GH', 'Central'], ['GH', 'Western'], ['GH', 'Eastern'],
     ['GH', 'Northern'], ['GH', 'Greater Accra'], ['GH', 'Volta'], ['GH', 'Ashanti'], ['GH', 'Upper East']],

    [['GN', 'Kindia'], ['GN', 'Kérouané'], ['GN', 'Koundara'], ['GN', 'Boké'], ['GN', 'Kouroussa'], ['GN', 'Beyla'],
     ['GN', 'Kissidougou'], ['GN', 'Boffa'], ['GN', 'Labé'], ['GN', 'Boké'], ['GN', 'Conakry'], ['GN', 'Labé'],
     ['GN', 'Coyah'], ['GN', 'Lélouma'], ['GN', 'Kindia'], ['GN', 'Lola'], ['GN', 'Dabola'], ['GN', 'Mamou'],
     ['GN', 'Macenta'], ['GN', 'Dinguiraye'], ['GN', 'Dalaba'], ['GN', 'Dubréka'], ['GN', 'Mandiana'],
     ['GN', 'Faranah'], ['GN', 'Mali'], ['GN', 'Faranah'], ['GN', 'Mamou'], ['GN', 'Nzérékoré'],
     ['GN', 'Nzérékoré'], ['GN', 'Forécariah'], ['GN', 'Fria'], ['GN', 'Gaoual'], ['GN', 'Pita'],
     ['GN', 'Guékédou'], ['GN', 'Siguiri'], ['GN', 'Kankan'], ['GN', 'Télimélé'], ['GN', 'Tougué'],
     ['GN', 'Kankan'], ['GN', 'Yomou'], ['GN', 'Koubia']],

    [['GM', 'Upper River'], ['GM', 'Banjul'], ['GM', 'Western'], ['GM', 'Lower River'], ['GM', 'Central River'],
     ['GM', 'North Bank']],

    [['GW', 'Cacheu'], ['GW', 'Quinara'], ['GW', 'Sul'], ['GW', 'Gabú'], ['GW', 'Tombali'], ['GW', 'Bafatá'],
     ['GW', 'Leste'], ['GW', 'Norte'], ['GW', 'Bolama'], ['GW', 'Biombo'], ['GW', 'Bissau'], ['GW', 'Oio']],

    [['GQ', 'Región Insular'], ['GQ', 'Bioko Norte'], ['GQ', 'Kié-Ntem'], ['GQ', 'Bioko Sur'], ['GQ', 'Litoral'],
     ['GQ', 'Región Continental'], ['GQ', 'Wele-Nzas'], ['GQ', 'Centro Sur'], ['GQ', 'Annobón']],

    [['GR', 'Zakynthos'], ['GR', 'Dytiki Makedonia'], ['GR', 'Pieria'], ['GR', 'Kerkyra'], ['GR', 'Ipeiros'],
     ['GR', 'Serres'], ['GR', 'Kefallonia'], ['GR', 'Florina'], ['GR', 'Thessalia'], ['GR', 'Lefkada'],
     ['GR', 'Chalkidiki'], ['GR', 'Ionia Nisia'], ['GR', 'Arta'], ['GR', 'Agio Oros'], ['GR', 'Dytiki Ellada'],
     ['GR', 'Thesprotia'], ['GR', 'Evros'], ['GR', 'Sterea Ellada'], ['GR', 'Ioannina'], ['GR', 'Attiki'],
     ['GR', 'Preveza'], ['GR', 'Xanthi'], ['GR', 'Peloponnisos'], ['GR', 'Karditsa'], ['GR', 'Rodopi'],
     ['GR', 'Voreio Aigaio'], ['GR', 'Aitolia kai Akarnania'], ['GR', 'Larisa'], ['GR', 'Dodekanisos'],
     ['GR', 'Voiotia'], ['GR', 'Kyklades'], ['GR', 'Kentriki Makedonia'], ['GR', 'Notio Aigaio'],
     ['GR', 'Magnisia'], ['GR', 'Evvoias'], ['GR', 'Lesvos'], ['GR', 'Kriti'], ['GR', 'Trikala'],
     ['GR', 'Evrytania'], ['GR', 'Samos'], ['GR', 'Grevena'], ['GR', 'Fthiotida'], ['GR', 'Chios'], ['GR', 'Drama'],
     ['GR', 'Fokida'], ['GR', 'Irakleio'], ['GR', 'Imathia'], ['GR', 'Argolida'], ['GR', 'Lasithi'],
     ['GR', 'Thessaloniki'], ['GR', 'Arkadia'], ['GR', 'Rethymno'], ['GR', 'Kavala'], ['GR', 'Achaïa'],
     ['GR', 'Chania'], ['GR', 'Kastoria'], ['GR', 'Ileia'], ['GR', 'Anatoliki Makedonia kai Thraki'],
     ['GR', 'Kilkis'], ['GR', 'Korinthia'], ['GR', 'Attiki'], ['GR', 'Kozani'], ['GR', 'Lakonia'], ['GR', 'Pella'],
     ['GR', 'Messinia']],

    [['GD', 'Saint Patrick'], ['GD', 'Southern Grenadine Islands'], ['GD', 'Saint George'], ['GD', 'Saint John'],
     ['GD', 'Saint Andrew'], ['GD', 'Saint Mark'], ['GD', 'Saint David']],

    [['GL', 'Kommune Kujalleq'], ['GL', 'Kommuneqarfik Sermersooq'], ['GL', 'Qeqqata Kommunia'],
     ['GL', 'Qaasuitsup Kommunia']],

    [['GT', 'Jutiapa'], ['GT', 'Petén'], ['GT', 'El Progreso'], ['GT', 'Quiché'], ['GT', 'Quetzaltenango'],
     ['GT', 'Retalhuleu'], ['GT', 'Sacatepéquez'], ['GT', 'San Marcos'], ['GT', 'Sololá'], ['GT', 'Santa Rosa'],
     ['GT', 'Suchitepéquez'], ['GT', 'Totonicapán'], ['GT', 'Alta Verapaz'], ['GT', 'Zacapa'],
     ['GT', 'Baja Verapaz'], ['GT', 'Chimaltenango'], ['GT', 'Chiquimula'], ['GT', 'Escuintla'],
     ['GT', 'Guatemala'], ['GT', 'Huehuetenango'], ['GT', 'Izabal'], ['GT', 'Jalapa']],

    [['GY', 'Barima-Waini'], ['GY', 'Mahaica-Berbice'], ['GY', 'Cuyuni-Mazaruni'], ['GY', 'Pomeroon-Supenaam'],
     ['GY', 'Demerara-Mahaica'], ['GY', 'Potaro-Siparuni'], ['GY', 'Upper Demerara-Berbice'],
     ['GY', 'East Berbice-Corentyne'], ['GY', 'Upper Takutu-Upper Essequibo'],
     ['GY', 'Essequibo Islands-West Demerara']],

    [['HN', 'Yoro'], ['HN', 'Colón'], ['HN', 'La Paz'], ['HN', 'Francisco Morazán'], ['HN', 'Comayagua'],
     ['HN', 'Ocotepeque'], ['HN', 'Gracias a Dios'], ['HN', 'Valle'], ['HN', 'Copán'], ['HN', 'Olancho'],
     ['HN', 'Islas de la Bahía'], ['HN', 'Cortés'], ['HN', 'Lempira'], ['HN', 'Atlántida'], ['HN', 'Intibucá'],
     ['HN', 'Santa Bárbara'], ['HN', 'El Paraíso'], ['HN', 'Choluteca']],

    [['HR', 'Požeško-slavonska županija'], ['HR', 'Brodsko-posavska županija'], ['HR', 'Zadarska županija'],
     ['HR', 'Osječko-baranjska županija'], ['HR', 'Šibensko-kninska županija'],
     ['HR', 'Vukovarsko-srijemska županija'], ['HR', 'Splitsko-dalmatinska županija'], ['HR', 'Istarska županija'],
     ['HR', 'Dubrovačko-neretvanska županija'], ['HR', 'Međimurska županija'], ['HR', 'Grad Zagreb'],
     ['HR', 'Zagrebačka županija'], ['HR', 'Krapinsko-zagorska županija'], ['HR', 'Sisačko-moslavačka županija'],
     ['HR', 'Karlovačka županija'], ['HR', 'Varaždinska županija'], ['HR', 'Koprivničko-križevačka županija'],
     ['HR', 'Bjelovarsko-bilogorska županija'], ['HR', 'Primorsko-goranska županija'],
     ['HR', 'Ličko-senjska županija'], ['HR', 'Virovitičko-podravska županija']],

    [['HT', 'Nord-Ouest'], ['HT', 'Artibonite'], ['HT', 'Ouest'], ['HT', 'Centre'], ['HT', 'Sud'],
     ['HT', 'Grande-Anse'], ['HT', 'Sud-Est'], ['HT', 'Nord'], ['HT', 'Nord-Est']],

    [['HU', 'Nagykanizsa'], ['HU', 'Békéscsaba'], ['HU', 'Nógrád'], ['HU', 'Békés'], ['HU', 'Zalaegerszeg'],
     ['HU', 'Nyíregyháza'], ['HU', 'Bács-Kiskun'], ['HU', 'Pest'], ['HU', 'Budapest'], ['HU', 'Pécs'],
     ['HU', 'Borsod-Abaúj-Zemplén'], ['HU', 'Szeged'], ['HU', 'Csongrád'], ['HU', 'Székesfehérvár'],
     ['HU', 'Debrecen'], ['HU', 'Szombathely'], ['HU', 'Dunaújváros'], ['HU', 'Szolnok'], ['HU', 'Eger'],
     ['HU', 'Sopron'], ['HU', 'Érd'], ['HU', 'Somogy'], ['HU', 'Fejér'], ['HU', 'Szekszárd'],
     ['HU', 'Győr-Moson-Sopron'], ['HU', 'Salgótarján'], ['HU', 'Győr'], ['HU', 'Szabolcs-Szatmár-Bereg'],
     ['HU', 'Hajdú-Bihar'], ['HU', 'Tatabánya'], ['HU', 'Heves'], ['HU', 'Tolna'], ['HU', 'Hódmezővásárhely'],
     ['HU', 'Vas'], ['HU', 'Jász-Nagykun-Szolnok'], ['HU', 'Veszprém (county)'], ['HU', 'Komárom-Esztergom'],
     ['HU', 'Veszprém'], ['HU', 'Kecskemét'], ['HU', 'Zala'], ['HU', 'Kaposvár'], ['HU', 'Baranya'],
     ['HU', 'Miskolc']],

    [['ID', 'Aceh'], ['ID', 'Bali'], ['ID', 'Nusa Tenggara Barat'], ['ID', 'Bangka Belitung'], ['ID', 'Bengkulu'],
     ['ID', 'Nusa Tenggara Timur'], ['ID', 'Banten'], ['ID', 'Nusa Tenggara'], ['ID', 'Papua'], ['ID', 'Gorontalo'],
     ['ID', 'Papua'], ['ID', 'Papua Barat'], ['ID', 'Jambi'], ['ID', 'Riau'], ['ID', 'Sulawesi Utara'],
     ['ID', 'Sumatra Barat'], ['ID', 'Jawa Barat'], ['ID', 'Sulawesi Tenggara'], ['ID', 'Jawa Timur'],
     ['ID', 'Jakarta Raya'], ['ID', 'Sulawesi'], ['ID', 'Jawa Tengah'], ['ID', 'Sumatera'], ['ID', 'Jawa'],
     ['ID', 'Kalimantan'], ['ID', 'Sulawesi Selatan'], ['ID', 'Kalimantan Barat'], ['ID', 'Sulawesi Barat'],
     ['ID', 'Sumatra Selatan'], ['ID', 'Sulawesi Tengah'], ['ID', 'Kalimantan Timur'], ['ID', 'Sumatera Utara'],
     ['ID', 'Kepulauan Riau'], ['ID', 'Kalimantan Selatan'], ['ID', 'Yogyakarta'], ['ID', 'Kalimantan Tengah'],
     ['ID', 'Lampung'], ['ID', 'Maluku'], ['ID', 'Maluku'], ['ID', 'Maluku Utara']],

    [['IN', 'Sikkim'], ['IN', 'Delhi'], ['IN', 'Telangana'], ['IN', 'Dadra and Nagar Haveli'], ['IN', 'Tamil Nadu'],
     ['IN', 'Goa'], ['IN', 'Tripura'], ['IN', 'Gujarat'], ['IN', 'Uttar Pradesh'], ['IN', 'Himachal Pradesh'],
     ['IN', 'Uttarakhand'], ['IN', 'Haryana'], ['IN', 'West Bengal'], ['IN', 'Jharkhand'],
     ['IN', 'Jammu and Kashmir'], ['IN', 'Karnataka'], ['IN', 'Kerala'], ['IN', 'Lakshadweep'],
     ['IN', 'Maharashtra'], ['IN', 'Meghalaya'], ['IN', 'Andaman and Nicobar Islands'], ['IN', 'Manipur'],
     ['IN', 'Andhra Pradesh'], ['IN', 'Madhya Pradesh'], ['IN', 'Arunachal Pradesh'], ['IN', 'Mizoram'],
     ['IN', 'Assam'], ['IN', 'Nagaland'], ['IN', 'Bihar'], ['IN', 'Odisha'], ['IN', 'Chandigarh'], ['IN', 'Punjab'],
     ['IN', 'Chhattisgarh'], ['IN', 'Puducherry'], ['IN', 'Daman and Diu'], ['IN', 'Rajasthan']],

    [['IE', 'Ulster'], ['IE', 'Cork'], ['IE', 'Carlow'], ['IE', 'Waterford'], ['IE', 'Dublin'], ['IE', 'Donegal'],
     ['IE', 'Westmeath'], ['IE', 'Galway'], ['IE', 'Wicklow'], ['IE', 'Kildare'], ['IE', 'Wexford'],
     ['IE', 'Kilkenny'], ['IE', 'Kerry'], ['IE', 'Leinster'], ['IE', 'Longford'], ['IE', 'Louth'],
     ['IE', 'Limerick'], ['IE', 'Leitrim'], ['IE', 'Laois'], ['IE', 'Munster'], ['IE', 'Meath'], ['IE', 'Monaghan'],
     ['IE', 'Connacht'], ['IE', 'Mayo'], ['IE', 'Offaly'], ['IE', 'Clare'], ['IE', 'Roscommon'], ['IE', 'Sligo'],
     ['IE', 'Cavan'], ['IE', 'Tipperary']],

    [['IR', 'Gīlān'], ['IR', 'Lorestān'], ['IR', 'Māzandarān'], ['IR', 'Markazī'], ['IR', 'Hormozgān'],
     ['IR', 'Āzarbāyjān-e Sharqī'], ['IR', 'Hamadān'], ['IR', 'Āzarbāyjān-e Gharbī'], ['IR', 'Yazd'],
     ['IR', 'Ardabīl'], ['IR', 'Qom'], ['IR', 'Eşfahān'], ['IR', 'Golestān'], ['IR', 'Īlām'], ['IR', 'Qazvīn'],
     ['IR', 'Būshehr'], ['IR', 'Khorāsān-e Janūbī'], ['IR', 'Tehrān'], ['IR', 'Khorāsān-e Razavī'],
     ['IR', 'Chahār Mahāll va Bakhtīārī'], ['IR', 'Khorāsān-e Shemālī'], ['IR', 'Khūzestān'], ['IR', 'Zanjān'],
     ['IR', 'Semnān'], ['IR', 'Sīstān va Balūchestān'], ['IR', 'Fārs'], ['IR', 'Kermān'], ['IR', 'Kordestān'],
     ['IR', 'Kermānshāh'], ['IR', 'Kohgīlūyeh va Būyer Ahmad']],

    [['IQ', 'Maysan'], ['IQ', 'Baghdad'], ['IQ', 'Salah ad Din'], ['IQ', 'Al Muthanna'], ['IQ', 'Dahuk'],
     ['IQ', 'As Sulaymaniyah'], ['IQ', 'Al Anbar'], ['IQ', 'An Najef'], ['IQ', 'Diyala'], ['IQ', "At Ta'mim"],
     ['IQ', 'Arbil'], ['IQ', 'Ninawa'], ['IQ', 'Dhi Qar'], ['IQ', 'Wasit'], ['IQ', 'Al Basrah'],
     ['IQ', 'Al Qadisiyah'], ['IQ', "Karbala'"], ['IQ', 'Babil']],

    [['IS', 'Vesturland'], ['IS', 'Suðurland'], ['IS', 'Vestfirðir'], ['IS', 'Norðurland vestra'],
     ['IS', 'Reykjavík'], ['IS', 'Norðurland eystra'], ['IS', 'Höfuðborgarsvæðið'], ['IS', 'Austurland'],
     ['IS', 'Suðurnes']],

    [['IL', 'HaDarom'], ['IL', 'Tel-Aviv'], ['IL', 'Hefa'], ['IL', 'HaZafon'], ['IL', 'Yerushalayim Al Quds'],
     ['IL', 'HaMerkaz']],

    [['IT', 'Carbonia-Iglesias'], ['IT', 'Medio Campidano'], ['IT', 'Caltanissetta'], ['IT', 'Viterbo'],
     ['IT', 'Cuneo'], ['IT', 'Vibo Valentia'], ['IT', 'Como'], ['IT', 'Cremona'], ['IT', 'Cosenza'],
     ['IT', 'Catania'], ['IT', 'Catanzaro'], ['IT', 'Enna'], ['IT', 'Forlì-Cesena'], ['IT', 'Ferrara'],
     ['IT', 'Foggia'], ['IT', 'Firenze'], ['IT', 'Fermo'], ['IT', 'Frosinone'], ['IT', 'Genova'], ['IT', 'Gorizia'],
     ['IT', 'Grosseto'], ['IT', 'Imperia'], ['IT', 'Isernia'], ['IT', 'Crotone'], ['IT', 'Lecco'], ['IT', 'Lecce'],
     ['IT', 'Livorno'], ['IT', 'Lodi'], ['IT', 'Latina'], ['IT', 'Lucca'], ['IT', 'Monza e Brianza'],
     ['IT', 'Macerata'], ['IT', 'Messina'], ['IT', 'Milano'], ['IT', 'Mantova'], ['IT', 'Modena'],
     ['IT', 'Massa-Carrara'], ['IT', 'Matera'], ['IT', 'Napoli'], ['IT', 'Novara'], ['IT', 'Nuoro'],
     ['IT', 'Ogliastra'], ['IT', 'Oristano'], ['IT', 'Olbia-Tempio'], ['IT', 'Palermo'], ['IT', 'Piacenza'],
     ['IT', 'Piemonte'], ['IT', 'Padova'], ['IT', "Valle d'Aosta"], ['IT', 'Pescara'], ['IT', 'Lombardia'],
     ['IT', 'Perugia'], ['IT', 'Trentino-Alto Adige'], ['IT', 'Pisa'], ['IT', 'Veneto'], ['IT', 'Pordenone'],
     ['IT', 'Friuli-Venezia Giulia'], ['IT', 'Prato'], ['IT', 'Liguria'], ['IT', 'Parma'], ['IT', 'Vicenza'],
     ['IT', 'Emilia-Romagna'], ['IT', 'Pistoia'], ['IT', 'Toscana'], ['IT', 'Pesaro e Urbino'], ['IT', 'Umbria'],
     ['IT', 'Pavia'], ['IT', 'Marche'], ['IT', 'Potenza'], ['IT', 'Lazio'], ['IT', 'Ravenna'], ['IT', 'Verona'],
     ['IT', 'Abruzzo'], ['IT', 'Reggio Calabria'], ['IT', 'Molise'], ['IT', 'Reggio Emilia'], ['IT', 'Campania'],
     ['IT', 'Ragusa'], ['IT', 'Puglia'], ['IT', 'Rieti'], ['IT', 'Basilicata'], ['IT', 'Roma'], ['IT', 'Calabria'],
     ['IT', 'Rimini'], ['IT', 'Sicilia'], ['IT', 'Rovigo'], ['IT', 'Sardegna'], ['IT', 'Salerno'],
     ['IT', 'Agrigento'], ['IT', 'Siena'], ['IT', 'Alessandria'], ['IT', 'Ancona'], ['IT', 'Sondrio'],
     ['IT', 'Aosta'], ['IT', 'Ascoli Piceno'], ['IT', 'La Spezia'], ['IT', "L'Aquila"], ['IT', 'Siracusa'],
     ['IT', 'Arezzo'], ['IT', 'Sassari'], ['IT', 'Asti'], ['IT', 'Savona'], ['IT', 'Avellino'], ['IT', 'Taranto'],
     ['IT', 'Bari'], ['IT', 'Teramo'], ['IT', 'Bergamo'], ['IT', 'Trento'], ['IT', 'Biella'], ['IT', 'Torino'],
     ['IT', 'Belluno'], ['IT', 'Trapani'], ['IT', 'Benevento'], ['IT', 'Terni'], ['IT', 'Bologna'],
     ['IT', 'Trieste'], ['IT', 'Brindisi'], ['IT', 'Treviso'], ['IT', 'Brescia'], ['IT', 'Udine'],
     ['IT', 'Barletta-Andria-Trani'], ['IT', 'Varese'], ['IT', 'Bolzano'], ['IT', 'Verbano-Cusio-Ossola'],
     ['IT', 'Cagliari'], ['IT', 'Vercelli'], ['IT', 'Campobasso'], ['IT', 'Venezia'], ['IT', 'Caserta'],
     ['IT', 'Chieti']],

    [['JM', 'Saint Ann'], ['JM', 'Manchester'], ['JM', 'Trelawny'], ['JM', 'Clarendon'], ['JM', 'Saint Thomas'],
     ['JM', 'Saint James'], ['JM', 'Saint Catherine'], ['JM', 'Hanover'], ['JM', 'Portland'],
     ['JM', 'Westmoreland'], ['JM', 'Kingston'], ['JM', 'Saint Mary'], ['JM', 'Saint Elizabeth'],
     ['JM', 'Saint Andrew']],

    [['JO', 'Jarash'], ['JO', 'Al ‘Aqabah'], ['JO', 'Al Karak'], ['JO', 'Aţ Ţafīlah'], ['JO', 'Al Mafraq'],
     ['JO', "Az Zarqā'"], ['JO', 'Mādabā'], ['JO', "Al Balqā'"], ['JO', '‘Ajlūn'], ['JO', 'Ma‘ān'], ['JO', 'Irbid'],
     ['JO', '‘Ammān (Al ‘Aşimah)']],

    [['JP', 'Okayama'], ['JP', 'Chiba'], ['JP', 'Hiroshima'], ['JP', 'Tokyo'], ['JP', 'Yamaguchi'],
     ['JP', 'Kanagawa'], ['JP', 'Tokushima'], ['JP', 'Niigata'], ['JP', 'Kagawa'], ['JP', 'Toyama'],
     ['JP', 'Ehime'], ['JP', 'Ishikawa'], ['JP', 'Kochi'], ['JP', 'Fukui'], ['JP', 'Fukuoka'], ['JP', 'Yamanashi'],
     ['JP', 'Saga'], ['JP', 'Nagano'], ['JP', 'Nagasaki'], ['JP', 'Gifu'], ['JP', 'Hokkaido'], ['JP', 'Kumamoto'],
     ['JP', 'Shizuoka'], ['JP', 'Aomori'], ['JP', 'Oita'], ['JP', 'Aichi'], ['JP', 'Iwate'], ['JP', 'Miyazaki'],
     ['JP', 'Mie'], ['JP', 'Miyagi'], ['JP', 'Kagoshima'], ['JP', 'Shiga'], ['JP', 'Akita'], ['JP', 'Okinawa'],
     ['JP', 'Kyoto'], ['JP', 'Yamagata'], ['JP', 'Osaka'], ['JP', 'Fukushima'], ['JP', 'Hyogo'], ['JP', 'Ibaraki'],
     ['JP', 'Nara'], ['JP', 'Tochigi'], ['JP', 'Wakayama'], ['JP', 'Gunma'], ['JP', 'Tottori'], ['JP', 'Saitama'],
     ['JP', 'Shimane']],

    [['KZ', 'Qyzylorda oblysy'], ['KZ', 'Almaty oblysy'], ['KZ', 'Batys Quzaqstan oblysy'],
     ['KZ', 'Mangghystaū oblysy'], ['KZ', 'Astana'], ['KZ', 'Zhambyl oblysy'], ['KZ', 'Pavlodar oblysy'],
     ['KZ', 'Atyraū oblysy'], ['KZ', 'Aqmola oblysy'], ['KZ', 'Soltüstik Quzaqstan oblysy'],
     ['KZ', 'Qaraghandy oblysy'], ['KZ', 'Aqtöbe oblysy'], ['KZ', 'Shyghys Qazaqstan oblysy'],
     ['KZ', 'Qostanay oblysy'], ['KZ', 'Almaty'], ['KZ', 'Ongtüstik Qazaqstan oblysy']],

    [['KE', 'Mombasa'], ['KE', 'Garissa'], ['KE', "Murang'a"], ['KE', 'Homa Bay'], ['KE', 'Nairobi City'],
     ['KE', 'Isiolo'], ['KE', 'Nakuru'], ['KE', 'Kajiado'], ['KE', 'Nandi'], ['KE', 'Kakamega'], ['KE', 'Narok'],
     ['KE', 'Kericho'], ['KE', 'Nyamira'], ['KE', 'Kiambu'], ['KE', 'Nyandarua'], ['KE', 'Kilifi'], ['KE', 'Nyeri'],
     ['KE', 'Kirinyaga'], ['KE', 'Samburu'], ['KE', 'Kisii'], ['KE', 'Siaya'], ['KE', 'Kisumu'],
     ['KE', 'Taita/Taveta'], ['KE', 'Kitui'], ['KE', 'Tana River'], ['KE', 'Kwale'], ['KE', 'Tharaka-Nithi'],
     ['KE', 'Laikipia'], ['KE', 'Trans Nzoia'], ['KE', 'Lamu'], ['KE', 'Baringo'], ['KE', 'Turkana'],
     ['KE', 'Machakos'], ['KE', 'Bomet'], ['KE', 'Uasin Gishu'], ['KE', 'Makueni'], ['KE', 'Bungoma'],
     ['KE', 'Vihiga'], ['KE', 'Mandera'], ['KE', 'Busia'], ['KE', 'Wajir'], ['KE', 'Marsabit'],
     ['KE', 'Elgeyo/Marakwet'], ['KE', 'West Pokot'], ['KE', 'Meru'], ['KE', 'Embu'], ['KE', 'Migori']],

    [['KG', 'Talas'], ['KG', 'Chü'], ['KG', 'Ysyk-Köl'], ['KG', 'Bishkek'], ['KG', 'Jalal-Abad'], ['KG', 'Naryn'],
     ['KG', 'Batken'], ['KG', 'Osh']],

    [['KH', 'Otdar Mean Chey'], ['KH', 'Krong Kaeb'], ['KH', 'Krong Pailin'], ['KH', 'Kampong Cham'],
     ['KH', 'Kampong Chhnang'], ['KH', 'Kampong Speu'], ['KH', 'Kampong Thom'], ['KH', 'Kampot'],
     ['KH', 'Banteay Mean Chey'], ['KH', 'Kandal'], ['KH', 'Krachoh'], ['KH', 'Kach Kong'], ['KH', 'Mondol Kiri'],
     ['KH', 'Phnom Penh'], ['KH', 'Preah Vihear'], ['KH', 'Prey Veaeng'], ['KH', 'Pousaat'], ['KH', 'Rotanak Kiri'],
     ['KH', 'Siem Reab'], ['KH', 'Krong Preah Sihanouk'], ['KH', 'Stueng Traeng'], ['KH', 'Battambang'],
     ['KH', 'Svaay Rieng'], ['KH', 'Taakaev']],

    [['KI', 'Phoenix Islands'], ['KI', 'Line Islands'], ['KI', 'Gilbert Islands']],

    [['KN', 'Christ Church Nichola Town'], ['KN', 'Saint Thomas Middle Island'], ['KN', 'Saint Mary Cayon'],
     ['KN', 'Saint Anne Sandy Point'], ['KN', 'Saint George Basseterre'], ['KN', 'Trinity Palmetto Point'],
     ['KN', 'Saint Paul Capisterre'], ['KN', 'Saint George Gingerland'], ['KN', 'Saint James Windward'],
     ['KN', 'Saint Kitts'], ['KN', 'Saint Paul Charlestown'], ['KN', 'Nevis'], ['KN', 'Saint John Capisterre'],
     ['KN', 'Saint Peter Basseterre'], ['KN', 'Saint John Figtree'], ['KN', 'Saint Thomas Lowland']],

    [['KR', "Gwangju Gwang'yeogsi"], ['KR', 'Jejudo'], ['KR', 'Chungcheongnamdo'], ['KR', "Daejeon Gwang'yeogsi"],
     ['KR', 'Seoul Teugbyeolsi'], ['KR', 'Jeonrabukdo'], ['KR', "Ulsan Gwang'yeogsi"], ['KR', "Busan Gwang'yeogsi"],
     ['KR', 'Jeonranamdo'], ['KR', 'Gyeonggido'], ['KR', "Daegu Gwang'yeogsi"], ['KR', 'Gyeongsangbukdo'],
     ['KR', "Gang'weondo"], ['KR', "Incheon Gwang'yeogsi"], ['KR', 'Gyeongsangnamdo'], ['KR', 'Chungcheongbukdo']],

    [['KW', 'Al Kuwayt (Al ‘Āşimah)'], ['KW', 'Al Ahmadi'], ['KW', 'Mubārak al Kabīr'], ['KW', 'Al Farwānīyah'],
     ['KW', 'Hawallī'], ['KW', 'Al Jahrrā’']],

    [['LA', 'Oudômxai'], ['LA', 'Champasak'], ['LA', 'Xaignabouli'], ['LA', 'Phôngsali'], ['LA', 'Houaphan'],
     ['LA', 'Xékong'], ['LA', 'Salavan'], ['LA', 'Khammouan'], ['LA', 'Attapu'], ['LA', 'Xiangkhouang'],
     ['LA', 'Savannakhét'], ['LA', 'Louang Namtha'], ['LA', 'Bokèo'], ['LA', 'Xaisômboun'], ['LA', 'Vientiane'],
     ['LA', 'Louangphabang'], ['LA', 'Bolikhamxai'], ['LA', 'Vientiane']],

    [['LB', 'Liban-Nord'], ['LB', 'Mont-Liban'], ['LB', 'Beyrouth'], ['LB', 'Nabatîyé'], ['LB', 'Baalbek-Hermel'],
     ['LB', 'Béqaa'], ['LB', 'Liban-Sud'], ['LB', 'Aakkâr']],

    [['LR', 'Grand Kru'], ['LR', 'Bomi'], ['LR', 'Rivercess'], ['LR', 'Lofa'], ['LR', 'Sinoe'],
     ['LR', 'Grand Cape Mount'], ['LR', 'Margibi'], ['LR', 'Montserrado'], ['LR', 'Grand Bassa'],
     ['LR', 'Maryland'], ['LR', 'Grand Gedeh'], ['LR', 'Nimba'], ['LR', 'Bong']],

    [['LY', 'Al Jufrah'], ['LY', 'Al Kufrah'], ['LY', 'Al Marqab'], ['LY', 'Mişrātah'], ['LY', 'Al Marj'],
     ['LY', 'Murzuq'], ['LY', 'Nālūt'], ['LY', 'An Nuqaţ al Khams'], ['LY', 'Sabhā'], ['LY', 'Surt'],
     ['LY', 'Ţarābulus'], ['LY', 'Al Wāḩāt'], ['LY', 'Wādī al Ḩayāt'], ['LY', 'Banghāzī'],
     ['LY', 'Wādī ash Shāţiʾ'], ['LY', 'Al Buţnān'], ['LY', 'Az Zāwiyah'], ['LY', 'Darnah'], ['LY', 'Ghāt'],
     ['LY', 'Al Jabal al Akhḑar'], ['LY', 'Jaghbūb'], ['LY', 'Al Jabal al Gharbī'], ['LY', 'Al Jifārah']],

    [['LI', 'Triesen'], ['LI', 'Mauren'], ['LI', 'Triesenberg'], ['LI', 'Planken'], ['LI', 'Vaduz'],
     ['LI', 'Ruggell'], ['LI', 'Balzers'], ['LI', 'Schaan'], ['LI', 'Eschen'], ['LI', 'Schellenberg'],
     ['LI', 'Gamprin']],

    [['LK', 'Mŏṇarāgala'], ['LK', 'Mātara'], ['LK', 'Sabaragamuva paḷāta'], ['LK', 'Ratnapura'],
     ['LK', 'Hambantŏṭa'], ['LK', 'Uturu paḷāta'], ['LK', 'Yāpanaya'], ['LK', 'Kægalla'], ['LK', 'Kilinŏchchi'],
     ['LK', 'Mannārama'], ['LK', 'Vavuniyāva'], ['LK', 'Mulativ'], ['LK', 'Næ̆gĕnahira paḷāta'],
     ['LK', 'Maḍakalapuva'], ['LK', 'Ampāara'], ['LK', 'Trikuṇāmalaya'], ['LK', 'Vayamba paḷāta'],
     ['LK', 'Basnāhira paḷāta'], ['LK', 'Kuruṇægala'], ['LK', 'Kŏḷamba'], ['LK', 'Gampaha'], ['LK', 'Puttalama'],
     ['LK', 'Kaḷutara'], ['LK', 'Madhyama paḷāta'], ['LK', 'Uturumæ̆da paḷāta'], ['LK', 'Mahanuvara'],
     ['LK', 'Anurādhapura'], ['LK', 'Pŏḷŏnnaruva'], ['LK', 'Mātale'], ['LK', 'Ūva paḷāta'], ['LK', 'Nuvara Ĕliya'],
     ['LK', 'Badulla'], ['LK', 'Dakuṇu paḷāta'], ['LK', 'Gālla']],

    [['LS', 'Mokhotlong'], ['LS', 'Berea'], ['LS', 'Thaba-Tseka'], ['LS', 'Mafeteng'], ['LS', "Mohale's Hoek"],
     ['LS', 'Maseru'], ['LS', 'Quthing'], ['LS', 'Butha-Buthe'], ['LS', "Qacha's Nek"], ['LS', 'Leribe']],

    [['LT', 'Vilniaus Apskritis'], ['LT', 'Panevėžio Apskritis'], ['LT', 'Šiaulių Apskritis'],
     ['LT', 'Alytaus Apskritis'], ['LT', 'Tauragés Apskritis'], ['LT', 'Klaipėdos Apskritis'],
     ['LT', 'Telšių Apskritis'], ['LT', 'Kauno Apskritis'], ['LT', 'Utenos Apskritis'],
     ['LT', 'Marijampolės Apskritis']],

    [['LU', 'Diekirch'], ['LU', 'Luxembourg'], ['LU', 'Grevenmacher']],

    [['LV', 'Aizkraukles novads'], ['LV', 'Kārsavas novads'], ['LV', 'Aizputes novads'], ['LV', 'Kocēnu novads'],
     ['LV', 'Aknīstes novads'], ['LV', 'Kokneses novads'], ['LV', 'Alojas novads'], ['LV', 'Krāslavas novads'],
     ['LV', 'Alsungas novads'], ['LV', 'Krimuldas novads'], ['LV', 'Alūksnes novads'], ['LV', 'Krustpils novads'],
     ['LV', 'Amatas novads'], ['LV', 'Kuldīgas novads'], ['LV', 'Apes novads'], ['LV', 'Ķeguma novads'],
     ['LV', 'Auces novads'], ['LV', 'Ķekavas novads'], ['LV', 'Ādažu novads'], ['LV', 'Lielvārdes novads'],
     ['LV', 'Babītes novads'], ['LV', 'Limbažu novads'], ['LV', 'Baldones novads'], ['LV', 'Līgatnes novads'],
     ['LV', 'Baltinavas novads'], ['LV', 'Līvānu novads'], ['LV', 'Balvu novads'], ['LV', 'Lubānas novads'],
     ['LV', 'Bauskas novads'], ['LV', 'Ludzas novads'], ['LV', 'Beverīnas novads'], ['LV', 'Madonas novads'],
     ['LV', 'Brocēnu novads'], ['LV', 'Mazsalacas novads'], ['LV', 'Burtnieku novads'], ['LV', 'Mālpils novads'],
     ['LV', 'Carnikavas novads'], ['LV', 'Mārupes novads'], ['LV', 'Cesvaines novads'], ['LV', 'Mērsraga novads'],
     ['LV', 'Naukšēnu novads'], ['LV', 'Cēsu novads'], ['LV', 'Ciblas novads'], ['LV', 'Neretas novads'],
     ['LV', 'Dagdas novads'], ['LV', 'Nīcas novads'], ['LV', 'Daugavpils novads'], ['LV', 'Ogres novads'],
     ['LV', 'Dobeles novads'], ['LV', 'Olaines novads'], ['LV', 'Dundagas novads'], ['LV', 'Ozolnieku novads'],
     ['LV', 'Durbes novads'], ['LV', 'Pārgaujas novads'], ['LV', 'Engures novads'], ['LV', 'Pāvilostas novads'],
     ['LV', 'Ērgļu novads'], ['LV', 'Pļaviņu novads'], ['LV', 'Garkalnes novads'], ['LV', 'Preiļu novads'],
     ['LV', 'Grobiņas novads'], ['LV', 'Priekules novads'], ['LV', 'Gulbenes novads'], ['LV', 'Priekuļu novads'],
     ['LV', 'Iecavas novads'], ['LV', 'Raunas novads'], ['LV', 'Ikšķiles novads'], ['LV', 'Rēzeknes novads'],
     ['LV', 'Ilūkstes novads'], ['LV', 'Riebiņu novads'], ['LV', 'Inčukalna novads'], ['LV', 'Rojas novads'],
     ['LV', 'Jaunjelgavas novads'], ['LV', 'Ropažu novads'], ['LV', 'Jaunpiebalgas novads'],
     ['LV', 'Rucavas novads'], ['LV', 'Jaunpils novads'], ['LV', 'Rugāju novads'], ['LV', 'Jelgavas novads'],
     ['LV', 'Rundāles novads'], ['LV', 'Jēkabpils novads'], ['LV', 'Rūjienas novads'], ['LV', 'Kandavas novads'],
     ['LV', 'Salas novads'], ['LV', 'Salacgrīvas novads'], ['LV', 'Salaspils novads'], ['LV', 'Saldus novads'],
     ['LV', 'Saulkrastu novads'], ['LV', 'Sējas novads'], ['LV', 'Siguldas novads'], ['LV', 'Skrīveru novads'],
     ['LV', 'Skrundas novads'], ['LV', 'Smiltenes novads'], ['LV', 'Stopiņu novads'], ['LV', 'Strenču novads'],
     ['LV', 'Talsu novads'], ['LV', 'Tērvetes novads'], ['LV', 'Tukuma novads'], ['LV', 'Vaiņodes novads'],
     ['LV', 'Valkas novads'], ['LV', 'Varakļānu novads'], ['LV', 'Vārkavas novads'], ['LV', 'Vecpiebalgas novads'],
     ['LV', 'Vecumnieku novads'], ['LV', 'Ventspils novads'], ['LV', 'Viesītes novads'], ['LV', 'Viļakas novads'],
     ['LV', 'Viļānu novads'], ['LV', 'Zilupes novads'], ['LV', 'Daugavpils'], ['LV', 'Jelgava'],
     ['LV', 'Jēkabpils'], ['LV', 'Jūrmala'], ['LV', 'Liepāja'], ['LV', 'Rēzekne'], ['LV', 'Rīga'],
     ['LV', 'Ventspils'], ['LV', 'Valmiera'], ['LV', 'Aglonas novads']],

    [['MA', 'Es-Semara (EH-partial)'], ['MA', 'Sidi Kacem'], ['MA', 'Fahs-Anjra'], ['MA', 'Sidi Slimane'],
     ['MA', 'Fès'], ['MA', 'Skhirate-Témara'], ['MA', 'Figuig'], ['MA', 'Tarfaya (EH-partial)'],
     ['MA', 'Fquih Ben Salah'], ['MA', 'Taourirt'], ['MA', 'Guelmim'], ['MA', 'Taounate'], ['MA', 'Guercif'],
     ['MA', 'Taroudant'], ['MA', 'El Hajeb'], ['MA', 'Tata'], ['MA', 'Al Haouz'], ['MA', 'Taza'],
     ['MA', 'Al Hoceïma'], ['MA', 'Tétouan'], ['MA', 'Ifrane'], ['MA', 'Tinghir'], ['MA', 'Inezgane-Ait Melloul'],
     ['MA', 'Tiznit'], ['MA', 'El Jadida'], ['MA', 'Tanger-Assilah'], ['MA', 'Jerada'],
     ['MA', 'Tan-Tan (EH-partial)'], ['MA', 'Kénitra'], ['MA', 'Youssoufia'], ['MA', 'Tanger-Tétouan-Al Hoceïma'],
     ['MA', 'El Kelâa des Sraghna'], ['MA', 'Zagora'], ['MA', "L'Oriental"], ['MA', 'Khemisset'],
     ['MA', 'Fès-Meknès'], ['MA', 'Khenifra'], ['MA', 'Rabat-Salé-Kénitra'], ['MA', 'Khouribga'],
     ['MA', 'Béni Mellal-Khénifra'], ['MA', 'Laâyoune (EH)'], ['MA', 'Casablanca-Settat'], ['MA', 'Larache'],
     ['MA', 'Marrakech-Safi'], ['MA', 'Marrakech'], ['MA', 'Drâa-Tafilalet'], ['MA', 'M’diq-Fnideq'],
     ['MA', 'Souss-Massa'], ['MA', 'Médiouna'], ['MA', 'Guelmim-Oued Noun (EH-partial)'], ['MA', 'Meknès'],
     ['MA', 'Laâyoune-Sakia El Hamra (EH-partial)'], ['MA', 'Midelt'], ['MA', 'Dakhla-Oued Ed-Dahab (EH)'],
     ['MA', 'Mohammadia'], ['MA', 'Agadir-Ida-Ou-Tanane'], ['MA', 'Moulay Yacoub'], ['MA', 'Aousserd (EH)'],
     ['MA', 'Assa-Zag (EH-partial)'], ['MA', 'Nador'], ['MA', 'Azilal'], ['MA', 'Béni Mellal'], ['MA', 'Nouaceur'],
     ['MA', 'Berkane'], ['MA', 'Ouarzazate'], ['MA', 'Benslimane'], ['MA', 'Oued Ed-Dahab (EH)'],
     ['MA', 'Boujdour (EH)'], ['MA', 'Oujda-Angad'], ['MA', 'Boulemane'], ['MA', 'Ouezzane'], ['MA', 'Berrechid'],
     ['MA', 'Rabat'], ['MA', 'Casablanca'], ['MA', 'Rehamna'], ['MA', 'Chefchaouen'], ['MA', 'Safi'],
     ['MA', 'Chichaoua'], ['MA', 'Salé'], ['MA', 'Chtouka-Ait Baha'], ['MA', 'Sefrou'], ['MA', 'Driouch'],
     ['MA', 'Settat'], ['MA', 'Sidi Bennour'], ['MA', 'Errachidia'], ['MA', 'Sidi Ifni'], ['MA', 'Essaouira']],

    [['MC', 'Moneghetti'], ['MC', 'La Gare'], ['MC', 'Spélugues'], ['MC', 'Monaco-Ville'], ['MC', 'La Colle'],
     ['MC', 'Jardin Exotique'], ['MC', 'Saint-Roman'], ['MC', 'Moulins'], ['MC', 'La Condamine'],
     ['MC', 'Larvotto'], ['MC', 'Vallon de la Rousse'], ['MC', 'Port-Hercule'], ['MC', 'Malbousquet'],
     ['MC', 'Sainte-Dévote'], ['MC', 'Fontvieille'], ['MC', 'Monte-Carlo'], ['MC', 'La Source']],

    [['MD', 'Șoldănești'], ['MD', 'Cimișlia'], ['MD', 'Sîngerei'], ['MD', 'Criuleni'],
     ['MD', 'Stînga Nistrului, unitatea teritorială din'], ['MD', 'Căușeni'], ['MD', 'Soroca'], ['MD', 'Cantemir'],
     ['MD', 'Strășeni'], ['MD', 'Chișinău'], ['MD', 'Ștefan Vodă'], ['MD', 'Dondușeni'], ['MD', 'Taraclia'],
     ['MD', 'Drochia'], ['MD', 'Telenești'], ['MD', 'Dubăsari'], ['MD', 'Ungheni'], ['MD', 'Edineț'],
     ['MD', 'Fălești'], ['MD', 'Florești'], ['MD', 'Găgăuzia, Unitatea teritorială autonomă'], ['MD', 'Glodeni'],
     ['MD', 'Hîncești'], ['MD', 'Anenii Noi'], ['MD', 'Ialoveni'], ['MD', 'Bălți'], ['MD', 'Leova'],
     ['MD', 'Tighina'], ['MD', 'Nisporeni'], ['MD', 'Briceni'], ['MD', 'Ocnița'], ['MD', 'Basarabeasca'],
     ['MD', 'Orhei'], ['MD', 'Cahul'], ['MD', 'Rezina'], ['MD', 'Călărași'], ['MD', 'Rîșcani']],

    [['MG', 'Antsiranana'], ['MG', 'Fianarantsoa'], ['MG', 'Mahajanga'], ['MG', 'Antananarivo'], ['MG', 'Toliara'],
     ['MG', 'Toamasina']],

    [['MV', 'Upper North'], ['MV', 'Thaa'], ['MV', 'Upper South'], ['MV', 'Meemu'], ['MV', 'Raa'], ['MV', 'Faafu'],
     ['MV', 'Dhaalu'], ['MV', 'Baa'], ['MV', 'Haa Dhaalu'], ['MV', 'Shaviyani'], ['MV', 'Noonu'], ['MV', 'Kaafu'],
     ['MV', 'Gaafu Alifu'], ['MV', 'Gaafu Dhaalu'], ['MV', 'Gnaviyani'], ['MV', 'Central'], ['MV', 'Male'],
     ['MV', 'Alifu Dhaalu'], ['MV', 'North Central'], ['MV', 'Seenu'], ['MV', 'Alifu Alifu'], ['MV', 'North'],
     ['MV', 'Lhaviyani'], ['MV', 'Vaavu'], ['MV', 'South Central'], ['MV', 'Laamu'], ['MV', 'South'],
     ['MV', 'Haa Alifu']],

    [['MX', 'Yucatán'], ['MX', 'Durango'], ['MX', 'Zacatecas'], ['MX', 'Guerrero'], ['MX', 'Guanajuato'],
     ['MX', 'Hidalgo'], ['MX', 'Jalisco'], ['MX', 'México'], ['MX', 'Michoacán de Ocampo'], ['MX', 'Morelos'],
     ['MX', 'Nayarit'], ['MX', 'Nuevo León'], ['MX', 'Oaxaca'], ['MX', 'Aguascalientes'], ['MX', 'Puebla'],
     ['MX', 'Baja California'], ['MX', 'Querétaro'], ['MX', 'Quintana Roo'], ['MX', 'Baja California Sur'],
     ['MX', 'Sinaloa'], ['MX', 'Campeche'], ['MX', 'San Luis Potosí'], ['MX', 'Chihuahua'], ['MX', 'Sonora'],
     ['MX', 'Chiapas'], ['MX', 'Tabasco'], ['MX', 'Ciudad de México'], ['MX', 'Tamaulipas'],
     ['MX', 'Coahuila de Zaragoza'], ['MX', 'Tlaxcala'], ['MX', 'Colima'],
     ['MX', 'Veracruz de Ignacio de la Llave']],

    [['MH', 'Kili'], ['MH', 'Kwajalein'], ['MH', 'Ralik chain'], ['MH', 'Lae'], ['MH', 'Lib'], ['MH', 'Likiep'],
     ['MH', 'Majuro'], ['MH', 'Maloelap'], ['MH', 'Mejit'], ['MH', 'Mili'], ['MH', 'Namdrik'], ['MH', 'Namu'],
     ['MH', 'Rongelap'], ['MH', 'Ratak chain'], ['MH', 'Ujae'], ['MH', 'Ailuk'], ['MH', 'Ailinglaplap'],
     ['MH', 'Utirik'], ['MH', 'Arno'], ['MH', 'Aur'], ['MH', 'Wotje'], ['MH', 'Ebon'], ['MH', 'Wotho'],
     ['MH', 'Enewetak'], ['MH', 'Jabat'], ['MH', 'Jaluit']],

    [['MK', 'Kriva Palanka'], ['MK', 'Berovo'], ['MK', 'Krivogaštani'], ['MK', 'Bitola'], ['MK', 'Kruševo'],
     ['MK', 'Bogdanci'], ['MK', 'Kumanovo'], ['MK', 'Bogovinje'], ['MK', 'Lipkovo'], ['MK', 'Bosilovo'],
     ['MK', 'Lozovo'], ['MK', 'Brvenica'], ['MK', 'Mavrovo-i-Rostuša'], ['MK', 'Butel'],
     ['MK', 'Makedonska Kamenica'], ['MK', 'Valandovo'], ['MK', 'Makedonski Brod'], ['MK', 'Vasilevo'],
     ['MK', 'Mogila'], ['MK', 'Vevčani'], ['MK', 'Negotino'], ['MK', 'Veles'], ['MK', 'Novaci'], ['MK', 'Vinica'],
     ['MK', 'Novo Selo'], ['MK', 'Vraneštica'], ['MK', 'Oslomej'], ['MK', 'Vrapčište'], ['MK', 'Ohrid'],
     ['MK', 'Gazi Baba'], ['MK', 'Petrovec'], ['MK', 'Gevgelija'], ['MK', 'Pehčevo'], ['MK', 'Gostivar'],
     ['MK', 'Plasnica'], ['MK', 'Gradsko'], ['MK', 'Prilep'], ['MK', 'Debar'], ['MK', 'Probištip'],
     ['MK', 'Radoviš'], ['MK', 'Debarca'], ['MK', 'Delčevo'], ['MK', 'Rankovce'], ['MK', 'Demir Kapija'],
     ['MK', 'Resen'], ['MK', 'Demir Hisar'], ['MK', 'Rosoman'], ['MK', 'Dojran'], ['MK', 'Saraj'],
     ['MK', 'Dolneni'], ['MK', 'Sveti Nikole'], ['MK', 'Drugovo'], ['MK', 'Sopište'], ['MK', 'Gjorče Petrov'],
     ['MK', 'Staro Nagoričane'], ['MK', 'Želino'], ['MK', 'Struga'], ['MK', 'Zajas'], ['MK', 'Strumica'],
     ['MK', 'Zelenikovo'], ['MK', 'Studeničani'], ['MK', 'Zrnovci'], ['MK', 'Tearce'], ['MK', 'Ilinden'],
     ['MK', 'Tetovo'], ['MK', 'Jegunovce'], ['MK', 'Centar'], ['MK', 'Kavadarci'], ['MK', 'Centar Župa'],
     ['MK', 'Karbinci'], ['MK', 'Čair'], ['MK', 'Karpoš'], ['MK', 'Čaška'], ['MK', 'Kisela Voda'],
     ['MK', 'Češinovo-Obleševo'], ['MK', 'Kičevo'], ['MK', 'Čučer Sandevo'], ['MK', 'Konče'], ['MK', 'Štip'],
     ['MK', 'Aerodrom'], ['MK', 'Kočani'], ['MK', 'Šuto Orizari'], ['MK', 'Aračinovo'], ['MK', 'Kratovo']],

    [['ML', 'Gao'], ['ML', 'Koulikoro'], ['ML', 'Kidal'], ['ML', 'Sikasso'], ['ML', 'Bamako'], ['ML', 'Ségou'],
     ['ML', 'Mopti'], ['ML', 'Kayes'], ['ML', 'Tombouctou']],

    [['MT', 'Dingli'], ['MT', 'San Ġwann'], ['MT', 'Marsaxlokk'], ['MT', 'Fgura'], ['MT', 'San Lawrenz'],
     ['MT', 'Mdina'], ['MT', 'Floriana'], ['MT', 'San Pawl il-Baħar'], ['MT', 'Mellieħa'], ['MT', 'Fontana'],
     ['MT', 'Sannat'], ['MT', 'Mġarr'], ['MT', 'Gudja'], ['MT', 'Santa Luċija'], ['MT', 'Mosta'], ['MT', 'Gżira'],
     ['MT', 'Santa Venera'], ['MT', 'Mqabba'], ['MT', 'Għajnsielem'], ['MT', 'Siġġiewi'], ['MT', 'Msida'],
     ['MT', 'San Ġiljan'], ['MT', 'Għarb'], ['MT', 'Sliema'], ['MT', 'Mtarfa'], ['MT', 'Għargħur'],
     ['MT', 'Swieqi'], ['MT', 'Munxar'], ['MT', 'Għasri'], ['MT', 'Ta’ Xbiex'], ['MT', 'Nadur'], ['MT', 'Għaxaq'],
     ['MT', 'Tarxien'], ['MT', 'Naxxar'], ['MT', 'Ħamrun'], ['MT', 'Valletta'], ['MT', 'Paola'], ['MT', 'Iklin'],
     ['MT', 'Xagħra'], ['MT', 'Pembroke'], ['MT', 'Isla'], ['MT', 'Xewkija'], ['MT', 'Pietà'], ['MT', 'Kalkara'],
     ['MT', 'Xgħajra'], ['MT', 'Qala'], ['MT', 'Kerċem'], ['MT', 'Żabbar'], ['MT', 'Attard'], ['MT', 'Qormi'],
     ['MT', 'Kirkop'], ['MT', 'Żebbuġ Għawdex'], ['MT', 'Balzan'], ['MT', 'Qrendi'], ['MT', 'Lija'],
     ['MT', 'Żebbuġ Malta'], ['MT', 'Birgu'], ['MT', 'Rabat Għawdex'], ['MT', 'Luqa'], ['MT', 'Żejtun'],
     ['MT', 'Birkirkara'], ['MT', 'Rabat Malta'], ['MT', 'Marsa'], ['MT', 'Żurrieq'], ['MT', 'Birżebbuġa'],
     ['MT', 'Safi'], ['MT', 'Marsaskala'], ['MT', 'Bormla']],

    [['MM', 'Magway'], ['MM', 'Shan'], ['MM', 'Kayah'], ['MM', 'Mandalay'], ['MM', 'Kayin'], ['MM', 'Tanintharyi'],
     ['MM', 'Chin'], ['MM', 'Yangon'], ['MM', 'Sagaing'], ['MM', 'Mon'], ['MM', 'Ayeyarwady'], ['MM', 'Bago'],
     ['MM', 'Rakhine'], ['MM', 'Kachin']],

    [['ME', 'Plav'], ['ME', 'Pljevlja'], ['ME', 'Plužine'], ['ME', 'Podgorica'], ['ME', 'Rožaje'], ['ME', 'Šavnik'],
     ['ME', 'Tivat'], ['ME', 'Ulcinj'], ['ME', 'Žabljak'], ['ME', 'Andrijevica'], ['ME', 'Bar'], ['ME', 'Berane'],
     ['ME', 'Bijelo Polje'], ['ME', 'Budva'], ['ME', 'Cetinje'], ['ME', 'Danilovgrad'], ['ME', 'Herceg-Novi'],
     ['ME', 'Kolašin'], ['ME', 'Kotor'], ['ME', 'Mojkovac'], ['ME', 'Nikšić']],

    [['MN', 'Arhangay'], ['MN', 'Orhon'], ['MN', 'Ulanbaatar'], ['MN', 'Darhan uul'], ['MN', 'Hentiy'],
     ['MN', 'Hövsgöl'], ['MN', 'Hovd'], ['MN', 'Uvs'], ['MN', 'Töv'], ['MN', 'Selenge'], ['MN', 'Sühbaatar'],
     ['MN', 'Ömnögovi'], ['MN', 'Övörhangay'], ['MN', 'Dzavhan'], ['MN', 'Dundgovi'], ['MN', 'Dornod'],
     ['MN', 'Dornogovi'], ['MN', 'Govi-Sumber'], ['MN', 'Govi-Altay'], ['MN', 'Bulgan'], ['MN', 'Bayanhongor'],
     ['MN', 'Bayan-Ölgiy']],

    [['MZ', 'Zambezia'], ['MZ', 'Inhambane'], ['MZ', 'Sofala'], ['MZ', 'Maputo'], ['MZ', 'Niassa'], ['MZ', 'Tete'],
     ['MZ', 'Maputo (city)'], ['MZ', 'Manica'], ['MZ', 'Numpula'], ['MZ', 'Gaza'], ['MZ', 'Cabo Delgado']],

    [['MR', 'Tagant'], ['MR', 'Gorgol'], ['MR', 'Guidimaka'], ['MR', 'Brakna'], ['MR', 'Tiris Zemmour'],
     ['MR', 'Trarza'], ['MR', 'Hodh ech Chargui'], ['MR', 'Inchiri'], ['MR', 'Adrar'], ['MR', 'Hodh el Charbi'],
     ['MR', 'Nouakchott'], ['MR', 'Dakhlet Nouadhibou'], ['MR', 'Assaba']],

    [['MU', 'Plaines Wilhems'], ['MU', 'Grand Port'], ['MU', 'Black River'], ['MU', 'Port Louis'],
     ['MU', 'Quatre Bornes'], ['MU', 'Moka'], ['MU', 'Beau Bassin-Rose Hill'], ['MU', 'Rodrigues Island'],
     ['MU', 'Pamplemousses'], ['MU', 'Cargados Carajos Shoals'], ['MU', 'Rivière du Rempart'], ['MU', 'Port Louis'],
     ['MU', 'Curepipe'], ['MU', 'Savanne'], ['MU', 'Agalega Islands'], ['MU', 'Flacq'], ['MU', 'Vacoas-Phoenix']],

    [['MW', 'Neno'], ['MW', 'Ntchisi'], ['MW', 'Nkhotakota'], ['MW', 'Balaka'], ['MW', 'Nsanje'],
     ['MW', 'Blantyre'], ['MW', 'Ntcheu'], ['MW', 'Central Region'], ['MW', 'Chikwawa'], ['MW', 'Phalombe'],
     ['MW', 'Rumphi'], ['MW', 'Chiradzulu'], ['MW', 'Southern Region'], ['MW', 'Chitipa'], ['MW', 'Dedza'],
     ['MW', 'Salima'], ['MW', 'Dowa'], ['MW', 'Karonga'], ['MW', 'Thyolo'], ['MW', 'Kasungu'], ['MW', 'Zomba'],
     ['MW', 'Lilongwe'], ['MW', 'Likoma'], ['MW', 'Mchinji'], ['MW', 'Mangochi'], ['MW', 'Machinga'],
     ['MW', 'Mulanje'], ['MW', 'Mwanza'], ['MW', 'Mzimba'], ['MW', 'Northern Region'], ['MW', 'Nkhata Bay']],

    [['MY', 'Melaka'], ['MY', 'Wilayah Persekutuan Labuan'], ['MY', 'Selangor'], ['MY', 'Negeri Sembilan'],
     ['MY', 'Wilayah Persekutuan Putrajaya'], ['MY', 'Terengganu'], ['MY', 'Pahang'], ['MY', 'Johor'],
     ['MY', 'Sabah'], ['MY', 'Pulau Pinang'], ['MY', 'Kedah'], ['MY', 'Sarawak'], ['MY', 'Perak'],
     ['MY', 'Kelantan'], ['MY', 'Wilayah Persekutuan Kuala Lumpur'], ['MY', 'Perlis']],

    [['NA', 'Hardap'], ['NA', 'Okavango'], ['NA', 'Karas'], ['NA', 'Oshana'], ['NA', 'Khomas'], ['NA', 'Omusati'],
     ['NA', 'Kunene'], ['NA', 'Caprivi'], ['NA', 'Oshikoto'], ['NA', 'Otjozondjupa'], ['NA', 'Erongo'],
     ['NA', 'Ohangwena'], ['NA', 'Omaheke']],

    [['NE', 'Tillabéri'], ['NE', 'Agadez'], ['NE', 'Zinder'], ['NE', 'Diffa'], ['NE', 'Niamey'], ['NE', 'Dosso'],
     ['NE', 'Maradi'], ['NE', 'Tahoua']],

    [['NG', 'Taraba'], ['NG', 'Enugu'], ['NG', 'Yobe'], ['NG', 'Federal Capital Territory'], ['NG', 'Zamfara'],
     ['NG', 'Gombe'], ['NG', 'Imo'], ['NG', 'Jigawa'], ['NG', 'Kaduna'], ['NG', 'Kebbi'], ['NG', 'Kano'],
     ['NG', 'Abia'], ['NG', 'Kogi'], ['NG', 'Adamawa'], ['NG', 'Katsina'], ['NG', 'Akwa Ibom'], ['NG', 'Kwara'],
     ['NG', 'Anambra'], ['NG', 'Lagos'], ['NG', 'Bauchi'], ['NG', 'Nassarawa'], ['NG', 'Benue'], ['NG', 'Niger'],
     ['NG', 'Borno'], ['NG', 'Ogun'], ['NG', 'Bayelsa'], ['NG', 'Ondo'], ['NG', 'Cross River'], ['NG', 'Osun'],
     ['NG', 'Delta'], ['NG', 'Oyo'], ['NG', 'Ebonyi'], ['NG', 'Plateau'], ['NG', 'Edo'], ['NG', 'Rivers'],
     ['NG', 'Ekiti'], ['NG', 'Sokoto']],

    [['NI', 'Boaco'], ['NI', 'Matagalpa'], ['NI', 'Jinotega'], ['NI', 'Carazo'], ['NI', 'Nueva Segovia'],
     ['NI', 'León'], ['NI', 'Chinandega'], ['NI', 'Rivas'], ['NI', 'Madriz'], ['NI', 'Chontales'],
     ['NI', 'Atlántico Norte'], ['NI', 'Río San Juan'], ['NI', 'Managua'], ['NI', 'Estelí'],
     ['NI', 'Atlántico Sur'], ['NI', 'Masaya'], ['NI', 'Granada']],

    [['NL', 'Noord-Brabant'], ['NL', 'Flevoland'], ['NL', 'Limburg'], ['NL', 'Bonaire'], ['NL', 'Zuid-Holland'],
     ['NL', 'Noord-Holland'], ['NL', 'Friesland'], ['NL', 'Saba'], ['NL', 'Overijssel'], ['NL', 'Gelderland'],
     ['NL', 'Sint Eustatius'], ['NL', 'Sint Maarten'], ['NL', 'Groningen'], ['NL', 'Curaçao'], ['NL', 'Utrecht'],
     ['NL', 'Aruba'], ['NL', 'Drenthe'], ['NL', 'Zeeland']],

    [['NO', 'Oppland'], ['NO', 'Buskerud'], ['NO', 'Vestfold'], ['NO', 'Telemark'], ['NO', 'Aust-Agder'],
     ['NO', 'Vest-Agder'], ['NO', 'Rogaland'], ['NO', 'Hordaland'], ['NO', 'Sogn og Fjordane'],
     ['NO', 'Møre og Romsdal'], ['NO', 'Nordland'], ['NO', 'Troms'], ['NO', 'Finnmark'],
     ['NO', 'Svalbard (Arctic Region)'], ['NO', 'Jan Mayen (Arctic Region)'], ['NO', 'Trøndelag'],
     ['NO', 'Østfold'], ['NO', 'Akershus'], ['NO', 'Oslo'], ['NO', 'Hedmark']],

    [['NP', 'Bagmati'], ['NP', 'Bheri'], ['NP', 'Dhawalagiri'], ['NP', 'Gandaki'], ['NP', 'Janakpur'],
     ['NP', 'Karnali'], ['NP', 'Kosi'], ['NP', 'Lumbini'], ['NP', 'Mahakali'], ['NP', 'Mechi'], ['NP', 'Narayani'],
     ['NP', 'Rapti'], ['NP', 'Sagarmatha'], ['NP', 'Seti'], ['NP', 'Madhyamanchal'],
     ['NP', 'Madhya Pashchimanchal'], ['NP', 'Pashchimanchal'], ['NP', 'Purwanchal'],
     ['NP', 'Sudur Pashchimanchal']],

    [['NR', 'Uaboe'], ['NR', 'Anetan'], ['NR', 'Denigomodu'], ['NR', 'Yaren'], ['NR', 'Ewa'], ['NR', 'Anibare'],
     ['NR', 'Ijuw'], ['NR', 'Aiwo'], ['NR', 'Baiti'], ['NR', 'Meneng'], ['NR', 'Anabar'], ['NR', 'Boe'],
     ['NR', 'Nibok'], ['NR', 'Buada']],

    [['NZ', 'Taranaki'], ['NZ', 'Wellington'], ['NZ', 'Waikato'], ['NZ', 'West Coast'], ['NZ', 'Auckland'],
     ['NZ', 'Bay of Plenty'], ['NZ', 'Canterbury'], ['NZ', 'Chatham Islands Territory'],
     ['NZ', 'Gisborne District'], ['NZ', "Hawke's Bay"], ['NZ', 'Marlborough District'],
     ['NZ', 'Manawatu-Wanganui'], ['NZ', 'North Island'], ['NZ', 'Nelson City'], ['NZ', 'Northland'],
     ['NZ', 'Otago'], ['NZ', 'South Island'], ['NZ', 'Southland'], ['NZ', 'Tasman District']],

    [['OM', 'Ash Sharqīyah'], ['OM', 'Al Wusţá'], ['OM', 'Ad Dākhilīya'], ['OM', 'Az̧ Z̧āhirah'], ['OM', 'Z̧ufār'],
     ['OM', 'Masqaţ'], ['OM', 'Al Bāţinah'], ['OM', 'Musandam'], ['OM', 'Al Buraymī']],

    [['PK', 'Khyber Pakhtunkhwa'], ['PK', 'Gilgit-Baltistan'], ['PK', 'Punjab'], ['PK', 'Sindh'],
     ['PK', 'Islamabad'], ['PK', 'Federally Administered Tribal Areas'], ['PK', 'Azad Kashmir'],
     ['PK', 'Balochistan']],

    [['PA', 'Panamá'], ['PA', 'Colón'], ['PA', 'Veraguas'], ['PA', 'Chiriquí'], ['PA', 'Emberá'], ['PA', 'Darién'],
     ['PA', 'Kuna Yala'], ['PA', 'Herrera'], ['PA', 'Bocas del Toro'], ['PA', 'Ngöbe-Buglé'], ['PA', 'Los Santos'],
     ['PA', 'Coclé']],

    [['PE', 'Loreto'], ['PE', 'Madre de Dios'], ['PE', 'Moquegua'], ['PE', 'Pasco'], ['PE', 'Piura'],
     ['PE', 'Amazonas'], ['PE', 'Puno'], ['PE', 'Ancash'], ['PE', 'San Martín'], ['PE', 'Apurímac'],
     ['PE', 'Tacna'], ['PE', 'Arequipa'], ['PE', 'Tumbes'], ['PE', 'Ayacucho'], ['PE', 'Ucayali'],
     ['PE', 'Cajamarca'], ['PE', 'El Callao'], ['PE', 'Cusco [Cuzco]'], ['PE', 'Huánuco'], ['PE', 'Huancavelica'],
     ['PE', 'Ica'], ['PE', 'Junín'], ['PE', 'La Libertad'], ['PE', 'Lambayeque'], ['PE', 'Lima'],
     ['PE', 'Municipalidad Metropolitana de Lima']],

    [['PE', 'Loreto'], ['PE', 'Madre de Dios'], ['PE', 'Moquegua'], ['PE', 'Pasco'], ['PE', 'Piura'],
     ['PE', 'Amazonas'], ['PE', 'Puno'], ['PE', 'Ancash'], ['PE', 'San Martín'], ['PE', 'Apurímac'],
     ['PE', 'Tacna'], ['PE', 'Arequipa'], ['PE', 'Tumbes'], ['PE', 'Ayacucho'], ['PE', 'Ucayali'],
     ['PE', 'Cajamarca'], ['PE', 'El Callao'], ['PE', 'Cusco [Cuzco]'], ['PE', 'Huánuco'], ['PE', 'Huancavelica'],
     ['PE', 'Ica'], ['PE', 'Junín'], ['PE', 'La Libertad'], ['PE', 'Lambayeque'], ['PE', 'Lima'],
     ['PE', 'Municipalidad Metropolitana de Lima']],

    [['PH', 'Lanao del Norte'], ['PH', 'Lanao del Sur'], ['PH', 'Leyte'], ['PH', 'La Union'], ['PH', 'Marinduque'],
     ['PH', 'Maguindanao'], ['PH', 'Masbate'], ['PH', 'Mindoro Occidental'], ['PH', 'Mindoro Oriental'],
     ['PH', 'Mountain Province'], ['PH', 'Misamis Occidental'], ['PH', 'Misamis Oriental'],
     ['PH', 'North Cotabato'], ['PH', 'Negros Occidental'], ['PH', 'Negros Oriental'], ['PH', 'Northern Samar'],
     ['PH', 'Nueva Ecija'], ['PH', 'Nueva Vizcaya'], ['PH', 'Pampanga'], ['PH', 'Pangasinan'], ['PH', 'Palawan'],
     ['PH', 'Quezon'], ['PH', 'Quirino'], ['PH', 'Rizal'], ['PH', 'Romblon'], ['PH', 'Sarangani'],
     ['PH', 'South Cotabato'], ['PH', 'Siquijor'], ['PH', 'Southern Leyte'], ['PH', 'Sulu'], ['PH', 'Sorsogon'],
     ['PH', 'Sultan Kudarat'], ['PH', 'Surigao del Norte'], ['PH', 'Surigao del Sur'], ['PH', 'Tarlac'],
     ['PH', 'Tawi-Tawi'], ['PH', 'Western Samar'], ['PH', 'Zamboanga del Norte'], ['PH', 'Zamboanga del Sur'],
     ['PH', 'Zambales'], ['PH', 'Zamboanga Sibugay'], ['PH', 'Caraga (Region XIII)'],
     ['PH', 'Autonomous Region in Muslim Mindanao (ARMM)'], ['PH', 'Cordillera Administrative Region (CAR)'],
     ['PH', 'CALABARZON (Region IV-A)'], ['PH', 'MIMAROPA (Region IV-B)'], ['PH', 'Abra'],
     ['PH', 'Agusan del Norte'], ['PH', 'Agusan del Sur'], ['PH', 'Aklan'], ['PH', 'Albay'], ['PH', 'Antique'],
     ['PH', 'Apayao'], ['PH', 'Aurora'], ['PH', 'Batasn'], ['PH', 'Basilan'], ['PH', 'Benguet'], ['PH', 'Biliran'],
     ['PH', 'Bohol'], ['PH', 'Batangas'], ['PH', 'Batanes'], ['PH', 'Bukidnon'], ['PH', 'Bulacan'],
     ['PH', 'Cagayan'], ['PH', 'Camiguin'], ['PH', 'Camarines Norte'], ['PH', 'Capiz'], ['PH', 'Camarines Sur'],
     ['PH', 'Catanduanes'], ['PH', 'Cavite'], ['PH', 'Cebu'], ['PH', 'Compostela Valley'], ['PH', 'Davao Oriental'],
     ['PH', 'National Capital Region'], ['PH', 'Davao del Sur'], ['PH', 'Ilocos (Region I)'],
     ['PH', 'Davao del Norte'], ['PH', 'Cagayan Valley (Region II)'], ['PH', 'Dinagat Islands'],
     ['PH', 'Central Luzon (Region III)'], ['PH', 'Eastern Samar'], ['PH', 'Bicol (Region V)'], ['PH', 'Guimaras'],
     ['PH', 'Western Visayas (Region VI)'], ['PH', 'Ifugao'], ['PH', 'Central Visayas (Region VII)'],
     ['PH', 'Iloilo'], ['PH', 'Eastern Visayas (Region VIII)'], ['PH', 'Ilocos Norte'],
     ['PH', 'Zamboanga Peninsula (Region IX)'], ['PH', 'Ilocos Sur'], ['PH', 'Northern Mindanao (Region X)'],
     ['PH', 'Isabela'], ['PH', 'Davao (Region XI)'], ['PH', 'Kalinga-Apayso'], ['PH', 'Soccsksargen (Region XII)'],
     ['PH', 'Laguna']],

    [['PW', 'Ngaraard'], ['PW', 'Angaur'], ['PW', 'Ngiwal'], ['PW', 'Ngarchelong'], ['PW', 'Hatobohei'],
     ['PW', 'Peleliu'], ['PW', 'Ngardmau'], ['PW', 'Kayangel'], ['PW', 'Sonsorol'], ['PW', 'Ngatpang'],
     ['PW', 'Koror'], ['PW', 'Aimeliik'], ['PW', 'Ngchesar'], ['PW', 'Melekeok'], ['PW', 'Airai'],
     ['PW', 'Ngeremlengui']],

    [['PG', 'National Capital District (Port Moresby)'], ['PG', 'New Ireland'], ['PG', 'Northern'],
     ['PG', 'Bougainville'], ['PG', 'Sandaun'], ['PG', 'Southern Highlands'], ['PG', 'West New Britain'],
     ['PG', 'Western Highlands'], ['PG', 'Western'], ['PG', 'Chimbu'], ['PG', 'Central'],
     ['PG', 'East New Britain'], ['PG', 'Eastern Highlands'], ['PG', 'Enga'], ['PG', 'East Sepik'], ['PG', 'Gulf'],
     ['PG', 'Milne Bay'], ['PG', 'Morobe'], ['PG', 'Madang'], ['PG', 'Manus']],

    [['PL', 'Kujawsko-pomorskie'], ['PL', 'Śląskie'], ['PL', 'Opolskie'], ['PL', 'Lubuskie'],
     ['PL', 'Warmińsko-mazurskie'], ['PL', 'Podlaskie'], ['PL', 'Łódzkie'], ['PL', 'Wielkopolskie'],
     ['PL', 'Podkarpackie'], ['PL', 'Lubelskie'], ['PL', 'Zachodniopomorskie'], ['PL', 'Pomorskie'],
     ['PL', 'Małopolskie'], ['PL', 'Dolnośląskie'], ['PL', 'Świętokrzyskie'], ['PL', 'Mazowieckie']],

    [['KP', 'Nasŏn (Najin-Sŏnbong)'], ['KP', 'P’yŏngyang'], ['KP', 'Hwanghae-bukto'], ['KP', 'Kangwŏn-do'],
     ['KP', 'P’yŏngan-namdo'], ['KP', 'Hamgyŏng-namdo'], ['KP', 'P’yŏngan-bukto'], ['KP', 'Hamgyŏng-bukto'],
     ['KP', 'Chagang-do'], ['KP', 'Yanggang-do'], ['KP', 'Hwanghae-namdo']],

    [['PT', 'Beja'], ['PT', 'Braga'], ['PT', 'Bragança'], ['PT', 'Castelo Branco'], ['PT', 'Coimbra'],
     ['PT', 'Évora'], ['PT', 'Faro'], ['PT', 'Guarda'], ['PT', 'Leiria'], ['PT', 'Lisboa'], ['PT', 'Portalegre'],
     ['PT', 'Porto'], ['PT', 'Santarém'], ['PT', 'Setúbal'], ['PT', 'Viana do Castelo'], ['PT', 'Vila Real'],
     ['PT', 'Viseu'], ['PT', 'Região Autónoma dos Açores'], ['PT', 'Região Autónoma da Madeira'], ['PT', 'Aveiro']],

    [['PY', 'Asunción'], ['PY', 'Central'], ['PY', 'Caaguazú'], ['PY', 'Alto Paraguay'], ['PY', 'Ñeembucú'],
     ['PY', 'Caazapá'], ['PY', 'Boquerón'], ['PY', 'Amambay'], ['PY', 'Itapúa'], ['PY', 'San Pedro'],
     ['PY', 'Canindeyú'], ['PY', 'Misiones'], ['PY', 'Concepción'], ['PY', 'Cordillera'], ['PY', 'Paraguarí'],
     ['PY', 'Presidente Hayes'], ['PY', 'Alto Paraná'], ['PY', 'Guairá']],

    [['PS', 'Deir El Balah'], ['PS', 'Rafah'], ['PS', 'Khan Yunis'], ['PS', 'Gaza'], ['PS', 'Salfit'],
     ['PS', 'Nablus'], ['PS', 'Hebron'], ['PS', 'Tubas'], ['PS', 'North Gaza'], ['PS', 'Jerusalem'],
     ['PS', 'Tulkarm'], ['PS', 'Qalqilya'], ['PS', 'Jenin'], ['PS', 'Bethlehem'], ['PS', 'Ramallah'],
     ['PS', 'Jericho - Al Aghwar']],

    [['QA', 'Al Wakrah'], ['QA', 'Ad Dawhah'], ['QA', 'Az̧ Z̧a‘āyin'], ['QA', 'Al Khawr wa adh Dhakhīrah'],
     ['QA', 'Ash Shamal'], ['QA', 'Ar Rayyan'], ['QA', 'Umm Salal']],

    [['RO', 'București'], ['RO', 'Ialomița'], ['RO', 'Bacău'], ['RO', 'Iași'], ['RO', 'Bihor'], ['RO', 'Mehedinți'],
     ['RO', 'Bistrița-Năsăud'], ['RO', 'Maramureș'], ['RO', 'Brăila'], ['RO', 'Mureș'], ['RO', 'Botoșani'],
     ['RO', 'Neamț'], ['RO', 'Brașov'], ['RO', 'Olt'], ['RO', 'Buzău'], ['RO', 'Prahova'], ['RO', 'Cluj'],
     ['RO', 'Sibiu'], ['RO', 'Călărași'], ['RO', 'Sălaj'], ['RO', 'Caraș-Severin'], ['RO', 'Satu Mare'],
     ['RO', 'Constanța'], ['RO', 'Suceava'], ['RO', 'Covasna'], ['RO', 'Tulcea'], ['RO', 'Dâmbovița'],
     ['RO', 'Timiș'], ['RO', 'Dolj'], ['RO', 'Teleorman'], ['RO', 'Gorj'], ['RO', 'Vâlcea'], ['RO', 'Galați'],
     ['RO', 'Vrancea'], ['RO', 'Giurgiu'], ['RO', 'Vaslui'], ['RO', 'Hunedoara'], ['RO', 'Alba'],
     ['RO', 'Harghita'], ['RO', 'Argeș'], ['RO', 'Ilfov'], ['RO', 'Arad']],

    [['RU', "Kurskaya oblast'"], ['RU', "Vladimirskaya oblast'"], ['RU', 'Krasnoyarskiy kray'],
     ['RU', "Vologodskaya oblast'"], ['RU', "Leningradskaya oblast'"], ['RU', "Voronezhskaya oblast'"],
     ['RU', "Lipetskaya oblast'"], ['RU', 'Yamalo-Nenetskiy avtonomnyy okrug'], ['RU', "Magadanskaya oblast'"],
     ['RU', "Yaroslavskaya oblast'"], ['RU', 'Mariy El, Respublika'], ['RU', "Yevreyskaya avtonomnaya oblast'"],
     ['RU', 'Mordoviya, Respublika'], ['RU', "Zabajkal'skij kraj"], ['RU', "Moskovskaya oblast'"], ['RU', 'Moskva'],
     ['RU', "Murmanskaya oblast'"], ['RU', 'Nenetskiy avtonomnyy okrug'], ['RU', "Novgorodskaya oblast'"],
     ['RU', "Nizhegorodskaya oblast'"], ['RU', "Novosibirskaya oblast'"], ['RU', "Omskaya oblast'"],
     ['RU', "Orenburgskaya oblast'"], ['RU', "Orlovskaya oblast'"], ['RU', 'Permskiy kray'],
     ['RU', "Penzenskaya oblast'"], ['RU', 'Primorskiy kray'], ['RU', "Pskovskaya oblast'"],
     ['RU', "Rostovskaya oblast'"], ['RU', "Ryazanskaya oblast'"], ['RU', 'Sakha, Respublika [Yakutiya]'],
     ['RU', "Sakhalinskaya oblast'"], ['RU', "Samaraskaya oblast'"], ['RU', "Saratovskaya oblast'"],
     ['RU', 'Severnaya Osetiya-Alaniya, Respublika'], ['RU', "Smolenskaya oblast'"], ['RU', 'Sankt-Peterburg'],
     ['RU', "Stavropol'skiy kray"], ['RU', "Sverdlovskaya oblast'"], ['RU', 'Tatarstan, Respublika'],
     ['RU', "Tambovskaya oblast'"], ['RU', "Tomskaya oblast'"], ['RU', "Tul'skaya oblast'"],
     ['RU', "Tverskaya oblast'"], ['RU', 'Tyva, Respublika [Tuva]'], ['RU', "Tyumenskaya oblast'"],
     ['RU', 'Udmurtskaya Respublika'], ['RU', "Ul'yanovskaya oblast'"], ['RU', "Volgogradskaya oblast'"],
     ['RU', 'Adygeya, Respublika'], ['RU', 'Altay, Respublika'], ['RU', 'Altayskiy kray'],
     ['RU', "Amurskaya oblast'"], ['RU', "Arkhangel'skaya oblast'"], ['RU', "Astrakhanskaya oblast'"],
     ['RU', 'Bashkortostan, Respublika'], ['RU', "Belgorodskaya oblast'"], ['RU', "Bryanskaya oblast'"],
     ['RU', 'Buryatiya, Respublika'], ['RU', 'Chechenskaya Respublika'], ['RU', "Chelyabinskaya oblast'"],
     ['RU', 'Chukotskiy avtonomnyy okrug'], ['RU', 'Chuvashskaya Respublika'], ['RU', 'Dagestan, Respublika'],
     ['RU', 'Respublika Ingushetiya'], ['RU', "Irkutiskaya oblast'"], ['RU', "Ivanovskaya oblast'"],
     ['RU', 'Kamchatskiy kray'], ['RU', 'Kabardino-Balkarskaya Respublika'],
     ['RU', 'Karachayevo-Cherkesskaya Respublika'], ['RU', 'Krasnodarskiy kray'], ['RU', "Kemerovskaya oblast'"],
     ['RU', "Kaliningradskaya oblast'"], ['RU', "Kurganskaya oblast'"], ['RU', 'Khabarovskiy kray'],
     ['RU', 'Khanty-Mansiysky avtonomnyy okrug-Yugra'], ['RU', "Kirovskaya oblast'"],
     ['RU', 'Khakasiya, Respublika'], ['RU', 'Kalmykiya, Respublika'], ['RU', "Kaluzhskaya oblast'"],
     ['RU', 'Komi, Respublika'], ['RU', "Kostromskaya oblast'"], ['RU', 'Kareliya, Respublika']],

    [['RW', 'Ouest'], ['RW', 'Sud'], ['RW', 'Ville de Kigali'], ['RW', 'Est'], ['RW', 'Nord']],

    [['SA', 'Najrān'], ['SA', 'Al Qaşīm'], ['SA', 'Al Bāhah'], ['SA', "Ḥā'il"], ['SA', 'Ar Riyāḍ'],
     ['SA', 'Al Jawf'], ['SA', 'Tabūk'], ['SA', 'Makkah'], ['SA', '`Asīr'], ['SA', 'Al Ḥudūd ash Shamāliyah'],
     ['SA', 'Al Madīnah'], ['SA', 'Jīzan'], ['SA', 'Ash Sharqīyah']],

    [['SD', 'Al Kharţūm'], ['SD', 'Janūb Dārfūr'], ['SD', 'An Nīl al Abyaḑ'], ['SD', 'Shamāl Kurdufān'],
     ['SD', 'Gharb Dārfūr'], ['SD', 'Al Baḩr al Aḩmar'], ['SD', 'Janūb Kurdufān'], ['SD', 'Al Qaḑārif'],
     ['SD', 'Zalingei'], ['SD', 'Sinnār'], ['SD', 'An Nīl al Azraq'], ['SD', 'Al Jazīrah'], ['SD', 'Sharq Dārfūr'],
     ['SD', 'Ash Shamālīyah'], ['SD', 'Kassalā'], ['SD', 'Shamāl Dārfūr'], ['SD', 'An Nīl']],

    [['SN', 'Sédhiou'], ['SN', 'Kolda'], ['SN', 'Saint-Louis'], ['SN', 'Kédougou'], ['SN', 'Diourbel'],
     ['SN', 'Tambacounda'], ['SN', 'Kaolack'], ['SN', 'Dakar'], ['SN', 'Thiès'], ['SN', 'Louga'], ['SN', 'Fatick'],
     ['SN', 'Ziguinchor'], ['SN', 'Matam'], ['SN', 'Kaffrine']],

    [['SG', 'North West'], ['SG', 'South East'], ['SG', 'South West'], ['SG', 'Central Singapore'],
     ['SG', 'North East']],

    [['SH', 'Tristan da Cunha'], ['SH', 'Saint Helena'], ['SH', 'Ascension']],

    [['SB', 'Choiseul'], ['SB', 'Rennell and Bellona'], ['SB', 'Capital Territory (Honiara)'], ['SB', 'Temotu'],
     ['SB', 'Guadalcanal'], ['SB', 'Western'], ['SB', 'Isabel'], ['SB', 'Makira'], ['SB', 'Central'],
     ['SB', 'Malaita']],

    [['SL', 'Eastern'], ['SL', 'Western Area (Freetown)'], ['SL', 'Southern (Sierra Leone)'], ['SL', 'Northern']],

    [['SV', 'Usulután'], ['SV', 'San Miguel'], ['SV', 'Cuscatlán'], ['SV', 'Sonsonate'], ['SV', 'La Libertad'],
     ['SV', 'San Salvador'], ['SV', 'Morazán'], ['SV', 'Ahuachapán'], ['SV', 'San Vicente'], ['SV', 'La Paz'],
     ['SV', 'Cabañas'], ['SV', 'La Unión'], ['SV', 'Santa Ana'], ['SV', 'Chalatenango']],

    [['SM', 'Faetano'], ['SM', 'Serravalle'], ['SM', 'Fiorentino'], ['SM', 'Borgo Maggiore'], ['SM', 'Acquaviva'],
     ['SM', 'San Marino'], ['SM', 'Chiesanuova'], ['SM', 'Montegiardino'], ['SM', 'Domagnano']],

    [['SO', 'Nugaal'], ['SO', 'Gedo'], ['SO', 'Bakool'], ['SO', 'Woqooyi Galbeed'], ['SO', 'Saneag'],
     ['SO', 'Hiirsan'], ['SO', 'Banaadir'], ['SO', 'Shabeellaha Dhexe'], ['SO', 'Togdheer'],
     ['SO', 'Jubbada Dhexe'], ['SO', 'Bari'], ['SO', 'Shabeellaha Hoose'], ['SO', 'Jubbada Hoose'], ['SO', 'Bay'],
     ['SO', 'Sool'], ['SO', 'Mudug'], ['SO', 'Galguduud'], ['SO', 'Awdal']],

    [['RS', 'Južnobanatski okrug'], ['RS', 'Pčinjski okrug'], ['RS', 'Zapadnobački okrug'],
     ['RS', 'Kosovski okrug'], ['RS', 'Južnobački okrug'], ['RS', 'Pećki okrug'], ['RS', 'Sremski okrug'],
     ['RS', 'Prizrenski okrug'], ['RS', 'Kosovsko-Mitrovački okrug'], ['RS', 'Mačvanski okrug'],
     ['RS', 'Kosovsko-Pomoravski okrug'], ['RS', 'Kolubarski okrug'], ['RS', 'Kosovo-Metohija'],
     ['RS', 'Vojvodina'], ['RS', 'Podunavski okrug'], ['RS', 'Braničevski okrug'], ['RS', 'Šumadijski okrug'],
     ['RS', 'Pomoravski okrug'], ['RS', 'Borski okrug'], ['RS', 'Zaječarski okrug'], ['RS', 'Zlatiborski okrug'],
     ['RS', 'Moravički okrug'], ['RS', 'Raški okrug'], ['RS', 'Rasinski okrug'], ['RS', 'Nišavski okrug'],
     ['RS', 'Toplički okrug'], ['RS', 'Beograd'], ['RS', 'Pirotski okrug'], ['RS', 'Severnobački okrug'],
     ['RS', 'Jablanički okrug'], ['RS', 'Srednjebanatski okrug'], ['RS', 'Severnobanatski okrug']],

    [['SS', 'Warrap'], ['SS', 'Western Equatoria'], ['SS', 'Jonglei'], ['SS', 'Northern Bahr el Ghazal'],
     ['SS', 'Lakes'], ['SS', 'Western Bahr el Ghazal'], ['SS', 'Upper Nile'], ['SS', 'Central Equatoria'],
     ['SS', 'Unity'], ['SS', 'Eastern Equatoria']],

    [['ST', 'São Tomé'], ['ST', 'Príncipe']],

    [['SR', 'Nickerie'], ['SR', 'Wanica'], ['SR', 'Paramaribo'], ['SR', 'Brokopondo'], ['SR', 'Para'],
     ['SR', 'Commewijne'], ['SR', 'Saramacca'], ['SR', 'Coronie'], ['SR', 'Sipaliwini'], ['SR', 'Marowijne']],

    [['SK', 'Prešovský kraj'], ['SK', 'Trnavský kraj'], ['SK', 'Banskobystrický kraj'], ['SK', 'Trenčiansky kraj'],
     ['SK', 'Bratislavský kraj'], ['SK', 'Žilinský kraj'], ['SK', 'Košický kraj'], ['SK', 'Nitriansky kraj']],

    [['SI', 'Dobrova-Polhov Gradec'], ['SI', 'Rogašovci'], ['SI', 'Benedikt'], ['SI', 'Žalec'],
     ['SI', 'Dol pri Ljubljani'], ['SI', 'Rogaška Slatina'], ['SI', 'Bistrica ob Sotli'], ['SI', 'Žetale'],
     ['SI', 'Domžale'], ['SI', 'Rogatec'], ['SI', 'Bloke'], ['SI', 'Žirovnica'], ['SI', 'Dornava'], ['SI', 'Ruše'],
     ['SI', 'Braslovče'], ['SI', 'Žužemberk'], ['SI', 'Dravograd'], ['SI', 'Semič'], ['SI', 'Cankova'],
     ['SI', 'Šmartno pri Litiji'], ['SI', 'Duplek'], ['SI', 'Sevnica'], ['SI', 'Cerkvenjak'], ['SI', 'Apače'],
     ['SI', 'Gorenja vas-Poljane'], ['SI', 'Sežana'], ['SI', 'Dobje'], ['SI', 'Cirkulane'], ['SI', 'Gorišnica'],
     ['SI', 'Slovenj Gradec'], ['SI', 'Dobrna'], ['SI', 'Kosanjevica na Krki'], ['SI', 'Gornja Radgona'],
     ['SI', 'Slovenska Bistrica'], ['SI', 'Dobrovnik/Dobronak'], ['SI', 'Makole'], ['SI', 'Gornji Grad'],
     ['SI', 'Slovenske Konjice'], ['SI', 'Dolenjske Toplice'], ['SI', 'Mokronog-Trebelno'],
     ['SI', 'Gornji Petrovci'], ['SI', 'Starče'], ['SI', 'Grad'], ['SI', 'Poljčane'], ['SI', 'Grosuplje'],
     ['SI', 'Sveti Jurij'], ['SI', 'Hajdina'], ['SI', 'Renče-Vogrsko'], ['SI', 'Šalovci'], ['SI', 'Šenčur'],
     ['SI', 'Hoče-Slivnica'], ['SI', 'Središče ob Dravi'], ['SI', 'Hrastnik'], ['SI', 'Šentilj'],
     ['SI', 'Hodoš/Hodos'], ['SI', 'Straža'], ['SI', 'Hrpelje-Kozina'], ['SI', 'Šentjernej'], ['SI', 'Horjul'],
     ['SI', 'Sveta Trojica v Slovenskih Goricah'], ['SI', 'Idrija'], ['SI', 'Šentjur'], ['SI', 'Jezersko'],
     ['SI', 'Sveti Tomaž'], ['SI', 'Ig'], ['SI', 'Škocjan'], ['SI', 'Komenda'], ['SI', 'Šmarjeske Topliče'],
     ['SI', 'Ilirska Bistrica'], ['SI', 'Škofja Loka'], ['SI', 'Kostel'], ['SI', 'Gorje'], ['SI', 'Ivančna Gorica'],
     ['SI', 'Škofljica'], ['SI', 'Križevci'], ['SI', 'Log-Dragomer'], ['SI', 'Izola/Isola'],
     ['SI', 'Šmarje pri Jelšah'], ['SI', 'Lovrenc na Pohorju'], ['SI', 'Rečica ob Savinji'], ['SI', 'Jesenice'],
     ['SI', 'Šmartno ob Paki'], ['SI', 'Markovci'], ['SI', 'Sveti Jurij v Slovenskih Goricah'], ['SI', 'Juršinci'],
     ['SI', 'Šoštanj'], ['SI', 'Miklavž na Dravskem polju'], ['SI', 'Šentrupert'], ['SI', 'Ajdovščina'],
     ['SI', 'Kamnik'], ['SI', 'Štore'], ['SI', 'Mirna Peč'], ['SI', 'Beltinci'], ['SI', 'Kanal'], ['SI', 'Tolmin'],
     ['SI', 'Oplotnica'], ['SI', 'Bled'], ['SI', 'Kidričevo'], ['SI', 'Trbovlje'], ['SI', 'Podlehnik'],
     ['SI', 'Bohinj'], ['SI', 'Kobarid'], ['SI', 'Trebnje'], ['SI', 'Polzela'], ['SI', 'Borovnica'],
     ['SI', 'Kobilje'], ['SI', 'Tržič'], ['SI', 'Prebold'], ['SI', 'Bovec'], ['SI', 'Kočevje'], ['SI', 'Turnišče'],
     ['SI', 'Prevalje'], ['SI', 'Brda'], ['SI', 'Komen'], ['SI', 'Velenje'], ['SI', 'Razkrižje'],
     ['SI', 'Brezovica'], ['SI', 'Koper/Capodistria'], ['SI', 'Velike Lašče'], ['SI', 'Ribnica na Pohorju'],
     ['SI', 'Brežice'], ['SI', 'Kozje'], ['SI', 'Videm'], ['SI', 'Selnica ob Dravi'], ['SI', 'Tišina'],
     ['SI', 'Kranj'], ['SI', 'Vipava'], ['SI', 'Sodražica'], ['SI', 'Celje'], ['SI', 'Kranjska Gora'],
     ['SI', 'Vitanje'], ['SI', 'Solčava'], ['SI', 'Cerklje na Gorenjskem'], ['SI', 'Krško'], ['SI', 'Vodice'],
     ['SI', 'Sveta Ana'], ['SI', 'Cerknica'], ['SI', 'Kungota'], ['SI', 'Vojnik'],
     ['SI', 'Sveta Andraž v Slovenskih Goricah'], ['SI', 'Cerkno'], ['SI', 'Kuzma'], ['SI', 'Vrhnika'],
     ['SI', 'Šempeter-Vrtojba'], ['SI', 'Črenšovci'], ['SI', 'Laško'], ['SI', 'Vuzenica'], ['SI', 'Tabor'],
     ['SI', 'Črna na Koroškem'], ['SI', 'Lenart'], ['SI', 'Zagorje ob Savi'], ['SI', 'Trnovska vas'],
     ['SI', 'Črnomelj'], ['SI', 'Lendava/Lendva'], ['SI', 'Zavrč'], ['SI', 'Trzin'], ['SI', 'Destrnik'],
     ['SI', 'Litija'], ['SI', 'Zreče'], ['SI', 'Velika Polana'], ['SI', 'Divača'], ['SI', 'Ljubljana'],
     ['SI', 'Železniki'], ['SI', 'Veržej'], ['SI', 'Ljubno'], ['SI', 'Dobrepolje'], ['SI', 'Žiri'],
     ['SI', 'Vransko'], ['SI', 'Ljutomer'], ['SI', 'Logatec'], ['SI', 'Loška dolina'], ['SI', 'Loški Potok'],
     ['SI', 'Luče'], ['SI', 'Lukovica'], ['SI', 'Majšperk'], ['SI', 'Maribor'], ['SI', 'Medvode'], ['SI', 'Mengeš'],
     ['SI', 'Metlika'], ['SI', 'Mežica'], ['SI', 'Miren-Kostanjevica'], ['SI', 'Mislinja'], ['SI', 'Moravče'],
     ['SI', 'Moravske Toplice'], ['SI', 'Mozirje'], ['SI', 'Murska Sobota'], ['SI', 'Muta'], ['SI', 'Naklo'],
     ['SI', 'Nazarje'], ['SI', 'Nova Gorica'], ['SI', 'Novo mesto'], ['SI', 'Odranci'], ['SI', 'Ormož'],
     ['SI', 'Osilnica'], ['SI', 'Pesnica'], ['SI', 'Piran/Pirano'], ['SI', 'Pivka'], ['SI', 'Podčetrtek'],
     ['SI', 'Podvelka'], ['SI', 'Postojna'], ['SI', 'Preddvor'], ['SI', 'Ptuj'], ['SI', 'Puconci'],
     ['SI', 'Rače-Fram'], ['SI', 'Radeče'], ['SI', 'Radenci'], ['SI', 'Radlje ob Dravi'], ['SI', 'Radovljica'],
     ['SI', 'Ravne na Koroškem'], ['SI', 'Ribnica']],

    [['SE', 'Kronobergs län'], ['SE', 'Kalmar län'], ['SE', 'Gotlands län'], ['SE', 'Blekinge län'],
     ['SE', 'Skåne län'], ['SE', 'Hallands län'], ['SE', 'Västra Götalands län'], ['SE', 'Värmlands län'],
     ['SE', 'Örebro län'], ['SE', 'Västmanlands län'], ['SE', 'Dalarnas län'], ['SE', 'Gävleborgs län'],
     ['SE', 'Västernorrlands län'], ['SE', 'Jämtlands län'], ['SE', 'Stockholms län'], ['SE', 'Västerbottens län'],
     ['SE', 'Norrbottens län'], ['SE', 'Uppsala län'], ['SE', 'Södermanlands län'], ['SE', 'Östergötlands län'],
     ['SE', 'Jönköpings län']],

    [['SZ', 'Shiselweni'], ['SZ', 'Hhohho'], ['SZ', 'Manzini'], ['SZ', 'Lubombo']],

    [['SC', 'Beau Vallon'], ['SC', 'Bel Air'], ['SC', 'Bel Ombre'], ['SC', 'Cascade'], ['SC', 'Glacis'],
     ['SC', 'Grand Anse Mahe'], ['SC', 'Grand Anse Praslin'], ['SC', 'La Digue'], ['SC', 'English River'],
     ['SC', 'Mont Buxton'], ['SC', 'Mont Fleuri'], ['SC', 'Plaisance'], ['SC', 'Pointe Larue'],
     ['SC', 'Port Glaud'], ['SC', 'Anse aux Pins'], ['SC', 'Saint Louis'], ['SC', 'Anse Boileau'],
     ['SC', 'Takamaka'], ['SC', 'Anse Etoile'], ['SC', 'Les Mamelles'], ['SC', 'Anse Louis'],
     ['SC', 'Roche Caiman'], ['SC', 'Anse Royale'], ['SC', 'Baie Lazare'], ['SC', 'Baie Sainte Anne']],

    [['SY', 'Ar Raqqah'], ['SY', 'Halab'], ['SY', 'Dimashq'], ['SY', 'Rif Dimashq'], ['SY', 'Hamah'],
     ['SY', "Dar'a"], ['SY', "As Suwayda'"], ['SY', 'Idlib'], ['SY', 'Dayr az Zawr'], ['SY', 'Tartus'],
     ['SY', 'Al Ladhiqiyah'], ['SY', 'Al Hasakah'], ['SY', 'Al Qunaytirah'], ['SY', 'Homs']],

    [['TD', 'Sīlā'], ['TD', 'Tānjilī'], ['TD', 'Tibastī'], ['TD', 'Wādī Fīrā'], ['TD', 'Al Baṭḩah'],
     ['TD', 'Baḩr al Ghazāl'], ['TD', 'Būrkū'], ['TD', 'Shārī Bāqirmī'], ['TD', 'Innīdī'], ['TD', 'Qīrā'],
     ['TD', 'Ḥajjar Lamīs'], ['TD', 'Kānim'], ['TD', 'Al Buḩayrah'], ['TD', 'Lūqūn al Gharbī'],
     ['TD', 'Lūqūn ash Sharqī'], ['TD', 'Māndūl'], ['TD', 'Shārī al Awsaṭ'], ['TD', 'Māyū Kībbī ash Sharqī'],
     ['TD', 'Māyū Kībbī al Gharbī'], ['TD', 'Madīnat Injamīnā'], ['TD', 'Waddāy'], ['TD', 'Salāmāt']],

    [['TG', 'Région de la Kara'], ['TG', 'Région Maritime'], ['TG', 'Région des Plateaux'],
     ['TG', 'Région des Savannes'], ['TG', 'Région du Centre']],

    [['TH', 'Chanthaburi'], ['TH', 'Ratchaburi'], ['TH', 'Trat'], ['TH', 'Kanchanaburi'], ['TH', 'Chachoengsao'],
     ['TH', 'Suphan Buri'], ['TH', 'Prachin Buri'], ['TH', 'Nakhon Pathom'], ['TH', 'Nakhon Nayok'],
     ['TH', 'Samut Sakhon'], ['TH', 'Sa Kaeo'], ['TH', 'Samut Songkhram'], ['TH', 'Nakhon Ratchasima'],
     ['TH', 'Phetchaburi'], ['TH', 'Buri Ram'], ['TH', 'Prachuap Khiri Khan'], ['TH', 'Surin'],
     ['TH', 'Nakhon Si Thammarat'], ['TH', 'Si Sa Ket'], ['TH', 'Krabi'], ['TH', 'Ubon Ratchathani'],
     ['TH', 'Phangnga'], ['TH', 'Yasothon'], ['TH', 'Phuket'], ['TH', 'Chaiyaphum'], ['TH', 'Surat Thani'],
     ['TH', 'Amnat Charoen'], ['TH', 'Ranong'], ['TH', 'Nong Bua Lam Phu'], ['TH', 'Chumphon'], ['TH', 'Khon Kaen'],
     ['TH', 'Songkhla'], ['TH', 'Udon Thani'], ['TH', 'Satun'], ['TH', 'Loei'], ['TH', 'Trang'],
     ['TH', 'Nong Khai'], ['TH', 'Phatthalung'], ['TH', 'Maha Sarakham'], ['TH', 'Pattani'], ['TH', 'Yala'],
     ['TH', 'Roi Et'], ['TH', 'Kalasin'], ['TH', 'Narathiwat'], ['TH', 'Sakon Nakhon'], ['TH', 'Phatthaya'],
     ['TH', 'Nakhon Phanom'], ['TH', 'Mukdahan'], ['TH', 'Chiang Mai'], ['TH', 'Lamphun'], ['TH', 'Lampang'],
     ['TH', 'Uttaradit'], ['TH', 'Phrae'], ['TH', 'Krung Thep Maha Nakhon Bangkok'], ['TH', 'Nan'],
     ['TH', 'Samut Prakan'], ['TH', 'Phayao'], ['TH', 'Nonthaburi'], ['TH', 'Chiang Rai'], ['TH', 'Pathum Thani'],
     ['TH', 'Mae Hong Son'], ['TH', 'Phra Nakhon Si Ayutthaya'], ['TH', 'Nakhon Sawan'], ['TH', 'Ang Thong'],
     ['TH', 'Uthai Thani'], ['TH', 'Lop Buri'], ['TH', 'Kamphaeng Phet'], ['TH', 'Sing Buri'], ['TH', 'Tak'],
     ['TH', 'Chai Nat'], ['TH', 'Sukhothai'], ['TH', 'Saraburi'], ['TH', 'Phitsanulok'], ['TH', 'Chon Buri'],
     ['TH', 'Phichit'], ['TH', 'Phetchabun'], ['TH', 'Rayong']],

    [['TJ', 'Sughd'], ['TJ', 'Khatlon'], ['TJ', 'Gorno-Badakhshan']],

    [['TM', 'Lebap'], ['TM', 'Mary'], ['TM', 'Ahal'], ['TM', 'Aşgabat'], ['TM', 'Balkan'], ['TM', 'Daşoguz']],

    [['TL', 'Aileu'], ['TL', 'Oecussi'], ['TL', 'Ermera'], ['TL', 'Ainaro'], ['TL', 'Viqueque'], ['TL', 'Lautem'],
     ['TL', 'Baucau'], ['TL', 'Liquiça'], ['TL', 'Bobonaro'], ['TL', 'Manufahi'], ['TL', 'Cova Lima'],
     ['TL', 'Manatuto'], ['TL', 'Díli']],

    [['TO', "'Eua"], ['TO', "Ha'apai"], ['TO', 'Niuas'], ['TO', 'Tongatapu'], ['TO', "Vava'u"]],

    [['TT', 'Point Fortin'], ['TT', 'Diego Martin'], ['TT', 'San Juan-Laventille'], ['TT', 'Rio Claro-Mayaro'],
     ['TT', 'Eastern Tobago'], ['TT', 'Tunapuna-Piarco'], ['TT', 'San Fernando'], ['TT', 'Penal-Debe'],
     ['TT', 'Western Tobago'], ['TT', 'Arima'], ['TT', 'Sangre Grande'], ['TT', 'Port of Spain'],
     ['TT', 'Chaguanas'], ['TT', 'Siparia'], ['TT', 'Princes Town'], ['TT', 'Couva-Tabaquite-Talparo']],

    [['TN', 'Gafsa'], ['TN', 'Tozeur'], ['TN', 'Kebili'], ['TN', 'Gabès'], ['TN', 'Tunis'], ['TN', 'Medenine'],
     ['TN', 'Ariana'], ['TN', 'Tataouine'], ['TN', 'Ben Arous'], ['TN', 'La Manouba'], ['TN', 'Nabeul'],
     ['TN', 'Zaghouan'], ['TN', 'Bizerte'], ['TN', 'Béja'], ['TN', 'Jendouba'], ['TN', 'Le Kef'], ['TN', 'Siliana'],
     ['TN', 'Kairouan'], ['TN', 'Kasserine'], ['TN', 'Sidi Bouzid'], ['TN', 'Sousse'], ['TN', 'Monastir'],
     ['TN', 'Mahdia'], ['TN', 'Sfax']],

    [['TR', 'Bilecik'], ['TR', 'Rize'], ['TR', 'Bingöl'], ['TR', 'Sakarya'], ['TR', 'Bitlis'], ['TR', 'Samsun'],
     ['TR', 'Bolu'], ['TR', 'Siirt'], ['TR', 'Burdur'], ['TR', 'Sinop'], ['TR', 'Bursa'], ['TR', 'Sivas'],
     ['TR', 'Çanakkale'], ['TR', 'Tekirdağ'], ['TR', 'Çankırı'], ['TR', 'Tokat'], ['TR', 'Çorum'],
     ['TR', 'Trabzon'], ['TR', 'Denizli'], ['TR', 'Tunceli'], ['TR', 'Diyarbakır'], ['TR', 'Şanlıurfa'],
     ['TR', 'Edirne'], ['TR', 'Uşak'], ['TR', 'Elazığ'], ['TR', 'Van'], ['TR', 'Erzincan'], ['TR', 'Yozgat'],
     ['TR', 'Erzurum'], ['TR', 'Zonguldak'], ['TR', 'Eskişehir'], ['TR', 'Aksaray'], ['TR', 'Gaziantep'],
     ['TR', 'Bayburt'], ['TR', 'Giresun'], ['TR', 'Karaman'], ['TR', 'Gümüşhane'], ['TR', 'Kırıkkale'],
     ['TR', 'Hakkâri'], ['TR', 'Batman'], ['TR', 'Şırnak'], ['TR', 'Hatay'], ['TR', 'Isparta'], ['TR', 'Bartın'],
     ['TR', 'Mersin'], ['TR', 'Ardahan'], ['TR', 'İstanbul'], ['TR', 'Iğdır'], ['TR', 'İzmir'], ['TR', 'Yalova'],
     ['TR', 'Kars'], ['TR', 'Karabük'], ['TR', 'Kastamonu'], ['TR', 'Kilis'], ['TR', 'Kayseri'], ['TR', 'Osmaniye'],
     ['TR', 'Kırklareli'], ['TR', 'Düzce'], ['TR', 'Kırşehir'], ['TR', 'Kocaeli'], ['TR', 'Konya'], ['TR', 'Adana'],
     ['TR', 'Kütahya'], ['TR', 'Adıyaman'], ['TR', 'Malatya'], ['TR', 'Afyonkarahisar'], ['TR', 'Manisa'],
     ['TR', 'Ağrı'], ['TR', 'Kahramanmaraş'], ['TR', 'Amasya'], ['TR', 'Mardin'], ['TR', 'Ankara'], ['TR', 'Muğla'],
     ['TR', 'Antalya'], ['TR', 'Muş'], ['TR', 'Artvin'], ['TR', 'Nevşehir'], ['TR', 'Aydın'], ['TR', 'Niğde'],
     ['TR', 'Ordu'], ['TR', 'Balıkesir']],

    [['TV', 'Vaitupu'], ['TV', 'Nukufetau'], ['TV', 'Nukulaelae'], ['TV', 'Nanumea'], ['TV', 'Nanumanga'],
     ['TV', 'Funafuti'], ['TV', 'Nui'], ['TV', 'Niutao']],

    [['TW', 'Miaoli'], ['TW', 'Nantou'], ['TW', 'Penghu'], ['TW', 'Pingtung'], ['TW', 'Taoyuan'],
     ['TW', 'Tainan City'], ['TW', 'Tainan'], ['TW', 'Taipei City'], ['TW', 'Taipei'], ['TW', 'Taitung'],
     ['TW', 'Taichung City'], ['TW', 'Taichung'], ['TW', 'Changhua'], ['TW', 'Yunlin'], ['TW', 'Chiay City'],
     ['TW', 'Chiayi'], ['TW', 'Hsinchu'], ['TW', 'Hsinchui City'], ['TW', 'Hualien'], ['TW', 'Ilan'],
     ['TW', 'Keelung City'], ['TW', 'Kaohsiung City'], ['TW', 'Kaohsiung']],

    [['TZ', 'Kilimanjaro'], ['TZ', 'Kusini Pemba'], ['TZ', 'Kusini Unguja'], ['TZ', 'Lindi'], ['TZ', 'Mara'],
     ['TZ', 'Mbeya'], ['TZ', 'Mjini Magharibi'], ['TZ', 'Morogoro'], ['TZ', 'Mtwara'], ['TZ', 'Mwanza'],
     ['TZ', 'Pwani'], ['TZ', 'Rukwa'], ['TZ', 'Ruvuma'], ['TZ', 'Arusha'], ['TZ', 'Shinyanga'],
     ['TZ', 'Dar-es-Salaam'], ['TZ', 'Singida'], ['TZ', 'Dodoma'], ['TZ', 'Tabora'], ['TZ', 'Iringa'],
     ['TZ', 'Tanga'], ['TZ', 'Kagera'], ['TZ', 'Manyara'], ['TZ', 'Kaskazini Pemba'], ['TZ', 'Kaskazini Unguja'],
     ['TZ', 'Kigoma']],

    [['UG', 'Northern'], ['UG', 'Western'], ['UG', 'Eastern'], ['UG', 'Apac'], ['UG', 'Arua'], ['UG', 'Gulu'],
     ['UG', 'Kalangala'], ['UG', 'Kitgum'], ['UG', 'Kampala'], ['UG', 'Kiboga'], ['UG', 'Kotido'], ['UG', 'Luwero'],
     ['UG', 'Masaka'], ['UG', 'Lira'], ['UG', 'Mpigi'], ['UG', 'Moroto'], ['UG', 'Mubende'], ['UG', 'Moyo'],
     ['UG', 'Mukono'], ['UG', 'Nebbi'], ['UG', 'Nakasongola'], ['UG', 'Nakapiripirit'], ['UG', 'Rakai'],
     ['UG', 'Pader'], ['UG', 'Sembabule'], ['UG', 'Yumbe'], ['UG', 'Kayunga'], ['UG', 'Amolatar'], ['UG', 'Wakiso'],
     ['UG', 'Kaabong'], ['UG', 'Mityana'], ['UG', 'Koboko'], ['UG', 'Nakaseke'], ['UG', 'Abim'],
     ['UG', 'Lyantonde'], ['UG', 'Dokolo'], ['UG', 'Bugiri'], ['UG', 'Amuru'], ['UG', 'Busia'], ['UG', 'Maracha'],
     ['UG', 'Oyam'], ['UG', 'Iganga'], ['UG', 'Bundibugyo'], ['UG', 'Jinja'], ['UG', 'Kamuli'], ['UG', 'Bushenyi'],
     ['UG', 'Kapchorwa'], ['UG', 'Hoima'], ['UG', 'Katakwi'], ['UG', 'Kabale'], ['UG', 'Kumi'], ['UG', 'Kabarole'],
     ['UG', 'Mbale'], ['UG', 'Kasese'], ['UG', 'Pallisa'], ['UG', 'Kibaale'], ['UG', 'Soroti'], ['UG', 'Kisoro'],
     ['UG', 'Tororo'], ['UG', 'Masindi'], ['UG', 'Kaberamaido'], ['UG', 'Mbarara'], ['UG', 'Mayuge'],
     ['UG', 'Ntungamo'], ['UG', 'Sironko'], ['UG', 'Rukungiri'], ['UG', 'Amuria'], ['UG', 'Kamwenge'],
     ['UG', 'Budaka'], ['UG', 'Kanungu'], ['UG', 'Bukwa'], ['UG', 'Kyenjojo'], ['UG', 'Butaleja'], ['UG', 'Ibanda'],
     ['UG', 'Kaliro'], ['UG', 'Isingiro'], ['UG', 'Manafwa'], ['UG', 'Kiruhura'], ['UG', 'Namutumba'],
     ['UG', 'Buliisa'], ['UG', 'Bududa'], ['UG', 'Central'], ['UG', 'Bukedea'], ['UG', 'Adjumani']],

    [['UA', "Dnipropetrovs'ka Oblast'"], ['UA', "Cherkas'ka Oblast'"], ['UA', "Donets'ka Oblast'"],
     ['UA', "Chernihivs'ka Oblast'"], ['UA', "Zhytomyrs'ka Oblast'"], ['UA', "Chernivets'ka Oblast'"],
     ['UA', "Zakarpats'ka Oblast'"], ['UA', "Zaporiz'ka Oblast'"], ['UA', "Ivano-Frankivs'ka Oblast'"],
     ['UA', "Kyïvs'ka mis'ka rada"], ['UA', "Kyïvs'ka Oblast'"], ['UA', "Kirovohrads'ka Oblast'"],
     ['UA', 'Sevastopol'], ['UA', 'Respublika Krym'], ['UA', "L'vivs'ka Oblast'"], ['UA', "Mykolaïvs'ka Oblast'"],
     ['UA', "Odes'ka Oblast'"], ['UA', "Poltavs'ka Oblast'"], ['UA', "Rivnens'ka Oblast'"],
     ['UA', "Sums 'ka Oblast'"], ['UA', "Ternopil's'ka Oblast'"], ['UA', "Kharkivs'ka Oblast'"],
     ['UA', "Vinnyts'ka Oblast'"], ['UA', "Khersons'ka Oblast'"], ['UA', "Volyns'ka Oblast'"],
     ['UA', "Khmel'nyts'ka Oblast'"], ['UA', "Luhans'ka Oblast'"]],

    [['UM', 'Kingman Reef'], ['UM', 'Navassa Island'], ['UM', 'Palmyra Atoll'], ['UM', 'Wake Island'],
     ['UM', 'Baker Island'], ['UM', 'Howland Island'], ['UM', 'Johnston Atoll'], ['UM', 'Jarvis Island'],
     ['UM', 'Midway Islands']],

    [['UY', 'San José'], ['UY', 'Soriano'], ['UY', 'Tacuarembó'], ['UY', 'Treinta y Tres'], ['UY', 'Artigas'],
     ['UY', 'Canelones'], ['UY', 'Cerro Largo'], ['UY', 'Colonia'], ['UY', 'Durazno'], ['UY', 'Florida'],
     ['UY', 'Flores'], ['UY', 'Lavalleja'], ['UY', 'Maldonado'], ['UY', 'Montevideo'], ['UY', 'Paysandú'],
     ['UY', 'Río Negro'], ['UY', 'Rocha'], ['UY', 'Rivera'], ['UY', 'Salto']],

    [['US', 'Delaware'], ['US', 'Virgin Islands'], ['US', 'North Carolina'], ['US', 'Florida'], ['US', 'Vermont'],
     ['US', 'North Dakota'], ['US', 'Georgia'], ['US', 'Washington'], ['US', 'Nebraska'], ['US', 'Guam'],
     ['US', 'Wisconsin'], ['US', 'New Hampshire'], ['US', 'Hawaii'], ['US', 'West Virginia'], ['US', 'New Jersey'],
     ['US', 'Iowa'], ['US', 'Wyoming'], ['US', 'New Mexico'], ['US', 'Idaho'], ['US', 'Nevada'], ['US', 'Illinois'],
     ['US', 'New York'], ['US', 'Indiana'], ['US', 'Ohio'], ['US', 'Kansas'], ['US', 'Oklahoma'],
     ['US', 'Kentucky'], ['US', 'Oregon'], ['US', 'Virginia'], ['US', 'Louisiana'], ['US', 'Pennsylvania'],
     ['US', 'Massachusetts'], ['US', 'Alaska'], ['US', 'Puerto Rico'], ['US', 'Maryland'], ['US', 'Alabama'],
     ['US', 'Rhode Island'], ['US', 'Maine'], ['US', 'Arkansas'], ['US', 'South Carolina'], ['US', 'Michigan'],
     ['US', 'American Samoa'], ['US', 'South Dakota'], ['US', 'Minnesota'], ['US', 'Arizona'], ['US', 'Tennessee'],
     ['US', 'Missouri'], ['US', 'California'], ['US', 'Texas'], ['US', 'Northern Mariana Islands'],
     ['US', 'Colorado'], ['US', 'United States Minor Outlying Islands'], ['US', 'Mississippi'],
     ['US', 'Connecticut'], ['US', 'Utah'], ['US', 'Montana'], ['US', 'District of Columbia']],

    [['UZ', 'Qashqadaryo'], ['UZ', 'Buxoro'], ['UZ', 'Toshkent'], ['UZ', "Qoraqalpog'iston Respublikasi"],
     ['UZ', "Farg'ona"], ['UZ', 'Xorazm'], ['UZ', 'Samarqand'], ['UZ', 'Jizzax'], ['UZ', 'Sirdaryo'],
     ['UZ', 'Namangan'], ['UZ', 'Surxondaryo'], ['UZ', 'Navoiy'], ['UZ', 'Andijon'], ['UZ', 'Toshkent']],

    [['VC', 'Saint George'], ['VC', 'Saint Patrick'], ['VC', 'Grenadines'], ['VC', 'Charlotte'],
     ['VC', 'Saint Andrew'], ['VC', 'Saint David']],

    [['VE', 'Trujillo'], ['VE', 'Yaracuy'], ['VE', 'Zulia'], ['VE', 'Distrito Federal'],
     ['VE', 'Dependencias Federales'], ['VE', 'Anzoátegui'], ['VE', 'Vargas'], ['VE', 'Apure'],
     ['VE', 'Delta Amacuro'], ['VE', 'Aragua'], ['VE', 'Amazonas'], ['VE', 'Barinas'], ['VE', 'Bolívar'],
     ['VE', 'Carabobo'], ['VE', 'Cojedes'], ['VE', 'Falcón'], ['VE', 'Guárico'], ['VE', 'Lara'], ['VE', 'Mérida'],
     ['VE', 'Miranda'], ['VE', 'Monagas'], ['VE', 'Nueva Esparta'], ['VE', 'Portuguesa'], ['VE', 'Sucre'],
     ['VE', 'Táchira']],

    [['VN', 'Nghệ An'], ['VN', 'Điện Biên'], ['VN', 'Đồng Tháp'], ['VN', 'Hà Tỉnh'], ['VN', 'Đắk Nông'],
     ['VN', 'Tiền Giang'], ['VN', 'Quảng Bình'], ['VN', 'Hậu Giang'], ['VN', 'Kiên Giang'], ['VN', 'Quảng Trị'],
     ['VN', 'Cần Thơ'], ['VN', 'Vĩnh Long'], ['VN', 'Thừa Thiên-Huế'], ['VN', 'Đà Nẵng'], ['VN', 'Bến Tre'],
     ['VN', 'Quảng Nam'], ['VN', 'Hà Nội'], ['VN', 'Trà Vinh'], ['VN', 'Kon Tum'], ['VN', 'Hải Phòng'],
     ['VN', 'Sóc Trăng'], ['VN', 'Quảng Ngãi'], ['VN', 'Hồ Chí Minh [Sài Gòn]'], ['VN', 'Lai Châu'],
     ['VN', 'Bắc Kạn'], ['VN', 'Gia Lai'], ['VN', 'Lào Cai'], ['VN', 'Bắc Giang'], ['VN', 'Bình Định'],
     ['VN', 'Hà Giang'], ['VN', 'Bạc Liêu'], ['VN', 'Phú Yên'], ['VN', 'Cao Bằng'], ['VN', 'Bắc Ninh'],
     ['VN', 'Đắc Lắk'], ['VN', 'Sơn La'], ['VN', 'Bình Dương'], ['VN', 'Khánh Hòa'], ['VN', 'Yên Bái'],
     ['VN', 'Bình Phước'], ['VN', 'Lâm Đồng'], ['VN', 'Tuyên Quang'], ['VN', 'Cà Mau'], ['VN', 'Ninh Thuận'],
     ['VN', 'Lạng Sơn'], ['VN', 'Hải Duong'], ['VN', 'Tây Ninh'], ['VN', 'Quảng Ninh'], ['VN', 'Hà Nam'],
     ['VN', 'Đồng Nai'], ['VN', 'Hoà Bình'], ['VN', 'Hưng Yên'], ['VN', 'Bình Thuận'], ['VN', 'Hà Tây'],
     ['VN', 'Nam Định'], ['VN', 'Long An'], ['VN', 'Ninh Bình'], ['VN', 'Phú Thọ'], ['VN', 'Vĩnh Phúc'],
     ['VN', 'Bà Rịa-Vũng Tàu'], ['VN', 'Thái Bình'], ['VN', 'Thái Nguyên'], ['VN', 'An Giang'],
     ['VN', 'Thanh Hóa']],

    [['VU', 'Shéfa'], ['VU', 'Taféa'], ['VU', 'Torba'], ['VU', 'Malampa'], ['VU', 'Pénama'], ['VU', 'Sanma']],

    [['WS', 'Atua'], ['WS', "Satupa'itea"], ['WS', "Fa'asaleleaga"], ['WS', 'Tuamasaga'], ['WS', "Gaga'emauga"],
     ['WS', "Va'a-o-Fonoti"], ['WS', 'Gagaifomauga'], ['WS', "A'ana"], ['WS', 'Vaisigano'], ['WS', 'Palauli'],
     ['WS', 'Aiga-i-le-Tai']],

    [['YE', 'Shabwah'], ['YE', "Şan'ā'"], ['YE', "Tā'izz"], ['YE', 'Abyān'], ['YE', "'Adan"], ['YE', "'Amrān"],
     ['YE', "Al Bayḑā'"], ['YE', 'Aḑ Ḑāli‘'], ['YE', 'Dhamār'], ['YE', 'Ḩaḑramawt'], ['YE', 'Ḩajjah'],
     ['YE', 'Ibb'], ['YE', 'Al Jawf'], ['YE', 'Laḩij'], ['YE', "Ma'rib"], ['YE', 'Al Mahrah'],
     ['YE', 'Al Ḩudaydah'], ['YE', 'Al Maḩwīt'], ['YE', 'Raymah'], ['YE', "Şa'dah"]],

    [['ZA', 'Gauteng'], ['ZA', 'Western Cape'], ['ZA', 'Limpopo'], ['ZA', 'Mpumalanga'], ['ZA', 'Northern Cape'],
     ['ZA', 'Eastern Cape'], ['ZA', 'Kwazulu-Natal'], ['ZA', 'Free State'], ['ZA', 'North-West (South Africa)']],

    [['ZM', 'Northern'], ['ZM', 'North-Western'], ['ZM', 'Western'], ['ZM', 'Southern (Zambia)'], ['ZM', 'Central'],
     ['ZM', 'Copperbelt'], ['ZM', 'Eastern'], ['ZM', 'Lusaka'], ['ZM', 'Luapula']],

    [['ZW', 'Midlands'], ['ZW', 'Bulawayo'], ['ZW', 'Matabeleland North'], ['ZW', 'Harare'],
     ['ZW', 'Matabeleland South'], ['ZW', 'Manicaland'], ['ZW', 'Masvingo'], ['ZW', 'Mashonaland Central'],
     ['ZW', 'Mashonaland West'], ['ZW', 'Mashonaland East']]

]


def add_country(request):
    for country in all_countries:
        Country.objects.create(alpha_2=country[0], name=country[1])
    messages.info(request, 'Countries added successfully')
    return render(request, 'users/messages.html')


def add_city(request):
    for state in all_states:
        for i in range(len(state)):
            code = state[0][0]
            name = state[i][1]
            country = Country.objects.get(alpha_2=code)
            City.objects.create(country=country, name=name)
    messages.info(request, 'Countries added successfully')
    return HttpResponse("Cities Added Successfully")


# AJAX
def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'users/city_dropdown_list_options.html', {'cities': cities})
    # return JsonResponse(list(cities.values('id', 'name')), safe=False)


def home(request):
    all_projects = Project.objects.all().order_by('-id')[:2]
    total_data = Project.objects.count()
    latest_posts = Post.published.order_by('-publish')[:2]
    context = {
        'all_projects': all_projects,
        'total_data': total_data,
        'latest_posts': latest_posts
    }
    return render(request, 'users/base.html', context)


def load_more_project(request):
    offset = int(request.GET['offset'])
    limit = int(request.GET['limit'])
    data = Project.objects.order_by('-id')[offset:offset+limit]
    t = render_to_string('users/more_projects.html', {'data': data})
    return JsonResponse({'data': t})


def project_details(request, id, slug):
    project = get_object_or_404(Project, id=id, slug=slug)
    comments = project.projects.filter(active=True).order_by('-created')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        body = request.POST['body']

        new_comment = ProjectComment(project=project, name=name, email=email, body=body)
        new_comment.save()
        return HttpResponseRedirect('/users/project_details/'+str(id)+'/'+slug+'/')
    context = {
        'project': project,
        'id': id,
        'slug': slug,
        'comments': comments
    }
    return render(request, 'users/project_details.html', context)


# signup view
def signup_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        password1 = request.POST['password1']

        # validate email
        email = email.strip().lower()
        if ("@" not in email) or (email[-4:] not in ".com.org.edu.gov.net"):
            messages.error(request, 'Your Email, ' + email + ', Is Invalid!!!')
            return render(request, 'users/signup.html')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Your Email, ' + email + ', Already Exists. Please Try Another Email')
            return render(request, 'users/signup.html')

        # validate password
        if password != password1:
            messages.error(request, "Your Passwords Don't match")
            return render(request, 'users/signup.html')
        User.objects.create_user(email=email, first_name=first_name, last_name=last_name, password=password)
        context = {
            'email': email, 'first_name': first_name, 'last_name': last_name
        }
        return render(request, 'users/signup_success.html', context)

    return render(request, 'users/signup.html')


# view for login
def user_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        # validate email
        email = email.strip().lower()
        if ("@" not in email) or (email[-4:] not in ".com.org.edu.gov.net"):
            messages.error(request, 'Your Email, ' + email + ', Is Invalid!!!')
            return render(request, 'users/login.html')
        # email is valid but does not exist
        if not User.objects.filter(email=email).exists():
            messages.error(request, 'This email, ' + email + ', Does Not Exist...')
            return render(request, 'users/login.html')
        else:
            user = authenticate(request, username=email, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('/users/home/')
    return render(request, 'users/login.html')


# log out
@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/users/home/')


# contact me views
def contact_me(request):
    if request.method == 'POST':
        message = request.POST['message']
        full_name = request.POST['full_name']
        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        contact = ContactMe(full_name=full_name, email=email, phone_number=phone_number, address=address, message=message)
        contact.save()
        messages.success(request, "Your Message Was Sent Successfully. We'll Get Back Shortly Via Your Email Provided")
        return render(request, 'users/contact.html')

    return render(request, 'users/contact.html')


# add project views
def add_project(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        features = request.POST['features']
        github_link = request.POST['github_link']
        demo_link = request.POST['demo_link']
        image = request.FILES['image']
        date_published = request.POST['date_published']
        Project.objects.create(
            name=name, description=description, features=features, github_link=github_link,demo_link=demo_link,
            image=image, show=True, date_published=date_published
        )
        return HttpResponseRedirect('/users/home/')
    return render(request, 'users/add_project.html')


# create profile view

@login_required
def profile_create_view(request):
    user = User.objects.get(email=request.user)
    countries = Country.objects.all().order_by('alpha_2')
    context = {
        'user': user,
        'countries': countries
    }

    if request.method == 'POST':
        gender = request.POST['gender']
        date_of_birth = request.POST['date_of_birth']
        country_id = request.POST['country']
        city_id = request.POST['city']
        address = request.POST['address']
        phone_number = request.POST['phone_number']
        profile_picture = request.FILES['profile_picture']
        interest = request.POST['interest']
        about_me = request.POST['about_me']

        country = Country.objects.get(id=country_id)
        city = City.objects.get(id=city_id)

        profile = Profile.objects.get(user=user)
        profile.gender = gender
        profile.date_of_birth = date_of_birth
        profile.country = country
        profile.city = city
        profile.address = address
        profile.phone_number = phone_number
        profile.profile_picture = profile_picture
        profile.interest = interest
        profile.about_me = about_me
        profile.save()
        return HttpResponseRedirect('/users/display_profile/')

    return render(request, 'users/create_profile.html', context)


@login_required
def display_profile(request):
    user = User.objects.get(email=request.user)
    profile = Profile.objects.get(user=request.user)
    if profile.date_of_birth is None:
        messages.info(request, 'You have no profile yet. Please create your profile.')
        return HttpResponseRedirect('/users/add_profile/')
    else:
        context = {
            'email': request.user, 'gender': profile.gender, 'date_of_birth': profile.date_of_birth, 'country': profile.country,
            'city': profile.city, 'address': profile.address, 'phone_number': profile.phone_number, 'profile_picture': profile.profile_picture,
            'interest': profile.interest, 'about_me': profile.about_me, 'created': profile.created, 'updated': profile.updated,
            'first_name': user.first_name, 'last_name': user.last_name, 'date_joined': user.date_joined
        }
        return render(request, 'users/display_profile.html', context)


def user_profile(request, id):
    user = get_object_or_404(User, id=id)
    profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'users/user_profile.html', context)


def owner_profile(request):
    # user = get_object_or_404(User, id=id)
    user = User.objects.get(email='akinade.mayowa@gmail.com')
    profile = Profile.objects.get(user=user)
    context = {
        'user': user,
        'profile': profile
    }
    return render(request, 'users/owner_profile.html', context)

'''
@login_required
def profile_create_view(request):
    form = ProfileForm()
    if request.method == 'POST':
        form = ProfileForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return render(request, 'users/user_created.html')
    return render(request, 'users/create_profile.html', {'form': form})
    
def contact_me(request):
    if request.method == 'POST':
        form = ContactMeForm(request.POST)

        try:
            if form.is_valid():
                form.save(commit=True)
                messages.success(request, 'Your Message Has Been Sent Successfully')
                return HttpResponseRedirect('/users/contact_me/')
        except:
            messages.error(request, 'Your Message Failed To Be Sent')
            return HttpResponseRedirect('/users/contact_me/')

    else:
        form = ContactMeForm()
    return render(request, 'users/contact_me.html', {'form': form})

'''

def profile_details(request, id):
    user = get_object_or_404(User, id=request.user.id)
    user_profile = Profile.objects.filter(user=request.user)
    return render(request, 'users/user_profile_details.html', {'user': user, 'id': id, 'user_profile': user_profile})


@login_required
def update_profile(request):
    context = {}
    obj = get_object_or_404(ProfileForm, user=request.user)
    form = ProfileForm(data=request.POST or None, files=request.FILES or None, instance=obj)
    x = obj.profile_picture
    if form.is_valid():
        form.save(commit=True)
        return render(request, 'users/user_updated.html')
    context['form'] = form
    context['x'] = x
    return render(request, 'users/update_profile.html', context)