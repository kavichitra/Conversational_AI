from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import Action as FormsAction
from rasa_sdk.events import SlotSet
import re
import pandas as pd


class RecommendEducationalPathAction(Action):
    def name(self) -> Text:
        return "recommendEducationalPaths"  
    
       

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # if not tracker.get_slot("slot_recommendationCompleted"):
        current_level_of_education = tracker.get_slot("slot_currentLevelOfEducation")
        preferred_field_of_study = tracker.get_slot("slot_preferredFieldOfStudy")
        preferred_mode_of_study = tracker.get_slot("slot_preferredModeOfStudy")
        preferred_location = tracker.get_slot("slot_preferredLocation")
        # budget = tracker.get_slot("budget")
        time_availability = tracker.get_slot("slot_timeAvailability")
        dispatcher.utter_message(text=f"Thank you for your response. Kindly spare me a moment to get you the perfect course based on your response")
            

        def recommendEducationalPaths(current_level_of_education: Text, preferred_field_of_study: Text, preferred_mode_of_study: Text, preferred_location: Text, time_availability: Text) -> List[Dict[Text, Any]]:
        # your code for recommending educational paths based on the user's inputs goes here
        # this is just a placeholder example that returns a hardcoded list of paths
        # paths = [
        #     {"name": "Bachelor's degree in Computer Science", "provider": "University of XYZ", "duration": "4 years", "cost": "$50,000"}
        # ]
            temp = [preferred_field_of_study, preferred_mode_of_study, time_availability, preferred_location]

            if current_level_of_education == "High school":
                req_edu_lvl = ["Level 6 NFQ", "Level 7 NFQ", "Level 6 NFQ, Level 7 NFQ", "Level 7 NFQ, Level 6 NFQ"]
                
            elif current_level_of_education == "Under graduate":
                req_edu_lvl = ["Level 8 NFQ", "Level 9 NFQ", "Level 8 NFQ, Level 9 NFQ", "Level 9 NFQ, Level 8 NFQ"]

            elif current_level_of_education == "Post graduate":
                req_edu_lvl = ["Level 10 NFQ"]
                
            filters = temp

            courses_df = pd.read_excel(r'.\misc\Courses.xlsx')
            edu_df = pd.read_excel(r'.\misc\Dataset.xlsx')

            filtered_courses = list(((courses_df[courses_df["Field"] == filters[0]]))["Course"])

            if preferred_location != "NA":
                display_df = edu_df[(edu_df["Course"].isin(filtered_courses)) & (edu_df["Mode of study"] == filters[1]) & \
                                    (edu_df["Time of study"] == filters[2]) & (edu_df["County"] == filters[3]) & \
                                    (edu_df["NFQ Level"].isin(req_edu_lvl))].iloc[:5,:]
            else:
                display_df = edu_df[(edu_df["Course"].isin(filtered_courses)) & (edu_df["Mode of study"] == filters[1]) & \
                                    (edu_df["Time of study"] == filters[2]) & (edu_df["NFQ Level"].isin(req_edu_lvl))].iloc[:5,:]
                
            paths = []
            idx = 1
            for i, row in display_df.iterrows():
                paths.append(f"\nRecommendation {idx}:\n")
                course = row["Course"]
                institute = row["Course Provider"]
                mode_of_study = row["Mode of study"]
                time_of_study = row["Time of study"]
                location = row["County"]
                course_fee = row["Course fee"]

                paths.append(f"Course : {course}\n")
                paths.append(f"Course Provider : {institute}\n")
                paths.append(f"Mode of study : {mode_of_study}\n")
                paths.append(f"Time of study : {time_of_study}\n")
                paths.append(f"County : {location}\n")
                paths.append(f"Course fee : {course_fee}\n")
                idx += 1
            
                # {"name": "Online certificate in Data Science", "provider": "Coursera", "duration": "6 months", "cost": "$1,000"},
                # {"name": "Master's degree in Business Administration", "provider": "Harvard University", "duration": "2 years", "cost": "$100,000"},
            # return paths
            return paths


        # Placeholder for recommendation logic based on user preferences
        educational_paths = recommendEducationalPaths(current_level_of_education, preferred_field_of_study, \
                                                    preferred_mode_of_study, preferred_location, \
                                                        time_availability)

        if educational_paths:
            # Build a string representation of the recommended educational paths
            recommended_paths_string = "Please find below recommendations\n"
            recommended_paths_string += "".join(["- " + path for path in educational_paths])
            # Construct the response with the recommended paths
            message = f"Based on your preferences, I recommend the following educational paths:\n\n{recommended_paths_string}"
        else:
            message = "I'm sorry, but I couldn't find any educational paths that match your preferences. Please try again with different preferences."

        dispatcher.utter_message(text=message)

        return []
    
class validateRecommendEducationalPathsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_recommendEducationalPathsForm"

    @staticmethod
    def currentLevelOfEducation_db() -> List[Text]:
        """Database of supported Education"""

        return ["high school", "under graduate", "post graduate", "phd"]

    """
    STEM fields
    """        
    
    @staticmethod
    def scienceFields_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["biology", "chemistry", "physics", "environmental science", "astronomy", "geology", "neuroscience"]
    
    @staticmethod
    def technologyFields_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["computer science", "information technology", "software engineering", "data science", \
                "artificial intelligence", "robotics", "cybersecurity"]
    
    @staticmethod
    def engineeringFields_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["civil engineering", "mechanical engineering", "electrical engineering", "chemical engineering", \
                "aerospace engineering", "biomedical engineering", "industrial engineering"]
    
    @staticmethod
    def mathematicsFields_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["pure mathematics","applied mathematics","statistics","operations research","mathematical physics","cryptography"]
    

    """
    Non-STEM fields
    """
    @staticmethod
    def humanities_db() -> List[Text]:
        """Database of supported fields in humanities"""

        return ["literature", "history", "philosophy", "linguistics", "archaeology", "anthropology", "classics"]
    
    @staticmethod
    def social_sciences_db() -> List[Text]:
        """Database of supported fields in social_sciences"""

        return ["psychology", "sociology", "economics", "political Science", "geography", "anthropology", "communication studies"]
    
    @staticmethod
    def arts_db() -> List[Text]:
        """Database of supported fields in arts"""

        return ["music", "theatre", "film studies", "dance", "creative writing", "visual arts"]
    
    @staticmethod
    def businessFields_db() -> List[Text]:
        """Database of supported fields in business"""

        return ["accounting", "finance", "marketing", "management", "entrepreneurship", "international business", "human resource management"]
    
    @staticmethod
    def education_db() -> List[Text]:
        """Database of supported fields in education"""

        return ["elementary education", "secondary education", "special education", "educational leadership", "curriculum and instruction", "counseling"]
    
    @staticmethod
    def counties_db() -> List[Text]:
        """Database of supported fields in education"""

        return ["carlow", "cavan", "clare", "cork", "donegal", "dublin", "galway", "kerry", "kildare", "kilkenny", "laois", \
                "leitrim", "limerick", "longford", "louth", "mayo", "meath", "monaghan", "offaly", "roscommon", "sligo", "tipperary", \
                "waterford", "westmeath", "wexford", "wicklow", "antrim", "armagh", "derry", "down", "fermanagh", "tyrone"]

    
    @staticmethod
    def preferredModeOfStudy_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["online", "offline", "any"]    
    

    @staticmethod
    def timeAvailability_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["full time", "part time", "any"]

    def validate_slot_currentLevelOfEducation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        
        if slot_value.lower() in self.currentLevelOfEducation_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_currentLevelOfEducation": slot_value}       
            
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="Could you type any one (\"High school\", \"Under graduate\", \"Post graduate\", \"PhD\") of these please?")
            return {"slot_currentLevelOfEducation": None}
        
    def validate_slot_preferredFieldOfStudy(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        
        if slot_value.lower() in self.scienceFields_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value}      

        elif slot_value.lower() in self.technologyFields_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value} 

        elif slot_value.lower() in self.engineeringFields_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value} 

        elif slot_value.lower() in self.mathematicsFields_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value}
        
        elif slot_value.lower() in self.humanities_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value}      

        elif slot_value.lower() in self.social_sciences_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value} 

        elif slot_value.lower() in self.arts_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value} 

        elif slot_value.lower() in self.businessFields_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value}  
        
        elif slot_value.lower() in self.education_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredFieldOfStudy": slot_value}  


            
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="I am sorry, We do not have support for this field of study at the moment. Would you like to try any other fields of interest?")
            return {"slot_preferredFieldOfStudy": None}

    def validate_slot_preferredModeOfStudy(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        
        if slot_value.lower() in self.preferredModeOfStudy_db():
            # validation succeeded, set the value of the "cuisine" slot to value 
            current_level_of_education = tracker.get_slot("slot_currentLevelOfEducation")
            preferred_field_of_study = tracker.get_slot("slot_preferredFieldOfStudy")
            preferred_mode_of_study = slot_value
            if slot_value.lower() == "online":
                # message = f'Before we proceed can you please confirm the following by saying yes or no:\nCurrent level of education: {current_level_of_education}\nPreferred field of study: {preferred_field_of_study}\nPreferred mode of study: {preferred_mode_of_study}'
                # dispatcher.utter_message(text=message)
                return {"slot_preferredModeOfStudy": slot_value, "slot_preferredLocation": "NA"}
            else:
                # message = f'Before we proceed can you please confirm the following by saying yes or no:\nCurrent level of education: {current_level_of_education}\nPreferred field of study: {preferred_field_of_study}\nPreferred mode of study: {preferred_mode_of_study}'
                # dispatcher.utter_message(text=message)
                if tracker.get_slot("slot_preferredLocation") == "NA":
                    return {"slot_preferredModeOfStudy": slot_value, "slot_preferredLocation": None}
                return {"slot_preferredModeOfStudy": slot_value}
                        
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="Could you type any one (\"Online\", \"Offline\", \"Any\") of these please?")
            return {"slot_preferredModeOfStudy": None}
        
    def validate_slot_preferredLocation(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        
        if slot_value.lower() in self.counties_db() or slot_value == "NA":
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_preferredLocation": slot_value}

        else:
            dispatcher.utter_message(text="Could you please mention a location Ireland?")
            return {"slot_preferredLocation": None}
    
    def validate_slot_timeAvailability(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        
        if slot_value.lower() in self.timeAvailability_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_timeAvailability": slot_value}       
            
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="Could you type any one (\"full time\", \"part time\", \"any\") of these please?")
            return {"slot_timeAvailability": None}

    # def validate_slot_budget(
    #     self,
    #     slot_value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     """Validate cuisine value."""
        
    #     try:
    #         user_response = tracker.latest_message.get("text")
    #         pattern = r'[^a-zA-Z0-9\s]'
    #         cleaned_text = re.sub(pattern, '', user_response)
    #         matched = str(re.findall(r'(\d+)(?:\.\d{2+})?', cleaned_text))
    #         print(user_response)
    #         print(cleaned_text)
    #         print(matched[0])
    #         if len(matched[0]) != 0: 
    #             slot_value = int((matched[0]))
    #         elif slot_value.lower() == "no" or slot_value.lower() == 0:
    #             slot_value = 0
    #         else:
    #             dispatcher.utter_message(text="Please enter a valid number or \"No\" if there is no limit on budget.")
    #             return {"slot_budget" : None}
    #         return {"slot_budget": slot_value}
    #     except ValueError:
    #         dispatcher.utter_message(text="Please enter a valid number or \"No\" if there is no limit on budget.")
    #         return {"slot_budget" : None}
     

class SlotsReset(Action):
    def name(self) -> Text:
        return "slots_reset"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        # Perform the action logic here

        # Reset slots
        return [
            SlotSet("slot_currentLevelOfEducation", None),
            SlotSet("slot_preferredFieldOfStudy", None),
            SlotSet("slot_preferredModeOfStudy", None),
            SlotSet("slot_preferredLocation", None),
            SlotSet("slot_timeAvailability", None),
            SlotSet("slot_budget", None)
            # Add more SlotSet instances for other slots you want to reset
        ]

class ActionChangeSlotValue(Action):
    def name(self) -> Text:
        return "action_change_slot_value"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Extract the user's request from the latest user message
        user_request = tracker.latest_message.get("text")
        intent = tracker.latest_message.get('intent').get('name')
        # Check if the user wants to change the slot value
        if intent == "change_slot_currentLevelOfEducation":
            # Set the new slot value based on the user's request
            obj = validateRecommendEducationalPathsForm()
            entities = tracker.latest_message.get('entities')
            if len(entities) > 0:
                validation_result = obj.validate_slot_currentLevelOfEducation(entities[0], dispatcher, tracker, domain)
            else:
                return [SlotSet("slot_currentLevelOfEducation", None)]
        
        elif intent == "change_slot_preferredFieldOfStudy":
            # Set the new slot value based on the user's request
            obj = validateRecommendEducationalPathsForm()
            entities = tracker.latest_message.get('entities')
            if len(entities) > 0:
                validation_result = obj.validate_slot_preferredFieldOfStudy(entities[0], dispatcher, tracker, domain)
            else:
                return [SlotSet("slot_preferredFieldOfStudy", None)]
        
        elif intent == "change_slot_preferredModeOfStudy":
            # Set the new slot value based on the user's request
            obj = validateRecommendEducationalPathsForm()
            entities = tracker.latest_message.get('entities')
            if len(entities) > 0:
                validation_result = obj.validate_slot_preferredModeOfStudy(entities[0], dispatcher, tracker, domain)
            else:
                return [SlotSet("slot_preferredModeOfStudy", None)]
        
        elif intent == "change_slot_preferredLocation":
            # Set the new slot value based on the user's request
            obj = validateRecommendEducationalPathsForm()
            entities = tracker.latest_message.get('entities')
            if len(entities) > 0:
                validation_result = obj.validate_slot_preferredLocation(entities[0], dispatcher, tracker, domain)
            else:
                return [SlotSet("slot_preferredLocation", None)]
        
        elif intent == "change_slot_timeAvailability":
            # Set the new slot value based on the user's request
            obj = validateRecommendEducationalPathsForm()
            entities = tracker.latest_message.get('entities')
            if len(entities) > 0:
                validation_result = obj.validate_slot_timeAvailability(entities[0], dispatcher, tracker, domain)
            else:
                return [SlotSet("slot_timeAvailability", None)]
        
        elif intent == "change_slot_budget":
            # Set the new slot value based on the user's request
            obj = Validate_budget()
            entities = tracker.latest_message.get('entities')
            if len(entities) > 0:
                validation_result = obj.validate_slot_budget(entities[0], dispatcher, tracker, domain)
            else:
                return [SlotSet("slot_budget", None)]
        else:
            dispatcher.utter_message("I'm sorry, I couldn't understand your request.")
            return []
        
class Validate_budget(Action):
    def name(self) -> Text:
        return "action_validate_budget"

    def run(self, dispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        try:
            user_response = tracker.latest_message.get("text")
            pattern = r'[^a-zA-Z0-9\s]'
            cleaned_text = re.sub(pattern, '', user_response)
            matched = str(re.findall(r'(\d+)(?:\.\d{2+})?', cleaned_text))
            print(user_response)
            print(cleaned_text)
            print(matched[0])
            if len(matched[0]) != 0: 
                slot_value = int((matched[0]))
            elif slot_value.lower() == "no" or slot_value.lower() == 0:
                slot_value = 0
            else:
                dispatcher.utter_message(text="Please enter a valid number or \"No\" if there is no limit on budget.")
                return {"slot_budget" : None}
            return {"slot_budget": slot_value}
        except ValueError:
            dispatcher.utter_message(text="Please enter a valid number or \"No\" if there is no limit on budget.")
            return {"slot_budget" : None}

# class TransitionToForm2aAction(Action):
#     def name(self) -> Text:
#         return "action_transition_to_form2a"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         return [SlotSet("requested_slot", "slot_preferredModeOfStudy")]
    
# class TransitionToForm2bAction(Action):
#     def name(self) -> Text:
#         return "action_transition_to_form2b"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any]
#     ) -> List[Dict[Text, Any]]:
#         return [SlotSet("requested_slot", "slot_preferredModeOfStudy")] 


class validateRecommendEducationalPathsForm2a(FormValidationAction):
    def name(self) -> Text:
        return "validate_recommendEducationalPathsForm2a"

    @staticmethod
    def timeAvailability_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["full time", "part time", "any"]
    
    def validate_slot_timeAvailability(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        
        if slot_value.lower() in self.timeAvailability_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_timeAvailability": slot_value}       
            
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="Could you type any one (\"full time\", \"part time\", \"any\") of these please?")
            return {"slot_timeAvailability": None}
        
class validateRecommendEducationalPathsForm2b(FormValidationAction):
    def name(self) -> Text:
        return "validate_recommendEducationalPathsForm2b"

    @staticmethod
    def timeAvailability_db() -> List[Text]:
        """Database of supported fields in science"""

        return ["full time", "part time", "any"]
    
    def validate_slot_timeAvailability(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate cuisine value."""
        
        
        if slot_value.lower() in self.timeAvailability_db():
            # validation succeeded, set the value of the "cuisine" slot to value
            return {"slot_timeAvailability": slot_value}       
            
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="Could you type any one (\"full time\", \"part time\", \"any\") of these please?")
            return {"slot_timeAvailability": None}


# class EducationalPathForm(FormsAction):
#     def name(self) -> Text:
#         return "EducationalPathForm"

#     @staticmethod
#     def required_slots(tracker: Tracker) -> List[Text]:
#         return ["current_level_of_education", "preferred_field_of_study", "preferred_mode_of_study", "preferred_location", "budget", "time_availability", "career_goals"]

#     def slot_mappings(self) -> Dict[Text, Any]:
#         return {
#             "current_level_of_education": [self.from_entity(entity="current_level_of_education"), self.from_text()],
#             "preferred_field_of_study": [self.from_entity(entity="preferred_field_of_study"), self.from_text()],
#             "preferred_mode_of_study": [self.from_entity(entity="preferred_mode_of_study"), self.from_text()],
#             "preferred_location": [self.from_entity(entity="preferred_location"), self.from_text()],
#             "budget": [self.from_entity(entity="budget"), self.from_text()],
#             "time_availability": [self.from_entity(entity="time_availability"), self.from_text()],
#             "career_goals": [self.from_entity(entity="career_goals"), self.from_text()],
#         }

#     def submit(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict]:
#         dispatcher.utter_message(template="utter_recommend_educational_path")
#         return [RecommendEducationalPathAction().run(dispatcher, tracker, domain)]


# class action_fallback(Action):
#     def name(self) -> Text:
#         return "action_fallback"

#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message("I'm sorry, I didn't understand. Could you please repeat that?")
#         return []