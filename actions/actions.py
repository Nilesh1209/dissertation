
from typing import Any, Dict, List, Text

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, FollowupAction, LoopInterrupted
from rasa_sdk.events import UserUttered
from rasa_sdk.events import ActionExecuted
from pymongo import MongoClient
from spellchecker import SpellChecker
from datetime import datetime

import re

def isValidUpgradeVersion(upgrade_version):
    # Regular expression pattern for valid upgrade version
    # pattern = r"\d{2}\.\d{2}(?:\.\d{2})?(?: LTS| Beta| 32bit| 64bit)?"
    pattern = r"\b((?:\d{2}\.\d{2}\.\d{1})|(?:\d{1}\.\d{2})|(?:\d{2}\.\d{2}))(?: LTS| Beta| 32bit| 64bit)?\b"


    # pattern = r"(?:\d{2}\.\d{2}(?:\.\d{2})?(?: LTS| Beta| 32bit| 64bit)?)"

    # if upgrade_version == "regular_version" or upgrade_version == "anything" or upgrade_version == "standard_version":
    #     return True

    
    # return bool(upgrade_version == "regular_version")
    return bool(re.match(pattern, upgrade_version))


# class Action_Setup_Printer(Action):
#     def name(self) -> Text:
#         return "action_setup_printer"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         latest_message = tracker.latest_message
#         intent = latest_message.get("intent", {}).get("name")

#         os_version = tracker.get_slot("os_version")

#         printer = tracker.get_slot("printer")

#         more_details = tracker.get_slot("more_details")



#         if printer is None:
#             dispatcher.utter_message("Which version of printer are you using? Type your version ..")
#             printer = next(tracker.get_latest_entity_values("printer"), None)
#             SlotSet("printer", tracker.latest_message['text'])
#             return [SlotSet("printer", printer)]
        
        
#         if os_version is None:
#             dispatcher.utter_message("On which version of ubuntu you wish to install the printer? Type your current version ..")
#             os_version = next(tracker.get_latest_entity_values("os_version"), None)
#             # SlotSet("os_version", tracker.latest_message['text'])
#             return [SlotSet("os_version", os_version)]  
#         else:
#             if not isValidUpgradeVersion(os_version) and os_version != "standard_version":
#                 [SlotSet("os_version", None)]
#                 dispatcher.utter_message("Please enter the correct version that you are using ..")
#                 os_version = next(tracker.get_latest_entity_values("os_version"), None)
#                 return [SlotSet("os_version", os_version)]
    
        

#         if more_details is None:
#             dispatcher.utter_message("Do you want to add more informations? ..")
#             more_details = next(tracker.get_latest_entity_values("more_details"), None)
#             return [SlotSet("more_details", more_details)]
             
#         if os_version.lower() != "standard_version":

#             if more_details.lower() != "nope":

#                 message_template = f"utter {printer.lower()}/{os_version.lower()}/{more_details.lower()}"
#             else:

#                 message_template = f"utter {printer.lower()}/{os_version.lower()}"
#         else:
                
#             if more_details.lower() == "nope":
                    
#                  message_template = f"utter {printer.lower()}"
#             else:

#                 message_template = f"utter {printer.lower()}/{more_details.lower()}"

                    
#         if message_template not in domain["responses"]:
#             # The desired utterance exists
#             # dispatcher.utter_message("The utterance exists in the domain!")
#             if message_template == f"utter {printer.lower()}/{os_version.lower()}/{more_details.lower()}":

#                 message_template = f"utter {printer.lower()}/{os_version.lower()}"

#                 if message_template not in domain["responses"]:

#                     message_template = f"utter {printer.lower()}/{more_details.lower()}"

#                 if message_template not in domain["responses"]:
                   
#                    message_template = f"utter {printer.lower()}"
                
#                 if message_template in domain["responses"]:

#                     dispatcher.utter_template(message_template, tracker)
#                     self.ask_for_feedback(dispatcher, tracker)
#                 else:

#                     dispatcher.utter_template(message_template, tracker)

#             elif message_template == f"utter {printer.lower()}/{os_version.lower()}":
                 
#                 message_template = f"utter {printer.lower()}"

#                 if message_template in domain["responses"]:

#                     dispatcher.utter_template(message_template, tracker)
#                     self.ask_for_feedback(dispatcher, tracker)
#                 else:

