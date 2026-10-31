set -a; source .env; set +a
echo "key set: $([ -n "$GEMINI_API_KEY" ] && echo yes || echo NO) (length ${#GEMINI_API_KEY})"
echo "== list models =="
curl -sS -m 20 -o /tmp/models.json -w "http %{http_code} in %{time_total}s\n" \
  -H "x-goog-api-key: $GEMINI_API_KEY" \
  "https://generativelanguage.googleapis.com/v1beta/models?pageSize=200"
grep -o '"name": *"models/gemma[^"]*"' /tmp/models.json | head
head -c 300 /tmp/models.json | head -n 8
for M in gemma-4-26b-a4b-it gemma-4-31b-it; do
  echo "== $M =="
  curl -sS -m 60 -o /tmp/out.json -w "http %{http_code} in %{time_total}s\n" \
    "https://generativelanguage.googleapis.com/v1beta/models/$M:generateContent" \
    -H "x-goog-api-key: $GEMINI_API_KEY" -H "Content-Type: application/json" \
    -d '{"contents":[{"parts":[{"text":"Say hello in Swahili, in one sentence."}]}]}'
  head -c 500 /tmp/out.json; echo
done
