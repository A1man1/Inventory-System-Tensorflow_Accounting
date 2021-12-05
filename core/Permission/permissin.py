class _Permission:
    LEGER={2:'create_leger_book', 4:"create_leger_page", 6:"edit_leger_book", 8:"edit_leger_page", 10:"delete_leger_page", 12:"delete_leger_book", 14:"view_leger_page" , 16:"view_leger_book"}
    ACCOUNT_ROLE_HANDLING={48:"create_user", 50:"edit_user",52:"view_user",53:"create_role", 54:"view_role", 56:"assign_role", 58:"view_permission",60:"assgin_permission"}
    PRODUCTS=  {18:"create_product",20:"view_product",22:"delete_product",24:"edit_product"}
    SUPPILERS= {32:"create_suppiler",34:"view_suppiler",36:"delete_suppiler",38:"edit_suppiler"}
    ORDERS=    {40:"create_order",42:"view_order",44:"delete_order",46:"edit_order"}
    PURCHASE=  {26:"create_purchase",27:"view_purchase",28:"delete_purchase",30:"edit_purchase"}
    COMPANY=   {55:"edit_company"}
    __all_over= dict.update(LEGER)
    __all_over= dict.update(ACCOUNT_ROLE_HANDLING)
    __all_over= dict.update(PRODUCTS)
    __all_over= dict.update(ORDERS)
    __all_over= dict.update(PURCHASE)
    __all_over= dict.update(SUPPILERS)
    __all_over=dict.update(COMPANY)

class _Schema_Admin():
    def __init__(self) -> None:
        super().__init__()
    
    def admin_permit(self):
        return 'd'
    def Schema_name(self):
        return "SUPER_ADMIN"

class userAdmin(_Permission):
    def __init__(self) -> None:
        super().__init__()


