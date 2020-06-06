import os
# Dict = os.environ
# for i in Dict:
    # print("{} {}".format(i, Dict[i]))


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    # n = int(input())

    # scores = list(map(int, input().rstrip().split()))

    # result = breakingRecords(scores)

    # print(' '.join(map(str, result)))
    fptr.write("Welcome to python")
    fptr.write('\n')

    fptr.close()