# Overwatch2_rag

**overwatch2_rag** is a comprehensive solution designed to enhance gameplay analysis and strategy development for Overwatch 2. This project integrates data extraction, semantic analysis, and intelligent recommendations to provide players with actionable insights and improve their in-game performance.

## Table of Contents

- [Project Description](#project-description)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)

## Project Description

**overwatch2_rag** (Overwatch 2 - Research and Analysis Guide) is a tool aimed at players, coaches, and analysts who want to gain a deeper understanding of gameplay data in Overwatch 2. The tool leverages advanced data processing techniques to analyze game stats, player performance, and strategic patterns. Key features include data extraction, semantic text splitting, and personalized recommendations.

## Features

- **Data Extraction**: Extracts detailed gameplay statistics and logs from Overwatch 2.
- **Semantic Analysis**: Applies semantic text splitting to analyze game reports, player communications, and match summaries.
- **Intelligent Recommendations**: Provides actionable insights and recommendations based on gameplay analysis.
- **Customizable Configurations**: Allows users to adjust settings to tailor the analysis to specific needs or preferences.
- **Interactive Interface**: Provides a user-friendly interface for easy access to features and insights.

## Installation

To get started with **overwatch2_rag**, follow these steps to set up the project on your local machine:

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/sasaxopajic/overwatch2_rag.git
   ```
2. **Navigate to the Project Directory**:
   ```bash
   cd overwatch2_rag
   ```
3. **Create and Activate a Virtual Environment**(recommended):
   ```bash
   python -m venv ./.venv
   .\.venv\Scripts\activate.ps1  # Windows
   ```
4. **Install dependencies**(recommended):
   ```bash
   pip freeze > requirements.txt
   ```
5. Import your **API KEY** into the .env file:
   ```bash
   OPENAI_API_KEY=XXXXXXXXXX
   ````

## Usage

   To use overwatch2_rag, follow these steps:

   ```bash
   streamlit run overwatch2.py
   ```
   And you're now all set up! Heroes never die! 
