import grammarly

client = grammarly.Client(api_key='your_api_key')

text = 'The quick brow fox jumps over the lazy dog.'
result = client.check(text)
print(result)