#                     dispatcher.utter_template(message_template, tracker)


#             elif message_template == f"utter {printer.lower()}/{more_details.lower()}":
                 
#                 message_template = f"utter {printer.lower()}"

#                 if message_template in domain["responses"]:

#                     dispatcher.utter_template(message_template, tracker)
#                     self.ask_for_feedback(dispatcher, tracker)
#                 else:

#                     dispatcher.utter_template(message_template, tracker)
#         else:
               
                
#             dispatcher.utter_template(message_template, tracker)
#             self.ask_for_feedback(dispatcher, tracker)
           

#         # self.ask_for_feedback(dispatcher, tracker)

#         return [SlotSet(slot, None) for slot in tracker.slots.keys()]

#     def ask_for_feedback(self, dispatcher: CollectingDispatcher, tracker: Tracker):
#        dispatcher.utter_template("utter_ask_solution_helpful", tracker)
    

class ActionUpgrade(Action):

    def __init__(self):
        self.ask_upgradeto_counter = 0


    def name(self) -> Text:
        return "action_upgrade"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        ubuntu_version = tracker.get_slot("ubuntu_version")
        upgrade_to = tracker.get_slot("upgrade_to")
        other_details = tracker.get_slot("other_details")


        if upgrade_to is None:
            self.ask_upgradeto_counter += 1
            dispatcher.utter_message("Which version do you want to upgrade to? Type your version ..")
            upgrade_to = next(tracker.get_latest_entity_values("upgrade_to"), None)
            return [SlotSet("upgrade_to", upgrade_to)]
        else:
            if not isValidUpgradeVersion(upgrade_to) and upgrade_to != "regular_version":
                SlotSet("upgrade_to", None)
                dispatcher.utter_message("Please enter the correct version that you want to upgrade to ..")
                upgrade_to = next(tracker.get_latest_entity_values("upgrade_to"), None)
                return [SlotSet("upgrade_to", "upgrade_to")]
            

        if ubuntu_version is None:
            dispatcher.utter_message("Which version of Ubuntu do you want to upgrade? Type your current version ..")
            ubuntu_version = next(tracker.get_latest_entity_values("ubuntu_version"), None)
            return [SlotSet("ubuntu_version", ubuntu_version)]
        else:
            if not isValidUpgradeVersion(ubuntu_version) and ubuntu_version != "anything":
                SlotSet("ubuntu_version", None)
                dispatcher.utter_message("Please enter the correct version that you are using ..")
                upgrade_to = next(tracker.get_latest_entity_values("ubuntu_version"), None)
                return [SlotSet("ubuntu_version", ubuntu_version)]
        

        if other_details is None:
            dispatcher.utter_message("Do you want to add any other details? ..")
            other_details = next(tracker.get_latest_entity_values("other_details"), None)
            return [SlotSet("other_details", other_details)]
        
        message_template = ""

        if ubuntu_version.lower()!="anything":

            if upgrade_to.lower()!="regular_version":

                if other_details.lower()!="nothing":

                    message_template = f"utter_update/from_{ubuntu_version.lower()}/to_{upgrade_to.lower()}/{other_details.lower()}"
                else:
                   
                   message_template = f"utter_update/from_{ubuntu_version.lower()}/to_{upgrade_to.lower()}"
            else:

                if other_details.lower()!="nothing":
                   
                   message_template = f"utter_update/from_{ubuntu_version.lower()}/{other_details.lower()}" 
                else:

                   message_template = f"utter_update/from_{ubuntu_version.lower()}"
        else:

            if upgrade_to.lower()!="regular_version":

                if other_details.lower()!="nothing":

                    message_template = f"utter_update/to_{upgrade_to.lower()}/{other_details.lower()}"   
                else:

                    message_template = f"utter_update/to_{upgrade_to.lower()}" 
            else:

                if other_details.lower()=="nothing":
                   
                   dispatcher.utter_message("You must provide me with some information for me to understand your needs")


        if message_template not in domain["responses"]:
            # The desired utterance exists
            # dispatcher.utter_message("The utterance exists in the domain!")
            if message_template == f"utter_update/from_{ubuntu_version}/to_{upgrade_to}/{other_details}":

                message_template = f"utter_update/from_{ubuntu_version}/to_{upgrade_to}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_update/from_{ubuntu_version}/{other_details}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_update/to_{upgrade_to}/{other_details}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_update/from_{ubuntu_version}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_update/to_{upgrade_to}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)

            


            elif message_template == f"utter_update/from_{ubuntu_version}/to_{upgrade_to}":
                    
                message_template = f"utter_update/from_{ubuntu_version}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_update/to_{upgrade_to}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)

            elif message_template == f"utter_update/from_{ubuntu_version}/{other_details}":
                    
                message_template = f"utter_update/from_{ubuntu_version}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)

            elif message_template == f"utter_update/to_{upgrade_to}/{other_details}":
                    
                message_template = f"utter_update/to_{upgrade_to}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)
        else:

            dispatcher.utter_template(message_template, tracker)
            self.ask_for_feedback(dispatcher, tracker)



        # if message_template in domain["responses"]:

        # self.ask_for_feedback(dispatcher, tracker)

        return [SlotSet(slot, None) for slot in tracker.slots.keys()]

    def ask_for_feedback(self, dispatcher: CollectingDispatcher, tracker: Tracker):
       dispatcher.utter_template("utter_ask_solution_helpful", tracker)
    

    



