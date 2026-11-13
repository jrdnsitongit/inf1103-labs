class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str) -> None:
        if not isinstance(supplier_id, str) or not supplier_id.strip():
            raise ValueError("Supplier ID cannot be empty.")
        if not isinstance(name, str) or not name.strip():
            raise ValueError("Supplier name cannot be empty.")
        if not isinstance(contact_email, str) or not self._is_valid_email(contact_email.strip()):
            raise ValueError("Invalid supplier email format.")        
             
        self.__supplier_id: str = supplier_id
        self.__name: str = name
        self.__contact_email: str = contact_email
    @staticmethod
    def _is_valid_email(email: str) -> bool:
        if " " in email or "@" not in email:
            return False
        local_part, _, domain_part = email.partition("@")
        return bool(
            local_part
            and "." in domain_part
            and not domain_part.startswith(".")
            and not domain_part.endswith(".")
        )
    def display_information(self) -> None:
        print(f"Supplier: {self.__name} (ID: {self.__supplier_id}) | Email: {self.__contact_email}")

    def to_dict(self) -> dict:
        return {"supplier_id": self.__supplier_id, "name": self.__name,
                "contact_email": self.__contact_email}