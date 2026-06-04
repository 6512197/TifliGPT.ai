#!/usr/bin/env python3
# -*- coding: utf-8 -*-

#----------------------------------------------------------------------
#  tiffligpt_pediatrics.py
#
#  A pediatric symptom checker chatbot for parents
#  Provides initial guidance based on reported symptoms
#----------------------------------------------------------------------

import re
import random

class PediatricChatbot:
    def __init__(self):
        # Build pattern-response pairs
        self.keys = []
        self.values = []
        
        for pattern, responses in gPedsPats:
            self.keys.append(re.compile(pattern, re.IGNORECASE))
            self.values.append(responses)
    
    def respond(self, text):
        """Find a matching pattern and return an appropriate response"""
        text = text.lower().strip()
        
        for i in range(len(self.keys)):
            match = self.keys[i].match(text)
            if match:
                # Randomly select a response from available options
                resp = random.choice(self.values[i])
                
                # Replace placeholders (%1, %2, etc.) with captured groups
                pos = resp.find('%')
                while pos > -1:
                    num = int(resp[pos+1:pos+2])
                    if num <= len(match.groups()):
                        replacement = match.group(num)
                        resp = resp[:pos] + replacement + resp[pos+2:]
                    pos = resp.find('%')
                
                return resp
        
        # Default response if no pattern matches
        return self.get_fallback_response()
    
    def get_fallback_response(self):
        """Provide a general response when no specific pattern matches"""
        fallbacks = [
            "Please tell me more about your child's symptoms. When did they start?",
            "Can you describe the symptoms in more detail? How severe are they?",
            "Is your child experiencing any fever, pain, or changes in behavior?",
            "For medical emergencies, please contact your pediatrician or seek immediate care.",
            "How old is your child, and how long have these symptoms been present?"
        ]
        return random.choice(fallbacks)


