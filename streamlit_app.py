import random
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="NUR3302 Nutrition Student Hub",
    page_icon="🍎",
    layout="wide",
    initial_sidebar_state="expanded",
)

FSC_RED = "#BA0C2F"
FSC_DARK = "#6E071C"
FSC_CREAM = "#F7F2EA"
FSC_CLAY = "#C49A6F"
FSC_TEXT = "#242424"

st.markdown(
    f"""
    <style>
    .stApp {{
        background: linear-gradient(180deg, #ffffff 0%, {FSC_CREAM} 100%);
        color: {FSC_TEXT};
    }}
    [data-testid="stSidebar"] {{
        background: {FSC_DARK};
    }}
    [data-testid="stSidebar"] * {{
        color: white;
    }}
    h1, h2, h3 {{
        color: {FSC_DARK};
    }}
    .hero {{
        border-left: 8px solid {FSC_RED};
        background: white;
        padding: 1.2rem 1.4rem;
        border-radius: 14px;
        margin-bottom: 1rem;
        box-shadow: 0 2px 10px rgba(0,0,0,.08);
    }}
    .topic-card {{
        background: white;
        border: 1px solid #eadde0;
        border-radius: 14px;
        padding: 1rem;
        min-height: 150px;
        box-shadow: 0 2px 8px rgba(0,0,0,.05);
    }}
    .pearl {{
        background: #fff5f7;
        border-left: 5px solid {FSC_RED};
        padding: .85rem 1rem;
        border-radius: 8px;
        margin: .6rem 0;
    }}
    .warning {{
        background: #fff8e8;
        border-left: 5px solid {FSC_CLAY};
        padding: .85rem 1rem;
        border-radius: 8px;
    }}
    div.stButton > button {{
        background: {FSC_RED};
        color: white;
        border: 0;
        border-radius: 10px;
        font-weight: 600;
    }}
    div.stButton > button:hover {{
        background: {FSC_DARK};
        color: white;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ----------------------------
# Content data
# ----------------------------

MACROS = {
    "Carbohydrates": {
        "icon": "🌾",
        "functions": "Primary energy source, supports brain and red blood cell metabolism, and supplies fiber when minimally processed.",
        "sources": "Whole grains, fruits, vegetables, legumes, milk, and yogurt.",
        "nursing": "Match carbohydrate intake with glucose management plans. Watch for concentrated added sugars and inadequate fiber.",
        "energy": "4 kcal/g",
    },
    "Protein": {
        "icon": "🥚",
        "functions": "Supports tissue repair, enzymes, hormones, immune function, fluid balance, and transport.",
        "sources": "Fish, poultry, eggs, dairy, soy, beans, lentils, nuts, and seeds.",
        "nursing": "Needs rise with healing, burns, some infections, pregnancy, and growth. Kidney or liver disease can change the plan.",
        "energy": "4 kcal/g",
    },
    "Fat": {
        "icon": "🥑",
        "functions": "Provides energy, insulation, cell membranes, essential fatty acids, and absorption of vitamins A, D, E, and K.",
        "sources": "Olive oil, avocado, nuts, seeds, fatty fish, dairy, and meats.",
        "nursing": "Favor unsaturated fats. Consider fat tolerance in pancreatic, gallbladder, or malabsorptive disorders.",
        "energy": "9 kcal/g",
    },
    "Water": {
        "icon": "💧",
        "functions": "Supports circulation, temperature regulation, digestion, waste removal, and chemical reactions.",
        "sources": "Water, milk, soups, fruits, vegetables, and other beverages.",
        "nursing": "Assess intake, output, edema, mucous membranes, weight trends, sodium, kidney function, and swallowing safety.",
        "energy": "0 kcal/g",
    },
    "Fiber": {
        "icon": "🥦",
        "functions": "Supports bowel regularity, satiety, glycemic control, and cardiovascular health.",
        "sources": "Vegetables, fruits, whole grains, legumes, nuts, and seeds.",
        "nursing": "Increase gradually with adequate fluid. Some acute GI conditions or procedures require temporary restriction.",
        "energy": "Not fully digested",
    },
}

MICROS = {
    "Vitamin A": ("Vision, epithelial integrity, and immunity", "Liver, eggs, dairy, orange and dark-green produce", "Night blindness; excess can cause toxicity"),
    "Vitamin D": ("Calcium absorption, bone health, and muscle function", "Fortified milk, fatty fish, egg yolk, sunlight exposure", "Deficiency increases bone risk; excess can cause hypercalcemia"),
    "Vitamin E": ("Antioxidant protection", "Nuts, seeds, vegetable oils", "Deficiency is uncommon; high supplemental doses can increase bleeding risk"),
    "Vitamin K": ("Blood clotting and bone proteins", "Leafy greens and intestinal synthesis", "Keep intake consistent with warfarin therapy"),
    "Vitamin C": ("Collagen formation, wound healing, antioxidant activity, and iron absorption", "Citrus, berries, peppers, tomatoes, broccoli", "Deficiency can impair healing and cause bleeding gums"),
    "Thiamine (B1)": ("Carbohydrate metabolism and neurologic function", "Whole/enriched grains, pork, legumes", "Risk rises with chronic alcohol use, prolonged vomiting, and severe malnutrition"),
    "Folate (B9)": ("DNA synthesis and red blood cell formation", "Leafy greens, legumes, fortified grains", "Deficiency causes megaloblastic anemia; adequate intake matters before and during pregnancy"),
    "Vitamin B12": ("Neurologic function and red blood cell formation", "Animal foods and fortified products", "Deficiency can cause macrocytic anemia and neurologic changes"),
    "Calcium": ("Bone, muscle contraction, nerve transmission, and clotting", "Dairy, fortified alternatives, tofu, greens", "Vitamin D supports absorption"),
    "Iron": ("Hemoglobin and oxygen transport", "Meat, beans, fortified grains, leafy greens", "Vitamin C improves nonheme iron absorption"),
    "Magnesium": ("Muscle, nerve, enzyme, and cardiac function", "Nuts, seeds, legumes, whole grains, greens", "Low levels can contribute to weakness and dysrhythmias"),
    "Potassium": ("Fluid balance, nerve transmission, muscle and cardiac function", "Potatoes, beans, bananas, oranges, dairy, vegetables", "Kidney disease and certain medications can cause dangerous high levels"),
    "Sodium": ("Fluid balance and nerve and muscle function", "Processed foods, restaurant foods, salt", "Excess intake can worsen fluid retention and hypertension"),
    "Zinc": ("Wound healing, immunity, taste, and growth", "Meat, shellfish, dairy, legumes, nuts", "Deficiency can impair healing and taste"),
    "Iodine": ("Thyroid hormone production", "Iodized salt, seafood, dairy", "Both low and excessive intake can affect thyroid function"),
}

SPECIAL_DIETS = {
    "Cardiac / Heart-Healthy": {
        "focus": "Vegetables, fruits, whole grains, legumes, fish, lean proteins, unsaturated fats, and lower sodium.",
        "limit": "Processed meats, high-sodium foods, trans fat, excess saturated fat, and added sugars.",
        "case": "A patient with coronary artery disease asks which lunch best supports cardiovascular health.",
        "best": "Grilled salmon, quinoa, roasted vegetables, and fruit",
        "options": ["Fried chicken sandwich and fries", "Grilled salmon, quinoa, roasted vegetables, and fruit", "Pepperoni pizza", "Processed deli meat wrap and chips"],
    },
    "DASH": {
        "focus": "Fruits, vegetables, low-fat dairy, whole grains, nuts, legumes, and lower sodium.",
        "limit": "High-sodium processed foods and excess saturated fat.",
        "case": "A patient with hypertension wants a DASH-style breakfast.",
        "best": "Oatmeal with berries, walnuts, and low-fat milk",
        "options": ["Sausage biscuit", "Oatmeal with berries, walnuts, and low-fat milk", "Sugary pastry and energy drink", "Bacon, hash browns, and salted eggs"],
    },
    "Diabetes / Consistent Carbohydrate": {
        "focus": "Consistent carbohydrate distribution, high-fiber choices, portion awareness, and pairing carbohydrate with protein or healthy fat.",
        "limit": "Sugar-sweetened beverages and large portions of refined carbohydrate.",
        "case": "A patient with diabetes needs a balanced snack.",
        "best": "Apple slices with peanut butter",
        "options": ["Regular soda", "Apple slices with peanut butter", "Large candy bar", "Sweetened coffee drink"],
    },
    "Renal": {
        "focus": "Individualize sodium, potassium, phosphorus, protein, and fluid according to kidney function, dialysis status, and laboratory results.",
        "limit": "Do not apply one universal renal diet to every patient.",
        "case": "Which action is safest before teaching a patient with chronic kidney disease?",
        "best": "Review current kidney function, potassium, phosphorus, fluid status, and treatment plan",
        "options": ["Automatically ban all fruits", "Recommend high-protein supplements to everyone", "Review current kidney function, potassium, phosphorus, fluid status, and treatment plan", "Encourage salt substitutes without checking potassium"],
    },
    "Liver Disease": {
        "focus": "Adequate energy and protein are often important. Sodium restriction can help ascites. Plans vary with encephalopathy and disease severity.",
        "limit": "Alcohol and unnecessary severe protein restriction.",
        "case": "A patient with cirrhosis and ascites needs teaching.",
        "best": "Choose lower-sodium foods and follow the individualized protein and fluid plan",
        "options": ["Avoid all protein indefinitely", "Choose lower-sodium foods and follow the individualized protein and fluid plan", "Use salt substitutes freely", "Skip meals to reduce abdominal fullness"],
    },
    "Gluten-Free": {
        "focus": "Avoid wheat, barley, and rye. Use certified gluten-free products when cross-contact matters.",
        "limit": "Hidden gluten and cross-contact.",
        "case": "Which grain is naturally gluten-free?",
        "best": "Quinoa",
        "options": ["Barley", "Rye", "Quinoa", "Wheat berries"],
    },
    "Low-FODMAP": {
        "focus": "A structured short-term elimination followed by systematic reintroduction, ideally with dietitian guidance.",
        "limit": "Long-term unnecessary restriction.",
        "case": "What is the purpose of the reintroduction phase?",
        "best": "Identify individual triggers and expand the diet",
        "options": ["Maintain permanent maximal restriction", "Identify individual triggers and expand the diet", "Diagnose inflammatory bowel disease", "Eliminate all carbohydrates"],
    },
    "Bariatric": {
        "focus": "Small portions, protein first, slow eating, lifelong vitamin and mineral supplementation, and avoiding fluids with meals as directed.",
        "limit": "Large meals, concentrated sweets when dumping is a concern, and nonadherence to supplements.",
        "case": "Which behavior best supports recovery after bariatric surgery?",
        "best": "Eat small meals slowly and prioritize prescribed protein and supplements",
        "options": ["Drink large amounts with meals", "Eat small meals slowly and prioritize prescribed protein and supplements", "Stop vitamins once weight stabilizes", "Choose concentrated sweets for calories"],
    },
    "Dysphagia / Texture-Modified": {
        "focus": "Use the prescribed food texture and liquid thickness. Position upright and follow speech-language pathology recommendations.",
        "limit": "Unapproved mixed textures and thin liquids when contraindicated.",
        "case": "What is the nurse's priority before offering food?",
        "best": "Verify the prescribed texture, liquid consistency, positioning, and swallowing plan",
        "options": ["Offer water to test swallowing", "Verify the prescribed texture, liquid consistency, positioning, and swallowing plan", "Place the patient flat", "Add a straw automatically"],
    },
    "Enteral Nutrition": {
        "focus": "Use the GI tract when functional. Verify tube placement according to policy, maintain head elevation, monitor tolerance, and flush as ordered.",
        "limit": "Unsafe medication mixing and interrupting feeds without a plan.",
        "case": "Which action reduces aspiration risk during gastric tube feeding?",
        "best": "Maintain appropriate head-of-bed elevation and assess tolerance",
        "options": ["Position supine", "Maintain appropriate head-of-bed elevation and assess tolerance", "Add medications directly to the formula bag", "Use food coloring to test placement"],
    },
    "Parenteral Nutrition": {
        "focus": "Central or peripheral IV nutrition when the GI tract cannot be used adequately. Monitor glucose, electrolytes, infection risk, and line care.",
        "limit": "Abrupt changes without orders and breaks in aseptic technique.",
        "case": "Which complication requires close monitoring with parenteral nutrition?",
        "best": "Bloodstream infection and hyperglycemia",
        "options": ["Only constipation", "Bloodstream infection and hyperglycemia", "Gluten exposure", "Lactose intolerance"],
    },
}

QUESTIONS = [
    # Macronutrients
    {"topic":"Macronutrients","q":"A nurse is teaching a client about energy provided by nutrients. Which nutrient provides 9 kcal per gram?","options":["Carbohydrate","Protein","Fat","Water"],"answer":"Fat","rationale":"Fat provides 9 kcal/g. Carbohydrate and protein provide 4 kcal/g."},
    {"topic":"Macronutrients","q":"Which meal provides the best combination of complex carbohydrate and fiber?","options":["White toast and jelly","Oatmeal with berries","Candy and juice","Crackers and soda"],"answer":"Oatmeal with berries","rationale":"Whole oats and berries provide complex carbohydrate and dietary fiber."},
    {"topic":"Macronutrients","q":"Which patient has the greatest expected increase in protein needs?","options":["Stable adult with no illness","Patient with a large pressure injury","Adult with seasonal allergies","Patient receiving routine eye drops"],"answer":"Patient with a large pressure injury","rationale":"Protein supports tissue repair and needs often rise with significant wounds."},
    {"topic":"Macronutrients","q":"A client suddenly increases fiber intake and develops bloating. Which teaching is best?","options":["Stop all fiber permanently","Increase fiber gradually and drink adequate fluid","Use only fiber supplements","Restrict all fruits"],"answer":"Increase fiber gradually and drink adequate fluid","rationale":"Gradual increases with adequate fluid reduce GI discomfort and constipation risk."},
    {"topic":"Macronutrients","q":"Which assessment best reflects short-term fluid balance changes?","options":["Daily weight","Height","Hair color","Waist-to-hip ratio"],"answer":"Daily weight","rationale":"Daily weight under consistent conditions is sensitive to fluid gain or loss."},
    {"topic":"Macronutrients","q":"Which food is a source of unsaturated fat?","options":["Avocado","Stick butter","Shortening","Fatty processed meat"],"answer":"Avocado","rationale":"Avocado is rich in unsaturated fat."},
    {"topic":"Macronutrients","q":"Which nutrient is the primary fuel source for the brain under usual conditions?","options":["Carbohydrate","Vitamin C","Calcium","Water"],"answer":"Carbohydrate","rationale":"Glucose derived from carbohydrate is the brain's usual primary fuel."},
    {"topic":"Macronutrients","q":"Which protein source is plant-based?","options":["Lentils","Chicken","Eggs","Tuna"],"answer":"Lentils","rationale":"Lentils are legumes and provide plant protein and fiber."},
    # Micronutrients
    {"topic":"Micronutrients","q":"Which vitamin improves absorption of nonheme iron?","options":["Vitamin C","Vitamin K","Vitamin D","Vitamin B12"],"answer":"Vitamin C","rationale":"Vitamin C enhances absorption of iron from plant and fortified sources."},
    {"topic":"Micronutrients","q":"A client taking warfarin asks about leafy greens. Which response is best?","options":["Avoid all greens forever","Keep vitamin K intake consistent and follow monitoring instructions","Double greens on weekends","Take vitamin K supplements daily without guidance"],"answer":"Keep vitamin K intake consistent and follow monitoring instructions","rationale":"Consistency supports stable anticoagulation. Abrupt intake changes can alter warfarin effect."},
    {"topic":"Micronutrients","q":"Which finding is most concerning for vitamin B12 deficiency?","options":["Paresthesias and macrocytic anemia","Night blindness only","Bleeding gums only","Hyperactive reflexes after exercise"],"answer":"Paresthesias and macrocytic anemia","rationale":"B12 deficiency can produce neurologic changes and macrocytic anemia."},
    {"topic":"Micronutrients","q":"Which mineral is essential for thyroid hormone production?","options":["Iodine","Zinc","Iron","Calcium"],"answer":"Iodine","rationale":"The thyroid uses iodine to synthesize thyroid hormones."},
    {"topic":"Micronutrients","q":"A patient with chronic alcohol misuse and confusion is at risk for deficiency of which vitamin?","options":["Thiamine","Vitamin K","Vitamin A","Vitamin E"],"answer":"Thiamine","rationale":"Chronic alcohol misuse increases risk for thiamine deficiency and serious neurologic complications."},
    {"topic":"Micronutrients","q":"Which nutrient deficiency can cause impaired wound healing and reduced taste?","options":["Zinc","Sodium","Fluoride","Vitamin K"],"answer":"Zinc","rationale":"Zinc supports wound healing, immune function, and taste."},
    {"topic":"Micronutrients","q":"Which patient requires the most caution with potassium-rich foods or salt substitutes?","options":["Patient with advanced kidney disease","Healthy adolescent athlete","Adult with corrected vision","Patient with seasonal rhinitis"],"answer":"Patient with advanced kidney disease","rationale":"Reduced kidney excretion can cause dangerous hyperkalemia."},
    {"topic":"Micronutrients","q":"Which vitamin supports calcium absorption?","options":["Vitamin D","Vitamin C","Thiamine","Folate"],"answer":"Vitamin D","rationale":"Vitamin D promotes intestinal calcium absorption."},
    {"topic":"Micronutrients","q":"Which manifestation is associated with vitamin A deficiency?","options":["Night blindness","Scurvy","Pellagra","Goiter"],"answer":"Night blindness","rationale":"Vitamin A is required for normal visual function, especially in low light."},
    {"topic":"Micronutrients","q":"Which nutrient is especially important before and during early pregnancy to reduce neural tube defect risk?","options":["Folate","Sodium","Vitamin E","Phosphorus"],"answer":"Folate","rationale":"Adequate folate before conception and in early pregnancy supports neural tube development."},
    # Special diets
    {"topic":"Special Diets","q":"Which meal best fits a heart-healthy eating pattern?","options":["Grilled fish, brown rice, vegetables","Fried chicken, fries, soda","Processed meat pizza","Bacon cheeseburger"],"answer":"Grilled fish, brown rice, vegetables","rationale":"This option emphasizes lean protein, whole grain, and vegetables."},
    {"topic":"Special Diets","q":"Which breakfast best fits the DASH pattern?","options":["Oatmeal, berries, walnuts, low-fat milk","Sausage biscuit","Donut and sweetened coffee","Bacon and salted hash browns"],"answer":"Oatmeal, berries, walnuts, low-fat milk","rationale":"DASH emphasizes fruits, whole grains, nuts, and low-fat dairy."},
    {"topic":"Special Diets","q":"Which food must a client with celiac disease avoid?","options":["Barley","Rice","Corn","Quinoa"],"answer":"Barley","rationale":"Gluten is found in wheat, barley, and rye."},
    {"topic":"Special Diets","q":"What is the safest approach to a renal diet?","options":["Individualize it using labs, kidney function, and treatment status","Ban all protein","Ban all produce","Use potassium salt substitutes freely"],"answer":"Individualize it using labs, kidney function, and treatment status","rationale":"Renal restrictions differ by disease stage, dialysis status, labs, and symptoms."},
    {"topic":"Special Diets","q":"Which instruction is appropriate for prescribed dysphagia precautions?","options":["Use the ordered texture and liquid consistency","Give thin water routinely","Feed while supine","Use a straw for every patient"],"answer":"Use the ordered texture and liquid consistency","rationale":"The swallowing plan should follow the individualized speech-language pathology recommendations."},
    {"topic":"Special Diets","q":"Which action is appropriate during enteral feeding?","options":["Maintain prescribed head elevation","Mix all medications into the formula","Confirm placement by injecting air and listening","Keep the patient flat"],"answer":"Maintain prescribed head elevation","rationale":"Appropriate head elevation helps reduce aspiration risk."},
    {"topic":"Special Diets","q":"Which complication is a priority with central parenteral nutrition?","options":["Bloodstream infection","Gluten exposure","Dental caries only","Motion sickness"],"answer":"Bloodstream infection","rationale":"Central venous access increases bloodstream infection risk."},
    {"topic":"Special Diets","q":"Which snack best supports consistent-carbohydrate teaching?","options":["Apple with peanut butter","Regular soda","Large candy bar","Sweetened frozen drink"],"answer":"Apple with peanut butter","rationale":"The snack combines carbohydrate and fiber with protein and fat."},
    {"topic":"Special Diets","q":"Which statement about low-FODMAP eating is correct?","options":["Reintroduction identifies individual triggers","It should remain maximally restrictive forever","It diagnoses celiac disease","It eliminates all carbohydrate"],"answer":"Reintroduction identifies individual triggers","rationale":"Low-FODMAP plans use short-term restriction followed by structured reintroduction."},
    {"topic":"Special Diets","q":"Which instruction is most appropriate after bariatric surgery?","options":["Prioritize protein and prescribed supplements","Stop supplements when weight stabilizes","Drink large volumes with meals","Choose concentrated sweets"],"answer":"Prioritize protein and prescribed supplements","rationale":"Protein and lifelong prescribed micronutrient supplementation help prevent malnutrition."},
    # Clinical/nutrition support
    {"topic":"Clinical Nutrition","q":"Which finding most strongly suggests aspiration risk during a meal?","options":["Wet voice and coughing","Request for seasoning","Preference for cold food","Eating slowly"],"answer":"Wet voice and coughing","rationale":"Coughing and a wet or gurgly voice can signal impaired airway protection."},
    {"topic":"Clinical Nutrition","q":"Which action is best when a hospitalized patient eats less than 25% of meals for several days?","options":["Assess barriers and request nutrition evaluation","Document only","Remove snacks","Wait until discharge"],"answer":"Assess barriers and request nutrition evaluation","rationale":"Persistent poor intake needs prompt assessment and interdisciplinary intervention."},
    {"topic":"Clinical Nutrition","q":"Which anthropometric measure is most useful for monitoring acute nutrition and fluid trends?","options":["Serial weight","Adult height","Shoe size","Arm span once"],"answer":"Serial weight","rationale":"Weight trends help identify changes, though fluid status must be considered."},
    {"topic":"Clinical Nutrition","q":"Which patient is at greatest risk for refeeding complications?","options":["Severely malnourished patient beginning nutrition support","Healthy adult eating breakfast","Patient on a stable regular diet","Adult taking a multivitamin"],"answer":"Severely malnourished patient beginning nutrition support","rationale":"Rapid nutrition after severe deprivation can cause dangerous electrolyte shifts."},
    {"topic":"Clinical Nutrition","q":"Which electrolyte deserves close monitoring when refeeding risk is high?","options":["Phosphorus","Chloride only","Bicarbonate only","Calcium only"],"answer":"Phosphorus","rationale":"Hypophosphatemia is a hallmark concern in refeeding syndrome."},
    {"topic":"Clinical Nutrition","q":"Which intervention best supports a patient with poor appetite?","options":["Offer small nutrient-dense meals and address symptoms","Force large meals","Restrict preferred foods without reason","Skip oral care"],"answer":"Offer small nutrient-dense meals and address symptoms","rationale":"Small frequent nutrient-dense intake and symptom management can improve intake."},
    {"topic":"Clinical Nutrition","q":"A patient receiving tube feeding develops diarrhea. What should the nurse do first?","options":["Assess medications, rate, formula handling, infection, and other causes","Stop all nutrition permanently","Add antidiarrheals without assessment","Dilute formula with tap water"],"answer":"Assess medications, rate, formula handling, infection, and other causes","rationale":"Diarrhea has multiple causes and requires assessment before changing the feeding plan."},
    {"topic":"Clinical Nutrition","q":"Which nursing action best reduces medication-tube interactions?","options":["Follow medication-specific guidance and flush as ordered","Crush every medication together","Mix medications into the formula bag","Skip flushing"],"answer":"Follow medication-specific guidance and flush as ordered","rationale":"Medication administration through feeding tubes requires drug-specific review and appropriate flushing."},
    # Maternal/peds/older adult
    {"topic":"Lifespan Nutrition","q":"Which teaching is most important for a pregnant client?","options":["Follow prenatal folate and iron recommendations","Avoid all fish","Double calorie intake immediately","Use herbal supplements freely"],"answer":"Follow prenatal folate and iron recommendations","rationale":"Folate and iron needs rise in pregnancy and should follow prenatal guidance."},
    {"topic":"Lifespan Nutrition","q":"Which food is unsafe for an infant younger than 12 months?","options":["Honey","Iron-fortified cereal","Pureed vegetables","Breast milk or formula"],"answer":"Honey","rationale":"Honey can contain spores associated with infant botulism."},
    {"topic":"Lifespan Nutrition","q":"Which approach supports healthy toddler eating?","options":["Offer structured meals and repeated exposure without pressure","Force a clean plate","Use sweets as the main reward","Allow continuous juice sipping"],"answer":"Offer structured meals and repeated exposure without pressure","rationale":"Repeated neutral exposure and structured meals support healthy food acceptance."},
    {"topic":"Lifespan Nutrition","q":"Which factor commonly raises dehydration risk in older adults?","options":["Reduced thirst sensation","Increased total body water","Improved kidney concentration","Greater muscle mass"],"answer":"Reduced thirst sensation","rationale":"Older adults may have reduced thirst and impaired renal concentrating ability."},
    {"topic":"Lifespan Nutrition","q":"Which intervention supports an older adult with limited dexterity?","options":["Adaptive utensils and easy-open containers","Remove all finger foods","Serve only liquids","Limit meal time to five minutes"],"answer":"Adaptive utensils and easy-open containers","rationale":"Adaptive equipment can increase independence and intake."},
    # Food safety
    {"topic":"Food Safety","q":"Which action best prevents cross-contamination?","options":["Use separate cutting boards for raw meat and ready-to-eat foods","Rinse raw poultry in the sink","Use one knife without washing","Place cooked meat on the raw-meat plate"],"answer":"Use separate cutting boards for raw meat and ready-to-eat foods","rationale":"Separation reduces transfer of pathogens from raw animal foods."},
    {"topic":"Food Safety","q":"Which client should avoid unpasteurized milk and soft cheese made from unpasteurized milk?","options":["Pregnant client","Healthy adult runner only","Client with corrected myopia","Adult with seasonal allergies"],"answer":"Pregnant client","rationale":"Pregnancy increases risk from foodborne pathogens such as Listeria."},
    {"topic":"Food Safety","q":"What is the safest action with perishable food left at room temperature for an uncertain prolonged period?","options":["Discard it","Taste it first","Refrigerate and serve later","Reheat briefly"],"answer":"Discard it","rationale":"When time and temperature safety are uncertain, discarding is safest."},
    {"topic":"Food Safety","q":"Which hand hygiene moment is essential during food preparation?","options":["After handling raw meat and before touching ready-to-eat food","Only after the meal","Only when hands look dirty","After putting on jewelry"],"answer":"After handling raw meat and before touching ready-to-eat food","rationale":"Handwashing interrupts cross-contamination."},
    # Assessment and teaching
    {"topic":"Assessment","q":"Which question best assesses food access?","options":["Have you worried that food would run out before you had money to buy more?","Do you like vegetables?","What is your favorite restaurant?","Do you own a blender?"],"answer":"Have you worried that food would run out before you had money to buy more?","rationale":"This question screens for household food insecurity."},
    {"topic":"Assessment","q":"Which finding requires the fastest follow-up?","options":["Unintentional 10% weight loss with poor intake","Stable weight and appetite","Preference for vegetarian meals","Occasional restaurant meal"],"answer":"Unintentional 10% weight loss with poor intake","rationale":"Significant unintentional weight loss and poor intake raise malnutrition risk."},
    {"topic":"Assessment","q":"Which response uses teach-back correctly?","options":["Show me how you will choose your meals at home","Do you understand?","Read this later","Sign here to confirm understanding"],"answer":"Show me how you will choose your meals at home","rationale":"Teach-back asks the patient to explain or demonstrate the plan in their own words."},
    {"topic":"Assessment","q":"Which teaching plan is most culturally responsive?","options":["Ask about preferred foods and adapt recommendations","Replace all traditional foods","Assume everyone eats the same foods","Provide a generic list without discussion"],"answer":"Ask about preferred foods and adapt recommendations","rationale":"Effective teaching respects preferences, access, beliefs, and usual eating patterns."},
    {"topic":"Assessment","q":"Which referral is most appropriate for a patient needing individualized medical nutrition therapy?","options":["Registered dietitian nutritionist","Hospital transporter","Billing specialist","Radiology scheduler"],"answer":"Registered dietitian nutritionist","rationale":"An RDN provides individualized medical nutrition therapy and works with the clinical team."},
]

# Verify count
assert len(QUESTIONS) == 50, f"Question bank has {len(QUESTIONS)} questions, expected 50."

PHOTO_URLS = {
    "produce": "https://images.unsplash.com/photo-1610348725531-843dff563e2c?auto=format&fit=crop&w=1200&q=80",
    "grains": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?auto=format&fit=crop&w=1200&q=80",
    "meal": "https://images.unsplash.com/photo-1543353071-873f17a7a088?auto=format&fit=crop&w=1200&q=80",
}

def plate_svg():
    return f"""
    <svg viewBox="0 0 600 360" width="100%" role="img" aria-label="Balanced plate diagram">
      <rect width="600" height="360" rx="24" fill="#ffffff"/>
      <circle cx="230" cy="180" r="135" fill="#fafafa" stroke="{FSC_DARK}" stroke-width="8"/>
      <path d="M230 45 A135 135 0 0 0 95 180 L230 180 Z" fill="#dfead8" stroke="white" stroke-width="4"/>
      <path d="M95 180 A135 135 0 0 0 230 315 L230 180 Z" fill="#f2d6c5" stroke="white" stroke-width="4"/>
      <path d="M230 45 A135 135 0 0 1 365 180 L230 180 Z" fill="#f2e4b7" stroke="white" stroke-width="4"/>
      <path d="M365 180 A135 135 0 0 1 230 315 L230 180 Z" fill="#d8e4ef" stroke="white" stroke-width="4"/>
      <text x="145" y="125" font-size="23" fill="#243124">Vegetables</text>
      <text x="145" y="240" font-size="23" fill="#4d2d22">Fruit</text>
      <text x="270" y="125" font-size="23" fill="#554915">Grains</text>
      <text x="265" y="240" font-size="23" fill="#243b52">Protein</text>
      <circle cx="455" cy="115" r="62" fill="#eef3f8" stroke="{FSC_DARK}" stroke-width="6"/>
      <text x="420" y="122" font-size="22" fill="#243b52">Dairy</text>
      <rect x="400" y="220" width="110" height="65" rx="15" fill="#e3f0fa" stroke="{FSC_DARK}" stroke-width="5"/>
      <text x="420" y="260" font-size="22" fill="#243b52">Water</text>
    </svg>
    """

def show_macro_chart():
    labels = ["Carbohydrate", "Protein", "Fat"]
    values = [4, 4, 9]
    fig, ax = plt.subplots()
    ax.bar(labels, values)
    ax.set_ylabel("Kilocalories per gram")
    ax.set_title("Energy Density of Macronutrients")
    ax.set_ylim(0, 10)
    for i, value in enumerate(values):
        ax.text(i, value + 0.2, str(value), ha="center")
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)

def immediate_question(question, key_prefix):
    st.write(question["q"])
    choice = st.radio(
        "Select one answer:",
        question["options"],
        key=f"{key_prefix}_choice",
        index=None,
    )
    if st.button("Check answer", key=f"{key_prefix}_check"):
        if choice is None:
            st.warning("Select an answer first.")
        elif choice == question["answer"]:
            st.success("Correct.")
            st.info(question["rationale"])
        else:
            st.error(f"Incorrect. Correct answer: {question['answer']}")
            st.info(question["rationale"])

def reset_full_quiz():
    for key in list(st.session_state.keys()):
        if key.startswith("fullquiz_"):
            del st.session_state[key]

# ----------------------------
# Sidebar navigation
# ----------------------------

st.sidebar.markdown("## NUR3302")
st.sidebar.caption("Nutrition Student Hub")
page = st.sidebar.radio(
    "Navigate",
    [
        "Home",
        "Macronutrients",
        "Micronutrients",
        "Special Diets",
        "Interactive Lab",
        "Clinical Cases",
        "NCLEX Review",
        "Calculators",
        "Study Resources",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption("Anonymous learning tool. Responses remain in the current browser session and are not saved.")

# ----------------------------
# Pages
# ----------------------------

if page == "Home":
    st.markdown(
        """
        <div class="hero">
          <h1>NUR3302 Nutrition Student Hub</h1>
          <p><strong>Florida Southern College</strong></p>
          <p>Build nutrition knowledge, connect nutrients to patient care, and practice nursing decisions.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown('<div class="topic-card"><h3>Learn</h3><p>Review macronutrients, micronutrients, special diets, and nutrition support.</p></div>', unsafe_allow_html=True)
    with c2:
        st.markdown('<div class="topic-card"><h3>Practice</h3><p>Use matching, sorting, meal-building, calculations, and clinical cases.</p></div>', unsafe_allow_html=True)
    with c3:
        st.markdown('<div class="topic-card"><h3>Prepare</h3><p>Complete topic quizzes or a 50-question mixed NCLEX-style review.</p></div>', unsafe_allow_html=True)

    st.subheader("Build a balanced plate")
    st.markdown(plate_svg(), unsafe_allow_html=True)
    st.caption("Use this visual as a general meal-planning framework. Individual clinical diets may differ.")

    st.subheader("Food gallery")
    p1, p2, p3 = st.columns(3)
    p1.image(PHOTO_URLS["produce"], caption="Colorful produce", use_container_width=True)
    p2.image(PHOTO_URLS["grains"], caption="Whole grains", use_container_width=True)
    p3.image(PHOTO_URLS["meal"], caption="Balanced meal preparation", use_container_width=True)

    st.markdown(
        '<div class="warning"><strong>Educational use only:</strong> This app supports course learning. It does not replace clinical judgment, current evidence, facility policy, provider orders, or individualized consultation with a registered dietitian nutritionist.</div>',
        unsafe_allow_html=True,
    )

elif page == "Macronutrients":
    st.header("Macronutrients")
    tabs = st.tabs(list(MACROS.keys()))
    for tab, (name, item) in zip(tabs, MACROS.items()):
        with tab:
            left, right = st.columns([2, 1])
            with left:
                st.subheader(f"{item['icon']} {name}")
                st.markdown(f"**Main functions:** {item['functions']}")
                st.markdown(f"**Food sources:** {item['sources']}")
                st.markdown(f"**Nursing connection:** {item['nursing']}")
                st.markdown(f'<div class="pearl"><strong>Energy:</strong> {item["energy"]}</div>', unsafe_allow_html=True)
            with right:
                if name in ["Carbohydrates", "Protein", "Fat"]:
                    show_macro_chart()
                else:
                    st.markdown(plate_svg(), unsafe_allow_html=True)

    st.subheader("Quick knowledge check")
    macro_q = [q for q in QUESTIONS if q["topic"] == "Macronutrients"]
    selected = st.selectbox("Choose a question", range(len(macro_q)), format_func=lambda i: f"Question {i+1}")
    immediate_question(macro_q[selected], f"macro_{selected}")

elif page == "Micronutrients":
    st.header("Micronutrients")
    st.write("Select a nutrient to review its function, sources, and nursing priority.")

    nutrient = st.selectbox("Nutrient", list(MICROS.keys()))
    function, sources, nursing = MICROS[nutrient]
    c1, c2, c3 = st.columns(3)
    c1.markdown(f'<div class="topic-card"><h3>Function</h3><p>{function}</p></div>', unsafe_allow_html=True)
    c2.markdown(f'<div class="topic-card"><h3>Sources</h3><p>{sources}</p></div>', unsafe_allow_html=True)
    c3.markdown(f'<div class="topic-card"><h3>Nursing priority</h3><p>{nursing}</p></div>', unsafe_allow_html=True)

    st.subheader("Flashcard mode")
    flash_name = st.selectbox("Choose a flashcard", list(MICROS.keys()), key="flash_name")
    if st.button("Reveal answer"):
        f, s, n = MICROS[flash_name]
        st.success(f"{flash_name}: {f}")
        st.write(f"Sources: {s}")
        st.write(f"Nursing priority: {n}")

    st.subheader("Micronutrient matching")
    match_items = {
        "Vitamin C": "Improves nonheme iron absorption",
        "Vitamin K": "Supports clotting proteins",
        "Vitamin D": "Supports calcium absorption",
        "Thiamine (B1)": "High-priority deficiency risk with chronic alcohol misuse",
        "Vitamin B12": "Deficiency can cause neurologic changes",
    }
    answers = []
    options = list(match_items.values())
    for nutrient_name, correct in match_items.items():
        answers.append(
            st.selectbox(
                nutrient_name,
                ["Choose..."] + options,
                key=f"match_{nutrient_name}",
            ) == correct
        )
    if st.button("Check matching activity"):
        score = sum(answers)
        st.write(f"Score: {score}/{len(match_items)}")
        if score == len(match_items):
            st.success("All matches are correct.")
        else:
            st.info("Review the micronutrient cards and try again.")

elif page == "Special Diets":
    st.header("Special Diets")
    selected_diet = st.selectbox("Choose a diet or nutrition-support plan", list(SPECIAL_DIETS.keys()))
    diet = SPECIAL_DIETS[selected_diet]

    a, b = st.columns(2)
    a.markdown(f'<div class="topic-card"><h3>Primary focus</h3><p>{diet["focus"]}</p></div>', unsafe_allow_html=True)
    b.markdown(f'<div class="topic-card"><h3>Important caution</h3><p>{diet["limit"]}</p></div>', unsafe_allow_html=True)

    st.subheader("Clinical decision")
    st.write(diet["case"])
    answer = st.radio("Choose the best response:", diet["options"], key=f"diet_{selected_diet}", index=None)
    if st.button("Check clinical decision"):
        if answer == diet["best"]:
            st.success("Correct.")
        elif answer is None:
            st.warning("Select an answer first.")
        else:
            st.error(f"Best answer: {diet['best']}")
        st.info(f"Key point: {diet['focus']}")

elif page == "Interactive Lab":
    st.header("Interactive Nutrition Lab")

    lab_tab1, lab_tab2, lab_tab3 = st.tabs(["Meal Builder", "Sort the Foods", "Label Detective"])

    with lab_tab1:
        st.subheader("Build a balanced meal")
        st.write("Select one item from each group. Then evaluate the meal.")
        vegetable = st.selectbox("Vegetable", ["None", "Broccoli", "Spinach salad", "Roasted peppers"])
        fruit = st.selectbox("Fruit", ["None", "Berries", "Orange", "Apple"])
        grain = st.selectbox("Grain or starch", ["None", "Brown rice", "Quinoa", "Whole-grain bread"])
        protein = st.selectbox("Protein", ["None", "Salmon", "Chicken", "Tofu", "Lentils"])
        beverage = st.selectbox("Beverage", ["Water", "Unsweetened milk", "Regular soda", "Sweet tea"])
        if st.button("Evaluate meal"):
            selected_groups = sum(x != "None" for x in [vegetable, fruit, grain, protein])
            if selected_groups >= 4 and beverage in ["Water", "Unsweetened milk"]:
                st.success("This meal includes all four food groups and a lower-added-sugar beverage.")
            elif selected_groups >= 3:
                st.info("Good start. Add any missing food group and consider a lower-added-sugar beverage.")
            else:
                st.warning("Add more food groups to improve balance.")

    with lab_tab2:
        st.subheader("Sort by predominant nutrient")
        foods = {
            "Olive oil": "Fat",
            "Lentils": "Protein",
            "Brown rice": "Carbohydrate",
            "Berries": "Carbohydrate",
            "Almonds": "Fat",
        }
        correct = 0
        for food, category in foods.items():
            selection = st.selectbox(food, ["Choose...", "Carbohydrate", "Protein", "Fat"], key=f"sort_{food}")
            if selection == category:
                correct += 1
        if st.button("Check sorting"):
            st.write(f"Score: {correct}/{len(foods)}")
            st.caption("Many foods contain more than one macronutrient. This activity asks for the predominant category used in basic meal planning.")

    with lab_tab3:
        st.subheader("Nutrition label detective")
        st.write("A packaged soup contains 780 mg sodium per serving and 2 servings per container.")
        servings = st.number_input("Servings eaten", min_value=0.0, max_value=4.0, value=1.0, step=0.5)
        sodium = 780 * servings
        st.metric("Total sodium consumed", f"{sodium:,.0f} mg")
        if servings > 1:
            st.info("Always multiply nutrients by the number of servings consumed.")

elif page == "Clinical Cases":
    st.header("Clinical Cases")

    cases = [
        {
            "title": "Pressure Injury and Poor Intake",
            "stem": "An older adult has a stage 3 pressure injury and eats about 25% of meals.",
            "question": "Which action is the priority?",
            "options": ["Request nutrition assessment and evaluate barriers to intake", "Restrict protein", "Wait one week", "Offer only clear liquids"],
            "answer": "Request nutrition assessment and evaluate barriers to intake",
            "feedback": "The patient has wound-healing demands and inadequate intake. Prompt interdisciplinary assessment is appropriate.",
        },
        {
            "title": "Heart Failure and Sodium",
            "stem": "A patient with heart failure reports eating canned soup and deli meat most days.",
            "question": "Which teaching is most relevant?",
            "options": ["Compare sodium labels and choose lower-sodium alternatives", "Avoid all carbohydrate", "Increase processed meat", "Use unlimited salt substitutes"],
            "answer": "Compare sodium labels and choose lower-sodium alternatives",
            "feedback": "Processed foods are major sodium sources. Salt substitutes require caution when potassium is a concern.",
        },
        {
            "title": "Dysphagia Safety",
            "stem": "A patient coughs during meals and has a wet voice after drinking water.",
            "question": "What should the nurse do first?",
            "options": ["Stop oral intake and follow swallowing-safety procedures", "Offer a straw", "Place the patient flat", "Encourage rapid drinking"],
            "answer": "Stop oral intake and follow swallowing-safety procedures",
            "feedback": "Coughing and a wet voice suggest aspiration risk and require immediate swallowing-safety action.",
        },
        {
            "title": "Refeeding Risk",
            "stem": "A severely malnourished patient begins aggressive nutrition support.",
            "question": "Which laboratory value is a priority?",
            "options": ["Phosphorus", "Hemoglobin A1c only", "LDL only", "Bilirubin only"],
            "answer": "Phosphorus",
            "feedback": "Rapid feeding can cause profound intracellular shifts, especially hypophosphatemia.",
        },
    ]

    case_index = st.selectbox("Choose a case", range(len(cases)), format_func=lambda i: cases[i]["title"])
    case = cases[case_index]
    st.markdown(f"### {case['title']}")
    st.write(case["stem"])
    response = st.radio(case["question"], case["options"], key=f"case_{case_index}", index=None)
    rationale = st.text_area("Explain your reasoning before checking the answer.", key=f"case_reason_{case_index}")
    if st.button("Review case"):
        if response == case["answer"]:
            st.success("Correct.")
        elif response is None:
            st.warning("Select an answer.")
        else:
            st.error(f"Best answer: {case['answer']}")
        st.info(case["feedback"])
        if rationale.strip():
            st.caption("Your reasoning remains in this browser session only.")

elif page == "NCLEX Review":
    st.header("NCLEX-Style Review")
    mode = st.radio("Choose a mode", ["Topic practice with immediate feedback", "50-question mixed exam"])

    if mode == "Topic practice with immediate feedback":
        topics = sorted(set(q["topic"] for q in QUESTIONS))
        topic = st.selectbox("Topic", topics)
        pool = [q for q in QUESTIONS if q["topic"] == topic]
        number = st.selectbox("Question", range(len(pool)), format_func=lambda i: f"{i+1} of {len(pool)}")
        immediate_question(pool[number], f"topic_{topic}_{number}")

    else:
        st.info("Answers remain only in the current browser session. The app does not save names or scores.")
        if "fullquiz_order" not in st.session_state:
            st.session_state.fullquiz_order = list(range(len(QUESTIONS)))
            random.shuffle(st.session_state.fullquiz_order)

        for display_num, q_index in enumerate(st.session_state.fullquiz_order, start=1):
            q = QUESTIONS[q_index]
            st.markdown(f"**{display_num}. {q['q']}**")
            st.radio(
                "Answer",
                q["options"],
                key=f"fullquiz_answer_{q_index}",
                index=None,
                label_visibility="collapsed",
            )
            st.markdown("---")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Submit 50-question exam"):
                score = 0
                unanswered = 0
                for q_index in st.session_state.fullquiz_order:
                    selected_answer = st.session_state.get(f"fullquiz_answer_{q_index}")
                    if selected_answer is None:
                        unanswered += 1
                    elif selected_answer == QUESTIONS[q_index]["answer"]:
                        score += 1
                percent = score / len(QUESTIONS) * 100
                st.session_state.fullquiz_result = (score, percent, unanswered)
        with c2:
            if st.button("Reset and reshuffle exam"):
                reset_full_quiz()
                st.rerun()

        if "fullquiz_result" in st.session_state:
            score, percent, unanswered = st.session_state.fullquiz_result
            st.subheader(f"Score: {score}/50 ({percent:.0f}%)")
            if unanswered:
                st.warning(f"Unanswered questions: {unanswered}")
            with st.expander("Review answers and rationales"):
                for display_num, q_index in enumerate(st.session_state.fullquiz_order, start=1):
                    q = QUESTIONS[q_index]
                    selected_answer = st.session_state.get(f"fullquiz_answer_{q_index}")
                    status = "Correct" if selected_answer == q["answer"] else "Review"
                    st.markdown(f"**{display_num}. {status}**")
                    st.write(f"Your answer: {selected_answer or 'No answer'}")
                    st.write(f"Correct answer: {q['answer']}")
                    st.caption(q["rationale"])

elif page == "Calculators":
    st.header("Nutrition Calculators")
    calc1, calc2, calc3, calc4 = st.tabs(["BMI", "Energy from Macros", "Protein Estimate", "Fluid Estimate"])

    with calc1:
        units = st.radio("Units", ["US", "Metric"], horizontal=True)
        if units == "US":
            weight_lb = st.number_input("Weight (lb)", min_value=1.0, value=150.0)
            height_in = st.number_input("Height (inches)", min_value=1.0, value=65.0)
            bmi = 703 * weight_lb / (height_in ** 2)
        else:
            weight_kg = st.number_input("Weight (kg)", min_value=1.0, value=68.0)
            height_cm = st.number_input("Height (cm)", min_value=1.0, value=165.0)
            bmi = weight_kg / ((height_cm / 100) ** 2)
        st.metric("BMI", f"{bmi:.1f}")
        st.caption("BMI is a screening measure, not a diagnosis. Interpret it with clinical context.")

    with calc2:
        carb_g = st.number_input("Carbohydrate grams", min_value=0.0, value=200.0)
        protein_g = st.number_input("Protein grams", min_value=0.0, value=70.0)
        fat_g = st.number_input("Fat grams", min_value=0.0, value=60.0)
        kcal = carb_g * 4 + protein_g * 4 + fat_g * 9
        st.metric("Estimated energy", f"{kcal:,.0f} kcal")
        st.write(f"Carbohydrate: {carb_g * 4:,.0f} kcal")
        st.write(f"Protein: {protein_g * 4:,.0f} kcal")
        st.write(f"Fat: {fat_g * 9:,.0f} kcal")

    with calc3:
        weight_kg = st.number_input("Weight (kg)", min_value=1.0, value=70.0, key="protein_weight")
        factor = st.slider("Classroom factor (g/kg/day)", 0.8, 2.0, 0.8, 0.1)
        estimate = weight_kg * factor
        st.metric("Estimated protein", f"{estimate:.0f} g/day")
        st.warning("This is a classroom estimate. Actual needs vary with age, pregnancy, wounds, critical illness, kidney or liver disease, dialysis, and the care plan.")

    with calc4:
        weight_kg = st.number_input("Weight (kg)", min_value=1.0, value=70.0, key="fluid_weight")
        factor = st.slider("Classroom factor (mL/kg/day)", 20, 35, 30)
        estimate = weight_kg * factor
        st.metric("Estimated fluid", f"{estimate:,.0f} mL/day")
        st.warning("Do not use a generic fluid estimate for patients with heart failure, kidney failure, major fluid losses, critical illness, or prescribed restrictions.")

elif page == "Study Resources":
    st.header("Study Resources")
    st.markdown(
        """
        ### How to use this app
        1. Review one content section.
        2. Complete its interactive activity.
        3. Answer topic questions with rationales.
        4. Finish with a clinical case.
        5. Use the mixed exam after reviewing all topics.

        ### Recommended evidence sources
        - Current course materials and assigned ATI Nutrition readings
        - USDA MyPlate and Dietary Guidelines resources
        - Centers for Disease Control and Prevention nutrition resources
        - National Institutes of Health Office of Dietary Supplements
        - Current facility policies and clinical practice guidelines

        ### Study prompts
        - What is the nutrient's main function?
        - What happens when the patient receives too little or too much?
        - Which patients have the highest risk?
        - What should the nurse assess?
        - What teaching is safe, realistic, and culturally responsive?
        """
    )

    st.markdown(
        '<div class="warning"><strong>Copyright note:</strong> This app uses original summaries and practice questions. Add your own course-specific notes, but do not paste copyrighted textbook chapters into a public repository.</div>',
        unsafe_allow_html=True,
    )