class ActionRecommendation(Action):

    def name(self) -> Text:
        return "action_recommend"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        software_type = tracker.get_slot("software_type")
        functionality = tracker.get_slot("functionality")
        other_info = tracker.get_slot("other_info")

        if software_type is None:
            dispatcher.utter_message("Which type of software are you looking for? Type your software type ..")
            software_type = next(tracker.get_latest_entity_values("software_type"), None)
            return [SlotSet("software_type", software_type)]

        if functionality is None:
            dispatcher.utter_message("Which functionality are you searching for? Type your answer ..")
            functionality = next(tracker.get_latest_entity_values("functionality"), None)
            return [SlotSet("functionality", functionality)]

        if other_info is None:
            dispatcher.utter_message("Do you want to add more information? ..")
            other_info = next(tracker.get_latest_entity_values("other_info"), None)
            return [SlotSet("other_info", other_info)]
        
        message_template = ""


        if functionality.lower()!="not sure":

            if software_type.lower()!="default":

                if other_info.lower()!="no thanks":

                    message_template = f"utter_recommend/{functionality.lower()}/{software_type.lower()}/{other_info.lower()}" 
                else:
                   
                   message_template = f"utter_recommend/{functionality.lower()}/{software_type.lower()}"   
            else:

                if other_info.lower()!="no thanks":
                   
                   message_template = f"utter_recommend/{functionality.lower()}/{other_info.lower()}"
                else:
                   
                   message_template = f"utter_recommend/{functionality.lower()}"
        else:

            if software_type.lower()!="default":

                if other_info.lower()!="no thanks":

                    message_template = f"utter_recommend/{software_type.lower()}/{other_info.lower()}"
                else:

                    message_template = f"utter_recommend/{software_type.lower()}"
            else:

                if other_info.lower()=="no thanks":
                   
                   dispatcher.utter_message("You must provide me with some information for me to understand your needs")


        if message_template not in domain["responses"]:
            # The desired utterance exists
            # dispatcher.utter_message("The utterance does not exists in the domain!")

            if message_template == f"utter_recommend/{functionality}/{software_type}/{other_info}":

                message_template = f"utter_recommend/{functionality}/{software_type}"

                if message_template not in domain["responses"]:
                    message_template = f"utter_recommend/{functionality.lower()}/{other_info.lower()}"
 
                if message_template not in domain["responses"]:
                    message_template = f"utter_recommend/{software_type.lower()}/{other_info.lower()}"

                if message_template not in domain["responses"]:
                    message_template = f"utter_recommend/{functionality.lower()}"

                if message_template not in domain["responses"]:
                    message_template = f"utter_recommend/{software_type.lower()}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)
                
            elif message_template == f"utter_recommend/{functionality.lower()}/{software_type.lower()}":
                    message_template = f"utter_recommend/{functionality.lower()}"

                    if message_template not in domain["responses"]:
                        message_template = f"utter_recommend/{software_type.lower()}"
 
                    if message_template in domain["responses"]:

                        dispatcher.utter_template(message_template, tracker)
                        self.ask_for_feedback(dispatcher, tracker)
                    else:

                        dispatcher.utter_template(message_template, tracker)

            elif message_template == f"utter_recommend/{functionality.lower()}/{other_info.lower()}":
                    message_template = f"utter_recommend/{functionality.lower()}"

                    if message_template in domain["responses"]:

                        dispatcher.utter_template(message_template, tracker)
                        self.ask_for_feedback(dispatcher, tracker)
                    else:

                        dispatcher.utter_template(message_template, tracker)

            elif message_template == f"utter_recommend/{software_type.lower()}/{other_info.lower()}":
                    message_template = f"utter_recommend/{software_type.lower()}"

                    if message_template in domain["responses"]:

                        dispatcher.utter_template(message_template, tracker)
                        self.ask_for_feedback(dispatcher, tracker)
                    else:

                        dispatcher.utter_template(message_template, tracker)
        else:
            # dispatcher.utter_message("The utterance does exists in the domain!")
            dispatcher.utter_template(message_template, tracker)
            self.ask_for_feedback(dispatcher, tracker)


        return [SlotSet(slot, None) for slot in tracker.slots.keys()]

    def ask_for_feedback(self, dispatcher: CollectingDispatcher, tracker: Tracker):
       dispatcher.utter_template("utter_ask_solution_helpful", tracker)
        



