import json
{
  "title": "Invoice",
  "type": "object",
  "properties": {
    "saskaitos_numeris": {
      "title": "Saskaitos Numeris",
      "type": "string"
    },
    "data": {
      "title": "Data",
      "type": "string",
      "format": "date"
    },
    "pardavejas": {
      "$ref": "#/definitions/PartyInfo"
    },
    "pirkejas": {
      "$ref": "#/definitions/PartyInfo"
    },
    "paslaugos": {
      "title": "Paslaugos",
      "type": "array",
      "items": {
        "$ref": "#/definitions/ServiceItem"
      }
    },
    "bendra_suma": {
      "title": "Bendra Suma",
      "type": "number"
    },
    "pvm": {
      "title": "Pvm",
      "type": "number"
    },
    "suma_zodziais": {
      "title": "Suma Zodziais",
      "type": "string"
    },
    "apmokejimo_budas": {
      "title": "Apmokejimo Budas",
      "type": "string"
    },
    "apmokejimo_terminas": {
      "title": "Apmokejimo Terminas",
      "type": "string"
    },
    "parasas": {
      "title": "Parasas",
      "type": "string"
    }
  },
  "required": [
    "saskaitos_numeris",
    "data",
    "pardavejas",
    "pirkejas",
    "paslaugos",
    "bendra_suma"
  ],
  "definitions": {
    "PartyInfo": {
      "title": "PartyInfo",
      "type": "object",
      "properties": {
        "name": {
          "title": "Name",
          "type": "string"
        },
        "asmens_kodas": {
          "title": "Asmens Kodas",
          "type": "string"
        },
        "individualios_veiklos_pazymejimo_numeris": {
          "title": "Individualios Veiklos Pazymejimo Numeris",
          "type": "string"
        },
        "address": {
          "title": "Address",
          "type": "string"
        },
        "phone": {
          "title": "Phone",
          "type": "string"
        },
        "email": {
          "title": "Email",
          "type": "string"
        }
      },
      "required": ["name"]
    },
    "ServiceItem": {
      "title": "ServiceItem",
      "type": "object",
      "properties": {
        "description": {
          "title": "Description",
          "type": "string"
        },
        "quantity": {
          "title": "Quantity",
          "type": "number"
        },
        "unit": {
          "title": "Unit",
          "type": "string"
        },
        "price_per_unit": {
          "title": "Price Per Unit",
          "type": "number"
        },
        "total": {
          "title": "Total",
          "type": "number"
        }
      },
      "required": ["description", "quantity", "unit", "price_per_unit", "total"]
    }
  }
}
# This JSON schema defines the structure of an invoice, including details about the seller and buyer, service items, and financial information.