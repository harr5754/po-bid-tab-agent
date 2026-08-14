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
    # GENERAL
    TechnicalParameter(category="GENERAL", parameter="Service", units="—", data_sheet_required="Demethanizer Column (vertical)", vendor_offer="Demethanizer (vertical)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Tower Diameter / Length", units="in × ft", data_sheet_required='48" I.D. × 125\'-0" S/S', vendor_offer='48" ID × 125\'-0" S/S', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Code", units="—", data_sheet_required="ASME Section VIII, Div. 1; U-Stamp YES", vendor_offer="ASME VIII Div 1, U-Stamp, NB Reg", compliance=ComplianceStatus.OK),
    # DESIGN DATA
    TechnicalParameter(category="DESIGN DATA", parameter="Design Pressure", units="psig", data_sheet_required="450", vendor_offer="450", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Design Temperature Min/Max", units="°F", data_sheet_required="-150 / 200", vendor_offer="-150 / 200", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Corrosion Allowance", units="in", data_sheet_required="0", vendor_offer="None (0)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Joint Efficiency", units="—", data_sheet_required="100%", vendor_offer="Per ASME (RT-1 implied)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Radiography", units="—", data_sheet_required="Per Code (RT-1 implied for 100% E)", vendor_offer="Per ASME VIII Div 1", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Stress Relief / PWHT", units="—", data_sheet_required="Per Code", vendor_offer="Per ASME VIII Div 1", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Impact Test", units="—", data_sheet_required="Per Code (filler material to -320°F if required)", vendor_offer="Per ASME VIII Div 1", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Hydro Test", units="—", data_sheet_required="Per Code; per DS Note 8 (15 ft liquid head)", vendor_offer="Per ASME (shop); Option for vertical field hydrotest", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Wind / Seismic", units="—", data_sheet_required="Note 7 (per Design Basis §2.0)", vendor_offer="Per ASME calcs", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Maximum Allowable Deflection", units="in/100 ft", data_sheet_required="8 in per 100 ft", vendor_offer="Per ASME calc", compliance=ComplianceStatus.OK),
    # MATERIALS
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Shell", units="—", data_sheet_required="SA-240-304", vendor_offer="SA-240-304", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Heads", units="—", data_sheet_required="SA-240-304", vendor_offer="SA-240-304 (2:1 elliptical)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Skirt / Legs", units="—", data_sheet_required="SA-240-304 (all SS)", vendor_offer="SS skirt with integral base plate", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Base Plate", units="—", data_sheet_required="SS", vendor_offer="SS (integral to skirt)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Nozzles", units="—", data_sheet_required="SA-312-TP304", vendor_offer="SA-182-F304", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Flanges", units="—", data_sheet_required="SA-182-F304", vendor_offer="SA-182-F304", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Pipe (downcomers)", units="—", data_sheet_required="SA-312-TP304", vendor_offer="B31.3 SS piping", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Gaskets", units="—", data_sheet_required="Spiral wound 0.125\" with appropriate filler", vendor_offer="SS304 spiral wound, graphite filler, CS outer ring", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="External Surface Prep", units="—", data_sheet_required="Per 22510-SP-ME003", vendor_offer="Pickle & passivate all welds & HAZ int & ext", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Paint", units="—", data_sheet_required="NOT REQUIRED (all-SS)", vendor_offer="None (pickling/passivation only)", compliance=ComplianceStatus.OK),
    # ATTACHMENTS
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Demister (mesh pad)", units="—", data_sheet_required="YES (12\" 304SS, 9#)", vendor_offer="Installation only (free issue mat'l)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Demister Supports", units="—", data_sheet_required="YES", vendor_offer="Plate parts & hardware for install", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Pipe Downcomers", units="—", data_sheet_required="YES (for DNCM nozzles N1–N9)", vendor_offer="Included as Option (priced)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Pipe Support / Guide Clips", units="—", data_sheet_required="YES", vendor_offer="Included", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Lift Lugs / Trunnions", units="—", data_sheet_required="YES (lift lugs)", vendor_offer="(2) Lift Lugs + (1) Tail Lug", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Insulation Supports / Rings", units="—", data_sheet_required="YES (rings only — insulation by others)", vendor_offer="Rings only (no insulation)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Tailing Lugs", units="—", data_sheet_required="YES", vendor_offer="(1) Tail Lug", compliance=ComplianceStatus.OK),
    # NOZZLE SCHEDULE (key ones)
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N1 Vapor Outlet", units="—", data_sheet_required='1 × 8" 300# RFWN, DNCM', vendor_offer='1 × 8" 300# RFWN, DNCM', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N2 Reflux", units="—", data_sheet_required='1 × 4" 300# RFWN, DNCM W/baffle', vendor_offer='1 × 4" 300# RFWN, DNCM W/baffle', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N3 Feed", units="—", data_sheet_required='1 × 8" 300# RFWN, DNCM W/baffle', vendor_offer='1 × 8" 300# RFWN, DNCM W/baffle', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N4 Liquid Outlet", units="—", data_sheet_required='1 × 8" 300# RFWN W/VB (vortex breaker)', vendor_offer='1 × 8" 300# RFWN W/VB (vortex breaker)', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N5 Side Draw", units="—", data_sheet_required='1 × 16" 300# RFWN, DNCM', vendor_offer='1 × 16" 300# RFWN, DNCM', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="MW1 Manway (Fill)", units="—", data_sheet_required='4 × 18" 300# RFWN W/B&D (blind + davit)', vendor_offer='4 × 18" 300# RFWN W/B&D (blind + davit)', compliance=ComplianceStatus.OK),
    # INTERNALS
    TechnicalParameter(category="INTERNALS", parameter="All Internals", units="—", data_sheet_required="Free issue by client — installed by Fabricator", vendor_offer="Included", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="INTERNALS", parameter="Chimney Trays", units="—", data_sheet_required="Fully welded", vendor_offer="Included", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="INTERNALS", parameter="Support Rings", units="—", data_sheet_required="Installed by Fabricator", vendor_offer="Included", compliance=ComplianceStatus.OK),
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
    # GENERAL
    TechnicalParameter(category="GENERAL", parameter="Service", units="—", data_sheet_required="Demethanizer Column (vertical)", vendor_offer="Demethanizer", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Tower Diameter / Length", units="in × ft", data_sheet_required='48" I.D. × 125\'-0" S/S', vendor_offer='48" ID × 125\'-0" S/S w/ 24\' flared skirt', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="GENERAL", parameter="Code", units="—", data_sheet_required="ASME Section VIII, Div. 1; U-Stamp YES", vendor_offer="ASME VIII Div 1, U-Stamp, NB Reg", compliance=ComplianceStatus.OK),
    # DESIGN DATA
    TechnicalParameter(category="DESIGN DATA", parameter="Design Pressure", units="psig", data_sheet_required="450", vendor_offer="450 (internal); 0 (external)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Design Temperature Min/Max", units="°F", data_sheet_required="-150 / 200", vendor_offer="-150 / 350", compliance=ComplianceStatus.OK, notes="Higher max temp than DS"),
    TechnicalParameter(category="DESIGN DATA", parameter="Corrosion Allowance", units="in", data_sheet_required="0", vendor_offer="0", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Joint Efficiency", units="—", data_sheet_required="100%", vendor_offer="RT-1 (100%)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Radiography", units="—", data_sheet_required="Per Code (RT-1 implied for 100% E)", vendor_offer="RT-1", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Stress Relief / PWHT", units="—", data_sheet_required="Per Code", vendor_offer="Not included", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Impact Test", units="—", data_sheet_required="Per Code (filler material to -320°F if required)", vendor_offer="Per code (implied)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Hydro Test", units="—", data_sheet_required="Per Code; per DS Note 8 (15 ft liquid head)", vendor_offer="Per ASME (shop); designed for field hydrotest (no adder)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Wind / Seismic", units="—", data_sheet_required="Note 7 (per Design Basis §2.0)", vendor_offer="Per ASME calcs", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="DESIGN DATA", parameter="Maximum Allowable Deflection", units="in/100 ft", data_sheet_required="8 in per 100 ft", vendor_offer="Per ASME calc", compliance=ComplianceStatus.OK),
    # MATERIALS
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Shell", units="—", data_sheet_required="SA-240-304", vendor_offer="SA240-304/304L", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Heads", units="—", data_sheet_required="SA-240-304", vendor_offer="SA240-304/304L", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Skirt / Legs", units="—", data_sheet_required="SA-240-304 (all SS)", vendor_offer="Hybrid: 1.5\" 304SS tip (4\'-0\") + 2 × 1.375\" SA516-70N flared", compliance=ComplianceStatus.DEV, notes="CS flared skirt portion — paint required"),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Base Plate", units="—", data_sheet_required="SS", vendor_offer="Carbon steel (per paint scope)", compliance=ComplianceStatus.DEV),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Nozzles", units="—", data_sheet_required="SA-312-TP304", vendor_offer="SA-182-F304", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Flanges", units="—", data_sheet_required="SA-182-F304", vendor_offer="SA-182-F304", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Pipe (downcomers)", units="—", data_sheet_required="SA-312-TP304", vendor_offer="B31.3 SS piping", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Gaskets", units="—", data_sheet_required="Spiral wound 0.125\" with appropriate filler", vendor_offer="Not specifically stated", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="External Surface Prep", units="—", data_sheet_required="Per 22510-SP-ME003", vendor_offer="Two-coat paint on CS skirt/baseplate only", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="MATERIALS OF CONSTRUCTION", parameter="Paint", units="—", data_sheet_required="NOT REQUIRED (all-SS)", vendor_offer="Two-coat (CS portions only)", compliance=ComplianceStatus.OK),
    # ATTACHMENTS
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Demister (mesh pad)", units="—", data_sheet_required="YES (12\" 304SS, 9#)", vendor_offer="Installation by BWFS (free issue by Crosstrails — Rev 3)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Demister Supports", units="—", data_sheet_required="YES", vendor_offer="Implied with chimney/tray install", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Pipe Downcomers", units="—", data_sheet_required="YES (for DNCM nozzles N1–N9)", vendor_offer="Included as Option (priced)", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Pipe Support / Guide Clips", units="—", data_sheet_required="YES", vendor_offer="Included", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Lift Lugs / Trunnions", units="—", data_sheet_required="YES (lift lugs)", vendor_offer="(2) 14\" lifting trunnions w/ donut ring; tailing lug", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Insulation Supports / Rings", units="—", data_sheet_required="YES (rings only — insulation by others)", vendor_offer="Insulation support rings INCLUDED", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="EXTERNAL & INTERNAL ATTACHMENTS", parameter="Tailing Lugs", units="—", data_sheet_required="YES", vendor_offer="INCLUDED", compliance=ComplianceStatus.OK),
    # NOZZLE SCHEDULE
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N1 Vapor Outlet", units="—", data_sheet_required='1 × 8" 300# RFWN, DNCM', vendor_offer='1 × 8" 300# RFWN, DNCM', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N2 Reflux", units="—", data_sheet_required='1 × 4" 300# RFWN, DNCM W/baffle', vendor_offer='1 × 4" 300# RFWN, DNCM W/baffle', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N3 Feed", units="—", data_sheet_required='1 × 8" 300# RFWN, DNCM W/baffle', vendor_offer='1 × 8" 300# RFWN, DNCM W/baffle', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N4 Liquid Outlet", units="—", data_sheet_required='1 × 8" 300# RFWN W/VB (vortex breaker)', vendor_offer='1 × 8" 300# RFWN W/VB (vortex breaker)', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="N5 Side Draw", units="—", data_sheet_required='1 × 16" 300# RFWN, DNCM', vendor_offer='1 × 16" 300# RFWN, DNCM', compliance=ComplianceStatus.OK),
    TechnicalParameter(category="NOZZLE SCHEDULE", parameter="MW1 Manway (Fill)", units="—", data_sheet_required='4 × 18" 300# RFWN W/B&D (blind + davit)', vendor_offer='4 × 18" 300# RFWN W/B&D (blind + davit)', compliance=ComplianceStatus.OK),
    # INTERNALS
    TechnicalParameter(category="INTERNALS", parameter="All Internals", units="—", data_sheet_required="Free issue by client — installed by Fabricator", vendor_offer="Included", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="INTERNALS", parameter="Chimney Trays", units="—", data_sheet_required="Fully welded", vendor_offer="Included", compliance=ComplianceStatus.OK),
    TechnicalParameter(category="INTERNALS", parameter="Support Rings", units="—", data_sheet_required="Installed by Fabricator", vendor_offer="Included", compliance=ComplianceStatus.OK),
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
    recommendation=None,  # left for user / future scoring
    created_at="2026-06-17",
    last_updated="2026-08-12 (Demo load)"
)