class Action_shutdown(Action):
    def name(self) -> Text:
        return "action_shutdown"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:

        method = tracker.get_slot("method")
        details = tracker.get_slot("details")
        verb_details = tracker.get_slot("verb_details")

        if method is None:
            dispatcher.utter_message("How do you want to shutdown your pc? Type your preferred method ..")
            method = next(tracker.get_latest_entity_values("method"), None)
            return [SlotSet("method", method)]

        if details is None:
            dispatcher.utter_message("Do you want to add more details? ..")
            details = next(tracker.get_latest_entity_values("details"), None)
            return [SlotSet("details", details)]

        message_template = ""

        if method.lower() == "any_way":

            if details.lower() == "reject":

                dispatcher.utter_message("You must provide me with some information for me to understand your needs")
            else:

                if verb_details is None:

                    message_template = f"utter_shutdown/{details.lower()}"
                else:
                    message_template = f"utter_shutdown/{verb_details.lower()}/{details.lower()}"
        else:

            if details.lower() == "reject":

                if verb_details is None:

                    message_template = f"utter_shutdown/{method.lower()}"
                else:
                    message_template = f"utter_shutdown/{method.lower()}/{verb_details.lower()}"
            else:

                if verb_details is None:

                    message_template = f"utter_shutdown/{method.lower()}/{details.lower()}"
                else:
                    message_template = f"utter_shutdown/{method.lower()}/{verb_details.lower()}/{details.lower()}"


        if message_template not in domain["responses"]:
            # The desired utterance exists
            # dispatcher.utter_message("The utterance exists in the domain!")
            if message_template == f"utter_shutdown/{method}/{verb_details}/{details}":

                message_template = f"utter_shutdown/{method}/{verb_details}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_shutdown/{method}/{details}"
 
                if message_template not in domain["responses"]:

                    message_template = f"utter_shutdown/{verb_details}/{details}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_shutdown/{method}"

                if message_template not in domain["responses"]:

                    message_template = f"utter_shutdown/{details}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)


            elif message_template == f"utter_shutdown/{method}/{verb_details}":
                    
                message_template = f"utter_shutdown/{method}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)


            elif message_template == f"utter_shutdown/{method}/{details}":
                    
                message_template = f"utter_shutdown/{method}"


                if message_template not in domain["responses"]:

                    message_template = f"utter_shutdown/{details}"
                
                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)


            elif message_template == f"utter_shutdown/{verb_details}/{details}":
                    
                message_template = f"utter_shutdown/{details}"

                if message_template in domain["responses"]:

                    dispatcher.utter_template(message_template, tracker)
                    self.ask_for_feedback(dispatcher, tracker)
                else:

                    dispatcher.utter_template(message_template, tracker)      
        else:

            dispatcher.utter_template(message_template, tracker)
            self.ask_for_feedback(dispatcher, tracker)

        return [SlotSet(slot, None) for slot in tracker.slots.keys()]

    def ask_for_feedback(self, dispatcher: CollectingDispatcher, tracker: Tracker):
       dispatcher.utter_template("utter_ask_solution_helpful", tracker)



