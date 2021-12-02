import locale

class Util:
    def __init__(self) -> None:
        self.basic_num=['zero' , 'one', 'two' , 'three' , 'four' , 'five' , 'six', 'seven', 'eight' ,'nine' ]
        self.tens_num = ['ten', 'eleven', 'twelve' , 'thirteen' , 'fourteen' 
        , 'fifteen' , 'sixteen', 'seventeen', 'eighteen' , 'ninteen' ]
        self.tens=[ 'twenty','thirty', 'fourty' , 'fifty', 'sixty', 'seventy', 'eighty', 'ninty' ]
        self.arab = 'arab'
        self.place_val_ind=['thousand' ,'lakh', 'corer','arab','kharab' , 'neel' , 'pdma' , 'shankh']
        self.hunders = 'hunderd' 
        self.place_val_inter = ['thousand','million', 'billion', 'trillion', 'quadrillion', 'quintillion']
         

    def _util_place_val_(self,num:str):
        word=''
        last_digit = int(num[-1])
        check_tens = int(num[-2])
        
        if  check_tens == 0:
            word+=self.basic_num[num]
            #print('0')
            
        elif check_tens == 1:
            word+=self.tens_num[int(str(check_tens)+num[-1])-10]
            #print('1')
            
        elif check_tens > 1 and last_digit == 0:
            word+=self.tens[check_tens-2]+" "
            #print('2')
            
        elif check_tens > 1 and last_digit > 0:
            #print('3')
            word+=self.tens[check_tens-2]+" "+self.basic_num[last_digit]
        
        return word

    def num2word(self,num:int,country:str)->str:
        word =''
        word_inner , word_outer='' ,''
        length = len(num)
        ineer_count , outer_count, nums = 0 , 0 , str(num)
        
        if length <=2:
           return self._util_place_val_ind(str(num))
           
        check_hunderd = int(nums[-3])
        
       
           
        word+=self._util_place_val_(str(num))
        
        if length >=3:
            word=self.basic_num[check_hunderd]+" "+self.hunders+" "+self._util_place_val_(str(num))
            if length == 3:
                return self.basic_num[check_hunderd]+" "+self.hunders+" "+self._util_place_val_(str(num))+" "
            
            elif length > 3:
                if country.lower() == 'india':
                    len_=len(list(nums))-4 
                    for nu in range(len_,-1,-2):
                        if nu == 0:
                            if len_%2 == 0:
                                word_outer+=self.basic_num[int(nums[nu])]+" "+self.place_val_[ineer_count]+" "
                                break
                            
                        word_inner=self._util_place_val_(str(nums[nu-1])+str(nums[nu]))+" "+self.place_val_[ineer_count]+" "+word_inner   
                        ineer_count+=1
                
                    return word_outer+word_inner+word
                else:
                    len_=len(list(nums))-4 
                    for nu in range(len_,-1,-3):
                        if nu == 0:
                            word_outer+=self.basic_num[int(nums[nu])]+" "+self.hunders+" "+self._util_place_val_(str(nums[nu+1])+str(nums[nu+2]))+" "+self.place_val_inter[ineer_count]+" "
                            break
                            
                        word_inner=self.basic_num[int(nums[nu])]+" "+self.hunders+" "+self._util_place_val_(str(nums[nu+1])+str(nums[nu+2]))+" "+self.place_val_inter[ineer_count]+" "+word_inner   
                        ineer_count+=1
                
                    return word_outer+word_inner+word
                
    
    def international_num2word(num:float)->str:
        pass
    
    def number_representation(num:float, system='en_IN')->str:
        if system == 'en_IN':
            return locale.currency(num, grouping=True,international=False)
        return locale.currency(num, grouping=True,international=True) 