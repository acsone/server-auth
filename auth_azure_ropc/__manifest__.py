# Copyright 2023 ACSONE SA/NV
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Auth Azure ROPC",
    "summary": """
        Allow to login with azure using ROPC flow""",
    "version": "16.0.1.0.0",
    "license": "AGPL-3",
    "author": "ACSONE SA/NV,Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/server-auth",
    "depends": ["base"],
    "data": [
        "security/azure_ropc_provider.xml",
        "views/azure_ropc_provider.xml",
    ],
}
