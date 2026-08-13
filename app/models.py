"""
Core data models for the PO Bid Tab Agent.
Based on real RFQ M001 (T-2100 Demethanizer) structure.
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import date
from enum import Enum


class ComplianceStatus(str, Enum):
    OK = "OK"
    DEV = "Dev"
    CLARIFY = "Clarify"
    NOT_ADDRESSED = "Not Addressed"


class VendorInfo(BaseModel):
    name: str
    proposal_number: str
    proposal_date: Optional[str] = None
    revision: Optional[str] = None
    sales_contact: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    shop_location: Optional[str] = None
    fob: Optional[str] = None
    asme_stamp: Optional[str] = None
    notes: Optional[str] = None


class PricingLine(BaseModel):
    item: str
    description: str
    amount_usd: float
    is_optional: bool = False
    notes: Optional[str] = None


class CommercialTerms(BaseModel):
    delivery_weeks: Optional[str] = None
    pricing_validity: Optional[str] = None
    payment_terms: Optional[str] = None
    warranty: Optional[str] = None
    cancellation_schedule: Optional[str] = None
    taxes: Optional[str] = None
    tariff_disclaimer: Optional[str] = None
    storage: Optional[str] = None
    notes: Optional[str] = None


class TechnicalParameter(BaseModel):
    category: str  # e.g. "GENERAL", "DESIGN DATA", "MATERIALS", "NOZZLE SCHEDULE"
    parameter: str
    units: Optional[str] = None
    data_sheet_required: str
    vendor_offer: str
    compliance: ComplianceStatus = ComplianceStatus.OK
    notes: Optional[str] = None


class VendorQuote(BaseModel):
    vendor: VendorInfo
    pricing_lines: List[PricingLine] = Field(default_factory=list)
    commercial: CommercialTerms = Field(default_factory=CommercialTerms)
    technical: List[TechnicalParameter] = Field(default_factory=list)
    raw_text_excerpt: Optional[str] = None  # for review screen
    extraction_confidence: Optional[float] = None
    needs_review: bool = False
    review_notes: Optional[str] = None


class RFQPackage(BaseModel):
    project_name: str
    project_number: str
    location: str
    owner: str
    engineer_buyer: str
    rfq_number: str
    equipment_tag: str
    equipment_description: str
    data_sheet_ref: str
    bid_tab_rev: str = "Rev 0"
    bid_tab_date: Optional[str] = None
    notes: Optional[str] = None


class BidTab(BaseModel):
    rfq: RFQPackage
    vendors: List[VendorQuote] = Field(default_factory=list)
    apples_to_apples_notes: Optional[str] = None
    recommendation: Optional[str] = None
    created_at: Optional[str] = None
    last_updated: Optional[str] = None


# Convenience helpers for totals
def calculate_apples_to_apples(quote: VendorQuote, include_optional: bool = False) -> float:
    """Sum base vessel + downcomers + base ladders (excludes pure options unless flagged)."""
    total = 0.0
    for line in quote.pricing_lines:
        if line.is_optional and not include_optional:
            continue
        # Heuristic: include lines that are core or base accessories
        desc_lower = line.description.lower()
        if any(k in desc_lower for k in ["base vessel", "tower", "column", "downcomer", "ladder", "platform", "fall arrest"]):
            if "optional" in desc_lower or "option" in desc_lower or "field hydro" in desc_lower:
                if not include_optional:
                    continue
            total += line.amount_usd
    return total
