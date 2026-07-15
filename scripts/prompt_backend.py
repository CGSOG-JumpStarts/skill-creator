#!/usr/bin/env python3
"""Prompt runner backends for skill-creator automation.

Supports Claude CLI, GitHub Copilot CLI, and custom wrapper commands such as
SDK-backed scripts. The default remains Claude for backward compatibility.
"""

from __future__ import annotations

import os
import shlex
import shutil
import subprocess
from pathlib import Path


SUPPORTED_BACKENDS = ("claude", "copilot", "custom")


def _normalize_backend(backend: str | None) -> str:
    value = (backend or os.environ.get("SKILL_CREATOR_PROMPT_BACKEND") or "claude").strip().lower()
    if value not in SUPPORTED_BACKENDS:
        raise ValueError(
            f"Unsupported prompt backend '{value}'. Expected one of: {', '.join(SUPPORTED_BACKENDS)}"
        )
    return value


def _split_command(command: str) -> list[str]:
    parts = shlex.split(command, posix=os.name != "nt")
    if not parts:
        raise ValueError("Prompt runner command is empty")
    return parts


def _resolve_copilot_executable(env: dict[str, str]) -> str:
    explicit = env.get("COPILOT_CLI_PATH")
    if explicit:
        candidate = Path(explicit)
        if not candidate.exists():
            raise ValueError(f"COPILOT_CLI_PATH does not exist: {explicit}")
        return str(candidate)

    for command_name in ("copilot", "copilot.cmd"):
        resolved = shutil.which(command_name)
        if resolved:
            return resolved

    if os.name == "nt":
        appdata = env.get("APPDATA")
        if appdata:
            candidate = Path(appdata) / "npm" / "copilot.cmd"
            if candidate.exists():
                return str(candidate)

    return "copilot"


def resolve_prompt_command(
    backend: str | None,
    model: str | None,
    output_format: str,
    prompt_arg: str | None = None,
    custom_command: str | None = None,
) -> tuple[list[str], dict[str, str]]:
    """Build the subprocess command and environment for a prompt backend."""
    resolved_backend = _normalize_backend(backend)
    env = dict(os.environ)

    if resolved_backend == "claude":
        env.pop("CLAUDECODE", None)
        cmd = ["claude"]
        if prompt_arg is not None:
            cmd.extend(["-p", prompt_arg])
        else:
            cmd.append("-p")
        cmd.extend(["--output-format", output_format])
        if output_format == "stream-json":
            cmd.extend(["--verbose", "--include-partial-messages"])
        if model:
            cmd.extend(["--model", model])
        return cmd, env

    if resolved_backend == "copilot":
        env["COPILOT_CLI"] = "1"
        cmd = [_resolve_copilot_executable(env)]
        if prompt_arg is not None:
            cmd.extend(["-p", prompt_arg])
        else:
            cmd.append("-p")
        cmd.append("--allow-all-paths")
        if model:
            cmd.extend(["--model", model])
        if output_format == "stream-json":
            cmd.extend(["--output-format", "json"])
        else:
            cmd.extend(["--output-format", "text"])
        return cmd, env

    resolved_command = custom_command or os.environ.get("SKILL_CREATOR_PROMPT_COMMAND")
    if not resolved_command:
        raise ValueError(
            "Prompt backend 'custom' requires SKILL_CREATOR_PROMPT_COMMAND to point to a wrapper command"
        )

    cmd = _split_command(resolved_command)
    if prompt_arg is not None:
        cmd.append(prompt_arg)

    env["SKILL_CREATOR_OUTPUT_FORMAT"] = output_format
    if model:
        env["SKILL_CREATOR_MODEL"] = model
    return cmd, env


def run_prompt(
    *,
    prompt: str,
    backend: str | None,
    model: str | None,
    output_format: str,
    cwd: Path | None = None,
    timeout: int = 300,
    prompt_as_arg: bool = False,
    custom_command: str | None = None,
) -> subprocess.CompletedProcess[str]:
    """Run a prompt through the configured backend and return the subprocess result."""
    prompt_arg = prompt if prompt_as_arg else None
    cmd, env = resolve_prompt_command(
        backend,
        model,
        output_format,
        prompt_arg=prompt_arg,
        custom_command=custom_command,
    )

    return subprocess.run(
        cmd,
        input=None if prompt_as_arg else prompt,
        capture_output=True,
        text=True,
        env=env,
        cwd=str(cwd) if cwd else None,
        timeout=timeout,
    )