import json

dict_HLR_op_code={}
dict_HLR_op_code_new={}
with open('HLR.json') as f:
	dict_HLR_op_code = json.load(f)
HLR_to_op={'aircel':'1','bsnl':'3','airtel':'28','vodafone':'22','docomo':'17','reliance':'13','idea':'8','uninor':'19','videocon':'5'}
op_code_map={'1':'AL','3':'BS','28':'AT','8':'IDX','10':'MS','12':'RL','13':'RG','17':'TD','19':'UN','5':'VD','22':'VF'}
for mccmnc in dict_HLR_op_code:
	lookup_query=dict_HLR_op_code[mccmnc]
	for op in HLR_to_op:
		if op in lookup_query:
			dict_HLR_op_code_new[mccmnc]=op_code_map[HLR_to_op[op]]
		
print dict_HLR_op_code_new
