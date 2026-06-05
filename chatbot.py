#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  chatbot.py
#
#  A pediatric symptom checker chatbot with clinical documentation
#  Features structured data collection, red-flag detection, and references
#----------------------------------------------------------------------

import re
import random
import json
from datetime import datetime

#----------------------------------------------------------------------
#  Reference Database for Evidence-Based Citations
#----------------------------------------------------------------------
REFERENCES = {
    "AAP": "American Academy of Pediatrics - https://www.healthychildren.org",
    "AAP_FEVER": "AAP Fever Guidance - https://www.healthychildren.org/English/health-issues/conditions/fever/Pages/default.aspx",
    "AAP_OTITIS": "AAP Acute Otitis Media - https://www.healthychildren.org/English/health-issues/conditions/ear-nose-throat/Pages/Middle-Ear-Infections.aspx",
    "CDC": "CDC Child Health - https://www.cdc.gov/childrenshealth",
    "CDC_RESPIRATORY": "CDC Respiratory Illness Guidance - https://www.cdc.gov/respiratory-viruses/guidance",
    "CDC_EMERGENCY": "CDC Emergency Warning Signs - https://www.cdc.gov/emergency",
    "NHS": "NHS Children's Health - https://www.nhs.uk/conditions/fever-in-children/",
    "NHS_RASH": "NHS Childhood Rashes - https://www.nhs.uk/conditions/childhood-rashes",
    "WHO": "WHO Child Health - https://www.who.int/health-topics/child-health",
    "WHO_DEHYDRATION": "WHO Dehydration Treatment - https://www.who.int/news-room/fact-sheets/detail/diarrhoeal-disease",
    "AAP_MEDS": "AAP Medication Safety - https://www.healthychildren.org/English/safety-prevention/at-home/medication-safety/Pages/default.aspx"
}

#----------------------------------------------------------------------
#  SOAP Template for Clinical Documentation
#----------------------------------------------------------------------
class ClinicalNote:
    def __init__(self):
        self.soap = {
            "timestamp": "",
            "age": "",
            "chief_complaint": "",
            "duration": "",
            "severity": "",
            "associated_symptoms": [],
            "temperature": "",
            "hydration_status": "",
            "medications_given": [],
            "past_medical_history": "",
            "red_flag_symptoms": [],
            "disposition": "",
            "references_cited": []
        }
    
    def generate_note(self):
        """Generate a formatted clinical note"""
        note = f"""
{'='*60}
PEDIATRIC CLINICAL NOTE
{'='*60}
Date/Time: {self.soap['timestamp']}

CHIEF COMPLAINT:
{self.soap['chief_complaint']}

HISTORY OF PRESENT ILLNESS:
Patient Age: {self.soap['age']}
Symptom Duration: {self.soap['duration']}
Severity: {self.soap['severity']}
Temperature: {self.soap['temperature']}
Associated Symptoms: {', '.join(self.soap['associated_symptoms']) if self.soap['associated_symptoms'] else 'None reported'}

MEDICATIONS:
{', '.join(self.soap['medications_given']) if self.soap['medications_given'] else 'None reported'}

PAST MEDICAL HISTORY:
{self.soap['past_medical_history'] if self.soap['past_medical_history'] else 'Not available'}

RED FLAG SYMPTOMS:
{', '.join(self.soap['red_flag_symptoms']) if self.soap['red_flag_symptoms'] else 'None identified'}

HYDRATION STATUS:
{self.soap['hydration_status']}

ASSESSMENT & PLAN:
{self.soap['disposition']}

REFERENCES:
{chr(10).join(self.soap['references_cited']) if self.soap['references_cited'] else 'Standard pediatric guidelines apply'}

DISCLAIMER: This is an AI-generated preliminary assessment. 
Please consult a healthcare provider for definitive medical advice.
{'='*60}
"""
        return note

#----------------------------------------------------------------------

# LATER ON EACH CLASS SHOULD BE DEVIDED IN SEPARATE FILES FOR BETTER ORGANIZATION
# use from chatbot import ClinicalNote
# from chatbot import PediatricChatbot
# from chatbot import command_interface
# from chatbot import gPedsPats
# from chatbot import REFERENCES
#  use innit.py to make it a package and import from there
#Use Enum for better organization of symptoms and responses

#----------------------------------------------------------------------

#features to consider for future development:
# train the model on pediatric datasets and fine-tune responses based on real-world interactions and feedback from healthcare professionals
#use machine learning to analyze user input and identify patterns in symptoms, allowing for more accurate and personalized responses over time
#save clinical notes in a structured format (e.g., JSON or database) for future reference and analysis, allowing for tracking of patient history and outcomes
#save conversation history to allow for follow-up interactions and continuity of care, enabling the chatbot to provide more informed responses based on previous interactions with the same user
#add a feedback mechanism for users to rate the helpfulness of responses, allowing for continuous improvement of the chatbot's performance and accuracy based on user input and satisfaction
#add a feature to connect users with local healthcare resources (e.g., nearby pediatricians, urgent care centers, emergency rooms) based on their location and the severity of symptoms, providing actionable next steps for users seeking in-person care
#add a feature to provide educational resources (e.g., articles, videos, infographics) related to common pediatric conditions and symptoms, empowering users with knowledge to better understand and manage their child's health
#add a feature to allow users to input and track their child's symptoms over time, providing a visual timeline of symptom progression and allowing for more informed discussions with healthcare providers during in-person visits
#add a ffeature to upload photos of rashes or other visible symptoms for analysis, allowing the chatbot to provide more accurate assessments and guidance based on visual information provided by users
#add a feature to provide reminders for follow-up care (e.g., medication dosing, upcoming appointments) based on the user's interactions and the clinical note generated, helping users stay organized and on top of their child's healthcare needs
#add a feature to allow users to share the generated clinical note with their healthcare provider via email or secure messaging, facilitating communication and continuity of care between the chatbot and in-person healthcare providers


