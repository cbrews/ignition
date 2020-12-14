import ignition

response1 = ignition.request('//gemini.circumlunar.space')
response2 = ignition.request('software', referer=response1.url)

print(response2)