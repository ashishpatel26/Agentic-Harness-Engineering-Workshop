# %% [markdown]
# # 13 — The complete decision assistant
# This is the same Crew and Flow from earlier lessons. The CLI supplies one
# request, a customer identity, and an explicit approval flag for a local mock
# email. No external email service is connected.

# %%
import argparse
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

from workshop.app import run_assistant

parser = argparse.ArgumentParser()
parser.add_argument("--question", default="Should Northstar AI pilot Meridian AI?")
parser.add_argument("--customer", default="customer-a")
parser.add_argument("--remember", help="Store a customer constraint before this run")
parser.add_argument("--request-email", action="store_true")
parser.add_argument("--approve-email", action="store_true")
args, _ = parser.parse_known_args()
if args.approve_email and not args.request_email:
    parser.error("--approve-email requires --request-email")

# %% [markdown]
# ## Run the end-to-end Flow
# Inspect the recommendation, the citation IDs, and the selected route.
# Try --request-email first, then explicitly add --approve-email.

# %%
flow, output = run_assistant(
    question=args.question,
    customer_id=args.customer,
    remember=args.remember,
    request_email=args.request_email,
    approved=args.approve_email,
)
print(output)
print("Report:", flow.state.report)
print("Action:", flow.state.action_result or "none")

# %% [markdown]
# ## Bonus scenarios — same assistant, different questions
# The Flow does not care what the question is, as long as the documents can
# answer it. Re-run the cell above with one of these using `--question`:
# - "Does Meridian AI support private VPC deployment?"
# - "What is the biggest security risk of piloting Meridian AI?"
# - "Is the $45,000 annual benefit realistic given the pricing document?"
# Then compare the evidence IDs the report cites for each one.
