# AI Service Configuration
# Set AI_PRIORITY to control which AI system to use first

# Options:
# "custom" - Use custom AI first (recommended after training)
# "gemini" - Use Gemini first (recommended for immediate deployment)
# "auto" - Auto-detect best option

AI_PRIORITY = "gemini"  # Gemini primary, Custom AI fallback

# Fallback settings
ENABLE_CUSTOM_AI = True
ENABLE_GEMINI_AI = True
ENABLE_RULE_BASED = True

# Performance settings
CUSTOM_AI_TIMEOUT = 5  # seconds
GEMINI_AI_TIMEOUT = 10  # seconds