# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from contextlib import closing
from urllib.request import urlopen
import json
import logging

WEATHER = {
	0: "Soleil",
	1: "Peu nuageux",
	2: "Ciel voilé",
	3: "Nuageux",
	4: "Très nuageux",
	5: "Couvert",
	6: "Brouillard",
	7: "Brouillard givrant",
	10: "Pluie faible",
	11: "Pluie modérée",
	12: "Pluie forte",
	13: "Pluie faible verglaçante",
	14: "Pluie modérée verglaçante",
	15: "Pluie forte verglaçante",
	16: "Bruine",
	20: "Neige faible",
	21: "Neige modérée",
	22: "Neige forte",
	30: "Pluie et neige mêlées faibles",
	31: "Pluie et neige mêlées modérées",
	32: "Pluie et neige mêlées fortes",
	40: "Averses de pluie locales et faibles",
	41: "Averses de pluie locales",
	42: "Averses locales et fortes",
	43: "Averses de pluie faibles",
	44: "Averses de pluie",
	45: "Averses de pluie fortes",
	46: "Averses de pluie faibles et fréquentes",
	47: "Averses de pluie fréquentes",
	48: "Averses de pluie fortes et fréquentes",
	60: "Averses de neige localisées et faibles",
	61: "Averses de neige localisées",
	62: "Averses de neige localisées et fortes",
	63: "Averses de neige faibles",
	64: "Averses de neige",
	65: "Averses de neige fortes",
	66: "Averses de neige faibles et fréquentes",
	67: "Averses de neige fréquentes",
	68: "Averses de neige fortes et fréquentes",
	70: "Averses de pluie et neige mêlées localisées et faibles",
	71: "Averses de pluie et neige mêlées localisées",
	72: "Averses de pluie et neige mêlées localisées et fortes",
	73: "Averses de pluie et neige mêlées faibles",
	74: "Averses de pluie et neige mêlées",
	75: "Averses de pluie et neige mêlées fortes",
	76: "Averses de pluie et neige mêlées faibles et nombreuses",
	77: "Averses de pluie et neige mêlées fréquentes",
	78: "Averses de pluie et neige mêlées fortes et fréquentes",
	100: "Orages faibles et locaux",
	101: "Orages locaux",
	102: "Orages fort et locaux",
	103: "Orages faibles",
	104: "Orages",
	105: "Orages forts",
	106: "Orages faibles et fréquents",
	107: "Orages fréquents",
	108: "Orages forts et fréquents",
	120: "Orages faibles et locaux de neige ou grésil",
	121: "Orages locaux de neige ou grésil",
	122: "Orages locaux de neige ou grésil",
	123: "Orages faibles de neige ou grésil",
	124: "Orages de neige ou grésil",
	125: "Orages de neige ou grésil",
	126: "Orages faibles et fréquents de neige ou grésil",
	127: "Orages fréquents de neige ou grésil",
	128: "Orages fréquents de neige ou grésil",
	130: "Orages faibles et locaux de pluie et neige mêlées ou grésil",
	131: "Orages locaux de pluie et neige mêlées ou grésil",
	132: "Orages fort et locaux de pluie et neige mêlées ou grésil",
	133: "Orages faibles de pluie et neige mêlées ou grésil",
	134: "Orages de pluie et neige mêlées ou grésil",
	135: "Orages forts de pluie et neige mêlées ou grésil",
	136: "Orages faibles et fréquents de pluie et neige mêlées ou grésil",
	137: "Orages fréquents de pluie et neige mêlées ou grésil",
	138: "Orages forts et fréquents de pluie et neige mêlées ou grésil",
	140: "Pluies orageuses",
	141: "Pluie et neige mêlées à caractère orageux",
	142: "Neige à caractère orageux",
	210: "Pluie faible intermittente",
	211: "Pluie modérée intermittente",
	212: "Pluie forte intermittente",
	220: "Neige faible intermittente",
	221: "Neige modérée intermittente",
	222: "Neige forte intermittente",
	230: "Pluie et neige mêlées",
	231: "Pluie et neige mêlées",
	232: "Pluie et neige mêlées",
	235: "Averses de grêle",
}

class ActionMeteo(Action):

    def name(self) -> Text:
        return "action_weather"

    def run(self, dispatcher: CollectingDispatcher,
			tracker: Tracker, 
			domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        city = tracker.get_slot("city")
        logger = logging.getLogger(__name__)
        logging.basicConfig(level='DEBUG')
        logger.info(city)

        with closing(urlopen('https://api.meteo-concept.com/api/location/cities?token=264861f8207a68de538729a029817d72b013c53b078d286e681d0acb33c1b328&search='+city)) as f :
            insee = json.loads(f.read())['cities'][0]['insee']

        with closing(urlopen('https://api.meteo-concept.com/api/forecast/daily/3/period/2?token=264861f8207a68de538729a029817d72b013c53b078d286e681d0acb33c1b328&amp;insee='+insee)) as f:
            forecast = json.loads(f.read())['forecast']
            out_message = u"Le temps prévu pour l'après-midi dans trois jours est : \"{}\"".format(WEATHER[forecast['weather']])
            dispatcher.utter_message(out_message)
        return []

            
            

