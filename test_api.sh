#!/bin/bash
# Test script to send API request to OpenAI model and print the response
# Usage: ./test_api.sh

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}=== OpenAI API Test Script ===${NC}"
echo ""

# Load environment variables from .env file if it exists
if [ -f .env ]; then
    echo -e "${YELLOW}Loading environment variables from .env file...${NC}"
    set -a
    source .env
    set +a
    echo -e "${GREEN}Environment variables loaded${NC}"
else
    echo -e "${YELLOW}Warning: .env file not found. Checking for OPENAI_API_KEY environment variable...${NC}"
fi

# Check if OPENAI_API_KEY is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo -e "${RED}Error: OPENAI_API_KEY is not set${NC}"
    echo "Please set OPENAI_API_KEY in your .env file or as an environment variable"
    echo "Example: export OPENAI_API_KEY='your-api-key-here'"
    exit 1
fi

echo -e "${GREEN}API Key found${NC}"
echo ""

# Check if curl is available
if ! command -v curl &> /dev/null; then
    echo -e "${RED}Error: curl is not installed${NC}"
    echo "Please install curl to use this script"
    exit 1
fi

# Check if python3 is available
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}Error: python3 is not installed${NC}"
    echo "Please install python3 to use this script"
    exit 1
fi

# Set default model if not specified (matching the default in find_job.py)
MODEL="${OPENAI_MODEL:-gpt-4}"
echo -e "${YELLOW}Using model: ${MODEL}${NC}"
echo ""

# Test prompt
TEST_PROMPT="Hello! This is a test message. Please respond with a brief confirmation that you received this message."

echo -e "${GREEN}Sending test request to OpenAI API...${NC}"
echo -e "${YELLOW}Test prompt: ${TEST_PROMPT}${NC}"
echo ""

# Make API request
RESPONSE=$(curl -s https://api.openai.com/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $OPENAI_API_KEY" \
  -d "{
    \"model\": \"$MODEL\",
    \"messages\": [
      {
        \"role\": \"system\",
        \"content\": \"You are a helpful assistant for testing API connectivity.\"
      },
      {
        \"role\": \"user\",
        \"content\": \"$TEST_PROMPT\"
      }
    ],
    \"max_tokens\": 150,
    \"temperature\": 0.7
  }")

# Check if response contains an error
if echo "$RESPONSE" | grep -q '"error"'; then
    echo -e "${RED}Error from API:${NC}"
    echo "$RESPONSE" | python3 -m json.tool
    exit 1
fi

# Print the full JSON response
echo -e "${GREEN}=== Full API Response ===${NC}"
if ! echo "$RESPONSE" | python3 -m json.tool; then
    echo -e "${RED}Failed to parse JSON response${NC}"
    echo "Raw response: $RESPONSE"
    exit 1
fi
echo ""

# Extract and print just the message content
echo -e "${GREEN}=== Extracted Message Content ===${NC}"
MESSAGE_CONTENT=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); print(data['choices'][0]['message']['content'] if 'choices' in data and len(data['choices']) > 0 else 'No content found')" 2>&1)

if [ $? -eq 0 ] && [ "$MESSAGE_CONTENT" != "No content found" ]; then
    echo -e "${YELLOW}$MESSAGE_CONTENT${NC}"
    echo ""
    echo -e "${GREEN}✓ API test completed successfully!${NC}"
else
    echo -e "${RED}Failed to extract message content from response${NC}"
    echo "Error: $MESSAGE_CONTENT"
    exit 1
fi

# Print usage statistics
echo ""
echo -e "${GREEN}=== Usage Statistics ===${NC}"
USAGE_DATA=$(echo "$RESPONSE" | python3 -c "import sys, json; data = json.load(sys.stdin); usage = data.get('usage', {}); print(f\"{usage.get('prompt_tokens', 'N/A')}|{usage.get('completion_tokens', 'N/A')}|{usage.get('total_tokens', 'N/A')}\")" 2>&1)

if [ $? -eq 0 ]; then
    IFS='|' read -r PROMPT_TOKENS COMPLETION_TOKENS TOTAL_TOKENS <<< "$USAGE_DATA"
    echo "Prompt tokens: $PROMPT_TOKENS"
    echo "Completion tokens: $COMPLETION_TOKENS"
    echo "Total tokens: $TOTAL_TOKENS"
else
    echo -e "${YELLOW}Usage statistics not available in response${NC}"
fi
