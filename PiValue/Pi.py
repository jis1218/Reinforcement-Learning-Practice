# coding: utf-8
'''
Created on 2018. 5. 2.

@author: Insup Jung
'''

import random

cnt=0

for i in range(1000000):
    x = random.uniform(0,1)
    y = random.uniform(0,1)
    
    if x*x + y*y <=1:
        cnt += 1
        

print(4*cnt/1000000)



