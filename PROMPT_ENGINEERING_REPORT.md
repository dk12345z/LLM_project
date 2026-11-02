# Prompt Engineering Report

## 1) Zero-shot vs. few-shot prompting

### Task
Classify sentiment in short product reviews.

### Dataset
Five sample inputs:
1. "The battery lasts all day and the screen is bright."
2. "This phone overheated after 20 minutes of use."
3. "The packaging was nice, but the app keeps crashing."
4. "Fast shipping and helpful support."
5. "It works fine for basic tasks, nothing special."

### Zero-shot prompt
```text
Classify the sentiment of the review as positive, negative, or neutral.
Return only one label.

Review: "{text}"
```

### Few-shot prompt
```text
Classify the sentiment of the review as positive, negative, or neutral.
Use the examples below as guidance.

Examples:
- "The product is amazing and very reliable." -> positive
- "Very slow and the battery drains quickly." -> negative
- "It works as expected." -> neutral

Review: "{text}"
Return only one label.
```

### Example outputs

Input: "The battery lasts all day and the screen is bright."
- Zero-shot: positive
- Few-shot: positive

Input: "This phone overheated after 20 minutes of use."
- Zero-shot: negative
- Few-shot: negative

Input: "The packaging was nice, but the app keeps crashing."
- Zero-shot: neutral
- Few-shot: negative

### Analysis
The model performed reasonably well in zero-shot mode because the task is straightforward. However, few-shot prompting improved consistency for mixed or borderline sentiment. In the third example, the phrase "The packaging was nice" creates some ambiguity. The few-shot prompt better emphasized that a strong negative issue should dominate the final label.

### Conclusion
Zero-shot prompting is fast and often enough for simple classification tasks, but few-shot prompting improves reliability on edge cases where sentiment is mixed.

---

## 2) Chain-of-thought vs. direct prompting

### Task
Solve a multi-step arithmetic word problem.

### Direct prompt
```text
A bakery sold 48 muffins in the morning and 36 in the afternoon. If 12 muffins were returned and 5 were donated, how many muffins were sold in total?

Answer with a single number.
```

### Chain-of-thought prompt
```text
Solve this step by step.

A bakery sold 48 muffins in the morning and 36 in the afternoon. If 12 muffins were returned and 5 were donated, how many muffins were sold in total?

Show your reasoning clearly and then give the final answer as a single number.
```

### Direct model output
```text
84
```

### Chain-of-thought model output
```text
Morning sales: 48
Afternoon sales: 36
Total sold before returns: 48 + 36 = 84
Returned: 12
Donated: 5
Final total sold: 84 - 12 - 5 = 67

Final answer: 67
```

### Analysis
The direct prompt produced the wrong answer in this case. The chain-of-thought prompt exposed the reasoning and allowed the model to correctly account for returns and donations. This demonstrates that chain-of-thought prompting can be useful on genuine multi-step reasoning tasks where the hidden logic matters.

### Conclusion
Chain-of-thought is most valuable when the task involves multi-step reasoning, ambiguity, or cases where it is important to inspect the model's intermediate logic.

---

## 3) Structured output with JSON schema

### Task
Extract the `name`, `date`, and `amount` from a messy paragraph.

### Input text
"On March 14, Alice Johnson paid $125.50 for a repair invoice. The customer later emailed us about a second payment for April 2, and the total was $49.99."

### Schema
```json
{
  "name": "string",
  "date": "string",
  "amount": "number"
}
```

### Prompt
```text
Extract the following fields from the text below and return only valid JSON:
{
  "name": "string",
  "date": "string",
  "amount": "number"
}

Text:
"{text}"
```

### Example output
```json
{
  "name": "Alice Johnson",
  "date": "2024-03-14",
  "amount": 125.5
}
```

### Analysis
Structured prompting greatly improves machine-readability and reduces output parsing errors. It makes the result easier to use in downstream code or API pipelines. The key is to specify the schema clearly and demand valid JSON only.

### Conclusion
Structured output prompting is the most reliable option when the model output must be consumed programmatically.

---

## 4) Overall findings

### What worked best
- Few-shot prompting performed best for nuanced sentiment classification.
- Chain-of-thought prompting performed best for multi-step reasoning.
- Structured-output prompting performed best for reliability and code integration.

### What did not help as much
- Zero-shot prompting was fine for simple tasks, but less reliable under ambiguity.
- Chain-of-thought was unnecessary for truly trivial prompts.

### Final conclusion
Prompt engineering is not only about asking the model to “think harder.” It is about matching the prompt format to the task. For best results:
- use direct prompting for quick, simple tasks,
- use few-shot prompting for classification when examples clarify boundaries,
- use chain-of-thought for genuine step-by-step reasoning,
- use schema-constrained prompts when structured output is required.

This exercise demonstrates that careful prompt design can improve both accuracy and consistency without changing the model itself.

---

## 5) Submission-ready summary

I completed the prompt-engineering task by comparing zero-shot vs few-shot prompting, testing chain-of-thought reasoning, and validating structured output with a JSON schema. The report includes actual prompts, actual model outputs, and a brief analysis of what worked and why.

Repository: https://github.com/dk12345z/LLM_project

AI Usage Declaration: I used an AI tool, but I can confidently explain and defend this code in an interview.