class CheckSolutionHelpfulAction(Action):
    def name(self) -> Text:
        return "action_check_solution_helpful"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        intent = tracker.latest_message.get('intent', {}).get('name')
        
        if intent == "happy_feedback":

            continueconversation = tracker.get_slot("continueconversation")
            if continueconversation is None:
                dispatcher.utter_message("Do You Want to continue the conversation ..")
                continueconversation = next(tracker.get_latest_entity_values("continueconversation"), None)
                return [SlotSet("continueconversation", continueconversation)]
            
            if continueconversation == "i_reject":

                improvement = tracker.get_slot("improvement")
                if improvement is None:
                    dispatcher.utter_message("Do You Want to give a feedback? ..")
                    improvement = next(tracker.get_latest_entity_values("improvement"), None)
                    return [SlotSet("improvement", improvement)]
                
                current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


                client = MongoClient("mongodb://localhost:27017/")
                db = client["feedback"]  
                collection = db["feedback_details"] 

                # Creating a document to insert into the MongoDB collection
                feedback_details = {
                    "feedback": improvement,
                    "date_time": current_datetime
                }

                # Inserting the document into the MongoDB collection
                collection.insert_one(feedback_details)

                dispatcher.utter_message("It was a pleasure to help you!")

                message = f"Thank you so much for your feedback! we will work on that soon!!!"
                dispatcher.utter_message(text=message)
                message = f"Bye"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message("Ok you can ask your question or use the options provided.")
                return [SlotSet(slot, None) for slot in tracker.slots.keys()]
        elif intent == "deny":
            dispatcher.utter_template("utter_ask_technician_details", tracker)
        else:
            dispatcher.utter_template("utter_default_response", tracker)

        return [SlotSet(slot, None) for slot in tracker.slots.keys()]


from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
from rasa.shared.core.events import UserUttered
from pymongo import MongoClient
from datetime import datetime

class CollectUserInfoAction(Action):
    def name(self) -> Text:
        return "action_collect_user_info"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract user information from slots
        name = tracker.get_slot("name")
        email = tracker.get_slot("email")
        phone_number = tracker.get_slot("phone_number")
        feedback = tracker.get_slot("feedback")

        if name is None:
            dispatcher.utter_message("Can you please provide me with your full name ..")
            name = next(tracker.get_latest_entity_values("name"), None)
            return [SlotSet("name", name)]

        if email is None:
            dispatcher.utter_message("Can you please provide me with your email address ..")
            email = next(tracker.get_latest_entity_values("email"), None)
            return [SlotSet("email", email)]
        
        if phone_number is None:
            dispatcher.utter_message("Can you please provide me with your phone number ..")
            phone_number = next(tracker.get_latest_entity_values("phone_number"), None)
            return [SlotSet("phone_number", phone_number)]
        
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")


        conversation = ""
        bot_message_count = 0
        count = 0
        bye_message_position = -1

        # Count bot messages and find the position of the 'Bye' message
        for idx, event in enumerate(tracker.events):
            if event.get("event") == "bot":
                bot_message_count += 1

        # Count bot messages and find the position of the 'Bye' message
        for idx, event in enumerate(reversed(tracker.events)):
            if event.get("event") == "bot":
                count += 1
                bot_message = event.get("text")
                if bot_message and bot_message.lower() == "bye":
                    bye_message_position = count
                    break

        if bye_message_position != -1:
            target_position = bot_message_count - bye_message_position

            current_position = 0
            save_conversation = False

            # Save messages in the conversation string from the target position onwards
            for event in tracker.events:
                if event.get("event") == "bot":
                    current_position += 1
                    if current_position > target_position:
                     save_conversation = True
                    if current_position > target_position + 1:
                        save_conversation = True
                        bot_message = event.get("text")
                        if bot_message:
                            conversation += f"Bot: {bot_message}\n"
                elif save_conversation and event.get("event") == "user":
                    user_message = event.get("text")
                    if user_message:
                        conversation += f"User: {user_message}\n"
        else:
            conversation = "No 'Bye' message found in the conversation."



        # Connect to MongoDB
        client = MongoClient("mongodb://localhost:27017/")
        db = client["Technician_assistance"]
        collection = db["user_details"]

        # Creating a document to insert into the MongoDB collection
        user_details = {
            "name": name,
            "phone": phone_number,
            "email": email,
            "date_time": current_datetime,
            "messages": conversation
        }

        # Inserting the document into the MongoDB collection
        collection.insert_one(user_details)

        conversation = ""


        continueconversation2 = tracker.get_slot("continueconversation2")
        if continueconversation2 is None:
            dispatcher.utter_message("Do You Want to ask something else ..")
            continueconversation2 = next(tracker.get_latest_entity_values("continueconversation2"), None)
            return [SlotSet("continueconversation2", continueconversation2)]
        else:
            if continueconversation2 == "says_no":

                if feedback is None:
                    dispatcher.utter_message("Can you please give us feedback? ..")
                    feedback = next(tracker.get_latest_entity_values("feedback"), None)
                    return [SlotSet("feedback", feedback)]

                client = MongoClient("mongodb://localhost:27017/")
                db = client["feedback"]
                collection = db["feedback_details"]

                # Creating a document to insert into the MongoDB collection
                feedback_details = {
                    "feedback": feedback,
                    "date_time": current_datetime
                }

                # Inserting the document into the MongoDB collection
                collection.insert_one(feedback_details)

                # Respond with a confirmation message
                message = f"{name}, thank you for using our chatbot. A technician will contact you on {email} or {phone_number} shortly. Please click on save conversation from the sidebar and keep the file to send to the technician that will be assigned to you."
                dispatcher.utter_message(text=message)

                message = f"Thank you so much for your feedback! We will work on that soon!"
                dispatcher.utter_message(text=message)
                message = f"Bye"
                dispatcher.utter_message(text=message)
            else:
                dispatcher.utter_message("Ok you can ask your question or use the options provided.")
                return [SlotSet(slot, None) for slot in tracker.slots.keys()]

        return [SlotSet(slot, None) for slot in tracker.slots.keys()]
    
    
