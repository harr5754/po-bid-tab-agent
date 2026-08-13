"""
PO Bid Tab Agent — Streamlit App
================================
Upload RFQ + technical docs + bidder proposals → structured Bid Tab (online + Excel).
Claude is the default extraction engine. Demo mode works with zero API cost.
"""

import streamlit as st
import pandas as pd
from datetime import datetime
from io import BytesIO
import sys
from pathlib import Path

# Allow imports from parent
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from app.models import BidTab, VendorQuote, ComplianceStatus, calculate_apples_to_apples
from app.excel_export import build_classic_excel
from data.m001_demo import demo_bid_tab

# ---------------------------------------------------------------------------
# Page config
# ---------------------------------------------------------------------------
st.set_page_config(
    page_title="Aegentik Bid Tab Agent",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------
if "bid_tab" not in st.session_state:
    st.session_state.bid_tab = demo_bid_tab
if "mode" not in st.session_state:
    st.session_state.mode = "Demo (M001)"
if "view_style" not in st.session_state:
    st.session_state.view_style = "Classic"
if "review_mode" not in st.session_state:
    st.session_state.review_mode = False
if "show_welcome" not in st.session_state:
    st.session_state.show_welcome = True

# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### Aegentik")
    st.title("Bid Tab Agent")
    st.caption("Built for real EPC RFQs")

    st.divider()
    st.subheader("Mode")
    mode = st.radio(
        "Select mode",
        ["Demo (M001 — zero cost)", "Live RFQ (Claude extraction)"],
        index=0,
        label_visibility="collapsed"
    )
    st.session_state.mode = mode

    st.divider()
    st.subheader("View Style")
    view = st.radio(
        "Bid Tab style",
        ["Classic (2-sheet style)", "Modern (multi-tab)"],
        index=0,
        label_visibility="collapsed"
    )
    st.session_state.view_style = "Classic" if "Classic" in view else "Modern"

    st.divider()
    st.subheader("Claude API (optional)")
    api_key = st.text_input(
        "Anthropic API Key",
        type="password",
        help="Company Claude key. Leave blank for Demo mode.",
        placeholder="sk-ant-..."
    )
    if api_key:
        st.success("Key loaded (not stored)")
    else:
        st.info("Demo mode active — no key needed")

    st.divider()
    if st.button("Show Welcome Screen"):
        st.session_state.show_welcome = True
    st.caption("Max 5 bidders · Manual review available")
    st.caption("aegentik.ai")

# ---------------------------------------------------------------------------
# Welcome / Landing Screen
# ---------------------------------------------------------------------------
if st.session_state.show_welcome:
    st.markdown("## Aegentik Bid Tab Agent")
    st.markdown("#### Turn RFQ packages + bidder proposals into a structured Bid Tab in minutes")
    st.write("")

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.success("**Demo ready** — Pre-loaded with real M001 data (Absolute + BWFS)\n\nNo API key required for this demo.")

        st.markdown("#### What you can do")
        st.markdown("""
        - View the online Bid Tab (Commercial + Technical)
        - Review & correct any extracted values
        - Download Excel in **Classic** or **Modern** format
        - Upload a new RFQ package when ready (Claude extraction)
        """)

        st.write("")
        if st.button("Enter Demo →", type="primary", use_container_width=True):
            st.session_state.show_welcome = False
            st.rerun()

        st.write("")
        st.caption("Powered by Aegentik · For Crosstrails Engineering demo")
    st.stop()

# ---------------------------------------------------------------------------
# Header (after welcome)
# ---------------------------------------------------------------------------
st.title("Aegentik Bid Tab Agent")
rfq = st.session_state.bid_tab.rfq
st.markdown(f"**{rfq.project_name}** · {rfq.rfq_number} · {rfq.equipment_tag}")

# ---------------------------------------------------------------------------
# Tabs
# ---------------------------------------------------------------------------
tab_demo, tab_upload, tab_review, tab_bidtab, tab_download = st.tabs([
    "📊 Current Bid Tab",
    "📤 Upload New RFQ",
    "✏️ Review & Correct",
    "🔍 Detailed Comparison",
    "⬇️ Download Excel"
])

# ===========================================================================
# TAB 1: Current Bid Tab (always shows current state)
# ===========================================================================
with tab_demo:
    bt = st.session_state.bid_tab

    st.subheader("Commercial Summary")
    st.markdown(f"**Project:** {bt.rfq.project_name}  \n"
                f"**Location:** {bt.rfq.location}  \n"
                f"**Owner:** {bt.rfq.owner}  \n"
                f"**Engineer / Buyer:** {bt.rfq.engineer_buyer}  \n"
                f"**Data Sheet:** {bt.rfq.data_sheet_ref}  \n"
                f"**Bid Tab:** {bt.rfq.bid_tab_rev} · {bt.rfq.bid_tab_date}")

    # Vendor header row
    cols = st.columns(len(bt.vendors) + 1)
    cols[0].markdown("**Field**")
    for i, v in enumerate(bt.vendors):
        cols[i+1].markdown(f"**{v.vendor.name}**")

    # Key commercial rows
    rows = [
        ("Proposal / Quote #", [v.vendor.proposal_number for v in bt.vendors]),
        ("Proposal Date", [v.vendor.proposal_date or "—" for v in bt.vendors]),
        ("Sales Contact", [v.vendor.sales_contact or "—" for v in bt.vendors]),
        ("Shop / FOB", [f"{v.vendor.shop_location or ''} ({v.vendor.fob or ''})" for v in bt.vendors]),
        ("ASME / NB Stamp", [v.vendor.asme_stamp or "—" for v in bt.vendors]),
    ]
    for label, values in rows:
        cols = st.columns(len(bt.vendors) + 1)
        cols[0].write(label)
        for i, val in enumerate(values):
            cols[i+1].write(val)

    st.divider()
    st.subheader("Pricing Summary (USD)")

    # Build pricing comparison table
    price_data = []
    for v in bt.vendors:
        base = next((p.amount_usd for p in v.pricing_lines if "Base Vessel" in p.item or "base vessel" in p.description.lower()), 0)
        down = next((p.amount_usd for p in v.pricing_lines if "Downcomer" in p.item), 0)
        ladd = next((p.amount_usd for p in v.pricing_lines if "Ladder" in p.item or "Platform" in p.item), 0)
        fall = next((p.amount_usd for p in v.pricing_lines if "Fall Arrest" in p.item), 0)
        total = calculate_apples_to_apples(v)
        price_data.append({
            "Vendor": v.vendor.name,
            "Base Vessel": f"${base:,.0f}",
            "Downcomers": f"${down:,.0f}",
            "Ladders/Platforms": f"${ladd:,.0f}",
            "Fall Arrest": f"${fall:,.0f}" if fall else "—",
            "Apples-to-Apples Total": f"**${total:,.0f}**"
        })

    st.dataframe(pd.DataFrame(price_data), use_container_width=True, hide_index=True)
    st.caption(bt.apples_to_apples_notes or "")

    st.divider()
    st.subheader("Commercial Terms Comparison")

    term_rows = [
        ("Delivery", [v.commercial.delivery_weeks or "—" for v in bt.vendors]),
        ("Pricing Validity", [v.commercial.pricing_validity or "—" for v in bt.vendors]),
        ("Payment Terms", [v.commercial.payment_terms or "—" for v in bt.vendors]),
        ("Warranty", [v.commercial.warranty or "—" for v in bt.vendors]),
        ("Cancellation", [v.commercial.cancellation_schedule or "—" for v in bt.vendors]),
        ("Tariff / Govt Action", [v.commercial.tariff_disclaimer or "—" for v in bt.vendors]),
        ("Storage", [v.commercial.storage or "—" for v in bt.vendors]),
    ]
    for label, values in term_rows:
        cols = st.columns(len(bt.vendors) + 1)
        cols[0].markdown(f"**{label}**")
        for i, val in enumerate(values):
            cols[i+1].write(val)

# ===========================================================================
# TAB 2: Upload New RFQ
# ===========================================================================
with tab_upload:
    st.subheader("Upload New RFQ Package")
    st.info("Demo mode is active. Upload is enabled for structure testing. Full Claude extraction requires an API key.")

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**RFQ / Technical Package**")
        rfq_files = st.file_uploader(
            "RFQ letter, Data Sheet, Design Basis, ITP, VDRL, Owner T&Cs",
            type=["pdf", "docx", "xlsx", "doc"],
            accept_multiple_files=True,
            key="rfq_upload"
        )
    with col2:
        st.markdown("**Bidder Proposals (max 5)**")
        bid_files = st.file_uploader(
            "Vendor quotes / proposals",
            type=["pdf", "docx", "xlsx", "doc"],
            accept_multiple_files=True,
            key="bid_upload"
        )

    if st.button("Run Extraction (Claude)", type="primary", disabled=not api_key):
        st.warning("Claude extraction pipeline will be fully wired in the next iteration. For now the Demo data is loaded.")
        st.session_state.bid_tab = demo_bid_tab

    if rfq_files or bid_files:
        st.success(f"Received {len(rfq_files or [])} RFQ files and {len(bid_files or [])} bidder files.")
        st.caption("Files are ready. Extraction will use the company Claude key when provided.")

# ===========================================================================
# TAB 3: Review & Correct
# ===========================================================================
with tab_review:
    st.subheader("Manual Review & Override")
    st.markdown("Correct any extraction errors before generating the final Bid Tab. Changes are kept in session.")

    bt = st.session_state.bid_tab
    for idx, vendor in enumerate(bt.vendors):
        with st.expander(f"{vendor.vendor.name}  ·  Confidence {vendor.extraction_confidence or 0:.0%}", expanded=False):
            st.markdown("**Vendor Info**")
            c1, c2 = st.columns(2)
            with c1:
                vendor.vendor.proposal_number = st.text_input("Proposal #", vendor.vendor.proposal_number, key=f"pn_{idx}")
                vendor.vendor.proposal_date = st.text_input("Date", vendor.vendor.proposal_date or "", key=f"pd_{idx}")
                vendor.vendor.sales_contact = st.text_input("Contact", vendor.vendor.sales_contact or "", key=f"sc_{idx}")
            with c2:
                vendor.vendor.phone = st.text_input("Phone", vendor.vendor.phone or "", key=f"ph_{idx}")
                vendor.vendor.email = st.text_input("Email", vendor.vendor.email or "", key=f"em_{idx}")
                vendor.vendor.fob = st.text_input("FOB", vendor.vendor.fob or "", key=f"fob_{idx}")

            st.markdown("**Commercial Terms**")
            vendor.commercial.delivery_weeks = st.text_input("Delivery", vendor.commercial.delivery_weeks or "", key=f"del_{idx}")
            vendor.commercial.pricing_validity = st.text_input("Validity", vendor.commercial.pricing_validity or "", key=f"val_{idx}")
            vendor.commercial.payment_terms = st.text_area("Payment Terms", vendor.commercial.payment_terms or "", key=f"pay_{idx}", height=70)
            vendor.commercial.warranty = st.text_input("Warranty", vendor.commercial.warranty or "", key=f"war_{idx}")

            st.markdown("**Pricing Lines**")
            for p_idx, line in enumerate(vendor.pricing_lines):
                cols = st.columns([3, 2, 1])
                line.description = cols[0].text_input("Desc", line.description, key=f"desc_{idx}_{p_idx}")
                line.amount_usd = cols[1].number_input("Amount", value=float(line.amount_usd), key=f"amt_{idx}_{p_idx}", step=1000.0)
                line.is_optional = cols[2].checkbox("Optional", value=line.is_optional, key=f"opt_{idx}_{p_idx}")

            vendor.needs_review = st.checkbox("Flag for further review", value=vendor.needs_review, key=f"flag_{idx}")
            vendor.review_notes = st.text_area("Review notes", vendor.review_notes or "", key=f"notes_{idx}")

    if st.button("Save Corrections", type="primary"):
        st.success("Corrections saved in session. Go to Download or Detailed Comparison to see updates.")

# ===========================================================================
# TAB 4: Detailed Comparison (Modern view)
# ===========================================================================
with tab_bidtab:
    st.subheader("Technical Compliance Comparison")
    bt = st.session_state.bid_tab

    # Collect all unique parameters
    all_params = []
    for v in bt.vendors:
        for t in v.technical:
            key = (t.category, t.parameter)
            if key not in [(p.category, p.parameter) for p in all_params]:
                all_params.append(t)

    if not all_params:
        st.info("No technical parameters loaded yet.")
    else:
        # Build comparison table
        rows = []
        for param in all_params:
            row = {
                "Category": param.category,
                "Parameter": param.parameter,
                "Data Sheet Required": param.data_sheet_required,
            }
            for v in bt.vendors:
                match = next((t for t in v.technical if t.parameter == param.parameter and t.category == param.category), None)
                if match:
                    status = match.compliance.value
                    color = {"OK": "🟢", "Dev": "🟠", "Clarify": "🟡", "Not Addressed": "⚪"}.get(status, "")
                    row[v.vendor.name] = f"{color} {match.vendor_offer}"
                else:
                    row[v.vendor.name] = "—"
            rows.append(row)

        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.caption("🟢 OK  ·  🟠 Deviation  ·  🟡 Clarify  ·  ⚪ Not Addressed")

# ===========================================================================
# TAB 5: Download
# ===========================================================================
with tab_download:
    st.subheader("Download Bid Tab")
    bt = st.session_state.bid_tab

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Classic Format")
        st.caption("Matches the professional 2-sheet Bid Tab layout you already use (Commercial + Technical)")
        if st.button("Generate Classic Excel", key="classic"):
            excel_bytes = build_classic_excel(bt)
            st.download_button(
                label="⬇️ Download Classic Excel",
                data=excel_bytes,
                file_name=f"BidTab_{bt.rfq.rfq_number}_Classic_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            st.success("Classic Excel ready — formatted to closely match your existing Bid Tab style.")

    with col2:
        st.markdown("### Modern Format")
        st.caption("Multi-sheet with Summary, Pricing Detail, Terms, Technical, Risk Flags")
        if st.button("Generate Modern Excel", key="modern"):
            output = BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                # Summary
                summary = []
                for v in bt.vendors:
                    summary.append({
                        "Vendor": v.vendor.name,
                        "Proposal": v.vendor.proposal_number,
                        "Apples-to-Apples Total": calculate_apples_to_apples(v),
                        "Delivery (weeks)": v.commercial.delivery_weeks,
                        "Validity": v.commercial.pricing_validity,
                        "Needs Review": v.needs_review
                    })
                pd.DataFrame(summary).to_excel(writer, sheet_name="Summary", index=False)

                # Full pricing
                all_prices = []
                for v in bt.vendors:
                    for p in v.pricing_lines:
                        all_prices.append({
                            "Vendor": v.vendor.name,
                            "Item": p.item,
                            "Description": p.description,
                            "Amount USD": p.amount_usd,
                            "Optional": p.is_optional,
                            "Notes": p.notes or ""
                        })
                pd.DataFrame(all_prices).to_excel(writer, sheet_name="Pricing Detail", index=False)

                # Terms
                terms = []
                for v in bt.vendors:
                    terms.append({
                        "Vendor": v.vendor.name,
                        "Delivery": v.commercial.delivery_weeks,
                        "Validity": v.commercial.pricing_validity,
                        "Payment Terms": v.commercial.payment_terms,
                        "Warranty": v.commercial.warranty,
                        "Cancellation": v.commercial.cancellation_schedule,
                        "Tariff Disclaimer": v.commercial.tariff_disclaimer,
                        "Storage": v.commercial.storage,
                        "Notes": v.commercial.notes or ""
                    })
                pd.DataFrame(terms).to_excel(writer, sheet_name="Commercial Terms", index=False)

                # Technical
                tech_rows = []
                for v in bt.vendors:
                    for t in v.technical:
                        tech_rows.append({
                            "Vendor": v.vendor.name,
                            "Category": t.category,
                            "Parameter": t.parameter,
                            "Data Sheet Required": t.data_sheet_required,
                            "Vendor Offer": t.vendor_offer,
                            "Compliance": t.compliance.value,
                            "Notes": t.notes or ""
                        })
                if tech_rows:
                    pd.DataFrame(tech_rows).to_excel(writer, sheet_name="Technical Compliance", index=False)

            st.download_button(
                label="⬇️ Download Modern Excel",
                data=output.getvalue(),
                file_name=f"BidTab_{bt.rfq.rfq_number}_Modern_{datetime.now().strftime('%Y%m%d')}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

    st.divider()
    st.caption(f"Generated from session data · Last updated: {bt.last_updated}")
