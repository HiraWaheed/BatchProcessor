## Batch Processing
This project explores different API's supporting batch processing. 

# WIP
Using OpenAI's gpt for batch processing.

# Setup
- Install Project Dependencies
```bash
pip3 install -r requirements.txt
```
- Setup .env with your API keys
```
OPENAI_API_KEY='sk-proj-'
```
- Keep your csvs in inputs folder

- Run project
```python
python3 main.py
```

# Example
The inputs folder csv contains story names
```data.csv
Boy who conquered space
```
The response (story) from Gpt-4o
```json
{ "Story Name": "The Boy Who Conquered Space", "Story": "Leo was just a curious twelve-year-old with a telescope and an unquenchable thirst for the stars. Every night, he’d lie on his rooftop, sketching constellations and dreaming of distant galaxies. One evening, he discovered a shimmering, silver stone in his backyard, humming with an energy he couldn't explain. The stone whispered secrets of the universe, unlocking knowledge beyond human comprehension. With this newfound wisdom, Leo built a ship from scrap metal and stardust, ready to embark on an adventure no boy had dared before.\n\nAs his ship soared past the moon and into the unknown, Leo encountered celestial wonders—dancing nebulas, shimmering asteroid belts, and alien civilizations. Instead of fear, he offered friendship, solving conflicts and bringing unity among distant planets. Word of the Earth boy spread across galaxies, naming him the peacemaker of the cosmos. When he finally returned home, the stars twinkled a little brighter, and the universe felt just a bit smaller. Leo had not just traveled through space—he had conquered it with kindness." }
```