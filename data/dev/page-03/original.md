# The Unsexy Truth About Email Deliverability (and How We Fixed Ours)

Let me tell you a story about the quarter we almost gave up on email.

Our newsletter had been growing steadily for two years. Then one Tuesday morning, our open rate — which had been cruising along comfortably — fell off a cliff. Over the following three weeks it slid from 38% all the way down to 11%. Nothing about our content had changed. What had changed, we eventually discovered, was where our emails were landing: the spam folder.

What followed was a two-month investigation that taught us more about email infrastructure than we ever wanted to know. Here's what actually moved the needle, in case your emails ever start vanishing too.

The first culprit was authentication, or rather the lack of it. We'd never set up DMARC, and Gmail's early-2024 sender requirements had started enforcing it for anyone sending to more than 5,000 Gmail addresses per day — a threshold we'd crossed without noticing. Adding a DMARC record, along with tightening our existing SPF and DKIM setup, was the single highest-impact fix in the whole saga.

The second discovery was our list itself. Buried in our subscriber base were thousands of addresses that hadn't opened anything in over a year. Every send to those dead addresses was quietly telling inbox providers that people didn't want our mail. We ran a re-engagement campaign, then removed everyone who stayed silent — a painful 22% of our list, gone in one afternoon. Our next send had the highest engagement rate in our history.

Third, and this one surprised us: our beautiful, image-heavy template was working against us. Spam filters were reading our 80%-image emails as a classic spammer pattern. We rebuilt the template to be roughly 60% text, and combined with everything else, our spam placement rate dropped below 2%.

The whole recovery took about four months from cliff to comeback. Today our open rate sits at 42% — higher than before the crash. Sometimes the best thing that can happen to your email program is a small disaster.
