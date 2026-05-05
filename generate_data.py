import pandas as pd
import random

real_news_templates = [
    "The government has announced a new initiative to boost {} production by {}% over the next {} years.",
    "Local authorities report a significant decrease in {} rates following the new {} program.",
    "Scientists have discovered a new species of {} in the {}, shedding light on biodiversity.",
    "The stock market saw a record high today as major {} companies released their quarterly earnings.",
    "A major {} is expected to hit the coastal region; residents are advised to evacuate.",
    "The Ministry of Health announced the successful rollout of the nationwide {} campaign.",
    "The international space agency successfully launched a new satellite to monitor {}.",
    "A recent economic study shows that {} has cooled down slightly over the past quarter.",
    "The local {} team won the championship game last night in a thrilling overtime victory.",
    "A new public {} line has opened in the city center, expected to reduce commute times.",
    "Global leaders gathered in {} today to discuss climate change and {} policies.",
    "The central bank decided to keep interest rates steady at {}% for the upcoming quarter.",
    "Tech giant {} unveiled its latest smartphone with revolutionary {} features.",
    "Researchers at {} University found a correlation between {} and improved mental health.",
    "A rare {} eclipse will be visible across North America tomorrow night.",
    "The upcoming election is seeing record voter turnout in key {} states.",
    "Healthcare workers are organizing a strike next week demanding better {} and working conditions.",
    "The {} film festival concluded last night with the top prize awarded to an independent director.",
    "A new cybersecurity report warns of increased {} attacks targeting financial institutions.",
    "The city council approved a budget of ${} million for upgrading infrastructure."
]

fake_news_templates = [
    "Shocking report reveals that {} have secretly taken over the government using mind control.",
    "Scientists confirm that drinking {} daily can cure all known diseases.",
    "The moon has officially been sold to a private corporation, and they plan to charge for {}.",
    "A new law has been passed making it illegal to own more than {} pairs of shoes.",
    "Local farmer discovers his cows are producing {} directly from their udders.",
    "Breaking: The earth will temporarily lose its {} next Tuesday, everyone must tie themselves down.",
    "The Eiffel Tower is being relocated to a new theme park in {} to make room for a mall.",
    "A newly discovered species of {} is capable of speaking fluent Spanish and works for the UN.",
    "Drinking water is a myth created by {}; scientists say drinking {} is much healthier.",
    "The popular social media app will begin charging users ${} a month unless they forward this message.",
    "A man claims to have time-traveled from the year {} to warn us about the impending {} invasion.",
    "Eating {} every day makes you immune to aging, top secret study reveals.",
    "The government is replacing all birds with robotic surveillance drones starting in {}.",
    "A giant {} has been spotted swimming in the local river, terrifying residents.",
    "Billionaire {} announces plan to build a massive dome over the entire city of {}.",
    "Using your smartphone for more than {} hours a day turns your blood into {}.",
    "Aliens landed in {} and immediately asked for the recipe to the world's best {}.",
    "Secret underground city discovered beneath {}, populated entirely by {}.",
    "The alphabet is being reduced to 20 letters to save space on digital keyboards.",
    "If you hold your breath for {} minutes, you unlock hidden superpowers."
]

fillers = {
    'real': [
        ['renewable energy', 'oil', 'solar'], [20, 15, 30], ['five', 'ten', 'three'],
        ['crime', 'poverty', 'pollution'], ['community policing', 'education', 'recycling'],
        ['marine life', 'insects', 'plants'], ['Mariana Trench', 'Amazon', 'Sahara'],
        ['technology', 'automotive', 'pharmaceutical'],
        ['hurricane', 'storm', 'blizzard'],
        ['vaccination', 'health awareness', 'fitness'],
        ['global climate change', 'deforestation', 'ocean currents'],
        ['inflation', 'unemployment', 'housing prices'],
        ['sports', 'football', 'basketball'],
        ['transportation', 'subway', 'bus'],
        ['Paris', 'New York', 'Tokyo'], ['environmental', 'trade', 'security'],
        ['2.5', '3.0', '1.5'],
        ['Apple', 'Google', 'Microsoft'], ['AI', 'camera', 'battery'],
        ['Harvard', 'Stanford', 'Oxford'], ['exercise', 'meditation', 'sleep'],
        ['lunar', 'solar'],
        ['swing', 'battleground', 'coastal'],
        ['pay', 'benefits', 'equipment'],
        ['Cannes', 'Sundance', 'Venice'],
        ['phishing', 'ransomware', 'DDoS'],
        ['100', '50', '200']
    ],
    'fake': [
        ['aliens', 'lizards', 'robots'],
        ['battery acid', 'bleach', 'gasoline'],
        ['looking at it', 'moonlight', 'tides'],
        ['three', 'two', 'five'],
        ['chocolate milk', 'soda', 'gold'],
        ['gravity', 'oxygen', 'sunlight'],
        ['Dubai', 'Las Vegas', 'Mars'],
        ['bird', 'dog', 'fish'],
        ['water companies', 'the government', 'Big Pharma'], ['soda', 'syrup', 'oil'],
        ['50', '100', '20'],
        ['3000', '2500', '2100'], ['zombie', 'alien', 'robot'],
        ['pizza', 'dirt', 'paper'],
        ['2025', '2030', 'tomorrow'],
        ['squid', 'monster', 'dinosaur'],
        ['Elon Musk', 'Jeff Bezos', 'Mark Zuckerberg'], ['New York', 'London', 'Tokyo'],
        ['10', '20', '24'], ['jelly', 'acid', 'sand'],
        ['New York', 'Paris', 'London'], ['pizza', 'tacos', 'burgers'],
        ['Los Angeles', 'London', 'Chicago'], ['vampires', 'mole people', 'clowns'],
        ['5', '10', '15']
    ]
}

data = []

# Generate 200 real and 200 fake news items
for _ in range(200):
    template = random.choice(real_news_templates)
    num_blanks = template.count("{}")
    
    # Simple strategy: just pick random words for blanks
    # Since we don't map specific blanks to specific fillers perfectly in this simple script, 
    # we'll just flatten the fillers and pick randomly
    flat_fillers = [item for sublist in fillers['real'] for item in sublist]
    filled = template.format(*[random.choice(flat_fillers) for _ in range(num_blanks)])
    data.append([filled, 'REAL'])

for _ in range(200):
    template = random.choice(fake_news_templates)
    num_blanks = template.count("{}")
    flat_fillers = [item for sublist in fillers['fake'] for item in sublist]
    filled = template.format(*[random.choice(flat_fillers) for _ in range(num_blanks)])
    data.append([filled, 'FAKE'])

df = pd.DataFrame(data, columns=['text', 'label'])
df = df.sample(frac=1).reset_index(drop=True)
df.to_csv('dataset.csv', index=False)
print("Generated a larger dataset.csv with 400 entries.")
