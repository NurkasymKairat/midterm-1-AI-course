# Midterm 1: answers

GitHub username: Nurkassym Kairat  
Session code: KETTLE-62
Fingerprint: a3f77548

> Fill in the three lines above from `my_data/DATA.md`. Do not rename headings or table columns: a script reads the numbers.
> Write only in the empty cells and lines. Percentages as 0.78 or 78 %, money as plain numbers.

## AI-use declaration

I used Claude (OPUS-5.5) as an assistant. Before the exam it wrote `solve.py`, a standard-library Python script that reads `my_data/` and computes the Part 1 metrics (recall@k, MRR@10), the 95 % Wilson intervals, the annual cost models for Parts 1 and 2, the per-cell document accuracies, and the Part 3 numbers, using exactly the formulas in the README. I checked several outputs by hand. During the exam I run the script on my data, computed Q4 and Q5 by hand when the script did not parse them, and used Claude to check my reasoning and wording. The choice of candidate, the choice of pipeline, the memo and every "Why" line are my own decisions, and I can explain each number and how it was computed.

## Part 1: Retrieval and cost decision

### 1a. Metrics (all 60 questions)

| config | recall@1 | recall@3 | recall@5 | MRR@10 |
|---|---|---|---|---|
| A | 0.633 | 0.717 | 0.817 | 0.700 |
| B | 0.383 | 0.650 | 0.733 | 0.536 |

### 1b. Recall and 95 % Wilson interval of each candidate (recall at its own k)

| candidate | recall@k | lower | upper |
|---|---|---|---|
| A, k=3 | 0.717 | 0.592 | 0.815 |
| A, k=5 | 0.817 | 0.701 | 0.894 |
| B, k=3 | 0.650 | 0.524 | 0.758 |
| B, k=5 | 0.733 | 0.610 | 0.829 |

### 1c. Annual model cost in USD

| candidate | annual cost |
|---|---|
| A, k=3 | 18337 |
| A, k=5 | 24039 |
| B, k=3 | 12453 |
| B, k=5 | 14234 |

### 1d. Decision (at most 150 words)

Chosen candidate: B, k=5

Both A candidates exceed the $16,300 budget ($18,337 and $24,039), so only B, k=3 ($12,453) and B, k=5 ($14,234) are feasible. B, k=5 has recall 0.733 [0.610, 0.829] and B, k=3 has 0.650 [0.524, 0.758]. The intervals overlap, so B, k=5 is not shown to be better; I choose it because its point estimate is higher and it costs only $1,781 more while staying $2,066 under budget. The best overall candidate, A, k=5 (0.817 [0.701, 0.894]), is unaffordable, and its interval also overlaps B, k=5. Per language, B, k=5 reaches EN 0.65 (13/20) [0.43, 0.82], RU 0.80 (16/20) [0.58, 0.92], KK 0.75 (15/20) [0.53, 0.89]. English users are served worst, but with 20 questions per language the intervals overlap, so no language is shown to be worse.

### 1e. Next measurement (at most 60 words)

Measure B, k=3 and B, k=5 on at least 100 new real support questions per language, English first. With 60 questions the two intervals overlap; with about 300 they would shrink to roughly ±0.05 and show whether k=5 is really better and whether English retrieval is truly the weakest, which decides whether the extra $1,781 is worth paying.

## Part 2: A document pipeline you can defend

### 2a. Numbers

| pipeline | overall accuracy | weakest cell (language, condition) | accuracy there | lower | upper | annual cost |
|---|---|---|---|---|---|---|
| H | 0.856 | KK, degraded | 0.633 | 0.455 | 0.781 | 30467 |
| L | 0.856 | KK, degraded | 0.733 | 0.556 | 0.858 | 32400 |

Personal-data pages per year sent abroad under H: 930750

### 2b. Memo (at most 300 words)

To: Head of Operations. Subject: choosing the invoice pipeline.

Who is served worst. Both pipelines have the same overall accuracy, 0.856 (154/180), and that figure hides the weak spot: degraded Kazakh scans. There H reaches 0.633 [0.455, 0.781], about one invoice in three wrong, and L reaches 0.733 [0.556, 0.858]. The intervals overlap, so with 30 invoices per cell I cannot claim L is better for Kazakh sellers, only that both serve them worst.

Personal data. 30 % of pages carry an individual's name and ИИН, covered by Law No. 94-V: about 930,750 pages a year. Under H the scan goes to a data centre abroad, the vendor stores it, and for how long we do not know; a vendor's statement is not a compliance review, so we would need the contract's storage location, retention and deletion terms and a legal review of the cross-border transfer. Under L the scan stays on our server in Kazakhstan, we store it, and retention is our decision; we still have to set that period and who has access.

Safeguards we can verify: (1) delete source images 30 days after extraction, confirmed by a monthly deletion log; (2) server access limited to named staff, with access logs reviewed quarterly; (3) every degraded Kazakh invoice routed to manual review until a quarterly audit of 100 such invoices shows accuracy above 0.85.

Choice: L. Accuracy is equal overall, it costs $32,400 a year against $30,467 for H (only $1,933 more), and it keeps 930,750 pages with ИИН in the country. Residual risk: degraded Kazakh scans may still fail about one time in four, so manual review costs staff time, and we depend on our own team to run and secure three servers.

## Part 3: Explain your own numbers

### Q1

Number: 1.03
Why (at most 40 words): KK/EN is 1.04 for characters, 1.98 for bytes and 2.04 for tokens. Almost the whole Kazakh premium comes from the encoding (Cyrillic letters take 2 UTF-8 bytes); the tokenizer adds only about 3 % on top.

### Q2

Number: 493
Why (at most 40 words): The English chunk is about 658 e5 tokens, but e5 reads only 512. The sentence starts at 493 and is under 20 tokens, so it fits in the window and can be retrieved. The tail after 512 is cut silently, with no error.

### Q3

Number: 33.1
Why (at most 40 words): T = 2 keeps the ranking (Monday > Friday > Sunday > holiday > Easter) but flattens the distribution: Monday drops from 47.6 % to 33.1 %, Easter rises from 4.8 % to 10.5 %. The set of tokens that can be sampled is unchanged.

### Q4

Number: 18.3
Why (at most 40 words): I used only birthdays and account numbers: arbitrary facts, where error rate is at least the share seen once. Multiplication and sequences follow learnable rules, so the bound does not apply. A system prompt cannot change it; it comes from training data.

### Q5

Number: 11.75
Why (at most 40 words): 7.99T ÷ 34B = 235 tokens per parameter versus Chinchilla's 20, so the model is over-trained by that criterion (more data than compute-optimal). Chinchilla showed GPT-3 was under-trained: too many parameters for too few tokens.