from typing import Any, Dict, List, Text
from rasa_sdk import Action, Tracker
from rasa_sdk.events import Restarted

class EndConversationAction(Action):
    def name(self) -> Text:
        return "action_end_conversation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Remove all previous events from the tracker
        tracker.events.clear()

        # Restart the conversation
        return [Restarted()]


# class CollectUserInfoAction(Action):
#     def name(self) -> Text:
#         return "action_collect_user_info"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         # Extract user information from slots
#         name = tracker.get_slot("name")
#         email = tracker.get_slot("email")
#         phone_number = tracker.get_slot("phone_number")
#         feedback = tracker.get_slot("feedback")

#         if name is None:
#             dispatcher.utter_message("Can you please provide me with your full name")
#             name = next(tracker.get_latest_entity_values("name"), None)
#             return [SlotSet("name", name)]

#         if email is None:
#             dispatcher.utter_message("can you please provide me with your email address")
#             email = next(tracker.get_latest_entity_values("email"), None)
#             return [SlotSet("email", email)]
        
#         # if phone_number is None:
#         #     dispatcher.utter_message("can you please provide me with your phone number")
#         #     phone_number = next(tracker.get_latest_entity_values("phone_number"), None)
#         #     return [SlotSet("phone_number", phone_number)]
        
#         current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
#         # Respond with a confirmation message
#         message = f"{name}, thank you for using our chatbot. A technician will contact you on {email} or {phone_number} shortly. Please Click on save conversation from the sidebar and keep the file to send to the technician that will be assigned to you."
#         dispatcher.utter_message(text=message)


#         client = MongoClient("mongodb://localhost:27017/")
#         db = client["Technician_assistance"]  
#         collection = db["user_details"]  

#         # Creating a document to insert into the MongoDB collection
#         user_details = {
#             "name": name,
#             # "phone": phone_number,
#             "email": email,
#             "date_time": current_datetime
#         }

#         # Inserting the document into the MongoDB collection
#         collection.insert_one(user_details)

#         # Close the MongoDB connection
#         client.close()

#         if feedback is None:
#             dispatcher.utter_message("Can you please give us a feedback Type only your feedback and click on Feedback else click on No ..")
#             feedback = next(tracker.get_latest_entity_values("feedback"), None)
#             return [SlotSet("feedback", feedback)]


#         client = MongoClient("mongodb://localhost:27017/")
#         db = client["feedback"]  
#         collection = db["feedback_details"] 

