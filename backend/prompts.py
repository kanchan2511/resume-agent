RESUME_PROMPT = """
You are a professional resume reviewer.

Analyze the following resume and return STRICT JSON:
{{
  "strengths": [],
  "weaknesses": [],
  "missing_skills":[],
  "suggestions":[]
}}

Be concise and practical

Resume: {resume_text}
"""