# Pediatric symptom-response database
gPedsPats = [
    # Fever-related symptoms
    [r'(my )?(son|daughter|child|baby) (has|have) a fever',
     ["How high is the temperature, how old is your child, and are there any other symptoms such as cough, rash, vomiting, or difficulty breathing? Fever is often caused by viral infections."]],
    
    [r'fever (for|of) (\d+) (days?|hours?)',
     ["Persistent %2 should be monitored closely. What is the highest temperature recorded? Has your child been eating and drinking normally?"]],
    
    [r'fever and (cough|rash|vomiting|diarrhea)',
     ["Fever with %1 should be evaluated carefully. Please describe how long this has been going on and how your child is acting overall."]],
    
    [r'fever after (vaccines|immunization)',
     ["Mild fever can occur after vaccination. What temperature are you measuring? Have you given any fever-reducing medication?"]],
    
    # Cough symptoms
    [r'(coughing|cough) all night',
     ["Is the cough dry or productive? Does your child have fever, wheezing, or trouble breathing?"]],
    
    [r'barking cough|croup',
     ["A barking cough may indicate croup. Is there noisy breathing or difficulty breathing? If your child is struggling to breathe, seek immediate medical care."]],
    
    [r'(dry|cough)',
     ["How long has the cough been present? Is it worse at night or with activity?"]],
    
    # Vomiting and digestive issues
    [r'(baby|child) (is vomiting|vomits|threw up)',
     ["How many times has your child vomited, and are they able to keep fluids down? Watch for signs of dehydration such as fewer wet diapers or no tears when crying."]],
    
    [r'vomiting after (every|each) meal',
     ["How long has this been happening, and can fluids be tolerated? This pattern warrants medical attention."]],
    
    [r'(diarrhea|loose stools)',
     ["Encourage fluids and monitor for dehydration. How long has the diarrhea been present? Are there any other symptoms like fever or vomiting?"]],
    
    [r'blood in (stool|poop|diarrhea)',
     ["Blood in the stool should be assessed promptly by a doctor. How much blood is present, and is your child in pain?"]],
    
    [r'(constipated|constipation)',
     ["When was the last bowel movement, and is your child having pain or straining? Increasing fluids and fiber may help."]],
    
    # Respiratory symptoms
    [r'(runny nose|congestion)',
     ["Does your child also have fever, cough, or difficulty breathing? Runny noses are common with viral illnesses."]],
    
    [r'(wheezing|wheeze)',
     ["Wheezing can be serious. Is your child having difficulty breathing or speaking? Any known asthma or allergies?"]],
    
    [r'(breathing fast|rapid breathing)',
     ["Rapid breathing can be concerning. Is your child struggling to breathe? Watch for nostril flaring or chest retractions."]],
    
    [r'(sore throat|throat hurts)',
     ["Does your child have fever, swollen glands, or difficulty swallowing? Strep throat is common in school-age children."]],
    
    # Ear and eye symptoms
    [r'(ear hurts|earache|ear pain)',
     ["Ear pain may indicate an ear infection. Has your child had fever or drainage from the ear?"]],
    
    [r'(tugging|pulling) at (her|his|the) ear',
     ["This may suggest ear discomfort, especially in young children. Any fever or irritability?"]],
    
    [r'(pink eye|conjunctivitis)',
     ["Is there redness, discharge, or itching in one or both eyes? Pink eye can be viral or bacterial."]],
    
    [r'(eye redness|red eye)',
     ["How long has the redness been present? Is there discharge, pain, or vision changes?"]],
    
    # Rash and skin issues
    [r'(rash|spots|bumps)',
     ["Where is the rash located, and does it itch, hurt, or occur with fever? Rashes can have many causes."]],
    
    [r'(hives|welts)',
     ["Are there breathing problems, facial swelling, or recent exposures to new foods, medications, or insect bites?"]],
    
    [r'(itchy skin|itching)',
     ["Is there a visible rash, dry skin (eczema), or recent exposure to new soaps, lotions, or fabrics?"]],
    
    [r'(hand.?foot.?mouth disease)',
     ["Hand-foot-mouth disease causes mouth sores and rash on hands/feet. It's usually viral and self-limiting. Monitor for dehydration from mouth pain."]],
    
    # Pain and injury
    [r'(stomach pain|belly ache|abdominal pain)',
     ["Where is the pain located (describe area), and is there vomiting, diarrhea, or fever? Appendicitis pain often starts near the belly button."]],
    
    [r'(headache|head hurts)',
     ["How severe is the headache (scale 1-10), and is it associated with fever, neck stiffness, or vision changes?"]],
    
    [r'(chest pain)',
     ["When did the chest pain start, and does it occur with activity or deep breathing? Chest pain in children often has benign causes but should be evaluated."]],
    
    [r'(leg pain|leg hurts)',
     ["Is the pain in one leg or both? Was there any injury? Growing pains often occur at night in both legs."]],
    
    [r'(limping|limp)',
     ["Did your child injure themselves or complain of pain? How long has the limping been present?"]],
    
    # Behavior and general symptoms
    [r'(sleepy|lethargic|very tired)',
     ["Is the sleepiness unusual for your child, and can they be easily awakened? Excessive sleepiness with fever warrants medical attention."]],
    
    [r'(not eating well|poor appetite)',
     ["How much has intake decreased, and is your baby still having normal wet diapers? Dehydration is a concern with poor intake."]],
    
    [r'(dehydrated|dehydration)',
     ["Is your child urinating normally (at least every 6-8 hours) and producing tears when crying? These are key signs of hydration status."]],
    
    [r'(nosebleed|bloody nose)',
     ["How long did the bleeding last (in minutes), and has this happened before? Most nosebleeds are harmless but recurrent ones need evaluation."]],
    
    # Serious symptoms requiring immediate attention
    [r'(difficulty breathing|trouble breathing|struggling to breathe)',
     ["Difficulty breathing is a medical emergency. Please seek immediate medical care or call emergency services right away."]],
    
    [r'(seizure|convulsion|fitting)',
     ["A seizure requires immediate medical attention. Keep your child safe, note the time, and call emergency services or go to the ER."]],
    
    [r'(turns blue|blue lips|blue skin)',
     ["This is an emergency. Call emergency services immediately. Your child needs urgent medical attention."]],
    
    # General queries and greetings
    [r'(hello|hi|hey|good morning|good afternoon)',
     ["Hello! I'm here to help with pediatric concerns. Please describe your child's symptoms and age for the best guidance."]],
    
    [r'(thank|thanks|appreciate)',
     ["You're welcome! Remember that this is general guidance only. Always consult your pediatrician for medical advice. Is there anything else I can help with?"]],
    
    [r'(quit|exit|goodbye|bye)',
     ["Take care of your little one! Remember to contact your pediatrician if symptoms worsen or you have concerns. Goodbye!"]],
]

def main():
    """Run the pediatric chatbot"""
    print("=" * 70)
    print("TiffliGPT - Pediatric Symptom Checker")
    print("=" * 70)
    print("\nWelcome! I can help provide initial guidance about your child's symptoms.")
    print("Please describe what's concerning you about your child (e.g., 'My son has a fever')")
    print("\n IMPORTANT: This is for informational purposes only.")
    print("   Always consult a healthcare provider for medical advice.")
    print("   For emergencies, call emergency services immediately.")
    print("\n" + "=" * 70)
    print("Type 'quit' to exit\n")
    
    chatbot = PediatricChatbot()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'goodbye', 'bye']:
                print("TiffliGPT: Take care of your little one! Remember to contact your pediatrician if symptoms worsen or you have concerns. Goodbye!")
                break
            
            if not user_input:
                continue
            
            response = chatbot.respond(user_input)
            print(f"TiffliGPT: {response}\n")
            
        except EOFError:
            break
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break

if __name__ == "__main__":
    main()