#         # Creating a document to insert into the MongoDB collection
#         feedback_details = {
#             "feedback": feedback,
#             "date_time": current_datetime
#         }

#                 # Inserting the document into the MongoDB collection
#         collection.insert_one(feedback_details)

#         message = f"Thank you so much for your feedback! we will work on that soon!!!"
#         dispatcher.utter_message(text=message)

#         return [SlotSet(slot, None) for slot in tracker.slots.keys()]

# from typing import Any, Dict, List, Text
# from rasa_sdk import Action, Tracker
# from rasa_sdk.events import Restarted

# class EndConversationAction(Action):
#     def name(self) -> Text:
#         return "action_end_conversation"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#          # Clear all events from the tracker
#         tracker.clear()

#         # Restart the conversation
#         return [Restarted()]
    

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import requests

# class ActionSearchInternet(Action):
#     def name(self) -> Text:
#         return "action_search_internet"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
#         user_query = tracker.latest_message.get("text")

#         # Google Custom Search API
#         search_api_url = "https://www.googleapis.com/customsearch/v1"
#         api_key = "AIzaSyC30RISeFu7PVuZU0i3vw9rI7vH3GS653U"
#         search_engine_id = "a73c6228340a0433e"  # Replace this with your Custom Search Engine ID
#         params = {
#             "key": api_key,
#             "cx": search_engine_id,
#             "q": user_query,
#         }

#         response = requests.get(search_api_url, params=params)
        
#         if response.status_code == 200:
#             # Extract relevant information from the response
#             search_results = response.json().get("items", [])
#             if search_results:
#                 max_votes_result = max(search_results, key=lambda x: x.get("votes", 0))
#                 title = max_votes_result.get("title", "")
#                 link = max_votes_result.get("link", "")
#                 snippet = max_votes_result.get("snippet", "")
#                 bot_response = f"I found this answer with the maximum votes for you:\nTitle: {title}\nLink: {link}\nSnippet: {snippet}"
#             else:
#                 bot_response = "Sorry, I couldn't find any relevant information at the moment."
#         else:
#             bot_response = "Sorry, there was an issue while searching. Please try again later."

#         dispatcher.utter_message(text=bot_response)

#         return []



import requests
from bs4 import BeautifulSoup

class ActionSearchInternet(Action):
    def name(self) -> Text:
        return "action_search_internet"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        user_query = tracker.latest_message.get("text")

        # Google Custom Search API
        search_api_url = "https://www.googleapis.com/customsearch/v1"
        api_key = "AIzaSyC30RISeFu7PVuZU0i3vw9rI7vH3GS653U"
        search_engine_id = "a73c6228340a0433e"
        params = {
            "key": api_key,
            "cx": search_engine_id,
            "q": user_query,
        }

        response = requests.get(search_api_url, params=params)
        
        if response.status_code == 200:
            # Extract relevant information from the response
            search_results = response.json().get("items", [])
            if search_results:
                max_votes_result = max(search_results, key=lambda x: x.get("votes", 0))
                title = max_votes_result.get("title", "")
                link = max_votes_result.get("link", "")
                
                # Fetch the full content (answer) from the webpage
                full_content_response = requests.get(link)
                if full_content_response.status_code == 200:
                    soup = BeautifulSoup(full_content_response.text, "html.parser")
                    # Extract the main content from the webpage using specific HTML tags and classes
                    main_content_element = soup.select("div.s-prose.js-post-body")
                    if main_content_element:
                        main_content = main_content_element[1].get_text()
                        images = main_content_element[1].find_all('img')
                        image_urls = [img.get('src') for img in images]
                        link_html = f"<a href='{link}' target='_blank'>{link}</a>"
                        images_html = ""
                        for image_url in image_urls:
                            images_html += f"<img src='{image_url}' /><br>"
                    
                    if images_html != "":

                        bot_response = f"I found this answer with the maximum votes for you:<br><br>Title: {title}<br>Link: {link_html}<br>Answer: {main_content}<br>Images:<br>{images_html}"
                    else:
                        bot_response = f"I found this answer with the maximum votes for you:<br><br>Title: {title}<br>Link: {link_html}<br>Answer: {main_content}"
                else:
                    bot_response = "Sorry, I couldn't retrieve the full answer at the moment."
            else:
                bot_response = "Sorry, I couldn't find any relevant information at the moment."
        else:
            bot_response = "Sorry, there was an issue while searching. Please try again later."

        dispatcher.utter_message(text=bot_response)

        return []


