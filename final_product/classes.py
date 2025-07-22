from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


class PartyInfo(BaseModel):
    name: str
    personal_code: Optional[str] = Field(None, alias="asmens_kodas")
    individual_activity_certificate_number: Optional[str] = Field(
        None, alias="individualios_veiklos_pazymejimo_numeris"
    )
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None

class ServiceItem(BaseModel):
    description: str
    quantity: float
    unit: str
    price_per_unit: float
    total: float

class Invoice(BaseModel):
    invoice_number: str = Field(..., alias="saskaitos_numeris")
    invoice_date: date = Field(..., alias="data")
    seller: PartyInfo = Field(..., alias="pardavejas")
    buyer: PartyInfo = Field(..., alias="pirkejas")
    services: List[ServiceItem] = Field(..., alias="paslaugos")
    total_amount: float = Field(..., alias="bendra_suma")
    vat: Optional[float] = Field(None, alias="pvm")
    amount_in_words: Optional[str] = Field(None, alias="suma_zodziais")
    payment_method: Optional[str] = Field(None, alias="apmokejimo_budas")
    payment_term: Optional[str] = Field(None, alias="apmokejimo_terminas")
    signature: Optional[str] = Field(None, alias="parasas")
