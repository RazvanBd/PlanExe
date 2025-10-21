# Using PlanExe with Google Gemini API

Google Gemini offers direct API access with competitive pricing and high performance.

## Why use Gemini?

- **Fast response times**: Gemini 2.0 Flash is optimized for speed
- **Large context windows**: Up to 1-2M tokens depending on the model
- **Competitive pricing**: Starting at $0.075/M input tokens for Gemini 2.0 Flash
- **Direct integration**: Connect directly to Google's API

## Configuration

### Step 1: Create API key

1. Visit [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Click `Get API Key` or `Create API Key` and create a new key for PlanExe
3. Copy the API key (it will look like: `AIzaSy...`)

### Step 2: Add API key to .env file

Copy `.env.example` to a new file called `.env` if you haven't already.

Open the `.env` file in a text editor and add your Gemini API key:

```
GEMINI_API_KEY='AIzaSy_YOUR_API_KEY_HERE'
```

### Step 3: Update llm_config.json

The `llm_config.json` file already includes Gemini configurations. You can use them as-is or customize them.

Example configurations:

```json
{
    "gemini-paid-flash-2.0": {
        "comment": "Fast and affordable. Good for most use cases.",
        "priority": 1,
        "class": "Gemini",
        "arguments": {
            "model": "models/gemini-2.0-flash-exp",
            "api_key": "${GEMINI_API_KEY}",
            "temperature": 0.1,
            "max_tokens": 8192
        }
    },
    "gemini-paid-pro-2.0": {
        "comment": "More capable model with reasoning capabilities.",
        "priority": 4,
        "class": "Gemini",
        "arguments": {
            "model": "models/gemini-2.0-flash-thinking-exp-01-21",
            "api_key": "${GEMINI_API_KEY}",
            "temperature": 0.1,
            "max_tokens": 8192
        }
    }
}
```

## Available Models

Visit [Google AI Studio Models](https://ai.google.dev/gemini-api/docs/models/gemini) for a complete list of available models.

Popular models for PlanExe:
- `models/gemini-2.0-flash-exp` - Fast, affordable, great for most tasks
- `models/gemini-2.0-flash-thinking-exp-01-21` - Advanced reasoning capabilities
- `models/gemini-1.5-pro` - Balanced performance and capability

## Using Gemini in PlanExe

1. Restart PlanExe after making configuration changes
2. Go to the `Settings` tab in the UI
3. Select one of the `gemini-paid-*` models from the dropdown
4. Start creating plans!

## Pricing

Check the latest pricing at [Google AI Pricing](https://ai.google.dev/pricing).

As of the documentation date:
- Gemini 2.0 Flash: $0.075/M input tokens, $0.30/M output tokens
- Gemini 1.5 Pro: $1.25/M input tokens, $5.00/M output tokens

Note: Pricing may change. Always verify current rates before use.

## Troubleshooting

### API Key Issues

If you see authentication errors:
- Verify your API key is correct in the `.env` file
- Ensure the API key is active in Google AI Studio
- Check if you have billing enabled (required for some models)

### Model Not Available

If a model isn't available:
- Check the [available models list](https://ai.google.dev/gemini-api/docs/models/gemini)
- Some models may require waitlist access or specific API tier
- Update the model name in `llm_config.json` to a supported model

### Rate Limiting

If you encounter rate limiting:
- Check your quota in Google AI Studio
- Consider upgrading your API tier
- Add delays between requests if needed

### General Issues

Inside PlanExe, when clicking `Submit`, a new `Output Dir` should be created containing a `log.txt`. Open that file and scroll to the bottom to see any error messages.

Report your issue on [Discord](https://neoneye.github.io/PlanExe-web/discord). Please include:
- Your system info (OS, hardware)
- The error message from `log.txt`
- The model you're trying to use
