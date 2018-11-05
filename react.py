class Particle:

    def __init__(self, sym, chg, massNumber):
        self.sym = sym
        self.chg = chg
        self.massNumber = massNumber

    def __str__(self):
      
        return self.sym

    def __repr__(self):
        className = self.__class__.__name__
        
        return "{}({!r}, {!r}, {!r})".format(
            className, self.sym, self.chg, self.massNumber)
    
    
    def __add__(self,other):
    
        if (not isinstance(other,tuple)):
           
            result = [self] + [other]
        else:
            result = list(other) + [self]
        return tuple(list(result))
    
        
    def __radd__(self,other):  
        
        return self.__add__(other)
    
    
    def __rmul__(self,other):  
        
        result = self
        for i in range(1,other):
            result = result + self 
        return result

class Nucleus(Particle):

    def __str__(self):
        
        return "({}){}".format(self.massNumber, self.sym)


class UnbalancedCharge(Exception):
    
    def __init__(self,diff):
        print("Unbalanced Charge here: ",diff)
        
class UnbalancedNumber(Exception):
    
    def __init__(self,diff):
        print("Unbalanced Mass Number here: ",diff)

class Reaction:
    
    def __init__(self, t1, t2):
        self.t1 = t1
        self.t2 = t2
      
    def __str__(self):
      
        left_hand_chg = 0
        right_hand_chg = 0
        
        left_hand_massNumber = 0
        right_hand_massNumber = 0
        format_left = ""
        format_right = ""
        format_list = []
        
        for index,nucleus in enumerate(self.t1):
            len_t1 = len(self.t1)
            left_hand_chg = left_hand_chg + self.t1[index].chg
            left_hand_massNumber = left_hand_massNumber + self.t1[index].massNumber
            if index == (len_t1-1):
                format_left = format_left + "{}" 
            else:
                format_left = format_left + "{} + "
            format_list = format_list + [self.t1[index]]
            
        for index,nucleus in enumerate(self.t2):
           
            right_hand_chg = right_hand_chg + self.t2[index].chg
            right_hand_massNumber = right_hand_massNumber + self.t2[index].massNumber
            len_t2 = len(self.t2)
            if index == (len_t2-1):
                format_right = format_right + "{}" 
            else:
                format_right = format_right + "{} + "
                
            format_list = format_list + [self.t2[index]]
        
        if left_hand_chg != right_hand_chg:
           
            raise UnbalancedCharge(right_hand_chg - left_hand_chg)
              
                   
        elif left_hand_massNumber != right_hand_massNumber:
             raise UnbalancedNumber(right_hand_massNumber - left_hand_massNumber)
        
        format_final = format_left + " -> "+ format_right
        
        return format_final .format(*format_list)

class ChainReaction:
    
    
    def __init__(self, name):
        self.name = name
        print(name)
        self.left_part=list()
        self.right_part=list()
        
        self.total_left_part=list()
        self.total_right_part=list()
        self.reac_final = ''
        
    def addReaction(self, rctn):
        
        for i in rctn.t1:
            self.left_part.append(i)
            self.total_left_part.append(str(i))
            
        for i in rctn.t2:
            self.right_part.append(i)
            self.total_right_part.append(str(i))
            
        self.reac_final =  self.reac_final + str(rctn) + '\n'
    
    def __repr__(self):
        
        total_left_part=list(self.total_left_part)
        total_right_part=list(self.total_right_part)

        for i in total_left_part:
           
            if i in self.total_right_part:
                pop_1=self.total_left_part.index(i)
                pop_2=self.total_right_part.index(i)
                self.left_part.pop(pop_1)
                self.total_left_part.pop(pop_1)
                self.right_part.pop(pop_2)
                self.total_right_part.pop(pop_2)
        
        print(self.reac_final,"net:")
        
        return str(Reaction(self.left_part,self.right_part))
        
        

if __name__ == "__main__":
    
    em = Particle("e-", -1, 0)       # an electron
    ep = Particle("e+", 1, 0)        # a positron
    p = Particle("p", 1, 1)          # a proton
    n = Particle("n", 0, 1)          # a neutron
    nu_e = Particle("nu_e", 0, 0)    # a neutrino
    gamma = Particle("gamma", 0, 0)  # a gamma particle
    d = Nucleus("H", 1, 2)    # hydrogen
    li6 = Nucleus("Li", 3, 6) # lithium
    he4 = Nucleus("He", 2, 4) # helium
    he3 = Nucleus("He", 2, 3) 
    chnPP = ChainReaction("proton -proton (branch I)")
    for rctn in (Reaction((p, p), (d, ep, nu_e)),
                 Reaction((p, p), (d, ep, nu_e)), 
                 Reaction((d, p), (he3, gamma)), 
                 Reaction((d, p), (he3, gamma)), 
                 Reaction((he3, he3), (he4, p, p))):
        chnPP.addReaction(rctn)
    
    print(chnPP)
    
    
    
    