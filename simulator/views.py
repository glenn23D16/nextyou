from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import os
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

client = OpenAI()

print("KEY:", os.getenv("OPENAI_API_KEY"))

@csrf_exempt
def simulate(request):
    if request.method == "POST":
        age = request.POST.get("age")
        work = request.POST.get("work")
        goal = request.POST.get("goal")
        scenario = f"The user wants to: {goal}"

        prompt = f"""
You are generating a highly shareable future simulation.

The output must feel real, structured, and emotionally satisfying.
It should show a clear path from struggle to progress to success.

Structure:

1. Caption (1 sentence)
- Personal and thought-provoking
- Should create immediate emotional connection

2. Story (2 short paragraphs)

- The story must revolve around ONE specific decision
- Start with the moment of that decision
- Make it feel like a turning point

- First paragraph: the moment of decision + immediate struggle
- Second paragraph: how life changed because of that decision

- Max 2 sentences per paragraph
- Max 12–16 words per sentence
- Keep it simple and clear
_ The decision must happen in a specific moment (e.g. "that day", "that night", "after work")

- The reader must clearly understand:
  "this decision changed everything"

Avoid vague progress. Focus on cause → effect.

3. Highlight (1 sentence, wrapped in [highlight] tags)
- Must feel personal and specific
- Should reflect a realization or turning point
- Must NOT be generic or philosophical

Tone:
- Real
- Grounded
- Clear
- Quietly confident

Avoid:
- Vague or abstract writing
- Overly poetic language
- Generic motivational phrases
- Losing structure or direction

User input:
Age: {age}
Current situation: {work}
Goal: {goal}

Generate the output in THREE SEPARATE PARTS, separated by two line breaks (\n\n):

First part:
- A single sentence caption

Second part:
- A structured story with clear progression

Third part:
- One highlight sentence wrapped in [highlight] tags

IMPORTANT:
- Do NOT include labels like "Caption", "Story", or "Highlight"
- Do NOT number the sections
- Output only the text itself
"""

        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.6
        )

        full_text = response.choices[0].message.content.strip()

        parts = full_text.split("\n\n")

        caption = parts[0].strip() if len(parts) > 0 else ""
        story_parts = parts[1:-1] if len(parts) > 2 else []
        highlight = parts[-1].strip() if len(parts) > 1 else ""

        story = "<p>" + "</p><p>".join(story_parts) + "</p>"

        # highlight fix
        highlight = highlight.replace("[highlight]", '<span class="highlight">')
        highlight = highlight.replace("[/highlight]", '</span>')

        story = story.replace("[highlight]", "")
        story = story.replace("[/highlight]", "")

        return render(request, "simulator/result.html", {
            "caption": caption,
            "story": story,
            "highlight": highlight
        })
    return render(request, "simulator/form.html")