class PediatricChatbot:
    def __init__(self):
        # Build pattern-response pairs
        self.keys = []
        self.values = []
        self.references = []
        self.clinical_note = ClinicalNote()
        
        for pattern, response_data in gPedsPats:
            self.keys.append(re.compile(pattern, re.IGNORECASE))
            if isinstance(response_data, list) and len(response_data) > 0:
                # Handle both simple and extended response formats
                if isinstance(response_data[0], dict):
                    self.values.append([r["response"] for r in response_data])
                    self.references.append([r.get("reference", "") for r in response_data])
                else:
                    self.values.append(response_data)
                    self.references.append([""] * len(response_data))
            else:
                self.values.append(response_data)
                self.references.append([""])
        
        # Initialize conversation context
        self.context = {
            "age": None,
            "symptoms": [],
            "duration": None,
            "temperature": None,
            "red_flags": []
        }
    
    def respond(self, text):
        """Find a matching pattern and return an appropriate response"""
        text = text.lower().strip()
        
        # Check for red flag symptoms first
        red_flag_response = self.check_red_flags(text)
        if red_flag_response:
            return red_flag_response
        
        # Extract clinical information
        self.extract_clinical_info(text)
        
        for i in range(len(self.keys)):
            match = self.keys[i].match(text)
            if match:
                # Randomly select a response from available options
                resp_index = random.choice(range(len(self.values[i])))
                resp = self.values[i][resp_index]
                ref = self.references[i][resp_index] if resp_index < len(self.references[i]) else ""
                
                # Replace placeholders (%1, %2, etc.) with captured groups
                pos = resp.find('%')
                while pos > -1:
                    num = int(resp[pos+1:pos+2])
                    if num <= len(match.groups()):
                        replacement = match.group(num)
                        resp = resp[:pos] + replacement + resp[pos+2:]
                    pos = resp.find('%')
                
                # Add reference if available
                if ref:
                    resp += f"\n\nReference: {ref}"
                elif ref == "" and i < len(REFERENCES.values()):
                    # Add default reference for pediatric content
                    resp += f"\n\nReference: {REFERENCES.get('AAP', 'Pediatric Guidelines')}"
                
                return resp
        
        # Default response if no pattern matches
        return self.get_fallback_response()
    
    def check_red_flags(self, text):
        """Check for emergency symptoms requiring immediate care"""
        red_flag_patterns = [
            (r'(difficulty breathing|trouble breathing|struggling to breathe|shortness of breath)', 
             "  RED FLAG: Difficulty breathing is a medical emergency. Seek immediate medical care or call emergency services.\n\nReference: CDC Emergency Warning Signs"),
            (r'(seizure|convulsion|fitting|uncontrolled movements)',
             "  RED FLAG: Seizure activity requires immediate medical attention. Keep your child safe, note the time, and seek emergency care.\n\nReference: AAP Seizure Emergency Guidance"),
            (r'(blue lips|blue skin|turning blue|cyanosis)',
             "  RED FLAG: Bluish discoloration indicates low oxygen. This is a medical emergency. Call emergency services immediately.\n\nReference: CDC Emergency Signs"),
            (r'(unconscious|unresponsive|can\'t wake|won\'t wake up)',
             "  RED FLAG: Unresponsiveness is a medical emergency. Seek immediate emergency medical care.\n\nReference: AAP Emergency Guidelines"),
            (r'(severe dehydration|no urine|no tears|sunken eyes)',
             "  RED FLAG: Severe dehydration requires immediate medical evaluation, especially in infants.\n\nReference: WHO Dehydration Treatment Guidelines"),
            (r'(stiff neck|neck stiffness) with (fever|temperature)',
             "  RED FLAG: Stiff neck with fever can indicate meningitis. Seek emergency medical care immediately.\n\nReference: CDC Meningitis Signs")
        ]
        
        for pattern, response in red_flag_patterns:
            if re.search(pattern, text, re.IGNORECASE):
                self.context["red_flags"].append(pattern)
                return response
        
        return None
    
    def extract_clinical_info(self, text):
        """Extract structured clinical information from user input"""
        # Extract age
        age_match = re.search(r'(\d+)\s*(month|year|week|day|yr|mo)s?\s+old', text, re.IGNORECASE)
        if age_match:
            self.context["age"] = f"{age_match.group(1)} {age_match.group(2)}s"
            self.clinical_note.soap["age"] = self.context["age"]
        
        # Extract temperature
        temp_match = re.search(r'(\d+(?:\.\d+)?)\s*(degrees?|°|c|f|centigrade|fahrenheit)', text, re.IGNORECASE)
        if temp_match:
            temp = temp_match.group(1)
            unit = temp_match.group(2).lower()
            if 'c' in unit or 'centigrade' in unit:
                self.context["temperature"] = f"{temp}°C"
            else:
                self.context["temperature"] = f"{temp}°F"
            self.clinical_note.soap["temperature"] = self.context["temperature"]
        
        # Extract duration
        duration_match = re.search(r'(\d+)\s*(day|hour|week|minute)s?', text, re.IGNORECASE)
        if duration_match:
            self.context["duration"] = f"{duration_match.group(1)} {duration_match.group(2)}s"
            self.clinical_note.soap["duration"] = self.context["duration"]
        
        # Update timestamp
        self.clinical_note.soap["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def update_clinical_note(self, symptom, value):
        """Update the clinical note with structured information"""
        if symptom == "chief_complaint":
            self.clinical_note.soap["chief_complaint"] = value
        elif symptom == "associated":
            if value not in self.clinical_note.soap["associated_symptoms"]:
                self.clinical_note.soap["associated_symptoms"].append(value)
        elif symptom == "medication":
            self.clinical_note.soap["medications_given"].append(value)
        elif symptom == "disposition":
            self.clinical_note.soap["disposition"] = value
    
    def get_clinical_note(self):
        """Return the current clinical note"""
        return self.clinical_note.generate_note()
    
    def get_fallback_response(self):
        """Provide a clinically useful response when no pattern matches"""
        fallbacks = [
            f"""To help me better understand your child's condition, please tell me:

• Child's age and weight
• Main symptom
• Duration of symptoms (when did it start?)
• Highest temperature (if fever)
• Other symptoms (cough, rash, vomiting, diarrhea, ear pain)
• Any medications already given
• Hydration status (wet diapers, tears when crying)

This information helps determine appropriate next steps.

Reference: {REFERENCES['AAP']}""",

            f"""Please describe your child's symptoms in more detail.

Key information needed:
• How old is your child?
• When did symptoms start?
• Have symptoms improved, worsened, or stayed the same?
• Is your child eating and drinking normally?
• Any fever? If yes, what temperature?

Reference: {REFERENCES['CDC']}""",

            f"""I can help with common pediatric concerns including:
• Fever (management, when to seek care)
• Cough and respiratory symptoms
• Vomiting and diarrhea (dehydration prevention)
• Rashes and skin conditions
• Ear pain and infections
• Sore throat
• Headaches

Please describe your specific concern.

Reference: {REFERENCES['NHS']}""",

            f"""     If your child has any of these emergency symptoms, seek immediate medical care:
• Difficulty breathing
• Seizure activity
• Blue lips or skin
• Unresponsiveness or difficulty waking
• Signs of severe dehydration

Otherwise, please provide:
• Child's age
• Main symptom
• When it started

Reference: {REFERENCES['CDC_EMERGENCY']}""",

            f"""For accurate pediatric guidance, please share:

1. Child's age: ______
2. Main concern: ______
3. Duration: ______
4. Temperature (if applicable): ______
5. Other symptoms: ______
6. Medications given: ______

Example: "My 2-year-old son has had fever of 39°C for 2 days with cough"

Reference: {REFERENCES['WHO']}"""
        ]
        
        return random.choice(fallbacks)


#----------------------------------------------------------------------
#  Pediatric Symptom-Response Database with References
#----------------------------------------------------------------------
gPedsPats = [
    # Fever Management & FAQ Section
    [r'(how can i reduce my (baby|child)s? fever|reduce fever|lower fever|bring down fever|reduce temperature)',
     [{
         "response": """To help reduce your child's fever:

• Offer plenty of fluids (breastmilk, formula, water, or oral rehydration solutions) to prevent dehydration
• Dress your child in lightweight clothing - do not bundle up
• Keep the room comfortably cool (20-22°C / 68-72°F)
• Allow your child to rest
• Sponge bathing with lukewarm (not cold) water may help - avoid alcohol or ice water

MEDICATION OPTIONS (consult your pediatrician for dosing):
• Acetaminophen (paracetamol/Tylenol): For infants over 2 months
• Ibuprofen (Advil/Motrin): For infants over 6 months

     DO NOT use aspirin in children under 18 years (Reye's syndrome risk)
     Never give honey to infants under 12 months

Please provide your child's age and weight for specific dosing guidance.""",
         "reference": REFERENCES['AAP_MEDS']
     }]],
    
    [r'(fever of 38\.?5|temperature of 38\.?5|38\.5 fever|38\.5°|101\.3)',
     [{
         "response": """A temperature of 38.5°C (101.3°F) is considered a moderate fever.

CRITICAL QUESTIONS TO ANSWER:
1. How old is your child? (this is the most important factor)
2. How long has the fever been present?
3. Is your child drinking fluids normally?
4. Is your child acting normally (playing, smiling, interactive)?
5. Are there concerning symptoms (cough, rash, vomiting, stiff neck, breathing difficulty)?

GENERAL GUIDANCE:
• Under 3 months: Any fever ≥38°C requires immediate medical evaluation
• 3-6 months: Contact your pediatrician for fever ≥38.5°C
• Over 6 months: Monitor closely, treat for comfort, seek care if fever >3 days

Most fevers are caused by viral infections and resolve on their own. Focus on child's behavior, not just the number.""",
         "reference": REFERENCES['NHS']
     }]],
    
    [r'(when should i take my baby to a doctor|when should i see a doctor|doctor for fever|seek medical care for fever)',
     [{
         "response": """     CONTACT YOUR HEALTHCARE PROVIDER IMMEDIATELY IF:

• Baby is under 3 months AND temperature is 38°C (100.4°F) or higher (ER visit recommended)
• Fever lasts more than 3 days (72 hours)
• Child appears unusually sleepy, fussy, or difficult to awaken
• Child refuses multiple feedings or fluids
• Signs of dehydration develop (dry mouth, no tears, fewer wet diapers)
• Fever exceeds 40°C (104°F)
• Symptoms are worsening instead of improving
• Pain with urination or stiff neck
• Fever returns after being gone for 24+ hours

  SEEK EMERGENCY CARE IF:
• Difficulty breathing
• Seizure occurs
• Blue/gray lips or skin
• Severe headache or stiff neck with fever
• Unresponsiveness or confusion
• Unable to keep down any fluids for 12+ hours

WHEN IN DOUBT, CONTACT YOUR PEDIATRICIAN. Trust your parental instinct.""",
         "reference": REFERENCES['AAP_FEVER']
     }]],
    
    [r'(should i go to emergency room|er|emergency department|urgent care)',
     [{
         "response": """  GO TO THE EMERGENCY ROOM OR CALL AMBULANCE FOR:

• Difficulty breathing, rapid breathing, or wheezing
• Seizure or convulsion
• Blue, pale, or gray skin/lips
• Unresponsiveness or difficulty waking
• Severe dehydration (no urine for 8+ hours, sunken eyes, no tears)
• Bulging fontanelle (soft spot) in infants
• Fever in baby under 3 months (any fever)
• Stiff neck with fever (possible meningitis)
• Severe allergic reaction (swelling of face/throat, difficulty breathing)
• Blood in vomit or stool
• Head injury with vomiting or loss of consciousness

GO TO URGENT CARE FOR:
• Fever 3+ days in a child acting relatively well
• Ear pain with fever
• Persistent vomiting (able to keep some fluids down)
• Mild dehydration
• Rash with fever (but child acting ok)

For non-urgent concerns, start with your pediatrician's office. They can often provide phone guidance or same-day appointments.""",
         "reference": REFERENCES['CDC_EMERGENCY']
     }]],
    
    [r'(can i give paracetamol|acetaminophen|tylenol|panadol|paracetamol)',
     [{
         "response": """ Acetaminophen (paracetamol/Tylenol) can be given to children according to weight-based dosing:

DOSING GUIDELINES (always confirm with your pediatrician):
• Dose: 10-15 mg per kg of body weight every 4-6 hours
• Maximum: 5 doses in 24 hours
• Age minimum: Generally over 2 months (confirm with doctor)
• Available forms: Infant drops, children's suspension, chewable tablets

     IMPORTANT SAFETY:
• Never exceed recommended dose
• Use only the measuring device that comes with the medication
• Check concentration differences: Infant (80mg/0.8ml) vs Children's (160mg/5ml)
• Do not combine with other medications containing acetaminophen
• Liver damage is possible with overdose

Please tell me: Child's age and weight for specific dosing calculation.

When to use: For fever causing discomfort OR pain. Focus on treating the child, not the number.""",
         "reference": REFERENCES['AAP_MEDS']
     }]],
    
    [r'(can i give ibuprofen|advil|motrin|nurofen)',
     [{
         "response": """      Ibuprofen (Advil/Motrin) can be given to children OVER 6 MONTHS old:

DOSING GUIDELINES (weight-based, confirm with pediatrician):
• Dose: 5-10 mg per kg of body weight every 6-8 hours
• Maximum: 4 doses in 24 hours
• Age minimum: 6 months or older (never under 6 months unless instructed)
• Take with food to reduce stomach upset

     CONTRAINDICATIONS & SAFETY:
• NOT for infants under 6 months
• NOT for children who are vomiting frequently or dehydrated
• NOT for children with asthma (can trigger wheezing in some)
• NOT for children with kidney problems or stomach issues
• Do not combine with other NSAIDs
• Never exceed recommended dose

COMPARING MEDICATIONS:
• Ibuprofen lasts longer (6-8 hours vs 4-6 hours for acetaminophen)
• Ibuprofen may be better for inflammation, muscle pain, high fevers
• Can alternate with acetaminophen if needed (consult doctor first)

Please tell me child's age, weight, and if they've taken any other medications today.""",
         "reference": REFERENCES['AAP_MEDS']
     }]],
    
    [r'(baby under 3 months fever|newborn fever|infant fever|baby 2 months fever)',
     [{
         "response": """  CRITICAL: Any baby younger than 3 months with a temperature of 38°C (100.4°F) or higher requires IMMEDIATE medical evaluation.

DO NOT give any fever medication before being evaluated by a doctor.

WHY IT'S URGENT:
• Newborns have immature immune systems
• Fever in this age group can indicate serious bacterial infections
• Requires blood work, urine test, and possibly spinal fluid analysis
• Early treatment is essential

WHAT TO DO:
1. Do not wait to see if fever resolves
2. Contact your pediatrician immediately
3. Go to the emergency room if doctor advises
4. Do not give any medication before being evaluated

Normal temperature in newborns: 36.5-37.5°C (97.7-99.5°F)

HOW TO TAKE TEMPERATURE:
• Digital rectal thermometer is most accurate for infants
• Do not use ear or forehead thermometers under 3 months
• Do not use mercury thermometers

Reference: AAP Newborn Fever Guidelines""",
         "reference": REFERENCES['AAP_FEVER']
     }]],
    
    [r'(fever not going away|fever for more than 3 days|persistent fever|fever > 3 days|fever 3 days)',
     [{
         "response": """A fever lasting more than 72 hours (3 days) should be evaluated by a healthcare professional.

WHEN PERSISTENT FEVER WARRANTS EVALUATION:
• Fever >3 days with no obvious source
• Fever that went away then returned after 24+ hours
• Fever accompanied by new or worsening symptoms
• Child's condition is deteriorating
• Child is not improving despite supportive care

PLEASE PROVIDE:
• Child's age: ______
• Highest temperature recorded: ______
• Pattern of fever (constant, intermittent, rising?)
• Other symptoms that developed: ______
• Medications already given and response: ______
• Hydration status: ______

POSSIBLE CAUSES OF PERSISTENT FEVER:
• Viral infections (can last 5-7 days)
• Urinary tract infection (common, especially in girls)
• Bacterial infections (strep, pneumonia, ear infections)
• Less common: Kawasaki disease, MIS-C, occult bacteremia

DO NOT continue to treat at home without medical evaluation for persistent fever in a child who appears ill.""",
         "reference": REFERENCES['NHS']
     }]],
    
    [r'(baby has fever but acting normal|fever but playing|fever happy|fever normal behavior)',
     [{
         "response": """Good news: A child with fever who is acting normally (playing, smiling, interactive, eating/drinking) is likely fighting a mild viral infection.

WHEN A FEVER IS LESS CONCERNING:
• Child is behaving normally when fever comes down
• Drinking fluids well
• Having normal wet diapers/urination
• No breathing difficulties
• No severe pain complaints

MANAGEMENT APPROACH:
• Focus on comfort, not the fever number
• Treat fever only if child seems uncomfortable
• Encourage fluids (offer frequently)
• Let child rest as needed
• Monitor for changes in behavior

     BUT STILL MONITOR FOR:
• Fever lasting >3 days
• Any change in behavior (becoming lethargic, excessively fussy)
• Refusing fluids for 8+ hours
• Signs of dehydration
• New symptoms developing

TRUST YOUR INSTINCTS: Parents know their children best. If something feels wrong, contact your pediatrician even if child seems ok.""",
         "reference": REFERENCES['AAP_FEVER']
     }]],
    
    # Fever-related symptoms
    [r'(my )?(son|daughter|child|baby) (has|have) a fever|temperature (\d+)',
     [{
         "response": """To provide appropriate guidance for your child's fever, please tell me:

ESSENTIAL INFORMATION:
• Child's age: ______
• Highest temperature: %2° if measured
• When fever started: ______
• Other symptoms (cough, rash, vomiting, diarrhea, ear pain, sore throat, breathing difficulty): ______
• How is child acting? (playing normally, sleepy, irritable, hard to wake?)
• Is child drinking fluids? ______
• Any medications given? ______

GENERAL FEVER GUIDANCE:
• Fever is a symptom, not an illness
• Fever helps fight infection
• Focus on child's behavior, not the number
• Hydration is key

Based on your responses, I can provide specific guidance about whether to treat at home or seek medical care.

Reference: American Academy of Pediatrics Fever Guidelines""",
         "reference": REFERENCES['AAP_FEVER']
     }]],
    
    [r'fever (and|with) (cough|runny nose|sore throat)',
     [{
         "response": """Fever with cough or cold symptoms is most commonly caused by viral respiratory infections.

TYPICAL COURSE:
• Fever often lasts 3-5 days
• Cough may persist for 1-2 weeks
• Symptoms peak around days 3-4

MANAGEMENT:
• Encourage fluids to prevent dehydration
• Use a cool-mist humidifier for cough
• Saline nasal drops/spray for congestion
• Acetaminophen or ibuprofen for fever/discomfort (age/weight appropriate)
• Honey (for children over 12 months) for cough at bedtime

WHEN TO WORRY (SEEK CARE):
• Difficulty breathing or rapid breathing
• Fever >3 days without improvement
• Not drinking fluids
• Signs of dehydration
• Worsening symptoms after day 5
• Child appears toxic or very ill

Reference: CDC Respiratory Illness Guidance""",
         "reference": REFERENCES['CDC_RESPIRATORY']
     }]],
    
    [r'fever after (vaccines|immunization|shots|vaccination)',
     [{
         "response": """Mild to moderate fever after vaccination is common and expected.

NORMAL POST-VACCINE RESPONSE:
• Onset: 12-24 hours after vaccination
• Duration: Usually 24-48 hours
• Temperature: Typically 38-39°C (100.4-102.2°F)
• May be accompanied by fussiness, poor feeding, local swelling

MANAGEMENT:
• Acetaminophen (paracetamol) appropriate for fever and discomfort
• Cool compresses at injection site if swollen
• Extra fluids/breastfeeding
• Comfort and reassurance

     WHEN TO CALL DOCTOR:
• Fever >40°C (104°F)
• Fever lasting >48 hours after vaccines
• Fever in baby under 3 months (any fever)
• Seizure-like activity
• Inconsolable crying for >3 hours
• Signs of allergic reaction (hives, difficulty breathing)

Benefits of vaccination outweigh the risk of mild fever responses.

Reference: CDC Vaccine Information Statements""",
         "reference": REFERENCES['AAP']
     }]],
    
    # Cough symptoms
    [r'(coughing|cough) (all night|at night|nighttime)',
     [{
         "response": """Nighttime coughing can disrupt sleep and may indicate several conditions.

COMMON CAUSES:
• Post-nasal drip from colds or allergies
• Asthma (cough-variant)
• Acid reflux (GERD)
• Croup (barking cough, worse at night)

ASSESSMENT QUESTIONS:
• Is cough dry, wet, or barking? ______
• Any fever, wheezing, or difficulty breathing? ______
• Any known asthma or allergies? ______
• Does child snore or breathe through mouth at night? ______

HOME MANAGEMENT:
• Elevate head of bed (for children >12 months)
• Cool-mist humidifier in bedroom
• Warm bath before bedtime
• Honey (for children >12 months): 1/2 to 1 teaspoon
• Avoid milk products if they increase mucus (in some children)

  SEEK CARE IF:
• Difficulty breathing or chest retractions
• Blue lips or skin
• Stridor (noisy breathing when inhaling)
• Cannot speak or cry normally due to coughing

Reference: American Academy of Pediatrics Cough Guidance""",
         "reference": REFERENCES['AAP']
     }]],
    
    [r'barking cough|croup',
     [{
         "response": """A barking cough that sounds like a seal is characteristic of croup (laryngotracheobronchitis).

WHAT IS CROUP:
• Viral infection causing swelling around the vocal cords
• Most common in children 6 months - 3 years
• Often worse at night
• Usually lasts 5-7 days

SYMPTOMS:
• Barking cough
• Hoarse voice
• Stridor (noisy, harsh breathing when inhaling)
• Worse at night and when upset

HOME MANAGEMENT:
• Steam therapy: Run hot shower, sit in bathroom with child for 15 minutes
• Cool night air: Open freezer door or take outside briefly
• Keep child calm (crying worsens symptoms)
• Hydrate with clear fluids
• Acetaminophen or ibuprofen for fever/discomfort

  EMERGENCY SIGNS (GO TO ER):
• Stridor at rest (not just when crying)
• Difficulty breathing or chest retractions
• Agitation or fatigue
• Blue or pale skin
• Difficulty swallowing or drooling

Seek medical care if home treatments don't improve symptoms or if child worsens.

Reference: AAP Croup Management Guidelines""",
         "reference": REFERENCES['AAP']
     }]],
    
    # Vomiting and digestive issues
    [r'(baby|child) (is vomiting|vomits|threw up|vomiting)',
     [{
         "response": """Vomiting in children is common but requires close monitoring for dehydration.

ASSESSMENT NEEDED:
• Age of child: ______
• Number of vomiting episodes: ______
• Time frame: ______
• Can child keep any fluids down? ______
• Any diarrhea, fever, or abdominal pain? ______
• Blood or green bile in vomit? ______
• Recent head injury? ______

MANAGEMENT:
• Wait 30-60 minutes after last vomit before offering fluids
• Start with small amounts (1 teaspoon every 5-10 minutes)
• Use oral rehydration solution (Pedialyte) for infants, clear fluids for older children
• Advance slowly as tolerated
• Resume breastfeeding/ formula if tolerated

DEHYDRATION WARNING SIGNS:
• Dry mouth and tongue
• No tears when crying
• No urine for 6-8 hours (infants) or 8-10 hours (older children)
• Sunken eyes or fontanelle (soft spot)
• Lethargy or excessive sleepiness

  SEEK CARE IMMEDIATELY IF:
• Unable to keep any fluids down for 8+ hours
• Signs of dehydration
• Blood or bile in vomit
• Severe abdominal pain
• Vomiting after head injury
• Lethargy or confusion
• Infant under 3 months

Reference: WHO Dehydration Treatment Guidelines""",
         "reference": REFERENCES['WHO_DEHYDRATION']
     }]],
    
    [r'(diarrhea|loose stools|watery stool)',
     [{
         "response": """Diarrhea in children can lead to rapid dehydration if fluid losses are not replaced.

ASSESSMENT NEEDED:
• Child's age: ______
• Number of diarrheal stools in past 24 hours: ______
• Consistency (watery, bloody, mucus): ______
• Duration: ______
• Associated vomiting, fever, or abdominal pain? ______
• Urine output (wet diapers): ______

MANAGEMENT (MILD TO MODERATE):
• Continue breastfeeding or formula
• Offer oral rehydration solution (Pedialyte, Enfalyte)
• Avoid sugary drinks (juice, soda - worsen diarrhea)
• BRAT diet when ready: Bananas, Rice, Applesauce, Toast
• Zinc supplementation (where available) reduces severity
• Probiotics may help

DEHYDRATION PREVENTION:
• Small, frequent sips every 15-20 minutes
• 1/2 to 1 cup of ORS for each diarrheal stool
• Monitor urine output (should be every 6-8 hours)

     AVOID ANTI-DIARRHEAL MEDICATIONS in children (can be dangerous)

  SEEK CARE IMMEDIATELY IF:
• Blood or mucus in stool
• Severe dehydration signs
• High fever (>39°C / 102°F)
• Profuse watery diarrhea (cholera risk in some areas)
• Unable to keep fluids down
• Infant with decreased feeding
• Diarrhea lasting >7 days

Reference: WHO Diarrheal Disease Treatment""",
         "reference": REFERENCES['WHO_DEHYDRATION']
     }]],
    
    # Ear and respiratory symptoms
    [r'(ear hurts|earache|ear pain|ear infection)',
     [{
         "response": """Ear pain is a common complaint in children, often related to middle ear infections (otitis media) or swimmer's ear.

ASSESSMENT NEEDED:
• Child's age: ______
• Duration of pain: ______
• Any fever? Temperature: ______
• Recent or current cold symptoms? ______
• Drainage from ear (clear, yellow, bloody)? ______
• Hearing changes? ______
• Tugging at ear (in infants/toddlers)? ______

OTITIS MEDIA (MIDDLE EAR INFECTION) SIGNS:
• Ear pain, especially when lying down
• Fever
• Fussiness or irritability
• Trouble sleeping
• Fluid drainage from ear if eardrum ruptures

SWIMMER'S EAR (OTITIS EXTERNA) SIGNS:
• Pain when touching/pulling ear
• Itching in ear canal
• Discharge from ear
• Recent swimming or water exposure

MANAGEMENT:
• Acetaminophen or ibuprofen for pain
• Warm compress to affected ear
• Keep child upright (reduces pressure)
• Watchful waiting (many viral ear infections resolve without antibiotics)

  SEEK CARE IF:
• Severe pain
• Fever >39°C (102°F) with ear pain
• Symptoms in child under 6 months
• Discharge from ear
• Symptoms not improving after 2-3 days
• Both ears affected
• Speech or hearing concerns

Reference: AAP Acute Otitis Media Guidelines""",
         "reference": REFERENCES['AAP_OTITIS']
     }]],
    
    # Rash and skin issues
    [r'(rash|spots|bumps|red spots)',
     [{
         "response": """Rashes in children have many causes, from viral infections to allergic reactions.

ASSESSMENT NEEDED:
• Child's age: ______
• Location of rash (where on body): ______
• When rash appeared: ______
• Does it itch, hurt, or blister? ______
• Any fever before or with rash? ______
• New foods, medications, or lotions introduced? ______
• Recent illness? ______

RASH TYPES AND POSSIBLE CAUSES:
• Fine, pink, flat or slightly raised with fever → Viral exanthem
• Blister-like, very itchy, appears in clusters → Chickenpox
• Lacy, red cheeks then body rash → Fifth disease (parvovirus)
• Sandpaper-like texture with fever → Scarlet fever
• Red, raised, itchy welts that move → Hives (allergic reaction)
• Clusters of small blisters on hands/feet/mouth → Hand-foot-mouth

GENERAL MANAGEMENT:
• Cool compresses for itching
• Oatmeal baths
• Antihistamines for allergic reactions (age appropriate)
• Keep nails short to prevent scratching

  SEEK CARE IMMEDIATELY IF:
• Rash with difficulty breathing or swallowing
• Swelling of face, lips, or tongue
• Rash that looks like bruises or bleeding under skin
• Very painful rash (especially with fever)
• Rash that doesn't blanch (turn white when pressed)

Reference: NHS Childhood Rashes Guide""",
         "reference": REFERENCES['NHS_RASH']
     }]],
    
    # Dehydration
    [r'(dehydrated|dehydration|not drinking|no wet diapers)',
     [{
         "response": """Dehydration is a serious concern in children, especially infants and those with vomiting/diarrhea.

DEHYDRATION ASSESSMENT:
Check for these signs:

MILD DEHYDRATION (Treat at home):
• Slightly dry mouth
• Fewer wet diapers than usual
• No tears when crying
• Irritable or fussy

MODERATE DEHYDRATION (Seek medical care):
• Very dry mouth and tongue
• No urine for 6-8 hours (infants) or 8-10 hours (children)
• Sunken eyes or soft spot (fontanelle)
• Lethargic or unusually sleepy
• Cool hands and feet

SEVERE DEHYDRATION (EMERGENCY):
• No urine for 12+ hours
• Very lethargic or difficult to wake
• Rapid breathing or heart rate
• Sunken eyes with dark circles
• Skin doesn't spring back when pinched
• Cold, mottled extremities

HOME REHYDRATION PROTOCOL:
1. Oral Rehydration Solution (ORS) like Pedialyte, Enfalyte
2. Start with 1 teaspoon every 5-10 minutes
3. Increase slowly as tolerated
4. Avoid plain water (no electrolytes), juice (too much sugar), sports drinks
5. For breastfeeding infants: Continue breast milk plus ORS

  GO TO ER IMMEDIATELY FOR:
• Signs of moderate to severe dehydration
• Unable to keep any fluids down for 8+ hours
• Lethargy or difficulty waking
• Seizure

Reference: WHO Dehydration Treatment""",
         "reference": REFERENCES['WHO_DEHYDRATION']
     }]],
    
    # Breathing problems (critical)
    [r'(difficulty breathing|trouble breathing|struggling to breathe|rapid breathing|shortness of breath)',
     [{
         "response": """  DIFFICULTY BREATHING IS A MEDICAL EMERGENCY 🚨

DO NOT WAIT. Seek emergency medical care immediately if your child has:

EMERGENCY WARNING SIGNS:
• Struggling to breathe or gasping
• Chest retractions (skin pulling in at ribs, collarbone, or neck)
• Nostril flaring
• Grunting with each breath
• Blue, pale, or grey lips/face/skin
• Cannot speak or cry normally due to breathing difficulty
• Stridor (noisy, harsh sound when breathing in)
• Wheezing (whistling sound when breathing out)
• Head bobbing (infants)
• Difficulty breathing even when resting

WHILE SEEKING CARE:
• Keep child calm (crying worsens breathing difficulty)
• Sit child upright (easier than lying down)
• Remove any tight clothing
• Do not give oral medications that could cause choking
• Do not wait to see if it improves

COMMON CAUSES OF RESPIRATORY DISTRESS:
• Severe asthma attack
• Pneumonia
• Croup (severe)
• Anaphylaxis (allergic reaction)
• Foreign body aspiration (something inhaled)
• Bronchiolitis (RSV)
• COVID-19

DO NOT HESITATE - Call emergency services or go directly to the nearest emergency room.

Reference: American Academy of Pediatrics Emergency Guidelines""",
         "reference": REFERENCES['CDC_EMERGENCY']
     }]],
    
    [r'(wheezing|whistling breath|noisy breathing)',
     [{
         "response": """Wheezing (a whistling sound when breathing out) indicates narrowed airways and requires medical evaluation.

ASSESSMENT NEEDED:
• Child's age: ______
• When did wheezing start? ______
• Any known asthma or reactive airway disease? ______
• Any difficulty breathing, retractions, or blue color? ______
• Recent cold symptoms? ______
• Exposure to allergens or smoke? ______

SEVERITY ASSESSMENT:
• Mild: Wheezing only with activity, no breathing difficulty
• Moderate: Wheezing at rest, mild retractions, talking in short sentences
• Severe: Wheezing at rest, significant retractions, difficulty completing sentences (EMERGENCY)
• Life-threatening: Silent chest (no wheezing because air not moving), confusion, blue color (EMERGENCY)

HOME MANAGEMENT (ONLY FOR KNOWN MILD WHEEZING):
• Use prescribed rescue inhaler (albuterol) if available
• Sit upright, keep calm
• Remove triggers (smoke, strong smells)

  SEEK URGENT CARE FOR:
• First-time wheezing
• Wheezing with difficulty breathing
• Any wheezing in infant under 6 months
• Blue lips or skin
• Wheezing not improving with rescue medication
• Child too breathless to speak or eat

Reference: CDC Respiratory Illness Guidance""",
         "reference": REFERENCES['CDC_RESPIRATORY']
     }]],
]


#----------------------------------------------------------------------
#  Command Interface
#----------------------------------------------------------------------
def command_interface():
    """Run the pediatric chatbot with clinical documentation"""
    print("=" * 70)
    print("TiffliGPT - Pediatric Symptom Checker (Enhanced Clinical Version)")
    print("=" * 70)
    print("\nWelcome! I provide evidence-based initial guidance for pediatric symptoms.")
    print("I can help with fever, cough, rashes, vomiting, and common childhood illnesses.")
    print("\n   For best results, include:")
    print("   • Child's age (e.g., '2-year-old', '6 months')")
    print("   • Main symptom and when it started")
    print("   • Temperature (if fever)")
    print("   • Other symptoms present")
    print("   • Any medications given")
    print("\n      IMPORTANT MEDICAL DISCLAIMER:")
    print("   • This is an AI assistant for informational purposes only")
    print("   • Not a substitute for professional medical advice")
    print("   • For emergencies, call emergency services immediately")
    print("   • Always consult your pediatrician for medical decisions")
    print("\n" + "=" * 70)
    print("Type 'note' to see the clinical documentation")
    print("Type 'clear note' to reset clinical documentation")
    print("Type 'quit' to exit\n")
    print("Example: 'My 3-year-old daughter has had fever of 39°C for 2 days with cough'")
    print("=" * 70 + "\n")
    
    chatbot = PediatricChatbot()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'goodbye', 'bye']:
                print("\nTiffliGPT: Take care of your little one! Remember to contact your pediatrician for any concerns.")
                print("Clinical note saved. Goodbye! \n")
                break
            
            if user_input.lower() == 'note':
                print("\n" + chatbot.get_clinical_note())
                continue
            
            if user_input.lower() == 'clear note':
                chatbot.clinical_note = ClinicalNote()
                print("\nClinical documentation has been reset.\n")
                continue
            
            if not user_input:
                continue
            
            # Update clinical note with chief complaint
            chatbot.update_clinical_note("chief_complaint", user_input[:100])
            
            response = chatbot.respond(user_input)
            print(f"\nTiffliGPT: {response}\n")
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n\nGoodbye! Take care of your little ones! ")
            break


if __name__ == "__main__":
    command_interface() 