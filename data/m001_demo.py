"""
Pre-loaded real M001 data (Absolute + BWFS) for zero-cost demo mode.
Extracted from actual documents provided 12-Aug-2026.
"""

from app.models import (
    RFQPackage, VendorInfo, PricingLine, CommercialTerms,
    TechnicalParameter, VendorQuote, BidTab, ComplianceStatus
)

# ---------------------------------------------------------------------------
# RFQ Header
# ---------------------------------------------------------------------------
rfq = RFQPackage(
    project_name="Hilcorp Ethane Processing Plant (Keystone C2 Purification)",
    project_number="22510",
    location="Refugio, TX",
    owner="Hilcorp Energy Company",
    engineer_buyer="Crosstrails Engineering",
    rfq_number="22510-RFQ-M001",
    equipment_tag="T-2100",
    equipment_description="Demethanizer Column (Tower)",
    data_sheet_ref="22510-DS-PE012 Rev A (48\" ID × 125'-0\" S/S, ASME VIII Div 1, 450 PSIG @ 200°F / -150°F)",
    bid_tab_rev="Rev 1 (Demo)",
    bid_tab_date="17 June 2026",
    notes="Rev 1: Updated for Absolute Rev 04 (05-Jun-2026) and BWFS Rev 3 (15-Jun-2026). GLEX P26-054 carried forward — no revision received."
)

# ---------------------------------------------------------------------------
# ABSOLUTE ENERGY FIELD (Rev 04)
# ---------------------------------------------------------------------------
absolute_vendor = VendorInfo(
    name="Absolute Energy Field P&S",
    proposal_number="05242026 Rev 04",
    proposal_date="5 June 2026",
    revision="04",
    sales_contact="Ravi Singh, President/CEO",
    phone="832.649.8227",
    email="ravi.singh@absoluteenergyfield.com",
    shop_location="Houston, TX",
    fob="Ex Works (EXW)",
    asme_stamp="U-Stamp + NB Reg",
    notes=None
)

absolute_pricing = [
    PricingLine(item="Base Vessel", description="T-2100 Demethanizer Tower — base vessel as quoted", amount_usd=857056.0, is_optional=False),
    PricingLine(item="Downcomer Piping", description="Downcomers N1, N2, N3, N5, N6, N7, N8, N9 (DS DNCM nozzles)", amount_usd=292944.0, is_optional=False),
    PricingLine(item="Ladders & Platforms", description="Caged ladder + 180° platform — access to level inst & bottom MW", amount_usd=25000.0, is_optional=False),
    PricingLine(item="Field Hydrotest", description="Vertical site hydrotest (water, manlift, air comp by client)", amount_usd=25000.0, is_optional=True, notes="Optional adder Rev 04"),
]

absolute_commercial = CommercialTerms(
    delivery_weeks="38–40 weeks (Ex Works)",
    pricing_validity="4 weeks",
    payment_terms="20% Eng / 40% major comp / 35% internals install / 5% data book Net 30",
    warranty="18 mo from shipment OR 12 mo from startup",
    cancellation_schedule="Not stated",
    taxes="Excluded — buyer responsibility",
    tariff_disclaimer="Not stated",
    storage="Not stated",
    notes="Absolute Rev 04 simplified terms (4 milestones)."
)

