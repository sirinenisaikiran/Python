def avg(List):
    sum = 0
    for i in List:
        sum += int(i)
    return (sum/len(List))

nums = input()
List = nums.split(' ')
Res = avg(List)

print("{:0.2f}".format(Res))