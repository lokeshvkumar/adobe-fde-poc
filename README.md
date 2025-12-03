# Creative Automation Pipeline (FDE POC)

## 📌 Project Overview
This project is a Proof of Concept (POC) for a **Content Supply Chain** pipeline. It automates the generation of localized social ad creatives by ingesting a campaign brief, validating requirements, and orchestrating Generative AI to produce assets at scale.

**Key Features:**
* **Smart Ingestion:** Strongly typed validation of campaign briefs using Pydantic.
* [cite_start]**Asset Intelligence:** Checks for existing assets (DAM/Local) before incurring GenAI costs.
* [cite_start]**Multi-Format Support:** Automatically handles aspect ratio mapping (1:1, 16:9, 9:16).
* [cite_start]**Brand Compliance:** Programmatic text overlays with dynamic contrast adjustments.
* **Modular Architecture:** Designed with the Adapter Pattern to easily swap GenAI backends (e.g., OpenAI, Firefly, Pollinations).

## 🚀 How to Run
1.  **Prerequisites:** Python 3.10+
2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Pipeline:**
    ```bash
    python -m src.main --brief brief.json
    ```
4.  **View Output:** Check the `output/` folder for the organized creative assets[cite: 33].

## 🏗 Design Decisions
* **Pydantic for Data Validation:** In an enterprise environment, "garbage in" leads to expensive failures. I used Pydantic to enforce schema validation at the entry point.
* **Factory/Adapter Pattern:** The `ImageGenerator` class is an abstraction. While this POC uses a rapid-prototyping API (Pollinations/OpenAI), the interface allows for a drop-in replacement with **Adobe Firefly Services** for commercial safety without refactoring the business logic.
* **Asset Caching Strategy:** The pipeline prioritizes existing assets in `assets/` over generation. In a production scenario, this would query a DAM (AEM Assets), significantly reducing latency and inference costs.

## 🔮 Enterprise Scalability (Next Steps)
[cite_start]To scale this from a local CLI to a global microservice:
1.  **Async Orchestration:** Move the generation step to a Message Queue (Celery/SQS) to handle high concurrency without blocking.
2.  **Brand Safety Guardrails:** Integrate a VLM (Visual Language Model) to "grade" generated images for logo integrity and policy compliance before they reach the creative team.
3.  **Localization:** Connect the `region` field to a Translation API to automatically localize the `campaign_message`.
