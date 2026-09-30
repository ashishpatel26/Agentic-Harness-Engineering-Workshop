# %% [markdown]
# # 10 — Checkpoint and resume
# CrewAI can save Crew execution state after tasks. Start the script, stop it
# after the first task finishes, then pass a checkpoint file to --resume.
# A checkpoint helps avoid repeating completed *research*; side effects still
# need an idempotent action boundary like the mock email from lesson 09.

# %%
import argparse
import sys
from pathlib import Path

here = Path(__file__).resolve() if "__file__" in globals() else Path.cwd() / "lesson.py"
sys.path.insert(0, str(next(p for p in here.parents if (p / "pyproject.toml").exists())))

import workshop  # configure project-local CrewAI storage
from crewai import Agent, CheckpointConfig, Crew, Process, Task

from workshop.common import model

parser = argparse.ArgumentParser()
parser.add_argument("--resume", type=Path, help="Path to a CrewAI .checkpoints JSON file")
args, _ = parser.parse_known_args()

researcher = Agent(role="Researcher", goal="Find two facts", backstory="Careful researcher", llm=model())
writer = Agent(role="Writer", goal="Summarize research", backstory="Clear communicator", llm=model())
crew = Crew(
    agents=[researcher, writer],
    tasks=[
        Task(description="List two facts about a cautious AI pilot", expected_output="Two bullets", agent=researcher),
        Task(description="Summarize the two facts", expected_output="A short paragraph", agent=writer),
    ],
    process=Process.sequential,
    checkpoint=True,
)

# %% [markdown]
# ## Run or resume
# The checkpoint path is printed by the workshop instructions after an
# interrupted run. Do not invent a checkpoint file; pass the one CrewAI saved.

# %%
if args.resume:
    print(crew.kickoff(from_checkpoint=CheckpointConfig(restore_from=str(args.resume))).raw)
else:
    print(crew.kickoff().raw)

# %% [markdown]
# ## Bonus scenario — writing a book chapter by chapter
# The idea behind resuming, without a model (inspired by CrewAI's *Write a Book* flow):
# finished work is saved, so a re-run skips it. Run this cell twice.

# %%
from workshop.common import ensure_runtime

book = ensure_runtime() / "book"
book.mkdir(exist_ok=True)
for number, title in enumerate(["Why agents", "Tools", "Flows"], start=1):
    chapter = book / f"chapter-{number}.txt"
    if chapter.exists():
        print("skip (already written):", title)
        continue
    chapter.write_text(f"Draft of {title}", encoding="utf-8")  # stands in for a slow Crew run
    print("wrote:", title)
