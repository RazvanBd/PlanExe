# PlanExe

**What does PlanExe do:** Turn your idea into a comprehensive plan in minutes, not months. Now includes automatic generation of technical task lists for developers!

- An business plan for a [Minecraft-themed escape room](https://neoneye.github.io/PlanExe-web/20251016_minecraft_escape_report.html).
- An business plan for a [Faraday cage manufacturing company](https://neoneye.github.io/PlanExe-web/20250720_faraday_enclosure_report.html).
- An pilot project for a [Human as-a Service](https://neoneye.github.io/PlanExe-web/20251012_human_as_a_service_protocol_report.html).
- See more [examples here](https://neoneye.github.io/PlanExe-web/examples/).

---

<details>
<summary><strong> Try it out now (Click to expand)</strong></summary>
<br>

You can generate 1 plan for free.

[Try it here →](https://app.mach-ai.com/planexe_early_access)

</details>

---

<details>
<summary><strong> Installation (Click to expand)</strong></summary>

<br>

**Prerequisite:** Python 3.10 or higher

# Quick Installation

```bash
git clone https://github.com/neoneye/PlanExe.git
cd PlanExe
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install '.[gradio-ui]'
```

**For detailed installation instructions, troubleshooting, and more options, see [INSTALL.md](INSTALL.md)**

# Configuration

**Config:** Run a model in the cloud using a paid provider. Follow the instructions in [Gemini](extra/gemini.md).

Recommendation: I recommend using **Gemini** as it offers the most straightforward path to getting PlanExe working reliably.

# Usage

PlanExe comes with a Gradio-based web interface. To start the local web server:

```bash
python -m planexe.plan.app_text2plan
```

This command launches a server at http://localhost:7860. Open that link in your browser, type a vague idea or description, and PlanExe will produce a detailed plan.

To stop the server at any time, press `Ctrl+C` in your terminal.

## Technical Task Lists

PlanExe now automatically generates language and framework-agnostic technical task lists! When you run the planner, it creates a detailed list of development tasks that developers can follow step-by-step to build the application.

Each task includes:
- **Title** and detailed **description**
- **Acceptance criteria** for testing completion
- **Examples** showing expected behavior
- **Dependencies** for proper task ordering
- **Effort estimates** and **priority levels**
- **Implementation notes** and considerations

Tasks are generated in the pipeline output as:
- `029-1-technical_tasks_raw.json` - JSON format
- `029-2-technical_tasks.md` - Human-readable markdown

For more details, see [`planexe/technical_tasks/README.md`](planexe/technical_tasks/README.md).

</details>

---

<details>
<summary><strong> Screenshots (Click to expand)</strong></summary>

<br>

You input a vague description of what you want and PlanExe outputs a plan. [See generated plans here](https://neoneye.github.io/PlanExe-web/use-cases/).

![Video of PlanExe](/extra/planexe-humanoid-factory.gif?raw=true "Video of PlanExe")

[YouTube video: Using PlanExe to plan a lunar base](https://www.youtube.com/watch?v=7AM2F1C4CGI)

![Screenshot of PlanExe](/extra/planexe-humanoid-factory.jpg?raw=true "Screenshot of PlanExe")

</details>

---

<details>
<summary><strong> Help (Click to expand)</strong></summary>

<br>

For help or feedback.

Join the [PlanExe Discord](https://neoneye.github.io/PlanExe-web/discord).

</details>
