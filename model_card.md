# Model Card: VibeFinder 2.0

## 1. Model Name
**VibeFinder 2.0** — Applied AI Music Recommendation System

---

## 2. Intended Use
VibeFinder 2.0 is designed to recommend music based on a user's mood, genre preference, and energy level. It combines content-based filtering with RAG retrieval, agentic Wikipedia search, and AI-generated explanations. It is built for the AI110 Final Project to demonstrate a full applied AI system pipeline.

---

## 3. How the Model Works
VibeFinder 2.0 uses a four-stage pipeline:

1. **Recommender** — scores songs from a local CSV using genre match (+2.0), mood match (+1.0), and energy similarity (0.0–1.0)
2. **RAG Retriever** — searches a local knowledge base of genre and mood descriptions to retrieve relevant context
3. **Wikipedia Agent** — autonomously searches Wikipedia for live context about the requested genre
4. **LLM Explainer** — combines all context and generates a natural language explanation using Gemini 2.5 Flash, with a rule-based fallback if the API is unavailable

---

## 4. Data
- Song catalog: 20 songs in `data/songs.csv`
- Knowledge base: `data/knowledge_base.txt` containing genre and mood descriptions
- External data: Wikipedia API (live, no authentication required)
- Genres: pop, rock, hip-hop, jazz, electronic, r&b, classical
- Moods: happy, sad, energetic, chill, romantic, focused

---

## 5. Strengths
- Fully explainable — every recommendation includes a reason
- Works without any API key thanks to Wikipedia and rule-based fallback
- Modular design makes each component independently testable
- Graceful error handling — app never crashes due to API failures
- 5/5 eval tests passed with 1.0 average confidence score

---

## 6. Limitations and Bias
- Song catalog is small (20 songs), limiting diversity in results
- Genre match is weighted 2x more than mood, which can create filter bubbles
- Wikipedia summaries can be generic and may not always match the user's specific vibe
- Gemini explanations depend on quota availability — free tier has daily limits
- The knowledge base only covers 7 genres and 6 moods — requests outside these may get weaker results
- Dataset reflects Western popular music and does not represent global music styles

---

## 7. Evaluation
Ran 5 predefined test cases using `eval.py`:

- **Happy Pop** — PASS (confidence: 1.0) — correct songs, strong explanation
- **Chill Jazz** — PASS (confidence: 1.0) — relaxed songs retrieved, Wikipedia context accurate
- **Energetic Rock** — PASS (confidence: 1.0) — high-energy songs ranked correctly
- **Sad R&B** — PASS (confidence: 1.0) — emotional songs matched mood well
- **Focused Classical** — PASS (confidence: 1.0) — steady, calm songs returned as expected

All 5 tests passed. The system struggled slightly with genres not well represented in the CSV (like lofi or ambient) returning general matches instead of specific ones.

---

## 8. Reflection and Ethics

**What are the limitations or biases in your system?**
The genre weight dominates scoring, which can create a filter bubble where users only see one genre. The small dataset also limits diversity — users with niche tastes get fewer relevant results.

**Could your AI be misused, and how would you prevent that?**
The system could be used to promote certain songs or artists unfairly by manipulating the dataset. Preventing this would require dataset auditing and transparency about how songs are scored.

**What surprised you while testing your AI's reliability?**
I was surprised that all 5 eval tests passed with perfect confidence scores. I expected at least one failure due to API quota issues, but the fallback system handled everything gracefully.

**Describe your collaboration with AI during this project.**
Claude helped me design the pipeline architecture and write the RAG, agent, and explainer modules. One helpful suggestion was building a rule-based fallback for the explainer, this made the system much more reliable. One flawed suggestion was using `gemini-2.0-flash` which turned out to be deprecated, had to switch to `gemini-2.5-flash` after getting errors.

---

## 9. Future Work
- Expand the song catalog to hundreds of songs across more genres
- Replace keyword RAG with embedding-based semantic search for better retrieval
- Add a real web search agent using Tavily or SerpAPI for richer song discovery
- Implement user feedback loop so the system learns from ratings over time
- Add collaborative filtering to complement content-based recommendations
