
file1 = 'GOLD_x3mult_t2_output.txt'
file2 = 'x3mult_t2_out.txt'

result_file = 'compare_result.txt'


if __name__ == '__main__':
    origin_output_file = open(file1, "r+")
    # print('reading', new_output_file)
    new_output_file = open(file2, "r+")
    number_of_line = 1
    origin_line = origin_output_file.readline()
    new_line = new_output_file.readline()
    result_file = open(result_file, 'w+')
    flag = 1
    if len(origin_line) == 0:
        print("original file is empty!")
        flag = 0
    if len(new_line) == 0:
        print("new file is empty!")
        flag = 0
    if origin_line is not None and new_line is not None:
        while origin_line:
            if origin_line != new_line:
                result_file.write('two output file are not same! at line %d\n' % number_of_line)
                result_file.write('%s' % origin_line)
                result_file.write('%s' % new_line)
                print('file different! different line is #', number_of_line)
                flag = 0

            else:
                flag = 1
            origin_line = origin_output_file.readline()
            new_line = new_output_file.readline()
            number_of_line += 1
    if flag == 1:
        result_file.write('two file are the same!')
        print('result are the same')
    else:
        print("result are not same!")
    result_file.close()
    origin_output_file.close()
    new_output_file.close()
