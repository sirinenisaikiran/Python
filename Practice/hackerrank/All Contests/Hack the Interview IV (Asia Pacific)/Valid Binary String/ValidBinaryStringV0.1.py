# s = input()
# d = input()
# d = int(d)

s = '0000'
d = 2

#print('Binary String {}' .format(s))
#print('The integer {}' .format(d))

s_len = len(s)
# print('Binary String length {}' .format(s_len))
sub_str=''
sub_str_list=[]
for i in range(s_len):
    sub_str=''
    if i + d <= s_len:
        for j in range(d):
            sub_str += s[i+j]
            #print("i={} d={} s_len={} j={}" .format(i,d,s_len,j))
        sub_str_list.append(sub_str)
        #print('Binary Sub String {}' .format(sub_str))
print(sub_str_list)

sub_str_list_wg = []
for i in sub_str_list:
    sub_str_list_wg.append(i.count('1'))
print(sub_str_list_wg)

# count = 0
# for ss in sub_str_list:
    # if ss.count('1') == 0:
        # count +=1

# print(count)