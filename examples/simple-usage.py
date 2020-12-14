import ignition

# Fetch capsule content
response = ignition.request('//gemini.circumlunar.space')

# Print full response from remote capsule
print(response)