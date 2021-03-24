import setuptools

setuptools.setup(
    setup_requires=["setuptools-odoo"],
    odoo_addon={
        "external_dependencies_override": {
            "python": {
                "jose": [
                    "python-jose[cryptography]",
                    "rsa<4.1",  # 4.0 was the last to support python 2
                ],
            }
        }
    },
)