# Key technical parameters (subset for demo; full list can be expanded)
absolute_technical = [
    TechnicalParameter(category="GENERAL", parameter="Service", units="—", data_sheet_required="Demethanizer Column (vertical)", vendor_offer="Demethanizer (vertical)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Tower Diameter / Length", units="in × ft", data_sheet_required='48" I.D. × 125\'-0" S/S', vendor_offer='48" ID × 125\'-0" S/S', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Code", units="—", data_sheet_required="ASME Section VIII, Div. 1; U-Stamp YES", vendor_offer="ASME VIII Div 1, U-Stamp, NB Reg", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Design Pressure", units="psig", data_sheet_required="450", vendor_offer="450", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Design Temperature Min/Max", units="°F", data_sheet_required="-150 / 200", vendor_offer="-150 / 200", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Corrosion Allowance", units="in", data_sheet_required="0", vendor_offer="None (0)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS", parameter="Shell", units="—", data_sheet_required="SA-240-304", vendor_offer="SA-240-304", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS", parameter="Heads", units="—", data_sheet_required="SA-240-304", vendor_offer="SA-240-304 (2:1 elliptical)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS", parameter="Skirt / Legs", units="—", data_sheet_required="SA-240-304 (all SS)", vendor_offer="SS skirt with integral base plate", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="ATTACHMENTS", parameter="Pipe Downcomers", units="—", data_sheet_required="YES (for DNCM nozzles N1–N9)", vendor_offer="Included as Option (priced)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="ATTACHMENTS", parameter="Ladders & Platforms", units="—", data_sheet_required="Base: caged ladder + 180° platform", vendor_offer="Included (base scope)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="HYDROTEST", parameter="Hydro Test", units="—", data_sheet_required="Per Code; per DS Note 8 (15 ft liquid head)", vendor_offer="Per ASME (shop); Option for vertical field hydrotest", compliance=ComplianceStatus.OK),
]

absolute_quote = VendorQuote(
    vendor=absolute_vendor,
    pricing_lines=absolute_pricing,
    commercial=absolute_commercial,
    technical=absolute_technical,
    extraction_confidence=0.95,
    needs_review=False
)

# ---------------------------------------------------------------------------
# BWFS INDUSTRIES (Rev 3)
# ---------------------------------------------------------------------------
bwfs_vendor = VendorInfo(
    name="BWFS Industries, LLC",
    proposal_number="BWFS 13954-26 Rev 3",
    proposal_date="15 June 2026",
    revision="3",
    sales_contact="Steve Rice",
    phone="832-554-1364",
    email="srice@bwfsindustries.com",
    shop_location="Houston, TX",
    fob="F.O.B. BWFS Shops",
    asme_stamp="U-Stamp + NB Reg (Appx 46 reserved for nozzle design)",
    notes=None
)

bwfs_pricing = [
    PricingLine(item="Base Vessel", description="T-2100 Demethanizer Tower — base vessel as quoted (48\" ID × 125'-0\" S/S with 24' Flared Skirt)", amount_usd=967680.0, is_optional=False),
    PricingLine(item="Downcomer Piping", description="Downcomers N1, N2, N3, N5, N6, N7, N8, N9", amount_usd=191050.0, is_optional=False),
    PricingLine(item="Ladders & Platforms", description="1 ladder × 32' + 180° platform × 48\" wide (galvanized)", amount_usd=19590.0, is_optional=False),
    PricingLine(item="Fall Arrest Devices", description="1 Fall arrest device(s) (less harnesses)", amount_usd=1250.0, is_optional=False),
]

bwfs_commercial = CommercialTerms(
    delivery_weeks="60 weeks ARO (verbally offered 58 wks)",
    pricing_validity="24 hrs (market volatility); 7 days L&O",
    payment_terms="20% prelim dwgs / 30% shell mat'l / 25% head mat'l / 20% complete / 5% final data Net 30",
    warranty="Earlier of 12 mo after install OR 18 mo after shipment",
    cancellation_schedule="20% / 65% / 85% / 100% (order / mat'l ordered / fab start / shells rolled)",
    taxes="Not stated",
    tariff_disclaimer="Explicit disclaimer; not liable for tariff/exec-order impacts",
    storage="2 wk free; then crane fees + $5/ft²/mo",
    notes="BWFS still front-loads ~75% before completion. Aggressive cancellation. Short validity = material re-pricing risk."
)

bwfs_technical = [
    TechnicalParameter(category="GENERAL", parameter="Service", units="—", data_sheet_required="Demethanizer Column (vertical)", vendor_offer="Demethanizer", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Tower Diameter / Length", units="in × ft", data_sheet_required='48" I.D. × 125\'-0" S/S', vendor_offer='48" ID × 125\'-0" S/S w/ 24\' flared skirt', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Code", units="—", data_sheet_required="ASME Section VIII, Div. 1; U-Stamp YES", vendor_offer="ASME VIII Div 1, U-Stamp, NB Reg", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Design Pressure", units="psig", data_sheet_required="450", vendor_offer="450 (internal); 0 (external)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Design Temperature Min/Max", units="°F", data_sheet_required="-150 / 200", vendor_offer="-150 / 350", compliance=ComplianceStatus.OK, notes="Higher max temp than DS"),
    TechnicalParameter(category="DESIGN DATA", parameter="Corrosion Allowance", units="in", data_sheet_required="0", vendor_offer="0", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS", parameter="Shell", units="—", data_sheet_required="SA-240-304", vendor_offer="SA240-304/304L", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS", parameter="Heads", units="—", data_sheet_required="SA-240-304", vendor_offer="SA240-304/304L", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS", parameter="Skirt / Legs", units="—", data_sheet_required="SA-240-304 (all SS)", vendor_offer="Hybrid: 1.5\" 304SS tip (4'-0\") + 2 × 1.375\" SA516-70N flared", compliance=ComplianceStatus.DEV, notes="CS flared skirt portion — paint required"),
    TechnicalParameter(category="MATERIALS", parameter="Base Plate", units="—", data_sheet_required="SS", vendor_offer="Carbon steel (per paint scope)", compliance=ComplianceStatus.DEV),
    TechnicalParameter(category="ATTACHMENTS", parameter="Pipe Downcomers", units="—", data_sheet_required="YES (for DNCM nozzles N1–N9)", vendor_offer="Included as Option (priced)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="HYDROTEST", parameter="Hydro Test", units="—", data_sheet_required="Per Code; per DS Note 8 (15 ft liquid head)", vendor_offer="Per ASME (shop); designed for field hydrotest (no adder)", compliance=ComplianceStatus.OK),
]

bwfs_quote = VendorQuote(
    vendor=bwfs_vendor,
    pricing_lines=bwfs_pricing,
    commercial=bwfs_commercial,
    technical=bwfs_technical,
    extraction_confidence=0.93,
    needs_review=False
)

# ---------------------------------------------------------------------------
# Assembled Bid Tab for Demo
# ---------------------------------------------------------------------------
demo_bid_tab = BidTab(
    rfq=rfq,
    vendors=[absolute_quote, bwfs_quote],
    apples_to_apples_notes="Vessel + downcomers + base-bid ladders. Excludes optional site hydrotest. BWFS sum also includes 1 fall-arrest device.",
    recommendation=None,
    created_at="2026-06-17",
    last_updated="2026-08-12 (Demo load)"
)
