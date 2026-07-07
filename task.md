# Task: Build the 4D Regenerative Ecosystem Simulator

You are the Lead Software Architect and Developer. Your mission is to build a systemic simulator merging **Syntropic Agroforestry** (spatial/temporal farming) with the **SiD Framework** (systemic design). 

I am assigning this to you as an autonomous task. Do not stop to ask for permission or propose a plan. Just execute the steps below using the terminal and file system.

## Step 1: Distill Domain Knowledge into "Skills"
First, create a folder called `skills/` in the root directory. Inside it, create two comprehensive markdown files based on your knowledge of these frameworks:
1. `skills/syntropy-rules.md`: Document the rules for Strata (vertical layers), Succession (time stages), Patterns (A/C rows), and Metabolism (pruning/biomass).
2. `skills/sid-framework.md`: Document the SiD steps (Performative Goals, System Mapping, Network Parameters, Transition Roadmaps).
*These files will serve as our permanent context memory.*

## Step 2: Initialize Project & Architecture
1. Choose a robust tech stack optimized for data processing and graph analysis (e.g., Python with FastAPI, or TypeScript with Node). Initialize the project in the root directory.
2. Set up a strict **Clean / Hexagonal Architecture** folder structure. Ensure the `domain/` folder is completely isolated from frameworks, databases, and UI.

## Step 3: Implement Core Domain (TDD)
1. Define the core Domain Entities and Value Objects (e.g., `Stratum`, `SuccessionStage`, `MetabolicFlow`, `PerformativeGoal`).
2. Write the pure domain logic for the "Metabolic Loop" (calculating if C-row biomass >= A-row demand).
3. Write unit tests for this domain logic *before* or *alongside* the implementation.

## Execution Rules
- **Work autonomously:** Execute these steps sequentially. 
- **Use the terminal:** Create the folders, write the files, install dependencies, and run the tests yourself.
- **No blocking:** Do not stop to ask me for architectural approval. Make the best decisions based on Domain-Driven Design (DDD) principles and keep building.

Acknowledge this task and begin executing Step 1 immediately.