class Action_Setup_Printer(Action):
    def name(self) -> Text:
        return "action_setup_printer"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        latest_message = tracker.latest_message
        intent = latest_message.get("intent", {}).get("name")

        os_version = tracker.get_slot("os_version")

        printer = tracker.get_slot("printer")

        more_details = tracker.get_slot("more_details")



        if printer is None:
            dispatcher.utter_message("Which version of printer are you using? Type your version ..")
            printer = next(tracker.get_latest_entity_values("printer"), None)
            SlotSet("printer", tracker.latest_message['text'])
            return [SlotSet("printer", printer)]
        
        
        if os_version is None:
            dispatcher.utter_message("On which version of ubuntu you wish to install the printer? Type your current version ..")
            os_version = next(tracker.get_latest_entity_values("os_version"), None)
            # SlotSet("os_version", tracker.latest_message['text'])
            return [SlotSet("os_version", os_version)]  
        else:
            if not isValidUpgradeVersion(os_version) and os_version != "standard_version":
                [SlotSet("os_version", None)]
                dispatcher.utter_message("Please enter the correct version that you are using ..")
                os_version = next(tracker.get_latest_entity_values("os_version"), None)
                return [SlotSet("os_version", os_version)]
    
        

        if more_details is None:
            dispatcher.utter_message("Do you want to add more informations? ..")
            more_details = next(tracker.get_latest_entity_values("more_details"), None)
            return [SlotSet("more_details", more_details)]
             
        if os_version.lower() != "standard_version":

            if more_details.lower() != "nope":

                message_template = f"utter {printer.lower()}/{os_version.lower()}/{more_details.lower()}"
            else:

                message_template = f"utter {printer.lower()}/{os_version.lower()}"
        else:
                
            if more_details.lower() == "nope":
                    
                 message_template = f"utter {printer.lower()}"
            else:

                message_template = f"utter {printer.lower()}/{more_details.lower()}"
        

                    
        # Check if the desired utterance exists in the domain
        if message_template not in domain["responses"]:

            if os_version.lower() != "standard_version":

                if more_details.lower() != "nope":

                    message_template = f"{printer.lower()} {os_version.lower()} {more_details.lower()}"
                else:

                    message_template = f"{printer.lower()} {os_version.lower()}"
            else:
                    
                if more_details.lower() == "nope":
                        
                    message_template = f"{printer.lower()}"
                else:

                    message_template = f"{printer.lower()} {more_details.lower()}"

            # The desired utterance doesn't exist, try to fetch from the internet
            search_result = self.perform_internet_search(message_template)
            if search_result:
                # If search result is found, use it as the bot's response
                dispatcher.utter_message(text=search_result)
                self.ask_for_feedback(dispatcher, tracker)
            else:
                    
                #If search result is not found, use a default response
                dispatcher.utter_message(text="I'm sorry, we can't process your question right now. Do you want assistance from a technician?")
        else:
            # The desired utterance exists in the domain, use it as the bot's response
            dispatcher.utter_template(message_template, tracker)
            self.ask_for_feedback(dispatcher, tracker)

        return [SlotSet(slot, None) for slot in tracker.slots.keys()]
    
    def ask_for_feedback(self, dispatcher: CollectingDispatcher, tracker: Tracker):
        dispatcher.utter_template("utter_ask_solution_helpful", tracker)

    def perform_internet_search(self, query: str) -> str:
        # Create an instance of the ActionSearchInternet class
        search_action = ActionSearchInternet()

        # Modify the dispatcher to capture the response from the search action
        class DummyDispatcher:
            def utter_message(self, text: str):
                self.response_text = text

        dummy_dispatcher = DummyDispatcher()

        # Create a dummy tracker for the search action
        class DummyTracker:
            def __init__(self, msg_template):
                self.latest_message = {"text": msg_template}

        dummy_tracker = DummyTracker(query)

        # Execute the search action
        search_action.run(dummy_dispatcher, dummy_tracker, {})

        # Return the search result from the dummy dispatcher
        return getattr(dummy_dispatcher, "response_text", None)