from jinja2 import Environment, FileSystemLoader

env = Environment(
    loader=FileSystemLoader('templates'),
    block_start_string=r'\BLOCK{',
    block_end_string='}',
    variable_start_string=r'\VAR{',
    variable_end_string='}',
    comment_start_string=r'\#{',
    comment_end_string='}',
    trim_blocks=True,
    autoescape=False
)

context = {
    "user_name": "Gad Nguette",
    "user_address": "Paris",
    "user_phone": "0600000000",
    "user_email": "test@example.com",
    "company_name": "Effidic",
    "company_address": "Trelaze",
    "job_title": "Data Engineer",
    "ai_generated_paragraph": "Test paragraph",
    "keywords": ["Python", "SQL", "BigQuery"]
}

try:
    template = env.get_template('template_lettre.tex')
    print("Loaded template")
    rendered = template.render(context)
    print("Rendered successfully")
    print(rendered[:100])
except Exception as e:
    print(f"Error: {e}")
