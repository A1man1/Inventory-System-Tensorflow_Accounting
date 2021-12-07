import locale
from typing import List
import numpy as np
from forex_python.converter import CurrencyRates


class Util:
    def __init__(self) -> None:
        
        self.EMPTY = ''
 
        self.X = [self.EMPTY, 'One ', 'Two ', 'Three ', 'Four ', 'Five ', 'Six ', 'Seven ',
        'Eight ', 'Nine ', 'Ten ', 'Eleven ', 'Twelve ', 'Thirteen ', 'Fourteen ',
        'Fifteen ', 'Sixteen ', 'Seventeen ', 'Eighteen ', 'Nineteen ']
 
        self.Y = [self.EMPTY, self.EMPTY, 'Twenty ', 'Thirty ', 'Forty ', 'Fifty ',
        'Sixty ', 'Seventy ', 'Eighty ', 'Ninety ']
        self.currency = CurrencyRates()
    
    # Function to convert a single-digit or two-digit number into words
    def convertToDigit(self,n, suffix):
        # if `n` is zero
        if n == 0:
            return self.EMPTY
    
        # split `n` if it is more than 19
        if n > 19:
            return self.Y[n // 10] + self.X[n % 10] + suffix
        else:
            return self.X[n] + suffix
    
    def convertToDigitInter(self,n, suffix):
        # if `n` is zero
        if n == 0:
            return self.EMPTY
    
        # split `n` if it is more than 19
        if len(str(n)) == 3:
                #print((n // 10) %10)
                return self.X[n//100] + 'Hunderd '+ self.Y[(n // 10 )% 10] + self.X[n % 10] + suffix 
        elif len(str(n)) == 2:
            return self.Y[n // 10] + self.X[n % 10] + suffix
        else:
            return self.X[n] + suffix


    # Function to convert a given number (max 9-digits) into words
    def convert_indin_place_value(self,n):

        result = self.convertToDigit((n // pow(10,25)) % 100, 'Ogha, ')

        result += self.convertToDigit((n // pow(10,23)) % 100, 'Samudra, ')

        result += self.convertToDigit((n // pow(10,21)) % 100, 'Kharva, ')

        result += self.convertToDigit((n // pow(10,19)) % 100, 'Padma, ')
        
        # add digits at ten million and hundred million place
        result += self.convertToDigit((n // pow(10,17)) % 100, 'Vrinda, ')

        # add digits at ten million and hundred million place
        result += self.convertToDigit((n // pow(10,13)) % 100, 'Shankh, ')

        # add digits at ten million and hundred million place
        result += self.convertToDigit((n // pow(10,11)) % 100, 'Karab, ')

        # add digits at ten million and hundred million place
        result += self.convertToDigit((n // pow(10,9)) % 100, 'Arab, ')
    
        # add digits at ten million and hundred million place
        result += self.convertToDigit((n // pow(10,7)) % 100, 'Crore, ')
    
        # add digits at hundred thousand and one million place
        result += self.convertToDigit(((n // pow(10,5)) % 100), 'Lakh, ')
    
        # add digits at thousand and tens thousand place
        result += self.convertToDigit(((n // 1000) % 100), 'Thousand, ')
    
        # add digit at hundred place
        result += self.convertToDigit(((n // 100) % 10), 'Hundred ')
    
        if n > 100 and n % 100:
            result += 'and '
    
        # add digits at ones and tens place
        result += self.convertToDigit((n % 100), '')
    
        return result.strip().rstrip(',').replace(', and', ' and')


        # Function to convert a given number (max 9-digits) into words
    def convert_international_place_value(self,n):
        """Grenrating Internation place value standard by giving numerical currency

        Args:
            n ([integer, float]): numerical value

        Returns:
            [String]:  readable sequnce of currency as e.g (450,030,004)->Forty Five Million, Thiry Thousand, and Four
        """
        result = self.convertToDigitInter((n // pow(10,36)) % 1000, 'novemdecillion, ')
        result += self.convertToDigitInter((n // pow(10,33)) % 1000, 'octodecillion, ')
        result += self.convertToDigitInter((n // pow(10,30)) % 1000, 'quattuordecillion, ')
        result += self.convertToDigitInter((n // pow(10,27)) % 1000, 'tredecillion, ')
        result += self.convertToDigitInter((n // pow(10,24)) % 1000, 'Nonillion, ')
        result += self.convertToDigitInter((n // pow(10,21)) % 1000, 'Octillion, ')
        result += self.convertToDigitInter((n // pow(10,18)) % 1000, 'Sextillion, ')
        # add digits at ten million and hundred million place
        result += self.convertToDigitInter((n // pow(10,15)) % 1000, 'Quadrillion, ')
        # add digits at ten million and hundred million place
        result += self.convertToDigitInter((n // pow(10,12)) % 1000, 'Trillion, ')
        # add digits at ten million and hundred million place
        result += self.convertToDigitInter((n // pow(10,9)) % 1000, 'Billion, ')
        # add digits at hundred thousand and one million place
        result += self.convertToDigitInter(((n // pow(10,6)) % 1000), 'Million, ')
        # add digits at thousand and tens thousand place
        result += self.convertToDigitInter(((n // 1000) % 1000), 'Thousand, ')        
        # add digit at hundred place
        result += self.convertToDigitInter(((n // 100) % 10), 'Hundred ')
    
        if n > 100 and n % 100:
            result += 'and '
    
        # add digits at ones and tens place
        result += self.convertToDigitInter((n % 100), '')    
        return result.strip().rstrip(',').replace(', and', ' and')                  

    def number_representation(self,num, system='en_IN')->str:
        locale.setlocale(locale.LC_MONETARY, system)
        return locale.currency(num, symbol=True, grouping=True)     

    def currency_conversion(self,base_currency,destination_currency):
        return self.currency.get_rate(base_cur=base_currency,dest_cur=destination_currency)

    def big_float_average(self,data:List[int]):
        return np.average(a=data)
        
    def big_float_subtraction(self, a:float, b:float)->float:
        return np.subtract(a,b)

    def big_float_addition(self, a:List[float])->float:
        return np.sum(a)

    def big_float_division(self,a:float , b:float)->float:
        return np.divide(a,b)

    def big_float_divmod(self,a:float , b:float)->float:
        return np.divmod(a,b)

    def big_float_multipilcaiton(self,a:List[float] , b:List[float])->float:
        return np.matmul(a,b)
