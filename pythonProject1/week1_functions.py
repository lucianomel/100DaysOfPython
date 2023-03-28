class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        if len(s)!=len(t):
            return False
        dic={}
        for i,char in enumerate(s):
            if(char in dic and dic[char]==t[i]):
                continue
            elif (char in dic):
                #s[i] in dic is already defined and t[i] doesn't hold same char than in dic
                return False
            else:
                dic[char]=t[i]
        return True