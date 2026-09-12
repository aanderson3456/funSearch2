import re

with open('/Users/austinanderson/AngularMathgod/mathgod/server.js', 'r') as f:
    content = f.read()

# Add the new API routes to proxyToPythonBackend array
old_array = """app.use([
    '/api/get-move',
    '/api/evaluate',
    '/api/generate-vibe-code',
    '/api/submit-strategy',
    '/api/leaderboard',
    '/api/recent-matches',
    '/api/strategy',
    '/api/alphago'
]"""

new_array = """app.use([
    '/api/get-move',
    '/api/evaluate',
    '/api/generate-vibe-code',
    '/api/submit-strategy',
    '/api/leaderboard',
    '/api/recent-matches',
    '/api/strategy',
    '/api/alphago',
    '/api/funsearch/status',
    '/api/funsearch/step'
]"""

new_content = content.replace(old_array, new_array)

with open('/Users/austinanderson/AngularMathgod/mathgod/server.js', 'w') as f:
    f.write(new_content)

print("Patched server.js")
