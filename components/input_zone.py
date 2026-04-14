"""
components/input_zone.py -- File upload, framework selector & client profile
AI Banking Compliance Auditor

Renders the input area that visually merges with the hero card above:
  - Left column:  PDF file uploader
  - Right column: audit framework multiselect
  - Signature verification checkbox
  - Collapsible client profile section
  - Center:       "Run AI Audit" action button

Also injects the JS that applies the .esg-input-zone class to the
Streamlit container so the card border is continuous.
"""

import streamlit as st

import config
from helpers import load_js


def render_input_zone() -> tuple:
    """Render the input controls and return user selections.

    Returns:
        (uploaded_file, standards, signature_match, client_profile, run_audit)
    """
    load_js("scripts/input_zone.js")

    # ── Two-column layout: uploader | framework selector ──────────
    col_up, col_std = st.columns([1, 1], gap="medium")

    with col_up:
        st.markdown(
            '<span class="slabel">Document Upload</span>',
            unsafe_allow_html=True,
        )
        uploaded_file = st.file_uploader(
            "Upload PDF",
            type="pdf",
            label_visibility="collapsed",
        )

    with col_std:
        st.markdown(
            '<span class="slabel">Audit Framework</span>',
            unsafe_allow_html=True,
        )
        standards = st.multiselect(
            "Standards",
            config.FRAMEWORK_OPTIONS,
            default=config.DEFAULT_FRAMEWORK,
            label_visibility="collapsed",
        )

    # ── Signature verification ────────────────────────────────────
    signature_match = st.checkbox(
        "\u2705 Signature verified against specimen",
        value=True,
        help="Uncheck if the client\u2019s signature does not match records.",
    )

    # ── Client profile (optional) ─────────────────────────────────
    client_profile: dict = {}
    with st.expander("Client Profile (Optional)"):
        p1, p2, p3 = st.columns(3)
        with p1:
            min_amt = st.number_input(
                "Usual Min Amount", min_value=0.0, value=0.0, step=100.0
            )
        with p2:
            max_amt = st.number_input(
                "Usual Max Amount", min_value=0.0, value=0.0, step=100.0
            )
        with p3:
            avg_amt = st.number_input(
                "Average Amount", min_value=0.0, value=0.0, step=100.0
            )

        threshold = st.number_input(
            "High Amount Threshold",
            min_value=0.0,
            value=10000.0,
            step=1000.0,
        )

        countries_str = st.text_input(
            "Typical Countries",
            placeholder="e.g. uk, usa, germany",
            help="Comma-separated list of countries the client normally transacts with.",
        )
        recipients_str = st.text_input(
            "Usual Recipients",
            placeholder="e.g. acme corp, globex inc",
            help="Comma-separated list of the client\u2019s usual payment recipients.",
        )

        if min_amt > 0:
            client_profile["usual_amount_min"] = min_amt
        if max_amt > 0:
            client_profile["usual_amount_max"] = max_amt
        if avg_amt > 0:
            client_profile["average_amount"] = avg_amt
        client_profile["high_amount_threshold"] = threshold
        if countries_str.strip():
            client_profile["typical_countries"] = [
                c.strip() for c in countries_str.split(",") if c.strip()
            ]
        if recipients_str.strip():
            client_profile["usual_recipients"] = [
                r.strip() for r in recipients_str.split(",") if r.strip()
            ]

    # ── Centred action button ─────────────────────────────────────
    _, btn_col, _ = st.columns([1, 1, 1])
    with btn_col:
        run_audit = st.button(
            "\u26a1 Run AI Audit", type="primary", use_container_width=True
        )

    st.markdown("<hr>", unsafe_allow_html=True)

    return uploaded_file, standards, signature_match, client_profile, run_audit
