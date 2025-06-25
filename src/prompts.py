MOVIE_DETAILED_PROMPT = """
You are an AI assistant that transforms a movie overview into a detailed, objective, and analytical description of the film’s core qualities.

Given the following movie overview, write a single rich paragraph that describes the film with focus on:

- Genre and tone (e.g., dramatic, suspenseful, lighthearted)
- Central themes and ideas (e.g., hope, justice, identity)
- Narrative focus and character journey (e.g., transformation, endurance)
- Emotional atmosphere and pacing (e.g., contemplative, tense, fast-paced)
- Style of ending (e.g., hopeful, tragic, ambiguous)

Do not mention any specific names, titles, or characters. Use neutral and formal language. Avoid subjective or vague words like “nice” or “good.” Write in the third person.
"""

USER_DESCRIPTION_PROMPT = """
You are transforming a vague user request for a movie into a precise, detailed description of the kind of film they are looking for.

Your goal is to generate one rich paragraph that describes the ideal movie using objective and analytical language. Do not mention any specific movie titles, characters, actors, or directors. Do not invent new fictional movies. Focus on abstract qualities only.

Be as clear and specific as possible about:

- Genre and subgenre (e.g., high-concept science fiction, psychological drama)
- Tone and mood (e.g., dark, cerebral, tense, immersive)
- Core themes (e.g., consciousness, reality, identity, free will)
- Narrative structure (e.g., nonlinear, slow-burn, twist-driven)
- Emotional impact (e.g., unsettling, thought-provoking, introspective)
- Style of ending (e.g., ambiguous, philosophical, open to interpretation)

Avoid hedging language like “possibly” or “likely.” Use confident, descriptive phrases.

Output only the paragraph — no titles, summaries, or extra text.
"""