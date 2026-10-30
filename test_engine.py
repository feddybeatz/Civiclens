from ai.ai_engine import ask_gemma

ps = [{"page": 12, "text": "Allocation for the water sector is KSh 5.2 billion in FY 2025/26."}]
print(ask_gemma("How much is allocated to water?", ps, "Test doc"))
print(ask_gemma("How much is allocated to defence?", ps, "Test doc"))
