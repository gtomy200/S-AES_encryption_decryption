#Function creating the array of plaintext
def arr(text):
    plain_text_array = list()
    count = 0
    strg = ' '
    first_time = 'Y'
    for value in text:
        if value != ' ':
            if count <= 3:
                if first_time == 'Y':
                    strg = value
                    first_time = 'N'
                    count += 1
                else:
                    strg = strg + value
                    count += 1
            else:
                plain_text_array.append(strg)
                count = 1
                strg = value
        else:
            count += 1
            pass
    plain_text_array.append(strg)
    return(plain_text_array)

#Function generating substitute keys
def keygen():
    w0 = key[0:8]
    w1 = key[8:]
    s_box_var1, s_box_var2 = rot_nib(w1)
    output = s_box(s_box_var1, s_box_var2)
    temp_str = output[0] + output [1]
    temp_w = int(w0,2) ^ 0b10000000 ^ int(temp_str,2) 
    w2 = format(temp_w, '08b')
    temp_w1 = int(w2, 2) ^ int(w1,2)
    w3 = format(temp_w1,'08b')
    key1 = w2+w3
    s_box_var1, s_box_var2 = rot_nib(w3)
    output = s_box(s_box_var1, s_box_var2)
    temp_str = output[0] + output [1]
    temp_w = int(w2,2) ^ 0b00110000^ int(temp_str,2)
    w4 = format(temp_w, '08b')
    temp_w1 = int(w4, 2) ^ int(w3,2)
    w5 = format(temp_w1,'08b')
    key2 = w4+w5
    return (key1, key2)

#Function for s-box    
def s_box(*a):
    dict_box = {'0000':'1001', '0001':'0100', '0010':'1010', '0011':'1011', '0100':'1101', '0101':'0001', '0110':'1000', '0111':'0101', '1000':'0110', '1001':'0010', '1010':'0000', '1011':'0011', '1100':'1100', '1101':'1110', '1110':'1111', '1111':'0111'}
    element = [dict_box[i] for i in a]
    return(element)

#Function for rotating the nibbles
def rot_nib(var):
    temp_str = var[0:4]
    temp_str1 = var[4:] + temp_str
    temp_str = temp_str1[0:4]
    var = temp_str1[4:]
    return(temp_str,var)
    
#Function for the checking length of plain text and key
def chk_length(strng):
    strg = ' '
    first_time = 'Y'
    for value in strng:
        if value != ' ':
            if first_time == 'Y':
                strg = value
                first_time = 'N'
            else:
                strg = strg + value
        else:
            pass
    return(len(strg), strg)

#Function for the state matix XOR operation
def matrix_operation(state_matrix,key):
    key_array = list()
    count = 0
    first_time = 'Y'
    for value in key:
           if count <= 3:
              if first_time == 'Y':
                    strg = value
                    first_time = 'N'
                    count += 1
              else:
                  strg = strg + value
                  count += 1
           else:
               key_array.append(strg)
               count = 1
               strg = value
    key_array.append(strg)
    temp_text = key_array[2]
    key_array[2] = key_array[1]
    key_array[1] = temp_text
    s00 = format(int(state_matrix[0],2) ^ int(key_array[0],2), '04b')
    state_matrix[0]= s00 
    s01 = format(int(state_matrix[1],2) ^ int(key_array[1],2), '04b')
    state_matrix[1] = s01
    s10 = format(int(state_matrix[2],2) ^ int(key_array[2],2), '04b')
    state_matrix[2] = s10
    s11 = format(int(state_matrix[3],2) ^ int(key_array[3],2), '04b')
    state_matrix[3] = s11

    return (state_matrix)

#Round 0 function
def round0():
       temp_text = plain_text_array[2]
       plain_text_array[2] = plain_text_array[1]
       plain_text_array[1] = temp_text
       state_matrix = matrix_operation(plain_text_array,key)

       return (state_matrix)

