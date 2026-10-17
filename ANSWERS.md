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

config	recall@1	recall@3	recall@5	MRR@10
A	0.633	0.717	0.817	0.700
B	0.383	0.650	0.733	0.536

### 1b. Recall and 95 % Wilson interval of each candidate (recall at its own k)

candidate	recall@k	lower	upper
A, k=3	0.717	0.592	0.815
A, k=5	0.817	0.701	0.894
B, k=3	0.650	0.524	0.758
B, k=5	0.733	0.610	0.829
### 1c. Annual model cost in USD

candidate	annual cost
A, k=3	18337
A, k=5	24039
B, k=3	12453
B, k=5	14234

### 1d. Decision (at most 150 words)

Chosen candidate: B, k=5

Both A candidates exceed the $16,300 budget ($18,337 and $24,039), so only B, k=3 ($12,453) and B, k=5 ($14,234) are feasible. B, k=5 has recall 0.733 [0.610, 0.829] and B, k=3 has 0.650 [0.524, 0.758]. The intervals overlap, so B, k=5 is not shown to be better; I choose it because its point estimate is higher and it costs only $1,781 more while staying $2,066 under budget. The best overall candidate, A, k=5 (0.817 [0.701, 0.894]), is unaffordable, and its interval also overlaps B, k=5. Per language, B, k=5 reaches EN 0.65 (13/20) [0.43, 0.82], RU 0.80 (16/20) [0.58, 0.92], KK 0.75 (15/20) [0.53, 0.89]. English users are served worst, but with 20 questions per language the intervals overlap, so no language is shown to be worse.

### 1e. Next measurement (at most 60 words)

Measure B, k=3 and B, k=5 on at least 100 new real support questions per language, English first. With 60 questions the two intervals overlap; with about 300 they would shrink to roughly ±0.05 and show whether k=5 is really better and whether English retrieval is truly the weakest, which decides whether the extra $1,781 is worth paying.

## Part 2: A document pipeline you can defend

### 2a. Numbers

| pipeline | overall accuracy | weakest cell (language, condition) | accuracy there | lower | upper | annual cost |
|---|---|---|---|---|---|---|
| H | | | | | | |
| L | | | | | | |

Personal-data pages per year sent abroad under H:

### 2b. Memo (at most 300 words)

## Part 3: Explain your own numbers

### Q1

Number:
Why (at most 40 words):

### Q2

Number:
Why (at most 40 words):

### Q3

Number:
Why (at most 40 words):

### Q4

Number:
Why (at most 40 words):

### Q5

Number:
Why (at most 40 words):
