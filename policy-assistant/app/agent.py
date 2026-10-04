# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import subprocess
from dotenv import load_dotenv
from google.adk.agents import Agent, LlmAgent
from google.adk.apps import App
from google.adk.models import Gemini
from google.genai import types
from google.oauth2.credentials import Credentials

from app.tools import check_expense_limit

load_dotenv()

MODEL = "gemini-3.8-flash"


def _get_client_kwargs() -> dict:
    kwargs = {}
    try:
        token = subprocess.check_output(
            ["gcloud", "auth", "print-access-token"], timeout=5
        ).decode().strip()
        if token:
            kwargs["credentials"] = Credentials(token=token)
    except Exception:
        pass
    return kwargs


root_agent = LlmAgent(
    # Keep in sync with agents-cli-manifest.yaml: agents-cli derives this name
    # from the project `name:` recorded there, and telemetry reports it as
    # gen_ai.agent.name. Renaming the agent only here makes the two disagree,
    # and anything selecting traces by name stops finding this agent's.
    name="policy_assistant",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
        client_kwargs=_get_client_kwargs(),
    ),
    instruction=(
        "You are a helpful policy assistant designed to provide accurate policy and expense guidance. "
        "Always consult the check_expense_limit tool before answering questions about expenses or allowances."
    ),
    tools=[check_expense_limit],
)

app = App(
    root_agent=root_agent,
    name="app",
)