#Round 1 function
def round1():
    state_matrix = s_box(round0_output[0], round0_output[1], round0_output[2], round0_output[3])
    temp_text = state_matrix[2]
    state_matrix[2] = state_matrix[3]
    state_matrix[3] = temp_text
    state_matrix = mix_column(state_matrix)
    state_matrix = matrix_operation(state_matrix,key1)

    return (state_matrix)

#Round 2 function
def round2():
    state_matrix = s_box(round1_output[0], round1_output[1], round1_output[2], round1_output[3])
    temp_text = state_matrix[2]
    state_matrix[2] = state_matrix[3]
    state_matrix[3] = temp_text
    state_matrix = matrix_operation(state_matrix,key2)

    return (state_matrix)

#mix column function
def mix_column (temp_matrix):
    state_matrix = list()
    mult_matrix = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15],[0,2,4,6,8,10,12,14,3,1,7,5,11,9,15,13],
                   [0,3,6,5,12,15,10,9,11,8,13,14,7,4,1,2],[0,4,8,12,3,7,11,15,6,2,14,10,5,1,13,9],[0,5,10,15,7,2,13,8,14,11,4,1,9,12,3,6],
                   [0,6,12,10,11,13,7,1,5,3,9,15,14,8,2,4],[0,7,14,9,15,8,1,6,13,10,3,4,2,5,12,11],[0,8,3,11,6,14,5,13,12,4,15,7,10,2,9,1],
                   [0,9,1,8,2,11,3,10,4,13,5,12,6,15,7,14],[0,10,7,13,14,4,9,3,15,5,8,2,1,11,6,12],[0,11,5,14,10,1,15,4,7,12,2,9,13,6,8,3],
                   [0,12,11,7,5,9,14,2,10,6,1,13,15,3,4,8],[0,13,9,4,1,12,8,5,2,15,11,6,3,14,10,7],[0,14,15,1,13,3,2,12,9,7,6,8,4,10,11,5],
                   [0,15,13,2,9,6,4,11,1,14,12,3,8,7,5,10]]
    mix_column_matrix = [1 , 4 , 4, 1]
    s00 = format(mult_matrix[mix_column_matrix[0]][int(temp_matrix[0],2)] ^ mult_matrix[mix_column_matrix[1]][int(temp_matrix[2],2)],'04b')
    state_matrix.append(s00)
    s01 = format(mult_matrix[mix_column_matrix[0]][int(temp_matrix[1],2)] ^ mult_matrix[mix_column_matrix[1]][int(temp_matrix[3],2)],'04b')
    state_matrix.append(s01)
    s10 = format(mult_matrix[mix_column_matrix[2]][int(temp_matrix[0],2)] ^ mult_matrix[mix_column_matrix[3]][int(temp_matrix[2],2)],'04b')
    state_matrix.append(s10)
    s11 = format(mult_matrix[mix_column_matrix[2]][int(temp_matrix[1],2)] ^ mult_matrix[mix_column_matrix[3]][int(temp_matrix[3],2)],'04b') 
    state_matrix.append(s11)
    return (state_matrix)

#Plain text input     
plain_text = input('Enter the binary plain_text: ')

#Checking the input length
length,strg = chk_length(plain_text)
if length != 16:
    print ('Enter a valid plaintext of length  16 bits')
    quit()
binary_input = all(i in '0,1' for i in strg)

#Checking the input to be binary
if binary_input == False:
    print ('Enter a valid binary plaintext of length  16 bits')
    quit()
    
#creating a list of the plain text input    
plain_text_array = arr(plain_text)

#Key Input
key = input('Enter the binary key: ')

#Checking the key length
length,key = chk_length(key)
if length != 16:
    print ('Enter a valid key of length  16 bits')
    quit()

#Checking the key to be binary    
binary_input = all(i in '0,1' for i in key)
if binary_input == False:
    print ('Enter a valid binary key of length  16 bits')
    quit()

#function to generate substitute keys.    
key1,key2=keygen()
#Round 0
round0_output = round0()
#Round 1
round1_output = round1()
#Round 2
round2_output = round2()
#Output Ciphertext
print('The ciphertext is: '+ round2_output[0]+' ' + round2_output[2]+' '+ round2_output[1]+' '+round2_output[3])


