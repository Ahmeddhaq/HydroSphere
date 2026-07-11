"""
llm.py — Shared LLM with automatic Groq fallback.

Primary:  Puter AI  (gpt-5.4-nano via OpenAI-compatible API)
Fallback: Groq      (llama-3.3-70b-versatile)

Usage in any agent:
    from llm import get_llm
    llm = get_llm()
"""

import os
import logging
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

logger = logging.getLogger(__name__)


def get_llm():
    """
    Returns a working LLM instance.
    Tries Puter AI first; if the key is missing or a call fails at import
    time, falls back to Groq automatically.
    """
    puter_key = os.getenv("PUTER_API_KEY")
    groq_key  = os.getenv("GROQ_API_KEY")

    if puter_key:
        try:
            from langchain_openai import ChatOpenAI
            primary = ChatOpenAI(
                base_url="https://api.puter.com/puterai/openai/v1/",
                api_key=puter_key,
                model="gpt-5.4-nano",
            )
            logger.info("LLM: using Puter AI (primary)")
            return primary
        except Exception as e:
            logger.warning(f"Puter AI unavailable ({e}), switching to Groq fallback.")

    # ── Groq fallback ──────────────────────────────────────────────────────────
    if not groq_key:
        raise EnvironmentError(
            "Neither PUTER_API_KEY nor GROQ_API_KEY is set. "
            "Add at least one to your .env file."
        )

    
    fallback = ChatGroq(
        api_key=groq_key,
        model="openai/gpt-oss-120b",   # fast, capable, free-tier friendly
        temperature=0.2,
    )
    logger.info("LLM: using Groq (fallback)")
    return fallback


def get_llm_with_fallback():
    """
    Returns a LangChain Runnable that tries the primary LLM and automatically
    falls back to Groq on any API / rate-limit error at call time (not just
    at startup).

    Use this when you want runtime retry, not just startup detection.
    """
    from langchain_core.runnables import RunnableLambda
    from langchain_openai import ChatOpenAI
    from langchain_groq import ChatGroq

    puter_key = os.getenv("PUTER_API_KEY")
    groq_key  = os.getenv("GROQ_API_KEY")

    primary = ChatOpenAI(
        base_url="https://api.puter.com/puterai/openai/v1/",
        api_key=puter_key or "dummy",
        model="gpt-5.4-nano",
    ) if puter_key else None

    if not groq_key:
        if primary:
            return primary
        raise EnvironmentError("No API keys configured.")

    fallback_llm = ChatGroq(
        api_key=groq_key,
        model="llama-3.3-70b-versatile",
        temperature=0.2,
    )

    if not primary:
        return fallback_llm

    # Wrap: call primary, catch errors, re-route to Groq
    def _invoke_with_fallback(messages):
        try:
            return primary.invoke(messages)
        except Exception as e:
            logger.warning(f"Primary LLM failed ({type(e).__name__}: {e}). Using Groq fallback.")
            return fallback_llm.invoke(messages)

    return RunnableLambda(_invoke_with_fallback)
