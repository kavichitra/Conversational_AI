from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker, FormValidationAction
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.types import DomainDict
from rasa_sdk.forms import Action as FormsAction
from rasa_sdk.events import SlotSet


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
            paths = ["Bachelor's degree in Computer Science", "University of XYZ", "4 years"]
            
                # {"name": "Online certificate in Data Science", "provider": "Coursera", "duration": "6 months", "cost": "$1,000"},
                # {"name": "Master's degree in Business Administration", "provider": "Harvard University", "duration": "2 years", "cost": "$100,000"},
            return paths

        # Placeholder for recommendation logic based on user preferences
        educational_paths = recommendEducationalPaths(current_level_of_education, preferred_field_of_study, \
                                                    preferred_mode_of_study, preferred_location, \
                                                        time_availability)

        if educational_paths:
            # Build a string representation of the recommended educational paths
            recommended_paths_string = "\n\n".join(["- " + path for path in educational_paths])
            # Construct the response with the recommended paths
            message = f"Based on your preferences, I recommend the following educational paths:\n\n{recommended_paths_string}"
        else:
            message = "I'm sorry, but I couldn't find any educational paths that match your preferences. Please try again with different preferences."

        dispatcher.utter_message(text=message)

        return []
        
        # else:
        #     message = "Would you like to change any other preferences?"
        #     dispatcher.utter_message(text=message)
    
class validateRecommendEducationalPathsForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_recommendEducationalPathsForm"

    @staticmethod
    def currentLevelOfEducation_db() -> List[Text]:
        """Database of supported Education"""

        return ["high school", "under graduate", "post graduate", "phd"]
    
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
                return {"slot_preferredModeOfStudy": slot_value}
                        
        else:
            # validation failed, set this slot to None so that the
            # user will be asked for the slot again
            dispatcher.utter_message(text="Could you type any one (\"Online\", \"Offline\", \"Any\") of these please?")
            return {"slot_preferredModeOfStudy": None}
        
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
            SlotSet("slot_timeAvailability", None)
            # Add more SlotSet instances for other slots you want to reset
        ]

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